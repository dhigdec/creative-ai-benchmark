# CREATIVE-AGENT BENCHMARK — COMPLETE PROJECT CONTEXT (A → Z)
**Single-file handoff. Written 2026-06-23. Paste this whole file into Claude to load the entire project cold.**

> Read top-to-bottom once. After that you can reason about, operate, and extend every part of this project.
> This supersedes the older `PROJECT_CONTEXT_HANDOFF.md` (2026-06-11), which covers only the early phases.

---

## 0. THE 60-SECOND SUMMARY

**What this is:** an end-to-end system that proves and *measures* whether an AI agent can do real freelance **creative/design** work — like a human designer would — by:
1. **Harvesting** thousands of real freelance design briefs (Upwork / Freelancer / PeoplePerHour).
2. **Verifying** which briefs are actually doable with the **Adobe Creative Cloud MCP connector** (and where Canva fits).
3. **Generating the input assets** a real client would hand over (logos, product photos, menus, CSVs, video, audio) — simulating the client — using **Gemini + OpenAI only (never Claude)**.
4. **Judging** those asset packages with a hardened 3-model panel + a deterministic closed-repair loop.
5. **Executing** the tasks end-to-end through the Adobe connector (real, logged tool calls) + local composition.
6. **Scoring** the results with content-specific rubrics in self-contained review websites (for a human annotation team).
7. **Formalizing** the whole thing into a publishable, sellable benchmark — **"StudioBench"** — with a data-derived taxonomy, an evaluation protocol, and a competitive position against the recent lab benchmarks (Contra's Human Creativity Benchmark and Lica's GDB).

**Why it matters:** the company behind this is a **data company**. The goal is the *best, most unique, most sellable* creative-**agent** benchmark in the field — and the labeled artifacts it produces (executable trajectories, verified doable/not-doable ground truth, rubric annotations) are themselves a sellable training/eval data product.

**Current state (2026-06-23):** every stage 1→6 has working v1 implementations with real artifacts on disk. Stage 7 (the benchmark formalization + competitive positioning) is designed and written up. The most recent work: a paper-style taxonomy spec ("StudioBench"), a competitive teardown vs Contra + GDB (adversarially verified), and a Word-doc export of the spec.

---

## 1. ENVIRONMENT & MACHINE (how to run anything)

- **OS:** macOS (darwin). Shell: zsh. **Not a git repo** (no version control here).
- **Project root:** `/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/`
- **Sibling project** (earlier, reused some classifiers): `/Users/dhiren/Downloads/Deccan/SWE-Freelance-Leads/`
- **Python venv** (the workhorse): `asset_pipeline/.venv/` → always invoke as `asset_pipeline/.venv/bin/python`.
  Has: Pillow 11, `openai`, `google-genai`, `anthropic`, `python-dotenv`, `requests`, `qrcode`, `imageio-ffmpeg`.
  (System python 3.9.6 is too bare; no numpy/scipy/sklearn in the venv — clustering etc. is hand-rolled pure-Python.)
