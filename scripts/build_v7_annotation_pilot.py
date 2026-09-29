#!/usr/bin/env python3
"""Build standalone pilot briefs and the matching annotation-sheet import rows."""

from __future__ import annotations

import html
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "docs/gatsby-v7/tasks"
OUT = ROOT / "docs/gatsby-v7/annotation-pilot"
RUN_SOURCES = ROOT.parents[1] / "benchmark_runs/pilot_v7_hybrid_2026-09-28"
SHEET_EXPORT = ROOT.parents[1] / "benchmark_runs/annotation_pilot_2026-09-29/sheet_rows.json"
BASE_URL = "https://dhigdec.github.io/creative-ai-benchmark/gatsby-v7/annotation-pilot/"
TASK_IDS = [
    "PHOTO-04", "PHOTO-06", "PHOTO-08", "PHOTO-10", "PHOTO-19",
    "PHOTO-20", "PHOTO-24", "PHOTO-26", "PHOTO-28", "LAYOUT-15",
]
RUBRICS = [
    "1. Completeness", "2. Feasibility Integrity", "3. Realism / Difficulty",
    "4. Brand Coherence", "5. No-Answer Leakage", "6. Provenance / Licensing",
    "7. Decision Quality", "8. Hallucination / Contradiction",
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def label(key: str) -> str:
    special = {
        "founded_place_size": "Origin and scale",
        "brand_assets_status": "Brand assets",
        "price_positioning": "Price positioning",
        "type_system": "Type system",
        "palette_rules": "Palette rules",
        "signature_type_move": "Signature type move",
    }
    return special.get(key, key.replace("_", " ").capitalize())


def render_value(value: object) -> str:
    if isinstance(value, dict):
        return '<dl class="detail-list">' + "".join(
            f"<div><dt>{esc(label(key))}</dt><dd>{render_value(item)}</dd></div>"
            for key, item in value.items()
        ) + "</dl>"
    if isinstance(value, list):
        return '<ul class="data-list">' + "".join(
            f"<li>{render_value(item)}</li>" for item in value
        ) + "</ul>"
    return f"<span>{esc(value)}</span>"


def render_brand(brand: dict) -> str:
    simple = [
        "sector", "founded_place_size", "about", "personality", "audience",
        "price_positioning", "values", "voice", "brand_assets_status",
    ]
    parts = [
        f'<p class="brand-name">{esc(brand["brand_name"])}</p>',
        f'<p class="tagline">{esc(brand["tagline"])}</p>',
        '<dl class="brand-facts">',
    ]
    for key in simple:
        parts.append(f"<div><dt>{esc(label(key))}</dt><dd>{render_value(brand[key])}</dd></div>")
    parts.append("</dl>")
    parts.append('<h3>Colour palette</h3><div class="palette-grid">')
    for colour in brand["palette"]:
        code = colour["hex"]
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", code):
            raise ValueError(f"Invalid brand hex: {code}")
        parts.append(
            '<div class="palette-item">'
            f'<span class="swatch" style="background:{code}"></span>'
            f'<div><strong>{esc(colour["name"])}</strong> <code>{esc(code)}</code>'
            f'<small>{esc(colour["role"])}</small><p>{esc(colour["usage"])}</p></div></div>'
        )
    parts.append("</div>")
    parts.append(f'<h3>Palette rules</h3>{render_value(brand["palette_rules"])}')
    parts.append('<h3>Typography</h3>')
    parts.append(f'<p>{esc(brand["typography"])}</p>')
    parts.append(f'<p><strong>Signature move:</strong> {esc(brand["signature_type_move"])}</p>')
    parts.append(f'<p><strong>Display face:</strong> {esc(brand["display_face"])}</p>')
    parts.append(f'<div class="type-system">{render_value(brand["type_system"])}</div>')
    return "".join(parts)


def source_preview(task_id: str, asset: dict) -> str:
    name = asset["filename"]
    suffix = Path(name).suffix.lower()
    url = esc(asset["public_url"])
    if suffix in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}:
        return f'<img loading="lazy" src="{url}" alt="Preview of {esc(name)}">'
    local_file = RUN_SOURCES / task_id / "source" / name
    if suffix == ".pdf" and local_file.is_file():
        preview = OUT / "previews" / f"{task_id}-{Path(name).stem}.png"
        if not preview.exists():
            preview.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                ["pdftoppm", "-f", "1", "-singlefile", "-scale-to", "480",
                 "-png", str(local_file), str(preview.with_suffix(""))],
                check=True, stdout=subprocess.DEVNULL,
            )
        return f'<img loading="lazy" src="previews/{esc(preview.name)}" alt="First page of {esc(name)}">'
    if suffix in {".csv", ".txt"} and local_file.is_file():
        sample = "\n".join(local_file.read_text(encoding="utf-8-sig", errors="replace").splitlines()[:6])
        return f'<pre class="file-excerpt">{esc(sample[:500])}</pre>'
    return f'<span class="file-icon">{esc(suffix.lstrip(".").upper())}</span>'


