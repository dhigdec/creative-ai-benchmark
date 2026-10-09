#!/usr/bin/env python3
"""V3 PDF renderer — the third deferred type from generate_v3.py.

Reads type=pdf assets from asset_plan.json files and renders a REAL, correctly-dimensioned,
single-record press PDF from each authored LAYOUT SPEC in `content`, baking in the load-bearing
structural traps the specs describe:
  - trim size in mm (+ bleed only when the spec says bleed is present; media-box == trim otherwise)
  - the item name / size / price set as ONE continuous text object (the single-flow reverse-eng trap)
  - a decorative roundel/sunburst drawn as a VECTOR PATH (not a picture frame) where the spec says so
  - a real picture WELL (graphic frame) only where the spec places a piece image

It parses dimensions, bleed, hex colours and field labels heuristically from the prose spec. Output is a
genuine convertible PDF (reportlab) at the right trim/bleed with embedded base-14 fonts.

Usage:
  python render_v3_pdfs.py --all [--force] [--dry-run]
  python render_v3_pdfs.py --only LAYOUT-02,LAYOUT-05
"""
from __future__ import annotations
import argparse, glob, json, re, sys, time
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, Color

V3 = Path(__file__).resolve().parent.parent / "input_assets_v3"

def _lum(hexs):
    c = HexColor(hexs); return 0.299*c.red + 0.587*c.green + 0.114*c.blue
def _sat(hexs):
    c = HexColor(hexs); mx=max(c.red,c.green,c.blue); mn=min(c.red,c.green,c.blue)
    return 0 if mx==0 else (mx-mn)/mx

def parse(content):
    c = content or ""
    # dimensions: first "W x H mm"
    dims = re.findall(r'(\d+)\s*x\s*(\d+)\s*mm', c, re.I)
    if dims:
        w, h = int(dims[0][0]), int(dims[0][1])
    else:
        w, h = 105, 148  # A6 default
    low = c.lower()
    if "portrait" in low and w > h: w, h = h, w
    if "landscape" in low and h > w: w, h = h, w
    # bleed
    if any(k in low for k in ("no bleed", "0 mm bleed", "media box = trim", "media box equals the trim", "trim = media box", "no bleed box")):
        bleed = 0
    else:
        mb = re.search(r'(\d+(?:\.\d+)?)\s*mm bleed', low)
        bleed = float(mb.group(1)) if mb else 0
    # colours
    hexes = re.findall(r'#[0-9A-Fa-f]{6}', c)
    hexes = list(dict.fromkeys(hexes))
    ground = max(hexes, key=_lum) if hexes else "#F3EFE7"
    ink = min(hexes, key=_lum) if hexes else "#231F20"
    accents = [h for h in hexes if h not in (ground, ink)]
    accent = max(accents, key=_sat) if accents else (max(hexes, key=_sat) if hexes else "#B4382C")
    # field labels: UPPERCASE tokens / known fields
    fields = re.findall(r'\b([A-Z][A-Z _]{2,}[A-Z])\b', c)
    known = ["ITEM_NAME","ITEM NAME","PIECE NAME","NAME","REFERENCE","SIZE","PRICE","METAL","DIMENSIONS","DIETARY_TAGS","DIETARY TAGS","MODEL","DESCRIPTION","SKU"]
    labels = [k for k in known if k.upper() in c.upper()]
    if not labels:
        labels = [f for f in fields if f not in ("PDF","LAYOUT","SPEC","WHAT","HOW","NO","NOTE","FIELD")][:5] or ["ITEM NAME","SIZE","PRICE"]
    single_flow = any(k in low for k in ("one flow","one continuous","single continuous","one text frame","one text story","continuous text story","one continuous text story"))
    roundel = any(k in low for k in ("roundel","sunburst","starburst"))
    picture = any(k in low for k in ("picture","piece image","photograph","image well","graphic frame","product photo")) and "not a picture" not in low
    return dict(w=w,h=h,bleed=bleed,ground=ground,ink=ink,accent=accent,labels=labels[:6],
                single_flow=single_flow,roundel=roundel,picture=picture)

SAMPLE = {"ITEM NAME":"House Special","ITEM_NAME":"House Special","PIECE NAME":"The Vesper","NAME":"The Vesper",
          "REFERENCE":"REF-0417","SIZE":"Half","PRICE":"$14","METAL":"18ct Yellow Gold","DIMENSIONS":"18 x 12 mm",
          "DIETARY TAGS":"V  GF","DIETARY_TAGS":"V  GF","MODEL":"MV-22","DESCRIPTION":"Single record proof","SKU":"SKU-0417"}

def starburst(cnv, cx, cy, r, color, points=16):
    from math import cos, sin, pi
    cnv.setFillColor(color); cnv.setStrokeColor(color)
    p = cnv.beginPath()
    for i in range(points*2):
        rr = r if i % 2 == 0 else r*0.72
        a = pi*i/points
        x = cx + rr*cos(a); y = cy + rr*sin(a)
        (p.moveTo if i == 0 else p.lineTo)(x, y)
    p.close(); cnv.drawPath(p, fill=1, stroke=0)

