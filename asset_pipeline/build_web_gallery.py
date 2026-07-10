#!/usr/bin/env python
"""Self-contained web gallery for GitHub Pages.

The normal dashboards reference the 1.4GB of media by relative path (gitignored -> on GCS), so they
render broken on Pages. This builds a Pages-hostable gallery that EMBEDS base64 THUMBNAILS of every
asset (images + a poster frame per video) so it needs no external media. Video/audio are shown as
preview thumbnails, not playable (too large to embed — full playback needs the GCS media).

Writes docs/assets/index.html + docs/assets/<AO-XX>.html.  Run: .venv/bin/python build_web_gallery.py
"""
from __future__ import annotations
import base64, io, glob, html, json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
import build_dashboard as bd
from PIL import Image

OUT = config.PROJECT_DIR / "docs" / "assets"
CSS = bd.CSS + """
.thumb{width:100%;border-radius:8px;background:#fff;display:block}
.vid-badge{position:absolute;top:8px;left:8px;background:#000a;color:#fff;font-size:11px;font-weight:700;border-radius:6px;padding:2px 8px}
.rel{position:relative}.miss{padding:30px;text-align:center;color:#6b6088;font-size:12px;background:#221a38;border-radius:8px}
"""

def _thumb(path, maxw=560, q=78):
    try:
        im = Image.open(path); im.thumbnail((maxw, maxw))
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGB")
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=q)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return None

def _video_thumb(video, maxw=560):
    pf = bd.poster_for(video)
    if pf and pf.exists():
        return _thumb(pf, maxw)
    tmp = video.parent / ("_wpv_" + video.name + ".jpg")
    try:
        from adapters.media_gen import _ffmpeg
        subprocess.run([_ffmpeg(), "-y", "-ss", "2", "-i", str(video), "-frames:v", "1", str(tmp)], capture_output=True)
        t = _thumb(tmp, maxw) if tmp.exists() else None
        if tmp.exists():
            tmp.unlink()
        return t
    except Exception:
        return None

