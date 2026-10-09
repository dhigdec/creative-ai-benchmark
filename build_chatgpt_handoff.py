#!/usr/bin/env python3
"""Build the ChatGPT+Adobe handoff appendix (all 100 tasks) from real specs/assets/verifiers."""
import json, glob, os, re

ROOT = "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads"
AO = f"{ROOT}/complex_benchmark/adobe_only"

def fam(d):
    tu = set(d.get('tools_used') or []); outs = json.dumps(d.get('outputs') or [])
    if tu & {'video_resize','video_create_quick_cut','media_summarize','media_enhance_speech'} or '.mp4' in outs or '.mov' in outs: return 'Motion & Audio'
    if tu & {'document_merge_data_layout','document_render_layout','document_merge_data_vector','document_render_vector','document_convert_pdf','prepare_indd_merge_template'}: return 'Layout & Data'
    if 'image_vectorize' in tu: return 'Vector & Print'
    return 'Photo & Image'

# newest spec per id
seen = {}
for f in glob.glob(f"{AO}/specs_rebuilt/*.json"): seen[os.path.basename(f).split('_')[0]] = f
for f in glob.glob(f"{AO}/specs/*.json"): seen.setdefault(os.path.basename(f).split('_')[0], f)

verifiers = {}
vf = f"{ROOT}/authored_verifiers.json"
if os.path.exists(vf):
    try: verifiers = json.load(open(vf))
    except Exception: verifiers = {}

# map AO-id -> input_assets dir
asset_dirs = {}
for d in glob.glob(f"{ROOT}/input_assets/*/"):
    b = os.path.basename(d.rstrip('/'))
    m = re.match(r'(AO-\d+)_', b)
    if m: asset_dirs[m.group(1)] = d.rstrip('/')

def list_assets(aid):
    d = asset_dirs.get(aid)
    if not d: return [], None
    ad = os.path.join(d, 'assets')
    if not os.path.isdir(ad): ad = d
    files = sorted([os.path.basename(x) for x in glob.glob(os.path.join(ad, '*'))
                    if os.path.isfile(x) and not os.path.basename(x).startswith('.')])
    rel = os.path.relpath(ad, ROOT)
    return files, rel

rows = []
for aid, f in seen.items():
    d = json.load(open(f))
    rows.append((aid, d))
def keyfn(r):
    m = re.match(r'AO-(\d+)', r[0]); return int(m.group(1)) if m else 999
rows.sort(key=keyfn)

FAM_ORDER = ['Photo & Image','Vector & Print','Layout & Data','Motion & Audio']
byfam = {k: [] for k in FAM_ORDER}
for aid, d in rows: byfam[fam(d)].append((aid, d))

out = []
out.append("# APPENDIX A — All 100 Tasks (runnable now)\n")
out.append(f"Generated from the live spec corpus. {len(rows)} tasks. Each block is one complete, runnable brief: "
           "the client ask, the exact input assets you must upload, the required deliverables, the scoring verifiers, "
           "and the tool chain a solver is expected to use.\n")
out.append("> **To run a task:** upload every file listed under **Input assets** (from the local path shown, or the "
           "GCS mirror) into the ChatGPT session with the Adobe connector enabled, then paste the **Client brief**. "
           "Do not paste the hardness/verifier notes to the solver — those are the grader's reference.\n")