def render(a, adir, force, dry):
    fn = a["filename"]; dest = adir / fn
    dest.parent.mkdir(parents=True, exist_ok=True)
    rec = {"filename": fn, "type": "pdf", "status": "?"}
    if dest.exists() and not force:
        rec["status"] = "skip"; return rec
    s = parse(a.get("content"))
    if dry:
        rec.update(status="dry", **{k: s[k] for k in ("w","h","bleed","single_flow","roundel","picture")}); return rec
    try:
        W = (s["w"] + 2*s["bleed"]) * mm; H = (s["h"] + 2*s["bleed"]) * mm
        b = s["bleed"] * mm
        c = canvas.Canvas(str(dest), pagesize=(W, H))
        c.setTitle(fn)
        # ground over full media box
        c.setFillColor(HexColor(s["ground"])); c.rect(0, 0, W, H, fill=1, stroke=0)
        cw = s["w"]*mm; ch = s["h"]*mm  # trim content box origin at (b,b)
        # picture well (a real graphic frame) top area
        if s["picture"] and not s["roundel"]:
            pw = cw*0.5; px = b + (cw-pw)/2; py = b + ch*0.46
            c.setStrokeColor(HexColor(s["ink"])); c.setLineWidth(0.6)
            c.setFillColor(Color(0,0,0,0.05)); c.rect(px, py, pw, pw*0.8, fill=1, stroke=1)
            c.setFillColor(HexColor(s["ink"])); c.setFont("Helvetica", 6)
            c.drawCentredString(px+pw/2, py+pw*0.4, "[ PIECE IMAGE ]")
        # decorative roundel (vector path, NOT a picture frame)
        if s["roundel"]:
            rx = b + cw*0.76; ry = b + ch*0.62; rr = min(cw, ch)*0.16
            starburst(c, rx, ry, rr, HexColor(s["accent"]))
            c.setFillColor(HexColor(s["ground"])); c.setFont("Helvetica-Bold", 11)
            c.drawCentredString(rx, ry-4, SAMPLE.get("PRICE","$14"))
        # field text — SINGLE continuous text object when the trap says one flow
        tx = b + cw*0.08; ty = b + ch*0.34
        c.setFillColor(HexColor(s["ink"]))
        if s["single_flow"]:
            to = c.beginText(tx, ty); first = True
            for lab in s["labels"]:
                val = SAMPLE.get(lab.upper(), SAMPLE.get(lab, lab.title()))
                to.setFont("Helvetica-Bold" if first else "Helvetica", 15 if first else 9)
                to.textLine(val); first = False
            c.drawText(to)  # one text object = the single-flow trap
        else:
            yy = ty
            for i, lab in enumerate(s["labels"]):
                val = SAMPLE.get(lab.upper(), SAMPLE.get(lab, lab.title()))
                c.setFont("Helvetica-Bold" if i == 0 else "Helvetica", 15 if i == 0 else 9)
                c.drawString(tx, yy, val); yy -= (18 if i == 0 else 12)
        # crop marks only if bleed present
        if s["bleed"] > 0:
            c.setStrokeColor(HexColor(s["ink"])); c.setLineWidth(0.3); ml = 3*mm
            for (x, y, dx, dy) in [(b,b,-1,0),(b,b,0,-1),(W-b,b,1,0),(W-b,b,0,-1),
                                   (b,H-b,-1,0),(b,H-b,0,1),(W-b,H-b,1,0),(W-b,H-b,0,1)]:
                c.line(x, y, x+dx*ml, y+dy*ml)
        c.showPage(); c.save()
        rec.update(status="ok", trim="%dx%dmm"%(s["w"],s["h"]), bleed=s["bleed"],
                   single_flow=s["single_flow"], roundel=s["roundel"], bytes=dest.stat().st_size)
    except Exception as e:
        rec["status"] = "ERR: %s: %s" % (type(e).__name__, str(e)[:180])
    return rec

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan"); ap.add_argument("--only"); ap.add_argument("--all", action="store_true")
    ap.add_argument("--force", action="store_true"); ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if args.plan: paths=[Path(args.plan)]
    elif args.only: paths=[V3/t.strip()/"asset_plan.json" for t in args.only.split(",")]
    else: paths=[Path(p) for p in sorted(glob.glob(str(V3/"*"/"asset_plan.json")))]
    paths=[p for p in paths if p.exists()]
    results={}
    for pp in paths:
        d=json.loads(pp.read_text()); tid=d["task_id"]; adir=V3/tid/"assets"; adir.mkdir(parents=True,exist_ok=True)
        for a in d.get("assets",[]):
            if a.get("type")=="pdf":
                results.setdefault(tid,[]).append(render(a,adir,args.force,args.dry_run))
    allr=[r for v in results.values() for r in v]
    ok=sum(1 for r in allr if r["status"]=="ok"); sk=sum(1 for r in allr if r["status"]=="skip")
    err=[r for r in allr if r["status"].startswith("ERR")]
    print("PDFs: %d ok, %d skip, %d err, %d tasks"%(ok,sk,len(err),len(results)))
    for r in err[:30]: print("  ERR",r["filename"],r["status"])
    # merge into manifests
    if not args.dry_run:
        for tid,recs in results.items():
            mp=V3/tid/"manifest.json"; man=json.loads(mp.read_text()) if mp.exists() else {"task_id":tid,"assets":[]}
            by={a.get("filename"):a for a in man.get("assets",[])}
            for r in recs: by[r["filename"]]=r
            man["assets"]=list(by.values()); man["pdf_rendered_at"]=int(time.time()); mp.write_text(json.dumps(man,indent=1))

if __name__=="__main__":
    main()
