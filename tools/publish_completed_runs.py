#!/usr/bin/env python3
"""Publish completed benchmark runs into the static Gatsby V5 site."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any

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
                "evidence": "The run advanced steadily, but included an avoidable batch/preset retry and one crop-quality parameter retry before the accepted exports.",
            },
            "K6_Q5": {
                "grade": "Pass",
                "evidence": "The agent detected the rejected crop quality and center-crop fallback, corrected the parameter, then visually checked the resulting compositions.",
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
                "evidence": "The work progressed to completion, but the initial all-image preset batch returned no results and had to be rerun in smaller chunks.",
            },
            "K6_Q5": {
                "grade": "Pass",
                "evidence": "The zero-result batch and Adobe PDF parsing failure were detected; image processing was retried in chunks and approved task-register sources were used for print specifications.",
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
    for output in manifest["outputs"]:
        src = source / output["path"]
        if not src.is_file():
            raise FileNotFoundError(src)
        shutil.copy2(src, destination / output["path"])
    for name in ("trajectory.json", "trajectory.md", "trajectory.html"):
        shutil.copy2(source / "trajectory" / name, destination / "trajectory" / name)
    intermediate = source / "trajectory" / "intermediate" / cfg["intermediate"]
    shutil.copy2(intermediate, destination / "trajectory" / "intermediate" / intermediate.name)
    for name in ("manifest.json", "README.md"):
        shutil.copy2(source / name, destination / name)
    package = source_root / "packages" / cfg["package"]
    shutil.copy2(package, destination / "package" / package.name)
    return destination, manifest, load_json(source / "trajectory" / "trajectory.json")


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
    return {
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
"""