def render_assets(task_id: str, assets: list[dict]) -> str:
    parts = ['<div class="asset-grid">']
    for asset in assets:
        name = asset["filename"]
        url = esc(asset["public_url"])
        size = (f'{asset["bytes"] / 1024:.1f} KB' if asset["bytes"] < 1024 * 1024
                else f'{asset["bytes"] / 1024 / 1024:.2f} MB')
        parts.append(
            '<article class="asset-card">'
            f'<a class="asset-preview" href="{url}" target="_blank" rel="noopener noreferrer" '
            f'aria-label="Open {esc(name)} in a new tab">{source_preview(task_id, asset)}</a>'
            '<div class="asset-info">'
            f'<strong title="{esc(name)}">{esc(name)}</strong>'
            f'<p>{esc(asset["role"].replace("_", " ").capitalize())} · {size}</p>'
            '<div class="asset-actions">'
            f'<a href="{url}" target="_blank" rel="noopener noreferrer">Open</a>'
            f'<a href="{url}" download="{esc(name)}" data-download>Download</a>'
            '</div></div></article>'
        )
    parts.append("</div>")
    return "".join(parts)


def render_outputs(outputs: list[dict], groups: list[dict]) -> str:
    group_names = {group["id"]: group["name"] for group in groups}
    parts = ['<div class="outputs">']
    last_group = None
    for output in outputs:
        group_id = output.get("group_id")
        if group_id != last_group:
            parts.append(f'<h3>{esc(group_names.get(group_id, "Requested files"))}</h3>')
            last_group = group_id
        spec = output.get("spec", {})
        spec_text = " · ".join(f"{label(key)}: {value}" for key, value in spec.items())
        record = output.get("source_record") or {}
        source_parts = []
        if record.get("table"):
            row_label = f', row {record["row_number"]}' if record.get("row_number") else ""
            source_parts.append(record["table"] + row_label)
        if output.get("source_image"):
            source_parts.append(output["source_image"])
        requirements = output.get("required_content") or []
        parts.append(
            '<article class="output-row">'
            f'<div><strong>{esc(output["name"])}</strong><code>{esc(Path(output["path"]).name)}</code>'
            f'<small>{esc(spec_text)}</small></div>'
        )
        if source_parts:
            parts.append(f'<p class="output-source"><strong>Source:</strong> {esc(" · ".join(source_parts))}</p>')
        if requirements:
            parts.append('<ul class="output-requirements">' + "".join(
                f"<li>{esc(item)}</li>" for item in requirements
            ) + "</ul>")
        parts.append("</article>")
    parts.append("</div>")
    return "".join(parts)


