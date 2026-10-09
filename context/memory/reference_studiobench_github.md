---
name: reference_studiobench_github
description: "StudioBench / Creative-AI-Benchmark GitHub repo — URL, scope, push setup, what's excluded"
metadata:
  node_type: memory
  type: reference
  originSessionId: 350c3d90-d24f-4d9c-aa65-50850b73e921
---

**Repo:** https://github.com/dhigdec/creative-ai-benchmark (PRIVATE, company account `dhigdec`). Pushed 2026-07-08.

- **Local root:** `Deccan/Adobe-Freelance-Leads/` (this is the git repo; `git init` was done here, branch `main`). Scope = the WHOLE Adobe-Freelance-Leads folder (specs + pipeline + input_assets manifests/dashboards + prior Adobe experiments), NOT the sibling `illusion_backend`/`darwin`/`SWE-Freelance-Leads` (those stay out).
- **Auth:** SSH via `~/.ssh/id_ed25519` (registered on `dhigdec`; `ssh -T git@github.com` → "Hi dhigdec!"). Remote `origin = git@github.com:dhigdec/creative-ai-benchmark.git`. `gh` CLI is NOT installed on this machine.
- **Commit identity (ALWAYS use):** `Dhiren Gangishetty <dhiren.gangishetty@deccan.ai>` — his company email, set repo-local. User wants ALL commits under this email so they count on `dhigdec`'s contribution graph (the email must be verified on that account). History was rewritten (filter-branch) + force-pushed 2026-07-08 to move the original 7 commits off `dhirengshetty@gmail.com` onto the company email. Commit real work in logical increments; do NOT pad with empty/fake commits.
- **Excluded via `.gitignore`** (see [[committed-secrets-risk]]): both `.env` files (asset_pipeline = Gemini/OpenAI/Anthropic/FAL keys; pipeline = Upwork OAuth), `.venv/`, `node_modules/`, `*.db`/backups, and ALL heavy media (`input_assets/**/assets/` + image/video/audio/pdf/zip exts) — the ~1.6GB of generated media lives on GCS, not git. Repo is ~148MB / 2100 files.
- **7 logical commits** (scaffolding → ingestion → specs → pipeline → manifests/dashboards → docs → brand-kit fixes). Commit convention ends with `Co-Authored-By: Claude Opus 4.8 (1M context)`.
- To push updates: `cd Deccan/Adobe-Freelance-Leads && git add -A && git commit && git push`.
- **Still NOT pushed / on disk only:** the broken AO-95 `voltcast_e42_master_16x9.mp4` (547MB, 740s 4K — should be a ~5s clip; excluded as media, still a benchmark defect to fix). Kept the raw-scraped `harvest_briefs.json`/`upwork_full*.json` (real 3rd-party job posts) since repo is private — drop + history-rewrite if it ever goes public. See [[project_studiobench_input_assets]], [[project_studiobench_artifacts]].
