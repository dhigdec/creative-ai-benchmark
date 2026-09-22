#!/usr/bin/env python3
"""Build auditable trajectory evidence from a manifest and real local snapshots.

The builder never synthesizes an intermediate image. Every trajectory step must
reference a distinct local file, and that file is decoded before it is copied
byte-for-byte into the output package. Action names, parameters, decisions, and
request IDs remain manifest-supplied claims; the generated reports say so.

Typical usage for a multi-task capture manifest::

    python3 tools/build_trajectory_evidence.py --manifest capture.json
      --task PHOTO-04 --output-dir build/PHOTO-04/trajectory

The manifest can either contain ``steps`` at its top level or a ``tasks`` map.
For the latter, pass ``--task``. Snapshot paths are resolved below the manifest
directory by default; override that root with ``--snapshots-root``.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import sys
import tempfile
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from PIL import Image, ImageDraw, ImageFont, ImageOps


SCHEMA_VERSION = "trajectory-evidence/v1"
MANAGED_MARKER = ".trajectory-evidence-builder.json"
REPORT_NAMES = (
    "trajectory.json",
    "trajectory.md",
    "trajectory.html",
    "contact-sheet.png",
    "contact-sheet.html",
    "decision-evidence.html",
)
SNAPSHOT_FIELDS = ("snapshot", "snapshot_path", "snapshot_url", "intermediate_snapshot")
PRESERVED_FIELDS = (
    "source_binding",
    "intent",
    "workflow",
    "look",
    "preset",
    "crop",
    "task_parameters",
    "retries",
    "shared_failures_and_recovery",
    "output_binding",
    "reasoning_summary",
    "status",
    "approval",
)


class EvidenceBuildError(ValueError):
    """Raised when the manifest cannot produce truthful evidence."""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise EvidenceBuildError(f"Manifest was not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise EvidenceBuildError(f"Manifest is not valid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise EvidenceBuildError("Manifest root must be a JSON object")
    return value


def select_task(manifest: dict[str, Any], task_key: str | None) -> dict[str, Any]:
    """Return one normalized task record without mutating the source manifest."""
    tasks = manifest.get("tasks")
    if tasks is None:
        if task_key:
            raise EvidenceBuildError("--task is only valid when the manifest has a tasks map")
        selected = dict(manifest)
    else:
        if not isinstance(tasks, dict) or not tasks:
            raise EvidenceBuildError("Manifest tasks must be a non-empty object")
        if not task_key:
            choices = ", ".join(sorted(str(key) for key in tasks))
            raise EvidenceBuildError(f"Manifest contains multiple tasks; choose one with --task ({choices})")
        raw = tasks.get(task_key)
        if not isinstance(raw, dict):
            raise EvidenceBuildError(f"Task {task_key!r} was not found in the manifest")
        selected = dict(raw)
        selected.setdefault("task_key", task_key)
        for field in ("workflow", "status", "shared_failures_and_recovery"):
            if field not in selected and field in manifest:
                selected[field] = manifest[field]

    if "task_id" not in selected:
        selected["task_id"] = selected.get("task_code") or selected.get("task_key")
    if not isinstance(selected.get("task_id"), str) or not selected["task_id"].strip():
        raise EvidenceBuildError("Selected task must define task_id, task_code, or a tasks-map key")
    selected["task_id"] = selected["task_id"].strip()
    selected.setdefault("title", f"{selected['task_id']} trajectory evidence")
    selected["title"] = nonempty_string(selected["title"], "Selected task title")
    return selected


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvidenceBuildError(f"{label} must be a non-empty string")
    return value.strip()


def snapshot_reference(step: dict[str, Any], position: int) -> str:
    found = []
    for field in SNAPSHOT_FIELDS:
        value = step.get(field)
        if isinstance(value, str) and value.strip():
            found.append((field, value.strip()))
    if not found:
        raise EvidenceBuildError(f"steps[{position}] must reference a snapshot")
    distinct = {value for _, value in found}
    if len(distinct) > 1:
        labels = ", ".join(f"{key}={value!r}" for key, value in found)
        raise EvidenceBuildError(f"steps[{position}] has conflicting snapshot fields: {labels}")
    return found[0][1]


def resolve_snapshot(reference: str, snapshots_root: Path, label: str) -> Path:
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", reference) or reference.startswith("//"):
        raise EvidenceBuildError(
            f"{label} must be a local file, not a URL or data URI: {reference}"
        )
    relative = Path(reference)
    if relative.is_absolute():
        raise EvidenceBuildError(
            f"{label} must be relative to --snapshots-root: {reference}"
        )
    root = snapshots_root.resolve()
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise EvidenceBuildError(f"{label} escapes --snapshots-root: {reference}") from exc
    if not candidate.is_file():
        raise EvidenceBuildError(f"{label} was not found: {candidate}")
    return candidate


def inspect_image(path: Path, label: str) -> dict[str, Any]:
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            width, height = image.size
            image_format = (image.format or "unknown").upper()
            mode = image.mode
            frames = int(getattr(image, "n_frames", 1))
            orientation = image.getexif().get(274)
            display = ImageOps.exif_transpose(image)
            display_width, display_height = display.size
    except Exception as exc:
        raise EvidenceBuildError(f"{label} is not a decodable image: {path}: {exc}") from exc
    if width < 1 or height < 1:
        raise EvidenceBuildError(f"{label} has invalid dimensions: {path}")
    return {
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "format": image_format,
        "mime_type": Image.MIME.get(image_format, "application/octet-stream"),
        "pixels": [width, height],
        "display_pixels": [display_width, display_height],
        "mode": mode,
        "frames": frames,
        "exif_orientation": orientation,
    }


def slug(value: str) -> str:
    clean = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return clean[:64] or "snapshot"


def extension_for(path: Path, image_format: str) -> str:
    extension = path.suffix.lower()
    if extension in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".tif", ".tiff", ".bmp"}:
        return extension
    return {
        "JPEG": ".jpg",
        "PNG": ".png",
        "WEBP": ".webp",
        "GIF": ".gif",
        "TIFF": ".tif",
        "BMP": ".bmp",
    }.get(image_format, ".img")


def validate_optional_asset_fields(asset: dict[str, Any], label: str) -> None:
    for field in ("input_url", "output_url", "request_id", "status"):
        if field in asset:
            asset[field] = nonempty_string(asset[field], f"{label}.{field}")
    if "parameters" in asset and not isinstance(asset["parameters"], dict):
        raise EvidenceBuildError(f"{label}.parameters must be an object")


def prepare_asset_snapshots(
    raw_assets: Any,
    stage: int,
    title: str,
    snapshots_root: Path,
    underlying: Path,
    step_position: int,
    previous_asset_state: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    if raw_assets is None:
        return []
    if not isinstance(raw_assets, list):
        raise EvidenceBuildError(f"steps[{step_position}].asset_snapshots must be an array")

    stage_directory = underlying / f"stage-{stage:02d}-{slug(title)}"
    prepared: list[dict[str, Any]] = []
    stage_asset_ids: set[str] = set()
    for asset_position, raw_asset in enumerate(raw_assets):
        label = f"steps[{step_position}].asset_snapshots[{asset_position}]"
        if not isinstance(raw_asset, dict):
            raise EvidenceBuildError(f"{label} must be an object")
        asset = dict(raw_asset)
        asset_id = nonempty_string(asset.get("asset_id"), f"{label}.asset_id")
        name = nonempty_string(asset.get("name"), f"{label}.name")
        reference = nonempty_string(asset.get("path"), f"{label}.path")
        if asset_id in stage_asset_ids:
            raise EvidenceBuildError(f"{label}.asset_id duplicates {asset_id!r} in the same stage")
        stage_asset_ids.add(asset_id)
        validate_optional_asset_fields(asset, label)

        source = resolve_snapshot(reference, snapshots_root, f"{label}.path")
        evidence = inspect_image(source, f"{label}.path")
        destination_name = (
            f"{asset_position + 1:03d}-{slug(asset_id)}-{slug(name)}"
            f"{extension_for(source, evidence['format'])}"
        )
        stage_directory.mkdir(parents=True, exist_ok=True)
        destination = stage_directory / destination_name
        shutil.copy2(source, destination)
        if sha256(destination) != evidence["sha256"]:
            raise EvidenceBuildError(f"Underlying snapshot copy verification failed: {source} -> {destination}")

        relative = destination.relative_to(underlying.parent)
        packaged_path = f"trajectory/{relative.as_posix()}"
        prior = previous_asset_state.get(asset_id)
        cleaned = {key: value for key, value in asset.items() if key != "path"}
        cleaned.update(
            {
                "asset_id": asset_id,
                "name": name,
                "path": packaged_path,
                "snapshot_evidence": {
                    **evidence,
                    "manifest_reference": reference,
                    "packaged_path": packaged_path,
                    "copied_byte_for_byte": True,
                    "same_bytes_as_previous_asset_state": bool(prior and prior["sha256"] == evidence["sha256"]),
                    "same_source_path_as_previous_asset_state": bool(
                        prior and prior["source_path"] == str(source)
                    ),
                },
            }
        )
        prepared.append(cleaned)
        previous_asset_state[asset_id] = {"sha256": evidence["sha256"], "source_path": str(source)}
    return prepared


def validate_and_prepare_steps(
    task: dict[str, Any], snapshots_root: Path, intermediate: Path, underlying: Path
) -> list[dict[str, Any]]:
    raw_steps = task.get("steps") or task.get("trajectory_steps")
    if not isinstance(raw_steps, list) or not raw_steps:
        raise EvidenceBuildError("Selected task must contain a non-empty steps or trajectory_steps array")

    prepared: list[dict[str, Any]] = []
    previous_stage: int | None = None
    previous_sha: str | None = None
    source_paths: set[Path] = set()
    previous_asset_state: dict[str, dict[str, Any]] = {}
    for position, raw in enumerate(raw_steps):
        if not isinstance(raw, dict):
            raise EvidenceBuildError(f"steps[{position}] must be an object")
        stage = raw.get("stage", raw.get("step"))
        if isinstance(stage, bool) or not isinstance(stage, int) or stage < 0:
            raise EvidenceBuildError(f"steps[{position}].stage must be a non-negative integer")
        if previous_stage is not None and stage <= previous_stage:
            raise EvidenceBuildError(
                f"steps must be in strictly increasing stage order; {stage} follows {previous_stage}"
            )
        title = nonempty_string(raw.get("title") or raw.get("name"), f"steps[{position}].title")
        action = nonempty_string(raw.get("action"), f"steps[{position}].action")
        decision = nonempty_string(
            raw.get("decision") or raw.get("important_decision"), f"steps[{position}].decision"
        )
        reference = snapshot_reference(raw, position)
        source = resolve_snapshot(reference, snapshots_root, f"steps[{position}] snapshot")
        if source in source_paths:
            raise EvidenceBuildError(
                f"steps[{position}] reuses the exact snapshot path {reference!r}; provide a per-stage file"
            )
        source_paths.add(source)
        evidence = inspect_image(source, f"steps[{position}] snapshot")
        destination_name = f"{stage:02d}-{slug(title)}{extension_for(source, evidence['format'])}"
        destination = intermediate / destination_name
        shutil.copy2(source, destination)
        if sha256(destination) != evidence["sha256"]:
            raise EvidenceBuildError(f"Snapshot copy verification failed: {source} -> {destination}")

        cleaned = {
            key: value
            for key, value in raw.items()
            if key not in SNAPSHOT_FIELDS and key not in {"step", "important_decision", "asset_snapshots"}
        }
        asset_snapshots = prepare_asset_snapshots(
            raw.get("asset_snapshots"),
            stage,
            title,
            snapshots_root,
            underlying,
            position,
            previous_asset_state,
        )
        packaged_path = f"trajectory/intermediate/{destination_name}"
        cleaned.update(
            {
                "stage": stage,
                "title": title,
                "action": action,
                "decision": decision,
                "snapshot": packaged_path,
                "snapshot_evidence": {
                    **evidence,
                    "manifest_reference": reference,
                    "packaged_path": packaged_path,
                    "copied_byte_for_byte": True,
                    "same_bytes_as_previous_step": previous_sha == evidence["sha256"],
                },
            }
        )
        if "asset_snapshots" in raw:
            cleaned["asset_snapshots"] = asset_snapshots
        prepared.append(cleaned)
        previous_stage = stage
        previous_sha = evidence["sha256"]
    return prepared


def build_actions(task: dict[str, Any], steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    existing = task.get("adobe_actions")
    if isinstance(existing, list):
        return existing
    actions: list[dict[str, Any]] = []
    for step in steps:
        if step["action"] == "source_inspection":
            continue
        action: dict[str, Any] = {
            "stage": step["stage"],
            "connector": step.get("connector", "Adobe"),
            "action": step["action"],
            "parameters": step.get("parameters", {}),
            "snapshot": step["snapshot"],
        }
        if step.get("request_id"):
            action["request_id"] = step["request_id"]
        actions.append(action)
    return actions


def normalize_retries(task: dict[str, Any]) -> list[Any]:
    retries = task.get("retries")
    if isinstance(retries, list):
        return retries
    shared = task.get("shared_failures_and_recovery")
    return shared if isinstance(shared, list) else []


def build_trajectory(task: dict[str, Any], steps: list[dict[str, Any]], generated_at: str) -> dict[str, Any]:
    trajectory: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "task_id": task["task_id"],
        "title": task["title"],
        "generated_at": generated_at,
        "evidence_policy": {
            "snapshot_requirement": (
                "Every step is backed by a decoded local primary image; every declared underlying asset "
                "snapshot is also decoded and packaged."
            ),
            "ordering": "Manifest order is preserved and numeric stages are strictly increasing.",
            "copy_integrity": (
                "Packaged primary and underlying asset snapshots are byte-for-byte copies verified by SHA-256."
            ),
            "claim_scope": (
                "The builder verifies snapshot files, ordering, dimensions, byte counts, and hashes. "
                "Action names, parameters, decisions, timestamps, and request IDs are manifest-supplied claims."
            ),
            "contact_sheet_scope": (
                "Each primary snapshot is the manifest-supplied stage contact sheet or decision card. "
                "The generated aggregate contact sheet is a labeled derivative visual index, not an Adobe output."
            ),
        },
    }
    if task.get("task_key"):
        trajectory["task_key"] = task["task_key"]
    for field in PRESERVED_FIELDS:
        if field in task:
            trajectory[field] = task[field]
    trajectory["retries"] = normalize_retries(task)
    trajectory["adobe_actions"] = build_actions(task, steps)
    trajectory["trajectory_steps"] = steps
    trajectory["intermediate_snapshot"] = steps[-1]["snapshot"]
    trajectory["evidence_artifacts"] = {
        "contact_sheet_image": "trajectory/contact-sheet.png",
        "contact_sheet_report": "trajectory/contact-sheet.html",
        "decision_evidence_report": "trajectory/decision-evidence.html",
        "trajectory_report": "trajectory/trajectory.html",
        "trajectory_markdown": "trajectory/trajectory.md",
    }
    return trajectory


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


def markdown_code(value: Any) -> str:
    serialized = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True)
    return serialized.replace("`", "\\`")


def report_reference_path(reference: str) -> str:
    """Return a package-root reference relative to reports stored inside trajectory/."""
    return reference[len("trajectory/") :] if reference.startswith("trajectory/") else reference


def report_snapshot_path(step: dict[str, Any]) -> str:
    return report_reference_path(str(step["snapshot"]))


def write_markdown(path: Path, trajectory: dict[str, Any]) -> None:
    lines = [
        f"# {trajectory['task_id']} trajectory evidence",
        "",
        f"**Title:** {trajectory['title']}",
        "",
        (
            "**Evidence boundary:** Every step below has a decoded local snapshot copied byte-for-byte into "
            "this package. The manifest—not this builder—is the source for action, parameter, decision, "
            "timestamp, and request-ID claims."
        ),
        "",
    ]
    for label, field in (("Intent", "intent"), ("Source binding", "source_binding"), ("Status", "status")):
        if trajectory.get(field):
            lines.extend((f"**{label}:** {trajectory[field]}", ""))
    lines.extend(
        (
            "[Contact sheet](contact-sheet.png) · [Contact sheet report](contact-sheet.html) · "
            "[Decision evidence](decision-evidence.html)",
            "",
            "## Ordered snapshot trajectory",
            "",
        )
    )
    for step in trajectory["trajectory_steps"]:
        evidence = step["snapshot_evidence"]
        report_snapshot = report_snapshot_path(step)
        lines.extend(
            (
                f"### Stage {step['stage']} — {step['title']}",
                "",
                f"![Stage {step['stage']}: {step['title']}]({report_snapshot})",
                "",
                f"- **Action:** `{markdown_code(step['action'])}`",
                f"- **Decision:** {step['decision']}",
            )
        )
        if "parameters" in step:
            lines.append(f"- **Parameters:** `{markdown_code(step['parameters'])}`")
        if step.get("reasoning") or step.get("rationale"):
            lines.append(f"- **Reasoning:** {step.get('reasoning') or step.get('rationale')}")
        if step.get("request_id"):
            lines.append(f"- **Request ID (manifest supplied):** `{markdown_code(step['request_id'])}`")
        lines.extend(
            (
                f"- **Snapshot:** `{step['snapshot']}` — {evidence['pixels'][0]}×{evidence['pixels'][1]} "
                f"{evidence['format']}, {evidence['bytes']:,} bytes",
                f"- **SHA-256:** `{evidence['sha256']}`",
                f"- **Same bytes as prior step:** `{str(evidence['same_bytes_as_previous_step']).lower()}`",
                "",
            )
        )
        asset_snapshots = step.get("asset_snapshots") or []
        if asset_snapshots:
            lines.extend((f"#### Underlying asset snapshots ({len(asset_snapshots)})", ""))
            for asset in asset_snapshots:
                asset_evidence = asset["snapshot_evidence"]
                asset_link = report_reference_path(asset["path"])
                lines.extend(
                    (
                        f"- [{asset['name']}]({asset_link}) — asset `{markdown_code(asset['asset_id'])}`; "
                        f"{asset_evidence['pixels'][0]}×{asset_evidence['pixels'][1]} "
                        f"{asset_evidence['format']}; `{asset_evidence['sha256']}`",
                    )
                )
            lines.append("")
    retries = trajectory.get("retries") or []
    if retries:
        lines.extend(("## Recorded retries and recovery", ""))
        for retry in retries:
            lines.append(f"- `{markdown_code(retry)}`")
        lines.append("")
    if trajectory.get("reasoning_summary"):
        lines.extend(("## Reasoning summary", "", str(trajectory["reasoning_summary"]), ""))
    path.write_text("\n".join(lines), encoding="utf-8")


def html_document(title: str, body: str, extra_css: str = "") -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>
:root{{--ink:#17211d;--muted:#647069;--line:#d8ded9;--paper:#f5f6f3;--card:#fff;--accent:#184f3d}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
main{{max-width:1180px;margin:auto;padding:38px 28px 72px}}a{{color:var(--accent)}}h1{{font-size:30px;line-height:1.15;margin:0 0 8px}}h2{{margin-top:34px}}code,pre{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}code{{overflow-wrap:anywhere}}.lede{{color:var(--muted);max-width:900px}}.notice{{padding:14px 16px;border-left:4px solid var(--accent);background:#e8efe9;margin:20px 0}}.links{{display:flex;gap:12px;flex-wrap:wrap;margin:20px 0}}.links a{{padding:7px 10px;background:#fff;border:1px solid var(--line);border-radius:5px;text-decoration:none}}.timeline{{display:grid;gap:18px}}.step{{background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}}.step-head{{display:flex;justify-content:space-between;gap:15px;padding:14px 18px;border-bottom:1px solid var(--line)}}.step-head h2{{font-size:18px;margin:0}}.stage{{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}}.step-body{{display:grid;grid-template-columns:minmax(280px,46%) minmax(0,1fr);gap:20px;padding:18px}}.snapshot img{{display:block;width:100%;max-height:440px;object-fit:contain;background:#eceeeb}}.details dl{{display:grid;grid-template-columns:130px 1fr;gap:8px 12px;margin:0}}.details dt{{color:var(--muted);font-size:12px;font-weight:700;text-transform:uppercase}}.details dd{{margin:0;overflow-wrap:anywhere}}pre{{margin:0;padding:10px;overflow:auto;background:#f0f2ef;border-radius:5px;white-space:pre-wrap}}.hash{{font-size:11px}}.badge{{display:inline-block;padding:3px 8px;border-radius:99px;background:#e8efe9;font-size:11px;font-weight:700}}.asset-section{{padding:0 18px 18px}}.asset-section h3{{font-size:14px;margin:2px 0 10px}}.asset-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px}}.asset-card{{min-width:0;padding:9px;border:1px solid var(--line);border-radius:7px;background:#f8f9f7}}.asset-card img{{display:block;width:100%;height:130px;object-fit:contain;background:#eceeeb}}.asset-name{{margin:7px 0 2px;font-weight:700;overflow-wrap:anywhere}}.asset-meta{{margin:2px 0;color:var(--muted);font-size:11px;overflow-wrap:anywhere}}.asset-card details{{font-size:11px}}table{{width:100%;border-collapse:collapse;background:#fff}}th,td{{padding:10px;border:1px solid var(--line);text-align:left;vertical-align:top}}th{{background:#eef1ed}}@media(max-width:760px){{main{{padding:25px 16px}}.step-body{{grid-template-columns:1fr}}.details dl{{grid-template-columns:1fr}}}}
{extra_css}</style></head><body><main>{body}</main></body></html>"""


