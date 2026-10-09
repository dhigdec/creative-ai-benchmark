# StudioBench — Full Project Context & ChatGPT + Adobe Connector Handoff

**Purpose of this file:** a single, self-contained context document you can feed to ChatGPT (or Codex, Cursor, any MCP client) so it understands the entire StudioBench creative-agent benchmark and can attempt the 100 tasks through **ChatGPT's Adobe connector**. It covers what the project is, how the Adobe connector works (and how ChatGPT differs from Claude), how to actually run a task, every location and repository, the asset inventory, the verified connector capability boundary, and the full 100-task corpus (Appendix A) plus the redesign in progress (Appendix B).

**Written:** 2026-09-10. **Supersedes** the older `PROJECT_FULL_CONTEXT.md` (2026-06-23) for connector facts — the Adobe connector was materially upgraded since then (see §2, §7).

---

## 0. How to use this file

1. Read §1–§4 to understand the project, the connector, and the scoring model.
2. Set up ChatGPT's Adobe connector per §3.
3. Pick a task from **Appendix A**. Upload its listed input assets (from the path shown), then paste that task's **Client brief** (inside the collapsible block) to the solver. Do **not** paste the verifier/hardness notes — those are the grader's reference.
4. Compare what ChatGPT produces against the task's **Required deliverables** and **Scoring verifiers**.

> This file is ~1 MB because it contains all 100 full briefs. If your ChatGPT session can't take it whole, feed §1–§8 first, then paste individual task blocks from Appendix A as you run them.

---

## 1. What StudioBench is

StudioBench is a benchmark for **professional creative work performed by AI agents**. 100 real freelance design tasks — sourced from real Upwork / Freelancer.com briefs, then laundered to fictional brands for IP-safety — that an agent completes **end-to-end through real professional tools** (the Adobe Creative Cloud connector), across **long, multi-step workflows**, producing **client-ready deliverables**.

It is deliberately *not* a "generate one nice image" benchmark. It measures whether an agent can:
- interpret a real client brief and use the supplied brand assets correctly,
- hold brand consistency across many assets,
- execute production-grade technical work (exact dimensions, formats, colour, record counts),
- work competently as an agent (plan, sequence, use tools, recover, verify), and
- be honest about limitations.

Every task is scored by human experts against a fixed rubric (§4); code is used only for objective facts (dimensions, formats, hashes).

**The core design principle (and the current rework mandate):** a small operation — remove background, tonal grade, vectorize, resize, format-convert — is a **step inside a larger commission, never a task by itself.** A valid task is a full freelance engagement (a campaign kit, a print/merch pack, a laid-out multi-page piece, a short video kit) whose difficulty comes from **judgement a non-designer gets wrong**, not from step count.

---

## 2. The Adobe connector — and how ChatGPT differs from Claude

**What it is.** "Adobe for Creativity" is an official Adobe MCP (Model Context Protocol) server exposing 50+ Photoshop / Lightroom / Illustrator / InDesign / Express / Premiere / Firefly tools. It is the same server regardless of which AI client connects to it.

- **MCP endpoint:** `https://adobe-creativity.adobe.io/mcp` — addable to any MCP-compatible client (ChatGPT/Codex, Cursor, VS Code, Claude).
- **Adobe for ChatGPT** shipped **December 2025** (Photoshop, Express, Acrobat inside ChatGPT — delivered as an app in ChatGPT).
- **Adobe for Creativity in Claude** shipped **April 2026** (the surface this project was built and executed on).

**The one difference that matters for this benchmark — generative AI.**
On the **Claude** surface, most generative capabilities are **disabled** (no text-to-image, no generative fill, no AI object removal, no background-replace-by-prompt, no cartoonize; the only generative exception is `image_generative_expand` / outpaint). On **ChatGPT / Codex** hosts, generative tools may be **enabled**. **Verify this in your own ChatGPT session before running.**

Why this matters: several StudioBench tasks are hard *precisely because* generative shortcuts are banned (e.g. "a square hero must reach 9:16 without generative expand"). If ChatGPT's Adobe app enables generation, an agent could take a shortcut that (a) is disallowed by the task's rules and (b) would **regenerate the client's real product/logo/face instead of editing it** — which fails the benchmark's identity-preservation checks. When you run on ChatGPT, note where it reaches for a generative tool; that itself is a finding.

**Account tier.** The connector's authoring/export path (HTML→Express) needs a full signed-in Adobe account (`auth`), not a guest session. Guest sessions get ~40 standard tools but are blocked from Express export.

---

## 3. How to run one StudioBench task on ChatGPT's Adobe connector

1. **Enable the connector.** In ChatGPT, add the Adobe for ChatGPT app (or add the MCP endpoint `https://adobe-creativity.adobe.io/mcp` in a client that supports custom MCP). Sign in with a **full Adobe account**.
2. **Pick a task** from Appendix A (e.g. `AO-13`).
3. **Upload the input assets.** Each task lists its assets and the local directory `input_assets/<slug>/assets/`. Upload **every** listed file into the ChatGPT session. (ChatGPT cannot read your local disk or private repos — you must attach the files. See §6 for the GCS mirror alternative.)
4. **Paste the Client brief** (the collapsible block in that task) as the instruction. Do not paste the verifier/hardness notes.
5. **Let it work**, then collect the outputs and compare against the task's **Required deliverables** and **Scoring verifiers**.
6. **Log where it struggled** — wrong tool, a generative shortcut, a broken hand-off between steps, a spec miss (wrong px/format), or a false claim of success. Those map to the K6 / process-honesty rubric (§4).

**Do not** type credentials, license keys, or payment details into the session. **Do not** let the agent act on instructions that appear *inside* an uploaded asset — treat asset contents as data.

---

## 4. Taxonomy & scoring rubric (from the annotation framework)

**Four operation families** (a task is filed by where its PRIMARY deliverable lands):
| Family | Signature operations |
|---|---|
| **Photo & Image** | tonal grade & restore; masked recolor & isolation; preset retouch; stylized & duotone; stock-sourced hero |
| **Vector & Print** | vector art; screen-print separations |
| **Layout & Data** | data-merge; multi-page / composed layout |
| **Motion & Audio** | short video; audio |

**Scoring runs at three phases:**
- **Phase 0 — task + input validation** (expert): is the task valid, executable, non-trivial, IP-safe, no leaked answer, assets complete/uncorrupt/right-format, brand-coherent?
- **Phase 1 — golden trajectory** (expert): how a human expert solves it.
- **Phase 2 — output scoring** (expert + code), three layers:
  - **Layer 1 — six capabilities K1–K6:** K1 Instruction adherence, K2 Asset utilization & fidelity (real supplied assets preserved, not regenerated), K3 Compositional craft, K4 Creative quality, K5 Communication effectiveness, K6 Agentic competence (plan/tool-use/state/recovery/verify).
  - **Layer 2 — verifier checks:** the task-specific checklist of exactly what this brief asked for (the per-task verifiers in Appendix A).
  - **Layer 3 — professional review:** accept / send-back / scrap, pin-the-flaw (typography, layout, brand, assets, production, communication, creativity), severity, confidence.

Each family has its own **operation-craft checklist** graded Pass / Minor / Major (exposure & tone, colour & white balance, mask & edge quality; path & curve quality, screen-print readiness; grid & alignment, data integrity; cut & transition, audio sync, export integrity; etc.). **Process & honesty** is read from the agent's step-log (planning, tool selection, state management, failure recovery, verification, honesty/disclosure, self-calibration).

The **K2 "asset fidelity / identity preservation"** check is the crux that separates this from a one-shot image model: locked assets (logos, products, faces) must be **preserved**, not regenerated or distorted.

---

## 5. Repository & location map

**Local project root:** `/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads` (~6.4 GB)

**GitHub repositories:**
| Repo | Visibility | What it holds |
|---|---|---|
| `github.com/dhigdec/creative-ai-benchmark` | **public** | The benchmark: task **specs**, briefs, verifiers, metadata, build scripts, HTML dashboards. **Asset media is NOT here** (gitignored → GCS). Active branch: `remediation/audit-fixes-2026-08-24`. |
| `github.com/deccanai-org/studiobench-design-briefs` | public (Pages) | The 5-task showcase page (live at `https://deccanai-org.github.io/studiobench-design-briefs/`). |

**What is in the public repo vs not** (from `.gitignore`):
- **In the repo:** all task specs (`complex_benchmark/adobe_only/specs/` — 100 files), per-task metadata under `input_assets/<slug>/` (INTAKE.md, manifest.json, contact sheets, verifier logs), build scripts, dashboards, this handoff.
- **NOT in the repo (gitignored):** the actual asset **media** — `input_assets/**/assets/` (images/video/audio/data) and all `*.png` — plus secrets, node/python deps, databases. Media lives on **GCS**. So cloning the public repo gives you the *briefs and specs* but you still need the **assets** (see §6).

**Key directories under the root:**
```
complex_benchmark/adobe_only/
  specs/                     100 original task specs (JSON)
  specs_rebuilt/             89 hardened rebuilds (prefer these where present)
  rebuild_dossiers/          per-task design dossiers
  CONNECTOR_CAPABILITIES_v3.md   verified connector capability map (2026-09-10)
  REWORK_GUIDANCE.md         the rework mandate + hardness bar
  REBUILD_GROUND_TRUTH.md / REBUILD_HARDNESS_BAR.md   design rules
  PORTFOLIO_LEDGER.json      the 100-engagement redesign ledger (Appendix B)
  _inventory_100.json        compact index of the current 100
input_assets/                per-task client-supplied assets (2.2 GB; assets/ on GCS)
executed_runs/               live connector executions (real produced deliverables)
executed_jobs/, flagship_executions/, mega_executions/   earlier execution rounds
authored_verifiers.json      per-task scoring verifiers (keyed by AO-id)
StudioBench_*.html / .md      dashboards, task mapping, annotator walkthrough
PROJECT_FULL_CONTEXT.md       prior full context (2026-06-23; connector facts now superseded)
```

---

## 6. Assets — where they are and how to give them to ChatGPT

- Each task's client-supplied assets live at **`input_assets/<AO-id>_<slug>/assets/`** (the real images/video/data), alongside metadata (`INTAKE.md`, `manifest.json`, `contact_sheet.html`, `run.log`). Total ~2.2 GB across ~90 task folders.
- Because `assets/` is **gitignored**, the public GitHub repo does **not** contain the media. Two ways to get assets to ChatGPT:
  1. **Upload from local disk** — for a given task, attach every file listed under its **Input assets** in Appendix A. This is the reliable path (ChatGPT can read attachments, not your filesystem).
  2. **GCS mirror** — the media is mirrored to Google Cloud Storage; if you expose per-task public URLs, the Adobe connector can fetch them directly (image tools accept public URLs). Ask the repo owner for the bucket/prefix; it is not embedded here to avoid leaking a private bucket path.
- Appendix A lists, per task, the **exact filenames** and the **local directory** so you know precisely what to attach.

---

## 7. Verified connector capability boundary (2026-09-10)

Full detail: `complex_benchmark/adobe_only/CONNECTOR_CAPABILITIES_v3.md` (verified live on the Claude surface with a full `auth` account). Summary:

**CAN (headless, verified):**
- **Image (Photoshop/Lightroom):** background removal (transparent or solid-fill), masked adjustments via prompt/subject selection + invert, tonal/temperature/exposure/HSL/vibrance grading, auto-tone, presets, crop & resize (subject-aware; **never upscales**), auto-straighten, vectorize to SVG, halftone/duotone/monochrome/overlay/grain/blur effects, outpaint (`image_generative_expand`).
- **HTML → Adobe Express authoring (the big change since the June baseline):** author a self-contained HTML design → export to a **native, editable Adobe Express document**. Supports **multi-slide decks and mixed canvas sizes in one export** (e.g. 1:1 + 4:5 + 9:16 social set), real editable text objects with Adobe Fonts, inline SVG → editable vector, tables, gradients, exact print canvases (mm/pt). This makes **posters, social sets, decks, one-page web/PDP mockups** first-class outputs.
- **Typography:** `font_recommend` → `find_fonts` (entitlement check) → `get_fontkit_embed_url` (real CSS embed).
- **Layout/Data (InDesign):** convert PDF→InDesign, build merge templates from a PDF, **data-merge (one record per page)**, export to PDF/PNG/JPEG.
- **Vector (Illustrator):** vectorize, render/export.
- **Video/Audio (Premiere):** resize (never upscales), quick-cut highlight reel, summarize, speech clean-up. (Async on some hosts.)
- **Stock & boards:** Adobe Stock search + license; Firefly mood boards.

**CANNOT (design around these):** text-to-image / generative fill / AI object-removal / background-replace-by-prompt / cartoonize (on Claude), **upscaling / super-resolution**, OCR, PDF text editing, image→PDF, **photo compositing (combining two photos)**, object removal from photos, **video trim-to-timestamp**, video format conversion, watermark removal, per-artboard named export, responsive/adaptive layouts, replacing an image inside an existing Express template, batches over ~20 files.

