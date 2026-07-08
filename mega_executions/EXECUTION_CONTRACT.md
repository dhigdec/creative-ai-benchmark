# Mega-Execution Contract (round-5 long-horizon tasks) — binding

Execute ONE long-horizon Adobe task end-to-end: real connector ops + local composition into the
exact deliverables, with a complete audit trajectory. Builds on
`../flagship_executions/EXECUTION_CONTRACT.md` (READ IT — Adobe upload/chain/download protocol,
trajectory rules, honest actor labels, self-verify). This contract adds: the full connector suite,
local data-merge, and local video.

## Paths
- Your task dir: `mega_executions/<id>_<slug>/` with `input_assets/` (generated client files),
  `work/`, `steps/`, `outputs/`, `manifest.json` + `INTAKE.md` (what each input is).
- Your task's FULL ordered workflow (with per-step [C]/[T]/[L] tags + the iterative chain) is in
  `../complex_benchmark/definitive_10_tasks.json` — find your task by id; that workflow is authoritative.
- Connector capabilities + tags: `../complex_benchmark/FEASIBILITY.md`. Python:
  `../asset_pipeline/.venv/bin/python`. Compose: `mega_executions/lib/compose_lib.py`
  (`sys.path.insert(0,'.../mega_executions/lib')`). Trajectory: `mega_executions/lib/traj.py`.

## Connector protocol (proven this session, CC Pro active)
Tool prefix `mcp__824485eb-b50f-42b9-9a0b-cb5774d6d30d__`. Load schemas via ToolSearch (`select:` the
exact tools your workflow's [C] steps need + adobe_mandatory_init + asset_initialize/finalize_file_upload).
Call adobe_mandatory_init ONCE. Upload → chain `outputUrl`→next `imageURI`/`imageURIs` → download
`curl -sL`. Masking recipe: `image_select_subject`/`image_select_by_prompt` → returns a MASK url →
pass as `maskURI` to `image_fill_area`/`image_adjust_*`/`image_apply_*`/`image_invert_selection`.
Solid backdrop = select_subject → invert_selection → fill_area(preset gray/white/custom RGB). Stock =
asset_search(StockAsset) → asset_license_and_download_stock → use the download URL. Record EVERY
requestId. Retry 5xx/504 twice (30s wait) then fall back per the workflow + log honestly.

## Step feasibility — how to run each tag
- **[C] connector-confirmed** → run the real Adobe connector. Snap the downloaded output.
- **[L] local** → do it locally (compose_lib / ffmpeg / PIL). Honest actor `local_compositor` /
  `local_video`. Final multi-element LAYOUT assembly is always local (connector processes elements).
- **[T] data-merge** → DO IT LOCALLY: `compose_lib.data_merge(csv_path, draw_record_fn, out_dir,
  prefix, fmt, limit)` renders one output per CSV row (exactly what Adobe data-merge produces). The
  Adobe data-merge CONNECTOR needs a desktop-authored template (confirmed unusable headless), so this
  step is local — actor `local_datamerge`, and the trajectory note MUST say "data-merge rendered
  locally from <csv> (N rows); the document_merge_data_* connector requires a human-authored template."
  For big sets (e.g. 510 badges) render ALL rows but only SNAP the first 2-3 into steps/ and note the
  full count. You MAY still exercise `document_convert_pdf`/`document_render_layout`/`render_vector`
  [C] on a composed PDF/.ai where the workflow calls for a genuine render (those work).
- **VIDEO** (task 9003): the connector video tools don't return retrievable results headless — do the
  edit LOCALLY with ffmpeg (`compose_lib`-adjacent / imageio-ffmpeg): concat/cut the Veo clips,
  reframe to 9:16 & 1:1, mux the cleaned VO. Actor `local_video`. Grade the hero thumbnail via the
  connector [C].

## Trajectory (audit trail — non-negotiable, same as flagship)
`traj.py init` once; one snapped step per: input_baseline (originals you use), each connector op (with
real requestId), each local stage (data-merge/compose/video) in ≥3 visible stages, exports, verify.
`traj.py finish` at the end. Honest actor labels: adobe_connector | local_compositor | local_datamerge
| local_video | local_verify.

## Composition & copy
ALL client copy read PROGRAMMATICALLY from the input JSON/CSV/MD — never retype a name/price/code.
compose_lib fonts/palette per the task's persona (manifest.json client_persona). Full-res at export.

## Outputs & self-verify (before finishing)
Produce the deliverables the task's `deliverables` list specifies into `outputs/` at sensible print/web
dims. Write `outputs/README.md`: asked deliverable → produced file(s) → how made (connector ops + local
steps), honest limitations (local data-merge, ~1536px source cap for print, video local). Self-verify:
assert output dims; Read your 2 most complex finals for clipped text / collisions / palette / garbles;
fix before finishing. Return structured: connector_ops (count + requestIds), outputs[], steps_logged,
datamerge_rows, issues.

## Don'ts
Don't touch other task folders or input_assets/ (read-only source). Don't fake a connector requestId.
Don't claim local steps as connector. Don't upscale and call it print-res.
