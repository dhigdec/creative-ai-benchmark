from __future__ import annotations

import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from PIL import Image


TOOLS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS_DIR))

import build_trajectory_evidence as builder  # noqa: E402
import publish_completed_runs as publisher  # noqa: E402


class PublishTrajectoryEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="publish-trajectory-test-")
        self.root = Path(self.temp_dir.name)
        self.captures = self.root / "captures"
        self.captures.mkdir()
        self.image("card-0.png", (120, 80), (70, 70, 70))
        self.image("card-1.png", (120, 80), (100, 100, 100))
        self.image("asset-a-0.png", (50, 40), (20, 40, 80))
        self.image("asset-a-1.png", (50, 40), (30, 60, 110))
        self.image("asset-b-1.jpg", (40, 60), (180, 170, 150))
        manifest = {
            "task_id": "SB3-TEST-PHO",
            "title": "Publisher test",
            "steps": [
                {
                    "stage": 0,
                    "title": "Source",
                    "action": "source_inspection",
                    "snapshot": "card-0.png",
                    "decision": "Bind the source state.",
                    "asset_snapshots": [
                        {"asset_id": "asset-a", "name": "A source", "path": "asset-a-0.png"}
                    ],
                },
                {
                    "stage": 1,
                    "title": "Tone",
                    "action": "image_apply_auto_tone",
                    "snapshot": "card-1.png",
                    "decision": "Bind the toned state.",
                    "asset_snapshots": [
                        {"asset_id": "asset-a", "name": "A toned", "path": "asset-a-1.png"},
                        {"asset_id": "asset-b", "name": "B toned", "path": "asset-b-1.jpg"},
                    ],
                },
            ],
        }
        self.manifest = self.root / "capture.json"
        self.manifest.write_text(json.dumps(manifest), encoding="utf-8")
        self.source = self.root / "source"
        builder.build(
            self.manifest,
            self.source / "trajectory",
            snapshots_root=self.captures,
            generated_at="2026-01-02T03:04:05Z",
        )
        self.trajectory = json.loads((self.source / "trajectory" / "trajectory.json").read_text())

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def image(self, name: str, size: tuple[int, int], color: tuple[int, int, int]) -> None:
        Image.new("RGB", size, color).save(self.captures / name)

    def test_copies_primary_underlying_and_reports_and_rewrites_public_urls(self) -> None:
        destination = self.root / "site-run"
        publisher.copy_step_snapshots(self.source, destination, self.trajectory)
        publisher.copy_evidence_artifacts(self.source, destination, self.trajectory)

        refs = []
        for step in self.trajectory["trajectory_steps"]:
            refs.append(step["snapshot"])
            refs.extend(asset["path"] for asset in step.get("asset_snapshots", []))
        for reference in refs:
            source_file = self.source.joinpath(*Path(reference).parts)
            destination_file = destination.joinpath(*Path(reference).parts)
            self.assertTrue(destination_file.is_file(), reference)
            self.assertEqual(destination_file.read_bytes(), source_file.read_bytes())
        for reference in publisher.EVIDENCE_ARTIFACT_PATHS.values():
            self.assertEqual(
                destination.joinpath(*Path(reference).parts).read_bytes(),
                self.source.joinpath(*Path(reference).parts).read_bytes(),
            )

        public = publisher.public_trajectory_steps(self.trajectory, "PHOTO TEST")
        self.assertEqual([step["stage"] for step in public], [0, 1])
        self.assertEqual(
            public[1]["snapshot_url"],
            "runs/PHOTO%20TEST/trajectory/intermediate/01-tone.png",
        )
        self.assertEqual(
            public[1]["asset_snapshots"][0]["snapshot_url"],
            "runs/PHOTO%20TEST/trajectory/underlying/stage-01-tone/001-asset-a-a-toned.png",
        )
        artifacts = publisher.public_evidence_artifacts(self.trajectory, "PHOTO TEST")
        self.assertEqual(
            artifacts["decision_evidence_report"],
            "runs/PHOTO%20TEST/trajectory/decision-evidence.html",
        )

    def test_rejects_asset_traversal_and_wrong_evidence_hash_before_copy(self) -> None:
        traversal = deepcopy(self.trajectory)
        traversal["trajectory_steps"][0]["asset_snapshots"][0]["path"] = (
            "trajectory/underlying/../escape.png"
        )
        destination = self.root / "unsafe-site-run"
        with self.assertRaisesRegex(ValueError, "canonical package path"):
            publisher.copy_step_snapshots(self.source, destination, traversal)
        self.assertFalse(destination.exists())

        wrong_hash = deepcopy(self.trajectory)
        wrong_hash["trajectory_steps"][0]["snapshot_evidence"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            publisher.copy_step_snapshots(self.source, destination, wrong_hash)
        self.assertFalse(destination.exists())

    def test_rejects_missing_declared_report_and_overwrites_changed_previous_publish(self) -> None:
        destination = self.root / "site-run"
        primary = self.trajectory["trajectory_steps"][0]["snapshot"]
        stale = destination.joinpath(*Path(primary).parts)
        stale.parent.mkdir(parents=True)
        stale.write_bytes(b"stale prior publish")
        publisher.copy_step_snapshots(self.source, destination, self.trajectory)
        self.assertEqual(stale.read_bytes(), self.source.joinpath(*Path(primary).parts).read_bytes())

        missing = deepcopy(self.trajectory)
        missing["evidence_artifacts"].pop("contact_sheet_report")
        with self.assertRaisesRegex(ValueError, "contact_sheet_report"):
            publisher.copy_evidence_artifacts(self.source, self.root / "missing-report", missing)


if __name__ == "__main__":
    unittest.main()
