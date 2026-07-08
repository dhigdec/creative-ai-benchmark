"""Top-level scorecard.html + scorecard.json from per-task judgements.
Reuses contact_sheet's house style (dark theme, base64 thumbs, badges)."""
from __future__ import annotations
import html
import json
import time
from pathlib import Path

from contact_sheet import CSS, _thumb_b64  # house style + base64 thumb

DIMS = ["task_fit", "completeness", "executability", "realism", "coherence", "decision_quality"]
DIM_SHORT = {"task_fit": "Fit", "completeness": "Compl", "executability": "Exec",
             "realism": "Real", "coherence": "Coher", "decision_quality": "Decis"}
VERDICT_CLASS = {"client-ready": "pass", "minor-gaps": "warn", "needs-rework": "fail", "reject": "fail"}

EXTRA_CSS = """
.heatcell{display:inline-block;width:42px;text-align:center;border-radius:6px;padding:5px 0;margin:1px;font-weight:800;font-size:12px;color:#06010e}
.lowconf{outline:2px dashed #9b93b3;outline-offset:-2px}
table.lead td,table.lead th{padding:8px 10px;border-bottom:1px solid #2c2440;font-size:13px;text-align:left}
.bar{display:inline-block;height:8px;border-radius:4px;vertical-align:middle}
.dimrow{margin:10px 0;padding:10px 12px;border:1px solid #2c2440;border-radius:10px}
.dimrow .sc{font-weight:850;font-size:18px;float:right}
.ev{font-size:12px;color:#b9aee0;margin:3px 0}
.ded{font-size:12px;color:#f4a9b6;margin:2px 0}
.fix{font-size:12.5px;color:#f4cf67;background:#2a2410;border-radius:8px;padding:7px 10px;margin-top:6px}
.risk{font-size:13px;color:#ff9eaf;margin:4px 0}
.gap{font-size:13px;color:#ffd27a;background:#2c2210;border-radius:8px;padding:8px 11px;margin:6px 0}
.delta{font-size:13px;font-weight:800}
h2.sec{margin-top:34px;border-bottom:1px solid #2c2440;padding-bottom:6px}
"""


def _ramp(score):
    """0-10 -> red→amber→green hex."""
    s = max(0, min(10, score)) / 10.0
    if s < 0.5:
        r, g, b = 244, int(80 + 120 * (s / 0.5)), 70
    else:
        t = (s - 0.5) / 0.5
        r, g, b = int(244 - 192 * t), int(200 - 0 * t), int(70 + 60 * t)
    return "#%02x%02x%02x" % (r, g, b)


def _verdict_badge(v):
    return '<span class="badge %s">%s</span>' % (VERDICT_CLASS.get(v, "warn"), v)


