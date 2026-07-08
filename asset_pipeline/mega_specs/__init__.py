"""Round-5 definitive mega-task specs — auto-discovers spec_<id>.py modules.

Each module exports RECORD (dataset row), SPEC (generation spec), BRIEF_MD.
specs.py merges MEGA_RECORDS into the dataset and MEGA_SPECS into the SPECS registry.
"""
from __future__ import annotations
import importlib
import pkgutil
from pathlib import Path

MEGA_SPECS = {}
MEGA_RECORDS = {}
MEGA_BRIEFS = {}

_pkg = __name__
for _m in pkgutil.iter_modules([str(Path(__file__).resolve().parent)]):
    if not _m.name.startswith("spec_"):
        continue
    try:
        mod = importlib.import_module("%s.%s" % (_pkg, _m.name))
    except Exception as _e:  # a half-written module shouldn't break the whole pipeline
        continue
    spec = getattr(mod, "SPEC", None)
    rec = getattr(mod, "RECORD", None)
    if spec and rec:
        MEGA_SPECS[rec["id"]] = spec
        MEGA_RECORDS[rec["id"]] = rec
        brief = getattr(mod, "BRIEF_MD", None)
        if brief:
            MEGA_BRIEFS[rec["id"]] = brief

MEGA_ORDER = sorted(MEGA_SPECS)