def asset_snapshot_html(asset: dict[str, Any]) -> str:
    evidence = asset["snapshot_evidence"]
    report_path = report_reference_path(asset["path"])
    optional = []
    for label, field in (
        ("Status", "status"),
        ("Request ID", "request_id"),
        ("Input URL", "input_url"),
        ("Output URL", "output_url"),
    ):
        if asset.get(field):
            optional.append(f"<div class='asset-meta'><strong>{label}:</strong> <code>{html.escape(str(asset[field]))}</code></div>")
    parameters = ""
    if "parameters" in asset:
        value = html.escape(json.dumps(asset["parameters"], ensure_ascii=False, indent=2, sort_keys=True))
        parameters = f"<details><summary>Parameters</summary><pre>{value}</pre></details>"
    duplicate = (
        " · unchanged bytes from prior state"
        if evidence.get("same_bytes_as_previous_asset_state")
        else ""
    )
    return (
        f"<article class='asset-card'><a href='{html.escape(report_path, quote=True)}'>"
        f"<img loading='lazy' src='{html.escape(report_path, quote=True)}' alt='{html.escape(asset['name'], quote=True)}'></a>"
        f"<div class='asset-name'>{html.escape(asset['name'])}</div>"
        f"<div class='asset-meta'>Asset <code>{html.escape(asset['asset_id'])}</code>{duplicate}</div>"
        f"<div class='asset-meta'>{evidence['pixels'][0]}×{evidence['pixels'][1]} {html.escape(evidence['format'])}</div>"
        f"<div class='asset-meta hash'><code>{evidence['sha256']}</code></div>{''.join(optional)}{parameters}</article>"
    )