JS_HELPERS = r"""
const formatBytes=n=>{if(!n)return '';const u=['B','KB','MB','GB'];let i=0,v=n;while(v>=1024&&i<u.length-1){v/=1024;i++;}return `${v.toFixed(i?1:0)} ${u[i]}`;};
const specLine=o=>Object.entries(o.spec||{}).filter(([k])=>['format','width','height','width_mm','height_mm','pages','duration_seconds','ratio','audio'].includes(k)).map(([k,v])=>`${k}: ${typeof v==='object'?JSON.stringify(v):v}`).join('; ');
function outputCard(o){const url=o.artifact_url||'';const image=/\.(png|jpe?g|webp|gif)$/i.test(url);const pdf=/\.pdf$/i.test(url);const preview=image?`<a href="${esc(url)}" target="_blank" rel="noopener"><img loading="lazy" src="${esc(url)}" alt="${esc(o.name)}"></a>`:pdf?`<iframe loading="lazy" title="${esc(o.name)} PDF preview" src="${esc(url)}#view=FitH&toolbar=0"></iframe>`:'';const actual=o.actual_pixels?`${o.actual_pixels[0]} x ${o.actual_pixels[1]} px`:o.actual_pages?`${o.actual_pages} page${o.actual_pages===1?'':'s'}`:'';return `<article class="output-card">${preview}<div class="output-card-body"><h3>${esc(o.name)}</h3><span class="result-badge ${o.verification==='passed'?'result-pass':'result-pending'}">${esc(o.verification||o.status||'pending')}</span><p class="output-meta"><code>${esc(o.path)}</code><br>${esc(actual||specLine(o))}${o.bytes?` · ${esc(formatBytes(o.bytes))}`:''}${o.sha256?`<span class="output-hash" title="${esc(o.sha256)}">SHA-256 ${esc(o.sha256)}</span>`:''}</p><div class="output-links">${url?`<a href="${esc(url)}" target="_blank" rel="noopener">Open</a><a href="${esc(url)}" download>Download</a>`:''}</div></div></article>`;}
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
    new_trajectory = "const scores=Object.fromEntries((t.run?.trajectory_scores||[]).map(x=>[x.question_id,x]));html+=(k6?k6.questions:[]).map(q=>{const s=scores[q.id];return `<div class=\"k-question\"><h3>${esc(kShort(q.id))} · ${esc(q.label)}${objBadge(q)}</h3><p class=\"k-qtext\">${esc(q.question)}</p><details class=\"expected-copy\"><summary>Grading guide</summary><p><strong>Pass:</strong> ${esc(q.grades?.pass)}</p><p><strong>Minor:</strong> ${esc(q.grades?.minor)}</p><p><strong>Major:</strong> ${esc(q.grades?.major)}</p></details>${s?`<div class=\"trajectory-result\"><span class=\"trajectory-grade grade-${esc(s.grade.toLowerCase())}\">${esc(s.grade)}</span><p>${esc(s.evidence)}</p></div>`:'<p class=\"k-pending\">Pending: populated from the run trajectory after the task is executed.</p>'}</div>`;}).join('');if(t.run){const l=t.run.links;html+=`<div class=\"intermediate-card\"><a href=\"${esc(t.run.intermediate_snapshot)}\" target=\"_blank\"><img loading=\"lazy\" src=\"${esc(t.run.intermediate_snapshot)}\" alt=\"Intermediate run snapshot\"></a><div><h3>Intermediate snapshot and full trajectory</h3><p>This snapshot records the asset after Adobe tone treatment and before final layout/export. The complete trajectory includes source/output bindings, Adobe actions, retries, and concise decision summaries.</p><div class=\"run-actions\"><a href=\"${esc(l.trajectory_report)}\" target=\"_blank\">Open trajectory report</a><a href=\"${esc(l.trajectory_json)}\" target=\"_blank\">Trajectory JSON</a><a href=\"${esc(l.trajectory_markdown)}\" target=\"_blank\">Trajectory Markdown</a></div></div></div>`;}"
    html = html.replace(old_trajectory, new_trajectory, 1)

    old_release = "if(section==='Release gates')html=`<p class=\"status\">Release held pending validation</p>${table(['Gate','State'],Object.entries(t.readiness).filter(([k,v])=>typeof v==='string').map(([k,v])=>[esc(k.replaceAll('_',' ')),esc(v)]))}<h3>Open prerequisites</h3>${t.readiness.blockers.length?`<ul>${t.readiness.blockers.map(b=>`<li>${esc(b)}</li>`).join('')}</ul>`:'<p>No additional source prerequisite was detected by structural checks. Visual review and connector trials remain required.</p>'}<h3>Record exclusions</h3>${t.exclusions.length?table(['Group','Source row','Reason'],t.exclusions.map(e=>[esc(e.group),`${esc(e.table)}, row ${e.row_number}`,esc(e.reason)])):'<p>No rule-based exclusions were made.</p>'}`;"
    new_release = "if(section==='Release gates')html=`<p class=\"status\">${t.run?'Run complete · independent creative review pending':'Release held pending validation'}</p>${table(['Gate','State'],Object.entries(t.readiness).filter(([k,v])=>typeof v==='string').map(([k,v])=>[esc(k.replaceAll('_',' ')),esc(v)]))}<h3>Open prerequisites</h3>${t.readiness.blockers.length?`<ul>${t.readiness.blockers.map(b=>`<li>${esc(b)}</li>`).join('')}</ul>`:t.run?'<p>Contracted artifacts and connector execution are complete. Independent creative review remains pending.</p>':'<p>No additional source prerequisite was detected by structural checks. Visual review and connector trials remain required.</p>'}<h3>Record exclusions</h3>${t.exclusions.length?table(['Group','Source row','Reason'],t.exclusions.map(e=>[esc(e.group),`${esc(e.table)}, row ${e.row_number}`,esc(e.reason)])):'<p>No rule-based exclusions were made.</p>'}`;"
    html = html.replace(old_release, new_release, 1)

    required_fragments = [new_check_rows, new_toolbar, new_heading, new_outputs, new_trajectory, new_release]
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
