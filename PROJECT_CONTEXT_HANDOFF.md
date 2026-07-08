# ADOBE FREELANCE-TASKS PROJECT — COMPLETE CONTEXT HANDOFF
**Written 2026-06-11 · for transferring the whole project to a new Claude session/subscription.**
Read this top-to-bottom once; after that you can operate everything in this project cold.

---

## 0. MISSION & WHERE WE ARE RIGHT NOW

**Mission:** Prove AI agents can execute real freelance design tasks end-to-end on Adobe tooling:
(1) harvest real freelance briefs → (2) verify which are doable via the Adobe Creative Cloud MCP connector →
(3) AI-generate the *input assets* a client would hand over (simulating the client) → (4) judge/score those
asset packages → (5) execute the tasks through the Adobe connector → (6) human-annotate the results.

**Status:** steps 1–6 ALL have working v1 implementations and real artifacts (see sections below).

**⚠️ THE OPEN THREAD (user's latest direction, unresolved):** The user reviewed the 5 executed tasks
(vectorize / background-removal / auto-tone) and said they are **"baby small tasks… trivial… look like job
postings"**. They want: **complex creative tasks** with rich, specific task descriptions ("everything the
business would want their freelancer to do"), full creative workflows that **use the generated input assets
and produce finished final outputs** (composed deliverables — finished social posts, postcards, posters —
not single-tool image ops). A clarifying question was asked (composition approach + which flagship
deliverables) but the user dismissed it — **decision still pending**. Key constraint to re-explain if needed:
the MCP connector is an *element processor* (bg-removal/grade/vectorize/expand/etc.) and CANNOT headlessly
compose multi-element layouts (Express `search_design` needs a human gallery click; `fill_text` swaps text
only; InDesign `document_merge_data_layout` needs a client-supplied .indd). Options previously laid out:
**(a) Hybrid** — connector processes all elements + an HTML/CSS (or PIL) compositor assembles finished
designs (recommended); **(b) connector-only multi-step image pipelines** (non-trivial but image-centric);
**(c) wire Adobe's direct REST APIs** (Firefly generative + Express/InDesign programmatic) for true headless
generation+composition. Flagship candidates proposed (all have brand assets already generated): Zaytoun
restaurant IG launch campaign; Sterling & Chase just-listed postcard; The Lock House cast key-art poster;
Pushing Packs product-hero campaign.

---

## 1. MACHINE / ENVIRONMENT

- macOS (darwin 25.3.0), zsh, **NOT a git repo** anywhere in the project.
- Project root: `/Users/dhiren/Downloads/Deccan/`
- Main project dir: `/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/`
- Sibling (earlier SWE project, reused classifiers): `/Users/dhiren/Downloads/Deccan/SWE-Freelance-Leads/`
  (notably `hardness.py` with is_hard/is_task_brief/is_real_task/project_score/role_score regex classifiers)
- System python is 3.9.6 (`/usr/bin/python3`); the pipeline has its own venv (below). Node v24 available.
- Pipeline venv: `Adobe-Freelance-Leads/asset_pipeline/.venv` → run as
  `asset_pipeline/.venv/bin/python` (has PIL/Pillow 11, openai 2.41.1, google-genai, anthropic 0.109.1,
  python-dotenv, requests).
- Node deps for doc builders: `Adobe-Freelance-Leads/node_modules` (docx lib). Run builders with
  `NODE_PATH=/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/node_modules node <script>`.
- **API keys live in `Adobe-Freelance-Leads/asset_pipeline/.env`** (chmod 600, gitignored):
  `GEMINI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` — ALL THREE SET and verified working.
  (Do not commit; read from there.)
- Preview server config: `Adobe-Freelance-Leads/.claude/launch.json` — name `survey`, python http.server
  on port 8793 serving `executed_jobs/`. (A separate "adobe-site" preview server has been used on port 8765
  serving the project root.)
- Claude Code memory dir (this machine):
  `/Users/dhiren/.claude/projects/-Users-dhiren-Downloads-Deccan/memory/` — see MEMORY.md index; Adobe files:
  `project_adobe_freelance_dataset.md`, `project_adobe_execution_survey.md`.

---

## 2. PROJECT ARC (chronological, what happened in order)

1. **Dataset harvest** (earlier sessions): scraped/collected freelance postings (Upwork browser harvests,
   Freelancer.com, PeoplePerHour) into `pipeline/data/adobe.db` (sqlite). 5,218 Adobe-relevant items.
2. **Cleaning:** `cleantask=1` flag → 3,888 genuine project briefs (job ads / vague posts removed).
3. **Connector capability verification:** loaded the real Adobe MCP tool schemas; discovered the connector
   has NO text-to-image generation (Firefly gen not exposed; `image_fill_area` = solid color only;
   `image_generative_expand` = outpaint edges only; Express = template+text-swap only).
4. **Doable classification:** 2 agent waves (46 agents total) verified candidates tool-by-tool →
   **1,260 connector-doable tasks** (`adobe_doable_full.json`), tiers: **57 full / 862 template / 341
   partial**, 23 categories, 6 families. ~1,275 dropped with reasons (483 bespoke logo/identity, 232
   illustration, 126 needs-generation, etc.).
5. **Deliverable docs built:** `Adobe_Connector_Doable_Tasks.docx` (+csv) with per-task colored boxes
   (workflow / input-assets / connector-limit / original brief), tier badges; master docs for all sources.
6. **Interactive dashboard:** `Adobe_Connector_Doable_Tasks.html` (~2MB, self-contained, dark theme,
   1,260 tasks embedded, charts + filterable explorer). Template: `site_template.html`, data builder:
   `build_site_data.py` (writes `adobe_site_data.json`, now also copied to project root).
7. **Asset-generation pipeline built** (`asset_pipeline/`): simulates the CLIENT — generates every input
   asset for chosen tasks via Gemini + OpenAI image/text APIs. Round 1: 5 tasks. Round 2 (wide-mix,
   top models incl. Nano Banana Pro + gpt-image-2): 5 more. **10 complete packages** under `input_assets/`.
8. **Package judge + closed loop** (`judge.py` + `scorecard.py`): 3-judge cross-provider panel
   (Claude/Gemini/GPT) scores each package 6 dimensions vs the task; adversarial red-team; per-asset-QC
   cross-check; closed loop regenerates flagged assets (surgical JSON patch for data; regen for images);
   deterministic `loop_success` ground truth. Hardened via sabotage testing (5 real bugs found+fixed).
9. **Adobe connector EXECUTION** (2026-06-11): proved headless execution works (block-upload → edit tool →
   download). Ran 5 tasks → 9 real Adobe outputs under `executed_jobs/`.
10. **Annotation survey:** `executed_jobs/Annotation_Survey.html` — 125 content-specific rubric items
    (5 vision agents viewed the real pixels and authored input/output/task rubrics), autosave + JSON export.
11. **User feedback:** executed tasks too trivial → wants full complex creative workflows with composed
    final deliverables. ← **YOU ARE HERE.**

---

## 3. THE DATASET (verified-doable freelance tasks)

**Canonical file: `Adobe-Freelance-Leads/adobe_doable_full.json`** (2.5MB, 1,260 records).
Per record: `id, family, category, task_type, title, source (upwork|freelancer|peopleperhour), date, url,
vertical (industry), mcp_workflow (the Adobe tool chain string), inputs[] (verbatim input-asset checklist),
feasibility (full|template|partial), note (connector-limit), desc (original client brief, verbatim)`.

Numbers that matter:
- Funnel: 5,218 collected → 3,888 clean briefs → 2,535 screened → **1,260 verified doable** (46 agents).
- Tiers: 57 full (4.5%) · 862 template (68%) · 341 partial (27%).
- Families: Express Template Design 966 · Photo & Image Editing 142 · Vector & Illustrator 68 ·
  Video & Audio 48 · InDesign & Documents 33 · Stock 3.
- Top categories: Logos(template) 159, Social Media Graphics 139, Flyers&Posters 114, Brochures 106,
  Presentations 79, Photo Retouch 78, Labels 70, Vectorize 68, Ads 60, Business Cards 53, Banners 48,
  Covers 46, Video Cut 42, Menus 39, BG-Removal 37…
- Sources: upwork 923 / freelancer 314 / pph 23. Briefs: median ~495 chars, 27% >1000 chars (rich),
  15% <300 (thin), 12% name a real business.
- Dropped 1,273 with reasons (bespoke logo/identity 483, custom illustration 232, needs AI generation 126,
  video production 113, web/app dev 105, multi-page layout 77, …).

**SQLite DB:** `pipeline/data/adobe.db` — table `items` (kind='task', cleantask flag, source, vertical,
title, description, url, posted_at, adobe_tools, budget, raw_json…). The pipeline package for it is
`pipeline/` (own venv pattern, `adobe_pipeline.db` module: `db.connect(path)`).

**Other dataset artifacts (project root):** `Adobe_Connector_Doable_Tasks.{docx,csv,html}`,
`Adobe_All_Sources_Master.docx` (3,888 clean), `Adobe_Upwork_Master.docx`, `Adobe_Tasks_Export.csv`,
`adobe_doable_final.json` (the earlier 120-task editing-only set, superseded), `db_all.json`,
`upw*.json` (raw harvests), older `tasks_*.js` build scripts, `_archive_pre_cleanup_2026_06_08/` (pre-clean docs).
Doc builders: `build_adobe_full.js` (current docx builder), `build_adobe_doable.js`, `build_adobe_ai.js` (older),
`export_db_json.py` (db→json for builders). Dashboard: `site_template.html` + `build_site_data.py`
(+ `adobe_site_data.json`; HTML at `Adobe_Connector_Doable_Tasks.html`; `serve_site.js` to serve).

---

## 4. ASSET-GENERATION PIPELINE (`asset_pipeline/`) — simulate the client

**Purpose:** for a chosen task id, generate EVERY input asset the brief implies (photos, logos, copy,
menus, CSVs), coherent under an invented/extracted brand persona, with QC, manifests, and contact sheets.

**Files (all in `Adobe-Freelance-Leads/asset_pipeline/`):**
- `config.py` — env loading, MODEL registry (roles → candidate (provider,model,quality) lists), PRICES,
  caps (MAX_IMAGES_PER_RUN=60, COST_GATE_USD=10, QC_MIN_SCORE=7, QC_MAX_REGENS=2), `resolve(role)`,
  `key_matrix()`. **Roles:** image_photoreal/logo/cheap (round-1), image_hero_text (→ gemini-3-pro-image
  "Nano Banana Pro" first), image_photoreal2 (→ gpt-image-2 high first), image_cheap2 (gemini-3.1-flash-image),
  writer (gemini-2.5-flash), judge (gemini-2.5-flash / gpt-4.1-mini), package_judge (claude-sonnet-4-6 /
  gemini / gpt-4.1).
- `specs.py` — **hand-authored TaskSpecs for the 10 tasks** (assets with prompts/prompt_fn, filenames,
  QC criteria, decisions[]); SPECS dict; PILOT_ORDER=[440,5272,239,1097,5649], PILOT2_ORDER=[430,3491,502,2335,5604].
  ⚠️ str.format prompts: literal JSON braces must be doubled `{{}}`.
- `personas.py` — stage-1 brand persona synthesis (cached `persona.json` per task; invent vs from_brief).
- `adapters/` — `openai_img.py` (gpt-image-1/2, b64, transparent bg support), `gemini_img.py`
  (flash-image/NBP/imagen via google-genai SDK + REST fallback; output normalized to exact WxH;
  ⚠️ NBP `image_size:"2K"` param is rejected by this SDK version — guarded by broad except),
  `text_llm.py` (TextLLM.complete/complete_json/review_image; gemini→openai→anthropic chain; `last_used`).
- `degrade.py` — seeded PIL degradation profiles (underexposed_warm/overexposed_flat/cool_cast_noisy/
  dull_lowcontrast) + `soften()` + `flatten_white()` (⚠️ alpha must flatten to WHITE not black).
- `qc.py` — technical checks (dims/size/uniform/messy_background/alpha) + vision judge wrapper.
- `generate.py` — orchestrator. CLI: `--task N (repeat) | --all-pilot | --check [--deep] | --dry-run |
  --force | --asset KEY | --images-provider | --skip-vision-qc | --yes | --quiet`. Stages: persona → data/text
  → images (QC loop ≤2 regens w/ judge feedback) → post-process (degrade/soften) → manifest+INTAKE+sheet.
  Resume-safe via per-task `state.json`. **Closed-loop hooks:** reads `feedback.json` ({asset_key: fix}) —
  for images appends to prompt; for data/text DOES A SURGICAL PATCH of the existing file (keeps shape, applies
  only the fix, retries once on check failure, marks qc.status=failed if still bad).
- `manifest.py` — manifest.json (the agent-facing contract: every asset ↔ verbatim input requirement,
  generator+prompt, qc, sha256, decisions[], coverage, ready_for_agent) + INTAKE.md renderer.
- `contact_sheet.py` — per-task contact_sheet.html + input_assets/index.html (dark theme, b64 thumbs).
- `validate.py` — offline invariants (files/sha/dims/coverage/pairings). Run anytime.
- `judge.py` + `scorecard.py` — see section 6.
- `README.md`, `requirements.txt`, `.env` (KEYS — all 3 set), `.env.example`, `.gitignore`, `.venv/`.

**Commands:**
```bash
cd /Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/asset_pipeline
.venv/bin/python generate.py --check            # key/model matrix + spec coverage lint
.venv/bin/python generate.py --task 440 --dry-run
.venv/bin/python generate.py --all-pilot --yes  # regenerate (resume-safe; cached assets skip)
.venv/bin/python validate.py                    # offline checks
```

**Generation cost so far:** round 1 ≈ $5.90, round 2 ≈ $9.60 (incl. NBP redo) → ~$15.5 for 88 assets/67 images.
Image census across manifests: gpt-image-2 ×24, gpt-image-1 ×21, gemini-2.5-flash-image ×13,
gemini-3-pro-image (NBP) ×8. Text/persona/QC: gemini-2.5-flash. **User rule: Claude generates NO assets**
(Claude as JUDGE is explicitly approved). gpt2 hero-logo alternates preserved as `originals/gpt2_alt_*.png`.

---

## 5. THE 10 GENERATED INPUT-ASSET PACKAGES (`input_assets/<id>_<slug>/`)

Each folder: `assets/` (the client-handoff files) · `originals/` (ground-truth/pre-degrade/alternates) ·
`prompts/` (full rendered prompt per asset) · `persona.json` · `manifest.json` · `INTAKE.md` ·
`contact_sheet.html` · `state.json` · `run.log` · `judgement.json` (package-judge verdict).
Top level: `input_assets/index.html` (gallery), `scorecard.html` + `scorecard.json` (judge leaderboard —
NOTE: predates final judge hardening; re-run `judge.py --all` to refresh).

| id | slug | persona/brand | key assets |
|---|---|---|---|
| 440 | logo-vectorize | **Emberleaf Teas** (artisan tea) | softened "ChatGPT" logo raster + brand_colors.json |
| 5272 | doordash-menu | **Zaytoun** (Levantine fast-casual; #5D705C/#C77C4F/#F5F5DC) | logo, menu.json/md (12 items), 7 dish photos |
| 239 | social-media-graphics | **Aura & Clay** (ceramics; #F8F4EE/#C27664/#7A8E7A) | transparent logo, brand_guide.md, 3 product + 3 lifestyle photos, post_copy.json (6 posts) |
| 1097 | photo-retouch-batch | **Willow Creek Living** (lifestyle blog) | 10 degraded photos in assets/ + 10 pristine ground-truths in originals/ (degrade params in manifest) |
| 5649 | shopify-card-photos | **Pushing Packs** (real store from brief; fictional products: Kaelen Vance/Zenith Ascent, Anya Sharma/Stellar Flux, Jax Nova/Chronos Relic, Galactic Gridiron box) | products.json + 8 messy iPhone-style slab/box photos, Shopify-handle filenames |
| 430 | cosmetics-label | **Veridian Dew** (clean beauty; #214E3B/#F7F2E8/#C5B48D) | logo, product_lines.json, ingredients.json/md (INCI+warnings), dieline_spec.json/csv, 2 blank container shots |
| 3491 | seniorcare-brand | **Modern Care Collective** (from brief; cream/sage/terracotta) | logo, 5 caregiver+senior photos, services_copy.json/md |
| 502 | lockhouse-pack | **The Lock House** (reality show, from brief; #00566B/#000/#FFD700) | show logo, 6 cast portraits (Anya Sharma, Marcus "Mac" Thorne, Izzy Rossi, Kai Tanaka, Bree Jenkins, Liam O'Connell), 2 sponsor logos (VOLTRA, StreamNest), show_copy.json (intros/voting/elimination) |
| 2335 | flashdelivery-ads | **Flash Delivery** (UK convenience delivery, from brief; #0047AB/#FF4500/#FFD700) + merchants **Gary's Groceries**, **The Night Nook** | parent+2 merchant logos, 4 ad photos, brand_pack.json, ad_copy.json (6 concepts) |
| 5604 | realestate-kit | **Sterling & Chase** (luxury realty; MANDATED kit #0A0A0A/#FFF/#C9A227/#B3282D) | team logo, agent headshot, 5 listing photos (twilight/kitchen/suite/pool/foyer), listing.json (price/open-house/agent/market tips) |

Latest judge results (hardened judge, individual runs): 430 intact scores stable 8.1–8.3; 440 8.7;
sabotaged-430 craters to 3.5 (cap grounded in deterministic data_checks). Earlier full-panel `--all`
leaderboard (pre-hardening, for reference): 440 10.0 · 502 9.3 · 1097 9.0 · 3491 8.8 · 239 8.7 · 430 8.6 ·
5649 8.5 · 5604 8.2 · 5272 8.0 · 2335 6.6 (the 2335 low score caught a REAL bug: ad_copy referenced
merchants whose logos didn't exist; surgically patched later).

---

## 6. PACKAGE JUDGE + CLOSED LOOP (`judge.py`, `scorecard.py`)

**What it is:** package-level LLM-as-judge: "are these the right assets for THIS task, could the Adobe
workflow consume them?" — distinct from per-asset QC.

**Design:** 6 anchored dimensions (task_fit, completeness, executability, realism, coherence,
decision_quality; 0–10 with written bands, evidence cited by asset id, machine-actionable `fix` =
{target_asset_key, problem, prompt_delta}). Per-archetype weights (editing tasks weight executability+fit;
template/brand tasks weight coherence+completeness+realism). **Panel:** one judge per provider —
claude-sonnet-4-6 + gemini-2.5-flash + gpt-4.1 (all 3 live) — per-dim MEDIAN, spread≥3 flagged low-confidence.
**Red-team:** hostile-client pass (biggest rejection reason + choke asset). **QC cross-check:** flags
"assets 9/10 individually but package dim low". Verdicts: ≥8.5 client-ready / 7–8.5 minor-gaps /
5–7 needs-rework / <5 reject.

**Hardening history (all verified by sabotage tests — deleting mandatory `warnings` from 430's
ingredients.json):**
1. False recovery eliminated: deterministic `data_checks` (`field[].sub` required-field syntax in specs),
   patch retries once, `loop_success` = ground-truth verdict (no unresolved fixes AND no remaining
   deterministic defects) — overrides any rosy score.
2. Accuracy: mandatory-missing → completeness ≤3 hard rule; red-team severity cap (sev≥9→cap 3.5,
   ≥8→5.0) — **gated**: fires only if a machine-detected deterministic defect exists OR ALL judges score a
   core dim ≤4 (stops one noisy vote capping good packages; killed the 5.0↔8.9 flicker → intact 430 stable
   8.1/8.1/8.3 across runs).
3. Loop targeting: `select_targets()` = deterministic data-check failures FIRST, then red-team choke (sev≥7),
   else single lowest-dim fix; one clean fix per asset (no concatenation); regen in spec order (deps first);
   ≤2 rounds; stall-guard; cost gate; snapshots `originals/preimprove_r{N}_*`; redundant post-loop re-judge
   removed (reuses last judging unless assets changed after it).

**Commands:**
```bash
cd asset_pipeline
.venv/bin/python judge.py --check                 # panel + per-task exposure (no spend)
.venv/bin/python judge.py --task 440              # judge one → judgement.json
.venv/bin/python judge.py --all                   # all 10 → input_assets/scorecard.html/json (~$0.6)
.venv/bin/python judge.py --task 2335 --improve --threshold 8 --yes   # closed loop
# flags: --panel gemini,openai,anthropic  --thumb-px 768  --skip-images  --rounds 2  --cost-gate
```
**Honest limits:** raw LLM score has ±1–2 noise on judgment-only dims (OpenAI lenient ~9–10, Claude strict
~5–6 on contested packages); the deterministic layer (data_checks + loop_success) is the trustworthy signal.
The closed loop's data-side fix is PROVEN (surgical patch adds exactly the flagged field in ~3s); image-side
regen works but is slow (gpt-image-2 ~2min/img) and end-to-end score-improvement on a contested package is
noisy — that's measurement noise, not a repair failure.

---

## 7. ADOBE CONNECTOR — WHAT IT IS, WHAT WORKS HEADLESSLY (verified live)

**Server id `e551eb5f-cec3-41e9-9bd4-9ff5f4d014ff` (Adobe Creative Cloud MCP), ~70 tools. ALWAYS call
`adobe_mandatory_init` first** (returns the file-handling/routing doc). A second Adobe Marketing MCP
(`fe9837f5-…`) exists (read-only analytics; irrelevant here). A Canva MCP (`4aef80de-…`) also appeared in
the env (generate-design/export-design etc.) — unexplored; potentially relevant to the composition problem.

**Verified headless execution recipe (egress IS enabled in this env):**
```
1. adobe_mandatory_init
2. asset_initialize_file_upload {path, file_size (wc -c), media_type}      → transfer_document with
   presigned block/transfer hrefs + filename
3. Bash:  dd if=<file> bs=<blocksize> skip=<i> count=1 | curl -s -L -X PUT "<transfer href>" \
          -H "Content-Type: <mime>" --data-binary @-          (HTTP 200; one PUT per chunk)
4. asset_finalize_file_upload {filename, transfer_document VERBATIM}       → presignedAssetUrl + assetId
5. Call edit tool with that URL (imageURI / imageURIs)                     → returns outputUrl
   (photoshop-api.adobe.io/v2/short-url/…)
6. curl -L <outputUrl> -o <local file>                                     → download result
```
**Headless-working tools (proven):** image_vectorize, image_remove_background, image_apply_auto_tone —
plus by the same pattern all image_adjust_*/effects/crop/select/expand tools, document_render_vector,
document_convert_pdf, asset_search/asset_license_and_download_stock.
**NOT headless / not available:** `asset_add_file` (interactive picker — never use), `search_design`+
`fill_text` (Express templates need a human gallery selection; fill_text = text-only swaps),
`document_merge_data_layout` (needs client .indd), all text-to-image/generative fill ("not available in
this environment" per init doc; only generative_expand outpainting), object removal, compositing,
upscaling, video trim/format-convert. Outputs may come back as JPEG even with .png names — check mime.

---

## 8. EXECUTED JOBS (`executed_jobs/`) — 5 tasks run live (2026-06-11)

Per task: `<id>_<slug>/{input_assets/, outputs/, job.json, TASK.md}`. Master metadata:
`executed_jobs/execution_data.json` (briefs, workflows, tools, Adobe requestIds, per-pair intended_prompt).

| task | tool | pairs (input → output) |
|---|---|---|
| 440 | image_vectorize | logo_chatgpt_raster.png → outputs/logo_vectorized.svg (1024², 32 paths) |
| 5649 | image_remove_background ×2 | slab.jpg→slab_cutout.png, box.jpg→box_cutout.png (clean transparent) |
| 502 | image_remove_background ×2 | anya.jpg→anya_cutout.png, izzy.jpg→izzy_cutout.png |
| 1097 | image_apply_auto_tone ×2 | photoNN_degraded.jpg→photoNN_corrected.jpg (+ photoNN_groundtruth.jpg refs) |
| 5604 | image_apply_auto_tone ×2 | twilight.jpg→twilight_toned.jpg, kitchen.jpg→kitchen_toned.jpg |

**Annotation survey: `executed_jobs/Annotation_Survey.html`** (7.8MB self-contained; open directly).
Sidebar job nav · per job: client brief, connector workflow + executed pipeline, tools+requestIds, persona ·
input→output displays (cutouts on checkerboard, 1097 three-up with ground-truth, inline SVG) ·
**125 scoring items** (input rubrics + output rubrics + task rubrics; likert5/yesno/text with guidance +
reference answers) · annotator name, live progress, localStorage autosave, **Export → JSON download**.
Builder: `executed_jobs/build_survey.py` (run with venv python; embeds downscaled b64 images).
Rubrics JSON (authored by 5 vision agents who viewed the real files): `executed_jobs/rubrics/rubrics_<id>.json`.

**⚠️ User verdict on these executions: TOO TRIVIAL** — they're single-tool ops, not finished creative
deliverables. This is the open thread (section 0). Do NOT present more single-tool runs as "task execution."

---

## 9. OTHER ARTIFACTS & LOCATIONS (quick map)

```
Adobe-Freelance-Leads/
├── adobe_doable_full.json          ← THE dataset (1,260)
├── Adobe_Connector_Doable_Tasks.{docx,csv,html}   ← deliverable doc + dashboard
├── adobe_site_data.json            ← dashboard data (also /tmp/adobe_site_data.json originally)
├── site_template.html, build_site_data.py, serve_site.js
├── build_adobe_full.js             ← current docx builder (build_adobe_doable.js/_ai.js older)
├── export_db_json.py, db_tasks.json, db_all.json
├── Adobe_All_Sources_Master.docx, Adobe_Upwork_Master.docx, Adobe_Tasks_Export.csv  (clean-set docs)
├── Adobe_Freelance_Tasks.docx, Adobe_Tasks_and_Jobs_Master.docx, Upwork_Tasks.docx  (older)
├── adobe_ai_sample.json, adobe_ai_sample5.json, adobe_doable_final.json             (superseded)
├── upw2.json, upwork_1001.json, upwork_full*.json, upwork_cards.json, tasks_*.js    (raw harvests/builders)
├── merge_upw2*.py, merge_upwork_1001.py, cleanup_db.py, prune_non_adobe.py          (ingest utils)
├── _archive_pre_cleanup_2026_06_08/   (pre-cleaning docs)
├── pipeline/                       ← sqlite + adobe_pipeline pkg (data/adobe.db)
├── asset_pipeline/                 ← generation + judge (see §4/§6; .env KEYS HERE)
├── input_assets/                   ← 10 packages + index.html + scorecard.{html,json}
├── executed_jobs/                  ← 5 executed tasks + Annotation_Survey.html + rubrics/
├── .claude/launch.json             ← preview server config
└── PROJECT_CONTEXT_HANDOFF.md      ← this file
SWE-Freelance-Leads/                ← sibling project (hardness.py classifiers, swe.db, personas docs)
```

---

## 10. KEY LESSONS / GOTCHAS (hard-won; don't re-learn)

1. **Connector truth:** no text-to-image anywhere in the MCP; Express path is template+text-swap and needs a
   human click; judge any "doable" claim against actual tool schemas (`ToolSearch "select:<tool>"`).
2. **`asset_add_file` is an interactive picker** — for automation always use initialize/PUT/finalize.
3. **Alpha flattening:** gpt-image-1/2 sometimes returns RGBA; naive `.convert("RGB")` → BLACK background.
   Always `flatten_white()` (in degrade.py) unless transparency is wanted.
4. **str.format prompts:** literal JSON braces in specs must be `{{ }}` (a single-brace bug killed 5649's
   first run with KeyError '"products"').
5. **Text-asset deps:** ctx.assets must include kind="text" assets too (post_copy depends_on brand_guide bug).
6. **NBP via google-genai SDK on py3.9:** `ImageConfig(image_size="2K")` raises pydantic extra_forbidden —
   catch broad Exception and fall back to aspect-ratio-only. Model ids verified live: gemini-3-pro-image,
   gemini-3.1-flash-image, gpt-image-2 (+dated), gpt-image-1.5 all exist on these keys.
7. **LLM-judge noise is real:** ±1–2 on subjective dims; OpenAI lenient / Claude strict. Anchor caps/verdicts
   in deterministic checks; never let a single noisy vote gate anything; don't re-judge unchanged state.
8. **Surgical patch > full regen for data fixes** ("add a fonts field" — regen forgot it, patch nailed it).
9. **Anthropic vision judge needs max_tokens 8192** (4096 truncated mid-JSON → "no parseable JSON").
10. **Outputs from photoshop-api can be JPEG despite .png naming** — verify mime, rename.
11. Costs are tiny: ~$15.5 total generation, ~$0.64 full judge pass, ~$0.01 surgical patch loop.

## 11. USER'S OPERATING RULES & PREFERENCES (respect these)

- **Asset generation must use non-Claude models** (Gemini/OpenAI; Nano Banana Pro + gpt-image-2 for round 2+).
  **Claude IS approved as a judge** (3rd panel member / tie-breaker).
- Wants honest, evidence-backed claims — they explicitly challenged "is the judge actually good?" and
  responded well to sabotage-test proof. Keep the deterministic-verification mindset.
- Wants rich specific task descriptions, not job-posting fluff; wants FULL workflows: brief → input assets →
  multi-step Adobe processing → **finished composed deliverable** ("strong tasks, strong input assets").
- Survey/HTML style: "decent and professional, nice colors, not too fancy" (the navy/indigo annotation
  survey was accepted; the dark-purple dashboard was accepted).
- Pays for APIs willingly (gave all 3 keys); budget gates at ~$10 per run are fine.
- Folder convention they asked for: task folder = task desc + source + input assets + outputs together
  (executed_jobs/<task>/ does this).

## 12. IMMEDIATE NEXT STEPS (when resuming in the new chat)

1. **Resolve the open decision** (section 0): hybrid compositor vs connector-only pipelines vs direct
   Firefly/Express REST APIs (the Canva MCP in the env may be a 4th option worth probing — it has
   generate-design/export-design tools that might compose headlessly).
2. Build 1–2 FLAGSHIP creative executions end-to-end (recommend Zaytoun IG launch campaign and/or
   Sterling & Chase just-listed postcard): rich rewritten brief → use existing input_assets package →
   6–10 connector ops per deliverable (bg-removal, relight/grade, expand, vectorize, crops per format)
   → composition step → finished 1080²+9:16 (+6×9" print) deliverables in executed_jobs/<task>/outputs/.
3. Re-run `judge.py --all` to refresh scorecard.{html,json} with the hardened judge.
4. Extend Annotation_Survey to the new composed deliverables (build_survey.py + new rubrics).
5. Possibly wire judge → auto-pre-score Adobe outputs alongside human rubrics.

— End of handoff. Everything above is verified-as-built on this machine as of 2026-06-11. —
