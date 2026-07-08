#!/usr/bin/env python
"""Build Metadata_Schema_v2.html — the granular StudioBench metadata tag schema, grouped by
facet, each tag with type / assignment / full enumerated allowed-values / why / example, plus
the migration map from the old 19 tags. Reads metadata_schema_v2.json.
Run: asset_pipeline/.venv/bin/python build_metadata_schema.py
"""
import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
def esc(s): return html.escape(str(s if s is not None else ""))

d = json.load(open(ROOT / "metadata_schema_v2.json", encoding="utf-8"))
S = d["schema"]; FACETS = d["facet_order"]; CORE = set(d["core_set"])
MAP = d.get("current_mapping", [])
TAX = d.get("taxonomy_axes", [])
n_core = len(CORE); n_ext = len(S) - n_core
def is_tax(t): return t.get("role") == "taxonomy"

TYPE_C = {"enum":"e","multi-enum":"m","integer":"n","float":"n","boolean":"b","string":"s"}

def av_cell(t):
    v = t["allowed_values"]
    if len(v) > 180:
        return f'<details><summary>{esc(v[:150])}…</summary><div class="av">{esc(v)}</div></details>'
    return f'<span class="av">{esc(v)}</span>'

facet_blocks = ""
for f in FACETS:
    ts = [t for t in S if t["facet"] == f]
    if not ts: continue
    ncore = sum(1 for t in ts if t["tag"] in CORE)
    rows = ""
    for t in ts:
        core = t["tag"] in CORE
        star = '<span class="core" title="core tag">core</span>' if core else ''
        tax = '<span class="taxb" title="taxonomy / distribution axis">taxonomy</span>' if is_tax(t) else ''
        tc = TYPE_C.get(t["type"], "s")
        rows += f'''<tr class="{'r-tax' if is_tax(t) else ('r-core' if core else '')}">
  <td class="tag"><code>{esc(t['tag'])}</code>{tax}{star}</td>
  <td><span class="ty ty-{tc}">{esc(t['type'])}</span><br><span class="asg">{esc(t['assignment'])}</span></td>
  <td class="cap">{esc(t['captures'])}</td>
  <td>{av_cell(t)}</td>
  <td class="why">{esc(t['why'])}<div class="ex"><b>e.g.</b> <code>{esc(t['example'])}</code></div></td>
</tr>'''
    facet_blocks += f'''<section class="facet" id="f-{esc(f).replace(' ','-').replace('&amp;','and')}">
<h2>{esc(f)} <span class="fc">{len(ts)} tags · {ncore} core</span></h2>
<table><thead><tr><th>tag</th><th>type / set by</th><th>captures</th><th>allowed values</th><th>why it matters</th></tr></thead><tbody>{rows}</tbody></table>
</section>'''

# migration map
DISP_C = {"keep":"k","rename":"r","split":"s","merge":"m","drop":"d"}
map_rows = ""
for m in MAP:
    dc = DISP_C.get(m["disposition"], "k")
    map_rows += f'<tr><td><code>{esc(m["current_tag"])}</code></td><td><span class="disp disp-{dc}">{esc(m["disposition"])}</span></td><td>{esc(m["becomes"])}</td></tr>'

nav = "".join(f'<a href="#f-{esc(f).replace(" ","-").replace("&amp;","and")}">{esc(f)}</a>' for f in FACETS)

