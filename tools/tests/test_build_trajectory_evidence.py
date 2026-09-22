from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


TOOLS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS_DIR))

import build_trajectory_evidence as builder  # noqa: E402


class TrajectoryEvidenceBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="trajectory-evidence-test-")
        self.root = Path(self.temp_dir.name)
        self.snapshots = self.root / "captures"
        self.snapshots.mkdir()
        self.make_image("00-source.jpg", (90, 60), (110, 85, 55))
        self.make_image("01-tone.png", (72, 48), (150, 140, 120))
        self.make_image("asset-a-source.png", (44, 30), (20, 60, 100))
        self.make_image("asset-a-tone.png", (44, 30), (40, 90, 140))
        self.make_image("asset-b-tone.jpg", (36, 52), (180, 170, 155))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def make_image(self, name: str, size: tuple[int, int], color: tuple[int, int, int]) -> Path:
        path = self.snapshots / name
        Image.new("RGB", size, color).save(path)
        return path

    def write_manifest(self, steps: list[dict] | None = None) -> Path:
        manifest = {
            "workflow": "test-workflow",
            "status": "awaiting_review",
            "tasks": {
                "PHOTO-TEST": {
                    "task_code": "SB3-TEST-PHO",
                    "title": "Test photo evidence",
                    "intent": "Exercise the evidence builder without creating final artifacts.",
                    "steps": steps
                    or [
                        {
                            "stage": 0,
                            "title": "Source state",
                            "action": "source_inspection",
                            "snapshot": "00-source.jpg",
                            "decision": "Use the supplied source as the baseline.",
                        },
                        {
                            "stage": 1,
                            "title": "Tone pass",
                            "action": "image_apply_auto_tone",
                            "parameters": {},
                            "snapshot": "01-tone.png",
                            "request_id": "request-test-1",
                            "decision": "Keep the neutral automatic tone result for review.",
                        },
                    ],
                }
            },
        }
        path = self.root / "manifest.json"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        return path

    def test_builds_ordered_reports_with_byte_identical_snapshots(self) -> None:
        manifest = self.write_manifest()
        output = self.root / "built" / "trajectory"
        trajectory = builder.build(
            manifest,
            output,
            task_key="PHOTO-TEST",
            snapshots_root=self.snapshots,
            generated_at="2026-01-02T03:04:05Z",
        )

        self.assertEqual(trajectory["task_id"], "SB3-TEST-PHO")
        self.assertEqual([step["stage"] for step in trajectory["trajectory_steps"]], [0, 1])
        self.assertEqual(
            trajectory["trajectory_steps"][1]["snapshot"],
            "trajectory/intermediate/01-tone-pass.png",
        )
        packaged = output / "intermediate" / "01-tone-pass.png"
        self.assertEqual(packaged.read_bytes(), (self.snapshots / "01-tone.png").read_bytes())
        self.assertEqual(
            trajectory["trajectory_steps"][1]["snapshot_evidence"]["sha256"],
            builder.sha256(packaged),
        )
        for name in builder.REPORT_NAMES:
            self.assertTrue((output / name).is_file(), name)
        self.assertTrue((output / builder.MANAGED_MARKER).is_file())
        self.assertIn('src="intermediate/01-tone-pass.png"', (output / "trajectory.html").read_text())
        self.assertIn("![Stage 1: Tone pass](intermediate/01-tone-pass.png)", (output / "trajectory.md").read_text())

    def test_rejects_missing_snapshot_without_publishing_partial_output(self) -> None:
        manifest = self.write_manifest(
            [
                {
                    "stage": 0,
                    "title": "Missing",
                    "action": "source_inspection",
                    "snapshot": "not-there.png",
                    "decision": "This must fail.",
                }
            ]
        )
        output = self.root / "missing" / "trajectory"
        with self.assertRaisesRegex(builder.EvidenceBuildError, "was not found"):
            builder.build(manifest, output, task_key="PHOTO-TEST", snapshots_root=self.snapshots)
        self.assertFalse(output.exists())

    def test_rejects_non_monotonic_stages(self) -> None:
        manifest = self.write_manifest(
            [
                {
                    "stage": 1,
                    "title": "Tone first",
                    "action": "image_apply_auto_tone",
                    "snapshot": "01-tone.png",
                    "decision": "First manifest row.",
                },
                {
                    "stage": 0,
                    "title": "Source second",
                    "action": "source_inspection",
                    "snapshot": "00-source.jpg",
                    "decision": "Out of order on purpose.",
                },
            ]
        )
        with self.assertRaisesRegex(builder.EvidenceBuildError, "strictly increasing"):
            builder.build(
                manifest,
                self.root / "unordered",
                task_key="PHOTO-TEST",
                snapshots_root=self.snapshots,
            )

    def test_rejects_url_and_reused_snapshot_path(self) -> None:
        url_manifest = self.write_manifest(
            [
                {
                    "stage": 0,
                    "title": "Remote",
                    "action": "source_inspection",
                    "snapshot": "https://example.invalid/not-evidence.png",
                    "decision": "Remote files are not accepted.",
                }
            ]
        )
        with self.assertRaisesRegex(builder.EvidenceBuildError, "local file"):
            builder.build(
                url_manifest,
                self.root / "remote",
                task_key="PHOTO-TEST",
                snapshots_root=self.snapshots,
            )

        reused_manifest = self.write_manifest(
            [
                {
                    "stage": 0,
                    "title": "Source",
                    "action": "source_inspection",
                    "snapshot": "00-source.jpg",
                    "decision": "Baseline.",
                },
                {
                    "stage": 1,
                    "title": "Fake second stage",
                    "action": "image_apply_auto_tone",
                    "snapshot": "00-source.jpg",
                    "decision": "The same path must not masquerade as another capture.",
                },
            ]
        )
        with self.assertRaisesRegex(builder.EvidenceBuildError, "reuses the exact snapshot path"):
            builder.build(
                reused_manifest,
                self.root / "reused",
                task_key="PHOTO-TEST",
                snapshots_root=self.snapshots,
            )

    def test_replace_preserves_unmanaged_files(self) -> None:
        manifest = self.write_manifest()
        output = self.root / "replace" / "trajectory"
        builder.build(manifest, output, task_key="PHOTO-TEST", snapshots_root=self.snapshots)
        unmanaged = output / "keep-me.txt"
        unmanaged.write_text("not managed by the builder", encoding="utf-8")

        builder.build(
            manifest,
            output,
            task_key="PHOTO-TEST",
            snapshots_root=self.snapshots,
            replace=True,
        )
        self.assertEqual(unmanaged.read_text(encoding="utf-8"), "not managed by the builder")

    def test_packages_underlying_assets_by_stage_and_links_them_in_reports(self) -> None:
        manifest = self.write_manifest(
            [
                {
                    "stage": 0,
                    "title": "Source state",
                    "action": "source_inspection",
                    "snapshot": "00-source.jpg",
                    "decision": "Establish the source collection.",
                    "asset_snapshots": [
                        {
                            "asset_id": "asset-a",
                            "name": "Asset A source",
                            "path": "asset-a-source.png",
                            "status": "source",
                        }
                    ],
                },
                {
                    "stage": 1,
                    "title": "Tone pass",
                    "action": "image_apply_auto_tone",
                    "snapshot": "01-tone.png",
                    "decision": "Review both toned assets.",
                    "asset_snapshots": [
                        {
                            "asset_id": "asset-a",
                            "name": "Asset A toned",
                            "path": "asset-a-tone.png",
                            "input_url": "https://assets.example.test/a-input",
                            "output_url": "https://assets.example.test/a-output",
                            "request_id": "asset-request-a",
                            "status": "complete",
                            "parameters": {"highlights": -20},
                        },
                        {
                            "asset_id": "asset-b",
                            "name": "Asset B toned",
                            "path": "asset-b-tone.jpg",
                        },
                    ],
                },
            ]
        )
        output = self.root / "assets" / "trajectory"
        trajectory = builder.build(
            manifest,
            output,
            task_key="PHOTO-TEST",
            snapshots_root=self.snapshots,
            generated_at="2026-01-02T03:04:05Z",
        )

        assets = trajectory["trajectory_steps"][1]["asset_snapshots"]
        self.assertEqual([asset["asset_id"] for asset in assets], ["asset-a", "asset-b"])
        self.assertEqual(
            assets[0]["path"],
            "trajectory/underlying/stage-01-tone-pass/001-asset-a-asset-a-toned.png",
        )
        packaged = output / "underlying" / "stage-01-tone-pass" / "001-asset-a-asset-a-toned.png"
        self.assertEqual(packaged.read_bytes(), (self.snapshots / "asset-a-tone.png").read_bytes())
        self.assertEqual(assets[0]["snapshot_evidence"]["pixels"], [44, 30])
        self.assertTrue(assets[0]["snapshot_evidence"]["copied_byte_for_byte"])
        self.assertFalse(assets[0]["snapshot_evidence"]["same_bytes_as_previous_asset_state"])

        trajectory_html = (output / "trajectory.html").read_text(encoding="utf-8")
        contact_html = (output / "contact-sheet.html").read_text(encoding="utf-8")
        relative = "underlying/stage-01-tone-pass/001-asset-a-asset-a-toned.png"
        self.assertIn(f"src='{relative}'", trajectory_html)
        self.assertIn(f"href='{relative}'", contact_html)
        self.assertIn("Underlying asset snapshots (2)", trajectory_html)
        self.assertIn("asset-request-a", trajectory_html)

    def test_rejects_invalid_underlying_asset_records(self) -> None:
        bad_steps = [
            {
                "stage": 0,
                "title": "Source",
                "action": "source_inspection",
                "snapshot": "00-source.jpg",
                "decision": "Validate nested evidence.",
                "asset_snapshots": [
                    {
                        "asset_id": "asset-a",
                        "name": "Escapes root",
                        "path": "../outside.png",
                    }
                ],
            }
        ]
        manifest = self.write_manifest(bad_steps)
        with self.assertRaisesRegex(builder.EvidenceBuildError, "escapes --snapshots-root"):
            builder.build(
                manifest,
                self.root / "escaped-asset",
                task_key="PHOTO-TEST",
                snapshots_root=self.snapshots,
            )

        bad_steps[0]["asset_snapshots"][0] = {
            "asset_id": "asset-a",
            "name": "Wrong parameter shape",
            "path": "asset-a-source.png",
            "parameters": ["not", "an", "object"],
        }
        manifest = self.write_manifest(bad_steps)
        with self.assertRaisesRegex(builder.EvidenceBuildError, "parameters must be an object"):
            builder.build(
                manifest,
                self.root / "bad-parameters",
                task_key="PHOTO-TEST",
                snapshots_root=self.snapshots,
            )


if __name__ == "__main__":
    unittest.main()
