#!/usr/bin/env python
"""Render the 12 corrected flagship specs (flagship_v2/specs/*.json) into human-readable
markdown briefs + an INDEX.md and a compact INDEX.html. Each brief leads with the honest
execution-mode breakdown so headless-vs-product scope is never misrepresented.

Run: asset_pipeline/.venv/bin/python build_flagship_briefs.py
"""
import glob
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FV = ROOT / "flagship_v2"
BR = FV / "briefs"
BR.mkdir(parents=True, exist_ok=True)
MODE = {"C": "headless-confirmed", "W": "interactive (Express widget)",
        "A": "async (video/audio widget)", "T": "authored-template", "L": "local glue"}

specs = [json.load(open(f)) for f in sorted(glob.glob(str(FV / "specs/*.json")))]
specs.sort(key=lambda s: s["id"])
rows = []

for s in specs:
    md = []
    md.append("# %s — %s\n" % (s["id"], s["title"]))
    md.append("**Vertical:** %s  ·  **Source:** [%s](%s)\n" % (
        s["vertical"], s["source"]["platform"], s["source"]["url"]))
    md.append("**Execution:** `%s`  ·  **Connector calls:** %d  ·  **Headless-doable:** %s\n" % (
        s.get("exec_mode_summary", "—"), s["tool_call_count"], "yes" if s.get("headless_doable") else "no (product)"))
    md.append("\n> **Grounding:** %s\n" % s["grounding_note"])
    md.append("\n## One-line ask\n%s\n" % s["one_line_ask"])
    md.append("\n## Brief\n%s\n" % s["full_brief"])

    md.append("\n## INPUT assets (%d)\n" % len(s["inputs"]))
    md.append("| asset | kind | gen model | used in steps |\n|---|---|---|---|")
    for i in s["inputs"]:
        md.append("| %s | %s | `%s` | %s |" % (
            i["name"], i["kind"], i["gen_model"], ", ".join(map(str, i.get("used_in_steps", []))) or "—"))

    md.append("\n\n## OUTPUT deliverables (%d)\n" % len(s["outputs"]))
    md.append("| deliverable | kind | spec |\n|---|---|---|")
    for o in s["outputs"]:
        md.append("| %s | %s | %s |" % (o["name"], o["kind"], o["spec"]))

    md.append("\n\n## CONNECTOR WORKFLOW (%d calls)\n" % s["tool_call_count"])
    md.append("| # | mode | tool | server | inputs from | output |\n|--:|:--:|---|---|---|---|")
    for st in s["connector_workflow"]:
        md.append("| %s | `%s` | `%s` | %s | %s | %s |" % (
            st["n"], st["exec_mode"], st["tool"], st["server"],
            "; ".join(st.get("inputs_from", [])) or "—", st["output"]))

    md.append("\n\n**Iterative chaining:** %s\n" % s.get("iterative_chaining_note", ""))
    md.append("\n**Why it's hard:** %s\n" % s.get("difficulty_rationale", ""))
    if s.get("corrections_applied"):
        md.append("\n**v2.1 corrections applied:**\n" + "\n".join("- " + c for c in s["corrections_applied"]))

    (BR / ("%s_%s.md" % (s["id"], s["slug"]))).write_text("\n".join(md))
    rows.append(s)

# INDEX.md
idx = ["# Flagship v2.1 — 12 long-horizon Adobe-connector tasks\n",
       "| id | task | vertical | calls | exec modes | headless |",
       "|---|---|---|--:|---|:--:|"]
for s in rows:
    idx.append("| %s | [%s](briefs/%s_%s.md) | %s | %d | `%s` | %s |" % (
        s["id"], s["title"][:48], s["id"], s["slug"], s["vertical"][:22],
        s["tool_call_count"], s.get("exec_mode_summary", "—"),
        "✓" if s.get("headless_doable") else "product"))
(FV / "INDEX.md").write_text("\n".join(idx))

# compact INDEX.html
def esc(x):
    return html.escape(str(x))