HTML = f"""<!doctype html><meta charset=utf-8><title>StudioBench — Metadata Schema v2</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;font:13.5px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#1c1830;background:#f6f5fb;padding:0 0 70px}}
.wrap{{max-width:1240px;margin:0 auto;padding:24px 26px}}
h1{{font-size:23px;margin:0 0 4px}}.lead{{color:#5a5274;margin:0 0 6px;font-size:14px;max-width:900px}}
.counts{{color:#6b6385;font-size:12.5px;margin:0 0 14px}}
.nav{{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 20px}}
.nav a{{font-size:12px;background:#efe9fb;border:1px solid #ddd2f2;border-radius:20px;padding:3px 11px;color:#4a3f75;text-decoration:none}}
.nav a:hover{{background:#e2d7f6}}
.facet{{margin:0 0 24px;scroll-margin-top:12px}}
.facet h2{{font-size:16px;margin:0 0 8px;color:#2f2360;border-bottom:2px solid #e6ddef;padding-bottom:5px}}
.facet h2 .fc{{font-size:11.5px;color:#9186b8;font-weight:400}}
table{{width:100%;border-collapse:collapse;font-size:12px;background:#fff;border:1px solid #e6ddef;border-radius:10px;overflow:hidden}}
th,td{{border-bottom:1px solid #efeaf8;padding:7px 9px;text-align:left;vertical-align:top}}
th{{background:#1a1333;color:#e9e4f5;font-weight:600;font-size:11px;position:sticky;top:0}}
tr.r-core td{{background:#fbfaff}}tr.r-tax td{{background:#f3f0fd}}
td.tag code{{font-size:12px;color:#3c2f73;font-weight:600;background:none;padding:0}}
.core{{display:inline-block;font-size:9px;font-weight:700;color:#1d7a52;background:#e1f5ee;border:1px solid #9fe1cb;border-radius:10px;padding:0 6px;margin-left:6px;text-transform:uppercase;letter-spacing:.03em;vertical-align:middle}}
.taxb{{display:inline-block;font-size:9px;font-weight:700;color:#4a3288;background:#eae4fb;border:1px solid #c9bdf0;border-radius:10px;padding:0 6px;margin-left:6px;text-transform:uppercase;letter-spacing:.03em;vertical-align:middle}}
.taxbox{{background:#f3f0fd;border:1px solid #d9cef5;border-radius:11px;padding:14px 18px;margin:0 0 20px}}
.taxbox h2{{font-size:15px;margin:0 0 4px;color:#2f2360;border:0}}
.taxbox p{{font-size:12.5px;color:#4a4363;margin:2px 0 8px}}
.taxbox .axes{{display:grid;gap:6px}}
.taxbox .ax{{background:#fff;border:1px solid #d9cef5;border-radius:8px;padding:6px 11px;font-size:12.5px;line-height:1.45}}
.taxbox .ax code{{color:#4a3288;font-weight:600}}.taxbox .ax span{{color:#7a7098;font-size:11px}}
.ty{{font-size:10.5px;font-weight:600;border-radius:5px;padding:1px 6px;white-space:nowrap}}
.ty-e{{background:#eae4fb;color:#4a3288}}.ty-m{{background:#e6f1fb;color:#0c447c}}.ty-n{{background:#eaf3de;color:#3b6d11}}.ty-b{{background:#faeeda;color:#854f0b}}.ty-s{{background:#f1efe8;color:#444441}}
.asg{{font-size:10px;color:#8a80a8}}
td.cap{{max-width:230px;color:#38304f}}
.av{{font-size:11px;color:#4f4869;font-family:ui-monospace,Menlo,monospace;word-break:break-word}}
details summary{{cursor:pointer;color:#6a5db0;font-size:11px;font-family:ui-monospace,Menlo,monospace}}
details .av{{margin-top:5px;padding:6px 8px;background:#faf8fe;border:1px solid #efeaf8;border-radius:6px;max-height:220px;overflow:auto}}
td.why{{max-width:280px;color:#4a4363;font-size:11.5px}}
.ex{{margin-top:4px;color:#7a7098;font-size:11px}}.ex code{{background:#f1eef9;padding:0 4px;border-radius:3px;color:#4a3f75}}
.mig h2{{font-size:16px;margin:26px 0 8px;color:#2f2360;border-bottom:2px solid #e6ddef;padding-bottom:5px}}
.disp{{font-size:10px;font-weight:700;border-radius:5px;padding:1px 7px;text-transform:uppercase}}
.disp-k{{background:#e1f5ee;color:#0f6e56}}.disp-r{{background:#e6f1fb;color:#185fa5}}.disp-s{{background:#eae4fb;color:#534ab7}}.disp-m{{background:#faeeda;color:#854f0b}}.disp-d{{background:#fbe9e9;color:#a3282d}}
.legend{{font-size:11.5px;color:#6b6385;margin:8px 0 0}}.legend b{{color:#3c2f73}}
</style>
<div class="wrap">
<h1>StudioBench — metadata schema v2</h1>
<p class="lead">A granular, crisply-enumerated tag set that replaces the coarse 19. Every tag has a closed value set (ordinals get per-level anchors), a clear <b>set-by</b> rule (auto / derived / human), and a stated slicing use. Grouped into {len(FACETS)} facets; the <span class="core">core</span> subset is the must-have layer, the rest is for deep slicing.</p>
<p class="counts"><b>{len(S)} tags</b> · {n_core} core + {n_ext} extended · {len(FACETS)} facets · <span class="taxb">taxonomy</span> = the {len(TAX)} distribution axes · distilled from 109 candidates.</p>
<div class="taxbox"><h2>Taxonomy axes — how the corpus is organized (the "distribution")</h2>
<p>Per the ops-team steer, the corpus is structured by the <b>nature of the task</b>, not by brand. These {len(TAX)} axes drive the distribution table, balance, and pricing. Every other tag is <b>descriptive</b> — captured for slicing, but not a structuring axis (brand/domain/audience/palette live here).</p>
<div class="axes">{"".join(f'<div class="ax"><code>{esc(a)}</code> — <span>{esc(next((t["captures"] for t in S if t["tag"]==a),""))}</span></div>' for a in TAX)}</div></div>
<div class="nav">{nav}<a href="#migration">↳ migration map</a></div>
{facet_blocks}
<section class="mig" id="migration">
<h2>Migration map — the old 19 → v2</h2>
<table><thead><tr><th>current tag</th><th>disposition</th><th>becomes</th></tr></thead><tbody>{map_rows}</tbody></table>
<p class="legend"><b>keep</b> = unchanged · <b>rename</b> = same idea, clearer name · <b>split</b> = broken into several precise tags · <b>merge</b> = folded with another · <b>drop</b> = removed (redundant/out-of-scope).</p>
</section>
</div>"""
(ROOT / "Metadata_Schema_v2.html").write_text(HTML, encoding="utf-8")
print(f"wrote Metadata_Schema_v2.html ({len(HTML)//1024} KB) — {len(S)} tags, {len(FACETS)} facets, {n_core} core")