def asset_gallery_html(step: dict[str, Any]) -> str:
    assets = step.get("asset_snapshots") or []
    if not assets:
        return ""
    cards = "".join(asset_snapshot_html(asset) for asset in assets)
    return (
        f"<section class='asset-section'><h3>Underlying asset snapshots ({len(assets)})</h3>"
        f"<div class='asset-grid'>{cards}</div></section>"
    )


def step_html(step: dict[str, Any]) -> str:
    evidence = step["snapshot_evidence"]
    report_snapshot = report_snapshot_path(step)
    parameters = ""
    if "parameters" in step:
        parameters = (
            "<dt>Parameters</dt><dd><pre>"
            + html.escape(json.dumps(step["parameters"], ensure_ascii=False, indent=2, sort_keys=True))
            + "</pre></dd>"
        )
    reasoning = step.get("reasoning") or step.get("rationale")
    reasoning_html = f"<dt>Reasoning</dt><dd>{html.escape(str(reasoning))}</dd>" if reasoning else ""
    request_html = (
        f"<dt>Request ID</dt><dd><code>{html.escape(str(step['request_id']))}</code> "
        "<span class='badge'>manifest supplied</span></dd>"
        if step.get("request_id")
        else ""
    )
    duplicate = (
        " <span class='badge'>same bytes as prior step</span>"
        if evidence["same_bytes_as_previous_step"]
        else ""
    )
    asset_gallery = asset_gallery_html(step)
    return f"""<article class="step">
<div class="step-head"><div><div class="stage">Stage {step['stage']}</div><h2>{html.escape(step['title'])}</h2></div><code>{html.escape(step['action'])}</code></div>
<div class="step-body"><div class="snapshot"><a href="{html.escape(report_snapshot, quote=True)}"><img loading="lazy" src="{html.escape(report_snapshot, quote=True)}" alt="Stage {step['stage']}: {html.escape(step['title'], quote=True)}"></a></div>
<div class="details"><dl><dt>Decision</dt><dd>{html.escape(step['decision'])}</dd>{reasoning_html}{parameters}{request_html}
<dt>Snapshot</dt><dd><code>{html.escape(step['snapshot'])}</code>{duplicate}</dd>
<dt>Measured</dt><dd>{evidence['pixels'][0]}×{evidence['pixels'][1]} {html.escape(evidence['format'])}; {evidence['bytes']:,} bytes</dd>
<dt>SHA-256</dt><dd class="hash"><code>{evidence['sha256']}</code></dd>
<dt>Integrity</dt><dd>Decoded successfully; packaged copy matches the source bytes.</dd></dl></div></div>{asset_gallery}</article>"""


