# Phase 0 — Task Validation

*The first filter that runs once per scraped task, **before** it is ever queued for an agent run or scored. Phase 0 decides whether a **task** is worth keeping. It judges **only the task itself — the brief and its metadata.** It does **not** look at the asset files (those are checked separately in **Phase 1 — Asset Validation**) and it does **not** score the agent (that happens later, against the agent's output). A task must clear Phase 0 before it is ever passed on to asset validation.*

---

## 0.1  What Phase 0 does, in one breath

A task is scraped from the wild, lightly polished, given fictional client/brand details, and tagged. Then it passes through **two independent gates**, each looking at a different surface of the task:

| Gate | Looks at | Asks |
|---|---|---|
| **Gate A — Task Quality** | the **brief / the ask** | Is this a good, clear, doable task a real client would pay for? |
| **Gate B — Metadata Correctness** | the **tags** on the task | Are the labels describing this task right and consistent? |

*(The third surface — the actual **asset files** + their origin — is validated in **Phase 1 — Asset Validation**, a separate stage. It is intentionally **not** part of Phase 0.)*

Every check resolves to **Pass / Fix / Reject**, and is marked **(code)** if a script can decide it, or **(expert)** if it needs a human eye. A task is **VALIDATED only when both Phase-0 gates (A and B) Pass** — and only then does it move on to Phase 1 (assets). The verifiers we *write* while gating become the **scoring contract** — the exact checks run later against the agent's output. So Phase 0 does double duty: validate the task now, define how it'll be scored later.

**The pipeline order:**

1. **Scrape** a real freelance brief → 2. **Polish** the wording + add fictional client/brand details → 3. **Tag** the metadata → 4. **Gate A** (task quality) → 5. **Gate B** (metadata correctness) → **VALIDATED / FIX / REJECT**.
*A validated task then goes to **Phase 1 — Asset Validation** (the files), and — much later — the scoring phase runs the verifiers defined here against the agent's deliverable.*

**Verdict words — used the same way everywhere:** at the **check** level → *Pass / Fix / Reject*; at the **task** level → *Admitted / Fix / Reject*.

---

## 0.2  Gate A — Task Quality (is the *task* good?)

Gate A judges **only the brief** — the words of the commission a real client would hand over. It does not look at tag values (that's Gate B) or the asset files (that's **Phase 1 — Asset Validation**, a separate stage). A task clears Gate A when a competent freelancer reading only the brief would know exactly what success looks like, believe it can be done with the tools on hand, and not need to email back asking what the client meant.

| # | Dimension | What it means | Atomic sub-checks | Pass / Fix / Reject | Who |
|---|---|---|---|---|---|
| **A1** | **Real-world brief** | Reads like a genuine commission someone would actually pay for. | • names a concrete deliverable • has a plausible purpose/audience • not a toy/puzzle/"test the AI" prompt | **Pass** plausible paid job · **Fix** real ask buried under fluff → trim · **Reject** contrived or no real-world analog | expert |
| **A2** | **Clear & unambiguous** | A reader lands on exactly one interpretation. | • each instruction has a single reading • no undefined "make it pop" • no contradictory directives | **Pass** one obvious reading · **Fix** one fuzzy phrase fixable in an edit · **Reject** two+ valid readings or self-contradiction | expert |
| **A3** | **Tool-feasible** | Doable with the agent's actual toolset — **this is where "not-doable" tasks are caught and rejected.** | • every required action maps to an available connector • no banned capability (**text-to-image / from-scratch logo or illustration with no source asset**) • output format is one the tools can make | **Pass** every step has a tool · **Fix** one out-of-scope flourish removable without gutting the task · **Reject** core deliverable needs a capability we don't have → set `feasibility = no` and drop | code (tool-map) + expert |
| **A4** | **Self-contained** | Everything essential is in the brief or its inputs. | • all referenced inputs named • no "as we discussed" dependency • required parameters (size, count, platform) stated or safely inferable | **Pass** nothing essential missing · **Fix** one gap fillable with a stated default · **Reject** a load-bearing input/instruction is absent and unrecoverable | expert |
| **A5** | **Measurable outcome** | An objective pass/fail criterion *can* be written for the result. | • success is checkable by observation, not pure taste • constraints are concrete (dims, format, count, element present) • "done" has an end state, not "improve" | **Pass** clear objective bar exists · **Fix** add one quantifier to make a soft ask checkable · **Reject** success is purely subjective with no anchorable criterion | expert |
| **A6** | **Single coherent commission** | One unified job, not several unrelated tasks bundled. | • all steps serve one end deliverable • shared subject/assets/theme • any multi-step flow is sequential toward one output | **Pass** one job (may be multi-step) · **Fix** trim one tangential add-on · **Reject** two+ independent jobs that should be separate tasks | expert |
| **A7** | **Right difficulty for its horizon** | Effort fits the task's intended length — not trivial, not unbounded. | • not a one-tool one-liner • not too broad to finish in its horizon • **step count sits within the H-band for its `est_calls`** (observable, see §0.3) | **Pass** complexity matches horizon · **Fix** scope up/down by a step · **Reject** trivially one-shot, or unbounded with no finish | code (`est_calls` band) + expert |
| **A8** | **Internally consistent** | The brief doesn't fight itself (numbers, specs, references all agree). | • counts/dims/dates/prices consistent • no instruction references a thing the brief never provides | **Pass** self-consistent · **Fix** one stray reference correctable · **Reject** fundamentally inconsistent brief | code + expert |
| **A9** | **Rubric-writable** | We can draft a concrete, atomic acceptance checklist for this task *now*. | • at least one objective verifier is drafted at gating time • each drafted verifier is atomic + observable + (code)/(expert)-tagged | **Pass** a clean verifier bundle is drafted · **Fix** sharpen a vague verifier · **Reject** no checkable acceptance criterion can be written (overlaps A5 → reject once) | expert |

> *Note: cross-task duplicate detection is **not** in Gate A — that's a corpus-level check and lives in Gate B (B5). A8 covers only a task's **internal** consistency.*

### The "Good Task" definition

**INCLUDE a task if it…**
- Reads like a **real commission** someone would genuinely pay for.
- Has **one clear goal** with a single obvious interpretation.
- Is **fully doable with the agent's tools** (edit, resize, crop, mask, retouch, vectorize, layout, data-merge, template-fill, stock-license, video/audio cut, etc.).
- Is **self-contained** — every essential input/parameter present or safely inferable.
- Has an **objective acceptance criterion** you could write in advance.
- Is a **single coherent commission** working toward one deliverable.
- Sits at the **right difficulty for its horizon** — real work, but bounded.
- Is **meaningfully distinct** from tasks already accepted.

**FILTER OUT a task if it…**
- Needs **text-to-image / generative image creation** from a prompt. **Excluded** (A3 → `feasibility = no`).
- Needs a **logo, illustration, or artwork invented from scratch** with no source asset. **Excluded** (A3 → `feasibility = no`).
- Is a **toy, puzzle, riddle, or "test the AI"** prompt with no real-world analog.
- Is **ambiguous** (two+ valid readings) or **self-contradictory**.
- **Can't be done with our tools** (needs a banned capability or an unreachable external system).
- Is **missing an essential input/instruction** that can't be recovered or defaulted.
- Has **no objective success criterion** (success rests entirely on taste).
- **Bundles unrelated jobs** that should each be their own task.
- Is **too trivial** (one-tool one-liner) **or too sprawling** to finish in its horizon.
- Is a **near-duplicate** of an already-accepted task (caught at Gate B).

---

## 0.3  The metadata tag schema (the tags every task carries)

These are the labels every admitted task ships with. **How assigned:** `A` = auto-derived from the workflow string, `H` = human/judge, `A+H` = auto-proposed then human-confirmed. *(The workflow is stored as one arrow-delimited string, e.g. `image_remove_background (...) -> image_apply_auto_tone (...) -> ...`; auto-derivation first **parses** it: split on `->`, strip the parenthetical notes, de-dupe the tool tokens.)*

### A. Core operation & structure (mandatory)

| Tag | Captures | Allowed values | Assigned | Why it matters |
|---|---|---|---|---|
| **`operation`** | The single dominant operation (our 8 data-derived clusters) | **O1** tonal grade & restore · **O2** masked recolor & isolation · **O3** video & audio · **O4** preset retouch & look-dev · **O5** data-merge & layout · **O6** stylized & duotone · **O7** vector & screen-print · **O8** stock-sourced hero | A+H | The primary capability slice; drives Gate B's operation-match check |
| **`family`** | The 4 super-families | `Photo & Image` (O1,O2,O4,O6,O8) · `Vector & Print` (O7) · `Layout & Data` (O5) · `Motion & Audio` (O3) | A (from `operation`) | One-glance portfolio balance across the four families |
| **`output_modality`** | What the deliverable **is** | `image` · `vector` · `document` · `video` · `audio` · `data` | A+H | Must match the actual deliverable (= Suma's "Asset Type" axis) |
| **`workflow_tag`** | Create / Edit / Analyze posture | `Create` · `Edit` · `Analyze` · or combos (`Create+Edit`, `Edit+Analyze`, …) | A+H | = Suma's "Workflow Tags"; net-new vs transform vs extract/judge |
| **`deliverable_type`** | The concrete artifact noun the brief asked for | derived from the brief's `task_type`, e.g. `menu` · `flyer` · `poster` · `banner` · `logo` · `social-post` · `story` · `ad` · `business-card` · `certificate` · `brochure` · `product-shot` · `headshot` · `label/packaging` · `catalog` · `thumbnail` · `sizzle-reel` · `explainer-video` · `podcast-audio` · `restored-photo` · `screen-print-seps` (extend as needed) | A+H | The human-readable handle |
| **`horizon_tier`** | Task length | **H1** ≤3 calls · **H2** 4–8 · **H3** 9–15 · **H4** 16+ — banded off `est_calls` | A (from `est_calls`) | Balances trivial vs long-horizon tasks |
| **`est_calls`** | Estimated connector-call count (the **cost / effort proxy**) | integer | A (audited) | The supply/cost-planning number; horizon is banded from it |

### B. Context (mandatory)

| Tag | Captures | Allowed values | Assigned | Why |
|---|---|---|---|---|
| **`domain`** | Industry the brief lives in | `food-bev` · `restaurant` · `beauty-cosmetics` · `fashion-apparel` · `jewelry` · `real-estate` · `tech-saas` · `fitness-wellness` · `events-weddings` · `education` · `finance` · `healthcare` · `nonprofit` · `ecommerce-retail` · `hospitality-travel` · `automotive` · `music-entertainment` · `professional-services` · `generic` | A+H | = Suma's "Domain"; drives domain spread |
| **`brand_persona`** | The fictional brand the task wears | free text (e.g. `"Maison Rouge / French-bistro"`) or `none` | H | Keeps tasks concrete, not generic (free text → presence-only check) |
| **`capability_footprint`** | Which **scoring buckets** the task is designed to exercise | any subset of the 7: `Instruction Following` · `Asset Utilization` · `Brand Alignment` · `Technical Quality` · `Creative Quality` · `Process` · `Honesty` | A+H | Tells the scoring phase which dimensions must light up for this task |

### C. Difficulty axes (optional, 1–5 each — all five or none)

| Tag | Captures | 1 → 5 |
|---|---|---|
| `planning_complexity` | sequencing/branching needed | linear recipe → multi-branch, reorder-sensitive |
| `brand_strictness` | how tightly outputs must obey the brand kit | none → exact hex/font/logo-safe-zone enforced |
| `tool_diversity` | count of distinct connectors (bucketed) | 1–2 tools → 16+ distinct tools |
| `visual_density` | content/elements on the canvas | sparse → dense multi-element |
| `creative_freedom` | open-ended vs pinned target | match-this → open brief |

### D. Feasibility & licensing (mandatory)

| Tag | Captures | Allowed values | Assigned | Why |
|---|---|---|---|---|
| **`feasibility`** | Audited doability | `full` (headless-doable) · `template` (Express/template-fill path) · `partial` (some steps need outside-connector work) · **`no`** (needs from-scratch art / text-to-image — **filtered out at Gate A3**) | A+H (audited) | The doability truth; `no` rows never reach Gate B |
| **`grade`** | Long-horizon weight (separate axis) | `express` · `full` · `flagship` | A+H | The "how heavy" weight, distinct from doability |
| **`execution_mode`** | Per-step + task-level runnability against the **real** connector | `[C]` headless · `[W]` interactive-widget (Express needs a human to pick) · `[A]` async-widget (video/audio, polls in-product) · `[T]` authored-template (needs a user .indd/.ai with merge fields) · or **mixed** (`[C]+[T]`) | A (lookup, see Appendix) | Prevents claiming a `[W]/[A]/[T]` task is headless |
| **`tool_coverage`** | Distinct connectors the task touches | integer + the explicit tool list (parsed from the workflow string) | A | Proves suite coverage; drives `tool_diversity` |
| **`licensing_clean`** | License status — **records the verdict Gate C6a produces** (a transcription, not an independent judgment) | `clean` · `stock-required` · `risk` | A (from C6a) | Keeps the benchmark redistributable |

> **Reconciliation with Suma's plan:** *Domain* → `domain`; *Asset Type* → `output_modality` + `deliverable_type`; *Workflow Tags* → `workflow_tag`; her 6 harvest-level families collapse into our 4 `family` values, with `operation` (O1–O8) as the finer layer underneath. *(Supply note: in the raw harvest, template-design work dominates demand — so when scaling to 100, consciously over-sample the harder operations, O2/O5/O7/O3, rather than letting templates flood the set.)*

---

## 0.4  Gate B — Metadata Correctness (are the *tags* right?)

Gate B runs after Gate A. It assumes the task is good and asks only **"are the labels right and consistent?"** It never re-judges brief quality (that's A) or the files (that's C).

**B1 — Presence.** Every mandatory tag exists. *Pass:* all present. *Fix:* ≤2 trivially-derivable tags missing (`family`, `horizon_tier`, `tool_coverage`) → auto-derive. *Reject:* a non-derivable mandatory tag missing (`operation`, `feasibility`, `output_modality`, `est_calls`). **(code)**

**B2 — Valid values.** Every tag sits in its controlled vocabulary (`operation ∈ {O1…O8}`, `family ∈ {the 4}`, `output_modality ∈ {image,vector,document,video,audio,data}`, `feasibility ∈ {full,template,partial,no}`, `execution_mode ∈ {[C],[W],[A],[T] or mixed}`, `licensing_clean ∈ {clean,stock-required,risk}`, difficulty axes integers 1–5). *Fix:* typo/alias → normalize. *Reject:* value outside the vocab with no mapping. *(Exception: `brand_persona` is free text — presence-only, not value-checked.)* **(code)**

**B3 — Consistency with the brief & workflow (the heart of Gate B).**

| # | Check (tag ↔ ground truth) | Pass / Fix / Reject |
|---|---|---|
| B3.1 | **`operation` matches the workflow** — the tagged O equals the dominant operation in the parsed workflow | Pass: matches · Fix: off-by-one within the same family → retag · Reject: wrong family entirely |
| B3.2 | **`output_modality` matches the deliverable** — vectorize→`vector`, quick-cut→`video`, data-merge→`document`, speech-enhance→`audio`, analysis-only→`data` | Pass: match · Fix: pick the primary of multiple outputs · Reject: modality contradicts the deliverable |
| B3.3 | **`deliverable_type` matches the brief** — the noun the brief actually requested | Pass: match · Fix: brief says "social graphic", tagged `flyer` → retag · Reject: deliverable absent from the brief |
| B3.4 | **`workflow_tag` matches posture** — Create/Edit/Analyze matches make-new vs transform vs extract | Pass: match · Fix: add a missing combined facet · Reject: `Analyze` on a task that edits an asset |
| B3.5 | **`horizon_tier` matches `est_calls`** — the H-band equals the estimated call count | Pass: in band · Fix: boundary case → snap to band · Reject: off by ≥2 bands (H1 on a 20-call task) |
| B3.6 | **`tool_coverage` is real** — the listed tools equal the distinct tools parsed from the workflow | Pass: agree · Fix: a step's tool missing → regenerate from the parse · Reject: listed tools that never appear (fabricated coverage) |
| B3.7 | **`execution_mode` matches the tools** — per-step mode follows the Appendix lookup; task-level mode is the union | Pass: agree · Fix: one step mis-tagged but union still right · Reject: labeled headless `[C]` but uses `[W]/[A]/[T]` tools (false-headless) |
| B3.8 | **`feasibility` matches A3's verdict** — Gate A *decides* feasibility; B only checks the recorded value matches (`full` only if every step is `[C]`; `template` implies a `[W]` path; `no` should never appear here, since A3 rejected it) | Pass: matches A3 · Fix: `full` with one `[T]` export step → downgrade to `partial` · Reject: recorded value contradicts A3 |
| B3.9 | **`capability_footprint` ⊇ what the rubric scores** — every bucket the task's verifier bundle scores is listed, using the 7 canonical bucket names (no parallel vocabulary) | Pass: footprint = the rubric's buckets · Fix: add a missing bucket · Reject: footprint claims a bucket the rubric has no check for |
| B3.10 | **`domain` / `brand_persona` are concrete & matched** — domain matches the industry; the persona names a brand actually in the brief | Pass: match · Fix: refine the industry bucket · Reject: domain contradicts the brief, or `none` on a brand-heavy brief |

**B4 — Cross-tag coherence.** Tags agree with each other. *e.g.* `family` ↔ `output_modality` plausible (a `Vector & Print` task can't be `audio`); `horizon_tier` ↔ `tool_diversity` sane (an H4 flagship shouldn't use 1 tool); `workflow_tag = Analyze`-only ↔ `output_modality = data`. *Reject:* an impossible pairing. **(code)**

**B5 — Corpus saturation (dedupe + supply balance).** A corpus-level check: is this task a near-duplicate of one already accepted, **and** is its `(family, operation, domain)` cell already over its quota? *Pass:* adds new coverage. *Fix:* retarget one parameter to differentiate a near-twin. *Reject:* a semantic duplicate, or a cell already saturated (redundant for supply). **(code + expert)**

**Gate B verdict:** **Pass** = all checks Pass (after Fixes). **Fix** = only Fix-level issues → auto-derive/normalize or annotator retags, then re-run B. **Reject** = a tag misrepresents the task (false-headless, wrong modality, wrong feasibility, fabricated coverage) → the task content may be fine, but the **labels** are wrong → bounce to re-tag (not to Gate A).

---

## 0.5  Phase 1 preview — Asset / Package validation *(a separate stage, not Phase 0)*

**Asset validation is Phase 1**, run only on tasks that have already passed Phase 0. It looks **only at the bytes that ship with the task** and where they came from — never the brief (that was Gate A) or the tags (Gate B). It is summarised here only so the boundary is clear; the full **Phase 1 spec** owns these checks. *(This is where Suma's "Asset Validation" lives.)*

| # | Dimension | What Phase-1 asset validation checks (files + provenance only) | Pass / Fix / Reject | Who |
|---|---|---|---|---|
| **C1** | **Completeness** | Every asset the brief references is physically attached and resolves — no missing fonts, no "see attached CSV" with no CSV. | Pass: all present & resolve · Fix: ≤2 re-fetchable assets missing · Reject: a core asset (the .indd, the source PSD) missing & unrecoverable | code + expert |
| **C2** | **File integrity / openability** | Each file opens in its format, isn't truncated/corrupt, MIME matches extension, fonts install, PDFs aren't locked. *(Integrity of the bytes — not feasibility of the ask; that's A3.)* | Pass: all open & parse · Fix: recoverable (re-export/repair/transcode) · Reject: corrupt with no recoverable source | code |
| **C3** | **Realism / authenticity** | Assets look like real working material, not gutted templates — real logos vs lorem-ipsum, plausible photos, real menu items/prices vs "Item 1 / $X.XX". | Pass: genuine material · Fix: isolated placeholder slots · Reject: pervasive dummy content | expert + code (lorem-ipsum / "$X.XX" detection) |
| **C4** | **Brand coherence (within the kit)** | The supplied assets are internally consistent as one brand — logo, palette, fonts, imagery share a voice. *(Scoring later judges the agent's output for on-brand-ness; C4 only judges the inputs.)* | Pass: one coherent kit · Fix: drop a stray asset · Reject: assets from clearly different brands | expert |
| **C5** | **No answer-leakage in the files** | None of the attached files **is** or **contains** the finished deliverable — no exported final PDF next to the "make this" source, no fully-laid-out comp in a hidden layer. *(Gate A handles leakage in the brief text; C5 handles it in the bytes.)* | Pass: no solution present · Fix: quarantine a leaky exemplar · Reject: the task **is** the attached finished file | code (rendered-final / hidden-layer detection) + expert |
| **C6a** | **License / usage rights** | Each asset has a usage right that permits benchmark + training use — stock has a license/ID, fonts are embeddable, no watermarked comps, brand assets aren't confidential IP. **This is the authoritative license verdict** (Gate B's `licensing_clean` just records it). | Pass: permissible for all · Fix: swap a risky asset for a licensed equivalent · Reject: unlicensable / watermarked / confidential | code (watermark, font-embed flag) + expert |
| **C6b** | **PII / confidentiality** | No personal data (names, emails, faces of real private individuals), no confidential business info, in any file or data row. | Pass: clean · Fix: redact a field · Reject: PII-bearing and unredactable → must drop | code (PII scan) + expert |
| **C7** | **Provenance consistency** | Files don't contradict each other or the metadata — image dims match the stated canvas, CSV columns match the merge template, declared format == actual format. | Pass: mutually consistent · Fix: one fixable mismatch · Reject: irreconcilable (data schema ≠ template fields) | code |
| **C8** | **Package decision-quality** | Holistic call: given C1–C7, is this a package a competent freelancer would actually accept and work from? Catches sets that pass every line-item but are collectively junk. | Pass: a real, workable kit · Fix: admit with the noted fixes · Reject: collectively not benchmark-worthy | expert |

---

## 0.6  Phase-0 verdict logic

A task runs through **both Phase-0 gates (A and B)**; each check returns Pass / Fix / Reject. The task-level verdict:

- **REJECT** if **either** gate returns a Reject. *(Short-circuit allowed — no point fixing a task that can't be done at all — but it's usually worth running both gates so remediation gets the full issue list in one pass.)*
- **FIX** if neither gate Rejects but **at least one** returns Fix → send to the remediation queue (re-word the brief, re-tag, fill a default) → **re-run both gates**.
- **VALIDATED** **iff** Gate A = Pass **AND** Gate B = Pass → the task moves on to **Phase 1 — Asset Validation**.

**What a validated task carries forward:** (a) the clean, correctly-tagged task, and (b) the **verifier bundle** — the concrete pass/fail checks and expert rubric items surfaced while gating ("output must have 3 panels", "final PDF must embed the brand font", "menu prices must match the supplied CSV"). At scoring time, those exact verifiers are run against the agent's deliverable. **The gates author the scoring contract; scoring executes it.**

**The MECE boundary, stated plainly:**
- *Phase 0 vs Phase 1:* Phase 0 judges only the **task** (brief + tags); the **asset files** are Phase 1. The two never overlap.
- *Inside Phase 0:* Gate A never inspects tag values; Gate B never re-judges brief quality. If the **task** is bad → Gate A. If the **labels** on a good task are wrong → Gate B.
- *Feasibility* means two different things: **Gate A3 (Phase 0)** = *can the ask be done with our tools at all*; file-openability is a Phase-1 check.
- *Dedupe* is corpus-level → **Gate B5** owns it; Gate A only checks a task's **internal** consistency.

---

## 0.7  Worked example — a restaurant tri-fold menu

**Scraped task (post-polish):** *"Design a print-ready tri-fold menu for Maison Rouge, a modern French bistro. Use the attached logo and brand fonts. Lay out the dishes and prices from the attached CSV across three panels. Match the warm, earthy brand palette. Export a print-ready PDF with bleed."*
**Attached package:** `maison_logo.svg`, `brand_fonts/` (2 OTFs), `menu_items.csv` (28 rows: dish · description · price · panel), `palette.png`, `brief.txt`.

**Gate A — Task:** doable via data-merge + layout + PDF-export (Pass) · unambiguous tri-fold print PDF with bleed (Pass) · no answer leaked in the wording (Pass) · single coherent commission (Pass) · a verifier bundle is writable (Pass). → **Gate A = PASS.**

**Gate B — Metadata:** `operation = O5`, `family = Layout & Data`, `output_modality = document`, `workflow_tag = Create+Edit`, `deliverable_type = menu`, `est_calls = 11 → horizon H3`, `domain = restaurant`, `feasibility = template`, `execution_mode = [C]+[T]` all present & consistent (Pass) — **except** the `workflow_tag` was first tagged `Create` only, but the task also transforms supplied photos → **Fix** (retag `Create+Edit`). → **Gate B = FIX.**

**Combine (Phase 0):** A = Pass, B = Fix, no Rejects → **VERDICT: FIX.** **Remediation:** retag the workflow tag → re-run both gates → **VALIDATED.**

**→ The validated task now passes to Phase 1 (Asset Validation),** where the *files* get checked — and Phase 1 catches two things Phase 0 never looks at: one font OTF lacks an embedding license (Fix → swap), and one CSV row says `panel = 4` on a *tri*-fold (Fix → re-map). Those are Phase-1 fixes, not Phase-0 ones.

**Verifier bundle handed to scoring** (authored here, run later against the agent's output):
- *(code)* output is a single PDF with bleed marks and three panels;
- *(code)* every dish + price in the output matches `menu_items.csv` exactly (no dropped/edited rows);
- *(code)* the output embeds only the licensed brand fonts;
- *(expert)* the layout reads as the warm, earthy Maison Rouge brand and the panel breaks are sensible.

---

## 0.8  Appendix — the tool → execution-mode lookup

Used to auto-assign `execution_mode` (Gate B3.7) deterministically after the workflow string is parsed:

| Tool pattern | Mode |
|---|---|
| `image_*` (all Photoshop/Lightroom edits), `asset_search`, `asset_license_and_download_stock`, `document_render_layout/_vector` (export-only), `document_convert_pdf`, `font_recommend`, `create_firefly_board` | **[C]** headless-confirmed |
| `search_design`, `fill_text`, `animate_design`, `change_background_color` (Adobe Express track) | **[W]** interactive-widget (needs a human to pick a template) |
| `video_create_quick_cut`, `video_resize`, `media_summarize`, `media_enhance_speech` | **[A]** async-widget (polls in the product; do video/audio locally for our own runs) |
| `document_merge_data_layout`, `document_merge_data_vector` | **[T]** authored-template (needs a user-authored .indd/.ai with real merge fields) |

*Task-level `execution_mode` = the union of its steps' modes. `feasibility = full` is only valid if every step is **[C]**.*
