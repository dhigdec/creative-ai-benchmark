#!/usr/bin/env python3
"""Apply the 2026-09-25 review-feedback patches to the Gatsby V5 corpus.

One patch per task (patches/<TASK>.json). A patch carries:
  sentence_edits        exact-substring rewrites of brief and requirement sentences. Optional per edit:
                        "expert_review": true also rewrites that sentence inside expert_review_criteria, where
                        the corpus copies group requirements (opt-in; unflagged edits never touch that field)
  brief_insertions      new text placed after an exact anchor in the brief
  deliverable_bindings  source_image / source_record per output (corpus convention)
  palette               role and usage per existing palette hex
  palette_rules         distribution, opacity, forbidden, photography
  checks_modify         human checks rewritten under their EXISTING ids
  checks_add            new human checks, given the next free H number per output
  checks_retire         optional: removes an EARLIER copy of a duplicated human id, by position (occurrence,
                        1-based) and exact current text. A few MOTION tasks carry two checks under one id; an
                        id-keyed lookup can only ever reach the last copy, so a stale first copy is otherwise
                        unreachable. Unique ids, automatic checks and the last copy can never be retired.

Why it is shaped like this:
  * The same fact is repeated in ~15 files per task (page data, task bank, TASK_SPEC, register,
    verifier JSON and MD, brand JSON and MD, brief MD, five CSVs). Updating some and not others is
    how the corpus drifted in the first place, so every write goes to every copy.
  * Automatic checks are never touched. PHOTO-04 and PHOTO-13 carry graded runs whose recorded
    answers are keyed to those check ids and assertions.
  * Human checks keep their ids when rewritten, so nothing that references them breaks.
  * A task is applied all or nothing: one failed guard rejects that whole task.
  * Each task's VERIFIERS.json is the base: it is the only copy that is current for all 100
    (the master ATOMIC file is stale for the two run tasks), and it is written back to every copy.

Dry run by default. --go writes. Apply to a clean tree at HEAD, all patches in one run.
"""
import argparse, csv, glob, io, json, os, re, sys

G5 = os.environ.get("G5_DIR", "/Users/dhiren/Documents/ChatGPT/Adobe_Gpt/publish/creative-ai-benchmark/docs/gatsby-v5")
V3 = "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/input_assets_v3"
HERE = os.path.dirname(os.path.abspath(__file__))
PATCHES = os.path.join(HERE, "patches")
REV = "2026-09-25 review feedback"

KLABEL = {"K1_Q1": "Content completeness", "K1_Q2": "Specification accuracy", "K1_Q3": "Constraint compliance",
          "K1_Q4": "Deliverable completeness", "K1_Q5": "Critical failure check", "K2_Q1": "Asset selection",
          "K2_Q2": "Asset preservation", "K2_Q3": "Brand-system compliance", "K2_Q4": "Identity fidelity",
          "K5_Q1": "Primary-message recovery", "K5_Q2": "Information hierarchy"}
DASH = re.compile("[\u2013\u2014]")
MAX_WORDS = 40


# ------------------------------------------------------------------ io helpers
def jload(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)

def indent_of(path, default=1):
    try:
        for line in open(path, encoding="utf-8"):
            m = re.match(r"^( +)\S", line)
            if m:
                return len(m.group(1))
    except FileNotFoundError:
        pass
    return default

def jsave(p, data, trailing_nl=None):
    ind = indent_of(p)
    had_nl = trailing_nl
    if had_nl is None:
        try:
            had_nl = open(p, encoding="utf-8").read().endswith("\n")
        except FileNotFoundError:
            had_nl = False
    txt = json.dumps(data, indent=ind, ensure_ascii=False)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(txt + ("\n" if had_nl else ""))

def read_blob():
    h = open(os.path.join(G5, "index.html"), encoding="utf-8").read()
    m = re.search(r'<script type="application/json" id="data">', h)
    s = m.end(); e = h.find("</script>", s)
    return h, s, e, json.loads(h[s:e])

