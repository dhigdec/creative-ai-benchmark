---
name: project_studiobench_gatsby_v5
description: "Gatsby V5 review page (dhigdec.github.io/creative-ai-benchmark/gatsby-v5): verifier set is objective-only, K-sectioned, dash-free, 18,118 atomic checks; where source + rebuild pipeline live"
metadata: 
  node_type: memory
  type: project
  originSessionId: aa9e6dfc-7579-493e-a3a8-45be309ed406
  modified: 2026-09-20T00:15:46.111Z
---

**Live page:** https://dhigdec.github.io/creative-ai-benchmark/gatsby-v5/ (GitHub Pages, repo `git@github.com:dhigdec/creative-ai-benchmark.git`, branch main, folder `docs/gatsby-v5`). Local clone: `~/Documents/ChatGPT/Adobe_Gpt/publish/creative-ai-benchmark/`. V4 preserved at `/gatsby-v4/`.

**State (2026-09-19):** 100 tasks, **18,118 atomic checks = 12,309 auto + 5,809 human**. Human verifiers grouped under the *objective-only* rubric questions from `Creative_AI_Benchmark refined (12).docx` (orange = objective): K1 Q1–Q5, K2 Q1–Q4, K5 Q1–Q2; K3/K4 and unmarked questions removed from the page. New **Trajectory verifiers** tab = K6 Q3–Q7 with Pass/Minor/Major guides, status "Pending: populated from the run trajectory". Coverage 1,091/1,100 task×question cells. Every check: one deliverable, one observable fact, artifact named as “Name” (file), exact value quoted, no em/en dashes in prose (dashes inside quoted record values kept as data), median 21 words. Commits: `e12bdf6` plain-language rewrite → `a1526be` K-sections → objective-only pass (latest).

**How the page is built:** `index.html` (~34 MB) = static head/CSS + one `<script type="application/json" id="data">` blob `{tasks[{checks[]…}], repairImages, kCatalog}` + the app JS. Same check objects are fanned out to `ATOMIC_VERIFIERS_ALL100.json`, `tasks/<ID>/VERIFIERS.json|.md`, `data/verifiers.csv`, `TASKS_V5_ALL100.json`. Rebuild by editing the blob + regenerating those by `check_id`.

**Pipeline scripts (session scratchpad, FRAGILE, copy into repo if reused):** `scratchpad/v5rw/compose_auto.py` (deterministic phrasebook per assertion op → `rewrite_auto.json`), `scratchpad/kmap/k_catalog_v2.json` (objective catalog), `app_new2.js` (renderer), `kapply2.py` (apply + gates + regen). Human rewrites/mappings/new checks were authored by 20-agent workflows writing per-task files (agents must write files; workflow return arrays cap at 4,096 items).

**Why:** Dhiren wants verifiers an expert can answer Yes/No in <20 s: explicit, artifact-named, atomic, objective, no dashes; K questions must be visibly covered, nothing "left behind". Google Sheet exports were NOT regenerated (still pre-K layout) — offer when relevant. See [[project_studiobench_v3_corpus]], [[reference_studiobench_github]].