def write_scorecard(judgements, out_root: Path):
    out_root = Path(out_root)
    js = sorted(judgements, key=lambda x: -x["overall"])
    panel = js[0]["panel"]["judges_ran"] if js else []
    total_cost = sum(j.get("judge_cost_usd", 0) for j in judgements)
    avg = round(sum(j["overall"] for j in js) / len(js), 2) if js else 0

    e = ["<html><head><meta charset='utf-8'><title>Input-Asset Package Scorecard</title>",
         "<style>%s\n%s</style></head><body><div class='wrap'>" % (CSS, EXTRA_CSS)]
    e.append("<p class='muted'><a href='index.html'>← asset index</a></p>")
    e.append("<h1>Input-Asset Package Scorecard</h1>")
    e.append("<p class='muted'>How good is each generated asset SET <b>for its task</b> — judged by a "
             "cross-provider panel (%s) on a 6-dimension rubric, with an adversarial red-team pass and a "
             "per-asset-QC cross-check. Avg overall <b>%.2f</b>/10 · est judge spend $%.2f · %s</p>"
             % (", ".join(panel) or "—", avg, total_cost,
                time.strftime("%Y-%m-%d %H:%M")))

    # ---- leaderboard ----
    e.append("<h2 class='sec'>Leaderboard</h2><table class='lead'><tr><th>#</th><th>Task</th><th>Overall</th>"
             "<th>Verdict</th>" + "".join("<th>%s</th>" % DIM_SHORT[d] for d in DIMS) + "</tr>")
    for i, j in enumerate(js, 1):
        cells = ""
        for d in DIMS:
            dd = j["dimensions"][d]
            cls = "heatcell lowconf" if dd.get("low_confidence") else "heatcell"
            cells += "<td><span class='%s' style='background:%s'>%d</span></td>" % (cls, _ramp(dd["score"]), dd["score"])
        e.append("<tr><td>%d</td><td><a href='#t%s'>%s</a><br><span class='muted' style='font-size:11px'>%s</span></td>"
                 "<td class='delta' style='color:%s'>%.1f</td><td>%s</td>%s</tr>" % (
                     i, j["task_id"], html.escape(j["title"][:42]), j["slug"],
                     _ramp(j["overall"]), j["overall"], _verdict_badge(j["verdict"]), cells))
    e.append("</table>")

    # ---- per-task drilldown ----
    e.append("<h2 class='sec'>Per-task detail</h2>")
    for j in js:
        td = out_root / ("%s_%s" % (j["task_id"], j["slug"]))
        e.append("<div class='card' id='t%s' style='margin-bottom:18px'>" % j["task_id"])
        e.append("<h3 style='margin:0'>#%s — %s &nbsp; <span class='delta' style='color:%s'>%.1f</span> %s</h3>" % (
            j["task_id"], html.escape(j["title"]), _ramp(j["overall"]), j["overall"], _verdict_badge(j["verdict"])))
        e.append("<p class='muted'>%s · %s · judges: %s%s</p>" % (
            j["category"], j["archetype"], ", ".join(j["panel"]["judges_ran"]),
            " · ⚠ " + "; ".join(j["panel"]["judges_failed"]) if j["panel"].get("judges_failed") else ""))

        if j.get("top_risks"):
            e.append("<div><b>Top risks</b>" + "".join("<div class='risk'>• %s</div>" % html.escape(str(r))
                                                       for r in j["top_risks"]) + "</div>")
        for g in j.get("qc_gaps", []):
            e.append("<div class='gap'>QC gap — %s</div>" % html.escape(g))

        for d in DIMS:
            dd = j["dimensions"][d]
            e.append("<div class='dimrow'><span class='sc' style='color:%s'>%d/10</span>"
                     "<b>%s</b>%s" % (_ramp(dd["score"]), dd["score"], DIM_SHORT[d].upper() if False else
                                      _dim_name(d), " <span class='muted'>(judges %s, low-confidence)</span>"
                                      % dd.get("per_judge") if dd.get("low_confidence") else ""))
            for ev in dd.get("evidence", [])[:3]:
                e.append("<div class='ev'>✓ %s</div>" % html.escape(str(ev)))
            for de in dd.get("deductions", [])[:3]:
                e.append("<div class='ded'>− %s</div>" % html.escape(str(de)))
            fx = dd.get("fix")
            if fx:
                e.append("<div class='fix'>FIX → <b>%s</b>: %s</div>" % (
                    html.escape(str(fx.get("target_asset_key"))), html.escape(str(fx.get("prompt_delta") or fx.get("problem")))))
            e.append("</div>")

        # rounds (improve loop)
        if j.get("rounds"):
            e.append("<p class='muted'>Improve loop: " + " → ".join(
                "r%s %s (%.1f)" % (r.get("round"), r.get("action"), r.get("overall", 0)) for r in j["rounds"]) + "</p>")

        # thumbnails + pre/post pairs
        e.append("<div class='grid' style='margin-top:10px'>")
        man = json.loads((td / "manifest.json").read_text()) if (td / "manifest.json").exists() else {"assets": []}
        for a in man["assets"]:
            if a.get("kind") != "image" or not a.get("file") or not (td / a["file"]).exists():
                continue
            pre = sorted((td / "originals").glob("preimprove_r*_" + Path(a["file"]).name)) if (td / "originals").exists() else []
            if pre:
                e.append("<div class='card'><div class='pair'><div><img src='%s'><br>before</div>"
                         "<div><img src='%s'><br>after (regen)</div></div><div class='meta'>%s</div></div>" % (
                             _thumb_b64(pre[0], 300), _thumb_b64(td / a["file"], 300), html.escape(a["key"])))
            else:
                e.append("<div class='card'><img src='%s'><div class='meta'>%s · self-QC %s</div></div>" % (
                    _thumb_b64(td / a["file"], 320), html.escape(a["key"]),
                    (a.get("qc") or {}).get("vision_score")))
        e.append("</div></div>")

    e.append("</div></body></html>")
    (out_root / "scorecard.html").write_text("".join(e))

    sj = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "panel": panel,
          "totals": {"judge_cost_usd": round(total_cost, 3), "n_tasks": len(js), "avg_overall": avg},
          "tasks": [{"task_id": j["task_id"], "slug": j["slug"], "overall": j["overall"],
                     "verdict": j["verdict"], "dimensions": {d: j["dimensions"][d]["score"] for d in DIMS},
                     "top_risks": j.get("top_risks", []), "qc_gaps": j.get("qc_gaps", [])} for j in js]}
    (out_root / "scorecard.json").write_text(json.dumps(sj, indent=2))


def _dim_name(d):
    return {"task_fit": "Task Fit", "completeness": "Completeness", "executability": "Executability",
            "realism": "Realism", "coherence": "Coherence", "decision_quality": "Decision Quality"}[d]