cards = []
for s in rows:
    toolchips = " ".join("<span class=t>%s</span>" % esc(t) for t in s.get("tools_used", [])[:18])
    steprows = "".join(
        "<tr><td>%s</td><td><span class='m m-%s'>%s</span></td><td><code>%s</code></td>"
        "<td>%s</td><td>%s</td></tr>" % (
            st["n"], st["exec_mode"], st["exec_mode"], esc(st["tool"]),
            esc("; ".join(st.get("inputs_from", [])) or "—"), esc(st["output"]))
        for st in s["connector_workflow"])
    cards.append("""<section class=card id="%s">
      <h2>%s <small>%s</small></h2>
      <div class=meta><b>%s</b> · <a href="%s" target=_blank>source</a> ·
        <span class=pill>%d connector calls</span>
        <span class=pill>%s</span>
        <span class="pill %s">%s</span></div>
      <p class=ask>%s</p>
      <details><summary>Brief & grounding</summary><p class=g>%s</p><p>%s</p></details>
      <div class=chips>%s</div>
      <details open><summary>Connector workflow (%d)</summary>
        <table><tr><th>#</th><th>mode</th><th>tool</th><th>inputs from</th><th>output</th></tr>%s</table>
      </details>
    </section>""" % (
        esc(s["id"]), esc(s["title"]), esc(s["id"]), esc(s["vertical"]), esc(s["source"]["url"]),
        s["tool_call_count"], esc(s.get("exec_mode_summary", "")),
        "ok" if s.get("headless_doable") else "warn",
        "headless" if s.get("headless_doable") else "product-mode",
        esc(s["one_line_ask"]), esc(s["grounding_note"]), esc(s["full_brief"]),
        toolchips, s["tool_call_count"], steprows))

nav = "".join('<a href="#%s">%s · %s</a>' % (esc(s["id"]), esc(s["id"]), esc(s["title"][:34])) for s in rows)
HTML = """<!doctype html><meta charset=utf-8><title>Flagship v2.1 — Adobe connector tasks</title>
<style>
:root{--ink:#1A1333;--ac:#7A1FA2;--line:#e6ddef;--bg:#faf7fd}
*{box-sizing:border-box}body{margin:0;font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:#fff}
.wrap{display:grid;grid-template-columns:280px 1fr;max-width:1280px;margin:auto}
nav{position:sticky;top:0;align-self:start;height:100vh;overflow:auto;padding:20px 14px;background:var(--bg);border-right:1px solid var(--line)}
nav h1{font-size:16px;margin:0 0 12px}nav a{display:block;padding:7px 9px;margin:2px 0;border-radius:7px;color:#43345a;text-decoration:none;font-size:12.5px}
nav a:hover{background:#fff}
main{padding:26px 30px}
.card{border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:0 0 22px;scroll-margin-top:14px}
.card h2{margin:0 0 6px;font-size:19px}.card h2 small{color:#9b8bb0;font-weight:500;font-size:12px}
.meta{font-size:12.5px;color:#5b4b70;margin-bottom:8px}.meta a{color:var(--ac)}
.pill{display:inline-block;background:#f0e8f7;color:#6a2e8c;border-radius:20px;padding:2px 10px;margin:0 3px;font-size:11.5px}
.pill.ok{background:#e7f5ec;color:#2E8B57}.pill.warn{background:#fdf3e3;color:#b3791e}
.ask{font-weight:600;margin:8px 0}.g{color:#6a5b80;font-style:italic}
.chips{margin:6px 0}.t{display:inline-block;background:#1A1333;color:#fff;border-radius:5px;padding:1px 7px;margin:2px;font-size:10.5px;font-family:ui-monospace,monospace}
details{margin:8px 0}summary{cursor:pointer;font-weight:600;font-size:13px;color:var(--ac)}
table{width:100%;border-collapse:collapse;margin-top:8px;font-size:12px}
th,td{border-bottom:1px solid var(--line);padding:4px 7px;text-align:left;vertical-align:top}
th{color:#8a7aa0;font-weight:600}
code{font-family:ui-monospace,monospace;font-size:11.5px;background:#f5f0fa;padding:1px 4px;border-radius:4px}
.m{font-family:ui-monospace,monospace;font-weight:700;padding:1px 6px;border-radius:5px;font-size:11px}
.m-C{background:#e7f5ec;color:#2E8B57}.m-W{background:#eaf2fb;color:#1F6FB2}.m-A{background:#fdf3e3;color:#b3791e}
.m-T{background:#f3e8fb;color:#7A1FA2}.m-L{background:#eee;color:#555}
</style>
<div class=wrap><nav><h1>Flagship v2.1<br><small>12 long-horizon tasks</small></h1>
<p style="font-size:11px;color:#7a6b90">mode legend: <span class="m m-C">C</span> headless ·
<span class="m m-W">W</span> Express widget · <span class="m m-A">A</span> async video/audio ·
<span class="m m-T">T</span> authored template · <span class="m m-L">L</span> local</p>__NAV__</nav>
<main>__CARDS__</main></div>"""
HTML = HTML.replace("__NAV__", nav).replace("__CARDS__", "".join(cards))
(FV / "INDEX.html").write_text(HTML)

print("wrote %d briefs + INDEX.md + INDEX.html" % len(rows))
for s in rows:
    print("  %s %-34s calls=%2d exec=%-18s headless=%s" % (
        s["id"], s["slug"][:34], s["tool_call_count"], s.get("exec_mode_summary", "—"),
        s.get("headless_doable")))