def write_blob(h, s, e, blob):
    payload = json.dumps(blob, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    open(os.path.join(G5, "index.html"), "w", encoding="utf-8").write(h[:s] + payload + h[e:])

def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


# ------------------------------------------------------------------ text edits
def edit(text, edits, counts):
    if not isinstance(text, str):
        return text
    for i, ed in enumerate(edits):
        n = text.count(ed["find"])
        if n:
            text = text.replace(ed["find"], ed["replace"]); counts[i] += n
    return text

def edit_list(lst, edits, counts):
    if isinstance(lst, str):          # MOTION tasks: required_content is a single string
        return edit(lst, edits, counts)
    return [edit(x, edits, counts) for x in lst] if isinstance(lst, list) else lst

def insert_brief(text, ins):
    if not isinstance(text, str):
        return text
    for it in ins:
        if text.count(it["after"]) == 1:
            text = text.replace(it["after"], it["after"] + it["insert"], 1)
    return text


# ------------------------------------------------------------------ validation
def validate(p, spec, checks):
    errs = []
    tid = p["task_id"]
    outs = {d["output_id"]: d for d in spec["deliverables"]}
    assets = {a["filename"] for a in spec.get("assets", [])}
    byid = {c["check_id"]: c for c in checks}
    new_text = []

    # sentence edits must hit at least one brief/requirement field
    fields = [spec.get("client_brief") or ""]
    for g in spec.get("deliverable_groups", []):
        fields += g.get("requirements") or []
    for d in spec["deliverables"]:
        # MOTION tasks carry required_content as one string, not a list; accept both shapes
        for fld in ("required_content", "acceptance_requirements"):
            v = d.get(fld) or []
            fields += [v] if isinstance(v, str) else list(v)
    for ed in p.get("sentence_edits", []):
        f, r = ed.get("find") or "", ed.get("replace") or ""
        if not f or not r or f == r:
            errs.append(f"sentence edit malformed: {f[:50]!r}"); continue
        if not any(f in x for x in fields if isinstance(x, str)):
            errs.append(f"sentence edit find not present: {f[:70]!r}")
        if ed.get("expert_review") and not any(f in x for d in spec["deliverables"]
                                               for x in (d.get("expert_review_criteria") or []) if isinstance(x, str)):
            errs.append(f"sentence edit flagged expert_review but in no expert_review_criteria: {f[:60]!r}")
        new_text.append(r)
    for it in p.get("brief_insertions", []):
        if (spec.get("client_brief") or "").count(it.get("after", "")) != 1:
            errs.append(f"brief insertion anchor not unique/present: {it.get('after','')[:60]!r}")
        new_text.append(it.get("insert", ""))
    for b in p.get("deliverable_bindings", []):
        if b.get("output_id") not in outs:
            errs.append(f"binding: unknown output {b.get('output_id')}"); continue
        si = b.get("source_image")
        for fn in ([si] if isinstance(si, str) else (si or [])):
            if fn not in assets:
                errs.append(f"binding: source_image not an asset: {fn}")
        sr = b.get("source_record")
        if sr and sr.get("table") not in assets:
            errs.append(f"binding: source_record table not an asset: {sr.get('table')}")
        # The executor reads the output register. A bound row whose approved values differ from its raw values
        # prints the very corrections the task is testing (an owner's corrected figure, a mapped label).
        if sr and (sr.get("values") or {}) != (sr.get("raw_values") or {}):
            diff = sorted(k for k in set(sr.get("values") or {}) | set(sr.get("raw_values") or {})
                          if (sr.get("values") or {}).get(k) != (sr.get("raw_values") or {}).get(k))
            errs.append(f"binding {b.get('output_id')}: source_record exposes corrected field(s) {diff} to the executor "
                        f"via the register; drop source_record (GUIDE rule 2)")
    hexes = {c["hex"].upper() for c in spec["brand_identity"].get("palette", [])}
    for pc in p.get("palette", []):
        if pc.get("hex", "").upper() not in hexes:
            errs.append(f"palette: hex not in brand palette: {pc.get('hex')}")
        new_text += [pc.get("role", ""), pc.get("usage", "")]
    new_text += [v for v in (p.get("palette_rules") or {}).values() if isinstance(v, str)]

    def check_ok(c, where):
        t = (c.get("check") or "").strip()
        if not t:
            errs.append(f"{where}: empty check text")
        if len(t.split()) > MAX_WORDS:
            errs.append(f"{where}: {len(t.split())} words (max {MAX_WORDS})")
        if c.get("k_id") not in KLABEL:
            errs.append(f"{where}: bad k_id {c.get('k_id')}")
        for fn in c.get("reference_assets") or []:
            if fn not in assets:
                errs.append(f"{where}: reference asset not in task: {fn}")
        new_text.extend([t, c.get("evidence") or ""])

    retire_seen = set()
    for r in p.get("checks_retire", []):
        rid, occ = r.get("check_id"), r.get("occurrence")
        copies = [c for c in checks if c["check_id"] == rid]
        if len(copies) < 2:
            errs.append(f"retire: {rid} is not a duplicated id; only an earlier copy of a duplicated id may be retired"); continue
        if not isinstance(occ, int) or isinstance(occ, bool) or not 1 <= occ < len(copies):
            errs.append(f"retire: {rid} occurrence must be 1..{len(copies) - 1} (an earlier copy; checks_modify reaches the last)"); continue
        if (rid, occ) in retire_seen:
            errs.append(f"retire: {rid} occurrence {occ} listed twice"); continue
        retire_seen.add((rid, occ))
        tgt = copies[occ - 1]
        if tgt.get("type") != "human":
            errs.append(f"retire: refuses automatic check {rid}"); continue
        if (r.get("check") or "").strip() != (tgt.get("check") or "").strip():
            errs.append(f"retire: {rid} occurrence {occ} text does not match the current copy: {(tgt.get('check') or '')[:60]!r}")
        if not (r.get("why") or "").strip():
            errs.append(f"retire: {rid} needs a why")
        new_text.append(r.get("why") or "")

    for c in p.get("checks_modify", []):
        cur = byid.get(c.get("check_id"))
        if not cur:
            errs.append(f"modify: unknown check {c.get('check_id')}"); continue
        if cur.get("type") == "auto":
            errs.append(f"modify: refuses automatic check {c['check_id']}"); continue
        check_ok(c, c["check_id"])
    seen = {(c["output_id"], re.sub(r"\W+", " ", (c.get("check") or "").lower()).strip()) for c in checks}
    for i, c in enumerate(p.get("checks_add", [])):
        if c.get("output_id") not in outs:
            errs.append(f"add[{i}]: unknown output {c.get('output_id')}"); continue
        check_ok(c, f"add[{i}] {c['output_id']}")
        key = (c["output_id"], re.sub(r"\W+", " ", (c.get("check") or "").lower()).strip())
        if key in seen:
            errs.append(f"add[{i}]: duplicates an existing check on {c['output_id']}")
        seen.add(key)
    for s in new_text:
        if isinstance(s, str) and DASH.search(s):
            errs.append(f"en/em dash in new text: {s[:70]!r}")

    # Evidence written as  file.txt: "quoted words"  must quote the file verbatim. A reviewer caught paraphrases
    # dressed as quotes; graders read these as the source's exact words.
    adir = os.path.join(V3, tid, "assets")
    norm = lambda x: re.sub(r"\s+", " ", x.replace("’", "'").replace("‘", "'")
                            .replace("“", '"').replace("”", '"')).strip().lower()
    cache = {}
    for c in list(p.get("checks_modify", [])) + list(p.get("checks_add", [])):
        for fn, q in re.findall(r'([\w.\-]+\.(?:txt|csv|md|tsv|json)):\s*"([^"]{8,})"', c.get("evidence") or ""):
            fp = os.path.join(adir, fn)
            if not os.path.exists(fp):
                continue
            if fn not in cache:
                cache[fn] = norm(open(fp, encoding="utf-8", errors="replace").read())
            if norm(q).rstrip(".") not in cache[fn]:
                errs.append(f"{c.get('check_id') or c.get('output_id')}: quote not verbatim in {fn}: {q[:60]!r}")
    return errs


# ------------------------------------------------------------------ check building
def retired_set(p):
    """(check_id, occurrence) pairs a patch retires. Occurrence counts copies of that id in file order, from 1."""
    return {(r["check_id"], int(r["occurrence"])) for r in p.get("checks_retire", [])}

def rewrite_atomic(atom_old, current, retired):
    """Rebuild the master verifier list without reordering it.

    Every old entry is replaced by the current copy at the SAME POSITION among the entries that share its id (an
    id-keyed map collapsed both copies of a duplicated id onto the last one, which duplicated the last copy and lost
    the first). An entry whose copy a patch retired is dropped. New checks go after their output's last old entry.
    current: {task_id: current VERIFIERS list}; retired: {task_id: {(check_id, occurrence)}} against the OLD list.
    """
    copies = {}
    for L in current.values():
        for x in L:
            copies.setdefault(x["check_id"], []).append(x)
    old_ids = {x["check_id"] for x in atom_old}
    fresh = {}
    for tid, L in current.items():
        for x in L:
            if x["check_id"] not in old_ids:
                fresh.setdefault((tid, x["output_id"]), []).append(x)
    last_pos = {}
    for i, x in enumerate(atom_old):
        last_pos[(x["task_id"], x["output_id"])] = i
    atom, seen = [], {}
    for i, x in enumerate(atom_old):
        cid = x["check_id"]
        k = seen[cid] = seen.get(cid, 0) + 1
        gone = retired.get(x["task_id"], set())
        if (cid, k) not in gone:
            j = k - sum(1 for (rid, rk) in gone if rid == cid and rk < k)
            cur = copies.get(cid, [])
            atom.append(cur[j - 1] if j <= len(cur) else x)
        key = (x["task_id"], x["output_id"])
        if last_pos.get(key) == i:
            atom += fresh.pop(key, [])
    for rest in fresh.values():
        atom += rest
    return atom

def retire_guard(ctx, patches, atom_old):
    """A retirement is positional, so the master file's copy at that position must be the same check the task file
    holds there. Refuse the task otherwise, before anything is written."""
    errs = {}
    for tid in ctx:
        for r in patches[tid].get("checks_retire", []):
            old = [x for x in atom_old if x["check_id"] == r["check_id"]]
            k = int(r["occurrence"])
            if len(old) < k or (old[k - 1].get("check") or "").strip() != (r.get("check") or "").strip():
                errs.setdefault(tid, []).append(f"retire: ATOMIC_VERIFIERS_ALL100 copy {k} of {r['check_id']} is not the check being retired")
    return errs

def build_checks(p, spec, checks):
    outs = {d["output_id"]: d for d in spec["deliverables"]}
    urls = {a["filename"]: a.get("public_url") for a in spec.get("assets", [])}
    refs = lambda names: [{"filename": n, "url": urls.get(n)} for n in (names or [])]
    gone = retired_set(p)
    kept, occ = [], {}
    for c in checks:
        occ[c["check_id"]] = occ.get(c["check_id"], 0) + 1
        if (c["check_id"], occ[c["check_id"]]) not in gone:
            kept.append(c)
    checks = [dict(c) for c in kept]
    byid = {c["check_id"]: c for c in checks}

    for m in p.get("checks_modify", []):
        c = byid[m["check_id"]]
        o = outs.get(c["output_id"], {})
        t = m["check"].strip()
        c.update({"check": t, "requirement": t, "pass_condition": t, "source_statement": t,
                  "evidence_reference": (m.get("evidence") or c.get("evidence_reference") or "").strip(),
                  "reference_assets": refs(m.get("reference_assets")),
                  "k_id": m["k_id"], "k_label": KLABEL[m["k_id"]],
                  "artifact_name": o.get("name", c.get("artifact_name")), "revision": REV})

    nxt = {}
    for c in checks:
        mm = re.search(r"/H(\d+)$", c["check_id"])
        if mm:
            nxt[c["output_id"]] = max(nxt.get(c["output_id"], 0), int(mm.group(1)))
    added = {}
    for a in p.get("checks_add", []):
        oid = a["output_id"]; o = outs[oid]
        nxt[oid] = nxt.get(oid, 0) + 1
        cid = f"{p['task_id']}/{oid}/H{nxt[oid]:03d}"
        t = a["check"].strip()
        ref = next((c.get("output_reference") for c in checks if c["output_id"] == oid and c.get("output_reference")), o.get("path"))
        added.setdefault(oid, []).append({
            "task_id": p["task_id"], "output_id": oid, "check_id": cid, "type": "human",
            "output_reference": ref, "check": t, "answer_type": "yes_no", "allowed_answers": ["Yes", "No"],
            "pass_answer": "Yes", "answer": None, "status": "not_assessed", "source_statement": t,
            "evidence_reference": (a.get("evidence") or "").strip(), "artifact_name": o.get("name"),
            "artifact_file": (o.get("path") or "").split("/")[-1], "requirement": t, "pass_condition": t,
            "reference_assets": refs(a.get("reference_assets")), "k_id": a["k_id"], "k_label": KLABEL[a["k_id"]],
            "origin": "review_feedback_2026_09_25", "revision": REV})

    # place new checks right after the last existing check of the same output
    out = []
    last = {c["output_id"]: i for i, c in enumerate(checks)}
    for i, c in enumerate(checks):
        out.append(c)
        if last.get(c["output_id"]) == i:
            out += added.pop(c["output_id"], [])
    for rest in added.values():
        out += rest
    return out


# ------------------------------------------------------------------ client policy B (2026-09-27)
def renumber_collisions(checks):
    """Some MOTION outputs carry two different, valid checks under one id (the short-form reframe reused H001).
    Stale copies are retired by the patch; any collision left is two real checks, so the earlier copy gets the next
    free H number on its output. Nothing is dropped."""
    top = {}
    for c in checks:
        m = re.search(r"/H(\d+)$", c["check_id"])
        if m:
            top[c["output_id"]] = max(top.get(c["output_id"], 0), int(m.group(1)))
    seen = {}
    for c in checks:
        seen[c["check_id"]] = seen.get(c["check_id"], 0) + 1
    count = {}
    for c in checks:
        cid = c["check_id"]; count[cid] = count.get(cid, 0) + 1
        if seen[cid] > 1 and count[cid] < seen[cid] and c.get("type") == "human":
            top[c["output_id"]] += 1
            c["check_id"] = f"{c['task_id']}/{c['output_id']}/H{top[c['output_id']]:03d}"
            c["renumbered_from"] = cid
    return checks


def policy_b(p, spec, checks):
    """Client decision: in a templated run (a group of more than 6 outputs), type and palette rule checks (K2_Q3)
    go only on the first output, the last output, and every output carrying a critical-trap check (K1_Q5).
    Distinct designs (groups of 6 or fewer) keep every rule. Content checks are never sampled.
    Returns (patch copy with the sampled checks_add, number dropped)."""
    groups = {}
    for d in spec["deliverables"]:
        groups.setdefault(d["group_id"], []).append(d["output_id"])
    trap = {c["output_id"] for c in checks if c.get("k_id") == "K1_Q5"} | \
           {c["output_id"] for c in p.get("checks_add", []) if c.get("k_id") == "K1_Q5"} | \
           {c["check_id"].split("/")[1] for c in p.get("checks_modify", []) if c.get("k_id") == "K1_Q5"}
    keep = set()
    for outs in groups.values():
        keep |= set(outs) if len(outs) <= 6 else ({outs[0], outs[-1]} | (set(outs) & trap))
    q = dict(p)
    q["checks_add"] = [c for c in p.get("checks_add", []) if c.get("k_id") != "K2_Q3" or c["output_id"] in keep]
    return q, len(p.get("checks_add", [])) - len(q["checks_add"])


LEAK_POLICY = ("Values are shown exactly as supplied. Where a supplied source corrects a value, the verifiers state the "
               "scoring target; the corrected value is not repeated here.")

def strip_leaks(entries, filt=None):
    """Client decision: an executor-facing record must not print a corrected value next to its raw value. Keep the
    binding (row, raw values, table) and drop only the correction. Returns how many entries changed."""
    n = 0
    for d in entries or []:
        if filt and not filt(d):
            continue
        sr = d.get("source_record")
        if isinstance(sr, dict) and (sr.get("values") or {}) != (sr.get("raw_values") or {}) and sr.get("raw_values"):
            sr["values"] = dict(sr["raw_values"])
            d["record_field_policy"] = LEAK_POLICY
            n += 1
    return n

def sync_register_specs(reg, spec):
    """Per-task OUTPUT_REGISTER.json drifted from TASK_SPEC in all 20 MOTION tasks (the short-form reframe updated
    every other copy). The executor reads the register, so its spec must be TASK_SPEC's."""
    want = {d["output_id"]: d.get("spec") for d in spec["deliverables"]}
    n = 0
    for d in reg or []:
        w = want.get(d.get("output_id"))
        if w is not None and json.dumps(d.get("spec"), sort_keys=True) != json.dumps(w, sort_keys=True):
            d["spec"] = w; n += 1
    return n

def deliverables_md(spec):
    rows = ["| Output | File | Specification |", "|---|---|---|"]
    for d in spec["deliverables"]:
        rows.append(f"| {d.get('name','')} | {d.get('path','')} | {json.dumps(d.get('spec'), ensure_ascii=False, separators=(',', ':'))} |")
    return f"# {spec['task_name']}: output register\n\n" + "\n".join(rows) + "\n"


# ------------------------------------------------------------------ brand helpers
def apply_palette(bi, p):
    if not isinstance(bi, dict):
        return
    by = {x["hex"].upper(): x for x in p.get("palette", [])}
    for c in bi.get("palette") or []:
        x = by.get(c.get("hex", "").upper())
        if x:
            c["role"] = x["role"]; c["usage"] = x["usage"]
    if p.get("palette_rules"):
        bi["palette_rules"] = p["palette_rules"]

def palette_md(bi):
    lines = []
    for c in bi.get("palette") or []:
        line = f"- {c['name']}: {c['hex']}"
        if c.get("role"):
            line += f" · {c['role']}"
        if c.get("usage"):
            line += f". {c['usage']}"
        lines.append(line)
    pr = bi.get("palette_rules") or {}
    if pr:
        lines += ["", "### Palette rules"]
        for k in ("distribution", "opacity", "forbidden", "photography"):
            if pr.get(k):
                lines.append(f"- {k.capitalize()}: {pr[k]}")
    return "\n".join(lines)

def typography_md(bi):
    ts = bi.get("type_system") or {}
    if not ts.get("scale"):
        return bi.get("typography") or ""
    lines = [f"Display face: {ts.get('display_face','')}. Text face: {ts.get('text_face','')}.", ""]
    for r in ts["scale"]:
        lines.append(f"- {r.get('step','')} {r.get('role','')}: {r.get('family','')}, {r.get('size','')} / "
                     f"{r.get('leading','')}, {r.get('weight','')}, tracking {r.get('tracking','')}.")
    if ts.get("signature_move"):
        lines += ["", f"Signature move: {ts['signature_move']}"]
    if ts.get("rules"):
        lines += ["", "Rules:"] + [f"- {x}" for x in ts["rules"]]
    return "\n".join(lines)

def replace_md_section(md, heading, body):
    pat = re.compile(rf"(^## {re.escape(heading)}\n)(.*?)(?=^## |\Z)", re.S | re.M)
    if pat.search(md):
        return pat.sub(lambda m: m.group(1) + body.rstrip() + "\n\n", md, count=1)
    return md


# ------------------------------------------------------------------ verifier markdown
def verifiers_md(task_name, task_id, checks, run_format):
    if run_format:   # identical to tools/publish_completed_runs.markdown_verifier_summary
        auto = [c for c in checks if c.get("type") == "auto"]
        human = [c for c in checks if c.get("type") == "human"]
        passed = sum(c.get("status") == "passed" for c in auto)
        rows = [f"| {c['check_id']} | {c.get('answer') or 'Pending'} | {c.get('status')} | {c.get('evidence_reference', '')} |" for c in auto]
        return (f"# {task_name}: verifier results\n\n"
                f"Automatic verification: **{passed}/{len(auto)} passed**. Human verification: **{len(human)} checks pending independent review**.\n\n"
                f"[Run result JSON](RUN_RESULT.json) · [Trajectory JSON](../../runs/{task_id}/trajectory/trajectory.json) · [Trajectory report](../../runs/{task_id}/trajectory/trajectory.html)\n\n"
                "| Check | Answer | Status | Measured evidence |\n|---|---|---|---|\n" + "\n".join(rows) + "\n")
    cell = lambda x: str(x or "").replace("|", "\\|").replace("\n", " ")
    rows = ["| Output | Check ID | Type | K question | Pass condition | Evidence | Answer |", "|---|---|---|---|---|---|---|"]
    for c in checks:
        kq = f"{c.get('k_id','')} {c.get('k_label','')}".strip() if c["type"] == "human" else ""
        rows.append(f"| {cell(c.get('output_reference'))} | {c['check_id']} | {c['type']} | {cell(kq)} | "
                    f"{cell(c.get('requirement') or c.get('check'))} | {cell(c.get('evidence_reference'))} | Yes / No |")
    return f"# {task_name}: verifiers\n\n" + "\n".join(rows) + "\n"


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--go", action="store_true")
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()

    patches = {}
    for f in sorted(glob.glob(os.path.join(PATCHES, "*.json"))):
        p = jload(f)
        if not a.only or p["task_id"] in a.only:
            patches[p["task_id"]] = p
    print(f"patches loaded: {len(patches)}")

    ctx, rejected = {}, {}
    for tid, p in patches.items():
        tdir = os.path.join(G5, "tasks", tid)
        spec = jload(os.path.join(tdir, "TASK_SPEC.json"))
        checks = jload(os.path.join(tdir, "VERIFIERS.json"))
        errs = validate(p, spec, checks)
        if errs:
            rejected[tid] = errs
        else:
            ctx[tid] = {"spec": spec, "checks": checks, "tdir": tdir}
    if any(patches[t].get("checks_retire") for t in ctx):
        for tid, errs in retire_guard(ctx, patches, jload(os.path.join(G5, "ATOMIC_VERIFIERS_ALL100.json"))).items():
            rejected[tid] = errs
            ctx.pop(tid, None)
    print(f"accepted: {len(ctx)}   rejected: {len(rejected)}")
    for tid, errs in rejected.items():
        print(f"  REJECT {tid}:")
        for e in errs[:8]:
            print(f"     - {e}")

    summary, sampled_out = {}, {}
    for tid in list(ctx):
        spec = ctx[tid]["spec"]
        p, dropped = policy_b(patches[tid], spec, ctx[tid]["checks"])
        patches[tid] = p; sampled_out[tid] = dropped
        new = build_checks(p, spec, ctx[tid]["checks"])
        new = renumber_collisions(new)
        ids = [c["check_id"] for c in new]
        dup = sorted({i for i in ids if ids.count(i) > 1})
        if dup:   # a duplicated id must be retired (checks_retire) or rewritten; never shipped
            rejected[tid] = [f"duplicate check id after patch: {d}" for d in dup]
            ctx.pop(tid); continue
        ctx[tid]["new_checks"] = new
        summary[tid] = {"human_before": sum(c["type"] == "human" for c in ctx[tid]["checks"]),
                        "human_after": sum(c["type"] == "human" for c in new),
                        "modified": len(p.get("checks_modify", [])), "added": len(p.get("checks_add", [])),
                        "sentence_edits": len(p.get("sentence_edits", [])),
                        "bindings": len(p.get("deliverable_bindings", [])), "policy_b_sampled_out": dropped}
    if rejected and any("duplicate check id" in e for v in rejected.values() for e in v):
        print(f"accepted after duplicate guard: {len(ctx)}   rejected: {len(rejected)}")
        for tid, errs in rejected.items():
            if any("duplicate" in e for e in errs):
                print(f"  REJECT {tid}: " + "; ".join(errs[:4]))
    print(f"policy B: {sum(sampled_out.values())} rule checks sampled out of templated runs")
    if not a.go:
        print("\nDRY RUN. nothing written. re-run with --go.")
        for tid, s in list(summary.items())[:12]:
            print(f"  {tid}: human {s['human_before']} -> {s['human_after']} (+{s['added']}, ~{s['modified']}), "
                  f"{s['sentence_edits']} sentence edits, {s['bindings']} bindings")
        for tid, errs in rejected.items():          # full list, so an agent can fix every guard in one pass
            if len(errs) > 8:
                print(f"  (all {len(errs)} for {tid})"); [print(f"     - {x}") for x in errs[8:]]
        if not a.only:   # parallel agents validate with --only; a shared report file would collide
            json.dump({"rejected": rejected, "summary": summary}, open(os.path.join(HERE, "apply_dryrun.json"), "w"), indent=1)
        return

    # ---------------- write everything
    h, s, e, blob = read_blob()
    bmap = {t["id"]: t for t in blob["tasks"]}
    bank = jload(os.path.join(G5, "TASKS_V5_ALL100.json"))
    bl = bank if isinstance(bank, list) else bank["tasks"]
    kmap = {t["new_id"]: t for t in bl}
    reg_all = jload(os.path.join(G5, "OUTPUT_REGISTER_ALL100.json"))
    edit_counts, leaks, synced, regen_md = {}, {}, {}, {}

    def apply_outputs(entries, tid, p, counts, key="output_id", filt=None):
        binds = {b["output_id"]: b for b in p.get("deliverable_bindings", [])}
        for d in entries:
            if filt and not filt(d):
                continue
            for fld in ("required_content", "acceptance_requirements"):
                if fld in d:
                    d[fld] = edit_list(d[fld], p.get("sentence_edits", []), counts)
            # opt-in: an edit flagged "expert_review": true also rewrites its sentence where a group requirement was
            # copied into expert_review_criteria (MOTION-05's stale narration line). Unflagged edits never touch it.
            er = [ed for ed in p.get("sentence_edits", []) if ed.get("expert_review")]
            if er and "expert_review_criteria" in d:
                d["expert_review_criteria"] = edit_list(d["expert_review_criteria"], er, [0] * len(er))
            b = binds.get(d.get(key))
            if b:
                if "source_image" in b:
                    d["source_image"] = b["source_image"]
                if "source_record" in b:
                    d["source_record"] = b["source_record"]

    for tid, c in ctx.items():
        p = patches[tid]; eds = p.get("sentence_edits", []); ins = p.get("brief_insertions", [])
        counts = [0] * len(eds)
        new = c["new_checks"]; auto = [x for x in new if x["type"] == "auto"]; hum = [x for x in new if x["type"] != "auto"]

        # page blob
        t = bmap[tid]
        t["brief"] = insert_brief(edit(t["brief"], eds, counts), ins)
        for g in t.get("groups", []):
            g["requirements"] = edit_list(g.get("requirements"), eds, counts)
        apply_outputs(t.get("outputs", []), tid, p, counts)
        strip_leaks(t.get("outputs", []))
        apply_palette(t.get("brand"), p)
        t["checks"] = new

        # task bank and TASK_SPEC, same shape
        for doc, path in ((kmap.get(tid), None), (c["spec"], os.path.join(c["tdir"], "TASK_SPEC.json"))):
            if doc is None:
                continue
            doc["client_brief"] = insert_brief(edit(doc.get("client_brief"), eds, counts), ins)
            for g in doc.get("deliverable_groups", []):
                g["requirements"] = edit_list(g.get("requirements"), eds, counts)
            apply_outputs(doc.get("deliverables", []), tid, p, counts)
            leaks[tid] = leaks.get(tid, 0) + strip_leaks(doc.get("deliverables", []))
            apply_palette(doc.get("brand_identity"), p)
            doc["verifiers_auto"] = auto
            doc["verifiers_human"] = hum
            if path:
                jsave(path, doc)

        # per-task register, verifiers, brief md
        rp = os.path.join(c["tdir"], "OUTPUT_REGISTER.json")
        if os.path.exists(rp):
            reg = jload(rp); apply_outputs(reg if isinstance(reg, list) else [], tid, p, counts)
            synced[tid] = sync_register_specs(reg, c["spec"]); strip_leaks(reg); jsave(rp, reg)
        apply_outputs(reg_all, tid, p, counts, filt=lambda d, t=tid: d.get("task_id") == t)
        sync_register_specs([d for d in reg_all if d.get("task_id") == tid], c["spec"])
        strip_leaks(reg_all, filt=lambda d, t=tid: d.get("task_id") == t)
        if not os.path.exists(os.path.join(c["tdir"], "RUN_RESULT.json")):   # run tasks keep the run tool's format
            dp = os.path.join(c["tdir"], "DELIVERABLES.md"); want = deliverables_md(c["spec"])
            if not os.path.exists(dp) or open(dp, encoding="utf-8").read() != want:
                with open(dp, "w", encoding="utf-8") as fh:
                    fh.write(want)
                regen_md[tid] = 1
        jsave(os.path.join(c["tdir"], "VERIFIERS.json"), new)
        run_fmt = os.path.exists(os.path.join(c["tdir"], "RUN_RESULT.json"))
        open(os.path.join(c["tdir"], "VERIFIERS.md"), "w", encoding="utf-8").write(
            verifiers_md(c["spec"]["task_name"], tid, new, run_fmt))
        bp = os.path.join(c["tdir"], "BRIEF.md")
        if os.path.exists(bp):
            # read BEFORE opening for write: open(..., "w") truncates, and an earlier version of this
            # line evaluated the write-open first and so read, and wrote back, an empty file
            src_md = open(bp, encoding="utf-8").read()
            new_md = insert_brief(edit(src_md, eds, [0] * len(eds)), ins)
            if src_md.strip() and not new_md.strip():
                raise SystemExit(f"refusing to empty {bp}")
            with open(bp, "w", encoding="utf-8") as fh:
                fh.write(new_md)

        # brand identity files: sync palette roles/rules AND the current type system (both were stale)
        bi = c["spec"]["brand_identity"]
        bjp = os.path.join(c["tdir"], "BRAND_IDENTITY.json")
        if os.path.exists(bjp):
            bj = jload(bjp)
            bj["palette"] = bi.get("palette"); bj["typography"] = bi.get("typography")
            if bi.get("type_system"):
                bj["type_system"] = bi["type_system"]
            if bi.get("palette_rules"):
                bj["palette_rules"] = bi["palette_rules"]
            jsave(bjp, bj)
        bmp = os.path.join(c["tdir"], "BRAND_IDENTITY.md")
        if os.path.exists(bmp):
            md = open(bmp, encoding="utf-8").read()
            md = replace_md_section(md, "Palette", palette_md(bi))
            md = replace_md_section(md, "Typography", typography_md(bi))
            open(bmp, "w", encoding="utf-8").write(md)
        edit_counts[tid] = counts

    write_blob(h, s, e, blob)
    jsave(os.path.join(G5, "TASKS_V5_ALL100.json"), bank)
    jsave(os.path.join(G5, "OUTPUT_REGISTER_ALL100.json"), reg_all)

    # master verifier file. Earlier passes appended checks at the end, so it is NOT grouped by task;
    # regrouping it reorders ~16k entries and buries the real change. Keep every entry where it is:
    # replace updated checks in place (the task's VERIFIERS.json is the current copy, which also
    # re-syncs the run tasks' recorded answers), and insert new checks after their last sibling.
    atom_old = jload(os.path.join(G5, "ATOMIC_VERIFIERS_ALL100.json"))
    current = {}
    for tid in {x["task_id"] for x in atom_old}:
        vp = os.path.join(G5, "tasks", tid, "VERIFIERS.json")
        src = ctx[tid]["new_checks"] if tid in ctx else (jload(vp) if os.path.exists(vp) else None)
        if src:
            current[tid] = src
    atom = rewrite_atomic(atom_old, current, {tid: retired_set(patches[tid]) for tid in ctx})
    jsave(os.path.join(G5, "ATOMIC_VERIFIERS_ALL100.json"), atom)
    order, per = [], {}
    for x in atom:
        if x["task_id"] not in per:
            order.append(x["task_id"]); per[x["task_id"]] = []
        per[x["task_id"]].append(x)

    # CSVs
    fam = {t["new_id"]: t["family"] for t in bl}; code = {t["new_id"]: t["task_code"] for t in bl}
    name = {t["new_id"]: t["task_name"] for t in bl}; bycode = {v: k for k, v in code.items()}
    buf = io.StringIO(); w = csv.writer(buf, lineterminator="\n")
    w.writerow(["Task code", "Task name", "Family", "Verifier type", "Verifier ID", "Output ID", "Deliverable",
                "Output file", "Pass condition", "Evidence", "K question", "Answer (Yes/No)"])
    for tid in order:
        arr = per[tid]
        for x in [y for y in arr if y["type"] == "auto"] + [y for y in arr if y["type"] != "auto"]:
            kq = f"{x.get('k_id','')} {x.get('k_label','')}".strip() if x["type"] == "human" else ""
            w.writerow([code[tid], name[tid], fam[tid], "Auto" if x["type"] == "auto" else "Human", x["check_id"],
                        x["output_id"], x.get("artifact_name") or "", (x.get("output_reference") or "").split(",")[0].strip(),
                        x.get("pass_condition") or x.get("requirement") or "", x.get("evidence_reference") or "", kq,
                        x.get("answer") or ""])
    open(os.path.join(G5, "data/verifiers.csv"), "w", encoding="utf-8").write(buf.getvalue())

    counts_by = {tid: (sum(x["type"] == "auto" for x in per[tid]), sum(x["type"] != "auto" for x in per[tid])) for tid in order}
    for f in glob.glob(os.path.join(G5, "data/*-tasks.csv")) + [os.path.join(G5, "data/task-register.csv")]:
        rows = list(csv.DictReader(open(f, encoding="utf-8")))
        if not rows:
            continue
        cols = list(rows[0].keys())
        for r in rows:
            tid = bycode.get(r.get("Task code"))
            if not tid:
                continue
            if "Auto verifiers" in r:
                r["Auto verifiers"] = str(counts_by[tid][0])
            if "Human verifiers" in r:
                r["Human verifiers"] = str(counts_by[tid][1])
            if tid in ctx and "Client brief" in r:
                p = patches[tid]
                r["Client brief"] = insert_brief(edit(r["Client brief"], p.get("sentence_edits", []), [0] * 99), p.get("brief_insertions", []))
        b2 = io.StringIO(); dw = csv.DictWriter(b2, fieldnames=cols, lineterminator="\n")
        dw.writeheader(); dw.writerows(rows)
        open(f, "w", encoding="utf-8").write(b2.getvalue())

    bi_csv = os.path.join(G5, "data/brand-identity.csv")
    rows = list(csv.DictReader(open(bi_csv, encoding="utf-8")))
    cols = list(rows[0].keys())
    if "Palette rules" not in cols:
        cols.append("Palette rules")
    for r in rows:
        tid = bycode.get(r["Task code"])
        r.setdefault("Palette rules", "")
        if tid in ctx:
            bi = ctx[tid]["spec"]["brand_identity"]
            r["Palette"] = "\n".join(f"{x['name']} {x['hex']}" + (f" · {x['role']}" if x.get("role") else "") +
                                     (f". {x['usage']}" if x.get("usage") else "") for x in bi.get("palette") or [])
            pr = bi.get("palette_rules") or {}
            r["Palette rules"] = "\n".join(f"{k.capitalize()}: {pr[k]}" for k in ("distribution", "opacity", "forbidden", "photography") if pr.get(k))
    b3 = io.StringIO(); dw = csv.DictWriter(b3, fieldnames=cols, lineterminator="\n")
    dw.writeheader(); dw.writerows(rows)
    open(bi_csv, "w", encoding="utf-8").write(b3.getvalue())

    rsp = os.path.join(G5, "RELEASE_STATUS.json"); rs = jload(rsp)
    rs["atomic_verifiers"] = len(atom); rs["auto"] = sum(x["type"] == "auto" for x in atom)
    rs["human"] = len(atom) - rs["auto"]
    jsave(rsp, rs)

    rep = {"revision": REV, "applied": sorted(ctx), "rejected": rejected, "summary": summary,
           "sentence_edit_hits": edit_counts,
           "corpus": {"checks": len(atom), "auto": rs["auto"], "human": rs["human"]}}
    json.dump(rep, open(os.path.join(HERE, "apply_report.json"), "w"), indent=1, ensure_ascii=False)
    print(f"\nwritten. tasks applied {len(ctx)}; corpus checks {len(atom)} (auto {rs['auto']}, human {rs['human']})")
    for tid, cnt in edit_counts.items():
        print(f"  {tid}: sentence-edit hits per edit {cnt}")


if __name__ == "__main__":
    main()