def report_header(trajectory: dict[str, Any], heading: str) -> str:
    intent = f"<p><strong>Intent:</strong> {html.escape(str(trajectory['intent']))}</p>" if trajectory.get("intent") else ""
    return f"""<h1>{html.escape(heading)}</h1><p class="lede">{html.escape(str(trajectory['title']))}</p>{intent}
<div class="notice"><strong>Evidence boundary.</strong> Each ordered step has a decoded primary stage card. Every declared underlying asset snapshot is also decoded, measured, and copied byte-for-byte. Tool actions, settings, decisions, timestamps, URLs, and request IDs are transcribed from the supplied manifest; they are not independently inferred from pixels.</div>
<nav class="links"><a href="trajectory.html">Trajectory</a><a href="contact-sheet.html">Contact sheet</a><a href="decision-evidence.html">Decision evidence</a><a href="trajectory.json">JSON</a><a href="trajectory.md">Markdown</a></nav>"""


def write_trajectory_html(path: Path, trajectory: dict[str, Any]) -> None:
    steps = "".join(step_html(step) for step in trajectory["trajectory_steps"])
    body = report_header(trajectory, f"{trajectory['task_id']} trajectory") + f'<section class="timeline">{steps}</section>'
    path.write_text(html_document(f"{trajectory['task_id']} trajectory", body), encoding="utf-8")


