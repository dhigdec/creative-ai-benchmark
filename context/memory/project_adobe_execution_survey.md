---
name: project_adobe_execution_survey
description: Executed 5 freelance tasks live via Adobe connector + built the annotation survey HTML
metadata: 
  node_type: memory
  type: project
  originSessionId: d211b4cb-a472-42fb-9b28-9830636b078c
---

**2026-06-11 — Adobe connector EXECUTION + annotation survey (COMPLETE).** Proved the Adobe Creative Cloud MCP connector executes headlessly in this env and ran 5 tasks on the generated input assets.

**How headless execution works (verified):** egress IS enabled. Per asset: `asset_initialize_file_upload({path,file_size,media_type})` → returns transfer doc with presigned block-transfer URL(s) → Bash `dd | curl -L -X PUT <url> --data-binary @-` (HTTP 200) → `asset_finalize_file_upload({filename, transfer_document verbatim})` → returns `presignedAssetUrl` → feed that URL to edit tools → tool returns `outputUrl` (photoshop-api short-url) → `curl -L` to download. `asset_add_file` is an interactive picker (needs human) — DON'T use it; use the block-upload path. Generative AI / Express-template `fill_text` flows are NOT headless-runnable (need gallery UI / no text-to-image). Editing tools (image_remove_background, image_vectorize, image_apply_auto_tone, image_adjust_*, image_crop_and_resize) ARE fully headless.

**5 executed tasks (9 input→output pairs, all real Adobe outputs):** 440 logo→`image_vectorize`→SVG (32 paths); 5649 2 card photos→`image_remove_background`→transparent cutouts (clean); 502 2 contestant portraits→`image_remove_background`→cutouts; 1097 2 degraded photos→`image_apply_auto_tone`→recovered (have ground-truth originals for 3-up before/after); 5604 2 listing photos→`image_apply_auto_tone`→graded.

**Deliverables under `Adobe-Freelance-Leads/executed_jobs/`:** per task `<id>_<slug>/{input_assets/, outputs/, job.json, TASK.md}`; `execution_data.json` (all tasks+tools+requestIds); **`Annotation_Survey.html`** (7.8MB self-contained) — sidebar job nav, per-job brief/workflow/tools/API, input→output displays (cutouts on checkerboard, 1097 3-up with ground-truth, inline SVG), 125 content-specific scoring items (input rubrics + output rubrics + task rubrics authored by 5 agents who viewed the real pixels), likert5/yesno/text controls, autosave to localStorage + JSON export. Builder: `executed_jobs/build_survey.py` (venv python, embeds downscaled base64 imgs). Rubrics in `/tmp/rubrics_<id>.json`. Preview server config in `.claude/launch.json` (name "survey" port 8793; an "adobe-site" server runs on 8765 serving project root → survey at /executed_jobs/Annotation_Survey.html).

**Next options:** scale to more assets/tasks; wire the package-judge to auto-score outputs; add the 2048² white-canvas finishing step for 5649; the Express-template design tasks need the Firefly/Express path (not headless here).
