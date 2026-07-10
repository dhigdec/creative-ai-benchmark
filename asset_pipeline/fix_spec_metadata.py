#!/usr/bin/env python
"""One-shot source-of-truth corrections to the specs so every derived artifact stays consistent.

1. distinct_adobe_tools: for tasks where this integer is stale (!= number of DISTINCT tools in tools_used),
   set it to len(set(tools_used)) — the accurate count. tools_used has no duplicates anywhere, so this is
   just correcting an under-count that had drifted when tools were added without updating the field.
2. AO-123: the manifest provides an extra `lecture_audio_raw.wav` (the extracted lecture audio track, a real
   companion input for the audio-clean step) that spec.inputs omits. Add it so spec.inputs matches what the
   agent actually receives.

Idempotent. Run:  .venv/bin/python fix_spec_metadata.py [--apply]   (default = dry-run)
"""
from __future__ import annotations
import glob, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config

APPLY = "--apply" in sys.argv
SPECS = config.PROJECT_DIR / "complex_benchmark/adobe_only/specs"

changed = []
for p in glob.glob(str(SPECS / "*.json")):
    s = json.load(open(p)); tid = s["id"]; dirty = False
    true_distinct = len(set(s.get("tools_used") or []))
    if true_distinct and s.get("distinct_adobe_tools") != true_distinct:
        changed.append(f"{tid}: distinct_adobe_tools {s.get('distinct_adobe_tools')} -> {true_distinct}")
        s["distinct_adobe_tools"] = true_distinct; dirty = True
    if tid == "AO-123":
        names = {i.get("name") for i in (s.get("inputs") or [])}
        if "lecture_audio_raw.wav" not in names:
            # insert right after the lecture video it derives from
            inputs = s.get("inputs") or []
            wav = {"name": "lecture_audio_raw.wav", "kind": "audio",
                   "note": "Extracted raw audio track of lecture_talkinghead_raw.mp4, supplied for the audio-clean/enhance step."}
            idx = next((k for k, i in enumerate(inputs) if i.get("name") == "lecture_talkinghead_raw.mp4"), len(inputs))
            inputs.insert(idx + 1, wav); s["inputs"] = inputs
            changed.append(f"{tid}: +input lecture_audio_raw.wav (now {len(inputs)} inputs)"); dirty = True
    if dirty and APPLY:
        json.dump(s, open(p, "w"), indent=2, ensure_ascii=False)

print("\n".join(changed) if changed else "no changes")
print(f"\n{len(changed)} corrections " + ("APPLIED" if APPLY else "(dry-run; pass --apply to write)"))
