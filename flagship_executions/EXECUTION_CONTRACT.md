# Flagship Execution Contract (binding for every execution agent)

You are executing ONE flagship freelance design task end-to-end: real Adobe connector
element-processing + local composition into the exact deliverables, with a complete
audit trajectory. The user presents this work — accuracy and visual quality are the bar.

## Paths & tools
- Project root: `/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/` (NOT a git repo).
- Your task dir: `flagship_executions/<id>_<slug>/` with `input_assets/` (client files),
  `work/` (intermediates), `steps/` (auto-managed snapshots), `outputs/` (deliverables),
  `TASK.md` (client work order), `PLAN.md` (your op plan — follow it exactly).
- Python: `asset_pipeline/.venv/bin/python` (PIL 11 available). Compose with
  `flagship_executions/lib/compose_lib.py` (`sys.path.insert(0, '<...>/flagship_executions/lib')`).
- Trajectory logger: `asset_pipeline/.venv/bin/python flagship_executions/lib/traj.py`.

## Adobe connector protocol (proven in this session)
Tool prefix: `mcp__824485eb-b50f-42b9-9a0b-cb5774d6d30d__`. Load schemas via ToolSearch
(`select:` the exact tools your PLAN lists, plus `adobe_mandatory_init`,
`asset_initialize_file_upload`, `asset_finalize_file_upload`). Then:
1. Call `adobe_mandatory_init` ONCE before anything.
2. Per file upload: `wc -c` + mime → `asset_initialize_file_upload {path:"flagship/<file>",
   file_size, media_type}` → for each `_links["...block/transfer"]` href:
   `dd if=<file> bs=<repo:blocksize> skip=<i> count=1 2>/dev/null | curl -s -o /dev/null
   -w "%{http_code}" -L -X PUT "<href>" -H "Content-Type: <mime>" --data-binary @-`
   (expect 200) → `asset_finalize_file_upload {filename, transfer_document: <VERBATIM full
   object from initialize — every key>}` → use `presignedAssetUrl`.
3. Call the edit tool with that URL (`imageURI`/`imageURIs`). Chain ops by passing the
   previous `outputUrl` directly as the next `imageURI` (no re-upload needed).
4. Download results: `curl -sL -o work/<name> "<outputUrl>"`. Outputs may be JPEG despite
   .png names — check with `file`, convert/rename via PIL if needed.
5. RECORD the `requestId` of EVERY connector result. On rate-limit/5xx: wait 30s, retry
   twice, then record the failure honestly and use the documented fallback in your PLAN.

## Trajectory (the audit trail — non-negotiable)
Init once: `traj.py init <task_dir> <id> <slug> "<title>"`.
Log ONE step per meaningful action via
`traj.py add <task_dir> --json '<entry>' --snap <image-path> [--snap-name <label>]`:
- entry fields: `phase` (element_processing|composition|export|verify), `actor`
  (adobe_connector|local_compositor|local_verify), `action` (tool/function name), `note`
  (one sentence: WHY this step serves THIS task), `input`, `output`, `params` (small dict),
  `adobe_request_id` (connector steps only — the real requestId).
- EVERY step gets a snapshot (`--snap`): connector steps snap the downloaded output;
  composition steps snap the in-progress canvas (save the canvas to /tmp first, then snap);
  export steps snap the final file; verify steps snap the thing verified.
- Step ZERO convention: log one `element_processing` step per ORIGINAL input you use,
  actor `local_verify`, action `input_baseline`, snapping the original — so the gallery
  shows before → after. Then proceed with ops.
- Composition must be logged in visible stages (background laid → imagery placed → type
  set → final), minimum 3 stages per composed piece or spread, each snapped.
- When done: `traj.py finish <task_dir>`.

## Composition rules
- ALL client copy is read PROGRAMMATICALLY from the JSON/MD input files and rendered
  verbatim — never retype a name, price, code or ingredient by hand in your script.
  (Tiny connective microcopy — a section header the layout needs — is allowed, max ~5
  strings/task, native-quality language, each noted in a trajectory note.)
- Use compose_lib fonts/palette EXACTLY as PLAN.md specifies. No emojis. Consistent
  margins. Nothing critical within the safe zone stated in the PLAN.
- Full print resolution at export only; work at full res but snap previews via traj.
- Honesty: print PDFs are assembled LOCALLY (PIL) because the connector has no image→PDF
  tool — the export step's note must say so. PDF/X-4 prepress conversion = print-house
  step; say that in outputs/README.md where relevant.

## Outputs & self-verification (before you finish)
- Produce EXACTLY the files PLAN.md lists, exact pixel dimensions, into `outputs/`.
- Write `outputs/README.md`: a table mapping every ASKED deliverable (from TASK.md) →
  produced file(s) → exact px/dpi → how it was made (connector ops used + composition),
  plus any honest limitations.
- Self-verify: a python pass asserting every output's exact dimensions (log as verify step),
  AND visually Read at least your 2 most complex finals (use the steps/ preview you
  snapped) checking: no clipped/overflowing text, no garbled glyphs, no element collisions,
  palette correct. Fix anything you find BEFORE finishing; log fixes as steps.
- Final structured return per your instructions (counts, requestIds, files, issues).

## Don'ts
- Don't touch other task folders or input_assets/ (read-only).
- Don't fake a connector op (every adobe_request_id must be real).
- Don't upscale anything and call it print-res — state true dims in README.
- Don't run interactive pickers (`asset_add_file` is forbidden).
