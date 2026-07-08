"""manifest.json (the agent-facing contract) + INTAKE.md renderer + coverage."""
from __future__ import annotations
import time
from pathlib import Path

from util import sha256_file, write_json

PIPELINE_VERSION = "0.1.0"


def _coverage(rec: dict, spec: dict, asset_entries: list) -> dict:
    inputs = list(rec.get("inputs") or [])
    claimed_assets = {a["input_requirement"] for a in asset_entries}
    claimed_decisions = {d["requirement"] for d in spec.get("decisions", [])}
    uncovered = [i for i in inputs if i not in claimed_assets and i not in claimed_decisions]
    return {
        "inputs_total": len(inputs),
        "covered_by_assets": sum(1 for i in inputs if i in claimed_assets),
        "covered_by_decisions": sum(1 for i in inputs if i in claimed_decisions and i not in claimed_assets),
        "uncovered": uncovered,
    }


def build(task_dir: Path, rec: dict, spec: dict, persona: dict, state: dict, stats: dict) -> dict:
    asset_entries = []
    for key in [a["key"] for a in spec["assets"]]:
        st = state.get("assets", {}).get(key)
        if not st:
            continue
        for entry in st["entries"]:
            e = dict(entry)
            f = e.get("file")
            if f and (task_dir / f).exists():
                e["sha256"] = sha256_file(task_dir / f)
            asset_entries.append(e)

    failed = [e for e in asset_entries if (e.get("qc") or {}).get("status") == "failed"]
    cov = _coverage(rec, spec, asset_entries)
    man = {
        "schema_version": 1,
        "task_id": rec["id"], "slug": spec["slug"],
        "title": rec["title"], "task_type": rec.get("task_type"),
        "category": rec["category"], "family": rec["family"], "feasibility": rec["feasibility"],
        "source": rec.get("source"), "source_url": rec.get("url"),
        "mcp_workflow": rec["mcp_workflow"],
        "original_brief": rec.get("desc"),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "pipeline_version": PIPELINE_VERSION,
        "client_persona": {
            "brand_name": persona.get("brand_name"), "tagline": persona.get("tagline"),
            "industry": persona.get("industry"), "palette": persona.get("palette"),
            "fonts": persona.get("fonts"), "voice": persona.get("voice"),
            "persona_file": "persona.json",
        },
        "assets": asset_entries,
        "decisions": spec.get("decisions", []),
        "coverage": cov,
        "stats": stats,
        "ready_for_agent": (not failed) and (not cov["uncovered"]),
    }
    write_json(task_dir / "manifest.json", man)
    return man


def render_intake(task_dir: Path, man: dict) -> None:
    p = man["client_persona"]
    lines = []
    a = lines.append
    a("# INTAKE — %s" % man["title"])
    a("")
    a("**Task %s** · %s · %s · feasibility: **%s** · source: [%s posting](%s)" % (
        man["task_id"], man["family"], man["category"], man["feasibility"],
        man.get("source", ""), man.get("source_url", "")))
    a("")
    a("## The simulated client")
    a("**%s** — %s. *%s*" % (p.get("brand_name"), p.get("industry"), p.get("tagline") or ""))
    pal = ", ".join("%s `%s` (%s)" % (c.get("name"), c.get("hex"), c.get("role"))
                    for c in (p.get("palette") or []))
    a("Palette: %s  " % pal)
    fonts = p.get("fonts") or {}
    a("Fonts: headings **%s**, body **%s**  " % (fonts.get("heading"), fonts.get("body")))
    a("Voice: %s" % (p.get("voice") or ""))
    a("")
    a("## Input assets supplied (what the agent picks up)")
    a("")
    a("| # | File / value | Fulfils client input | Generator |")
    a("|---|---|---|---|")
    for i, e in enumerate(man["assets"], 1):
        gen = e.get("generator") or {}
        src = "`%s`" % e["file"] if e.get("file") else "inline: %s…" % str(e.get("value"))[:40]
        a("| %d | %s | %s | %s |" % (
            i, src, (e.get("input_requirement") or "")[:90],
            "%s/%s" % (gen.get("provider", "-"), gen.get("model", "-"))))
    a("")
    a("## Decisions & assumptions (items the brief left open)")
    for d in man["decisions"]:
        a("- **%s** → %s  \n  *why:* %s" % (d["requirement"], d["assumed_value"], d["why"]))
    a("")
    a("## Next step — the Adobe workflow the agent runs")
    a("```")
    a(man["mcp_workflow"])
    a("```")
    a("")
    cov = man["coverage"]
    a("Coverage: %d client inputs — %d supplied as assets, %d resolved by recorded decisions, %d uncovered. "
      "**ready_for_agent: %s**" % (cov["inputs_total"], cov["covered_by_assets"],
                                   cov["covered_by_decisions"], len(cov["uncovered"]),
                                   man["ready_for_agent"]))
    a("")
    a("## Original client brief (verbatim)")
    a("> " + (man.get("original_brief") or "").replace("\n", "\n> ")[:3000])
    (task_dir / "INTAKE.md").write_text("\n".join(lines))
