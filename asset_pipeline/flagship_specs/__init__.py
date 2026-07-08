"""Flagship round-3 TaskSpecs (complex multi-deliverable creative tasks).

Each module is self-contained (no pipeline imports) and exports SPEC + BRIEF_MD.
specs.py merges FLAGSHIP_SPECS into the global SPECS registry.
"""
from .spec_5366 import SPEC as SPEC_5366, BRIEF_MD as BRIEF_5366
from .spec_3437 import SPEC as SPEC_3437, BRIEF_MD as BRIEF_3437
from .spec_3252 import SPEC as SPEC_3252, BRIEF_MD as BRIEF_3252
from .spec_5388 import SPEC as SPEC_5388, BRIEF_MD as BRIEF_5388
from .spec_1559 import SPEC as SPEC_1559, BRIEF_MD as BRIEF_1559

FLAGSHIP_SPECS = {5366: SPEC_5366, 3437: SPEC_3437, 3252: SPEC_3252,
                  5388: SPEC_5388, 1559: SPEC_1559}
FLAGSHIP_BRIEFS = {5366: BRIEF_5366, 3437: BRIEF_3437, 3252: BRIEF_3252,
                   5388: BRIEF_5388, 1559: BRIEF_1559}
FLAGSHIP_ORDER = [1559, 3437, 5366, 5388, 3252]  # cheapest-first