for famname in FAM_ORDER:
    items = byfam[famname]
    out.append(f"\n---\n\n## {famname} ({len(items)} tasks)\n")
    for aid, d in items:
        assets, arel = list_assets(aid)
        ins = d.get('inputs') or []
        # asset intent from spec inputs (name + what it is)
        in_lines = []
        for a in ins:
            if isinstance(a, dict):
                nm = a.get('name','?'); kind = a.get('kind','')
                gp = (a.get('gen_prompt') or '').strip().replace('\n',' ')
                intent = gp[:160] + ('…' if len(gp) > 160 else '')
                in_lines.append(f"    - `{nm}` ({kind}) — {intent}" if intent else f"    - `{nm}` ({kind})")
            else:
                in_lines.append(f"    - `{a}`")
        outs = d.get('outputs') or []
        out_lines = []
        for o in outs:
            if isinstance(o, dict):
                nm = o.get('name','?'); spec = (o.get('spec') or '').strip().replace('\n',' ')
                out_lines.append(f"    - **{nm}** — {spec[:220]}{'…' if len(spec)>220 else ''}")
            else:
                out_lines.append(f"    - {o}")
        tools = sorted(set(d.get('tools_used') or []) - {
            'asset_initialize_file_upload','asset_finalize_file_upload','asset_add_file',
            'asset_preview_file','asset_inline_preview','asset_get_presigned_urls'})
        vlist = verifiers.get(aid) or []
        vtxt = []
        if isinstance(vlist, dict): vlist = vlist.get('verifiers') or []
        for v in (vlist or [])[:12]:
            if isinstance(v, dict):
                t = v.get('text') or v.get('check') or v.get('desc') or json.dumps(v)[:120]
                vtxt.append(f"    - {t}")
        brief = (d.get('full_brief') or d.get('one_line_ask') or '').strip()

        out.append(f"\n### {aid} — {d.get('title','').strip()}")
        out.append(f"- **Family:** {famname}  |  **Vertical:** {d.get('vertical','?')}  |  **Category:** {d.get('category','?')}")
        out.append(f"- **One-line ask:** {(d.get('one_line_ask') or '').strip()}")
        out.append(f"- **Input assets** (upload these — local dir `{arel or 'MISSING'}`, {len(assets)} files):")
        if assets:
            out.append("    ```")
            for a in assets: out.append(f"    {a}")
            out.append("    ```")
        if in_lines:
            out.append("  - Asset intent (what each supplied file is):")
            out.extend(in_lines)
        out.append("- **Required deliverables:**")
        out.extend(out_lines or ["    - (see brief)"])
        if tools:
            out.append(f"- **Expected connector tools:** {', '.join(tools)}")
        if vtxt:
            out.append("- **Scoring verifiers (grader reference — do NOT show the solver):**")
            out.extend(vtxt)
        hr = (d.get('hardness_rationale') or d.get('difficulty_rationale') or '').strip()
        if hr:
            out.append(f"- **Why it's hard (grader reference):** {hr[:400]}{'…' if len(hr)>400 else ''}")
        out.append(f"\n<details><summary>Full client brief — paste THIS to the solver</summary>\n\n{brief}\n\n</details>\n")

# Appendix B: the redesign ledger (final reconciled v2 if present)
led_path = f"{AO}/PORTFOLIO_LEDGER_v2.json" if os.path.exists(f"{AO}/PORTFOLIO_LEDGER_v2.json") else f"{AO}/PORTFOLIO_LEDGER.json"
if os.path.exists(led_path):
    led = json.load(open(led_path))
    out.append("\n---\n\n# APPENDIX B — Redesign ledger (reconciled, concept-only)\n")
    out.append(f"The {len(led)} composite engagements the corpus is being reworked into (full commissions; small ops become "
               "stages). Distribution: Photo 30 / Vector 15 / Layout 35 / Motion 20; all 5 Photo signature ops represented. "
               "These are CONCEPTS — full specs + fresh assets are not built yet, so run tasks from Appendix A for now; this "
               "shows the direction. (Five minor residuals tracked in complex_benchmark/adobe_only/STAGE_C_RESIDUALS.md.)\n")
    lf = {}
    for r in led: lf.setdefault(r.get('family','?'), []).append(r)
    for famname in FAM_ORDER:
        items = lf.get(famname, [])
        out.append(f"\n## {famname} ({len(items)})\n")
        for r in items:
            out.append(f"- **{r.get('new_id')} — {r.get('engagement_title')}**  ")
            out.append(f"  _{r.get('one_line_ask','')[:200]}_  ")
            out.append(f"  Collateral: {', '.join((r.get('collateral_set') or [])[:6])}  ")
            out.append(f"  Absorbs: {', '.join((r.get('absorbs') or []))[:200]}  ")
            out.append(f"  Engine: {r.get('engine')}  |  Why-not-VLM: {r.get('why_not_vlm','')[:140]}")

txt = "\n".join(out)
open(f"{ROOT}/_handoff_appendix.md", "w").write(txt)
print("wrote _handoff_appendix.md", len(txt.encode())//1024, "KB")
print("family counts:", {k: len(v) for k, v in byfam.items()})
print("tasks with assets found:", sum(1 for aid,_ in rows if asset_dirs.get(aid)))
print("tasks with verifiers:", sum(1 for aid,_ in rows if verifiers.get(aid)))