def write_decision_html(path: Path, trajectory: dict[str, Any]) -> None:
    rows = []
    for step in trajectory["trajectory_steps"]:
        evidence = step["snapshot_evidence"]
        report_snapshot = report_snapshot_path(step)
        parameters = html.escape(json.dumps(step.get("parameters", {}), ensure_ascii=False, sort_keys=True))
        rows.append(
            "<tr>"
            f"<td>{step['stage']}</td><td><a href=\"{html.escape(report_snapshot, quote=True)}\">{html.escape(step['title'])}</a></td>"
            f"<td><code>{html.escape(step['action'])}</code><br><code>{parameters}</code></td>"
            f"<td>{html.escape(step['decision'])}</td>"
            f"<td>{evidence['pixels'][0]}×{evidence['pixels'][1]}<br><code class=\"hash\">{evidence['sha256']}</code></td>"
            "</tr>"
        )
    body = report_header(trajectory, f"{trajectory['task_id']} decision evidence") + (
        "<p class='lede'>One manifest-recorded decision is bound to each measured snapshot. Row order is the supplied stage order.</p>"
        "<div style='overflow:auto'><table><thead><tr><th>Stage</th><th>Snapshot</th><th>Action / parameters</th><th>Decision</th><th>File evidence</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table></div>"
    )
    path.write_text(html_document(f"{trajectory['task_id']} decision evidence", body), encoding="utf-8")