CSS = """
:root{color-scheme:light;font-family:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#202724;background:#fff;font-size:15px;line-height:1.52}
*{box-sizing:border-box}body{margin:0}.page{max-width:1050px;margin:auto;padding:28px 32px 56px}h1,h2,h3,p{margin-top:0}h1{font-size:27px;line-height:1.2;margin:8px 0 9px}h2{font-size:20px;line-height:1.3;margin-bottom:18px}h3{font-size:16px;line-height:1.35;margin:28px 0 12px}.eyebrow{color:#59645f;font-weight:700;font-size:12px;text-transform:uppercase;letter-spacing:.08em}.subline{color:#59645f;margin-bottom:28px}.section{border-top:1px solid #dce3df;padding-top:25px;margin-top:27px}.brief-text{white-space:pre-wrap;overflow-wrap:anywhere;max-width:83ch}.brand-name{font-size:20px;font-weight:700;margin-bottom:2px}.tagline{font-style:italic;color:#51605a}.brand-facts,.detail-list{margin:0}.brand-facts>div,.detail-list>div{display:grid;grid-template-columns:minmax(150px,23%) 1fr;gap:12px;padding:10px 0;border-bottom:1px solid #edf0ed}.brand-facts dt,.detail-list dt{font-weight:700;color:#52605a}.brand-facts dd,.detail-list dd{margin:0;min-width:0}.brand-facts dd p,.detail-list dd p{margin:0}.data-list{margin:0;padding-left:18px}.palette-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.palette-item{display:flex;gap:12px;border:1px solid #e0e6e1;border-radius:6px;padding:10px;min-width:0}.palette-item .swatch{width:55px;min-width:55px;height:55px;border-radius:3px;border:1px solid #0002}.palette-item strong{display:inline-block;margin-right:6px}.palette-item code{font-size:12px;color:#57645e}.palette-item small{display:block;text-transform:uppercase;color:#66726d;font-size:11px;font-weight:700;letter-spacing:.04em}.palette-item p{font-size:13px;margin:5px 0 0}.type-system>.detail-list>div{grid-template-columns:minmax(150px,23%) 1fr}.type-system .data-list li{margin-bottom:8px}.asset-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:13px}.asset-card{border:1px solid #dce3df;border-radius:6px;overflow:hidden;min-width:0;background:#fff}.asset-preview{display:flex;height:190px;align-items:center;justify-content:center;background:#f2f5f3;border-bottom:1px solid #e3e8e4;overflow:hidden;color:#386951}.asset-preview img{display:block;width:100%;height:100%;object-fit:contain}.asset-info{padding:11px 12px}.asset-info strong{display:block;font-size:13px;overflow-wrap:anywhere;line-height:1.35}.asset-info p{font-size:12px;color:#65716a;margin:4px 0 9px}.asset-actions{display:flex;gap:14px}.asset-actions a{font-size:12px;color:#176348;text-decoration:underline;text-underline-offset:2px}.file-excerpt{font-size:10px;line-height:1.35;white-space:pre-wrap;overflow-wrap:anywhere;margin:0;padding:12px;width:100%;height:100%;color:#364a3e}.file-icon{font-size:24px;font-weight:700;color:#6d8577}.output-row{border:1px solid #e0e6e1;border-radius:6px;padding:13px 15px;margin-bottom:9px}.output-row>div:first-child{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 14px}.output-row strong{font-size:14px}.output-row code{font-size:12px;color:#375d4d;overflow-wrap:anywhere}.output-row small{display:block;width:100%;font-size:12px;color:#5b6760}.output-requirements{font-size:13px;padding-left:20px;margin:8px 0 0}.output-requirements li{margin:3px 0}a:focus-visible{outline:2px solid #146344;outline-offset:2px}@media(max-width:720px){.page{padding:20px 18px 40px}.asset-grid,.palette-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.brand-facts>div,.detail-list>div,.type-system>.detail-list>div{display:block}.brand-facts dt,.detail-list dt{margin-bottom:3px}.asset-preview{height:150px}}@media(max-width:470px){.asset-grid,.palette-grid{grid-template-columns:1fr}.asset-preview{height:220px}h1{font-size:23px}}
"""
CSS += ".output-source{font-size:12px;color:#5b6760;margin:7px 0 0}"

DOWNLOAD_SCRIPT = """
<script>
document.addEventListener('click', async (event) => {
  const link = event.target.closest('a[data-download]');
  if (!link) return;
  event.preventDefault();
  const original = link.textContent;
  link.textContent = 'Downloading...';
  try {
    const response = await fetch(link.href, {mode: 'cors'});
    if (!response.ok) throw new Error(`Asset returned ${response.status}`);
    const objectUrl = URL.createObjectURL(await response.blob());
    const saveLink = document.createElement('a');
    saveLink.href = objectUrl;
    saveLink.download = link.getAttribute('download');
    document.body.append(saveLink);
    saveLink.click();
    saveLink.remove();
    setTimeout(() => URL.revokeObjectURL(objectUrl), 60000);
  } catch (error) {
    window.open(link.href, '_blank', 'noopener');
  } finally {
    link.textContent = original;
  }
});
</script>
"""


def write_page(task_id: str, spec: dict, assets: list[dict], outputs: list[dict]) -> None:
    title = spec["task_name"]
    content = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(task_id)} · {esc(title)}</title><style>{CSS}</style></head><body>
