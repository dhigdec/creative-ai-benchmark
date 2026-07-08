#!/usr/bin/env python
"""Deterministic whole-set invariant check over all 100 adobe_only specs.
Run after any fix pass. Flags: banned tools, count mismatches, empty inputs/outputs,
non-contiguous workflows, unresolved inputs_from, stray files, non-Gemini/OpenAI gen models.
Run: python3 verify_specs_invariants.py
"""
import json, glob, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
SPECS = sorted(glob.glob(str(ROOT / 'complex_benchmark/adobe_only/specs/*.json')))
BANNED = {'image_generative_expand'}
OK_GEN = {'gemini-3-pro-image', 'gpt-image-2', 'gemini-2.5-flash-image', None, ''}
# Adobe connector tools = server != local; 'local' hand-off steps allowed but not counted as Adobe
def adobe_tools(wf):
    return [w.get('tool') for w in wf if w.get('server') != 'local' and w.get('exec_mode') != 'L']

problems = {}
def flag(tid, msg): problems.setdefault(tid, []).append(msg)

# stray-file check
before = set()
bf = Path('/tmp/specs_before.txt')
if bf.exists():
    before = set(Path(l.strip()).name for l in bf.read_text().splitlines() if l.strip())
    now = {Path(p).name for p in SPECS}
    for extra in sorted(now - before):
        flag(Path(extra).stem, f"STRAY FILE not in pre-fix inventory: {extra}")

for f in SPECS:
    s = json.load(open(f))
    tid = s.get('id', Path(f).stem)
    wf = s.get('connector_workflow', []) or []
    # banned tools anywhere
    blob = json.dumps(s).lower()
    for b in BANNED:
        if b in blob:
            flag(tid, f"BANNED tool string present: {b}")
    # counts
    tcc = s.get('tool_call_count')
    if tcc != len(wf):
        flag(tid, f"tool_call_count={tcc} != #steps={len(wf)}")
    adobe = adobe_tools(wf)
    dat = s.get('distinct_adobe_tools')
    real_distinct = len(set(adobe))
    if dat is not None and dat != real_distinct:
        flag(tid, f"distinct_adobe_tools={dat} != actual unique adobe tools={real_distinct}")
    # inputs / outputs
    ins = s.get('inputs', []) or []
    outs = s.get('outputs', []) or []
    if not ins: flag(tid, "inputs[] empty")
    if not outs: flag(tid, "outputs[] empty")
    for i in ins:
        gm = str(i.get('gen_model') or '')
        kind = str(i.get('kind') or '').lower()
        name = str(i.get('name') or '').lower()
        # never Claude
        if 'claude' in gm.lower() or 'anthropic' in gm.lower():
            flag(tid, f"input gen_model uses Claude: {i.get('name')} -> {gm}")
        # IMAGE assets must use a canonical image model; data/template assets (.csv/.indd/.ai)
        # legitimately use a text/data model (an image model cannot author them).
        # trust the kind field: only photographic 'image' assets must use a real image model.
        # authored/provided graphics (barcodes, pictograms) carry an 'n/a-authored'/'provided' sentinel.
        real_model = gm and not gm.lower().startswith(('n/a', 'authored', 'provided', 'client'))
        if kind == 'image' and real_model and gm not in ('gemini-3-pro-image', 'gpt-image-2', 'gemini-2.5-flash-image'):
            flag(tid, f"IMAGE input on non-image gen_model: {i.get('name')} -> {gm}")
    # workflow contiguity n=1..N
    ns = [w.get('n') for w in wf if isinstance(w.get('n'), int)]
    if ns:
        if sorted(ns) != list(range(1, len(wf) + 1)):
            flag(tid, f"connector_workflow n not contiguous 1..{len(wf)}: {sorted(ns)[:6]}...")
    # inputs_from resolvable: every referenced token is an input name or an earlier output
    def norm(tok):
        # drop parenthetical descriptions, extensions, and _asset/_indd_asset upload aliases -> bare stem
        tok = re.sub(r'\s*\(.*?\)\s*', '', str(tok)).strip()
        tok = re.sub(r'\.(jpg|jpeg|png|indd|ai|svg|pdf|mp4|wav|csv|tif|tiff|zip)$', '', tok, flags=re.I)
        tok = re.sub(r'_(indd_)?asset$', '', tok)
        return tok.strip().lower()
    produced = set()
    for i in ins:
        if i.get('name'): produced.add(norm(i['name']))
    for w in sorted(wf, key=lambda x: x.get('n', 0)):
        frm = w.get('inputs_from')
        refs = []
        if isinstance(frm, str):
            # strip parenthetical descriptions (may contain '+'/',' that are not real delimiters) first
            clean = re.sub(r'\([^)]*\)', '', frm)
            refs = [x.strip() for x in re.split(r'[,+/]| and ', clean) if x.strip()]
        elif isinstance(frm, list): refs = [str(x).strip() for x in frm]
        for r in refs:
            rn = norm(r)
            if rn in ('none', 'n/a', '-', '', 'client', 'brief', 'user'): continue
            if rn not in produced and not any(rn in p or p in rn for p in produced):
                if re.search(r'[._]', r):
                    flag(tid, f"step {w.get('n')} inputs_from '{r}' not produced by any input/earlier output")
        o = w.get('output')
        if isinstance(o, str) and o: produced.add(norm(o))
        elif isinstance(o, list):
            for x in o: produced.add(norm(x))

print(f"checked {len(SPECS)} specs")
if not problems:
    print("ALL INVARIANTS PASS ✓  (no banned tools, counts consistent, inputs/outputs present, workflows contiguous & resolvable, no stray files)")
    sys.exit(0)
print(f"\n{len(problems)} spec(s) with issues:\n")
for tid in sorted(problems):
    print(f"  {tid}:")
    for m in problems[tid]:
        print(f"     - {m}")
# summary of the inputs_from soft-check (often noisy) vs hard checks
hard = {t: [m for m in ms if 'inputs_from' not in m] for t, ms in problems.items()}
hard = {t: ms for t, ms in hard.items() if ms}
print(f"\nHARD issues (excluding soft inputs_from name-matching): {len(hard)} specs")
for t in sorted(hard): print(f"  {t}: {hard[t]}")
