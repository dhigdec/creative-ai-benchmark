# 100-Task Rework Guidance (2026-09-10)

## The mandate (from the client/product-designer feedback)
Every task must be a **realistic, full freelance commission** — an end-to-end engagement a real
client would pay for. The small operations (remove background, tonal grade, vectorize, format
conversion, resize) are **STEPS inside a larger job, NEVER a task by themselves.** A task whose whole
point is one atomic op is invalid and must be absorbed into a bigger commission.

## Target distribution across the doc's 4 operation families (100 total)
- **Photo & Image — 30** (signature: tonal grade & restore, masked recolor & isolation, preset retouch, stylized & duotone, stock-sourced hero)
- **Vector & Print — 15** (signature: vector art, screen-print separations)
- **Layout & Data — 35** (signature: data-merge, multi-page layout, composed collateral)
- **Motion & Audio — 20** (signature: short video, audio)

Family = the family of the task's PRIMARY deliverable. A task may (and should) use ops from other
families as steps; it is classified by where its headline deliverable lands.

## The composition engine rule ("deliverable picks the engine")
- **HTML → Adobe Express authoring** for DESIGNED one-off collateral: posters, social post sets
  (mixed 1:1/4:5/9:16 in ONE export), pitch/brand decks, ad units, one-page web/PDP mockups,
  infographics, menus-as-design. Fully headless, produces a native EDITABLE Express doc. This is the
  default for Layout & Data collateral now — it REPLACES the old "populate a pre-authored .indd" pattern.
- **InDesign data-merge** ONLY for genuine variable-data runs where one record = one page at volume:
  catalogs, badge/name-tag batches, certificates, price lists, direct-mailers, labels. Requires a real
  merge template; keep these to the subset that genuinely needs record-per-page.
- Never end a task in `document_render_layout` against a template we don't actually have.

## What makes a task HARD (decision-density, NOT step-count)
Frontier agents (GPT-6 Astra, Opus, Sonnet) are explicitly good at long multi-step workflows. Length =
tedium, and tedium is exactly what they absorb. So hardness must come from JUDGEMENT the agent can get
wrong. Every task MUST carry at least two of:
1. **An irreversible early craft decision that visibly breaks a later deliverable** (a wrong grade/white
   point/crop/type choice made in stage 2 that only shows as broken on the stage-7 collateral).
2. **Triage of look-alike inputs needing DIFFERENT correct treatments** (vectorize the flat raster mark,
   but cut out the photographed one; grade the card-bearing master, exclude the card from the crop).
3. **Cross-asset consistency to a measurable target** across N differently-lit/shot sources (one white
   point / warmth / black point / crop logic), not a single hero.