- **Node** v24 for the `.docx`/HTML builders. `docx` 9.7.1 is in `node_modules` (used by the doc builders).
- **API keys:** `asset_pipeline/.env` (chmod 600) — `GEMINI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, all set & working. **Never commit these.** (No keys are reproduced in this doc.)
- **Adobe access:** a **CC Pro** account is used (unlocked Illustrator + InDesign entitlements; earlier a free account blocked those). Account is signed into the Adobe Creative Cloud MCP connector.
- **`pandoc` is NOT installed** → all Word docs are built with **docx-js**, not pandoc.
- **`ffmpeg` not on PATH** → use `imageio-ffmpeg`'s `get_ffmpeg_exe()`.
- **`soffice`/LibreOffice not installed** → can't headlessly render a `.docx` to an image; verify docs by opening in Word or inspecting the OOXML.
- **Preview servers:** Python `http.server` is sometimes sandbox-blocked → the review sites use a tiny **node** static server instead (`serve_review.js`). Ports used historically: 8765 (root), 8793 (survey), 8801 (flagship review), 8802 (mega review).

---

## 2. THE FULL CHRONOLOGICAL ARC (every phase / scenario, in order)

This is the story A→Z. Each phase left real artifacts (mapped in §3–§11).

1. **Harvest** — scraped real freelance design postings (Upwork browser harvests, Freelancer.com, PeoplePerHour) into a SQLite DB (`pipeline/data/adobe.db`). ~**5,218** Adobe-relevant items.
2. **Clean** — a `cleantask=1` filter removed job-ads / vague posts → **3,888 genuine project briefs** (`db_all.json`).
3. **Connector capability discovery** — loaded the real Adobe MCP tool schemas and discovered the hard truth: **the connector has NO text-to-image generation**, `image_fill_area` is solid-color fill only, `image_generative_expand` is edge-outpaint only, and the Adobe Express design path needs a human gallery click. (This single fact governs everything downstream — see §5.)
4. **Doable classification (v1)** — 46 verification agent batches checked candidates tool-by-tool → **1,260 connector-doable tasks** (`adobe_doable_full.json`), tiered **57 full / 862 template / 341 partial**. ~1,275 dropped with reasons (bespoke logo/identity, illustration, needs-generation, etc.).
5. **Deliverable docs + dashboard** — built per-task Word/CSV docs and a self-contained interactive HTML dashboard of the 1,260 doable tasks.
6. **Asset-generation pipeline built** (`asset_pipeline/`) — simulates the *client*: for a chosen task, generates every input asset the brief implies (photos, logos, copy, menus, CSVs), coherent under an invented brand persona, with QC, manifests and contact sheets. **Round 1: 5 tasks. Round 2 (wide-mix, top image models): 5 more → 10 packages.**
7. **Package judge + closed loop** (`judge.py`, `scorecard.py`) — a 3-judge cross-provider panel (Claude + Gemini + GPT) scores each *package* on 6 anchored dimensions; an adversarial red-team pass; a deterministic data-check layer; and a closed repair loop that surgically patches flagged assets. **Hardened via sabotage testing** (deliberately deleting a mandatory field and proving the judge catches it and the loop doesn't fake recovery).
8. **First connector EXECUTION (2026-06-11)** — proved the Adobe connector runs **headlessly** (upload → edit tool → download). Ran **5 tasks** → 9 real outputs (`executed_jobs/`). Built a **125-item annotation survey** HTML.
9. **User feedback: "too trivial"** — those 5 were single-tool ops (vectorize / bg-removal / auto-tone). The user wanted **complex, long-horizon creative tasks** with rich briefs and **composed final deliverables** (finished posters/postcards/social posts), not single image ops.
10. **Flagship round 3** — authored **5 complex multi-deliverable tasks** (`5366` wedding signage, `3437` Blausweta insert, `3252` THC postcard, `5388` TeenTalk ads, `1559` George Inn menus), generated their input-asset packages (with a photorealism doctrine + a new `program` asset kind for real QR codes), and judge/loop-verified them.
11. **Flagship EXECUTIONS** — ran all 5 end-to-end (**47 real connector ops**, 250 step images, 40 outputs) using a resolved **hybrid** composition strategy: the connector does element ops, a local **PIL compositor** assembles finished layouts (the connector can't compose headlessly). Wrapped in a scorable review site (`Flagship_Review.html`, **185 rubric items**).
12. **MEGA benchmark (2026-06-14)** — user wanted MAXIMUM connector utilization + video/audio. Probed and proved **video gen (Veo 3 / Sora-2) + TTS** for input assets. Authored **7 → then a definitive 10** long-horizon tasks (18–31 connectors each) covering **all 38 headless-confirmed connectors, 0 uncovered**. Generated all 10 packages (incl. video/audio), judged, and **executed all 10** (`mega_executions/`: ~280 connector ops, ~370 trajectory steps, ~340 before/after images) with a review site (`Mega_Review.html`, **410 rubric items**).
13. **Connector capability re-grade + ADVERSARIAL AUDIT (v2.1, 2026-06-16)** — with the Pro connector set, re-graded **all 3,888 briefs** execution-mode-aware (`adobe_doable_v2.json`, 3,900 rows). First pass **over-claimed**; a 2-pass adversarial audit found ~half the "doable" grades wrong (mostly "needs original design from scratch"). **Verified-final: 1,170 truly doable** (`adobe_doable_VERIFIED.json/.csv`), not 2,182.
14. **Wide-mix Adobe-only task set** — user wanted variety + many connectors per task (not the express-heavy market reality). Authored **66 long-horizon Adobe-only tasks** (`complex_benchmark/adobe_only/specs/`, avg ~20 Adobe calls, ~16 distinct tools, 94% output→input chaining, 48/50 tools covered), data-derived into **8 operation clusters** via TF-IDF + hierarchical clustering. Viewer: `Adobe_WideMix_Tasks.html`.
15. **flagship_v2** — 12 more flagship long-horizon mixed tasks (`flagship_v2/specs/`), each grounded in a real brief, exercising the previously-unused tools.
16. **Canva-only + Adobe-vs-Canva bake-off** — saw Canva working alone (`canva_solo/`), then ran a **same-input bake-off** (`bake_off/`): the identical public photo through both the Adobe connector and the Canva connector per task, judged by a 3-judge panel → `Adobe_vs_Canva_Bakeoff.html`. Conclusion: Adobe = element/pixel processing; Canva = composition/layout/data-merge — complementary mirror images.
17. **Doable-tasks browser** — `Doable_Tasks.html`, a full self-contained HTML of all verified-doable tasks (brief, source, one-liner, input assets, expected outputs, Adobe workflow, connectors).
18. **Benchmark formalization ("StudioBench")** — turned the work into a paper-style **taxonomy + evaluation spec**: a **measurement-first, 4-axis** design (8 brand verticals × 8 data-derived operations × 6 capabilities × 4 horizon tiers + tags), a populated Company×Operation matrix over the 66 tasks, a task-instance schema, and an evaluation protocol (Claude-connector execution + automated agentic-process score + SME annotation + leaderboard). Plain-English version for the design/SME team too.
19. **Competitive positioning (2026-06-22/23)** — studied the two recent lab benchmarks the user shared (Contra Human Creativity Benchmark; Lica GDB), built and **adversarially verified** (against the labs' own published text) the case for why StudioBench is uniquely stronger and more sellable: it scores the **worker** (process, honesty, brand-fidelity, cost, client acceptance), not just the **picture**. Produced buyer personas and "new aspects to add."
20. **Doc exports** — `Benchmark_Taxonomy_Proposal.{md,docx}` (plain-English) and `StudioBench_Spec.docx` (the paper-style spec, built with docx-js).

---

## 3. THE CORE TECHNICAL TRUTH — ADOBE CONNECTOR EXECUTION MODES

**This is the most important fact in the project.** Everything about feasibility hinges on it. The Adobe Creative Cloud MCP connector (~70 tools) is an **element/pixel processor**, not a layout composer. **Always call `adobe_mandatory_init` first.** Tag every connector step with an execution mode:

- **[C] headless-confirmed** — runs autonomously in a headless harness. All `image_*` Photoshop/Lightroom tools (adjust/select/mask/crop/effects/remove-bg/vectorize/generative-expand), `asset_search` + `asset_license_and_download_stock` (Adobe Stock), `document_render_layout` / `document_render_vector` (**EXPORT ONLY** — they render a *pre-existing* .indd/.ai → PDF/PNG; they do NOT author a layout), `document_convert_pdf` (PDF→.indd only), `font_recommend`, `create_firefly_board`, asset upload/preview. **38 connectors confirmed [C] on CC Pro.**
- **[W] interactive-widget** — Adobe Express track: `search_design` returns templates headlessly, BUT `fill_text` / `animate_design` / `change_background_color` need a **human to pick a template in a gallery**. Works in the Adobe×Claude *product*, NOT autonomous-headless.
- **[A] async-widget** — `video_create_quick_cut`, `video_resize`, `media_summarize`, `media_enhance_speech`: return `status:"working"` and a progress widget that polls/notifies *in the product*; **not retrievable in a headless harness** → do video/audio editing **locally (ffmpeg)** for our own execution.
- **[T] authored-template** — `document_merge_data_layout` / `_vector` need a **user-authored desktop .indd/.ai** with real Data-Merge/Variable fields. (Confirmed unusable purely headless even on CC Pro — `convert_pdf` gives literal `<<field>>` text that won't bind. So data-merge is done **locally** in our executions, honestly labeled.)
- **[L] local** — local PIL/ffmpeg steps (composition, data-merge, video editing).
- **[X] not available anywhere** — generative fill, text-to-image, AI object-removal, bg-replace-by-prompt, upscale, OCR, PDF-text-edit, video-trim-to-timestamp, compositing. (The ONLY generative tool is `image_generative_expand` = outpaint.)

**Headless execution recipe (verified, egress is enabled):**
```
1. adobe_mandatory_init
2. asset_initialize_file_upload {path, file_size (wc -c), media_type}  → transfer_document (presigned block hrefs)
3. Bash: dd if=<file> bs=<blocksize> skip=<i> count=1 | curl -s -L -X PUT "<href>" -H "Content-Type: <mime>" --data-binary @-   (HTTP 200 per chunk)
4. asset_finalize_file_upload {filename, transfer_document VERBATIM}   → presignedAssetUrl + assetId
5. call edit tool with that URL (imageURI/imageURIs)                   → outputUrl (photoshop-api short-url)
6. curl -L <outputUrl> -o <local>                                      → download; chain outputUrl → next imageURI
```
Gotchas: outputs may come back **JPEG despite a .png name** (check mime). `image_remove_background` can drop white interior letterforms of logos (use the original-on-white for placement). `asset_add_file` is an **interactive picker — never use it** for automation.

**Binding ground-truth sheet:** `complex_benchmark/CONNECTOR_CAPABILITIES_v2.md` (v2.1). Honest headless **composition** path = local PIL, or Canva, or an authored [T] template.

---

## 4. THE DATASETS (the verified task universe)

The funnel, with the authoritative current row counts:

```
5,218 harvested  →  3,888 clean briefs  →  1,260 v1 doable  →  (full re-grade 3,900)  →  1,170 VERIFIED doable
                    (db_all.json)         (adobe_doable_full)  (adobe_doable_v2)         (adobe_doable_VERIFIED)