def write_contact_html(path: Path, trajectory: dict[str, Any]) -> None:
    cards = []
    for step in trajectory["trajectory_steps"]:
        evidence = step["snapshot_evidence"]
        report_snapshot = report_snapshot_path(step)
        asset_gallery = asset_gallery_html(step)
        cards.append(
            f"<article class='step'><div class='step-head'><div><div class='stage'>Stage {step['stage']}</div><h2>{html.escape(step['title'])}</h2></div></div>"
            f"<div style='padding:14px'><a href='{html.escape(report_snapshot, quote=True)}'><img loading='lazy' src='{html.escape(report_snapshot, quote=True)}' alt='{html.escape(step['title'], quote=True)}' style='width:100%;height:300px;object-fit:contain;background:#eceeeb'></a>"
            f"<p>{html.escape(step['decision'])}</p><p class='hash'><code>{evidence['sha256']}</code></p></div>{asset_gallery}</article>"
        )
    css = ".contact-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:16px}.contact-grid .step h2{margin:0}"
    body = report_header(trajectory, f"{trajectory['task_id']} contact sheet") + (
        "<p class='lede'>Derived visual index only. Each large image is the primary stage card; any underlying asset snapshots are linked beneath it.</p>"
        f"<section class='contact-grid'>{''.join(cards)}</section>"
    )
    path.write_text(html_document(f"{trajectory['task_id']} contact sheet", body, css), encoding="utf-8")