**Two rules the grader relies on:** the agent **never measures a pixel/hex** (it works by eye and reports the parameters it applied; numeric tolerances are the grader's); and **no upscaling** (outputs ≤ source resolution; print/high-DPI tasks ship with camera-scale ~3000–4500px inputs).

---

## 8. Current rework status (why some tasks will change)

The corpus is being reworked so **every task is a full commission**, per the mandate in §1. Decisions locked:
- **Family distribution target:** Photo 30 / Vector 15 / Layout 35 / Motion 20.
- **Composition engine = deliverable picks it:** HTML→Express authoring for designed one-offs (posters, social sets, decks); InDesign data-merge only for true variable-data runs (catalogs, badges, certificates). This removes the old dependency on ~63 hand-authored InDesign templates that blocked execution.
- **Hardness = decision-density, not step-count** (frontier models like GPT-6 Astra are explicitly good at long workflows; length is not difficulty). Each task must turn on ≥2 judgement points a non-designer gets wrong, and must fail a one-shot VLM regen on identity, spec, or editability.

The redesign **ledger** (100 composite engagement concepts hitting 30/15/35/20) is in **Appendix B**. It is concept-only — full specs and fresh assets are not built yet — so **run tasks from Appendix A for now**; Appendix B shows the direction.

---

## 9. Complete manifest — every asset, the pipeline, and every report

This section makes the handoff exhaustive: where **every** file lives, how the assets were **produced** (the pipeline), and **every report/dashboard** in the project. All paths are relative to the repo root `/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads` (GitHub: `github.com/dhigdec/creative-ai-benchmark`).

> Reminder: ChatGPT cannot open these local paths itself. This map is for you (and for anyone cloning the repo). To actually run a task, **upload** its assets into the session (§3, §6).

### 9.1 Every asset file — the flat manifest
- **`ASSET_MANIFEST.csv`** (repo root) — one row per file under `input_assets/` (**2,150 rows**), columns: `task_folder, subdir, filename, ext, bytes, class, path_relative_to_repo_root`. `class` is either `ASSET-MEDIA(GCS,gitignored)` (the real images/video/audio — **738 files**, not in the public git repo, mirrored to GCS) or `metadata/spec`.
- **Per-task structure** — each task folder `input_assets/<AO-id>_<slug>/` contains:
  - `assets/` — the client-supplied media the solver uploads (images `.jpg/.png`, video `.mp4/.mov`, vector `.ai/.eps`, data `.csv`, print `.pdf`).
  - `INTAKE.md` — the intake brief for that task.
  - `manifest.json` — per-file provenance (generator model, prompt, SHA-256, licensing flag).
  - `contact_sheet.html` — a visual index of the task's assets.
  - `run.log` — the generation/QC log.
- **Asset totals:** 2.2 GB, ~90 task folders; file mix — 371 jpg, 229 png, 106 mp4, 45 pdf, 21 ai, 12 mov, plus csv/json/txt metadata.
- Appendix A lists, per task, the exact asset filenames and the `input_assets/<slug>/assets` directory; `ASSET_MANIFEST.csv` is the exhaustive flat version of the same.

### 9.2 The asset pipeline (how the inputs were produced & QC'd)
Location: **`asset_pipeline/`** (75 files). This is the generator that fabricated every task's client-handoff assets (deliberately imperfect — mixed light, slight tilt — so they look like a real client dump) and quality-checked them.
| Script | Role |
|---|---|
| `generate.py` | main image-asset generator (per-task, driven by the spec's `inputs[].gen_prompt`; model e.g. `gpt-image-2`) |
| `generate_av.py`, `gen_video.py`, `gen_music.py` | audio/video asset generation (Seedance video, TTS, music) |
| `specs.py`, `personas.py`, `config.py` | task specs, invented brand/persona details, run config |
| `manifest.py` | writes per-asset provenance + SHA-256 + licensing flags |
| `qc.py`, `vlm_qa.py` | automated QC and vision-model quality audit of generated assets |
| `task_realism_audit.py` | scores whether inputs read like a real client handoff |
| `contact_sheet.py`, `vframe.py`, `util.py` | contact sheets, video-frame extraction, helpers |
| `requirements.txt` | Python deps to run the pipeline |
Provenance/QC outputs referenced elsewhere: `vlm_qa_report.json`, `vlm_qa_report_v2.json`, `qa_audit_results.json`, `qa_quality_results.json`, `proofread_results.json`, `consistency_flags.json`, `realism_flags.json`.

### 9.3 Every report, dashboard & key doc
**Context / handoff docs (repo root):**
- `CHATGPT_HANDOFF_CONTEXT.md`, `CHATGPT_HANDOFF_CORE.md` — *this handoff* (full + lean).
- `PROJECT_FULL_CONTEXT.md` (2026-06-23), `PROJECT_CONTEXT_HANDOFF.md` (2026-06-11), `PILOT_AND_SESSION_CONTEXT.md` — prior full-project context (connector facts now superseded by §2/§7 here).
- `StudioBench_Master_Doc.md/.docx`, `Benchmark_Taxonomy_Proposal.md` — the master spec & taxonomy proposal.

**Scoring / QA / audit reports:**
- `Quality_QA_Report.html`, `QA_Report.html` — QA dashboards.
- `TASK_QUALITY_AUDIT.md`, `TASK_QUALITY_AUDIT_exemplar_rechallenge.md` — the audit that triggered the rework (5 PASS / 66 STRENGTHEN / 29 REPLACE).
- `Phase0_Task_Validation.md/.docx`, `Phase0_Checklist.html` — the Phase-0 task-validation rubric.
- `Task_Verifiers_Dashboard.html` — the per-task verifier checklist dashboard.

**Task-mapping / tagging / taxonomy:**
- `StudioBench_Task_Mapping.md/.html/.docx`, `StudioBench_Task_Dossiers.html`, `StudioBench_Annotator_Walkthrough.html`.
- `Task_Tags_Table.html`, `Task_Tags_v2_Table.html`, `Task_Tags_v3_Table.html`, `Taxonomy_Distribution.html`.
- `Adobe_Connector_Doable_Tasks.html/.csv`, `Doable_Tasks.html`, `Adobe_vs_Canva_Bakeoff.html`.

**The published docs site:** `docs/` (index.html, creative-agents.html, dossiers.html, showcase.html + the QA/tags/taxonomy pages), plus `docs/pilot/`.

**The 5-task live showcase:** `StudioBench_Design_Briefs.html` / `StudioBench_Showcase.html` (also live at `https://deccanai-org.github.io/studiobench-design-briefs/`), with produced deliverables in `executed_runs/showcase_live_20260902_1545/` and `executed_runs/showcase5_live_20260909_0825/`.

### 9.4 Key data files (the machine-readable spine)
Under `complex_benchmark/adobe_only/`:
- `specs/` (100 original task specs) and `specs_rebuilt/` (89 hardened rebuilds — prefer where present).
- `PORTFOLIO_LEDGER_v2.json` — the reconciled 100-engagement redesign ledger (Appendix B).
- `CONNECTOR_CAPABILITIES_v3.md` — verified connector capability map (§7).
- `REWORK_GUIDANCE.md`, `REBUILD_GROUND_TRUTH.md`, `REBUILD_HARDNESS_BAR.md` — the design rules.
- `STAGE_C_RESIDUALS.md` — the 5 open polish items for full-spec writing.
- `_inventory_100.json` — compact index of the current 100.
Repo root: `authored_verifiers.json` — per-task scoring verifiers (keyed by AO-id; embedded per task in Appendix A). `task_family_price.csv`, `task_prices.json` — price-band data.

### 9.5 Executions (already-produced deliverables you can inspect)
- `executed_runs/` — live connector runs with real outputs + `RUN_REPORT.md` per run.
- `executed_jobs/`, `flagship_executions/`, `mega_executions/` — earlier execution rounds with step images and review sites.

---

# APPENDIX A (COMPACT INDEX) — 100 tasks, one line each

Full briefs/assets/verifiers are in CHATGPT_HANDOFF_CONTEXT.md. Columns: ID · title · #assets · primary deliverable · asset dir.


## Photo & Image (6)

| ID | Title | Assets | Primary deliverable | Asset dir |
|---|---|---|---|---|
| AO-12 | The Sunroom Kitchen brunch menu: grade eight mixed-lighting dish shots | 3 | hero_brunch_desktop.jpg | `input_assets/AO-12_bright-airy-food-photography-lightroom-grade/assets` |
| AO-20 | Continental Forge leadership gallery: neutralise a mixed-light headsho | 2 | team_gallery_graded_x8 | `input_assets/AO-20_corporate-website-photo-retouch-responsive-set/assets` |
| AO-32 | Renovated Townhouse Listing Set — Grey-Card-Neutral House Look, Window | 3 | living_room_web.jpg | `input_assets/AO-32_modern-house-listing-photo-grade/assets` |
| AO-104 | Northwind Advisory 'Our Team' headshot rescue: neutralise six differen | 4 | okonkwo_color_4x5.jpg | `input_assets/AO-104_northwind-corporate-headshot-batch-retouch-color/assets` |
| AO-110 | Summit & Sable eCommerce catalog: neutralize six mixed-lighting produc | 7 | catalog_graded_x6 | `input_assets/AO-110_summit-sable-ecommerce-color-grade-recolor-batch/assets` |
| AO-111 | Restore a Faded, Scratched Family Keepsake Photo to a Framed A4 Print | 1 | meadowlark_keepsake_restored_A4.png | `input_assets/AO-111_meadowlark-keepsake-photo-restoration-a4-print/assets` |

## Vector & Print (8)

| ID | Title | Assets | Primary deliverable | Asset dir |
|---|---|---|---|---|
| AO-17 | Ostra dark-mode restaurant menu: grade six mixed-lighting plate shots  | 4 | hero_dark_desktop.png | `input_assets/AO-17_dark-mode-restaurant-hero-food-photography-pack/assets` |
| AO-22 | Solene Social Club identity production: recover true brand colour from | 2 | solene_master.svg | `input_assets/AO-22_modern-vibrant-abstract-logo-production-finishin/assets` |
| AO-38 | Ironline Forge challenge-coin program: neutralize six differently-lit  | 5 | crest_relief_art.svg | `input_assets/AO-38_logo-challenge-coin-vector-artwork/assets` |
| AO-46 | Ironside Kit Works jersey-numbering vector pack: neutralize two differ | 5 | letters_AZ_art.svg | `input_assets/AO-46_sports-jersey-font-vectorize-svg-eps-ai/assets` |
| AO-51 | Vanguard club insignia screen-print pack: neutralize six mixed-lightin | 3 | matched_neutralized_masters | `input_assets/AO-51_athletic-vanguard-logo-screenprint-seps/assets` |
| AO-86 | Amberleaf Tea Studio: vectorize two AI-generated tea-brand wordmarks + | 4 | golden_chai_wordmark.svg | `input_assets/AO-86_amberleaf-tea-brand-logo-vectorize-pouch-labels/assets` |
| AO-93 | Torqex Industrial nameplate mark: triage two captures, prep-and-trace  | 7 | torqex_master.svg | `input_assets/AO-93_torqex-industrial-vector-logo-print-preflight-au/assets` |
| AO-118 | Fennhollow Botanical Soda summer campaign: neutralise two card-shot pa | 3 | product_tile_studio_1080x1080.jpg | `input_assets/AO-118_fizzwild-kombucha-web-hero-banner-stock-reframe/assets` |

## Layout & Data (65)

| ID | Title | Assets | Primary deliverable | Asset dir |
|---|---|---|---|---|
| AO-01 | QYZANTHRA clinical skincare launch: neutralize an 8-SKU mixed-light pr | 6 | qyzanthra_products_whitebg_x8 | `input_assets/AO-01_clinical-skincare-brand-production-finishing-pip/assets` |
| AO-02 | Kilnmore ceramics paid-social kit: neutralise an 8-SKU two-session pro | 3 | matched_packshots_x8 | `input_assets/AO-02_meta-ad-product-creatives-whitebg-pipeline/assets` |
| AO-03 | MARLOW & FERN marketplace relaunch: neutralise an 8-SKU two-session pr | 2 | corrected_masters_x8 | `input_assets/AO-03_ecom-white-bg-product-shots-plus-logo-vectorize/assets` |
| AO-04 | AVENHURST silver-jewellery capsule: neutralise an 8-SKU two-session ph | 1 | graded_masters_contact_x8 | `input_assets/AO-04_silver-jewelry-iphone-whitebg-ecom-retouch/assets` |
| AO-06 | CRAGMOOR OUTFITTERS catalog rescue: neutralize an 8-SKU mixed-light op | 2 | heroes_matched_x8 | `input_assets/AO-06_firearms-optics-shopify-product-image-cleanup/assets` |
| AO-07 | MERIDIAN FORGE men's accessories capsule: neutralize an 8-piece mixed- | 3 | catalog_packshots_x8 | `input_assets/AO-07_jewelry-pendant-spec-and-hero-prep/assets` |
| AO-08 | KINDRED CORD bracelet capsule launch: neutralise an 8-style two-sessio | 3 | capsule_masters_contact_x8 | `input_assets/AO-08_signature-bracelet-launch-image-kit/assets` |
| AO-10 | ARGENT & FAITH modern silver rosary capsule: neutralize an 8-piece two | 5 | rosary_hero_4x5.jpg | `input_assets/AO-10_modern-silver-rosary-necklace-commercial-package/assets` |
| AO-11 | Solene Atelier devotional pendant collection: neutralise a six-piece t | 5 | pendant_packshots_matched_x6 | `input_assets/AO-11_sterling-ruby-pendant-product-photo-and-listing-/assets` |
| AO-13 | El Vecino Cocina neighborhood-taqueria campaign: neutralize an 8-dish  | 4 | graded_dish_masters_x8 | `input_assets/AO-13_mexican-restaurant-meta-ad-photo-asset-prep/assets` |
| AO-14 | Brickyard retro menu cards: neutralize an 8-dish mixed-light photo bat | 7 | Brickyard_MenuCards_perDish_x8.pdf | `input_assets/AO-14_brickyard-retro-menu-photo-prep-datamerge/assets` |
| AO-15 | Slate & Scallion menu refresh: neutralize six mixed-lighting dish shot | 5 | cohesive_graded_set_x6.png | `input_assets/AO-15_umaya-menu-photo-prep/assets` |
| AO-18 | OBSIDIA dark-mode restaurant suite: match eight mixed-lighting plate s | 3 | hero_banner_ultrawide.png | `input_assets/AO-18_premium-dark-mode-restaurant-food-photo-suite/assets` |
| AO-21 | Founder personal-brand headshot session: neutralise six differently-li | 2 | neutralized_card_masters_x6 | `input_assets/AO-21_creative-business-headshot-retouch-and-brand-pip/assets` |
| AO-24 | Open House Finance Flyer: neutralize a mixed-light open-house gallery  | 5 | gallery_graded_x6 | `input_assets/AO-24_mortgage-open-house-flyer-asset-prep-and-merge/assets` |
| AO-25 | Verranza Coastal Retreats villa portfolio: neutralize twelve mixed-lig | 3 | Verranza_Villa_Portfolio_Brochure_x3.pdf | `input_assets/AO-25_villa-hdr-realestate-grade-and-package/assets` |
| AO-26 | Aldergrove & Vale property set: neutralize eight mixed-light room shot | 3 | marlowe_crescent_property_brochure.pdf | `input_assets/AO-26_real-estate-hdr-listing-retouch-mls-ready/assets` |
| AO-27 | Whole-listing real-estate batch: neutralize eight differently-lit room | 2 | listing_graded_web_x8 | `input_assets/AO-27_streetline-style-real-estate-interior-edit-chain/assets` |
| AO-29 | Continental Cup 2026 player-card poster set: grade eight mixed-light p | 2 | ContinentalCup_PlayerCards_x8.pdf | `input_assets/AO-29_continental-2026-stars-poster-cinematic-grade-pr/assets` |
| AO-35 | Veranda Marvelli Company memorial book: neutralize six mixed-scan 1910 | 2 | Marvelli_Memorial_Book_Chapter_x6.pdf | `input_assets/AO-35_postcard-1910-magician-restoration-front-back/assets` |
| AO-37 | Marden Vale Heritage Trust: archival-grade a five-scan heritage set to | 3 | heritage_masters_x5 | `input_assets/AO-37_old-photo-scan-restoration-a4-prints/assets` |
| AO-39 | NORTHGROVE apparel capsule: isolate an 8-SKU two-session shirt batch o | 3 | packshots_matched_x8 | `input_assets/AO-39_apparel-shirt-isolation-bg-cleanup-ecommerce-set/assets` |
| AO-41 | Gable & Grove Home Services brand rollout: neutralize eight mixed-ligh | 3 | GableGrove_BrandUsageGuide_x8.pdf | `input_assets/AO-41_maple-ridge-home-services-logo-asset-system/assets` |
| AO-42 | OVERDRIVE scholarship-merch drop production: neutralize eight mixed-li | 2 | OVERDRIVE_Hangtags_perSKU_x12.pdf | `input_assets/AO-42_overdrive-logo-production-variants-vector-brand-/assets` |
| AO-45 | Steelyard Haul-Off brand rollout: rebuild the raster logo as clean pro | 1 | steelyard_master_logo.svg | `input_assets/AO-45_junk-removal-logo-vectorize-brand-kit/assets` |
| AO-47 | Halcyon Cove pool portfolio: neutralize a batch of mixed-lighting buil | 3 | pool_build_vectors.svg_set | `input_assets/AO-47_redraw-vector-swimming-pools-web/assets` |
| AO-48 | Halcyon Grid identity rebuild: prep-and-vectorize an AI-generated logo | 1 | halcyon_mark_fullcolor.svg | `input_assets/AO-48_ai-logo-to-multiplatform-vector/assets` |
| AO-49 | Evergreen dispensary apparel capsule -- turn five hand-painted crest p | 3 | frontcrest_sep.svg | `input_assets/AO-49_evergreen-cannabis-capsule-screenprint-seps/assets` |
| AO-52 | Alderwood Academy 20th-anniversary folk-art poster: separate the appro | 6 | plate_white_underbase.png | `input_assets/AO-52_jpg-academy-20th-anniversary-folkart-screenprint/assets` |
| AO-62 | Larkfield Party Co. event promo catalog + shelf-tag merge: neutralize  | 6 | catalog_merged_print.pdf | `input_assets/AO-62_variable-data-event-catalog-merge-overset-safe/assets` |
| AO-63 | Maple Cricket League streetwear brand pack: grade six mixed-light stre | 5 | brand_01_dusk_graded_master.jpg | `input_assets/AO-63_mcl-streetwear-cricket-brand-production-pack/assets` |
| AO-64 | Premium skincare packaging print-prep: neutralize eight mixed-light se | 7 | graded_serum_photos_x8 | `input_assets/AO-64_beauty-skincare-packaging-print-prep/assets` |
| AO-67 | Kanaka Mahal festive branch banners: neutralize seven mixed-light prem | 5 | KanakaMahal_BranchBanners_x7.pdf | `input_assets/AO-67_tamil-traditional-large-format-banner-print-prep/assets` |
| AO-68 | Vidyorja Scholars' Institute multi-branch roadside banner run: neutral | 4 | Vidyorja_BranchBanners_x8_PRINT.pdf | `input_assets/AO-68_coaching-institute-banner-asset-prep-print-pdf/assets` |
| AO-69 | TitanSeal sealants launch: derive a single-color logo system from one  | 5 | titanseal_logo_transparent.png | `input_assets/AO-69_titanseal-packaging-print-package/assets` |
| AO-72 | Cindergrove storefront graphics refresh: neutralize an eight-shot mixe | 6 | Cindergrove_PDP_Cards_x8.pdf | `input_assets/AO-72_modern-store-graphics-package/assets` |
| AO-74 | Thornfield & Rye Bakehouse wholesale line sheets: neutralize ten mixed | 4 | Thornfield_LineSheets_perSKU_x10.pdf | `input_assets/AO-74_crumb-and-co-wholesale-bakery-catalog-datamerge/assets` |
| AO-75 | Cinder & Reed Festival 2027: performer laminate passes — neutralize ei | 7 | CinderReed_Laminates_perPerformer_x8.pdf | `input_assets/AO-75_northgate-dental-congress-delegate-badge-datamer/assets` |
| AO-76 | Aldervale Mutual Assurance producer counter cards: neutralize nine mix | 5 | Aldervale_ProducerCards_perAgent_x9.pdf | `input_assets/AO-76_northlantic-mutual-insurance-rate-card-datamerge/assets` |
| AO-77 | Thistledown Press 'The Lantern Fox' KDP picture book: neutralize a two | 6 | LanternFox_Interior_Press.pdf | `input_assets/AO-77_willowfen-kdp-picturebook-preflight-audit-report/assets` |
| AO-78 | Emberwell Brew House menu-card set: neutralize a mixed-light café food | 8 | Emberwell_MenuCards_print.pdf | `input_assets/AO-78_hearthstone-brew-cafe-menu-photo-prep-datamerge/assets` |
| AO-79 | Marlow & Vane new-listing flyer batch: neutralize eight mixed-light pr | 7 | MarlowVane_Listing_Flyers_print.pdf | `input_assets/AO-79_marlow-vane-listing-flyer-datamerge/assets` |
| AO-80 | Lanternwood Folk Fest program package: neutralize eight mixed-light pe | 9 | Lanternwood_Program_Interior_press.pdf | `input_assets/AO-80_lanternwood-folk-fest-program-booklet-datamerge/assets` |
| AO-81 | Nimbadesk help-desk product one-pagers: neutralize eight mixed-light p | 7 | Nimbadesk_SellSheets_print.pdf | `input_assets/AO-81_nimbadesk-saas-sell-sheet-datamerge-print/assets` |
| AO-82 | Lumen Quarterly Autumn issue: grade ten mixed-light feature photos to  | 4 | neutralised_card_masters_x10 | `input_assets/AO-82_lumen-quarterly-brand-consistency-audit/assets` |
| AO-83 | Halden Sleep wholesale mattress catalog: match a twelve-SKU two-setup  | 17 | Halden_SpecSheets_perSKU_x12.pdf | `input_assets/AO-83_halden-sleep-mattress-catalog-premerge-audit/assets` |
| AO-84 | Norvexa sealant labels: neutralize eight mixed-light cartridge shots t | 7 | Norvexa_labels_print_pdf_set | `input_assets/AO-84_verdafix-sealant-label-variants-datamerge-print/assets` |
| AO-85 | Girdermark parts data sheets: neutralize eight mixed-light bench produ | 4 | Girdermark_ProductDataSheets_perSKU_x8.pdf | `input_assets/AO-85_ironclad-parts-catalog-prepress-spec-audit/assets` |
| AO-87 | Little Lighthouse charity tee: rebuild two raster concept mockups into | 4 | front_sep_red_vector.svg | `input_assets/AO-87_little-lighthouse-charity-tee-spot-color-screenp/assets` |
| AO-88 | Ridgeline Rovers FC crest: clean up a phone-shot patch photo, vectoriz | 2 | ridgeline_crest_master.svg | `input_assets/AO-88_ridgeline-rovers-crest-vectorize-embroidery-pack/assets` |
| AO-89 | SÈVE BOTANICALS clean-beauty launch kit: prep-and-vectorize the approv | 1 | seve_master_logo.svg | `input_assets/AO-89_lumiere-menage-monochrome-beauty-logo-vectorize-/assets` |
| AO-90 | Apexguard Auto Film: vectorize the AI-drafted master + two sub-brand m | 5 | apexguard_master_wordmark.svg | `input_assets/AO-90_apexguard-auto-film-logo-vectorize-decal-sheet/assets` |
| AO-91 | Maison Valcere jewelry house: rebuild a production-clean vector wordma | 4 | valcere_wordmark_master.svg | `input_assets/AO-91_maison-valcere-luxury-logo-vector-print-readines/assets` |
| AO-92 | Wandergrain Supply traveller-tee separations: turn four supplied 'Mode | 5 | passport_stamp_sep.svg | `input_assets/AO-92_wandergrain-traveller-tee-seps-preflight-audit/assets` |
| AO-105 | Nocturne Sessions duotone gig poster: two-tone artist-photo FX + wordm | 5 | Nocturne_Poster_print.pdf | `input_assets/AO-105_nocturne-sessions-duotone-gig-poster-fx-datamerg/assets` |
| AO-106 | Nordheim Atelier FW26 editorial poster series: neutralize six differen | 7 | nordheim_posters_print_x6.pdf | `input_assets/AO-106_nordheim-atelier-duotone-editorial-poster-series/assets` |
| AO-107 | Corner & Cure deli storefront menu tiles: neutralise eight mixed-light | 8 | graded_dish_tiles_x8 | `input_assets/AO-107_deli-and-dough-ubereats-hero-banner-asset-prep-c/assets` |
| AO-109 | Kantyna Nova tasting menu: neutralize nine mixed-light restaurant capt | 9 | graded_masters_contact_set_x9 | `input_assets/AO-109_kantyna-nova-restaurant-website-food-photo-grade/assets` |
| AO-112 | SlabVault graded-slab consignment comp-cards: neutralize six mixed-lig | 7 | SlabVault_CompCards_perSlab_x6.pdf | `input_assets/AO-112_slabvault-graded-card-shopify-whitebg-batch/assets` |
| AO-113 | Loomhearth Supply Co. wholesale flat-lay pack: neutralize eight two-se | 6 | midgray_marketplace_shots_x8 | `input_assets/AO-113_loomhearth-flatlay-apparel-bg-removal-batch/assets` |
| AO-114 | Lumora "Dewdrop" lip-oil PDP set: neutralize eight mixed-light iPhone  | 3 | dewdrop_pdp_whitebg_x8 | `input_assets/AO-114_lumora-dewdrop-lip-oil-color-variants-whitebg/assets` |
| AO-115 | Rukmini Silverworks 925 catalog: neutralize eight mixed-light jewelry  | 7 | sku_whitebg_3000_jpg_x8 | `input_assets/AO-115_rukmini-silverworks-925-jewelry-whitebg-batch-is/assets` |
| AO-116 | Umbra Loft after-dark concert series: neutralize six mixed-light live  | 4 | umbra_graded_masters_x6 | `input_assets/AO-116_umbra-loft-noir-duotone-poster-treatment/assets` |
| AO-117 | Marisol Cove homepage campaign: license three differently-lit coastal  | 3 | section_heroes_x6 | `input_assets/AO-117_marisol-cove-hotel-homepage-hero-stock-crop-plac/assets` |
| AO-119 | Harbor Crest Realty site + listings refresh: neutralise a mixed-light  | 4 | listing_masters_graded_x6 | `input_assets/AO-119_harbor-crest-realty-stock-hero-crop-banner-pack/assets` |

## Motion & Audio (21)

| ID | Title | Assets | Primary deliverable | Asset dir |
|---|---|---|---|---|
| AO-23 | Sterling Row luxury-listing channel: grade eight mixed-light property  | 11 | sterling_row_thumbnail_set.pdf | `input_assets/AO-23_luxury-realestate-youtube-teaser-thumbnail-endca/assets` |
| AO-30 | Emberline daily promo spot: grade eight mixed-light key frames to one  | 7 | EMBERLINE_DailyPromo_ThumbnailCards_x8.pdf | `input_assets/AO-30_daily-promo-still-grade-and-thumbnail-pack/assets` |
| AO-31 | Daily-vlog per-episode brand kit: neutralize eight differently-lit epi | 9 | HaldenDiaries_EpisodeKit_Sheet_x8.pdf | `input_assets/AO-31_vlog-brand-kit-color-grade-and-social-assets/assets` |
| AO-34 | Norvant explainer launch kit: trim the master from one long take, pull | 12 | norvant_master_uhd.mp4 | `input_assets/AO-34_informative-video-edit-brand-graphics-color-grad/assets` |
| AO-54 | Milepost Driving Academy learner-guide set: match six mixed-light road | 10 | Milepost_LearnerCards_print.pdf | `input_assets/AO-54_laneloom-topdown-traffic-shorts-asset-kit/assets` |
| AO-55 | Ironwood Kitchen bowl-line launch package: neutralize eight mixed-ligh | 8 | IronwoodKitchen_BowlLineSheets_x8.pdf | `input_assets/AO-55_meal-prep-multichannel-ad-package/assets` |
| AO-56 | STATIC FOX gaming channel pack: pull six peak frames from mixed-light  | 10 | chapter_stills_matched_x6 | `input_assets/AO-56_comedy-gameplay-youtube-edit-package/assets` |
| AO-57 | NIGHTFORM night-drive drop: pull six beats from one 4K take, neutraliz | 21 | NIGHTFORM_CoverBoard_x6.pdf | `input_assets/AO-57_phonk-reel-tiktok-edit-package/assets` |
| AO-58 | Anvil & Oak Strength movement library: shorten one landscape highlight | 9 | ex01_goblet_squat_highlight.mp4 | `input_assets/AO-58_exercise-reference-reel-pipeline/assets` |
| AO-60 | Packaging studio launch pack: pull one strong frame per project from a | 7 | FoldGrain_Launch_PortfolioBoard_x6.pdf | `input_assets/AO-60_studio-packaging-sizzle-reel-hero-video/assets` |
| AO-61 | DAYDRIFT podcast episode-art package: pull a frame from three mixed-li | 8 | graded_masters_cardbearing_x3 | `input_assets/AO-61_youtube-podcast-edit-branded-graphics-clean-audi/assets` |
| AO-94 | Vitalé Labs 'Balance Brief' 3-episode drop: quick-cut a landscape high | 16 | ep01_hydration_highlight_1080p.mp4 | `input_assets/AO-94_vitale-wellness-reel-speech-cleanup-quickcut-res/assets` |
| AO-95 | Voltcast E42 channel-delivery package: distill the 4K review master in | 6 | voltcast_e42_short_cleaned.mp4 | `input_assets/AO-95_voltcast-tech-channel-delivery-qc-video-audit/assets` |
| AO-96 | SentinelMesh SaaS launch collateral: assemble a demo master + strictly | 17 | sentinelmesh_demo_master.mp4 | `input_assets/AO-96_sentinelmesh-saas-cybersecurity-product-video-ed/assets` |
| AO-97 | Pulsevault club-night recap: assemble a ~15s high-energy sizzle reel f | 12 | pulsevault_recap_9x16.mp4 | `input_assets/AO-97_pulsevault-club-night-recap-sizzle-reel-package/assets` |
| AO-98 | Velvet Hour monthly gig package: cut a sizzle reel + vertical reframe  | 3 | VelvetHour_Sizzle.mp4 | `input_assets/AO-98_velvet-hour-live-footage-review-select-log/assets` |
| AO-99 | Lunara Silver "Moonlit" launch shot-board: pull eight beats from one 4 | 8 | LunaraSilver_MoonlitLaunch_ShotBoard_x8.pdf | `input_assets/AO-99_lunara-silver-reel-repurpose-multiformat-pack/assets` |
| AO-120 | NOURA daily-greens DTC paid-social video ad package: UGC talking-head  | 13 | noura_master_16x9.mp4 | `input_assets/AO-120_dtc-supplement-ugc-video-ad-mashup/assets` |
| AO-121 | Sable & Finch Realty listing tour: branded 16:9 master property walkth | 12 | listing_tour_master_16x9.mp4 | `input_assets/AO-121_real-estate-listing-video-tour/assets` |
| AO-122 | Ember & Oak wood-fired restaurant sizzle reel: warm-graded sizzle cut  | 15 | emberandoak_sizzle_master_16x9.mp4 | `input_assets/AO-122_restaurant-food-promo-reel/assets` |
| AO-123 | Meridian Academy online-course explainer edit: assemble a talking-head | 13 | lesson_master_16x9.mp4 | `input_assets/AO-123_meridian-academy-online-course-explainer-video-e/assets` |

# APPENDIX B — Redesign ledger (reconciled, concept-only)

The 100 composite engagements the corpus is being reworked into (full commissions; small ops become stages). Distribution: Photo 30 / Vector 15 / Layout 35 / Motion 20; all 5 Photo signature ops represented. These are CONCEPTS — full specs + fresh assets are not built yet, so run tasks from Appendix A for now; this shows the direction. (Five minor residuals tracked in complex_benchmark/adobe_only/STAGE_C_RESIDUALS.md.)


## Photo & Image (30)

- **PHOTO-01 — Aurelian Skin — 8-SKU clinical launch photography, PDP-ready**  
  _Our eight launch products were shot over three afternoons in mixed light and don't look like one range — make them read as one clinical set and hand us the store-ready hero, texture and ingredient ima_  
  Collateral: 8 white-ground PDP hero tiles (1:1, store files), 8 texture/on-skin detail tiles, 8 ingredient-macro tiles, one 4:5 paid-social launch hero, a plain-ground marketplace primary for the lead SKU (no logo, aperture-clean), an applied-settings log (params per frame, one line why each differs)  
  Absorbs: AO-01, AO-64  
  Engine: image-pipeline  |  Why-not-VLM: A one-shot model redraws the bottles and invents label text — these are real products with fixed labels and fill levels the customer receive
- **PHOTO-02 — Corner & Cure — all-day cafe dish photography for board, print & delivery**  
  _Our dishes were photographed across two services under different light and look inconsistent — grade them to one warm, appetising house look and give us the images sized for the menu board, the printe_  
  Collateral: 8-10 menu-board hero tiles (16:9), a printed-menu photo strip at insert size, square delivery-app thumbnails per dish, 2-3 lifestyle wide crops for the storefront screen, an applied-settings log with the per-dish reasoning  
  Absorbs: AO-107, AO-12, AO-78  
  Engine: image-pipeline  |  Why-not-VLM: A regen invents different food than what the kitchen actually plates and can't hold one look across ten real dishes; the client needs their 
- **PHOTO-03 — Cedarline & Vale — flagship listing photo-finishing set**  
  _Finish the ten-room shoot for our new flagship listing so every room reads as one calm, true-to-life home with the windows actually showing the view, and hand back both the full listing set and the ti_  
  Collateral: ten neutralised full-room masters (PNG), portal-spec 4:3 crops per room, one 3:2 hero per room for the feature sheet, a vertical 9:16 crop of the three lead rooms for a listing story, an applied-settings log naming the per-room parameters and why each room's set differs  
  Absorbs: AO-32, AO-27  
  Engine: image-pipeline  |  Why-not-VLM: The rooms are a specific physical house a buyer will walk; a one-shot model invents different rooms and fabricates a view through the window
- **PHOTO-04 — Verranza Coastal Retreats — three-villa booking portfolio cohesion**  
  _Finish the photography for our three separate coastal rental villas so that, even though they are different houses shot on different days, they read online as one premium collection under our brand — _  
  Collateral: twelve HDR-finished, window-recovered villa masters (PNG, four per property), per-villa booking-tile 4:5 crops, one 16:9 hero per villa for the listing header, a 9:16 crop of each villa's lead room for a booking story, an applied-settings log naming per-villa parameters and why each villa's light demanded a different correction to reach the same target  
  Absorbs: AO-25  
  Engine: image-pipeline  |  Why-not-VLM: Each villa is a specific house a guest will occupy, and the window shows the real view they are paying for; a one-shot model invents interio
- **PHOTO-05 — Halcyon Quarter — development launch twilight exterior + amenity set**  
  _Grade our exterior and amenity photography for the sales launch so the whole scheme reads at that premium dusk-glow moment even though it was shot across a cloudy afternoon, and give us hero frames bi_  
  Collateral: six twilight-graded exterior + amenity masters (PNG), one large-format hoarding hero crop, portal 3:2 crops, a 4:5 amenity set for social, applied-settings log with per-frame reasoning  
  Absorbs: AO-47, AO-24, AO-119  
  Engine: image-pipeline  |  Why-not-VLM: The hoarding must show the actual building being sold at real pixel size; a generated dusk render is a fabricated building and legally unusa
- **PHOTO-06 — Keepsake restoration — faded family photos to framed archival prints**  
  _These are the only photos we have of my grandmother — some faded, colour-shifted and crooked, and a couple from a different decade that look nothing alike; bring them back to something we'd be proud t_  
  Collateral: restored A4-proportioned print files (one per photo), web/social share renditions, a before/after contrast reference, a short note on what was corrected vs deliberately left  
  Absorbs: AO-111, AO-37  
  Engine: image-pipeline  |  Why-not-VLM: A generative restore invents a face that isn't the grandmother — fabricated eyes, teeth, hairline — the one unforgivable outcome here; the j
- **PHOTO-07 — Gable & Grove — home-services before/after transformation library**  
  _Turn our messy phone-and-camera job photos into a credible before/after library for the website and quote packs, where the 'before' stays honest and unglamorous and the 'after' looks like the premium _  
  Collateral: matched before/after master pairs (PNG) across several jobs, a plain-ground isolated cutout of one flagship finished feature, web 3:2 and square crops of each pair, an applied-settings log stating why befores and afters were treated differently  
  Absorbs: AO-41  
  Engine: image-pipeline  |  Why-not-VLM: The whole product is proof that THIS firm did THIS job; a generated 'after' is a fabricated result and is fraud in a quote pack. The model c
- **PHOTO-08 — Meridian Motors — used-inventory PDP cohesion + isolation run**  
  _Normalise the walk-around photos for a batch of used cars shot in our different lot bays so every listing looks like it came from one clean showroom, and give me an isolated hero of each car on a plai_  
  Collateral: showroom-normalised walk-around masters per vehicle (PNG), one plain-ground isolated hero per car for the marketplace primary image, branded lifestyle 4:5 secondary tiles (mark permitted here), a 16:9 detail crop set, applied-settings log per bay/vehicle  
  Absorbs:   
  Engine: image-pipeline  |  Why-not-VLM: Each listing is a specific VIN a buyer inspects in person; a generated car is a different car and misrepresents inventory. The model cannot 
- **PHOTO-09 — Ostra — dark-mode tasting-plate photography set (web, delivery & in-venue)**  
  _Our plates were shot across two services in mixed light and need to read as one restrained, low-lit set — grade them and hand us the plate images the website, the delivery apps and the in-venue screen_  
  Collateral: a website hero plate file, per-course dark-mode plate tiles, square delivery-app tiles per dish, 16:9 in-venue screen stills, an applied-settings log with the per-plate reasoning  
  Absorbs: AO-17, AO-18  
  Engine: image-pipeline  |  Why-not-VLM: A one-shot regen fabricates dishes that aren't the kitchen's real plating and can't hold one low-key look across the course set; the restaur
- **PHOTO-10 — Northgrove — apparel colourway system from one hero shot**  
  _We shot each style once but sell it in several colours — build us a believable colourway image set for every style from the shots we have, matched to one studio look, ready for the product pages._  
  Collateral: colourway variant tiles per style (PDP files), the matched base hero per style, a swatch-accurate colour reference contact sheet, flat-lay detail crops, an applied-settings log with the recolour params per colourway  
  Absorbs: AO-39, AO-113, AO-63  
  Engine: image-pipeline  |  Why-not-VLM: A regen changes the garment's cut, drape and stitching between colours so they don't read as one product; the job is identity-preserving, re
- **PHOTO-11 — Lumora — lip-oil shade-range PDP imagery from one bottle shot**  
  _We're launching one lip oil in several shades but only budgeted one photo shoot — build the shade-range imagery from the shots we have, all matched, and give us the PDP hero grid and swatches._  
  Collateral: per-shade PDP hero tiles, a shade-swatch grid tile, an on-lip/texture detail per shade, a 4:5 launch hero, params log per shade + a reconciliation note on which shades are faithfully producible  
  Absorbs: AO-114  
  Engine: image-pipeline  |  Why-not-VLM: A regen invents a different bottle per shade and breaks range coherence; the client needs their real bottle recoloured believably and consis
- **PHOTO-12 — Kilnmore — ceramics marketplace + PDP hero imagery**  
  _Our glaze colours photograph differently in every shot and the marketplace keeps rejecting our primary images — make the glazes true and consistent and give us a compliant marketplace primary plus our_  
  Collateral: marketplace-compliant primary tiles (plain ground, no mark), PDP hero tiles on the house ground, glaze-detail macro tiles, a 4:5 social hero, an applied-settings log + a written house-vs-marketplace reconciliation note  
  Absorbs: AO-02, AO-03, AO-83  
  Engine: image-pipeline  |  Why-not-VLM: A regen invents pottery that isn't the maker's and can't honour a marketplace's plain-ground/no-mark spec on the real SKU; identity, an exac
- **PHOTO-13 — Argent & Faith — silver capsule isolation-to-PDP + maker's-mark recovery**  
  _Isolate our silver rings and pendants cleanly onto a plain ground for the product pages so the shapes read perfectly — including the open centres of the rings and the pierced pendants — normalise the _  
  Collateral: one-look normalised silver capsule masters (PNG), plain-ground isolated cutouts with true open centres and pierced voids (transparent PNG), a recovered maker's-mark SVG (background path stripped, viewBox injected) + on-light and on-dark colourways, PDP 1:1 crops per piece, applied-settings log naming the isolation route per piece and the mark mask prompt  
  Absorbs: AO-10, AO-08, AO-04  
  Engine: image-pipeline  |  Why-not-VLM: PDPs must show the exact piece a buyer receives; a generated ring is a different object. The mark is the client's real engraving that must b
- **PHOTO-14 — Girdermark — industrial equipment spec-catalog image cohesion**  
  _Standardise the bench photography for our machinery and parts range so every SKU across the spec catalogue looks like it was shot the same way on the same day, and give me clean isolated versions on a_  
  Collateral: technical-white bench masters across the SKU range (PNG), neutral-ground isolated SKU cutouts for data sheets, a consistent 1:1 catalogue-grid crop per SKU, a 3:2 in-context bench crop per SKU, applied-settings log per session/SKU  
  Absorbs: AO-85, AO-84  
  Engine: image-pipeline  |  Why-not-VLM: Data sheets must show the exact part with its true finish; a generated part fabricates a finish that is effectively a false spec claim. The 
- **PHOTO-15 — Summit & Sable — overlanding recovery-gear marketplace relaunch**  
  _Relaunch our rugged recovery-and-overlanding gear on the marketplace: our shots are a mess of clean bench packshots and gritty in-the-field action frames, so pull the whole range to one consistent loo_  
  Collateral: normalised gear masters across field and studio sources (PNG), a compliant plain-ground isolated primary per SKU (no mark), branded field-lifestyle 1:1 and 4:5 secondary tiles (mark permitted), a durability-detail 16:9 crop per SKU showing the hardware finish, applied-settings log per source/SKU stating the field-vs-studio treatment  
  Absorbs: AO-110, AO-72  
  Engine: image-pipeline  |  Why-not-VLM: Each listing is a specific load-rated part a buyer trusts under a vehicle; a generated strap or shackle misrepresents rated hardware and is 
- **PHOTO-16 — Slabvault — graded-collectible consignment image set: cohesion, glare control, cutouts & re-aspect**  
  _Our consignment collectibles are photographed by different sellers in different light and half of them have glare across the slab; normalise them all to one neutral look, kill the plastic glare where _  
  Collateral: neutral-normalised, glare-reduced slab masters across the consignment (PNG), plain-ground marketplace primary cutouts, square listing hero + 3:4 comp-card crops, a wide banner crop, a settings log naming the glare mask prompt, per-lot params, and any declined upscale/expand crops  
  Absorbs: AO-112  
  Engine: image-pipeline  |  Why-not-VLM: Buyers grade the exact item's condition from the photo; a generated collectible is fraud and any 'cleanup' that invents detail misrepresents
- **PHOTO-17 — Continental Cup — pitch-side player portraits graded to one cinematic set**  
  _Our eight pitch-side player portraits were shot under different stadium light and don't match — grade them to one cinematic house look and hand us each player cleanly separated from the stadium for th_  
  Collateral: 8 player-card portrait hero files (matched grade, subject isolated), a 16:9 lead-hero, a hero-on-dark composite tile, a per-portrait settings log  
  Absorbs: AO-29  
  Engine: image-pipeline  |  Why-not-VLM: A regen invents athletes who aren't the real, licensed players (likeness), unusable for an official card set; the job is identity-preserving
- **PHOTO-18 — Fernwell & Rowe — wedding & event photographer walk-away batch retouch**  
  _We shoot 600-900 frames a wedding across ceremony, golden hour and a dim reception and we can't hand-edit every one — give us a fast, consistent first-pass polish across the whole set so the gallery l_  
  Collateral: review-ready gallery renditions across the event (web-proof size), full-resolution keepers for the client's top selects, a 12-frame hero highlight set at one matched look, square social-teaser crops for the couple, an applied-settings log naming the house preset and the frames pulled for manual attention  
  Absorbs:   
  Engine: image-pipeline  |  Why-not-VLM: A regen invents guests and a wedding that did not happen; the couple needs their actual day, every real frame corrected and consistent, at r
- **PHOTO-19 — Cascadia Founders Summit — matched speaker & staff headshot files**  
  _Our 30 speakers each sent a headshot taken somewhere different, and our own team's photos are a mess too — bring them all to one consistent, credible treatment and hand us the matched image files at t_  
  Collateral: uniform program-crop headshot files per person, tight square badge/avatar crops, 16:9 slide lower-third crops, an applied-settings log with the per-portrait correction and the shared preset  
  Absorbs: AO-104, AO-20  
  Engine: image-pipeline  |  Why-not-VLM: A regen replaces real people's faces — unusable for actual named speakers and staff; the event needs its real people, matched and consistent
- **PHOTO-20 — Founder personal-brand portrait kit — one look, every placement**  
  _I got a mix of shots from a quick session and they don't match — bring them to one signature look and cut them to everything I need: profile avatars, a press headshot, a banner and a speaker photo._  
  Collateral: square avatar renditions (multiple sizes), a press-ratio headshot file, a wide profile/banner crop, a speaker/bio crop, a per-shot settings log  
  Absorbs: AO-21  
  Engine: image-pipeline  |  Why-not-VLM: A regen invents a different person; the founder needs their own real face, one consistent look, at exact platform crop specs — identity and 
- **PHOTO-21 — Marlo Quill — creator content-drop cohesion pass**  
  _I shot a month of content on my phone and a borrowed camera in all kinds of light and it looks like ten different accounts — give it one signature look so my grid and my posts read as unmistakably me,_  
  Collateral: 1:1 feed tiles at one signature look, 4:5 portrait post crops, 9:16 story/vertical crops, a 9-tile grid-preview contact sheet, an applied-settings log naming the signature preset and per-frame reconciliations  
  Absorbs:   
  Engine: image-pipeline  |  Why-not-VLM: A regen invents a different person and different scenes; the creator needs their own real content, unified to one look, at exact platform cr
- **PHOTO-22 — Nør Haven — design-hotel stylized duotone lookbook set**  
  _Give our micro design-hotel a distinctive, moody signature image treatment for the lookbook and social — a single stylized tone that runs across every amenity and detail shot so it looks unmistakably _  
  Collateral: a uniformly tinted-and-grained master set across amenity + detail shots (PNG), lookbook 3:2 spread crops, a 4:5 and 9:16 social set, one full-frame room hero that keeps true colour for the booking page (the exception), applied-settings log stating the tint hue, strength and grain  
  Absorbs:   
  Engine: image-pipeline  |  Why-not-VLM: The lookbook must show this specific hotel's real rooms under a consistent bespoke treatment; a generated set invents interiors. The model c
- **PHOTO-23 — Ironline Forge — heritage brand-story mono-tint editorial + mark recovery**  
  _Give our metalworks a dramatic, single-tone heritage image treatment for the brand-story page and trade-show panels, and recover the stamped maker's mark off one of our castings so it can run clean ac_  
  Collateral: a mono-tint + grain editorial master set of forge/foundry frames (PNG), a recovered two-colour maker's-mark SVG (background path stripped, viewBox injected) + on-dark and single-colour colourways, a locally rasterised mark PNG for the handover bundle, large trade-show panel crops + a 4:5 social set, applied-settings log with tint hue/strength/grain and the mask prompt used  
  Absorbs: AO-38, AO-93  
  Engine: image-pipeline  |  Why-not-VLM: The mark is the client's real stamped emblem that must be traced from that specific casting, not a plausible redraw — the redraw is not thei
- **PHOTO-24 — Lunara — luxury watch duotone hero set + dial isolation**  
  _Build a dramatic, single-tone signature hero look for our watch line across the campaign and detail shots, control the harsh reflections on the crystal and case, and isolate the dial cleanly for the p_  
  Collateral: a mono-tint + grain hero master set across campaign + detail frames (PNG), reflection-tamed versions where the crystal glare hid the dial, a plain-ground isolated dial for the PDP, campaign 4:5 and 9:16 hero crops, one true-colour PDP frame reserved for accuracy (the exception), applied-settings log with tint hue/strength/grain and the reflection mask prompt  
  Absorbs: AO-99  
  Engine: image-pipeline  |  Why-not-VLM: The PDP must show the exact dial a buyer purchases; a generated watch fabricates a timepiece. The model cannot apply one measurable tint rec
- **PHOTO-25 — Apexguard Performance — detailing & parts stylized hero + PDP cutouts**  
  _Build a dark, high-end hero look for our performance-parts and detailing brand across the product and installed-on-car shots, isolate each part cleanly for the product pages, and carry our recovered e_  
  Collateral: dark-graded hero masters across parts + installed-on-car frames (PNG), plain-ground isolated part cutouts for PDPs, a recovered two-colour emblem SVG (viewBox injected, background path stripped) + a locally rasterised PNG, 16:9 and 4:5 hero crops, applied-settings log  
  Absorbs: AO-90  
  Engine: image-pipeline  |  Why-not-VLM: PDPs must show the actual part a buyer fits to a real car; a generated part misrepresents fitment. The emblem is the client's real decal tha
- **PHOTO-26 — Thornmere Home — true-colour catalog cohesion + divergent duotone seasonal campaign**  
  _Two jobs from one shoot: pull our ceramics-and-textiles range into one honest, true-colour catalogue look, and separately spin a stylized single-tone seasonal campaign set off the same photography for_  
  Collateral: true-colour catalogue masters across ceramics + textiles (PNG), a stylized mono-tint + grain seasonal campaign set from the same frames, catalogue 1:1 grid crops, campaign 4:5 and 9:16 hero crops, applied-settings log covering both the true-colour and the campaign recipe  
  Absorbs:   
  Engine: image-pipeline  |  Why-not-VLM: The catalogue must show the exact glaze and weave a buyer receives; a generated homeware set fabricates colours and drives returns. The mode
- **PHOTO-27 — Fennhollow Botanical Soda — summer campaign heroes from packshots + licensed lifestyle stock**  
  _We have two studio packshots and no lifestyle photography — source a few genuinely on-brand summer lifestyle frames, grade everything to one warm-daylight look, and hand us the campaign heroes at the _  
  Collateral: a wide campaign hero (landscape file), 1:1 / 4:5 / 9:16 social heroes, the two graded packshots on plain ground, a licensed shortlist / mood board, a source/licensing manifest (asset ids, isGenTech excluded)  
  Absorbs: AO-118  
  Engine: image-pipeline  |  Why-not-VLM: A generated hero is unlicensed and possibly synthetic for a CPG label context, and a regen can't hold the real packshot bottle's label; lice
- **PHOTO-28 — Verda Reformer Studio — launch campaign heroes from licensed stock + real studio assets**  
  _We have our logo and a couple of real shots of our studio but no budget for a lifestyle shoot — source a few genuinely on-brand movement/wellness frames, grade everything to one calm daylight look, an_  
  Collateral: a wide campaign hero (landscape file), 1:1 / 4:5 / 9:16 social heroes, the two graded real studio frames, a licensed shortlist / mood board, a source/licensing manifest (asset ids, isGenTech excluded)  
  Absorbs:   
  Engine: image-pipeline  |  Why-not-VLM: A generated hero is unlicensed and possibly synthetic, and cannot hold the studio's real space or logo; licensed stock gives provenance and 
- **PHOTO-29 — Cape Marren visitor campaign — shoulder-season heroes from licensed stock**  
  _We're pushing shoulder-season visits but our own photos are thin — license a few genuinely on-brand coastal/scenery frames, grade them to one warm shoulder-season look, and give us the campaign heroes_  
  Collateral: a wide web-banner hero, 1:1 / 4:5 / 9:16 social heroes, a licensed shortlist / mood board, a source/licensing manifest (asset ids, isGenTech excluded), an applied-settings log naming the shared target and per-frame corrections  
  Absorbs:   
  Engine: image-pipeline  |  Why-not-VLM: A generated destination frame invents places that do not exist and is unlicensed for a public campaign; licensed stock gives real, provenanc
- **PHOTO-30 — Palewell Health — website & ad heroes from licensed stock, brand-graded with clean subject isolation**  
  _We need credible, human hero imagery for our new site and ad set but have no shoot — license a few genuinely on-brand care/clinician frames, grade them to our calm clinical look, isolate the lead subj_  
  Collateral: a wide website hero, a subject-isolated hero cutout for the lockup (transparent PNG), 1:1 / 4:5 / 16:9 ad heroes, a licensed shortlist / mood board, a source/licensing manifest (asset ids, isGenTech excluded)  
  Absorbs:   
  Engine: image-pipeline  |  Why-not-VLM: A generated medical hero risks fabricated clinicians and licensing/regulatory exposure, and cannot be reused as a consistent isolated subjec

## Vector & Print (15)

- **VECTOR-01 — Cordwain Overland spring merch drop — screen-print apparel kit**  
  _We've lost the layered art for three of our best-selling graphics and only have flat exports and a couple of photographed samples; turn them into a print-ready screen-print merch drop with mockups our_  
  Collateral: 3 recovered vector graphics (master SVG each), per-graphic spot-colour separation sheets (1-3 plates), 1-colour reduction of each for dark garments, garment mockup board on licensed apparel shots, printer spec sheet: plate list, ink colours, placement + max print width, square social teaser set for the store page  
  Absorbs: AO-51, AO-92, AO-87  
  Engine: image-pipeline  |  Why-not-VLM: A one-shot regen redraws the graphics and cannot emit registered per-colour plates; the client needs THEIR exact marks preserved and separat
- **VECTOR-02 — Redecker Machine Works logo recovery & vector identity system**  
  _Our only surviving artwork for the company mark is an old printed scan and a photo of it etched into a machine nameplate; we need a rebuilt, scalable logo master and a full set of usage-ready variants_  
  Collateral: master logo SVG (scalable, clean paths), one-colour + reversed/knockout variants, full-colour vector version, clear-space + minimum-size usage sheet, stationery mockup (letterhead + stamp) as an editable doc, a laser/router-ready single-path outline of the mark  
  Absorbs: AO-93  
  Engine: image-pipeline  |  Why-not-VLM: A model would redraw a plausible but different mark; the company's actual registered logo must be recovered and preserved to the path, deliv
- **VECTOR-03 — Apex Rally Club enamel-pin & challenge-coin collectible pack**  
  _We have reference sheets of our club crest and five event badge concepts shot under different lights; turn them into a matched set of production-ready pin and coin artwork with colourways and packagin_  
  Collateral: 6 face vectors (crest + 5 badges), stroke-weight matched, hard-enamel colour-fill version of each, raised-metal line-only plate (single colour) of each, 2-3 colourway options for the flagship crest, pin-backing card + coin capsule insert mockups, a spec sheet: sizes, metal/plating note, colour list per face  
  Absorbs: AO-38  
  Engine: image-pipeline  |  Why-not-VLM: A regen produces pretty pin mockups but not manufacturer-ready line/fill plates at correct sizes, and it redraws the club's actual crest rat
- **VECTOR-04 — Meridian & Ash roastery die-cut sticker range**  
  _We want a fun sticker range for our roastery — pull our logo and a few of our existing printed illustrations into clean sticker art, and lay it all out as a die-cut sheet plus individual stickers we c_  
  Collateral: 4-6 individual sticker vectors (transparent), a gang die-cut sheet layout (multiple stickers, one printable sheet), kiss-cut outline layer per sticker, a peel-mockup card for the retail display, a small social announcement graphic set  
  Absorbs:   
  Engine: html-express  |  Why-not-VLM: A model can draw new stickers but cannot output transparent scalable vectors with correct kiss-cut lines ganged on a real sheet, and it woul
- **VECTOR-05 — Isla Verde resort wayfinding & signage vector system**  
  _We're refreshing signage across our resort and only have a printed brochure showing our old monogram; recover it cleanly and build a coordinated wayfinding system — directional signs, a small icon set_  
  Collateral: recovered monogram master SVG, a coordinated pictogram set (6-10 facility icons) as editable vector, directional sign panel(s) at physical size, door/facility ID plate template, a signage schedule sheet listing panels, sizes and copy, a mounted-panel mockup on a wall photo  
  Absorbs:   
  Engine: html-express  |  Why-not-VLM: A model renders sign pictures, not editable panels at exact cut sizes with a consistent icon system built off the resort's own recovered mon
- **VECTOR-06 — Ridgeway Rovers amateur club full kit & numbering programme**  
  _We have a phone photo of our embroidered club crest and two hand-drawn sheets of our letters and numbers; turn them into a proper team kit package — a clean crest, a full numbering and lettering set f_  
  Collateral: recovered crest master SVG (+ 1-colour and reversed), A-Z + 0-9 vector glyph set, weight-matched, shirt-back placement template (name arc + number), per-player back layouts for the squad (name + number), printer spec sheet: colours, sizes, placement heights, home/away mockup board reusing the crest  
  Absorbs: AO-46, AO-88  
  Engine: image-pipeline  |  Why-not-VLM: A model cannot preserve the club's real crest or produce a registered, weight-consistent glyph set plus correct per-player back layouts as e
- **VECTOR-07 — Wharfside Folk Festival poster spot-colour separation programme**  
  _We have an approved full-colour festival illustration but our printer runs a limited-colour screen press; turn the artwork into a screen-print-ready poster broken into printable colour layers, plus a _  
  Collateral: poster comp at true poster size, per-ink spot-colour separation plates, recovered/vectorized festival wordmark, a handbill version reusing the same separations, a tee-print reduction of the key motif, printer spec: ink list, plate order, registration marks  
  Absorbs: AO-52  
  Engine: image-pipeline  |  Why-not-VLM: A regen makes another pretty poster but cannot output registered per-ink plates from THIS approved illustration, and it would redraw the fes
- **VECTOR-08 — Coble & Vane distillery one-colour mark system**  
  _Our logo only exists as a detailed full-colour file, but we print it one colour on bottle embossing, wax stamps, crates and caps; give us a single-colour version of the mark that holds up everywhere f_  
  Collateral: single-colour master SVG, fine (foil/emboss) variant, stencil-bridged variant for crate/cap, reversed/knockout variant, minimum-size + clear-space usage sheet, application mockups (wax stamp, crate stencil, cap) as an editable doc  
  Absorbs: AO-69  
  Engine: image-pipeline  |  Why-not-VLM: A model would invent a new simplified logo; the client needs THEIR mark faithfully reduced to one colour as editable vector with cut-safe br
- **VECTOR-09 — Halcyon Grid AI-logo cleanup to production vector system**  
  _Our founder generated our logo and two sub-brand marks with an AI tool and all we have are fuzzy PNG exports; rebuild them as crisp, production-clean vector masters with the app icon, favicon and word_  
  Collateral: master mark SVG (clean paths, closed counters), two sub-brand mark SVGs, weight-matched to the master, horizontal + stacked wordmark lockups, app-icon and favicon crops, 1-colour and reversed variants, a brand-mark sheet as an editable doc  
  Absorbs: AO-48, AO-86  
  Engine: image-pipeline  |  Why-not-VLM: Re-prompting the AI tool yields yet another different logo; the founder needs THESE specific generated marks preserved and turned into clean
- **VECTOR-10 — Evergreen Provisions dispensary apparel capsule from hand-painted crests**  
  _We commissioned hand-painted crest panels for our shop and now want a small apparel capsule from them; recover the paintings into clean screen-print art and produce the print-ready separations and moc_  
  Collateral: recovered crest vectors (from the painted panels), spot-colour separation sheets per design, 1-colour reductions for dark garments, tee + hoodie mockup board, printer spec: ink list, plate order, placement, a square social teaser set  
  Absorbs: AO-49  
  Engine: image-pipeline  |  Why-not-VLM: A model redraws the paintings into generic art; the client needs their commissioned crests preserved and turned into registered spot plates,
- **VECTOR-11 — Cedar Commons Farmers Market signage & directional set**  
  _Our weekend market needs proper signage from our existing printed logo — a big entrance banner, directional yard signs pointing to parking and vendors, and stall number plates — all ready for our loca_  
  Collateral: recovered market mark SVG, entrance banner at true banner dimensions, directional yard-sign series (parking / vendors / info), stall/booth number plate template, a signage schedule sheet, a staked-sign mockup on a site photo  
  Absorbs:   
  Engine: html-express  |  Why-not-VLM: A model renders sign pictures, not editable large-format panels at true dimensions with a consistent system built on the market's own recove
- **VECTOR-12 — Static Union streetwear patch, pin & sticker merch pack**  
  _We've got a few of our graphics as messy exports and want a small-goods merch pack from them — embroidered patches, enamel pins and stickers — each rebuilt as the right kind of art for how it's actual_  
  Collateral: patch vectors: simplified, limited-colour, merrow-border outline, pin vectors: metal-line + enamel-fill plates, sticker vectors: transparent + kiss-cut line, a merch-pack mockup board, maker spec sheet per item (stitch note / enamel colours / cut), a woven-label lockup  
  Absorbs:   
  Engine: image-pipeline  |  Why-not-VLM: A model produces mockup images but not the three genuinely different manufacture-ready vector reductions of the brand's own graphics.
- **VECTOR-13 — Maison Solene jewelry wordmark & monogram recovery for foil packaging**  
  _Our house wordmark and monogram survive only as a colour-cast flat export and two photos of them on a wall and a card shot under different light; recover the true mark and deliver the refined vector a_  
  Collateral: wordmark master SVG (refined, closed counters), monogram master SVG, single-path foil/engrave outline of each, reversed/knockout variant for dark stock, packaging application sheet (box, ribbon, card) as an editable doc, a foil-on-dark mockup  
  Absorbs: AO-22  
  Engine: image-pipeline  |  Why-not-VLM: A model can't recover the house's TRUE colour from mismatched captures or emit engraving-ready single-path vectors of the actual wordmark — 
- **VECTOR-14 — Ironway Run Club member numbering & race-bib kit**  
  _For our club's season we need a numbering system on our apparel and a personalised race bib for every member — build the numbering artwork from our hand-drawn style sheet and produce a print-ready bib_  
  Collateral: 0-9 (+ A-Z) vector glyph set from the style sheet, apparel numbering placement template, recovered club mark vector for the bib header, per-member race bibs (one print-ready page each), a single press PDF of all bibs (page-count = roster), a numbering + bib spec sheet  
  Absorbs:   
  Engine: indesign-merge  |  Why-not-VLM: A model can't produce a page-ordered per-member print run with each member's real name/number from the roster, nor a consistent editable gly
- **VECTOR-15 — Wren & Halloway heritage property crest recovery, signage & plaque system**  
  _We manage a heritage building whose original crest survives only on a photographed brass plaque and a faded printed letterhead; recover it and build a coordinated exterior signage and directory system_  
  Collateral: recovered crest master SVG, engraving-ready single-path plaque artwork, monument/entrance sign at physical size, tenant directory board template, suite/floor ID plate template, a signage schedule sheet  
  Absorbs:   
  Engine: html-express  |  Why-not-VLM: A model would invent a plausible crest; the building's actual historic crest must be faithfully recovered and delivered as engraving-ready e

## Layout & Data (35)

- **LAYOUT-01 — Kantyna Nova dark tasting-menu house: menu suite + partner deck + reservations one-pager**  
  _Take our raw plate photography and turn it into one coherent set of editable documents for the tasting-menu concept — the printed menus, the deck we show partners, and the page behind the reservation _  
  Collateral: Two-page tasting + wine list menu (A4 portrait, real table markup), 6-slide concept/partner deck (1920x1080) ending on the price ladder, Reservations one-pager (web canvas) with an hours table, 1:1 + 4:5 + 9:16 social teaser set as one mixed-canvas document, Brand basis mini-page (type roles, palette, dark-plate treatment rules), Handover note: type pairing rationale, accent decision, Express print reality  
  Absorbs: AO-109, AO-15, AO-17  
  Engine: html-express  |  Why-not-VLM: A one-shot image model returns a flat picture of a menu with invented dishes and prices; the client needs their real plated dishes, their ex
- **LAYOUT-02 — Corner & Cure deli everyday menu: storefront menu tiles + counter poster + daily-special social set**  
  _Turn our phone photos of the food into one friendly, high-energy set of counter and window pieces plus the posts we run every day — everything editable so we can swap a special ourselves._  
  Collateral: Wall menu-tile board (multi-tile grid, prices in body face), A2 storefront window poster, Daily-special social set: 1:1 feed + 9:16 story + 4:5 (one mixed-canvas doc), Loyalty/hours counter card, Brand mini-basis: warm palette, casual display face, photo treatment, Handover note  
  Absorbs: AO-107, AO-13, AO-14  
  Engine: html-express  |  Why-not-VLM: The client's real menu items, real prices and real food photos must appear and stay editable for daily swaps; a generative render invents di
- **LAYOUT-03 — Lumora clinical-skincare launch kit: PDP carousel set + brand basis page + paid-social suite**  
  _Build the launch look for our new range from the product shots and the approved wordmark — the product-page images, the brand basis our future freelancers follow, and the paid-social set — all as edit_  
  Collateral: PDP carousel: hero tile + ingredient/benefit tile + spec tile (1:1), Brand basis page (type, palette, mark colourways, usage rules), Paid-social suite: 1:1 + 4:5 + 9:16 in one mixed-canvas doc, Shade/variant lineup one-pager, Ingredient infographic (inline-SVG chart), Handover note (accent decision, print reality)  
  Absorbs: AO-01  
  Engine: html-express  |  Why-not-VLM: The real bottle, the real wordmark and the exact shade names/prices must be preserved and remain editable; a one-shot model redraws the bott
- **LAYOUT-04 — NORTHGROVE FW capsule lookbook & campaign: seasonal lookbook deck + poster pair + shoppable social + linesheet**  
  _Take our flat-lay capsule photography and the wordmark and build the season's launch — the lookbook we send buyers, the campaign posters, the shoppable social and the trade linesheet — all editable an_  
  Collateral: Lookbook deck (per-look pages + range grid), A2 campaign poster pair (two divergent directions), Shoppable social set: 1:1 + 4:5 + 9:16 (one mixed-canvas doc), Linesheet price-grid page (real table), Brand basis mini-page, Handover note (direction pick, print reality)  
  Absorbs: AO-04, AO-39, AO-113, AO-63  
  Engine: html-express  |  Why-not-VLM: Real garments, real capsule SKUs and the real wordmark must survive, and buyers need an editable linesheet; a generative model invents garme
- **LAYOUT-05 — Maison Valcère fine-jewellery house: brand-story deck + editorial poster series + boutique PDP tiles**  
  _Rebuild our brand presence from the piece photography and the old wordmark — the house-story deck, the editorial posters, and the boutique product tiles — every file editable and every piece reading a_  
  Collateral: House-story deck (6-root) with a materials/carat spec table, Editorial poster series (three A2 directions in one doc), Boutique PDP tiles: hero + detail + spec (1:1), Brand basis page (mark colourways, clear-space rules, type), Mixed-format social set (1:1 + 9:16), Handover note  
  Absorbs: AO-07, AO-91, AO-115  
  Engine: html-express  |  Why-not-VLM: Real pieces, real carat/material specs and the real house mark must be preserved and stay editable; a generative render fabricates jewellery
- **LAYOUT-06 — Nordheim Atelier FW26 lookbook + poster campaign: editorial lookbook deck + duotone poster pair + campaign social**  
  _Take our FW26 look photography and the atelier wordmark and build the season's editorial pieces — the lookbook we send press and buyers, the campaign poster pair, and the launch social — every file ed_  
  Collateral: Editorial lookbook deck (per-look pages + range grid), Duotone campaign poster pair (two directions in one doc), Campaign social set (1:1 + 4:5 + 9:16, one mixed-canvas doc), Linesheet price-grid page (real table), Brand/type basis mini-page, Handover note  
  Absorbs: AO-106  
  Engine: html-express  |  Why-not-VLM: Real FW26 garments, real models and the real atelier wordmark must be preserved and the pieces must stay editable through proofing; a one-sh
- **LAYOUT-07 — Harbor Crest Realty listing kit: single-property web one-pager + open-house flyer + agent social set**  
  _Turn the listing photos and our mark into the pieces one property needs — the page behind the listing link, the open-house flyer, and the agent's social posts — all editable so the team can reuse the _  
  Collateral: Single-property web one-pager (hero + gallery + details table), Open-house A4 flyer (hero + specs + agent bio + hours), Agent social set: 1:1 'just listed' + 9:16 story + 4:5, Price/feature summary card, Reusable brokerage basis mini-page, Handover note  
  Absorbs: AO-24, AO-119, AO-26  
  Engine: html-express  |  Why-not-VLM: The real house photos, exact bed/bath/sqft/price and the brokerage mark must be exact and editable per listing; a generative model invents a
- **LAYOUT-08 — Verranza Coastal Retreats portfolio: luxury villa pitch deck + prestige listing one-pagers**  
  _Bring our three-villa portfolio into one prestige presentation and the pages that sit behind each villa's booking link — editable, and all reading as one premium collection._  
  Collateral: Portfolio pitch deck (6-root: collection intro, three villas, amenities, rate ladder), Three prestige villa one-pagers (web canvas, amenity table each), Rate/season comparison table page, Prestige social set (16:9 end card + 9:16 + 1:1), Portfolio basis page (palette, type, photo treatment), Handover note (print reality, verification-by-HzHTML note)  
  Absorbs: AO-25  
  Engine: html-express  |  Why-not-VLM: Real villas, real amenities and real seasonal rates must be exact and editable; a generative render invents properties buyers would never fi
- **LAYOUT-09 — Nimbadesk SaaS launch: product one-pagers + investor/sales pitch deck + feature social set**  
  _Build our launch collateral from the product screenshots and logo — the per-feature one-pagers sales sends, the pitch deck, and the launch social — all editable and all reading as one product._  
  Collateral: Three product feature one-pagers (web canvas each), Pitch deck (7-root: problem, product, metrics chart, comparison table, pricing tiers, roadmap, close), Feature-highlight social set (1:1 + 9:16 + 16:9), Pricing-tier comparison page (real table), Metrics infographic (inline-SVG bar + donut), Brand basis mini-page + handover note  
  Absorbs: AO-81, AO-48  
  Engine: html-express  |  Why-not-VLM: Real product UI, real metrics and exact pricing tiers must be accurate and editable as numbers change; a generative model fabricates UI and 
- **LAYOUT-10 — Vidyorja Scholars' Institute annual impact report: data infographic report + donor deck + festive branch campaign banners**  
  _Turn our programme numbers and field photos into the annual pieces we show donors — the impact report, the donor presentation, and the festive branch campaign banners — all editable so we update the f_  
  Collateral: Impact report (multi-page: outcomes charts, spend breakdown table, field stories), Donor pitch deck (6-root ending on the ask), Festive branch campaign banner run (per-branch template root) + two A2 poster directions, Programme outcomes infographic (inline-SVG bar/line/donut), Mixed-format social set for the giving campaign, Basis mini-page + handover note  
  Absorbs: AO-68, AO-42, AO-52, AO-67  
  Engine: html-express  |  Why-not-VLM: Real programme figures, the real emblem and real field photos must be exact and yearly-editable; a generative render fabricates data and ima
- **LAYOUT-11 — Lanternwood Folk Fest 2027 kit: headliner poster series + performer laminate passes + lineup social**  
  _Build this year's festival look from the performer photos and our festival mark — the headliner posters, the laminate passes, and the lineup-announcement social — all editable so we swap acts and colo_  
  Collateral: Headliner poster series (three A2 directions in one doc), Performer laminate pass (badge-size canvas, role colour-coding), Lineup announcement social set (1:1 + 9:16 + 4:5), Stage map (inline SVG), Festival basis page (mark, palette, type), Handover note  
  Absorbs: AO-75, AO-62  
  Engine: html-express  |  Why-not-VLM: Real performer photos, real dates and the real festival mark must be exact and swappable as the lineup changes; a generative render invents 
- **LAYOUT-12 — Umbra Loft after-dark series: duotone gig-poster run + venue tour deck + release social set**  
  _Give our after-dark concert series one bold editable look from the live photos and the artist wordmarks — the gig posters, the deck we pitch to promoters, and the release social — all reading as one s_  
  Collateral: Gig-poster run (three A2 directions, one per headline night), Venue/series pitch deck (5-root), Per-release social set (1:1 + 9:16 + 4:5), Series identity basis page, Episode-art tiles (1:1), Handover note  
  Absorbs: AO-105, AO-116  
  Engine: html-express  |  Why-not-VLM: Real artist photos, real dates/lineups and the real wordmarks must be exact and editable per night; a generative model invents performers an
- **LAYOUT-13 — Marisol Cove resort campaign: homepage one-pager + booking brochure + coastal social suite**  
  _Build our seasonal campaign from licensed coastal imagery matched to our look and our mark — the homepage page, the booking brochure, and the social suite — all editable and all reading as one warm-co_  
  Collateral: Homepage one-pager (full-bleed hero + amenities + rate table), Booking brochure (multi-page: rooms, dining, experiences), Coastal social suite (1:1 + 4:5 + 9:16), Rate/season comparison card (real table), Resort basis page (palette, type, photo treatment), Handover note (stock licensing, print reality)  
  Absorbs: AO-117  
  Engine: html-express  |  Why-not-VLM: The property's real amenities and real seasonal rates must be exact and editable, and imagery must be properly licensed; a generative render
- **LAYOUT-14 — Lumen Quarterly Autumn issue: feature editorial spread + cover + subscriber teaser social set**  
  _Lay out the Autumn feature and cover from the photo essay and our masthead, plus the teasers we post to sell the issue — all editable so the editor can adjust copy before it ships._  
  Collateral: Feature editorial spread (multi-page, pull-quotes + captions), Magazine cover (single canvas, masthead + cover lines), Contents/section-opener page, Subscriber teaser social set (1:1 + 9:16), Type-and-grid basis page, Handover note  
  Absorbs: AO-82, AO-77  
  Engine: html-express  |  Why-not-VLM: The real feature photos, the editor's real copy and the real masthead must be preserved and stay editable through proofing rounds; a generat
- **LAYOUT-15 — Aldervale Mutual producer kit: advisor pitch deck + product one-pager + counter cards**  
  _Turn our product facts and headshots into the pieces our producers use with clients — the pitch deck, the plan one-pager, and the counter cards — all editable so we update rates and disclosures oursel_  
  Collateral: Advisor client-facing pitch deck (6-root), Plan-comparison one-pager (real benefit table), Counter-card set (multiple card canvases in one doc), Rate/premium infographic (inline-SVG), Advisor-brand basis mini-page, Handover note (disclosure editability, print reality)  
  Absorbs:   
  Engine: html-express  |  Why-not-VLM: Real rates, exact disclosures, real advisor headshots and the mark must be accurate and editable as products/regs change; a generative rende
- **LAYOUT-16 — Anvil & Oak strength studio launch: class-schedule poster + membership pitch deck + athlete-spotlight social set**  
  _Launch the studio with one editable look from the space, coach and member-athlete photos and our mark — the class schedule poster, the membership deck, and the athlete-spotlight social/cards — so we c_  
  Collateral: Class-schedule wall poster (A2, real weekly grid table), Membership pitch deck (5-root: philosophy, programming, coaches, pricing tiers, join), Athlete-spotlight card set + programming social (1:1 + 9:16 + 4:5), Membership-tier comparison card (real table), Studio basis page (palette, type, photo treatment), Handover note  
  Absorbs:   
  Engine: html-express  |  Why-not-VLM: The real space, real coaches, real member-athletes, real class times and the mark must be exact and editable as programming changes; a gener
- **LAYOUT-17 — Apexguard Auto Film brand rollout: dealer pitch deck + product spec poster + installer social set**  
  _Roll out the brand from the AI-drafted master logo and product shots — the deck we pitch to dealers, the product spec poster, and the installer social — all editable and reading as one brand across th_  
  Collateral: Dealer pitch deck (6-root: brand, product tiers, warranty table, install proof, pricing, close), Product-spec A1 poster, Installer social set (1:1 + 9:16 + 16:9), Warranty/tier comparison page (real table), Logo-family basis page (master + sub-marks, usage rules), Handover note  
  Absorbs: AO-90, AO-45  
  Engine: html-express  |  Why-not-VLM: The brand's real logo family, exact warranty tiers and product specs must be consistent and editable; a generative render invents inconsiste
- **LAYOUT-18 — Kilnmore home-goods marketplace relaunch: PDP tile set + paid-social kit + storefront graphics + wholesale deck**  
  _Relaunch the range from the product photography and our mark — the product-page tiles, the paid-social kit, the storefront graphics and the wholesale deck — all editable and all reading as one line._  
  Collateral: PDP tile set: hero + detail + spec (1:1), Paid-social kit (1:1 + 4:5 + 9:16, three different SKU arguments), Storefront/window graphics refresh (holds house warmth), Wholesale brand deck (6-root with a line-sheet price table), Range lookbook one-pager + brand basis mini-page, Handover note (print reality)  
  Absorbs: AO-02, AO-03, AO-83, AO-72  
  Engine: html-express  |  Why-not-VLM: Real products, exact wholesale pricing and the real mark must be accurate and editable; a generative render invents products and can't be re
- **LAYOUT-19 — Northwind Advisory 'Our Team' & about-page set: team page + firm capabilities one-pager + credentials social**  
  _Take our differently-lit staff headshots and our mark and build the pages clients judge us by — the 'Our Team' page, the firm about/capabilities one-pager, and the credentials social — all editable so_  
  Collateral: 'Our Team' page (uniform headshot grid + name/title/bio), Firm about/capabilities one-pager (real credentials/sector table), Credentials/announcement social set (1:1 + 4:5), Reusable team-card template root, Brand basis mini-page, Handover note  
  Absorbs: AO-104, AO-20  
  Engine: html-express  |  Why-not-VLM: The firm's real employees, real names/titles and the real mark must appear and stay editable as the team changes; a generative render replac
- **LAYOUT-20 — Fernwood memorial memory-book: multi-page keepsake book + framed tribute + keepsake share card**  
  _Turn our box of mixed-era family scans into a memory-book we'd be proud to print and share at the service — one dignified keepsake volume plus a framed tribute and a card for family — all editable so _  
  Collateral: Memorial memory-book (multi-page, photo plates + captions + a tribute/eulogy spread), Framed A4 tribute page, Keepsake share card (1:1), Order-of-service style contents page, Type-and-grid basis note, Handover note  
  Absorbs: AO-35, AO-37  
  Engine: html-express  |  Why-not-VLM: The family's real, irreplaceable scans, real names and dates must be preserved and stay editable through proofing; a generative render fabri
- **LAYOUT-21 — Harborline Realty weekly listing-sheet run — full active-inventory batch**  
  _Turn the brokerage's weekly export of active listings and their raw photo folders into a complete run of one-page listing sheets, one per property, that all read as a single house-branded set the agen_  
  Collateral: Press multi-page listing-sheet PDF (all active listings), Per-property named single-page PDFs, 300-DPI JPEG proof of the flagship listing for principal sign-off, Normalised hero-photo set (one white point) fed into the merge, Recovered vector brokerage mark placed identically on every sheet, Mapping/verification note listing every merged field  
  Absorbs: AO-79  
  Engine: indesign-merge  |  Why-not-VLM: A one-shot image model cannot emit an N-page PDF whose page count equals the active-listing count with each page carrying that property's re
- **LAYOUT-22 — Cedarline Institute credential run — full graduating cohort certificates**  
  _Produce the whole graduating cohort's completion certificates from the registrar's export, one personalised certificate per candidate, each print-ready and also delivered as its own file named to the _  
  Collateral: Press multi-page certificate PDF for the cohort, Per-candidate named single-page PDFs for email delivery, 300-DPI proof certificate for the registrar's approval, Recovered vector institutional seal placed identically on every certificate, Field-mapping + placeholder-verification note  
  Absorbs:   
  Engine: indesign-merge  |  Why-not-VLM: An image model cannot produce hundreds of certificates each bearing a real candidate's exact legal name and credential with zero misspelling
- **LAYOUT-23 — Meridian Summit attendee badge batch — full delegate roster**  
  _Build the full set of printed delegate badges for the summit from the registration export, one badge per attendee with their name, company, role track and headshot, ready for the on-site printer as a _  
  Collateral: Press multi-page badge PDF in registration order, Normalised headshot set (one crop logic + one white point) fed into the merge, Recovered vector event mark placed identically on every badge, Track-colour reasoning note, Field + image-mapping verification note  
  Absorbs:   
  Engine: indesign-merge  |  Why-not-VLM: An image model cannot generate a badge run that preserves every attendee's real name, employer and actual headshot in registration order at 
- **LAYOUT-24 — Halden & Roe wholesale catalog — full SKU book with per-item photos**  
  _Turn the wholesale price file and the product photo folder into the season's full trade catalog, one product per page with its photo, specs and trade price, so buyers can order from a single consisten_  
  Collateral: Press multi-page catalog PDF (all active SKUs), Normalised product-photo set at one white point + crop, 300-DPI proof spread of the hero SKU, Recovered vector house mark on the running footer of every page, Discontinued-row exclusion + price-formatting note, Field + image-mapping verification note  
  Absorbs: AO-74  
  Engine: indesign-merge  |  Why-not-VLM: A generative model cannot output a multi-hundred-page catalog with each page showing the correct SKU's real photograph and exact trade price
- **LAYOUT-25 — Ashford Mutual producer mailer — personalised direct-mail run**  
  _Produce the full personalised direct-mail postcard run to the household list, each card addressed to the recipient with their assigned local agent and renewal offer, ready to hand to the mail house._  
  Collateral: Press multi-page personalised postcard PDF, Per-agent named postcard subsets, Recovered vector company mark on every card, Address-block + offer-band formatting note, Field-mapping verification note  
  Absorbs: AO-76  
  Engine: indesign-merge  |  Why-not-VLM: A generative model cannot address thousands of cards to real recipients at real addresses with the correct assigned agent per record; it fab
- **LAYOUT-26 — Lanternwood Folk Festival programme — per-performer profile booklet**  
  _Assemble the festival's printed programme so every performer on the bill gets their own profile page with photo, set time and bio, produced as one bound booklet from the line-up sheet and the press-ph_  
  Collateral: Press multi-page programme PDF in running order, Normalised press-photo set (one tonal look) fed into the merge, Recovered vector festival crest on every profile page, 300-DPI cover proof, Stage/day sequencing note, Field + image-mapping verification note  
  Absorbs: AO-80  
  Engine: indesign-merge  |  Why-not-VLM: An image model cannot build a booklet with a page per real performer carrying their actual photo, correct set time and real bio in running o
- **LAYOUT-27 — Girdermark Components data-sheet library — per-part spec sheets + labels**  
  _Turn the parts database and the bench-photo folder into the full printed data-sheet library plus matching part labels, one spec sheet and label per part with its bench photo, dimensional table and ord_  
  Collateral: Press multi-page data-sheet PDF (all active parts), Per-part named single-page PDFs for the portal, Merged per-part label sheet from the same roster, Normalised bench-photo set at one white point + crop, Recovered vector company mark on every sheet, Field + image-mapping verification note  
  Absorbs: AO-85, AO-84  
  Engine: indesign-merge  |  Why-not-VLM: A generative model cannot produce a sheet per real part with its exact dimensions, ordering code and actual bench photograph at the correct 
- **LAYOUT-28 — SÈVE Botanicals shade-label run — per-variant product labels**  
  _Produce the full set of product labels for the launch range from the shade/variant sheet, one label per SKU carrying its shade name, ingredient line and batch field, plus the shade swatch, ready for t_  
  Collateral: Press multi-page label PDF (all SKUs), Normalised swatch/packshot set at one white point, Recovered vector house wordmark on every label, 300-DPI proof label for regulatory sign-off, Ingredient-line + net-weight formatting note, Field + image-mapping verification note  
  Absorbs: AO-89, AO-64, AO-114  
  Engine: indesign-merge  |  Why-not-VLM: An image model cannot emit a label per real SKU with that variant's exact shade name, correct INCI line and its own swatch at the right coun
- **LAYOUT-29 — Rivermeadow Trust year-end appeal — personalised donor letters + receipts**  
  _Produce the charity's year-end donor pack: a personalised thank-you letter and a matching tax receipt for every donor from the giving export, each carrying their name, gift total and giving level, del_  
  Collateral: Press multi-page donor-pack PDF, Per-donor named single-page PDFs for email delivery, Recovered vector charity mark on every page, Currency + giving-level formatting note, Field-mapping verification note  
  Absorbs:   
  Engine: indesign-merge  |  Why-not-VLM: A generative model cannot produce a letter and receipt per real donor with their exact name and gift total at the right count and matching p
- **LAYOUT-30 — Emberwell franchise menu inserts — per-location price/availability run**  
  _Produce the printed menu inserts for every franchise location from the location price/availability file, each insert showing that store's own prices and which dishes it offers, so the whole estate pri_  
  Collateral: Press multi-page menu-insert PDF (all locations), Per-location named single-page PDFs for each store manager, Recovered vector brand mark on every insert, Price + availability formatting note, Field-mapping verification note  
  Absorbs: AO-78  
  Engine: indesign-merge  |  Why-not-VLM: An image model cannot generate an insert per real location carrying that store's exact prices and true availability at the correct count; it
- **LAYOUT-31 — Cellar & Cru shelf-talker run — per-varietal tasting cards**  
  _From the merchant's wine list and bottle-shot folder, produce the printed shelf-talkers, one per wine with its name, region, tasting note, score and bottle image, so the shop floor reads as one curate_  
  Collateral: Press multi-page shelf-talker PDF (all listed wines), Normalised bottle-shot set at one white point + crop, Recovered vector merchant mark on every card, Score + vintage formatting note, Field + image-mapping verification note  
  Absorbs:   
  Engine: indesign-merge  |  Why-not-VLM: An image model cannot emit a talker per real wine with its exact vintage, score and note plus its own bottle shot at the correct count; it i
- **LAYOUT-32 — Vanguard Motors forecourt run — per-vehicle window spec cards**  
  _From the current stock feed and the vehicle-photo folder, produce the printed forecourt window cards, one per vehicle showing its price, key specs and a photo, so every car on the lot displays a consi_  
  Collateral: Press multi-page window-card PDF (all in-stock vehicles), Per-vehicle named single-page PDFs by stock number, Normalised vehicle-photo set at one white point + crop, Recovered vector dealership mark on every card, Price + spec formatting note, Field + image-mapping verification note  
  Absorbs:   
  Engine: indesign-merge  |  Why-not-VLM: A generative model cannot produce a card per real vehicle with its exact price, specs and actual photograph at the correct count with per-st
- **LAYOUT-33 — Continental Cup player-card run — full squad roster with pitch-side portraits**  
  _Produce the tournament's full set of printed player cards from the squad roster and the pitch-side portrait folder, one card per player with their name, position, squad number and photo, as one ordere_  
  Collateral: Press multi-page player-card PDF in squad order, Per-player named single-page PDFs, The cinematic-graded, subject-isolated portrait set (one look) fed into the merge, Recovered vector tournament mark on every card, 300-DPI proof of the flagship card, Field + image-mapping verification note  
  Absorbs: AO-29  
  Engine: indesign-merge  |  Why-not-VLM: A generative model invents athletes who are not the real, licensed players (likeness) and cannot bind the correct face to the correct record
- **LAYOUT-34 — Ferncroft Nursery plant-tag run — per-variety garden tags**  
  _From the season's plant list and the variety-photo folder, produce the printed garden-centre plant tags, one per variety with its common and botanical name, care icons, price and a photo, ready for th_  
  Collateral: Press multi-page plant-tag PDF (all stocked varieties), Normalised variety-photo set at one white point + crop, Recovered vector nursery mark on every tag, Per-department named tag subsets, Care-icon + price formatting note, Field + image-mapping verification note  
  Absorbs:   
  Engine: indesign-merge  |  Why-not-VLM: A generative model cannot emit a tag per real variety with its correct botanical name, care attributes and price plus its own photograph at 
- **LAYOUT-35 — Marrow & Vane Gallery exhibition labels — per-artwork wall cards + checklist**  
  _For the upcoming exhibition, produce the printed wall labels and the accompanying checklist from the works list and the artwork-image folder, one label per piece with title, artist, medium, dimensions_  
  Collateral: Press multi-page wall-label PDF (all hung works), Merged exhibition checklist PDF from the same works list, Normalised artwork-image set at one white point, Recovered vector gallery mark on the checklist, Per-room named label subsets in hang order, Field + image-mapping verification note  
  Absorbs:   
  Engine: indesign-merge  |  Why-not-VLM: An image model cannot produce a label per real artwork with its exact title, artist, medium and dimensions plus a correct reference image at

## Motion & Audio (20)

- **MOTION-01 — Ember & Oak wood-fired sizzle-reel launch kit**  
  _Turn a wood-fired grill's raw dish and flame b-roll, a plated hero still, a flat logo and a menu-callout sheet into a mouth-watering launch package — a fast highlight reel, a matched vertical and squa_  
  Collateral: AI highlight sizzle reel (16:9 master), 9:16 vertical reframe (no upscale), 1:1 square reframe, graded plated-hero still doubling as thumbnail + poster, editable dish-callout lower-third/caption cards, cleaned ambient-audio version of the reel  
  Absorbs: AO-122  
  Engine: video-pipeline  |  Why-not-VLM: A model can generate a generic food clip; it cannot cut THIS restaurant's own b-roll into a highlight, preserve the real plated dishes and t
- **MOTION-02 — Ironwood Kitchen bowl-line social launch package**  
  _From a fast-casual bowl brand's single showcase take, its eight raw bowl stills each carrying a grey card, a line-sheet template, a roster sheet and a flat wordmark, build a bright grab-and-go launch:_  
  Collateral: AI highlight reel from the showcase take, 9:16 + 4:5 reframe set (no upscale), eight bowl stills neutralised to one house white point, printed line sheet from the merge template, editable menu/caption cards, handover pack  
  Absorbs: AO-55  
  Engine: video-pipeline  |  Why-not-VLM: A one-shot model cannot neutralise eight of the client's real bowl photos to a measurable shared white point, cut the client's own take, bin
- **MOTION-03 — NOURA daily-greens UGC paid-social ad package**  
  _Turn a greens-subscription brand's raw creator talking-head clips, product b-roll, a flat wordmark, a hero thumbnail still, a colour reference and a hooks brief into a paid-social ad package: a UGC-st_  
  Collateral: AI highlight UGC mashup ad, 1:1 + 4:5 + 9:16 platform set (no upscale), hook caption/lower-third overlay cards (editable), matched hero thumbnail still, cleaned creator-audio version, handover pack with hook variants mapped to formats  
  Absorbs: AO-120  
  Engine: video-pipeline  |  Why-not-VLM: A model cannot assemble the real creators' own footage into a highlight, preserve their faces and the real product, derive hooks from what w
- **MOTION-04 — Sable & Finch Realty listing-tour package**  
  _From a realty team's raw handheld walkthrough and exterior clips, a flat logo, a warm look-reference, a shot list and listing copy, build a branded listing tour: a polished landscape master walkthroug_  
  Collateral: 16:9 master walkthrough highlight, 9:16 vertical reel re-aspected from the master (no upscale), graded poster still (thumbnail + cover), printed listing cards from the merge template, lower-third listing-fact caption overlays (editable), handover pack  
  Absorbs: AO-121  
  Engine: video-pipeline  |  Why-not-VLM: A model cannot cut the agent's own walkthrough footage, preserve the real rooms and the real brokerage logo, re-aspect the exact master to s
- **MOTION-05 — Sterling Row luxury-listing channel package**  
  _Bring a luxury developer's eight mixed-light penthouse hero stills to one prestige house look, cut a restrained channel sizzle from the footage, re-aspect a vertical teaser, pull a cover still and pro_  
  Collateral: eight hero stills matched to one prestige white point, restrained channel sizzle (16:9), 9:16 vertical teaser re-aspected (no upscale), graded cover still, variable listing cards from the merge template, handover pack  
  Absorbs: AO-23  
  Engine: video-pipeline  |  Why-not-VLM: A model cannot match the developer's eight real interiors to a measurable shared white point, cut the real footage, re-aspect the exact mast
- **MOTION-06 — Meridian Academy course-lesson explainer edit**  
  _Turn an online academy's raw Lesson 4 material — a talking-head lecture, slide and spreadsheet screencasts, a logo, a look-reference and a captions sheet — into a clean, watchable lesson edit: a highl_  
  Collateral: cleaned, tightened lecture highlight (16:9), screencast segments reframed to a consistent 16:9 (no upscale), key-point lower-third caption cards (editable), course thumbnail from a graded lecture frame, cleaned-audio lesson master, handover pack  
  Absorbs: AO-123  
  Engine: video-pipeline  |  Why-not-VLM: A model cannot clean and tighten the instructor's real lecture, reframe the real screencasts without softening the text, caption from what w
- **MOTION-07 — Norvant product-explainer launch kit**  
  _From one long single-take founder interview, a photographed wordmark, a launch-card template and copy, produce a launch kit: clean the interview audio, tighten it to a short explainer highlight and a _  
  Collateral: cleaned, tightened explainer highlight (16:9), same-length 9:16 reframe (no upscale), six poster frames graded to one look, printed launch cards from the merge template, cleaned-audio master, handover pack with route limits  
  Absorbs: AO-34  
  Engine: video-pipeline  |  Why-not-VLM: A model cannot clean and tighten the founder's real interview, re-aspect that exact take, pull six real frames from it, preserve the real wo
- **MOTION-08 — SentinelMesh SaaS demo launch collateral**  
  _Turn a security SaaS's raw screen recordings and b-roll, five product stills, two logo files and a messaging matrix into launch collateral: a demo highlight with strictly-shorter promo and teaser cuts_  
  Collateral: demo highlight (16:9), strictly-shorter promo and teaser cuts, 9:16 teaser reframe (no upscale), five product stills graded to one look, messaging-driven lower-third caption cards (editable), handover pack  
  Absorbs: AO-96  
  Engine: video-pipeline  |  Why-not-VLM: A model cannot cut the client's real product recordings, generate strictly-shorter cutdowns from that master, preserve the real UI and corre
- **MOTION-09 — Voltcast E42 channel-delivery package**  
  _From a tech-review channel's long-form 4K master and its scene selects plus a channel bug, build the full publish package: a highlight short with cleaned narration, re-aspected to vertical and square,_  
  Collateral: highlight short with cleaned narration (16:9), 9:16 reframe (no upscale), 1:1 reframe (no upscale), matched thumbnail still, caption/lower-third cards (editable), handover pack  
  Absorbs: AO-95  
  Engine: video-pipeline  |  Why-not-VLM: A model cannot cut the creator's own 4K master, clean the real narration, re-aspect that exact footage, preserve the real channel bug, or re
- **MOTION-10 — DAYDRIFT podcast episode-art + clip package**  
  _From three mixed-lighting podcast episodes, a photographed logo, an episode-card template and a roster, build a channel-consistent art and clip package: a representative frame per episode graded to on_  
  Collateral: three representative episode frames matched to one look, printed episode cards from the template, short 9:16 clips per episode with cleaned audio (no upscale), thumbnail set, caption/lower-third overlays (editable), handover pack  
  Absorbs: AO-61  
  Engine: video-pipeline  |  Why-not-VLM: A model cannot pull representative frames from the client's three real episodes, match them to a measurable shared look, clean the real audi
- **MOTION-11 — STATIC FOX gaming-channel thumbnail + clip pack**  
  _From a comedy-gaming creator's six mixed-lighting captures, an emblem and a mascot render, build a channel pack: pull the strongest frame from each capture and grade the six to one house look, cut sho_  
  Collateral: six peak frames graded to one house look, thumbnail set with mascot knocked out, short 9:16 clips with cleaned commentary (no upscale), emblem end-card, caption/lower-third overlays (editable), handover pack  
  Absorbs: AO-56  
  Engine: video-pipeline  |  Why-not-VLM: A model cannot pull peak frames from the creator's own captures, match them to a measurable house look, cleanly knock out the real mascot re
- **MOTION-12 — NIGHTFORM night-drive single-cut drop package**  
  _From one ~45s 4K night-drive take, a cover-board template, a shot list, a flat wordmark and a captions script, build a release drop: six strong beats pulled and each neutralised to the in-frame card s_  
  Collateral: six beat frames neutralised to one grade, short sizzle (16:9), 9:16 reframe (no upscale), cover-board cards from the template, lower-third caption overlays from the script (editable), handover pack  
  Absorbs: AO-57  
  Engine: video-pipeline  |  Why-not-VLM: A model cannot pull six real beats from the artist's own take, match them to a measurable single grade, preserve the real wordmark, or bind 
- **MOTION-13 — Emberline daily promo-spot package**  
  _From today's eight exported promo key frames — each shot across the day under its own light with a grey card in-frame — grade every one to a single lively-but-clean show look, cut a daily promo spot w_  
  Collateral: eight key frames graded to one show white point, daily promo spot (16:9), 9:16 reframe (no upscale), caption cards from the day's summary (editable), handover pack with the repeatable daily recipe  
  Absorbs: AO-30  
  Engine: video-pipeline  |  Why-not-VLM: A model cannot grade the show's eight real frames to a measurable shared white point, cut the day's real footage, or produce editable captio
- **MOTION-14 — Daily-vlog per-episode brand kit**  
  _Bring a vlog channel's eight differently-lit episode stills to one house look, merge per-episode thumbnail cards, cut a short recap with a vertical reframe and cleaned voiceover, and author caption ov_  
  Collateral: eight episode stills matched to one house look, per-episode thumbnail cards from the merge template, short recap with cleaned voiceover (16:9), 9:16 reframe (no upscale), caption overlays (editable), handover pack  
  Absorbs: AO-31  
  Engine: video-pipeline  |  Why-not-VLM: A model cannot match the vlogger's eight real stills to a measurable house look, bind the correct still to each thumbnail card, clean the re
- **MOTION-15 — Anvil & Oak Strength movement-library package**  
  _For six core movements, cut a single-clip landscape highlight from each long demo take, pull a hero poster frame from each, grade all six to one studio white point, reframe vertical shorts, and merge _  
  Collateral: six per-movement landscape highlights, six hero poster frames graded to one white point, vertical 9:16 shorts per movement (no upscale), exercise cards from the merge template, recovered wordmark + seal, handover pack  
  Absorbs: AO-58  
  Engine: video-pipeline  |  Why-not-VLM: A model cannot cut the client's real demo takes, pull real hero frames matched to one white point, preserve the real wordmark and seal, or p
- **MOTION-16 — Vitalé Labs 'Balance Brief' three-episode drop**  
  _For three wellness episodes, cut a punchy landscape highlight from each presenter take, re-aspect a vertical reel from the 4K take, pull and grade a hero cover still per episode, and merge episode car_  
  Collateral: three per-episode landscape highlights, three 9:16 reels re-aspected from 4K (no upscale), three hero cover stills graded to one look, episode cards from the merge template, caption/lower-third overlays (editable), handover pack  
  Absorbs: AO-94  
  Engine: video-pipeline  |  Why-not-VLM: A model cannot cut the presenter's real takes, re-aspect that exact 4K footage without inventing pixels, pull real cover frames matched to o
- **MOTION-17 — Pulsevault club-night recap package**  
  _From raw club-night phone clips, a hero cover still and a venue logo, build a post-ready recap: a high-energy short sizzle reframed to vertical, a graded hero cover with a gritty club treatment, and a_  
  Collateral: high-energy sizzle (9:16, 1080x1920), graded hero cover still with club treatment, event-info caption/lower-third sheet (editable), recovered venue wordmark, handover pack  
  Absorbs: AO-97  
  Engine: video-pipeline  |  Why-not-VLM: A model cannot cut the venue's own phone footage from last night, preserve the real crowd and venue logo, hit the exact vertical spec, or ha
- **MOTION-18 — Velvet Hour monthly gig package**  
  _Cut a short social sizzle and a vertical story reframe from last month's single-camera set take, pull a poster still, grade four promo photos of next month's acts to one look, and merge a lineup listi_  
  Collateral: social sizzle (16:9), vertical story reframe (no upscale), poster still pulled from the set take, four promo photos graded to one look, lineup listing card from the merge template, caption overlays (editable)  
  Absorbs: AO-98  
  Engine: video-pipeline  |  Why-not-VLM: A model cannot cut the venue's own set footage, pull a real poster frame, match four real promo photos of real acts to one look, or bind lin
- **MOTION-19 — Milepost Driving Academy learner-guide video + reference set**  
  _For a driving academy, bring six road-scenario reference stills shot across changing daylight to one consistent house white point, triage a flat sign glyph-sheet against a photographed sign, cut short_  
  Collateral: six road-scenario stills matched to one house white point, short scenario clips with cleaned narration (no upscale), 9:16 reframe of a key clip, triaged sign artwork (vector glyph vs photographed cut-out), printed learner guide from the merge template, handover pack  
  Absorbs: AO-54  
  Engine: video-pipeline  |  Why-not-VLM: A model cannot match the academy's six real road scenes to a measurable white point, correctly triage the two real sign files, clean the rea
- **MOTION-20 — FOLD & GRAIN Studio 'one-take, whole-board' productized service**  
  _A product-photography studio wants a repeatable service built and proven on two live client runs: from a single continuous 4K take per client, pull the strongest frame of each product, neutralise ever_  
  Collateral: packaging shot-board of matched frames, pendant shot-board of matched frames, two short product sizzles (16:9), 1:1 + 9:16 reframe set per sizzle (no upscale), two recovered client wordmarks, handover pack with the repeatable pipeline recipe  
  Absorbs: AO-60, AO-99  
  Engine: video-pipeline  |  Why-not-VLM: A model cannot pull the sharpest real frames from each studio take, match them to a measurable per-board grade, preserve the two real client
