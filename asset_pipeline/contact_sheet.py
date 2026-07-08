"""Per-task contact_sheet.html (base64 thumbs, prompts, QC badges) + input_assets/index.html."""
from __future__ import annotations
import base64
import html
import io
import json
from pathlib import Path

import config

CSS = """
body{font-family:-apple-system,Segoe UI,Inter,sans-serif;background:#0d0717;color:#ece7f6;margin:0;padding:32px}
a{color:#7cd6ee}.muted{color:#9b93b3}.wrap{max-width:1180px;margin:0 auto}
h1{letter-spacing:-1px}h2{margin-top:38px;border-bottom:1px solid #2c2440;padding-bottom:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}
.card{background:#171028;border:1px solid #2c2440;border-radius:14px;padding:14px}
.card img{width:100%;border-radius:9px;background:#fff}
.badge{display:inline-block;font-size:11px;font-weight:700;border-radius:99px;padding:3px 10px;margin-right:6px}
.pass{background:#10402c;color:#5ee0a8}.warn{background:#4a3a10;color:#f4cf67}.fail{background:#4a1620;color:#ff8b9e}
.meta{font-size:12px;color:#9b93b3;margin:8px 0 4px}
details{margin-top:8px;font-size:12px}summary{cursor:pointer;color:#b9aee0}
pre{white-space:pre-wrap;background:#0a0512;border:1px solid #2c2440;border-radius:8px;padding:10px;font-size:11.5px;color:#cfc6e8}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:8px}.pair div{text-align:center;font-size:11px;color:#9b93b3}
table{border-collapse:collapse;width:100%;font-size:13px}td,th{border:1px solid #2c2440;padding:7px 10px;text-align:left}
.idx{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:18px}
.big{font-size:26px;font-weight:800}
"""


def _thumb_b64(path, maxw=560):
    from PIL import Image
    im = Image.open(path)
    im.thumbnail((maxw, maxw))
    buf = io.BytesIO()
    if im.mode in ("RGBA", "LA"):
        im.save(buf, "PNG")
        mime = "image/png"
    else:
        im.convert("RGB").save(buf, "JPEG", quality=80)
        mime = "image/jpeg"
    return "data:%s;base64,%s" % (mime, base64.b64encode(buf.getvalue()).decode())


def _qc_badge(qc):
    qc = qc or {}
    s = qc.get("status", "?")
    cls = {"pass": "pass", "accepted_with_warnings": "warn", "failed": "fail"}.get(s, "warn")
    score = qc.get("vision_score")
    return '<span class="badge %s">%s%s</span>' % (
        cls, s, (" · %s/10" % score) if score is not None else "")


