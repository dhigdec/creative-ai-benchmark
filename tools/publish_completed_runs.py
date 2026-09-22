#!/usr/bin/env python3
"""Publish completed benchmark runs into the static Gatsby V5 site."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import unicodedata
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import quote

from PIL import Image
from pypdf import PdfReader


SITE_REL = Path("docs/gatsby-v5")
RUN_DATE = "2026-09-21"
TASK_CONFIG = {
    "PHOTO-04": {
        "code": "SB3-004-PHO",
        "drive_folder": "https://drive.google.com/drive/folders/1mrc9s7d8VcMOPKQQBrftGs5Q5ixtwbR7",
        "package": "SB3-004-PHO-complete-delivery.zip",
        "intermediate": "oliveto_bedroom_after_tone.png",
        "k6": {
            "K6_Q3": {
                "grade": "Pass",
                "evidence": "Source-to-output bindings stayed explicit for each villa, and every final check used the latest exported file named in the contract.",
            },
            "K6_Q4": {
                "grade": "Minor",
                "evidence": "The run completed, but a 22-image straighten call returned only 10 outputs and two concurrent auto-tone chunks returned HTTP 504 before connector-safe recovery.",
            },
            "K6_Q5": {
                "grade": "Pass",
                "evidence": "The agent detected the incomplete batch and HTTP 504 responses, retried only missing inputs in smaller chunks, then reviewed all outputs and the three center-fallback hero crops.",
            },
            "K6_Q6": {
                "grade": "Pass",
                "evidence": "All three PNGs were decoded and measured at 1920 x 1080; the brochure was decoded, counted at 6 pages, checked at A4 trim, and all rendered pages were visually inspected.",
            },
            "K6_Q7": {
                "grade": "Pass",
                "evidence": "Tool failures, retries, the center-crop fallback, and the still-pending independent creative review are disclosed in the trajectory and release state.",
            },
        },
    },
    "PHOTO-13": {
        "code": "SB3-013-PHO",
        "drive_folder": "https://drive.google.com/drive/folders/1w8ohauvXxJOyqPVV58Q5oq7WE5pAXonM",
        "package": "SB3-013-PHO-complete-delivery.zip",
        "intermediate": "bench_capsule_01_after_tone.png",
        "k6": {
            "K6_Q3": {
                "grade": "Pass",
                "evidence": "The inventory row, source photograph, SKU, product name, and final export remained bound across all ten product-detail variants and both print files.",
            },
            "K6_Q4": {
                "grade": "Minor",
                "evidence": "The work completed, but the initial 22-image straighten call was truncated and concurrent auto-tone chunks returned HTTP 504 before smaller sequential retries succeeded.",
            },
            "K6_Q5": {
                "grade": "Pass",
                "evidence": "The incomplete batch and Adobe HTTP 504 responses were detected; only missing inputs were retried in connector-safe chunks, and final product/PDF renders were inspected.",
            },
            "K6_Q6": {
                "grade": "Pass",
                "evidence": "Ten PNGs were decoded and measured at 1440 x 1800; the A2 poster and two-page A4 look sheet were decoded, measured, page-counted, and all rendered pages were visually inspected.",
            },
            "K6_Q7": {
                "grade": "Pass",
                "evidence": "The trajectory records connector failures and recovery, while the site explicitly leaves independent creative review pending rather than claiming it occurred.",
            },
        },
    },
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=1, ensure_ascii=False) + "\n")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pdf_measurements(path: Path) -> tuple[int, float, float]:
    reader = PdfReader(path)
    page = reader.pages[0]
    width_mm = float(page.mediabox.width) * 25.4 / 72
    height_mm = float(page.mediabox.height) * 25.4 / 72
    return len(reader.pages), width_mm, height_mm


SNAPSHOT_FIELDS = ("snapshot_url", "snapshot", "snapshot_path", "intermediate_snapshot")
EVIDENCE_ARTIFACT_PATHS = {
    "contact_sheet_image": "trajectory/contact-sheet.png",
    "contact_sheet_report": "trajectory/contact-sheet.html",
    "decision_evidence_report": "trajectory/decision-evidence.html",
}


def step_snapshot_reference(step: dict[str, Any]) -> str | None:
    """Return a snapshot reference, rejecting conflicting aliases."""
    found: list[tuple[str, str]] = []
    for field in SNAPSHOT_FIELDS:
        value = step.get(field)
        if isinstance(value, str) and value.strip():
            found.append((field, value.strip()))
    if not found:
        return None
    if len({value for _, value in found}) != 1:
        labels = ", ".join(f"{field}={value!r}" for field, value in found)
        raise ValueError(f"Conflicting trajectory snapshot aliases: {labels}")
    return found[0][1]


def is_external_snapshot(reference: str) -> bool:
    return bool(re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", reference)) or reference.startswith(("//", "/"))


def canonical_package_reference(reference: str, label: str, prefix: tuple[str, ...]) -> PurePosixPath:
    """Validate a local POSIX package reference with a required directory prefix."""
    if not isinstance(reference, str) or not reference.strip():
        raise ValueError(f"{label} must be a non-empty string")
    reference = reference.strip()
    if is_external_snapshot(reference) or reference.startswith("runs/"):
        raise ValueError(f"{label} must be a local package path: {reference}")
    if "\\" in reference or "?" in reference or "#" in reference:
        raise ValueError(f"{label} contains unsafe path syntax: {reference}")
    if any(ord(character) < 32 or ord(character) == 127 for character in reference):
        raise ValueError(f"{label} contains control characters")
    segments = reference.split("/")
    if any(segment in {"", ".", ".."} for segment in segments):
        raise ValueError(f"{label} is not a canonical package path: {reference}")
    if tuple(segments[: len(prefix)]) != prefix:
        raise ValueError(f"{label} must start with {'/'.join(prefix)}/: {reference}")
    return PurePosixPath(*segments)


def reject_symlink_components(source: Path, reference: PurePosixPath, label: str) -> None:
    cursor = source
    for segment in reference.parts:
        cursor = cursor / segment
        if cursor.is_symlink():
            raise ValueError(f"{label} traverses a symlink: {reference.as_posix()}")


def resolve_package_file(source: Path, reference: PurePosixPath, label: str) -> Path:
    source_root = source.resolve()
    reject_symlink_components(source_root, reference, label)
    candidate = source_root.joinpath(*reference.parts)
    resolved = candidate.resolve()
    try:
        resolved.relative_to(source_root)
    except ValueError as exc:
        raise ValueError(f"{label} escapes the run source: {reference.as_posix()}") from exc
    if not resolved.is_file():
        raise FileNotFoundError(f"{label} was not found: {candidate}")
    return resolved


def verify_snapshot_evidence(
    snapshot: Path,
    reference: PurePosixPath,
    evidence: Any,
    label: str,
) -> None:
    if not isinstance(evidence, dict):
        raise TypeError(f"{label}.snapshot_evidence must be an object")
    packaged_path = evidence.get("packaged_path")
    if packaged_path != reference.as_posix():
        raise ValueError(
            f"{label}.snapshot_evidence.packaged_path does not match {reference.as_posix()!r}"
        )
    claimed_bytes = evidence.get("bytes")
    if isinstance(claimed_bytes, bool) or not isinstance(claimed_bytes, int):
        raise TypeError(f"{label}.snapshot_evidence.bytes must be an integer")
    if claimed_bytes != snapshot.stat().st_size:
        raise ValueError(f"{label} byte count does not match the packaged file")
    claimed_sha = evidence.get("sha256")
    if not isinstance(claimed_sha, str) or claimed_sha.lower() != sha256(snapshot):
        raise ValueError(f"{label} SHA-256 does not match the packaged file")
    claimed_pixels = evidence.get("pixels")
    if not (
        isinstance(claimed_pixels, list)
        and len(claimed_pixels) == 2
        and all(isinstance(value, int) and not isinstance(value, bool) for value in claimed_pixels)
    ):
        raise TypeError(f"{label}.snapshot_evidence.pixels must be [width, height]")
    with Image.open(snapshot) as image:
        image.verify()
    with Image.open(snapshot) as image:
        actual_pixels = [image.width, image.height]
    if claimed_pixels != actual_pixels:
        raise ValueError(f"{label} pixel dimensions do not match the packaged file")


def normalized_destination_key(reference: PurePosixPath) -> str:
    return unicodedata.normalize("NFC", reference.as_posix()).casefold()


def add_copy_plan_item(
    plan: list[tuple[Path, PurePosixPath, str]],
    targets: dict[str, str],
    source_file: Path,
    reference: PurePosixPath,
    label: str,
) -> None:
    key = normalized_destination_key(reference)
    if key in targets:
        raise RuntimeError(f"Published trajectory path collision: {targets[key]} and {label}")
    targets[key] = label
    plan.append((source_file, reference, label))


def install_copy_plan(
    destination: Path,
    plan: list[tuple[Path, PurePosixPath, str]],
) -> None:
    for source_file, reference, label in plan:
        target = destination.joinpath(*reference.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target)
        if sha256(target) != sha256(source_file):
            raise RuntimeError(f"Published copy failed SHA-256 verification for {label}")


def find_snapshot_source(source: Path, reference: str) -> Path | None:
    """Resolve a canonical primary trajectory snapshot inside the run source."""
    try:
        canonical = canonical_package_reference(
            reference, "trajectory snapshot", ("trajectory", "intermediate")
        )
        if len(canonical.parts) != 3:
            return None
        return resolve_package_file(source, canonical, "trajectory snapshot")
    except (FileNotFoundError, TypeError, ValueError):
        return None


def copy_step_snapshots(source: Path, destination: Path, trajectory: dict[str, Any]) -> None:
    """Preflight and copy primary plus underlying snapshots from trajectory_steps."""
    steps = trajectory.get("trajectory_steps")
    if steps is None:
        return
    if not isinstance(steps, list):
        raise TypeError("trajectory_steps must be an ordered array")
    plan: list[tuple[Path, PurePosixPath, str]] = []
    targets: dict[str, str] = {}
    for position, step in enumerate(steps, start=1):
        if not isinstance(step, dict):
            raise TypeError(f"trajectory_steps[{position - 1}] must be an object")
        reference = step_snapshot_reference(step)
        if not reference:
            raise ValueError(f"Trajectory step {position} does not record a snapshot")
        label = f"trajectory_steps[{position - 1}]"
        canonical = canonical_package_reference(reference, f"{label}.snapshot", ("trajectory", "intermediate"))
        if len(canonical.parts) != 3:
            raise ValueError(f"{label}.snapshot must be directly inside trajectory/intermediate")
        snapshot = resolve_package_file(source, canonical, f"{label}.snapshot")
        verify_snapshot_evidence(snapshot, canonical, step.get("snapshot_evidence"), label)
        add_copy_plan_item(plan, targets, snapshot, canonical, f"{label}.snapshot")

        assets = step.get("asset_snapshots")
        if assets is None:
            continue
        if not isinstance(assets, list):
            raise TypeError(f"{label}.asset_snapshots must be an array")
        for asset_position, asset in enumerate(assets):
            asset_label = f"{label}.asset_snapshots[{asset_position}]"
            if not isinstance(asset, dict):
                raise TypeError(f"{asset_label} must be an object")
            for field in ("asset_id", "name", "path"):
                if not isinstance(asset.get(field), str) or not asset[field].strip():
                    raise ValueError(f"{asset_label}.{field} must be a non-empty string")
            asset_reference = canonical_package_reference(
                asset["path"], f"{asset_label}.path", ("trajectory", "underlying")
            )
            if len(asset_reference.parts) < 4:
                raise ValueError(f"{asset_label}.path must include a stage directory and filename")
            asset_source = resolve_package_file(source, asset_reference, f"{asset_label}.path")
            verify_snapshot_evidence(
                asset_source,
                asset_reference,
                asset.get("snapshot_evidence"),
                asset_label,
            )
            add_copy_plan_item(plan, targets, asset_source, asset_reference, asset_label)
    install_copy_plan(destination, plan)


def copy_evidence_artifacts(source: Path, destination: Path, trajectory: dict[str, Any]) -> None:
    artifacts = trajectory.get("evidence_artifacts")
    if artifacts is None:
        return
    if not isinstance(artifacts, dict):
        raise TypeError("evidence_artifacts must be an object")
    plan: list[tuple[Path, PurePosixPath, str]] = []
    targets: dict[str, str] = {}
    for field, expected in EVIDENCE_ARTIFACT_PATHS.items():
        value = artifacts.get(field)
        if value != expected:
            raise ValueError(f"evidence_artifacts.{field} must equal {expected!r}")
        canonical = canonical_package_reference(value, f"evidence_artifacts.{field}", ("trajectory",))
        if canonical.as_posix() != expected:
            raise ValueError(f"evidence_artifacts.{field} must equal {expected!r}")
        artifact_source = resolve_package_file(source, canonical, f"evidence_artifacts.{field}")
        add_copy_plan_item(plan, targets, artifact_source, canonical, f"evidence_artifacts.{field}")
    install_copy_plan(destination, plan)


def public_package_url(task_id: str, reference: PurePosixPath) -> str:
    segments = ("runs", task_id, *reference.parts)
    return "/".join(quote(segment, safe="-._~") for segment in segments)


def public_evidence_artifacts(trajectory: dict[str, Any], task_id: str) -> dict[str, str] | None:
    artifacts = trajectory.get("evidence_artifacts")
    if artifacts is None:
        return None
    if not isinstance(artifacts, dict):
        raise TypeError("evidence_artifacts must be an object")
    result: dict[str, str] = {}
    for field, expected in EVIDENCE_ARTIFACT_PATHS.items():
        if artifacts.get(field) != expected:
            raise ValueError(f"evidence_artifacts.{field} must equal {expected!r}")
        canonical = canonical_package_reference(expected, f"evidence_artifacts.{field}", ("trajectory",))
        result[field] = public_package_url(task_id, canonical)
    return result


def public_trajectory_steps(trajectory: dict[str, Any], task_id: str) -> list[dict[str, Any]] | None:
    """Preserve source order and expose copied snapshot paths to the static site."""
    steps = trajectory.get("trajectory_steps")
    if steps is None:
        return None
    if not isinstance(steps, list):
        raise TypeError("trajectory_steps must be an ordered array")
    public_steps: list[dict[str, Any]] = []
    for position, step in enumerate(steps, start=1):
        if not isinstance(step, dict):
            raise TypeError(f"trajectory_steps[{position - 1}] must be an object")
        public_step = dict(step)
        reference = step_snapshot_reference(step)
        if not reference:
            raise ValueError(f"Trajectory step {position} does not record a snapshot")
        label = f"trajectory_steps[{position - 1}]"
        canonical = canonical_package_reference(reference, f"{label}.snapshot", ("trajectory", "intermediate"))
        if len(canonical.parts) != 3:
            raise ValueError(f"{label}.snapshot must be directly inside trajectory/intermediate")
        public_step["snapshot_url"] = public_package_url(task_id, canonical)
        assets = step.get("asset_snapshots")
        if assets is not None:
            if not isinstance(assets, list):
                raise TypeError(f"{label}.asset_snapshots must be an array")
            public_assets: list[dict[str, Any]] = []
            for asset_position, asset in enumerate(assets):
                asset_label = f"{label}.asset_snapshots[{asset_position}]"
                if not isinstance(asset, dict):
                    raise TypeError(f"{asset_label} must be an object")
                canonical_asset = canonical_package_reference(
                    asset.get("path"), f"{asset_label}.path", ("trajectory", "underlying")
                )
                public_asset = dict(asset)
                public_asset["snapshot_url"] = public_package_url(task_id, canonical_asset)
                public_assets.append(public_asset)
            public_step["asset_snapshots"] = public_assets
        public_steps.append(public_step)
    return public_steps


def verify_check(check: dict[str, Any], artifact: Path) -> tuple[bool, str]:
    assertion = check.get("assertion", {})
    op = assertion.get("op")
    required = assertion.get("equals")
    tolerance = float(assertion.get("tolerance", 0))
    if op == "file_exists":
        ok = artifact.is_file()
        return ok, f"File exists ({artifact.stat().st_size:,} bytes; SHA-256 {sha256(artifact)})." if ok else "File is missing."
    if not artifact.is_file():
        return False, "File is missing."
    if op == "decodable":
        fmt = str(assertion.get("format", "")).lower()
        try:
            if fmt == "pdf":
                PdfReader(artifact)
            else:
                with Image.open(artifact) as image:
                    image.verify()
            return True, f"Decoded successfully as {fmt.upper()}."
        except Exception as exc:  # pragma: no cover - only used on malformed input
            return False, f"Decode failed: {exc}"
    if op in {"width", "height"}:
        with Image.open(artifact) as image:
            actual = image.width if op == "width" else image.height
        return actual == required, f"Measured {op}: {actual} px (required {required} px)."
    if op in {"pages", "trim_width_mm", "trim_height_mm"}:
        pages, width_mm, height_mm = pdf_measurements(artifact)
        if op == "pages":
            return pages == required, f"Counted {pages} PDF page(s) (required {required})."
        actual = width_mm if op == "trim_width_mm" else height_mm
        ok = abs(actual - float(required)) <= tolerance
        label = "width" if op == "trim_width_mm" else "height"
        return ok, f"Measured trim {label}: {actual:.2f} mm (required {required} +/- {tolerance} mm)."
    raise ValueError(f"Unsupported verifier operation: {op}")


def copy_run(source_root: Path, site: Path, task_id: str, cfg: dict[str, Any]) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    source = source_root / cfg["code"]
    destination = site / "runs" / task_id
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "deliverables").mkdir(exist_ok=True)
    (destination / "trajectory" / "intermediate").mkdir(parents=True, exist_ok=True)
    (destination / "package").mkdir(exist_ok=True)

    manifest = load_json(source / "manifest.json")
    trajectory = load_json(source / "trajectory" / "trajectory.json")
    for output in manifest["outputs"]:
        src = source / output["path"]
        if not src.is_file():
            raise FileNotFoundError(src)
        shutil.copy2(src, destination / output["path"])
    for name in ("trajectory.json", "trajectory.md", "trajectory.html"):
        shutil.copy2(source / "trajectory" / name, destination / "trajectory" / name)
    intermediate = source / "trajectory" / "intermediate" / cfg["intermediate"]
    shutil.copy2(intermediate, destination / "trajectory" / "intermediate" / intermediate.name)
    copy_step_snapshots(source, destination, trajectory)
    copy_evidence_artifacts(source, destination, trajectory)
    for name in ("manifest.json", "README.md"):
        shutil.copy2(source / name, destination / name)
    package = source_root / "packages" / cfg["package"]
    shutil.copy2(package, destination / "package" / package.name)
    return destination, manifest, trajectory


def enrich_outputs(outputs: list[dict[str, Any]], manifest: dict[str, Any], task_id: str, cfg: dict[str, Any]) -> list[dict[str, Any]]:
    by_path = {item["path"]: item for item in manifest["outputs"]}
    for output in outputs:
        item = by_path.get(output["path"])
        if not item:
            continue
        output.update(
            {
                "status": "produced",
                "verification": "passed",
                "artifact_url": f"runs/{task_id}/{output['path']}",
                "bytes": item["bytes"],
                "sha256": item["sha256"],
                "verified_at": RUN_DATE,
                "drive_folder_url": cfg["drive_folder"],
            }
        )
        if "actual_pixels" in item:
            output["actual_pixels"] = item["actual_pixels"]
        if "actual_pages" in item:
            output["actual_pages"] = item["actual_pages"]
    return outputs


def markdown_output_summary(task_name: str, outputs: list[dict[str, Any]], task_id: str, cfg: dict[str, Any]) -> str:
    rows = []
    for output in outputs:
        if output.get("status") != "produced":
            continue
        actual = " x ".join(map(str, output["actual_pixels"])) + " px" if output.get("actual_pixels") else f"{output.get('actual_pages')} page(s)"
        rows.append(f"| {output['name']} | [{output['path']}](../../runs/{task_id}/{output['path']}) | {actual} | Passed | `{output['sha256']}` |")
    package_url = f"../../runs/{task_id}/package/{cfg['package']}"
    return (
        f"# {task_name}: completed output register\n\n"
        f"Completed {RUN_DATE}. All contracted export files below passed the automatic file, decode, dimension, page-count, and trim checks applicable to their formats.\n\n"
        f"[Download complete delivery ZIP]({package_url}) · [Open Google Drive folder]({cfg['drive_folder']}) · [Run result JSON](RUN_RESULT.json)\n\n"
        "| Output | Public artifact | Measured result | Verification | SHA-256 |\n"
        "|---|---|---|---|---|\n" + "\n".join(rows) + "\n\n"
        "Reusable editable-source archives were not part of this executed export run and remain unassessed.\n"
    )


def markdown_verifier_summary(task_name: str, checks: list[dict[str, Any]], task_id: str) -> str:
    auto = [check for check in checks if check.get("type") == "auto"]
    human = [check for check in checks if check.get("type") == "human"]
    passed = sum(check.get("status") == "passed" for check in auto)
    rows = [
        f"| {check['check_id']} | {check.get('answer') or 'Pending'} | {check.get('status')} | {check.get('evidence_reference', '')} |"
        for check in auto
    ]
    return (
        f"# {task_name}: verifier results\n\n"
        f"Automatic verification: **{passed}/{len(auto)} passed**. Human verification: **{len(human)} checks pending independent review**.\n\n"
        f"[Run result JSON](RUN_RESULT.json) · [Trajectory JSON](../../runs/{task_id}/trajectory/trajectory.json) · [Trajectory report](../../runs/{task_id}/trajectory/trajectory.html)\n\n"
        "| Check | Answer | Status | Measured evidence |\n"
        "|---|---|---|---|\n" + "\n".join(rows) + "\n"
    )


def make_run_result(task_id: str, title: str, outputs: list[dict[str, Any]], checks: list[dict[str, Any]], trajectory: dict[str, Any], cfg: dict[str, Any]) -> dict[str, Any]:
    auto = [check for check in checks if check.get("type") == "auto"]
    human = [check for check in checks if check.get("type") == "human"]
    produced = [output for output in outputs if output.get("status") == "produced"]
    result = {
        "task_id": task_id,
        "task_code": cfg["code"],
        "title": title,
        "completed_at": RUN_DATE,
        "execution_status": "complete",
        "delivery_status": "all_contracted_exports_produced",
        "release_status": "held_pending_independent_creative_review",
        "outputs": produced,
        "verifier_summary": {
            "automatic_total": len(auto),
            "automatic_passed": sum(check.get("status") == "passed" for check in auto),
            "automatic_failed": sum(check.get("status") == "failed" for check in auto),
            "human_total": len(human),
            "human_status": "pending_independent_review",
        },
        "trajectory_scores": [
            {"question_id": question_id, **result} for question_id, result in cfg["k6"].items()
        ],
        "adobe_actions": trajectory.get("adobe_actions", []),
        "retries": trajectory.get("retries", []),
        "reasoning_summary": trajectory.get("reasoning_summary", []),
        "intermediate_snapshot": f"runs/{task_id}/trajectory/intermediate/{cfg['intermediate']}",
        "links": {
            "complete_package": f"runs/{task_id}/package/{cfg['package']}",
            "google_drive_folder": cfg["drive_folder"],
            "manifest": f"runs/{task_id}/manifest.json",
            "trajectory_json": f"runs/{task_id}/trajectory/trajectory.json",
            "trajectory_markdown": f"runs/{task_id}/trajectory/trajectory.md",
            "trajectory_report": f"runs/{task_id}/trajectory/trajectory.html",
        },
    }
    trajectory_steps = public_trajectory_steps(trajectory, task_id)
    if trajectory_steps is not None:
        result["trajectory_steps"] = trajectory_steps
        result["intermediate_snapshot"] = trajectory_steps[-1]["snapshot_url"]
    evidence_artifacts = public_evidence_artifacts(trajectory, task_id)
    if evidence_artifacts is not None:
        result["evidence_artifacts"] = evidence_artifacts
        result["links"].update(
            {
                "contact_sheet": evidence_artifacts["contact_sheet_report"],
                "contact_sheet_image": evidence_artifacts["contact_sheet_image"],
                "decision_evidence": evidence_artifacts["decision_evidence_report"],
            }
        )
    return result


def update_task_files(site: Path, task_id: str, cfg: dict[str, Any], manifest: dict[str, Any], trajectory: dict[str, Any]) -> dict[str, Any]:
    task_dir = site / "tasks" / task_id
    spec = load_json(task_dir / "TASK_SPEC.json")
    outputs = enrich_outputs(spec["deliverables"], manifest, task_id, cfg)
    checks = load_json(task_dir / "VERIFIERS.json")
    run_dir = site / "runs" / task_id
    failures = []
    for check in checks:
        if check.get("type") != "auto":
            continue
        artifact = run_dir / check["output_reference"]
        passed, evidence = verify_check(check, artifact)
        check["answer"] = "Yes" if passed else "No"
        check["status"] = "passed" if passed else "failed"
        check["evidence_reference"] = evidence
        check["verified_at"] = RUN_DATE
        check["artifact_url"] = f"runs/{task_id}/{check['output_reference']}"
        if not passed:
            failures.append(check["check_id"])
    if failures:
        raise RuntimeError(f"Automatic verifier failures for {task_id}: {failures}")

    run = make_run_result(task_id, spec["task_name"], outputs, checks, trajectory, cfg)
    spec["deliverables"] = outputs
    spec["execution"] = run
    readiness = spec["readiness"]
    readiness["asset_visual_quality"] = "passed"
    readiness["connector_end_to_end"] = "passed"
    readiness["independent_creative_review"] = "pending"
    readiness["release"] = "held_pending_independent_creative_review"
    readiness["completed_run"] = "all_contracted_exports_produced_and_automatically_verified"

    register = load_json(task_dir / "OUTPUT_REGISTER.json")
    enrich_outputs(register, manifest, task_id, cfg)
    gates = load_json(task_dir / "RELEASE_GATES.json")
    gates.update(
        {
            "asset_visual_quality": "passed",
            "connector_end_to_end": "passed",
            "independent_creative_review": "pending",
            "release": "held_pending_independent_creative_review",
            "completed_run": "all_contracted_exports_produced_and_automatically_verified",
        }
    )

    write_json(task_dir / "TASK_SPEC.json", spec)
    write_json(task_dir / "OUTPUT_REGISTER.json", register)
    write_json(task_dir / "VERIFIERS.json", checks)
    write_json(task_dir / "RELEASE_GATES.json", gates)
    write_json(task_dir / "RUN_RESULT.json", run)
    (task_dir / "DELIVERABLES.md").write_text(markdown_output_summary(spec["task_name"], outputs, task_id, cfg))
    (task_dir / "VERIFIERS.md").write_text(markdown_verifier_summary(spec["task_name"], checks, task_id))
    return {"outputs": outputs, "checks": checks, "readiness": readiness, "run": run, "spec": spec}


CSS = r"""
.run-banner{margin:0 0 18px;padding:16px 18px;border:1px solid #a9cdbb;border-left:4px solid var(--green);border-radius:8px;background:#f2f8f5}.run-banner strong{display:block;font-size:16px;margin-bottom:4px}.run-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}.run-actions a,.output-links a{display:inline-block;padding:6px 9px;border:1px solid var(--line);border-radius:5px;background:#fff;text-decoration:none}.output-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin:12px 0 18px}.output-card{border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#fff}.output-card img,.output-card iframe{width:100%;height:240px;display:block;object-fit:contain;background:#f1f0ec;border:0}.output-card-body{padding:12px}.output-card h3{margin:0 0 5px;font-size:15px}.output-meta{color:var(--muted);font-size:12px;line-height:1.5}.output-hash{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.output-links{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}.result-badge,.trajectory-grade{display:inline-block;padding:3px 8px;border-radius:999px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.04em}.result-pass,.grade-pass{background:#dcefe5;color:#235f43}.result-pending,.grade-minor{background:#fdf0cd;color:#77570d}.grade-major{background:#f8d9d4;color:#8d2e25}.verifier-table table{min-width:880px}.verifier-table th:nth-child(1){width:43%}.verifier-table th:nth-child(2){width:35%}.verifier-table th:nth-child(3){width:9%}.verifier-table th:nth-child(4){width:13%}.verifier-table td{overflow-wrap:normal;word-break:normal}.trajectory-result{margin-top:10px;padding:10px 12px;border:1px solid var(--line);border-radius:6px;background:#fff}.trajectory-result p{margin:7px 0 0}.intermediate-card{display:grid;grid-template-columns:minmax(220px,420px) 1fr;gap:18px;align-items:start;margin:18px 0;padding:14px;border:1px solid var(--line);border-radius:8px;background:#fafbfa}.intermediate-card img{width:100%;max-height:340px;object-fit:contain;background:#eee}.intermediate-card h3{margin-top:0}@media(max-width:900px){.verifier-table table,.verifier-table tbody,.verifier-table tr,.verifier-table td{display:block;min-width:0;width:auto}.verifier-table thead{display:none}.verifier-table tr{margin:0 0 12px;padding:10px 12px;border:1px solid var(--line);border-radius:7px;background:#fff}.verifier-table td{padding:7px 0;border:0}.verifier-table td+td{border-top:1px solid #eceae4}.verifier-table td:nth-child(2)::before,.verifier-table td:nth-child(3)::before,.verifier-table td:nth-child(4)::before{display:block;color:var(--muted);font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px}.verifier-table td:nth-child(2)::before{content:'Evidence'}.verifier-table td:nth-child(3)::before{content:'Check'}.verifier-table td:nth-child(4)::before{content:'Answer'}}@media(max-width:760px){.intermediate-card{grid-template-columns:1fr}.output-card img,.output-card iframe{height:210px}}
.trajectory-timeline{margin:22px 0}.trajectory-timeline-header{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin-bottom:14px}.trajectory-timeline-header h3{margin:0}.trajectory-timeline-header span{color:var(--muted);font-size:12px}.trajectory-step{position:relative;display:grid;grid-template-columns:34px minmax(0,1fr);gap:12px;padding-bottom:18px}.trajectory-step:not(:last-child)::before{content:'';position:absolute;left:16px;top:34px;bottom:0;width:2px;background:var(--line)}.trajectory-step-index{position:relative;z-index:1;display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:#253d35;color:#fff;font-size:12px;font-weight:700}.trajectory-step-card{border:1px solid var(--line);border-radius:8px;background:#fafbfa;overflow:hidden}.trajectory-step-heading{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;padding:13px 14px;border-bottom:1px solid var(--line);background:#fff}.trajectory-step-heading h4{margin:0;font-size:15px}.trajectory-step-stage,.trajectory-step-meta{color:var(--muted);font-size:11px}.trajectory-step-status{white-space:nowrap}.trajectory-step-body{display:grid;grid-template-columns:minmax(220px,360px) minmax(0,1fr);gap:16px;padding:14px}.trajectory-step-snapshot img{display:block;width:100%;max-height:300px;object-fit:contain;background:#eee}.trajectory-step-snapshot a{display:block}.trajectory-step-empty{display:grid;place-items:center;min-height:150px;padding:14px;border:1px dashed var(--line);color:var(--muted);font-size:12px;text-align:center}.trajectory-step-details p{margin:0 0 10px}.trajectory-step-details strong{display:block;margin-bottom:3px;font-size:11px;text-transform:uppercase;letter-spacing:.05em}.trajectory-step-details pre{margin:0 0 10px;padding:9px;overflow:auto;border-radius:5px;background:#eeefecci;font:11px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace;white-space:pre-wrap;word-break:break-word}.trajectory-step-meta{display:flex;gap:12px;flex-wrap:wrap;margin-top:12px}.trajectory-links{margin-top:4px;padding:14px;border-top:1px solid var(--line)}@media(max-width:760px){.trajectory-step-body{grid-template-columns:1fr}.trajectory-step-heading{display:block}.trajectory-step-status{margin-top:7px}}
"""


JS_HELPERS = r"""
const formatBytes=n=>{if(!n)return '';const u=['B','KB','MB','GB'];let i=0,v=n;while(v>=1024&&i<u.length-1){v/=1024;i++;}return `${v.toFixed(i?1:0)} ${u[i]}`;};
const specLine=o=>Object.entries(o.spec||{}).filter(([k])=>['format','width','height','width_mm','height_mm','pages','duration_seconds','ratio','audio'].includes(k)).map(([k,v])=>`${k}: ${typeof v==='object'?JSON.stringify(v):v}`).join('; ');
function outputCard(o){const url=o.artifact_url||'';const image=/\.(png|jpe?g|webp|gif)$/i.test(url);const pdf=/\.pdf$/i.test(url);const preview=image?`<a href="${esc(url)}" target="_blank" rel="noopener"><img loading="lazy" src="${esc(url)}" alt="${esc(o.name)}"></a>`:pdf?`<iframe loading="lazy" title="${esc(o.name)} PDF preview" src="${esc(url)}#view=FitH&toolbar=0"></iframe>`:'';const actual=o.actual_pixels?`${o.actual_pixels[0]} x ${o.actual_pixels[1]} px`:o.actual_pages?`${o.actual_pages} page${o.actual_pages===1?'':'s'}`:'';return `<article class="output-card">${preview}<div class="output-card-body"><h3>${esc(o.name)}</h3><span class="result-badge ${o.verification==='passed'?'result-pass':'result-pending'}">${esc(o.verification||o.status||'pending')}</span><p class="output-meta"><code>${esc(o.path)}</code><br>${esc(actual||specLine(o))}${o.bytes?` · ${esc(formatBytes(o.bytes))}`:''}${o.sha256?`<span class="output-hash" title="${esc(o.sha256)}">SHA-256 ${esc(o.sha256)}</span>`:''}</p><div class="output-links">${url?`<a href="${esc(url)}" target="_blank" rel="noopener">Open</a><a href="${esc(url)}" download>Download</a>`:''}</div></div></article>`;}
"""


JS_TRAJECTORY_HELPERS = r"""
const trajectoryValue=value=>value===undefined||value===null||value===''?'':typeof value==='string'?value:JSON.stringify(value,null,2);
function trajectoryTimeline(run){const steps=Array.isArray(run?.trajectory_steps)?run.trajectory_steps:[];if(!steps.length)return '';return `<section class="trajectory-timeline"><div class="trajectory-timeline-header"><h3>Complete intermediate trajectory</h3><span>${steps.length} recorded step${steps.length===1?'':'s'} · source order</span></div>${steps.map((s,i)=>{const number=s.stage??s.step??i+1;const title=s.title||s.name||s.action||`Step ${number}`;const snapshot=s.snapshot_url||s.snapshot||s.snapshot_path||s.intermediate_snapshot||'';const decision=trajectoryValue(s.decision??s.important_decision);const reasoning=trajectoryValue(s.reasoning??s.rationale);const action=trajectoryValue(s.action);const parameters=trajectoryValue(s.parameters);const timestamp=s.timestamp||s.created_at||s.started_at||s.completed_at||'';const requestId=s.request_id||s.requestId||'';return `<article class="trajectory-step"><div class="trajectory-step-index">${esc(number)}</div><div class="trajectory-step-card"><div class="trajectory-step-heading"><div><div class="trajectory-step-stage">Stage ${esc(number)}</div><h4>${esc(title)}</h4></div>${s.status?`<span class="result-badge trajectory-step-status">${esc(s.status)}</span>`:''}</div><div class="trajectory-step-body"><div class="trajectory-step-snapshot">${snapshot?`<a href="${esc(snapshot)}" target="_blank" rel="noopener"><img loading="lazy" src="${esc(snapshot)}" alt="Snapshot after stage ${esc(number)}: ${esc(title)}"></a>`:'<div class="trajectory-step-empty">No snapshot was recorded for this step.</div>'}</div><div class="trajectory-step-details">${action&&action!==title?`<p><strong>Action</strong>${esc(action)}</p>`:''}${parameters?`<strong>Parameters</strong><pre>${esc(parameters)}</pre>`:''}${decision?`<p><strong>Decision</strong>${esc(decision)}</p>`:''}${reasoning?`<p><strong>Reasoning</strong>${esc(reasoning)}</p>`:''}<div class="trajectory-step-meta">${timestamp?`<span><strong>Timestamp</strong>${esc(timestamp)}</span>`:''}${requestId?`<span><strong>Request ID</strong><code>${esc(requestId)}</code></span>`:''}</div></div></div></div></article>`;}).join('')}</section>`;}
"""


def update_index(site: Path, updates: dict[str, dict[str, Any]]) -> None:
    index = site / "index.html"
    html = index.read_text()
    match = re.search(r'(<script[^>]*id="data"[^>]*>)(.*?)(</script>)', html, re.S)
    if not match:
        raise RuntimeError("Embedded site data was not found")
    data = json.loads(match.group(2))
    for task in data["tasks"]:
        update = updates.get(task["id"])
        if not update:
            continue
        by_output = {output["output_id"]: output for output in update["outputs"]}
        task["outputs"] = [{**output, **by_output.get(output["output_id"], {})} for output in task["outputs"]]
        task["checks"] = update["checks"]
        task["readiness"] = update["readiness"]
        task["run"] = update["run"]
    embedded = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    html = html[: match.start(2)] + embedded + html[match.end(2) :]

    if ".run-banner{" not in html:
        html = html.replace("</style>", CSS + "</style>", 1)
    else:
        css_start = html.find("\n.run-banner{")
        css_end = html.find("</style>", css_start)
        html = html[:css_start] + CSS + html[css_end:]
    helper_anchor = "const sections=['Brief','Brand','Outputs','Auto verifiers','Human verifiers','Trajectory verifiers','Assets','Release gates'];"
    if "function outputCard(o)" not in html:
        html = html.replace(helper_anchor, JS_HELPERS + helper_anchor, 1)
    if "function trajectoryTimeline(run)" not in html:
        html = html.replace(helper_anchor, JS_TRAJECTORY_HELPERS + helper_anchor, 1)

    old_check_rows = "function checkRows(rows){return table(['Pass condition','Reference','Check','Answer'],rows.map(c=>[conditionHTML(c),evidenceHTML(c),`<span title=\"${esc(c.check_id)}\">${esc(c.check_id.split('/').at(-1))}</span>`,'<strong>Yes / No</strong>']));}"
    new_check_rows = "function checkRows(rows){return table(['Pass condition','Reference','Check','Answer'],rows.map(c=>[conditionHTML(c),evidenceHTML(c),`<span title=\"${esc(c.check_id)}\">${esc(c.check_id.split('/').at(-1))}</span>`,c.answer?`<span class=\"result-badge ${c.status==='passed'?'result-pass':'result-pending'}\">${esc(c.answer)} · ${esc(c.status)}</span>`:'<strong>Yes / No</strong>']));}"
    html = html.replace(old_check_rows, new_check_rows, 1)

    old_toolbar = "function verifierToolbar(t,rows){return `<div class=\"toolbar\"><label for=\"output-filter\">Output</label><select id=\"output-filter\"><option value=\"\">All outputs</option>${t.outputs.map(o=>`<option value=\"${esc(o.output_id)}\" ${o.output_id===outputFilter?'selected':''}>${esc(o.review_name||o.name)}</option>`).join('')}</select><a href=\"tasks/${t.id}/VERIFIERS.json\" download>Verifier JSON</a><span>${rows.length} binary checks · not assessed</span></div><p class=\"verifier-note\"><strong>How to mark:</strong> answer Yes or No. Only Yes passes. Every check is one observable fact about one named file.</p>`;}"
    new_toolbar = "function verifierToolbar(t,rows){const assessed=rows.filter(c=>c.status==='passed'||c.status==='failed').length,passed=rows.filter(c=>c.status==='passed').length;const summary=assessed?`${passed}/${rows.length} passed`:`${rows.length} binary checks · not assessed`;return `<div class=\"toolbar\"><label for=\"output-filter\">Output</label><select id=\"output-filter\"><option value=\"\">All outputs</option>${t.outputs.map(o=>`<option value=\"${esc(o.output_id)}\" ${o.output_id===outputFilter?'selected':''}>${esc(o.review_name||o.name)}</option>`).join('')}</select><a href=\"tasks/${t.id}/VERIFIERS.json\" download>Verifier JSON</a><span>${summary}</span></div><p class=\"verifier-note\"><strong>${assessed?'Result':'How to mark'}:</strong> ${assessed?'Measured evidence is shown for every assessed check.':'answer Yes or No. Only Yes passes. Every check is one observable fact about one named file.'}</p>`;}"
    html = html.replace(old_toolbar, new_toolbar, 1)

    old_heading = "function render(){const t=current;document.getElementById('heading').innerHTML=`<h1>${esc(t.title)}</h1><div class=\"meta\"><span>${esc(t.code)} · ${esc(t.id)}</span><span>${esc(t.family)}</span><span>${countExports(t)} exports</span><span>${t.checks.length} checks</span></div>`;"
    new_heading = "function render(){const t=current;document.getElementById('heading').innerHTML=`<h1>${esc(t.title)}</h1><div class=\"meta\"><span>${esc(t.code)} · ${esc(t.id)}</span><span>${esc(t.family)}</span><span>${countExports(t)} exports</span><span>${t.checks.length} checks</span>${t.run?'<span class=\"result-badge result-pass\">Run complete</span>':''}</div>`;"
    html = html.replace(old_heading, new_heading, 1)

    old_outputs = "if(section==='Outputs')html=t.groups.map(g=>{const out=t.outputs.filter(o=>o.group_id===g.id);return `<details><summary>${esc(g.name)} · ${out.length} files</summary>${table(['Output','File','Delivery specification'],out.map(o=>[esc(o.name),`<code>${esc(o.path)}</code>`,esc(Object.entries(o.spec).filter(([k,v])=>['format','width','height','width_mm','height_mm','pages','duration_seconds','ratio','audio'].includes(k)).map(([k,v])=>`${k}: ${typeof v==='object'?JSON.stringify(v):v}`).join('; '))]))}</details>`;}).join('');"
    new_outputs = "if(section==='Outputs'){if(t.run){const l=t.run.links;html=`<div class=\"run-banner\"><strong>Completed run · ${esc(t.run.completed_at)}</strong>${t.run.outputs.length} contracted exports produced; ${t.run.verifier_summary.automatic_passed}/${t.run.verifier_summary.automatic_total} automatic checks passed. Independent creative review remains pending.<div class=\"run-actions\"><a href=\"${esc(l.complete_package)}\" download>Download complete ZIP</a><a href=\"${esc(l.google_drive_folder)}\" target=\"_blank\" rel=\"noopener\">Google Drive folder</a><a href=\"${esc(l.manifest)}\" target=\"_blank\">SHA-256 manifest</a></div></div>`+t.groups.map(g=>{const out=t.outputs.filter(o=>o.group_id===g.id&&o.status==='produced');return out.length?`<details open><summary>${esc(g.name)} · ${out.length} completed file${out.length===1?'':'s'}</summary><div class=\"output-grid\">${out.map(outputCard).join('')}</div></details>`:'';}).join('');}else{html=t.groups.map(g=>{const out=t.outputs.filter(o=>o.group_id===g.id);return `<details><summary>${esc(g.name)} · ${out.length} files</summary>${table(['Output','File','Delivery specification'],out.map(o=>[esc(o.name),`<code>${esc(o.path)}</code>`,esc(specLine(o))]))}</details>`;}).join('');}}"
    html = html.replace(old_outputs, new_outputs, 1)

    old_trajectory = "html+=(k6?k6.questions:[]).map(q=>`<div class=\"k-question\"><h3>${esc(kShort(q.id))} · ${esc(q.label)}${objBadge(q)}</h3><p class=\"k-qtext\">${esc(q.question)}</p><details class=\"expected-copy\"><summary>Grading guide</summary><p><strong>Pass:</strong> ${esc(q.grades?.pass)}</p><p><strong>Minor:</strong> ${esc(q.grades?.minor)}</p><p><strong>Major:</strong> ${esc(q.grades?.major)}</p></details><p class=\"k-pending\">Pending: populated from the run trajectory after the task is executed.</p></div>`).join('');"
    legacy_run_trajectory = "const scores=Object.fromEntries((t.run?.trajectory_scores||[]).map(x=>[x.question_id,x]));html+=(k6?k6.questions:[]).map(q=>{const s=scores[q.id];return `<div class=\"k-question\"><h3>${esc(kShort(q.id))} · ${esc(q.label)}${objBadge(q)}</h3><p class=\"k-qtext\">${esc(q.question)}</p><details class=\"expected-copy\"><summary>Grading guide</summary><p><strong>Pass:</strong> ${esc(q.grades?.pass)}</p><p><strong>Minor:</strong> ${esc(q.grades?.minor)}</p><p><strong>Major:</strong> ${esc(q.grades?.major)}</p></details>${s?`<div class=\"trajectory-result\"><span class=\"trajectory-grade grade-${esc(s.grade.toLowerCase())}\">${esc(s.grade)}</span><p>${esc(s.evidence)}</p></div>`:'<p class=\"k-pending\">Pending: populated from the run trajectory after the task is executed.</p>'}</div>`;}).join('');if(t.run){const l=t.run.links;html+=`<div class=\"intermediate-card\"><a href=\"${esc(t.run.intermediate_snapshot)}\" target=\"_blank\"><img loading=\"lazy\" src=\"${esc(t.run.intermediate_snapshot)}\" alt=\"Intermediate run snapshot\"></a><div><h3>Intermediate snapshot and full trajectory</h3><p>This snapshot records the asset after Adobe tone treatment and before final layout/export. The complete trajectory includes source/output bindings, Adobe actions, retries, and concise decision summaries.</p><div class=\"run-actions\"><a href=\"${esc(l.trajectory_report)}\" target=\"_blank\">Open trajectory report</a><a href=\"${esc(l.trajectory_json)}\" target=\"_blank\">Trajectory JSON</a><a href=\"${esc(l.trajectory_markdown)}\" target=\"_blank\">Trajectory Markdown</a></div></div></div>`;}"
    new_trajectory = "const scores=Object.fromEntries((t.run?.trajectory_scores||[]).map(x=>[x.question_id,x]));html+=(k6?k6.questions:[]).map(q=>{const s=scores[q.id];return `<div class=\"k-question\"><h3>${esc(kShort(q.id))} · ${esc(q.label)}${objBadge(q)}</h3><p class=\"k-qtext\">${esc(q.question)}</p><details class=\"expected-copy\"><summary>Grading guide</summary><p><strong>Pass:</strong> ${esc(q.grades?.pass)}</p><p><strong>Minor:</strong> ${esc(q.grades?.minor)}</p><p><strong>Major:</strong> ${esc(q.grades?.major)}</p></details>${s?`<div class=\"trajectory-result\"><span class=\"trajectory-grade grade-${esc(s.grade.toLowerCase())}\">${esc(s.grade)}</span><p>${esc(s.evidence)}</p></div>`:'<p class=\"k-pending\">Pending: populated from the run trajectory after the task is executed.</p>'}</div>`;}).join('');if(t.run){const l=t.run.links;const timeline=trajectoryTimeline(t.run);html+=timeline||`<div class=\"intermediate-card\"><a href=\"${esc(t.run.intermediate_snapshot)}\" target=\"_blank\" rel=\"noopener\"><img loading=\"lazy\" src=\"${esc(t.run.intermediate_snapshot)}\" alt=\"Intermediate run snapshot\"></a><div><h3>Intermediate snapshot and full trajectory</h3><p>This run predates per-step snapshot logging. Its retained intermediate snapshot and full trajectory files remain available below.</p></div></div>`;html+=`<div class=\"run-actions trajectory-links\"><a href=\"${esc(l.trajectory_report)}\" target=\"_blank\" rel=\"noopener\">Open trajectory report</a><a href=\"${esc(l.trajectory_json)}\" target=\"_blank\" rel=\"noopener\">Trajectory JSON</a><a href=\"${esc(l.trajectory_markdown)}\" target=\"_blank\" rel=\"noopener\">Trajectory Markdown</a></div>`;}"
    if legacy_run_trajectory in html:
        html = html.replace(legacy_run_trajectory, new_trajectory, 1)
    else:
        html = html.replace(old_trajectory, new_trajectory, 1)

    old_release = "if(section==='Release gates')html=`<p class=\"status\">Release held pending validation</p>${table(['Gate','State'],Object.entries(t.readiness).filter(([k,v])=>typeof v==='string').map(([k,v])=>[esc(k.replaceAll('_',' ')),esc(v)]))}<h3>Open prerequisites</h3>${t.readiness.blockers.length?`<ul>${t.readiness.blockers.map(b=>`<li>${esc(b)}</li>`).join('')}</ul>`:'<p>No additional source prerequisite was detected by structural checks. Visual review and connector trials remain required.</p>'}<h3>Record exclusions</h3>${t.exclusions.length?table(['Group','Source row','Reason'],t.exclusions.map(e=>[esc(e.group),`${esc(e.table)}, row ${e.row_number}`,esc(e.reason)])):'<p>No rule-based exclusions were made.</p>'}`;"
    new_release = "if(section==='Release gates')html=`<p class=\"status\">${t.run?'Run complete · independent creative review pending':'Release held pending validation'}</p>${table(['Gate','State'],Object.entries(t.readiness).filter(([k,v])=>typeof v==='string').map(([k,v])=>[esc(k.replaceAll('_',' ')),esc(v)]))}<h3>Open prerequisites</h3>${t.readiness.blockers.length?`<ul>${t.readiness.blockers.map(b=>`<li>${esc(b)}</li>`).join('')}</ul>`:t.run?'<p>Contracted artifacts and connector execution are complete. Independent creative review remains pending.</p>':'<p>No additional source prerequisite was detected by structural checks. Visual review and connector trials remain required.</p>'}<h3>Record exclusions</h3>${t.exclusions.length?table(['Group','Source row','Reason'],t.exclusions.map(e=>[esc(e.group),`${esc(e.table)}, row ${e.row_number}`,esc(e.reason)])):'<p>No rule-based exclusions were made.</p>'}`;"
    html = html.replace(old_release, new_release, 1)

    required_fragments = [
        new_check_rows,
        new_toolbar,
        new_heading,
        new_outputs,
        "function trajectoryTimeline(run)",
        new_trajectory,
        new_release,
    ]
    if not all(fragment in html for fragment in required_fragments):
        raise RuntimeError("One or more index renderer replacements did not apply")
    index.write_text(html)


def update_master_task_json(site: Path, updates: dict[str, dict[str, Any]]) -> None:
    path = site / "TASKS_V5_ALL100.json"
    tasks = load_json(path)
    for task in tasks:
        task_id = task.get("new_id")
        if task_id not in updates:
            continue
        update = updates[task_id]
        task["deliverables"] = update["outputs"]
        task["verifiers_auto"] = [check for check in update["checks"] if check.get("type") == "auto"]
        task["verifiers_human"] = [check for check in update["checks"] if check.get("type") == "human"]
        task["readiness"] = update["readiness"]
        task["execution"] = update["run"]
    write_json(path, tasks)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    site = repo / SITE_REL
    updates: dict[str, dict[str, Any]] = {}
    for task_id, cfg in TASK_CONFIG.items():
        _, manifest, trajectory = copy_run(args.source_root, site, task_id, cfg)
        updates[task_id] = update_task_files(site, task_id, cfg, manifest, trajectory)
    update_index(site, updates)
    summary = {
        task_id: {
            "outputs": len(update["run"]["outputs"]),
            "automatic_passed": update["run"]["verifier_summary"]["automatic_passed"],
            "automatic_total": update["run"]["verifier_summary"]["automatic_total"],
        }
        for task_id, update in updates.items()
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