<main class="page">
<header><div class="eyebrow">Gatsby · Pilot brief · {esc(task_id)}</div><h1>{esc(title)}</h1><p class="subline">{esc(spec["task_code"])} · {esc(spec["family"])}</p></header>
<section class="section" aria-labelledby="brief-title"><h2 id="brief-title">Client brief</h2><div class="brief-text">{esc(spec["client_brief"])}</div>
<h3>Source of truth</h3><p>{esc(spec["source_of_truth"])}</p>
<h3>Production constraints</h3><ul class="data-list">{"".join(f"<li>{esc(item)}</li>" for item in spec["truth_constraints"] + spec["production_requirements"])}</ul></section>
<section class="section" aria-labelledby="brand-title"><h2 id="brand-title">Brand identity</h2>{render_brand(spec["brand_identity"])}</section>
<section class="section" aria-labelledby="assets-title"><h2 id="assets-title">Source assets ({len(assets)})</h2>{render_assets(task_id, assets)}</section>
<section class="section" aria-labelledby="outputs-title"><h2 id="outputs-title">Requested deliverables ({len(outputs)})</h2>{render_outputs(outputs, spec["deliverable_groups"])}</section>
</main>{DOWNLOAD_SCRIPT}<script src="https://cdn.jsdelivr.net/npm/@iframe-resizer/child@5"></script></body></html>
"""
    (OUT / f"{task_id}.html").write_text(content, encoding="utf-8")


def platform_verifiers(verifiers: list[dict], outputs: list[dict]) -> list[dict]:
    chosen = []
    for output in outputs:
        output_id = output["output_id"]
        output_checks = [v for v in verifiers if v["output_id"] == output_id]
        auto = [v for v in output_checks if v["type"] == "auto"]
        human = [v for v in output_checks if v["type"] == "human"]
        # The platform's Phase 2 review should stay usable, while the full bank
        # remains available through the canonical verifier JSON linked in the sheet.
        chosen.extend(auto[:1])
        chosen.extend(human[:4 if len(outputs) <= 7 else 2])
        if output_id == "producer-card-r015":
            chosen.extend(v for v in human if "no photograph presented as Priya" in v["check"])
    seen = set()
    result = []
    for item in chosen:
        if item["check_id"] in seen:
            continue
        seen.add(item["check_id"])
        result.append({"verifier_question": f'{len(result) + 1}. {item["check"]}', "verifer_radio": "", "comment_box": ""})
    return result


def write_review_verifiers(task_id: str, verifiers: list[dict]) -> None:
    bank = OUT / "verifier-bank"
    bank.mkdir(parents=True, exist_ok=True)
    fields = ("check_id", "output_id", "type", "output_reference", "check", "reference_assets")
    review_only = [{key: item[key] for key in fields if key in item} for item in verifiers]
    (bank / f"{task_id}.json").write_text(
        json.dumps(review_only, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def sheet_row(index: int, task_id: str, assets: list[dict], verifiers: list[dict], outputs: list[dict]) -> list[object]:
    asset_names = ["Brief", "Brand identity"] + [a["filename"] for a in assets]
    rubrics = []
    for heading in RUBRICS:
        rubrics.append({
            "side_headers": heading,
            "AcceptRejectRadio": "",
            "AssestRepeater": [{
                "placeholder_assest_comment": f"What is wrong with the {name}?",
                "asset_options": [{"label": name}],
                "Assest_comment": "",
            } for name in asset_names],
        })
    review_checks = platform_verifiers(verifiers, outputs)
    row = [
        f"gatsby_v7_pilot_{task_id.lower().replace('-', '_')}",
        json.dumps(rubrics, ensure_ascii=False, separators=(",", ":")),
        json.dumps(review_checks, ensure_ascii=False, separators=(",", ":")),
        index, "", "NORMAL", "", BASE_URL + task_id + ".html",
        BASE_URL + "verifier-bank/" + task_id + ".json",
        f"https://dhigdec.github.io/creative-ai-benchmark/gatsby-v7/tasks/{task_id}/ASSET_MANIFEST.json",
        len(assets), len(outputs), len(review_checks), len(verifiers),
    ]
    if len(row[1]) > 49000 or len(row[2]) > 49000:
        raise ValueError(f"Sheet cell too large for {task_id}: {len(row[1])}, {len(row[2])}")
    return row


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [[
        "task_id", "MainSectionRepeater", "VerifiersRepeater", "uniqueId",
        "taskTags", "taskCategory", "CustomVerifiersRepeater", "url_link",
        "full_verifiers_url", "asset_manifest_url", "asset_count", "output_count",
        "platform_verifier_count", "full_verifier_count",
    ]]
    for index, task_id in enumerate(TASK_IDS, 1):
        folder = TASKS / task_id
        spec = json.loads((folder / "TASK_SPEC.json").read_text(encoding="utf-8"))
        assets = json.loads((folder / "ASSET_MANIFEST.json").read_text(encoding="utf-8"))
        outputs = json.loads((folder / "OUTPUT_REGISTER.json").read_text(encoding="utf-8"))
        verifiers = json.loads((folder / "VERIFIERS.json").read_text(encoding="utf-8"))
        if len(outputs) != len(spec["deliverables"]):
            raise ValueError(f"Output mismatch for {task_id}")
        if any(not asset["public_url"].startswith("https://annotationprod.s3.ap-south-1.amazonaws.com/") for asset in assets):
            raise ValueError(f"Unexpected asset host for {task_id}")
        write_page(task_id, spec, assets, outputs)
        write_review_verifiers(task_id, verifiers)
        row = sheet_row(index, task_id, assets, verifiers, outputs)
        rows.append(row)
        print(f"{task_id}: {len(assets)} assets, {len(outputs)} outputs, {row[12]}/{row[13]} platform/full checks; sheet cells {len(row[1])}/{len(row[2])} chars")
    SHEET_EXPORT.parent.mkdir(parents=True, exist_ok=True)
    SHEET_EXPORT.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    print(f"Sheet payload: {SHEET_EXPORT}")


if __name__ == "__main__":
    main()
