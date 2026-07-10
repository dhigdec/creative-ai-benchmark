#!/usr/bin/env python
"""One-off: generate the MISSING broker walkthrough VO scratch wav for AO-23.

AO-23's spec requires walkthrough_raw_1080p.mp4 to carry a real continuous spoken
voice-over (steps 14 media_summarize / 15 quick_cut / 17 media_enhance_speech + the
two teaser deliverables all depend on it). The Seedance clip is silent and no VO
asset was ever produced. Every sibling AV task (AO-121/122/123/55/96/97) ships a
separate roughened scratch VO wav; this reproduces that pattern for AO-23.
"""
import glob, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
import generate_av as av
from adapters.text_llm import TextLLM

OUT = config.PROJECT_DIR / "input_assets"
outdir = Path(glob.glob(str(OUT / "AO-23_*"))[0])
tl = TextLLM()
def log(m): print(m)

inp = {
    "name": "walkthrough_vo_scratch.wav",
    "kind": "audio",
    "gen_prompt": (
        "Natural broker lavalier voice-over for a luxury Manhattan real-estate YouTube "
        "walkthrough of a Tribeca penthouse. A confident 45-year-old male luxury broker "
        "opens with a market-insight HOOK line, then walks the viewer through the property "
        "-- the great room with floor-to-ceiling windows and the Manhattan skyline, herringbone "
        "oak floors, the chef's kitchen, and the primary suite -- and references a recent "
        "comparable sale in the building/neighborhood to make the value case. Prestige, "
        "understated, editorial tone; unhurried delivery; roughly 60-75 seconds."
    ),
    "realism_notes": (
        "Raw lavalier take with light room tone and subtle handheld recording imperfections "
        "so media_enhance_speech has genuine denoise work; a single continuous spoken "
        "voice-over for media_summarize to transcribe and quick_cut to find the hook."
    ),
}

asset = av.do_audio("AO-23", inp, outdir, tl, log, force=True)
print("\n=== RETURNED ASSET DICT ===")
print(json.dumps(asset, indent=2))