def find_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def wrapped_lines(draw: ImageDraw.ImageDraw, value: str, font: ImageFont.ImageFont, width: int, limit: int) -> list[str]:
    words = value.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textbbox((0, 0), trial, font=font)[2] <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
        if len(lines) >= limit:
            break
    if current and len(lines) < limit:
        lines.append(current)
    if len(lines) == limit and " ".join(lines) != value:
        lines[-1] = lines[-1].rstrip(" .") + "…"
    return lines


def write_contact_sheet_png(path: Path, trajectory: dict[str, Any], output_root: Path) -> None:
    steps = trajectory["trajectory_steps"]
    columns = 1 if len(steps) == 1 else 2
    canvas_width = 1600
    margin = 54
    gap = 28
    header_height = 150
    card_width = (canvas_width - 2 * margin - gap * (columns - 1)) // columns
    card_height = 560
    rows = (len(steps) + columns - 1) // columns
    canvas_height = header_height + rows * card_height + max(rows - 1, 0) * gap + margin
    canvas = Image.new("RGB", (canvas_width, canvas_height), "#f2f4f0")
    draw = ImageDraw.Draw(canvas)
    title_font = find_font(34, bold=True)
    subtitle_font = find_font(17)
    card_title_font = find_font(22, bold=True)
    body_font = find_font(15)
    tiny_font = find_font(12)
    draw.text((margin, 38), f"{trajectory['task_id']} · ordered trajectory evidence", fill="#17211d", font=title_font)
    draw.text(
        (margin, 88),
        "DERIVED VISUAL INDEX · originals are copied byte-for-byte; action and decision text comes from the manifest",
        fill="#526159",
        font=subtitle_font,
    )

    for index, step in enumerate(steps):
        row, column = divmod(index, columns)
        left = margin + column * (card_width + gap)
        top = header_height + row * (card_height + gap)
        right = left + card_width
        bottom = top + card_height
        draw.rounded_rectangle((left, top, right, bottom), radius=14, fill="#ffffff", outline="#d4dbd5", width=2)
        draw.text((left + 22, top + 18), f"STAGE {step['stage']}", fill="#527064", font=tiny_font)
        draw.text((left + 22, top + 42), step["title"], fill="#17211d", font=card_title_font)
        image_box = (left + 22, top + 82, right - 22, top + 402)
        draw.rectangle(image_box, fill="#e9ece8")
        source = output_root / report_snapshot_path(step)
        with Image.open(source) as image:
            visual = ImageOps.exif_transpose(image).convert("RGB")
            visual.thumbnail((image_box[2] - image_box[0], image_box[3] - image_box[1]), Image.Resampling.LANCZOS)
            image_left = image_box[0] + (image_box[2] - image_box[0] - visual.width) // 2
            image_top = image_box[1] + (image_box[3] - image_box[1] - visual.height) // 2
            canvas.paste(visual, (image_left, image_top))
        y = top + 420
        draw.text((left + 22, y), step["action"], fill="#184f3d", font=body_font)
        y += 28
        for line in wrapped_lines(draw, step["decision"], body_font, card_width - 44, 3):
            draw.text((left + 22, y), line, fill="#313d37", font=body_font)
            y += 22
        evidence = step["snapshot_evidence"]
        asset_count = len(step.get("asset_snapshots") or [])
        asset_label = f" · {asset_count} underlying asset{'s' if asset_count != 1 else ''}" if asset_count else ""
        footer = (
            f"{evidence['pixels'][0]}×{evidence['pixels'][1]} · {evidence['format']}"
            f"{asset_label} · sha256 {evidence['sha256'][:16]}…"
        )
        draw.text((left + 22, bottom - 28), footer, fill="#6b756f", font=tiny_font)
    canvas.save(path, "PNG", optimize=True)


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def managed_files(staging: Path) -> list[str]:
    return sorted(
        str(path.relative_to(staging))
        for path in staging.rglob("*")
        if path.is_file() and path.name != MANAGED_MARKER
    )