```

| File | Rows | What it is |
|---|---|---|
| `db_all.json` | 3,888 | All clean briefs (the raw verified-genuine project briefs). |
| `adobe_doable_full.json` | 1,260 | **v1** doable set (46-agent verification). Tiers 57 full / 862 template / 341 partial. Fields: id, family, category, task_type, title, source, date, url, vertical, mcp_workflow, inputs[], feasibility, note, desc. |
| `adobe_doable_v2.json` | 3,900 | **Full re-grade** of every brief against the Pro connector set, execution-mode-aware. Each row carries `feasibility_v2` (first pass), `feasibility_final` (audited truth), `audit` verdict, `execution_mode`, `groups_v2`. |
| `adobe_doable_VERIFIED.json` / `.csv` | 1,170 | **The trustworthy doable subset** after a 2-pass adversarial audit. |

**v2.1 audited-final grades:** `no` 2,007 · `express` 1,018 · `partial` 723 · `full` 140 · `flagship` 12 → **truly doable (full+express+flagship) = 1,170** (1,012 first-pass over-claims removed). **Lesson learned:** "fill a template with the client's OWN assets" = doable; "design something original from scratch" = NOT doable with this toolchain.

**Builders/utilities:** `build_doable_v2.py`, `finalize_audit.py` (the re-grade + audit); `build_adobe_full.js` / `build_adobe_doable.js` (Word/CSV docs); `build_site_data.py` + `site_template.html` + `serve_site.js` (the dashboard); `export_db_json.py`, `cleanup_db.py`, `prune_non_adobe.py`, `merge_upw*.py` (ingest). The SQLite source is `pipeline/data/adobe.db` (table `items`).

**Deliverable docs/dashboards (project root):** `Adobe_Connector_Doable_Tasks.{docx,csv,html}` (the 1,260-task dashboard), `Doable_Tasks.html` (full verified-doable browser), `Adobe_All_Sources_Master.docx`, `Adobe_Tasks_Export.csv`, plus older/superseded `Adobe_*` docs and `adobe_ai_sample*.json` / `adobe_doable_final.json` (early sets). `_archive_pre_cleanup_2026_06_08/` holds pre-clean docs.

---

## 5. THE ASSET-GENERATION PIPELINE (`asset_pipeline/`) — "simulate the client"

**Purpose:** for a chosen task id, generate EVERY input asset the brief implies, coherent under an invented/extracted brand persona, with QC, manifests and contact sheets — so the agent-under-test gets a realistic client handoff.

**HARD RULE (user-mandated):** *all creative generation uses **Gemini / OpenAI only, never Claude**.* Claude is allowed only as **orchestrator / agent-under-test / judge**. (Also: the harness **blocks uploading workspace-origin images to public file hosts** as data exfiltration — a hard boundary; don't work around it.)

**Code (`asset_pipeline/`):**
- `config.py` — env loading, MODEL registry (roles → candidate (provider, model, quality) lists), prices, caps (MAX_IMAGES_PER_RUN, COST_GATE_USD≈$10, QC_MIN_SCORE, QC_MAX_REGENS=2). Roles: image_photoreal/logo/cheap/hero_text, image_photoreal2 (→ gpt-image-2), image_cheap2 (gemini flash-image), hero (→ gemini-3-pro-image "Nano Banana Pro"), **video** (→ Veo 3.1/3.0 "veo-3.x-generate"), **video_sora** (→ sora-2-pro/sora-2), **audio_vo** (OpenAI TTS), writer/judge/package_judge (gemini/gpt/claude). **This is the single secrets/model seam.**
- `specs.py` — hand-authored `TaskSpec`s (assets with prompts/prompt_fn, filenames, QC criteria, decisions[]); merges `flagship_specs/` + `mega_specs/`. ⚠️ `str.format` prompts: literal JSON braces must be doubled `{{ }}`.
- `personas.py` — stage-1 brand persona synthesis (cached `persona.json`).
- `adapters/` — `openai_img.py` (gpt-image-1/2, transparent bg), `gemini_img.py` (flash-image / Nano-Banana-Pro / imagen via google-genai + REST fallback; normalizes to exact WxH), `text_llm.py` (gemini→openai→anthropic chain), **`media_gen.py`** (Veo 3 + Sora-2 video, OpenAI TTS, `roughen_audio` repair via imageio-ffmpeg; HQ-first: 1080p video, 48kHz EBU-R128-normalized audio).
- `degrade.py` — seeded PIL degradation profiles (for "fix this photo" tasks) + `flatten_white()` (⚠️ alpha must flatten to WHITE not black).
- `qc.py` — technical checks (dims/size/uniform/alpha) + vision-judge wrapper.
- `generate.py` — orchestrator. Stages: persona → data/text → images (QC loop ≤2 regens) → post-process → manifest + INTAKE.md + contact sheet. Resume-safe via per-task `state.json`. Asset kinds: image / text / data / **program** (deterministic python render, e.g. QR codes) / **video** / **audio**. Closed-loop hook reads `feedback.json` and **surgically patches** data assets (keeps shape, applies only the fix).
- `manifest.py` (the agent-facing contract: every asset ↔ verbatim input requirement, generator+prompt, qc, sha256, decisions[], coverage, ready_for_agent), `contact_sheet.py`, `validate.py` (offline invariants), `judge.py` + `scorecard.py` (§6), `README.md`.

**Commands:**
```bash
cd asset_pipeline
.venv/bin/python generate.py --check           # key/model matrix + spec coverage lint
.venv/bin/python generate.py --task 440 --dry-run
.venv/bin/python generate.py --all-pilot --yes # resume-safe (cached assets skip)
.venv/bin/python validate.py                   # offline checks
```
**Cost reference:** ~$15.5 for the first 10 packages; ~$33 for the 10 mega packages (incl. video/audio). Tiny per-judge passes (~$0.6 full panel).

---

## 6. THE PACKAGE JUDGE + CLOSED LOOP (`judge.py`, `scorecard.py`)

**What:** a package-level LLM-as-judge — "are these the right assets for THIS task; could the Adobe workflow consume them?" — distinct from per-asset QC.

**Design:** 6 anchored dimensions (task_fit, completeness, executability, realism, coherence, decision_quality; 0–10 with written bands; evidence cited by asset id; machine-actionable `fix`). Per-archetype weights. **Panel:** one judge per provider — **claude-sonnet-4-6 + gemini-2.5-flash + gpt-4.1** — per-dimension MEDIAN, spread≥3 flagged low-confidence. **Red-team** hostile-client pass. **Deterministic `data_checks`** (specs declare required fields; missing mandatory/legal element → hard cap). Verdict bands: ≥8.5 client-ready / 7–8.5 minor-gaps / 5–7 needs-rework / <5 reject. **`loop_success` = deterministic ground truth** (no unresolved fixes AND no remaining defects) — overrides any rosy LLM score.

**Hardened via sabotage testing:** deliberately deleting a mandatory `warnings` field from a cosmetics-label package → the intact package scores stable ~8.1–8.3, the sabotaged one craters to 3.5 (data_checks fires, gated red-team cap overrules a lenient vote), and the repair loop **restores the field deterministically and never fakes "client-ready."** This caught & fixed real harness bugs (text truncation, program-file invisibility, image-count overflow, false-recovery).

**Commands:** `judge.py --check | --task N | --all | --task N --improve --threshold 8 --yes`. **Honest limit:** raw LLM score has ±1–2 noise on subjective dims (OpenAI lenient, Claude strict); the **deterministic layer is the trustworthy signal**.

---

## 7. THE TASK SUITES (what's authored, where)

| Suite | Location | Count | What |
|---|---|---|---|
| v1 doable | `adobe_doable_full.json` | 1,260 | The market-reality doable set (express-heavy). |
| Flagship round 3 | `asset_pipeline/flagship_specs/` + `flagship_shortlist.json` | 5 | Complex multi-deliverable print/ad tasks (5366/3437/3252/5388/1559). |
| flagship_v2 | `flagship_v2/specs/` (+ `briefs/`, `INDEX.html`) | 12 | Long-horizon mixed Adobe(+Canva+video/audio) tasks; hit previously-unused tools. |
| Mega / Definitive | `complex_benchmark/mega_benchmark.json` → `definitive_10_tasks.json` | 7→10 | Max-utilization long-horizon (18–31 connectors each); cover all 38 [C] tools. |
| **Wide-mix Adobe-only** | `complex_benchmark/adobe_only/specs/` (+ `_clusters.json`) | **66** | 100% Adobe connectors, ~20 calls + ~16 distinct tools/task, 94% output→input chaining. **This is the set the StudioBench taxonomy is built on.** Viewer: `Adobe_WideMix_Tasks.html`. |

Each wide-mix spec: `id, slug, title, category, vertical, one_line_ask, full_brief, inputs, outputs, connector_workflow[{n,tool,exec_mode,inputs_from,output}], tools_used, tool_call_count, distinct_adobe_tools, reverify`.

Supporting capability/feasibility docs in `complex_benchmark/`: `CONNECTOR_CAPABILITIES_v2.md` (the binding sheet), `FEASIBILITY.md`, `GROUNDING.md`, `SMOKE_RESULTS.md` + `SMOKE_RESULTS_v2.md` (live tool smoke-tests), `TEMPLATE_AUTHORING_GUIDE.md` (the 12 .indd/.ai the user authors for [T] tasks).

---

## 8. THE EXECUTIONS (tasks run for real) + REVIEW SITES

| Dir | Tasks | Scale | Review site |
|---|---|---|---|
| `executed_jobs/` | 5 | 9 single-tool pairs (vectorize/bg-removal/auto-tone) | `Annotation_Survey.html` (125 items) |
| `flagship_executions/` | 5 | 47 connector ops · 250 step images · 40 outputs | `Flagship_Review.html` (185 items, port 8801) |
| `mega_executions/` | 10 | ~280 connector ops · ~370 steps · ~340 before/after images · ~230 deliverables | `Mega_Review.html` (410 items, port 8802) |
| `canva_solo/` | — | Canva-alone design run (steps/designs/exports) | — |
| `bake_off/` | 4 | Adobe vs Canva, same input | `Adobe_vs_Canva_Bakeoff.html` |

**Per-execution layout:** `<id>_<slug>/{input_assets/, work/, steps/ (numbered snapshot trail), outputs/, TASK.md (work order), PLAN.md, compose_<id>.py (parametric layout = editable source), trajectory.json (every op with actor tag + requestId + before/after snap), rubrics.json, outputs/README.md (asked→produced map + honest limits)}`. Shared libs: `lib/compose_lib.py` (print typography, 300dpi units, data-merge) + `lib/traj.py` (trajectory logger). Binding protocol: `EXECUTION_CONTRACT.md`.

**Composition decision (resolved): HYBRID** — the Adobe connector does element ops (remove-bg, grade, vectorize, expand, crops per format), then a **local PIL compositor** assembles the finished multi-element layout (the connector has no headless composition tool). Data-merge done locally; video edited locally with ffmpeg; inputs generated via Veo/Sora/TTS. Every step is **honestly actor-labeled** (`adobe_connector` / `local_compositor` / `local_datamerge` / `local_video` / `local_verify`).

The review sites are self-contained HTML: left-sidebar task nav with live progress bars + annotator name + Export-scores (JSON) + localStorage autosave; per task → at-a-glance, verbatim brief, the Adobe workflow chain, input-asset groups (thumbnail + generator model + QC badge) with scorable items, output groups ("Fulfils:" mapping + exact px) with items, task-level items, and a collapsible **trajectory gallery** (every step's actor/action/note/requestId/before-after). Rubrics are **content-specific** (cite real strings like "The Clementine", "DANKE5") and authored by agents that viewed every pixel.

---

## 9. ADOBE vs CANVA BAKE-OFF (`bake_off/`)

Same identical public photo fed to **both** connectors per task (Adobe by upload; Canva by public URL — same source pixels, no input-quality advantage), then a 3-judge panel (social-media manager · graphic designer · brand director) scores deliverable fitness. Result wrapped in `Adobe_vs_Canva_Bakeoff.html` (base64-embedded, fully portable). Builder: `build_bakeoff_html.py`.

**Conclusion:** Adobe = **element/pixel processing** (can't compose layouts headless). Canva = **composition / layout / data-merge** (can't process pixels). They're complementary mirror images. (Cross-connector blockers learned: Canva can't fetch Adobe redirect/long signed URLs; Adobe rejects non-whitelisted domains like Unsplash — feed each connector via its own accepted path.)

---

## 10. THE BENCHMARK DESIGN — "StudioBench" taxonomy & evaluation

**Living spec:** `~/.claude/plans/snoopy-imagining-kite.md` (paper-style). Word export: `StudioBench_Spec.docx`. Plain-English version for the SME team: `Benchmark_Taxonomy_Proposal.{md,docx}`.

**Core principle — measurement-first, "tag, don't bucket":** real freelance jobs are messy (one task retouches a photo *and* lays out an ad *and* writes copy). Don't force each task into one category — define the skills to measure, score every task on the same rubric, and **tag** each task with what it exercises. Messy composite tasks still give clean, comparable signal.

**4 axes over a brand grounding:**
- **Grounding — 8 companies (data-derived):** classified the 66 tasks by true industry → one fictional brand per well-populated vertical, each with a frozen brand kit; every task uses only its company's assets. V1 Hearthstone (Real Estate), V2 NIGHTSHIFT (Content/Media/Music), V3 Maison Rouge (Food), V4 Apex Goods (Retail/Industrial), V5 VOLT (Apparel/Sports), V6 Aurelle (Jewelry/Luxury), V7 Northwind (Corporate/Tech/Finance), V8 LUMA (Beauty/Wellness).
- **Axis A — 8 Creative Operations** (discovered by **TF-IDF + UPGMA clustering** of tool fingerprints, not asserted), in 4 super-families: **Photo & Image** (O1 Tonal grade & restore, O2 Masked recolor & isolation, O4 Preset retouch & look-dev, O6 Stylized & duotone, O8 Stock-sourced hero), **Vector & Print** (O7 Vector & screen-print), **Layout & Data** (O5 Data-merge & layout), **Motion & Audio** (O3 Video & audio).
- **Axis B — 6 Capabilities (the scoring rubric):** K1 instruction adherence, K2 asset utilization & fidelity, K3 compositional craft, K4 creative quality, K5 communication effectiveness, K6 agentic competence (judged from the trajectory). *(Proposed upgrade: add **K7 Honesty/Calibration** — see §11.)*
- **Axis C — 4 Horizon tiers:** H1 atomic (≤3 calls) · H2 standard (4–8) · H3 composite (9–15) · H4 long-horizon (16+). **Headline analysis = how performance degrades as horizon grows.**
- **Tags:** tool-coverage + modality (image/vector/data/pdf/video/audio).

**The matrix:** an 8×8 Company×Operation grid, populated with the 66 tasks, **sparse by design** (each brand uses only realistic operations). Column totals = the cluster sizes (internally consistent).

**Evaluation protocol:** (1) execute every frozen task through Claude's Adobe connectors → capture deliverables + `trajectory.json`; (2) automated process & spec scoring from the trajectory (valid-tool rate, chaining correctness, spec adherence, recovery, efficiency = the agentic-process score); (3) SME blind annotation on K1–K5; (4) metrics: per-capability means, client-ready rate, per-operation/company/horizon breakdowns, the horizon-degradation curve; (5) leaderboard (v1 reports Claude; OpenAI added later for A/B).

**Dataset stats (v1, measured):** 66 tasks · 8 operations / 4 super-families · avg **19.9** connector calls (14–30) · 48 of ~50 connectors exercised · output→input chaining ≥~80% of steps. **Honest limitations:** photo-heavy, currently all H4 (need H1–H3 for the degradation curve), 66 is small (expand to ~150 by filling empty matrix cells), single-model v1.

---

## 11. COMPETITIVE POSITIONING — why StudioBench wins (verified)

The two rival benchmarks the user shared, grounded from their live pages:

- **Contra — Human Creativity Benchmark:** 8 single-shot generative *models*; a fixed 3-phase **human script** (Ideation→Mockup→Refinement, prior image feeds next — NOT an autonomous agent, NOT a client loop); 5 domains × 3 dims (Prompt Adherence, Usability, Visual Appeal); 5 expert evaluators/domain; pairwise **Bradley-Terry → ELO** + Likert + **Kendall's W**; ~15,000 judgments; 93 prompts. **They admit (their words):** *"process is rarely this linear… does not fully represent how creative work unfolds in practice."* **Absent:** tools, refusal/escalation, brand-contract verification, production validation, real client/revision loop, cost, process/trajectory scoring.
- **Lica — GDB (GraphicDesignBench):** 49 tasks, understand vs generate, 7 single-shot closed models (temp 0); **automated metrics only** (accuracy/Macro-F1/mAP); tiers mostly/partial/unsolved (2/25/22); grounded in generic LICA templates. **They admit:** *"relies on automated metrics and only evaluates closed-source models… both gaps we are actively fixing"* and *"fixing an 80%-right layout often takes longer than starting from scratch"* (acknowledged, **not measured**). **Absent:** tools, agent, humans, brand assets, client loop, cost, production validation.

**The one-line wedge:** *Contra and GDB grade the **picture** from a single-shot model. StudioBench grades the **worker** — an agent using real tools over long horizons on real briefs with real brand assets.* That gives us four things they **structurally cannot retrofit**: a **process** to judge, a **tool boundary** to hit (→ honesty/refusal), **brand assets** to verify against (→ objective rewards), and **multi-app handoffs** (→ provenance).

**Adversarial verification:** the competitive case was built by two strategist lenses and checked by two independent skeptics against the labs' quoted facts → **28 claims, 0 dropped, 9 fully solid, 19 tightened for precision, 13 structurally impossible for a single-shot benchmark.** (The precision correction that matters: Contra is NOT purely single-shot — it has a 3-phase scripted refinement — so say "human-scripted pipeline, not agent-driven," never "single output.")

**The recommended upgrade — the "Truth Stack" (5 scoring layers + anti-gaming wrapper):**
- **L1 Verifiable floor (RLVR):** deterministic brand-contract oracle (palette ΔE, mandatory legal-string OCR, DPI/bleed/aspect, **logo provenance: used the client's real logo vs regenerated it**).
- **L2 Honesty probe (the headline novelty):** seed briefs with deliverables the toolchain *can't* do (drawn from the **2,007 not-doable + 723 partial** audited rows) and score correct-refusal / escalation / disclosure vs **confident fabrication** → add capability **K7 Honesty/Calibration**. *"The first creative benchmark that rewards an agent for saying 'I can't do that part.'"*
- **L3 Process moat:** trajectory-pairwise ELO over the step filmstrip + counterfactual decision forks → **step-level preference pairs**.
- **L4 Taste:** SME pairwise but with **IRT + annotator-ability calibration** (beats flat Bradley-Terry).
- **L5 Outcome crown:** model the brief as a client with a hidden acceptance function → **first-pass acceptance + revisions-to-done**.
- **Wrapper:** living/adversarial brief mutation (un-memorizable) + **capability-per-dollar** + crippled-toolset twins.

**Why a data company sells this (the buyers):** the leaderboard is marketing; the **labeled trajectories are the product.** Each layer emits a distinct dataset a buyer pays for:
1. **Frontier AI lab (creative-agent RL/post-training):** buys the verified-doable tasks + client-asset packages + scored execution trajectories as a train/held-out corpus (regenerating pipeline → contamination-proof). Hook: *"Every other dataset tells your agent what good design looks like; this tells it what good work looks like."*
2. **Creative-tooling company (Adobe/Canva/Figma-type):** buys a capability-and-gap report keyed to their tool surface (feasibility map + per-tool coverage + demand-ranked roadmap + regression suite). Hook: *"We ran your tools against 3,888 real jobs and found exactly which your agent can finish, which it fakes, which it can't touch."*
3. **Enterprise design/marketing org:** buys a procurement-grade blind A/B report + a reusable acceptance harness instantiated on *their* brand kit.
4. **Model-eval / AI-safety team:** buys the hardened methodology (multi-judge + deterministic overrides, sabotage-tested, refusal/effort controls, contamination-resistant regeneration).

---

## 12. OPERATING RULES & HARD-WON LESSONS (respect these)

**User rules / constraints:**
- **Creative generation = Gemini/OpenAI only, never Claude.** Claude = orchestrator / agent-under-test / judge only.
- **Don't use people's names in chat.**
- Wants **honest, evidence-backed** claims (challenged "is the judge actually good?" → responded well to sabotage-test proof). Keep the deterministic-verification mindset; never overclaim, especially about competitors.
- Wants **rich, specific** task briefs (not job-ad fluff) and **full workflows → composed final deliverables**, not single-tool ops.
- HTML/doc style: "decent and professional, nice colors, not too fancy."
- The harness **blocks uploading workspace images to public file hosts** (data exfiltration — a hard boundary that explicit intent cannot clear). Don't work around it.

**Technical gotchas (don't re-learn):**
- No text-to-image anywhere in the MCP; verify any "doable" claim against actual tool schemas (`ToolSearch "select:<tool>"`).
- `asset_add_file` is an interactive picker — use the initialize/PUT/finalize upload path.
- Alpha flattening: image models return RGBA; naive `.convert("RGB")` → BLACK bg. Use `flatten_white()`.
- `str.format` specs: literal JSON braces must be doubled `{{ }}`.
- LLM-judge noise is ±1–2 on subjective dims (OpenAI lenient, Claude strict) → anchor caps/verdicts in deterministic checks; don't let one noisy vote gate anything.
- Surgical patch > full regen for data fixes.
- Anthropic vision judge needs max_tokens 8192 (4096 truncates mid-JSON).
- Adobe outputs can be JPEG despite `.png` naming (verify mime).
- `document_render_layout/_vector` EXPORT only (don't use them as composers); data-merge needs an authored [T] template → do it locally.
- Word docs: build with **docx-js** (no pandoc); set **fixed table layout + explicit column widths** or Word collapses columns; use cross-platform fonts (Arial / Courier New, not Consolas/Calibri-only).
- Clustering/stats are pure-Python (no numpy/sklearn in the venv).

---

## 13. FULL FILE & DIRECTORY MAP (A → Z)

```
Adobe-Freelance-Leads/
├── PROJECT_FULL_CONTEXT.md            ← THIS FILE (the master handoff)
├── PROJECT_CONTEXT_HANDOFF.md         ← older handoff (2026-06-11; early phases only)
│
│  ── DATASETS ──
├── db_all.json                        ← 3,888 clean briefs
├── adobe_doable_full.json             ← 1,260 v1 doable
├── adobe_doable_v2.json               ← 3,900 full re-grade (feasibility_v2/_final/audit/exec_mode)
├── adobe_doable_VERIFIED.json/.csv    ← 1,170 audited-doable (the trustworthy set)
├── adobe_doable_final.json, adobe_ai_sample*.json   ← superseded early sets
├── adobe_site_data.json               ← dashboard data
├── flagship_shortlist.json            ← flagship round-3 candidates
│
│  ── DATASET BUILDERS / DOCS / DASHBOARDS ──
├── build_doable_v2.py, finalize_audit.py            ← re-grade + audit
├── build_adobe_full.js / _doable.js / _ai.js        ← Word/CSV doc builders
├── build_site_data.py, site_template.html, serve_site.js, serve_doable.js
├── build_doable_html.py, build_adobe_only_html.py, build_bakeoff_html.py
├── export_db_json.py, cleanup_db.py, prune_non_adobe.py, merge_upw*.py   ← ingest utils
├── Adobe_Connector_Doable_Tasks.{docx,csv,html}     ← 1,260-task dashboard
├── Doable_Tasks.html                  ← full verified-doable browser
├── Adobe_WideMix_Tasks.html           ← the 66 Adobe-only tasks viewer
├── Adobe_vs_Canva_Bakeoff.html        ← bake-off comparison
├── Adobe_*Master*.docx, Adobe_Tasks_Export.csv, Upwork_Tasks.docx   ← clean-set / older docs
├── _archive_pre_cleanup_2026_06_08/   ← pre-clean docs
│
│  ── BENCHMARK DESIGN DOCS ──
├── Benchmark_Taxonomy_Proposal.{md,docx}   ← plain-English taxonomy (for SME team)
├── StudioBench_Spec.docx              ← paper-style spec (Word; source MD lives in ~/.claude/plans/)
├── build_studiobench_docx.js          ← the md→docx builder for the spec
│
│  ── ASSET-GENERATION PIPELINE ──
├── asset_pipeline/
│   ├── config.py specs.py personas.py generate.py judge.py scorecard.py
│   ├── manifest.py contact_sheet.py degrade.py qc.py validate.py util.py README.md
│   ├── adapters/ {openai_img, gemini_img, text_llm, media_gen, base}.py
│   ├── flagship_specs/ (5 spec_<id>.py + CONTRACT.md)
│   ├── mega_specs/ (10 spec_<id>.py)
│   ├── .env (KEYS — chmod 600, do not commit), .venv/
│
│  ── INPUT-ASSET PACKAGES (the generated "client handoffs") ──
├── input_assets/<id>_<slug>/ × 25     ← assets/ originals/ prompts/ persona.json
│       manifest.json INTAKE.md contact_sheet.html state.json judgement.json
│   (+ index.html gallery, scorecard.html/json judge leaderboard)
│
│  ── TASK SUITES / CAPABILITY GROUND TRUTH ──
├── complex_benchmark/
│   ├── CONNECTOR_CAPABILITIES_v2.md   ← THE binding capability sheet (v2.1)
│   ├── FEASIBILITY.md GROUNDING.md SMOKE_RESULTS.md SMOKE_RESULTS_v2.md TEMPLATE_AUTHORING_GUIDE.md
│   ├── mega_benchmark.json definitive_10_tasks.json definitive_benchmark.json
│   ├── flagship_candidates.json regrade_pool.json
│   ├── adobe_only/specs/*.json (66) + _clusters.json    ← the wide-mix suite (StudioBench basis)
│   └── audit/ enrich/ probes/ smoke/ regrade_* canva_assess/ canva_probe/   ← working dirs
├── flagship_v2/ {specs/(12), briefs/(12), specs_raw/, INDEX.html/md, _workflow_result.json}
│
│  ── EXECUTIONS + REVIEW SITES ──
├── executed_jobs/ (5 tasks) + Annotation_Survey.html (125 items) + rubrics/ + build_survey.py
├── flagship_executions/ (5 tasks) + lib/ web/ Flagship_Review.html (185) + EXECUTION_CONTRACT.md
│       + build_presentation.py serve_review.js
├── mega_executions/ (10 tasks) + lib/ web/ Mega_Review.html (410) + build_presentation.py serve_review.js
├── canva_solo/ {designs/ exports/ steps/}        ← Canva-alone run
├── bake_off/ {inputs/ inputs2/ adobe/ canva/ pub/ _judge.json _compare.jpg}
│
│  ── SOURCE DB + EARLY HARVEST ──
├── pipeline/ {data/adobe.db, adobe_pipeline/, scripts/, exports/, logs/}
├── tasks_*.js, build_*.js (early harvest/doc builders), package.json, node_modules/
└── .claude/launch.json                ← preview-server configs

Memory (Claude Code, persists across sessions):
  ~/.claude/projects/-Users-dhiren-Downloads-Deccan/memory/  (see MEMORY.md index)
  Relevant files: project_adobe_freelance_dataset, project_adobe_execution_survey,
  project_adobe_flagship_round3, project_adobe_flagship_executions, project_adobe_mega_benchmark,
  project_adobe_v21_dataset, reference_adobe_connector_exec_modes.
StudioBench paper spec (not in repo): ~/.claude/plans/snoopy-imagining-kite.md
```
*(Counts: ~565 JSON, ~36 HTML, ~94 PY, ~27 JS, ~149 MD, ~3,348 images, ~26 videos, ~10 audio.)*

---

## 14. COMMANDS CHEAT-SHEET

```bash
# always from project root
cd /Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads
PY=asset_pipeline/.venv/bin/python

# generate input assets for a task (resume-safe; Gemini/GPT only)
cd asset_pipeline && .venv/bin/python generate.py --task 9004 --yes && cd ..

# judge a package / run the closed repair loop
cd asset_pipeline && .venv/bin/python judge.py --task 9004 && cd ..
cd asset_pipeline && .venv/bin/python judge.py --task 2335 --improve --threshold 8 --yes && cd ..

# rebuild dashboards / docs
$PY build_doable_html.py             # Doable_Tasks.html
$PY build_adobe_only_html.py         # Adobe_WideMix_Tasks.html
node build_studiobench_docx.js       # StudioBench_Spec.docx

# serve a review site (python http.server is sandbox-blocked → use node)
node flagship_executions/serve_review.js     # :8801
node mega_executions/serve_review.js         # :8802

# Adobe connector: ALWAYS call adobe_mandatory_init first, then the upload→edit→download recipe (§3)
```

---

## 15. OPEN THREADS / NEXT STEPS

1. **Fold the competitive positioning + the Truth Stack into the StudioBench spec** (§11): add K7 Honesty capability, the Contra/GDB related-work rows, and the 5-layer evaluation protocol. (Designed; not yet written into the spec/proposal docs.)
2. **Build the headline differentiators** (when greenlit): the L2 **honesty-probe** task slice (seed infeasible briefs from the 2,007 not-doable rows + a 4-way refuse/escalate/disclose/fabricate rubric) and the L1 **brand-contract oracle** (deterministic palette ΔE / OCR / DPI / logo-provenance verifier).
3. **Balance + grow the task matrix:** add H1–H3 (low-horizon) tasks so the degradation curve is plottable; top up thin verticals; expand 66 → ~150 by filling empty Company×Operation cells.
4. **Add OpenAI as a second agent** for an A/B leaderboard (v1 is Claude-only).
5. **Wire the package judge to pre-score executed outputs** alongside the human rubrics.
6. **Scale story:** a clean AWS pipeline (Secrets Manager for keys, queue-driven generation/execution, S3 for artifacts) was discussed for future no-intervention scaling — not built.

---

## 16. HOW TO USE THIS DOC (for whoever pastes it into Claude)

- This file is **context, not instructions** — it tells Claude what exists and how it fits together.
- The **single most important section is §3** (connector execution modes). Most "can the agent do X?" questions resolve there.
- Treat the **datasets (§4)** and **capability sheet** (`complex_benchmark/CONNECTOR_CAPABILITIES_v2.md`) as ground truth; verify tool claims against live schemas before asserting feasibility.
- Respect the **operating rules (§12)** — especially *creative generation uses Gemini/OpenAI only, never Claude*, and *never overclaim* (back every claim with evidence; the project's credibility is built on adversarial verification).
- The **benchmark identity** is: *the first long-horizon, tool-using, brand-grounded creative-**agent** benchmark — it scores the worker, not just the picture.* Keep that framing.

*— End of complete context. Everything above is verified-as-built on this machine as of 2026-06-23. —*
