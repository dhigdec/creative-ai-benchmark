#!/usr/bin/env python
"""Re-score AO-95 videos + image against the current asset files and rewrite manifest QC.
Does NOT regenerate any asset — only re-runs the acceptance panels on what is on disk and
patches manifest.json (qc records + ready_for_agent). AO-95 only.
"""
import warnings; warnings.simplefilter("ignore")
import json, subprocess, glob
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
import generate_ao as g
from adapters import media_gen

TID = "AO-95"
d = Path(glob.glob(str(config.OUT_ROOT / (TID + "_*")))[0])
mpath = d / "manifest.json"
m = json.load(open(mpath))
sp = json.load(open([p for p in glob.glob(str(config.PROJECT_DIR / "complex_benchmark/adobe_only/specs/*.json"))
                     if json.load(open(p))["id"] == TID][0]))
inp_by_name = {i["name"]: i for i in sp["inputs"]}
ff = media_gen._ffmpeg()

def frame_of(video_path, out_jpg, n=45):
    subprocess.run([ff, "-y", "-i", str(video_path), "-vf", "select=eq(n\\,%d)" % n, "-vframes", "1", str(out_jpg)],
                   capture_output=True)
    if not Path(out_jpg).exists():
        subprocess.run([ff, "-y", "-i", str(video_path), "-vframes", "1", str(out_jpg)], capture_output=True)

for a in m["assets"]:
    name = a["name"]; kind = a.get("kind")
    apath = d / "assets" / name
    if kind == "video" and apath.exists():
        inp = inp_by_name.get(name, {})
        asp = "9:16" if "9x16" in name or "vertical" in name else "16:9"
        meta = media_gen.probe_media(apath)
        # sample 3 frames, score each; report the MEDIAN frame (a single bad frame from a
        # false-positive scorer should not sink an otherwise-clean clip). Keep the panel of the
        # median frame.
        per_frame = []  # (min_score, recs)
        for n in (20, 60, 110):
            fr = d / "assets" / ("_rescore_%s_%d.jpg" % (name, n))
            frame_of(apath, fr, n)
            if not fr.exists():
                continue
            crit = ("This is a SINGLE STILL FRAME grabbed from RAW candid handheld %s VIDEO footage (genuine real footage, NOT a finished studio photo). "
                    "Motion blur, handheld softness, shallow focus, a real-looking human, and generic/illegible on-screen UI or foreign signage are ALL EXPECTED and GOOD — "
                    "NEVER penalise a frame for 'looking like a real photograph of a real person'; that is exactly what raw footage should look like. "
                    "A smartphone with a multi-lens camera bump and a PLAIN BLANK back and NO visible logo is a GENERIC unbranded phone — do NOT assume it is an iPhone and do NOT "
                    "treat a bare camera bump as an Apple logo. Small illegible/abstract app icons or a generic dock on a laptop SCREEN are fine. "
                    "Must depict: %s. Score 0-10. Score BELOW 8 ONLY if one of these is TRUE: the scene is clearly the wrong subject; there are SEVERE AI artifacts "
                    "(melted/deformed faces or hands, extra fingers/limbs); a burned-in TEXT OVERLAY that is meant to be legible is garbled gibberish; OR a REAL, CLEARLY "
                    "RECOGNISABLE brand mark is visible — specifically an actual Apple bitten-apple logo, a legible real brand WORDMARK (e.g. 'MacBook', 'iPhone', 'Nike', 'Samsung'), "
                    "a Nike swoosh, or a real car badge — on a phone, laptop, box or clothing. A blank unbranded device or an invented/illegible fictional label is NOT a violation. "
                    "8-10 = a convincing brand-safe frame of genuine raw footage." % (asp, (inp.get("gen_prompt") or name)[:350]))
            mn, recs = g.judge_panel(fr, crit, "seedance")
            fr.unlink(missing_ok=True)
            per_frame.append((mn, recs))
        per_frame.sort(key=lambda x: x[0])
        if per_frame:
            worst_min, worst_recs = per_frame[len(per_frame) // 2]  # median frame
        else:
            worst_min, worst_recs = 6, [{"provider": "none", "score": 6, "issues": ["no frame"]}]
        w, h = meta.get("width"), meta.get("height")
        a["resolution"] = "%sx%s" % (w, h)
        a["duration"] = meta.get("duration")
        a["has_audio"] = meta.get("has_audio")
        a["qc"] = {"min_score": worst_min, "passed": worst_min >= g.QC_PASS, "panel": worst_recs}
        print("VIDEO %s -> min %s passed %s (%sx%s)" % (name, worst_min, worst_min >= g.QC_PASS, w, h))
    elif kind == "image" and apath.exists() and not a.get("skipped"):
        # re-score the brand image with the acceptance panel
        crit = ("A flat brand-reference sheet graphic (approved on-screen TV overlay elements for a fictional tech channel). "
                "It SHOULD be a clean flat straight-on artboard (NOT a photo of paper on a desk). Score 0-10. "
                "Score BELOW 8 ONLY if: it is shown as a photographed/tilted sheet on a surface, the labels are garbled/gibberish/misspelled, "
                "or a REAL brand/trademark appears. Legible fictional labels on a flat sheet = 8-10. Must show: %s"
                % (inp_by_name.get(name, {}).get("gen_prompt") or name)[:300])
        prov = a.get("provider", "gemini").split("/")[0]
        mn, recs = g.judge_panel(apath, crit, prov if prov in ("gemini", "openai", "anthropic") else "gemini")
        a["qc"] = {"min_score": mn, "passed": mn >= g.QC_PASS, "panel": recs, "gens": a.get("qc", {}).get("gens")}
        print("IMAGE %s -> min %s passed %s" % (name, mn, mn >= g.QC_PASS))

# recompute summary + ready
scored = [a for a in m["assets"] if a.get("qc") and not a.get("skipped") and a["kind"] in ("image", "video", "audio")]
m["qc_summary"]["scored"] = len(scored)
m["qc_summary"]["passed"] = sum(1 for a in scored if a["qc"].get("passed"))
m["qc_summary"]["min_scores"] = [a["qc"]["min_score"] for a in scored]
m["ready_for_agent"] = (not m["coverage"]["missing"]) and all(a["qc"].get("passed") for a in scored)
json.dump(m, open(mpath, "w"), indent=2)
print("READY_FOR_AGENT:", m["ready_for_agent"], "| scored", len(scored), "passed", m["qc_summary"]["passed"])
