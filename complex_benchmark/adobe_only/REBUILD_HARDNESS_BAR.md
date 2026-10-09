# The hardness bar — every rebuilt task must clear ALL of these

Goal (owner's directive): **the task must not be trivial. It must be hard for a skilled human freelancer AND hard for the agent (Claude).** A novice should produce a visibly worse result; the agent must be able to *fail* it.

## CRITICAL: the agent never measures — the grader does
The connector has **no eyedropper, ruler, or pixel/hex/luminance readout** (see ground truth). So a "verification loop" where the **agent reads the grey card's RGB, reports recovered hex, or checks to ±3 levels** is **not doable** and collapses to a narrated no-op. Split the two roles cleanly:
- **The agent works by EYE and reports the PARAMETERS IT APPLIED.** It neutralises a grey card until it *looks* neutral; it dials per-frame temperature/tint/exposure and *reports those settings it chose* (it knows them because it set them). It must **never** be asked to read a pixel value, verify a channel level, or report a *measured* hex.
- **The numeric tolerance is the GRADER's acceptance rubric**, evaluated by the eval harness/human on the output (which CAN measure) — stated as "acceptance (grader-checked): grey card neutral within ±3 levels", never as an agent workflow step.
- **The agent's failure gate is therefore a CRAFT DECISION with a visible failure mode**, not a self-measured check (see gate 1).

## The 6 gates (all required)
1. **A failure gate the agent can actually trip — via a wrong DECISION, not a self-measurement.** Sanctioned agent-side gates: a **triage** where two look-alike inputs need different correct treatments (get it wrong and the output is visibly broken); **mask polarity / prep-before-trace** where the wrong path yields a blob or garbage paths; **per-frame divergent corrections by eye** toward one look (identical params / one global WB / per-frame auto-tone visibly fails to match); a **dependent step** where a wrong intermediate visibly breaks a downstream op. Disqualifying: open-loop "apply the slider in the stated direction", AND any gate whose enforcement requires the agent to measure pixels.
2. **A brief that states GOALS, not METHODS.** Sentences must NOT map 1:1 onto tool names. If the agent can transcribe the brief straight into calls, it is trivial. Describe the client's problem and acceptance bar; make the agent choose the operations.
3. **An agent-AUTHORED look, built from primitives.** Masked HSL / curves / split-tone / exposure the agent must reason to. NOT a preset pick, NOT `auto_tone`, NOT `quick_cut`, NOT a supplied `.xmp` / palette merely matched.
4. **Every artifact producible AS WRITTEN** — nothing from the CANNOT list; validate against REBUILD_GROUND_TRUTH.md.
5. **Difficulty from DEPTH, not breadth or plumbing.** Adaptive reasoning across DEPENDENT steps. Strip uploads, folder-creates, repeated identical calls and auto-ops before counting; what remains must still be hard. Repeating one recipe N times is breadth, not depth.
6. **A designed endpoint the agent OWNS** — a finished artifact whose distinctive quality is the agent's decision, not the client's template and not a canned tool's default.

## What makes it hard for a HUMAN too (add at least two)
- **Cross-asset consistency to a measurable target** (a common white point / warmth / black point across N differently-lit assets), not a single hero.
- **Constraint-reasoning around a tool limitation** — e.g. mask-polarity tricks (fill the art field to vectorize lettering-only; fill the lettering to halftone the art field), knockouts via `remove_background({backgroundColor})` not select→invert→fill, spot plates by masking-then-flatten *before* vectorize.
- **Triage: two superficially-similar inputs needing DIFFERENT correct treatments** (vectorize the flat raster logo, but `select_by_prompt → remove_background` the photographed one). Getting it wrong is invisible until inspected.
- **Prep-before-trace discipline** (straighten/tone/crisp/crop-to-bounds/knock-to-transparency before `image_vectorize`).
- **A deliberate TRAP**: a naive path that looks right and fails — identical params on differently-exposed frames, whole-image overlay tinting the wrong pixels, tracing the raw file.

## Measurability (grader-side — so "hard" is checkable, not asserted)
Every consistency or quality claim needs a checkable acceptance criterion the GRADER evaluates on the output (never a step the agent performs by reading pixels):
- A physical **grey / colour reference card in frame** (inputs are generated, so this is free); the agent neutralises to it **by eye**; the grader measures channel spread.
- Stated **grader tolerances**: white-point / black-point / warmth, exact output px, page-count = row-count, effective DPI at trim, bleed, CMYK.
- The agent must **REPORT the final per-image PARAMETERS IT APPLIED** (the temp/tint/exposure it dialed) — an applied-settings log, not a measurement. This makes divergent per-frame reasoning visible and gradeable. Do **not** ask it to report a *recovered/measured* hex or a read channel value.
- If the "fix" needs an **unknown specific colour matched by reading it** (e.g. solid-fill a wall scuff with the wall's exact RGB), it is **not doable** — drop it or replace with a crop/mask move that needs no readout.
- **Grade the reference region where it still exists.** If the grey/colour card is **cropped out** of the final deliverable, the grader cannot check neutrality on the delivered file. Grade neutrality on the **retained card-bearing neutralized master** (a distinct retained/exported artifact with the card still in frame) and check card-**exclusion** on the delivered product crop **separately** — never state a card tolerance against a file the workflow crops the card out of.
- **No per-record named export.** `document_render_layout` exports the **whole** merged multi-page document; you cannot pull one named record out as its own file. Make a "hero" simply the first page of the merged PDF.
- **Print/high-DPI ⇒ camera-scale inputs.** Any 300 DPI / large-frame deliverable requires the input photo declared at **~3000–4500 px camera scale** (not a ~1024–1536 px AI-gen size); the agent never upscales.
- **Nothing in a client-supplied field may telegraph the triage answer.** A supplied roster/CSV must not encode the treatment via output **file extensions** (`.svg` vs `.png`) or a "type" column, and two supplied inputs that need *different* treatments should look the **same kind** (e.g. both raw raster scans) so the agent must decide which is which. The merge binds **agent-produced** outputs the agent names per its own triage — the answer never sits in a field the agent is handed. This bans, specifically:
  - **Input filenames that describe why an input is special** — never `logo_on_door.jpg` vs `logo_flat.png`, `aerial_swimmers.jpg` among pool-shape names, `badge_gameworn.png` vs `..._proof.png`. Inputs that get different treatments share a **neutral scheme** (`ref_01`, `ref_02`, … / `capture_01`…, same extension) so the agent must open them to decide.
  - **`title` and `one_line_ask`** (both agent-facing) — they state the goal, never which input gets which treatment or "trace the flat one, not the photo".
  - The trap / triage answer lives ONLY in `inputs[].realism_notes`, `connector_workflow` step notes, and `hardness_rationale` — the grader-facing reference solution.

## IP rule (hard requirement)
No **real** person, brand, org, team, school, product, or trademark named anywhere in the spec — brief, `grounding_note`, inputs, `gen_prompt`s, outputs.
Policy (owner's decision — "social yes, marketplaces no"):
- **Name freely (realistic format / tool references):** Adobe's own products — Photoshop, Lightroom, InDesign, Illustrator, Express, Firefly (the benchmark's tools); AND the big social / video **delivery platforms used as a format or destination** — Instagram, YouTube, TikTok, LinkedIn, Facebook, Pinterest, X ("an Instagram 1:1", "a YouTube 16:9 thumbnail", "a LinkedIn banner"). These are descriptive, not impersonation.
- **Launder (they name a real business / entity, not just a format):**
  - **Marketplaces & storefront platforms** — Shopify, Amazon, eBay, Etsy, Walmart → generic ("an online store", "a marketplace channel").
  - **Every real company, person, athlete, org, school, team, product, model, or standard** — Kodak Q-13, a real skincare line like *DermaVera*, real footballers, a real academy → a generic or genuinely-invented name. A "fictional" client brand must be a **coined name that is not itself a real trademark** (an invented-sounding name can still collide with a real one — pick something distinctive).
  - Scan **every task-facing field**: `slug`, `title`, `full_brief`, `grounding_note`, `source.url`, `gen_prompt` prose, `outputs`.
- **Exempt:** `inputs[].gen_model` (the AI model that generated an asset, e.g. `gpt-image-2`, `veo-3`) is pipeline metadata — leave it. If the task was sourced from a real brief, **launder the brand to a fictional one consistently** (e.g. real footballers → fictional players + fictional "Continental Cup"; a real named school → a fictional academy). `grounding_note` may say "adapted from a real Upwork brief" but must not reproduce the real name.

## Output contract for a rebuilt spec
- Same JSON schema and field set as the current spec; **preserve `id`, `slot_id`, `slug`, `category`, `vertical`, `source.platform`.** For a REPLACE, you may change `title`/`slug`/`one_line_ask`/`full_brief`/`inputs`/`outputs`/`connector_workflow` to a new concept that fills the same slot; for a STRENGTHEN, keep the job, raise the bar.
- `workflow_nature` ∈ {create, edit, create-edit} — never "analyze".
- `connector_workflow[]` steps use ONLY allowed tools, correct `inputs_from` chaining, real `note`s; deprecated tool names replaced.
- `tool_call_count` / `distinct_adobe_tools` / `tools_used` reconciled to the actual array; do not pad with plumbing.
- Add a `hardness_rationale` field: one paragraph naming the failure gate, the human-hard element(s), the trap, and the measurable acceptance criterion.
- Keep `reverify` as a JSON string asserting no banned capability is used and the slot still matches.
