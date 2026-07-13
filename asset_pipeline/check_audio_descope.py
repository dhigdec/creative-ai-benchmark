#!/usr/bin/env python
"""Deterministic gate after the audio-descope reframe. For every spec, verify audio is fully gone and the
structural invariants still hold. Prints per-spec problems; exit 0 iff all clean.

Run:  .venv/bin/python check_audio_descope.py
"""
from __future__ import annotations
import glob, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config

AUDIO_KIND = {"audio"}
AUDIO_NAME = re.compile(r"\.(wav|mp3|m4a|aac|flac|ogg)\b|voice[-_ ]?over|voiceover|\bvo[_ ]|music[_ ]?bed|scratch[_ ]?vo|"
                        r"agent_narration|host_voice|founder_vo|lecture_audio|cleaned_commentary|hype_intro", re.I)
AUDIO_TOOLS = {"media_enhance_speech"}  # media_summarize allowed only if a remaining step uses it


def check(sp):
    s = json.load(open(sp)); tid = s["id"]; P = []
    ins = s.get("inputs") or []; outs = s.get("outputs") or []
    wf = s.get("connector_workflow") or []
    # 1) no audio inputs/outputs
    for i in ins:
        if (i.get("kind") or "").lower() in AUDIO_KIND or AUDIO_NAME.search(i.get("name", "")):
            P.append(f"audio INPUT remains: {i.get('name')} ({i.get('kind')})")
    for o in outs:
        if (o.get("kind") or "").lower() in AUDIO_KIND or AUDIO_NAME.search(o.get("name", "")):
            P.append(f"audio OUTPUT remains: {o.get('name')} ({o.get('kind')})")
    # 2) workflow: no audio tool, renumbered, tcc matches, inputs_from resolves
    tools_in_wf = []
    step_outputs = set()
    for idx, st in enumerate(wf):
        n = st.get("n"); tool = st.get("tool", ""); tools_in_wf.append(tool)
        if n != idx + 1:
            P.append(f"step {idx} has n={n} (not renumbered)")
        if tool in AUDIO_TOOLS:
            P.append(f"audio TOOL step remains: {tool} (n={n})")
        out = st.get("output")
        if out and AUDIO_NAME.search(str(out)):
            P.append(f"step n={n} outputs audio: {out}")
    if s.get("tool_call_count") != len(wf):
        P.append(f"tool_call_count {s.get('tool_call_count')} != workflow len {len(wf)}")
    # inputs_from resolution
    input_names = {i.get("name") for i in ins}
    produced = set()
    for st in wf:
        for ref in (st.get("inputs_from") or []):
            base = str(ref)
            if base in ("uploaded_assets", "upload_session"):
                continue
            ok = (base in input_names) or (base in produced) or any(base in str(p) for p in produced) \
                 or any(str(p) in base for p in produced)
            if not ok and AUDIO_NAME.search(base):
                P.append(f"step n={st.get('n')} inputs_from references removed AUDIO: {base}")
        o = st.get("output")
        if o:
            produced.add(o if isinstance(o, str) else json.dumps(o))
    # 3) tools_used == distinct workflow tools; distinct_adobe_tools count
    tools_used = s.get("tools_used") or []
    wf_set = set(tools_in_wf)
    tu_set = set(tools_used)
    # allow local_* helpers in tools_used that aren't "adobe" steps
    extra_in_wf = wf_set - tu_set
    if extra_in_wf:
        P.append(f"workflow uses tools not in tools_used: {sorted(extra_in_wf)}")
    stale = {t for t in (tu_set - wf_set) if not t.startswith("local_")}
    if stale:
        P.append(f"tools_used has tools not in workflow: {sorted(stale)}")
    da = len({t for t in tools_used if not t.startswith("local_")})
    if s.get("distinct_adobe_tools") != da:
        P.append(f"distinct_adobe_tools {s.get('distinct_adobe_tools')} != {da}")
    # 4) prose has no audio-as-task language
    # audio-WORK / deliverable language (not the bare "video/audio" capability tag, which describes ABSENCE)
    AUDIO_PROSE = re.compile(
        r"voice-?over|voiceover|\bVO track|\.wav|\.mp3|music bed|clean(ed)? (the )?(speech|voice|audio)|"
        r"\bdenoise|de-noise|ducking|loudness|LUFS|mix the audio|on-camera speech|scratch (vo|voice)|"
        r"narration balance|music-vs-narration", re.I)
    ABSENCE = re.compile(r"no (video/)?audio|video/audio (inspection|A-mode|media)|are NOT used|not used|no async", re.I)
    for f in ("one_line_ask", "full_brief", "chaining_note", "difficulty_rationale", "reverify"):
        v = s.get(f)
        txt = v if isinstance(v, str) else json.dumps(v or "")
        for m in AUDIO_PROSE.finditer(txt):
            ctx = txt[max(0, m.start() - 25): m.start() + 25]
            if not ABSENCE.search(ctx):
                P.append(f"prose field '{f}' still mentions audio: ...{ctx}...")
                break
    return tid, P


def main():
    specs = sorted(glob.glob(str(config.PROJECT_DIR / "complex_benchmark/adobe_only/specs/*.json")),
                   key=lambda p: int(Path(p).parent.name and Path(p).name.split("_")[0].split("-")[1]))
    total_problems = 0; bad = 0
    for sp in specs:
        try:
            tid, P = check(sp)
        except Exception as e:
            print(f"  {Path(sp).name}: JSON/parse ERROR: {e}"); total_problems += 1; bad += 1; continue
        if P:
            bad += 1; total_problems += len(P)
            print(f"### {tid} ({len(P)}):")
            for x in P:
                print(f"    - {x}")
    print(f"\nspecs with problems: {bad} | total problems: {total_problems}")
    sys.exit(0 if total_problems == 0 else 1)


if __name__ == "__main__":
    main()