def install_staging(staging: Path, output_dir: Path, replace: bool, generated_at: str) -> None:
    existing_entries = list(output_dir.iterdir()) if output_dir.is_dir() else []
    if output_dir.exists() and not output_dir.is_dir():
        raise EvidenceBuildError(f"Output path exists and is not a directory: {output_dir}")
    if existing_entries and not replace:
        raise EvidenceBuildError(
            f"Output directory is not empty: {output_dir}. Use --replace to overwrite builder-managed files."
        )

    new_managed = managed_files(staging)
    old_managed: list[str] = []
    marker = output_dir / MANAGED_MARKER
    if replace and marker.is_file():
        try:
            marker_data = json.loads(marker.read_text(encoding="utf-8"))
            if isinstance(marker_data.get("managed_files"), list):
                old_managed = [item for item in marker_data["managed_files"] if isinstance(item, str)]
        except (json.JSONDecodeError, OSError):
            old_managed = []

    output_dir.mkdir(parents=True, exist_ok=True)
    for relative in new_managed:
        source = staging / relative
        destination = output_dir / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        os.replace(source, destination)

    # Remove only stale files explicitly recorded as managed by an earlier build.
    for relative in sorted(set(old_managed) - set(new_managed)):
        candidate = (output_dir / relative).resolve()
        try:
            candidate.relative_to(output_dir.resolve())
        except ValueError:
            continue
        if candidate.is_file():
            candidate.unlink()

    write_json(
        marker,
        {
            "schema_version": SCHEMA_VERSION,
            "generated_at": generated_at,
            "managed_files": new_managed,
        },
    )


def build(
    manifest_path: Path,
    output_dir: Path,
    task_key: str | None = None,
    snapshots_root: Path | None = None,
    replace: bool = False,
    generated_at: str | None = None,
) -> dict[str, Any]:
    manifest_path = manifest_path.resolve()
    manifest = load_json(manifest_path)
    task = select_task(manifest, task_key)
    snapshot_base = (snapshots_root or manifest_path.parent).resolve()
    if not snapshot_base.is_dir():
        raise EvidenceBuildError(f"Snapshot root is not a directory: {snapshot_base}")
    output_dir = output_dir.resolve()
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    generated = generated_at or utc_now()
    staging = Path(tempfile.mkdtemp(prefix=".trajectory-evidence-", dir=str(output_dir.parent)))
    try:
        intermediate = staging / "intermediate"
        intermediate.mkdir()
        underlying = staging / "underlying"
        steps = validate_and_prepare_steps(task, snapshot_base, intermediate, underlying)
        trajectory = build_trajectory(task, steps, generated)
        write_json(staging / "trajectory.json", trajectory)
        write_markdown(staging / "trajectory.md", trajectory)
        write_trajectory_html(staging / "trajectory.html", trajectory)
        write_contact_html(staging / "contact-sheet.html", trajectory)
        write_decision_html(staging / "decision-evidence.html", trajectory)
        write_contact_sheet_png(staging / "contact-sheet.png", trajectory, staging)
        install_staging(staging, output_dir, replace, generated)
        return trajectory
    finally:
        shutil.rmtree(staging, ignore_errors=True)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    result.add_argument("--manifest", required=True, type=Path, help="JSON manifest containing steps or a tasks map")
    result.add_argument("--task", help="Task key when the manifest contains a tasks map")
    result.add_argument(
        "--snapshots-root",
        type=Path,
        help="Root for relative snapshot paths (default: manifest directory)",
    )
    result.add_argument("--output-dir", required=True, type=Path, help="Trajectory output directory")
    result.add_argument(
        "--replace",
        action="store_true",
        help="Overwrite generated files; only stale files listed by a prior builder marker are removed",
    )
    result.add_argument("--generated-at", help=argparse.SUPPRESS)
    return result


def main(argv: Iterable[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        trajectory = build(
            manifest_path=args.manifest,
            output_dir=args.output_dir,
            task_key=args.task,
            snapshots_root=args.snapshots_root,
            replace=args.replace,
            generated_at=args.generated_at,
        )
    except EvidenceBuildError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(
        f"Built {len(trajectory['trajectory_steps'])} snapshot-bearing steps for "
        f"{trajectory['task_id']} in {args.output_dir.resolve()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
