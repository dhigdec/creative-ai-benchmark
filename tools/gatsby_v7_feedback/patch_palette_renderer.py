#!/usr/bin/env python3
"""Show each palette colour's role and usage, and the brand's colour rules, on the Brand tab.

Reviewers could not tell mandatory colours from optional ones, and had no rule to judge
translucent panels against. The data now carries both; this makes the page show them. Brands
without roles keep the original compact swatch row, so nothing changes where data is absent.
Idempotent: a second run reports "already applied".
"""
import os, re

HP = "/Users/dhiren/Documents/ChatGPT/Adobe_Gpt/publish/creative-ai-benchmark/docs/gatsby-v5/index.html"

OLD = ("<h3>Palette</h3><div class=\"swatches\">${b.palette.map(c=>`<div class=\"swatch\"><i style=\"background:"
       "${/^#[0-9a-f]{6}$/i.test(c.hex)?c.hex:'#fff'}\"></i><span>${esc(c.name)}<br><code>${esc(c.hex)}</code>"
       "</span></div>`).join('')}</div>")
NEW = ("<h3>Palette</h3><div class=\"swatches${b.palette.some(c=>c.role)?' rich':''}\">${b.palette.map(c=>`<div class=\"swatch\">"
       "<i style=\"background:${/^#[0-9a-f]{6}$/i.test(c.hex)?c.hex:'#fff'}\"></i><span>${esc(c.name)}<br><code>${esc(c.hex)}</code>"
       "${c.role?`<em class=\"pal-role${/^mandatory/i.test(c.role)?' req':''}\">${esc(c.role)}</em>`:''}"
       "${c.usage?`<small class=\"pal-use\">${esc(c.usage)}</small>`:''}</span></div>`).join('')}</div>${paletteRules(b)}")

FN = ("function paletteRules(b){const r=b.palette_rules;if(!r)return '';"
      "const rows=[['Distribution',r.distribution],['Opacity',r.opacity],['Not allowed',r.forbidden],['Photography',r.photography]]"
      ".filter(x=>x[1]);if(!rows.length)return '';"
      "return `<div class=\"pal-rules\"><p class=\"pal-rules-h\">Colour rules</p><dl>${rows.map(x=>`<dt>${esc(x[0])}</dt><dd>${esc(x[1])}</dd>`).join('')}</dl></div>`;}")

CSS = (".swatches.rich{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}"
       ".swatches.rich .swatch{align-items:flex-start;border:1px solid var(--line);border-radius:6px;padding:10px 12px;background:#fcfcfb}"
       ".swatches.rich .swatch i{flex:0 0 30px}"
       ".pal-role{display:inline-block;margin-top:5px;padding:2px 8px;border-radius:999px;font-style:normal;font-size:10.5px;"
       "letter-spacing:.03em;background:#eef1ef;color:var(--muted)}"
       ".pal-role.req{background:#dcefe5;color:#235f43;font-weight:700}"
       ".pal-use{display:block;margin-top:5px;color:var(--muted);font-size:11.5px;line-height:1.45}"
       ".pal-rules{margin:14px 0 6px;border:1px solid var(--line);border-left:3px solid var(--green);border-radius:6px;padding:12px 14px;background:#fcfcfb}"
       ".pal-rules-h{margin:0 0 6px;font-weight:700;font-size:13px}"
       ".pal-rules dl{display:grid;grid-template-columns:120px 1fr;gap:6px 14px;margin:0}"
       ".pal-rules dt{color:var(--muted);font-size:12px}.pal-rules dd{margin:0;font-size:12.5px;line-height:1.5}"
       "@media(max-width:700px){.pal-rules dl{grid-template-columns:1fr}.pal-rules dd{margin-bottom:6px}}")


def main():
    h = open(HP, encoding="utf-8").read()
    m = re.search(r'<script type="application/json" id="data">', h)
    s = m.end(); e = h.find("</script>", s)
    js_start = h.find("<script>", e) + 8; js_end = h.rfind("</script>")
    head, blob, mid, js, tail = h[:s], h[s:e], h[e:js_start], h[js_start:js_end], h[js_end:]
    done = []
    if "function paletteRules(" not in js:
        js = js.replace("const esc=", FN + "const esc=", 1); done.append("paletteRules fn")
    if OLD in js:
        js = js.replace(OLD, NEW, 1); done.append("palette section")
    elif "${paletteRules(b)}" not in js:
        raise SystemExit("palette render site not found")
    if ".pal-rules{" not in head:
        head = head.replace("</style>", CSS + "</style>", 1); done.append("css")
    open(HP, "w", encoding="utf-8").write(head + blob + mid + js + tail)
    print("patched:", ", ".join(done) or "already applied")


if __name__ == "__main__":
    main()
