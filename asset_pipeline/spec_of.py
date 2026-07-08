#!/usr/bin/env python
"""Print a task's brief + the SPEC requirement for every input asset (what each asset must be).
Usage: .venv/bin/python spec_of.py AO-XX
"""
import glob, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
tid = sys.argv[1]
sp = [json.load(open(p)) for p in glob.glob(str(config.PROJECT_DIR / "complex_benchmark/adobe_only/specs/*.json"))
      if json.load(open(p))["id"] == tid]
if not sp:
    print("no spec for", tid); sys.exit(1)
s = sp[0]
print("TASK   :", tid, "-", s.get("title"))
print("ASK    :", s.get("one_line_ask"))
print("INPUTS (what each client-supplied asset must be):")
for i in s.get("inputs", []):
    print("  * %-34s [%s]" % (i.get("name"), i.get("kind")))
    gp = (i.get("gen_prompt") or "").strip()
    rn = (i.get("realism_notes") or "").strip()
    if gp: print("      requirement:", gp)
    if rn: print("      realism    :", rn)