def write_task_sheet(task_dir: Path, man: dict) -> None:
    e = []
    e.append("<html><head><meta charset='utf-8'><title>%s — assets</title><style>%s</style></head>"
             "<body><div class='wrap'>" % (html.escape(man["title"]), CSS))
    p = man["client_persona"]
    e.append("<p class='muted'><a href='../index.html'>← all tasks</a></p>")
    e.append("<h1>Task %s — %s</h1>" % (man["task_id"], html.escape(man["title"])))
    e.append("<p class='muted'>%s · %s · feasibility <b>%s</b> · client: <b>%s</b> (%s)</p>" % (
        man["family"], man["category"], man["feasibility"],
        html.escape(p.get("brand_name") or ""), html.escape(p.get("industry") or "")))
    pal = " ".join("<span class='badge' style='background:%s;color:#000'>%s</span>" %
                   (c.get("hex"), c.get("hex")) for c in (p.get("palette") or []))
    e.append("<p>%s</p>" % pal)

    def _is_imagefile(a):
        return str(a.get("file") or "").lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
    img_entries = [a for a in man["assets"]
                   if a.get("kind") == "image" or (a.get("kind") == "program" and _is_imagefile(a))]
    other = [a for a in man["assets"] if a not in img_entries]

    if img_entries:
        e.append("<h2>Generated images (%d)</h2><div class='grid'>" % len(img_entries))
        for a in img_entries:
            f = task_dir / a["file"]
            if not f.exists():
                continue
            post = a.get("post_process") or []
            degr = next((pp for pp in post if pp.get("op") == "degrade"), None)
            e.append("<div class='card'>")
            if degr and degr.get("original") and (task_dir / degr["original"]).exists():
                e.append("<div class='pair'><div><img src='%s'><br>original (ground truth)</div>"
                         "<div><img src='%s'><br>degraded → agent input<br><span class='muted'>%s</span></div></div>"
                         % (_thumb_b64(task_dir / degr["original"], 360), _thumb_b64(f, 360),
                            degr.get("params", {}).get("profile", "")))
            else:
                e.append("<img src='%s'>" % _thumb_b64(f))
            gen = a.get("generator") or {}
            e.append("<div class='meta'><b>%s</b><br>%s/%s · %s · attempts %s</div>" % (
                html.escape(a["file"]), gen.get("provider"), gen.get("model"),
                a.get("dims"), (a.get("qc") or {}).get("attempts", 1)))
            e.append(_qc_badge(a.get("qc")))
            e.append("<details><summary>prompt</summary><pre>%s</pre></details>" %
                     html.escape((gen.get("prompt") or "")[:1800]))
            e.append("</div>")
        e.append("</div>")

    if other:
        e.append("<h2>Text & data assets (%d)</h2>" % len(other))
        for a in other:
            f = task_dir / a["file"] if a.get("file") else None
            e.append("<div class='card' style='margin-bottom:14px'><b>%s</b> %s"
                     % (html.escape(a.get("file") or a["key"]), _qc_badge(a.get("qc"))))
            e.append("<div class='meta'>%s</div>" % html.escape((a.get("input_requirement") or "")[:120]))
            if f and f.exists():
                try:
                    body = f.read_text()[:2600]
                except (UnicodeDecodeError, ValueError):
                    body = "(binary file, %d bytes)" % f.stat().st_size
                e.append("<details open><summary>content</summary><pre>%s</pre></details>"
                         % html.escape(body))
            e.append("</div>")

    e.append("<h2>Decisions & assumptions</h2><table><tr><th>Brief said</th><th>We assumed</th><th>Why</th></tr>")
    for d in man["decisions"]:
        e.append("<tr><td>%s</td><td>%s</td><td class='muted'>%s</td></tr>" % (
            html.escape(d["requirement"]), html.escape(d["assumed_value"]), html.escape(d["why"])))
    e.append("</table>")

    st = man.get("stats", {})
    e.append("<p class='muted' style='margin-top:24px'>images %s · regens %s · est cost $%.2f · ready_for_agent: <b>%s</b></p>"
             % (st.get("images_generated"), st.get("regenerations"), st.get("est_cost_usd", 0),
                man["ready_for_agent"]))
    e.append("<h2>Adobe workflow (next phase)</h2><pre>%s</pre>" % html.escape(man["mcp_workflow"]))
    e.append("</div></body></html>")
    (task_dir / "contact_sheet.html").write_text("".join(e))


def write_index() -> None:
    root = config.OUT_ROOT
    cards = []
    for mf in sorted(root.glob("*/manifest.json")):
        man = json.loads(mf.read_text())
        d = mf.parent.name
        st = man.get("stats", {})
        ready = man.get("ready_for_agent")
        # first image as cover
        cover = ""
        for a in man["assets"]:
            if a.get("kind") == "image" and (mf.parent / a.get("file", "")).exists():
                cover = "<img src='%s' style='width:100%%;border-radius:10px;background:#fff'>" % _thumb_b64(
                    mf.parent / a["file"], 420)
                break
        cards.append(
            "<div class='card'>%s<div class='big'>#%s</div><b>%s</b>"
            "<div class='meta'>%s · %s · %s assets · $%.2f</div>"
            "<span class='badge %s'>%s</span> "
            "<div style='margin-top:10px'><a href='%s/contact_sheet.html'>contact sheet</a> · "
            "<a href='%s/INTAKE.md'>INTAKE.md</a> · <a href='%s/manifest.json'>manifest</a></div></div>"
            % (cover, man["task_id"], html.escape(man["title"]),
               man["category"], man["client_persona"].get("brand_name") or "—",
               len(man["assets"]), st.get("est_cost_usd", 0),
               "pass" if ready else "fail", "ready_for_agent" if ready else "NOT READY",
               d, d, d))
    page = ("<html><head><meta charset='utf-8'><title>input_assets — pilot</title><style>%s</style></head>"
            "<body><div class='wrap'><h1>Input assets — 5-task pilot</h1>"
            "<p class='muted'>AI-generated client assets, ready for the Adobe-connector agent. "
            "Each folder: assets/ + manifest.json (the contract) + INTAKE.md.</p>"
            "<div class='idx'>%s</div></div></body></html>" % (CSS, "".join(cards)))
    root.mkdir(parents=True, exist_ok=True)
    (root / "index.html").write_text(page)