def build():
    OUT.mkdir(parents=True, exist_ok=True)
    cons = bd.load_consistency()
    cards = []
    tot = {"img": 0, "vid": 0, "aud": 0, "data": 0}
    for mf in sorted(glob.glob(str(config.OUT_ROOT / "AO-*/manifest.json")),
                     key=lambda p: int(Path(p).parent.name.split("_")[0].split("-")[1])):
        td = Path(mf).parent
        man = json.load(open(mf))
        tid = man.get("task_id") or td.name.split("_")[0]
        title = man.get("title") or tid
        brief = man.get("one_line_ask") or bd.spec_ask(tid)
        pr = bd.price_of(tid)
        files, groups = bd.group_files(td, man)
        for k, kk in (("img", "image"), ("vid", "video"), ("aud", "audio"), ("data", "data")):
            tot[k] += len(groups[kk])
        # per-task page
        e = ["<html><head><meta charset='utf-8'><title>%s — %s</title><style>%s</style></head><body><div class='wrap'>"
             % (tid, html.escape(title), CSS)]
        e.append("<p class='muted'><a href='index.html'>← all tasks</a></p>")
        e.append("<h1>%s — %s</h1>" % (tid, html.escape(title)))
        if pr.get("display"):
            e.append("<span class='chip price'>\U0001F4B0 %s</span> " % html.escape(pr["display"]))
        e.append("<span class='chip'>%d assets</span>" % len(files))
        if brief:
            e.append("<p class='muted' style='margin-top:8px'>%s</p>" % html.escape(brief))
        cover = None
        if groups["image"]:
            e.append("<h2>Images (%d)</h2><div class='grid'>" % len(groups["image"]))
            for p, _m in groups["image"]:
                t = _thumb(p)
                if t and cover is None:
                    cover = _thumb(p, 300)
                cell = ("<img class='thumb' loading='lazy' src='%s'>" % t) if t else "<div class='miss'>image unavailable</div>"
                e.append("<div class='asset'>%s<div class='aname'>%s</div></div>" % (cell, html.escape(p.name)))
            e.append("</div>")
        if groups["video"]:
            e.append("<h2>Video (%d) <span class='muted' style='font-size:12px'>— preview frame; full playback via GCS</span></h2><div class='grid'>" % len(groups["video"]))
            for p, _m in groups["video"]:
                t = _video_thumb(p)
                if t and cover is None:
                    cover = t
                cell = ("<div class='rel'><img class='thumb' loading='lazy' src='%s'><span class='vid-badge'>▶ VIDEO</span></div>" % t) if t else "<div class='miss'>video preview unavailable</div>"
                e.append("<div class='asset'>%s<div class='aname'>%s</div></div>" % (cell, html.escape(p.name)))
            e.append("</div>")
        if groups["audio"]:
            e.append("<h2>Audio (%d)</h2><div class='grid'>" % len(groups["audio"]))
            for p, _m in groups["audio"]:
                e.append("<div class='asset'><div class='miss'>\U0001F509 audio — playback via GCS</div><div class='aname'>%s</div></div>" % html.escape(p.name))
            e.append("</div>")
        if groups["data"]:
            e.append("<h2>Data &amp; other (%d)</h2>" % len(groups["data"]))
            for p, _m in groups["data"]:
                e.append("<div class='asset' style='margin-bottom:10px'><b>%s</b>" % html.escape(p.name))
                if p.suffix.lower() in (".csv", ".json", ".txt", ".md") or p.name.endswith(".proxy.txt"):
                    try:
                        e.append("<details><summary>content</summary><pre>%s</pre></details>" % html.escape(p.read_text()[:2000]))
                    except Exception:
                        pass
                e.append("</div>")
        e.append("</div></body></html>")
        (OUT / ("%s.html" % tid)).write_text("".join(e))
        cards.append({"tid": tid, "title": title, "brief": brief, "cover": cover,
                      "price": pr.get("display", ""), "consistent": cons.get(tid, True),
                      "img": len(groups["image"]), "vid": len(groups["video"]),
                      "aud": len(groups["audio"]), "data": len(groups["data"])})
    # index
    e = ["<html><head><meta charset='utf-8'><title>StudioBench — asset gallery</title><style>%s</style></head><body><div class='wrap'>" % CSS]
    e.append("<h1>StudioBench — input asset gallery</h1>")
    e.append("<p class='muted'>Every input asset for all %d tasks, shown as embedded thumbnails (self-contained — no external media). "
             "Video tiles show a preview frame; full-resolution / playable media is on GCS. "
             "<a href='../index.html'>← reports</a></p>" % len(cards))
    e.append("<div class='summary'>")
    for n, l in [(len(cards), "tasks"), (sum(tot.values()), "assets"), (tot["img"], "images"),
                 (tot["vid"], "video"), (tot["aud"], "audio"), (tot["data"], "data")]:
        e.append("<div class='stat'><div class='n'>%s</div><div class='l'>%s</div></div>" % (n, l))
    e.append("</div><div class='idx'>")
    for c in cards:
        cov = ("<img class='cover' loading='lazy' src='%s'>" % c["cover"]) if c["cover"] else "<div class='novid'>data / audio only</div>"
        counts = " · ".join("%d %s" % (c[k], lbl) for k, lbl in [("img", "img"), ("vid", "vid"), ("aud", "aud"), ("data", "data")] if c[k])
        e.append("<div class='card'><a href='%s.html'>%s</a><div class='tid'>%s</div><div class='ttl'>%s</div>"
                 "<div class='counts'>%s%s</div><div style='margin-top:6px'><a href='%s.html'>open →</a></div></div>"
                 % (c["tid"], cov, c["tid"], html.escape(c["title"]),
                    ("\U0001F4B0 %s · " % c["price"]) if c["price"] else "", counts, c["tid"]))
    e.append("</div></div></body></html>")
    (OUT / "index.html").write_text("".join(e))
    print("wrote %s (%d task pages + index)" % (OUT, len(cards)))
    print("assets embedded: %d img, %d video-frames, %d audio(label), %d data" % (tot["img"], tot["vid"], tot["aud"], tot["data"]))

if __name__ == "__main__":
    build()
