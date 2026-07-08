#!/usr/bin/env python
"""task_realism_audit.py — audit whether each of the 100 StudioBench tasks is a GENUINE,
LONG-HORIZON, real freelance creative task that a professional designer would actually be hired
for (Upwork/Fiverr/agency style) — not artificial, trivial, or contrived.

Two independent text-LLM judges (gemini + openai) read each task's brief/deliverables/workflow and score:
  realism 0-10 (is this a real job a client would post & pay for?), long_horizon yes/no (substantial multi-step),
  and flag anything weak. Writes task_realism_flags.json + prints the flagged tasks.

Usage: .venv/bin/python task_realism_audit.py
"""
from __future__ import annotations
import glob, json, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
from adapters.text_llm import TextLLM

SPECDIR = config.PROJECT_DIR / "complex_benchmark/adobe_only/specs"
FLAG = 7

def summarize(sp):
    outs = [o.get("name") for o in sp.get("outputs", [])]
    return ("TITLE: %s\nCLIENT ASK: %s\nBRIEF: %s\nWORKFLOW: %d connector steps (%d distinct tools), nature=%s\n"
            "INPUTS: %s\nDELIVERABLES: %s"
            % (sp.get("title", ""), sp.get("one_line_ask", ""), (sp.get("full_brief") or "")[:900],
               len(sp.get("connector_workflow", [])), sp.get("distinct_adobe_tools", 0), sp.get("workflow_nature", ""),
               ", ".join(i.get("name", "") for i in sp.get("inputs", [])[:10]),
               ", ".join(str(o) for o in outs[:10])))

SYS = ("You are a veteran creative-agency producer who has hired freelance designers for 15 years. "
       "Judge whether a task is a GENUINE, REALISTIC freelance creative job a real client would post and pay for, "
       "and whether it is LONG-HORIZON (substantial, multi-step real production work — not a trivial one-off).")

def judge(sp, tl):
    q = ("%s\n\nAnswer as JSON ONLY: {\"realism\":0-10, \"long_horizon\":true/false, \"real_freelance_job\":true/false, "
         "\"verdict\":\"strong\"|\"ok\"|\"weak\", \"issues\":[\"...\"]}. "
         "Score realism LOW (<7) if the task is artificial, contrived, trivial, incoherent, or not something a real client "
         "would actually hire a freelancer to do. long_horizon=false if it is a quick single-step job." % summarize(sp))
    recs = {}
    for prov in ("gemini", "openai"):
        try:
            recs[prov] = tl.complete_json(SYS, q, role="judge", prefer=prov, temperature=0.2)
        except Exception as e:
            recs[prov] = {"realism": None, "error": str(e)[:80]}
    rs = [r.get("realism") for r in recs.values() if isinstance(r.get("realism"), int)]
    mn = min(rs) if rs else 0
    lh = all(r.get("long_horizon", True) for r in recs.values())
    job = all(r.get("real_freelance_job", True) for r in recs.values())
    issues = [i for r in recs.values() for i in (r.get("issues") or [])][:4]
    return {"id": sp["id"], "realism": mn, "long_horizon": lh, "real_job": job, "issues": issues,
            "scores": {p: r.get("realism") for p, r in recs.items()}}

def main():
    specs = [json.load(open(f)) for f in sorted(glob.glob(str(SPECDIR / "*.json")))]
    tl = TextLLM()
    print("task-realism auditing %d tasks (2 judges each)..." % len(specs))
    results = []
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=8) as ex:
        for fut in as_completed([ex.submit(judge, sp, tl) for sp in specs]):
            results.append(fut.result())
    results.sort(key=lambda r: (r["realism"], r["long_horizon"]))
    flagged = [r for r in results if r["realism"] < FLAG or not r["long_horizon"] or not r["real_job"]]
    json.dump({"flagged": flagged, "all": results}, open(config.PROJECT_DIR / "task_realism_flags.json", "w"), indent=2)
    print("\n==== TASK-REALISM AUDIT (%d tasks, %.0fs) ====" % (len(results), time.time() - t0))
    print("  realistic & long-horizon: %d/%d" % (sum(1 for r in results if r["realism"] >= FLAG and r["long_horizon"] and r["real_job"]), len(results)))
    print("  flagged: %d\n" % len(flagged))
    for r in flagged:
        tags = []
        if r["realism"] < FLAG: tags.append("realism=%s" % r["realism"])
        if not r["long_horizon"]: tags.append("NOT-long-horizon")
        if not r["real_job"]: tags.append("not-a-real-job")
        print("  %-7s [%s] %s" % (r["id"], ", ".join(tags), (r["issues"][0] if r["issues"] else "")[:110]))
    print("\n  full -> task_realism_flags.json")

if __name__ == "__main__":
    main()