4. **Constraint-reasoning around a tool limitation** (square hero → 9:16 with generative-expand banned;
   knockout via remove_background(backgroundColor) not select→invert→fill; spot plates by mask-then-flatten
   BEFORE vectorize; enclosed letter-counters can't be punched by remove_background).
5. **Taste: generate N distinct options and justify a pick** where a non-designer picks wrong.
6. **Element extracted ONCE then reused, identical, across many collaterals** (a crest/logo/product
   silhouette pulled and reused on poster + social + deck; brand drift is the failure mode a VLM shows).

## The VLM-substitutability gate (every task must pass)
Imagine the client uploads the assets and pastes the brief into a frontier image model. If what comes
back is something they could ship, the task is INVALID. A valid task fails a one-shot regen on
**identity** (real product/logo/face preserved, not redrawn), **spec** (exact px/format/record-count),
or **editability** (a native editable doc, not a flat raster). State the rebuttal per task.

## Hard constraints (unchanged, still enforced)
- Only VERIFIED connector tools (see CONNECTOR_CAPABILITIES_v3.md). No banned capability: text-to-image,
  generative fill, AI object removal, background-replace-by-prompt, cartoonize, upscaling, OCR, PDF text
  edit, image→PDF, photo compositing, video trim-to-timestamp, video format conversion, per-artboard
  named export, >20-file batches. `image_generative_expand` (outpaint) is the ONLY generative exception.
- **No upscaling** — outputs ≤ source px; print/high-DPI ⇒ camera-scale inputs (~3000-4500px).
- **The agent never measures a pixel/hex** — it works by eye and REPORTS the params it applied; numeric
  tolerances are the GRADER's rubric.
- **Brief states GOALS not methods** — never leak the trap, the triage answer, or map sentences 1:1 to tools.
- **IP-safe** — no real brand/person/trademark. Social platform names (Instagram/YouTube/LinkedIn) OK as
  format descriptors; marketplaces stay generic. Fictional brands must be genuinely coined.
- **Brand identity adds price-range + demographics, made LOAD-BEARING** — the design must visibly differ
  if the price band were different (a $40 taqueria vs a $200 tasting menu look different).

## ORCHESTRATION DEPTH (hard requirement, raised 2026-09-10)
A task is not a pipeline. Real freelance work loops: you lay something out, discover it does not hold, and
go back into the image editor to fix the thing you made three steps ago. Every task must encode that.

**1. Tool breadth: at least FOUR distinct Adobe surfaces per task.**
Count distinct products, not tool calls. The surfaces: Lightroom/Photoshop imaging, Illustrator vector,
InDesign layout and data-merge, Express/HTML authoring, Premiere video and audio, Adobe Fonts, Stock and
Boards. A task touching only one surface is rejected regardless of how many calls it makes.

**2. At least TWO UN-ANTICIPATABLE EMPIRICAL CHECKPOINTS.**
(This REPLACES the earlier "declare two revisit loops" rule, which was wrong. Mandating loops rewards bad
planning: an agent that sequences well and gets it right first time would score worse. Never design a task
that punishes competence.)

A checkpoint is a point where the outcome **cannot be known without running the operation and looking at the
result**. Loops must EMERGE from the material reality of the assets and the tools, never be scripted.

Test every candidate with three questions. If any answer is "yes", it is NOT a checkpoint:
- (a) Could a careful agent who read the brief and the tool docs avoid it by ordering, or by simply doing it
  right the first time?
- (b) Does the brief, the deliverable list, or an earlier step already STATE the thing the loop "discovers"?
  (A brief that asks "tell us how small the mark can safely go" cannot later "discover" the mark fails small.)
- (c) Is it merely a propagation re-run (re-merge, re-export after an input changed)? That is the TAIL of a
  checkpoint, not a checkpoint.

Legitimate sources of genuinely un-anticipatable information:
- What a PDF-to-InDesign conversion actually exposes as editable frames (granularity is not under your control).
- Whether a subject selection clips, or leaves a fringe, on this specific photograph.
- Whether a traced mark still holds at its real reproduction size on the real ground colour.
- Whether a merged record's text overflows its frame at true trim.
- How the Express importer normalizes a particular construct (returned HzHTML is the only way to know).
- Whether a licensed stock frame actually sits with the graded set once the two are finally adjacent.
- Whether a generative expand builds edges that match the house neutral.

Rules that follow from this:
- The TASK must not script the loop. The brief states goals; only the grader-facing reference solution may
  note where a checkpoint is likely to fire.
- Never let a step claim it fixed a defect that a later step then "discovers" is unfixed. The auditors caught
  this repeatedly; it is the clearest tell of a manufactured loop.
- Count surfaces honestly: `image_vectorize` is a Photoshop-family tool, NOT an Illustrator surface.
  `document_render_vector` and `document_merge_data_vector` are dead headlessly, so a true "Illustrator
  surface" is rarely real. Do not inflate the count.
- A long loop-free opening run is acceptable and often correct. What is NOT acceptable is a task whose
  entire trajectory re-sequences into a straight line producing identical deliverables.

**3. Deliverables must span at least THREE distinct classes.**
Classes: graded raster set; isolation/cutout set; vector artwork system; laid-out print document;
editable Express collateral; data-merged batch document; video or motion set; brand or handover document.
**N crops or N recolours of one image is ONE deliverable, not N.** A deliverable set that is only
"the same picture at different sizes" is rejected.

**4. The trajectory must be non-linear and dependency-bound.**
A wrong early decision must FORCE a revisit, not merely look bad. State which one.

**5. Realism bar: it must read like a posted freelance job.**
The kind of multi-part commission actually listed on freelance marketplaces: a launch kit, a store opening,
a season rollout, a rebrand rollout, a catalogue plus campaign. Not an exercise.

## Cultural frame: WESTERN / EUROPEAN / NORTH-AMERICAN ONLY (hard requirement)
The benchmark is annotated by international annotators, so every task must sit in a Western cultural frame.
This applies to ALL 100 tasks, across brief text AND generated assets:
- **Brand & persona names:** Western / European / North-American (English, French, Italian, Spanish/Latin,
  German, Nordic are all fine). NO Indian / South-Asian / East-Asian / Middle-Eastern names, deities,
  or coined names built from those languages (e.g. no "Rukmini", "Kanaka Mahal", "Tamil ...").
- **Culture & occasion:** Western holidays/occasions only (e.g. Thanksgiving, Christmas, Halloween,
  Fourth of July, a European football league, a farmers' market) — NOT Diwali, Navratri, Pongal, Holi,
  cricket/IPL, mehndi, etc. A festive/seasonal task uses a Western festival.
- **Products & cuisine:** Western product worlds and food (a taqueria, a trattoria, a diner, a patisserie,
  a steakhouse, a wine bar) — NOT biryani/dosa/masala-chai/paneer or an Indian sweet shop.
- **Generated asset imagery (the gen_prompt is where this bites):** any person is Western/European-looking;
  any signage/packaging text is in a Western language; architecture, interiors, streetscapes, props and
  styling read as North-American or European. A model shoot, a headshot batch, a property tour, a menu —
  all Western settings. Never specify saris/kurtas/jhumkas, temple/mandir architecture, rangoli, Indian
  street scenes, or non-Latin script unless the task's whole point is a Western brand's "imported" product
  (rare; avoid).
- **Existing non-Western tasks to convert when absorbed:** AO-63 (cricket → a Western sport, e.g. lacrosse
  or amateur football), AO-67 (Tamil festive banners → a Western seasonal event), AO-86 (masala/chai tea →
  a Western herbal/botanical tea or coffee house), AO-115 (Rukmini/jhumka → a Western/European fine-jewelry
  house with Western pieces: pendants, signet rings, tennis bracelets).
The reconciled ledger (`PORTFOLIO_LEDGER_v2.json`) is already keyword-clean, but Stage C must apply this to
every gen_prompt and re-check every coined name against it.

## Reuse the existing corpus
Preserve the 68/100 adversarial-verified work. ABSORB existing task concepts + their assets/verticals as
STAGES of the new engagements — do not throw away good inputs. Combine several thin existing tasks into
one rich commission. Generate net-new engagements only to fill family quotas the existing pool can't reach.
