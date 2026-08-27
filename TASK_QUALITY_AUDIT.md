# CREATIVE BENCHMARK QUALITY AUDIT — 100 TASKS
**Synthesis report · 2026-08-26 · adobe_only/specs**

---

## 1. BOTTOM LINE

**No. Not sellable as-is.** Five tasks out of 100 clear the owner's bar. That is a 5% pass rate on a set being pitched to Adobe as a measure of professional freelance creative work.

| Verdict | Count |
|---|---|
| PASS — meets the bar today | **5** (AO-15, AO-17, AO-24, AO-74, AO-110) |
| STRENGTHEN — real task, currently too easy/thin/partly undoable | **66** |
| REPLACE — fails the bar, not cheaply fixable | **29** |

Mean scores across all 100: creative_substance **2.76**, human_difficulty **3.12**, agent_difficulty **3.10**, realism **4.06**, connector_doability **3.32**.

The three numbers that matter:

- **36 of 100 score ≤2 on creative_substance.** Over a third of a *creative* benchmark produces no designed artifact, or produces one by mechanical filter application.
- **63 of 100 score ≤3 on connector_doability** — i.e. at least one promised deliverable cannot be produced as written, or comes out degraded. 16 of those are outright impossible.
- **25 of 100 score ≤2 on agent_difficulty.** A quarter of the set is near-impossible for the agent to fail. That measures nothing.

Realism is the one genuinely strong axis (4.06 mean, most briefs verbatim from Upwork/Freelancer/PeoplePerHour). The sourcing work was good. The *specification* work was not: the set repeatedly promises deliverables the connectors cannot make, then quietly hands the paid part of the job to a human.

**Caveat on the PASS tier — be direct about this.** 10 verdicts were adversarially re-challenged; 7 flipped. Five REPLACE calls were overturned as too harsh (AO-20, AO-22, AO-32, AO-46, AO-118) — but **two of seven original PASSes did not survive challenge** (AO-18 dropped to creative 3 / agent 2; AO-49 dropped to 3/3/3). Extrapolating that hit rate, the true PASS count under uniform adversarial pressure is plausibly **3, not 5**. Do not sell "5 exemplars" without re-challenging the remaining five.

---

## 2. THE KILL LIST — 29 REPLACE, worst first

### Tier A — inverts the purpose of the benchmark (7)

| ID | Why it dies | Replacement for the slot |
|---|---|---|
| **AO-82** | Lumen brand audit. Only outputs are a .md + .json; brief says "do NOT re-lay-out, restyle, recolour or edit anything." Only task in the set whose outputs are *exclusively* `kind:"data"`. Ground truth (~5% hue delta, 104% stretch) is unmeasurable — no eyedropper, no ruler; the two `select_by_prompt` calls point at the *reference* PNGs, never the proof. Rewards guessing over looking. | Same magazine, inverted: grade 12 mixed-light feature photos to the guide's warm-editorial rule, build coral pull-quote plates at the approved hex, vectorize the masthead, merge and export a press-ready 300 dpi issue. |
| **AO-92** | Screen-print "seps preflight memo." Deliverable written by a *local* tool. Asks `select_by_prompt` to find a 1px halo, `invert_selection` to *count* inks, and calls halftone "a press-LPI probe" (no LPI parameter exists). Every measurement is unobtainable. | Same shop, four graphics → actual burnable art: gradient skyline converted to a holdable halftone, halo genuinely removed, per-design SVG, 4-row merged sell-sheet PDF. |
| **AO-91** | Valcere logo "findings PDF + JSON," both local-authored. Defects pre-planted in the input prompt; `select_by_prompt` used as an "inspection locator" that returns no measurement. | The **remediation** job on the same defective master: expand strokes, close contours, fix the reverse variant, ship favicon/print/foil masters, merge into a usage-sheet .indd. |
| **AO-95** | Voltcast delivery QC. Brief hands the agent the answer key verbatim ("we expect you to catch…"). No connector measures overlay position at a timecode or identifies a burned-in typeface. Steps 7-8 are copy-paste residue from another spec. | Real channel package: quick-cut short, 9:16/1:1 reframes, graded thumbnail from `video_render_frame`, vectorized bug. |
| **AO-98** | Velvet Hour shot log + contact sheet. Brief says "do NOT cut, grade, add music." All three deliverables local-authored; `asset_preview_file` misused where `video_render_frame` is required. | Monthly session package: quick-cut, reframes, duotone gig-poster treatment, vectorized venue mark, merged multi-artist listing PDF. |
| **AO-83** | Halden catalog audit — `workflow_nature: "analyze"`, agent_difficulty **1** (lowest in the set). Defects enumerated in the input gen_prompt. | Ship the catalog: normalise the roster, prep 12 packshots to one house look, merge, export 300 dpi spreads, re-crop the overset offenders. |
| **AO-61** | Podcast "graphics kit": a same-length reframe (no edit at all) plus a tinted colour bar with no text called a "lower third." Input block incoherent (25-min video, `gen_model: gemini-3-pro-image`). | Podcast artwork package: 3-episode thumbnail set matched tonally from `video_render_frame`, vectorized logo, merged episode-card .indd. |

### Tier B — the paid work is disclaimed away (9)

| ID | Why it dies | Replacement |
|---|---|---|
| **AO-94** | One `quick_cut` + three `video_resize`; two of three "deliverables" are the same 1080×1920 spec rendered twice. Caption note copied out of a supplied PDF by a local step. | 6 takes / 3 topics → per-topic cuts + graded covers + merged episode-card carousel. |
| **AO-93** | Torqex preflight. Open paths, anchor points, live-vs-outlined text, RGB-vs-CMYK are **document-structure** properties; the spec tries to detect them by rendering to raster. Physically impossible. | Nameplate scan → cleaned, traced, production set: K100 etch, reverse knockout, isolated bolt mark, sized lockups. |
| **AO-54** | LaneWeave. Commissioned deliverable (10 AE explainer templates) discarded outright; end-card is a crop with a grey rectangle painted on. Four declared clips consumed by zero steps. | Learner-guide set: 6-8 road scenes to one look, vectorized sign glyphs, scenario CSV merged into an authored .indd, print+screen PDFs. |
| **AO-77** | Willowfen KDP preflight. "Do NOT redesign or re-lay-out anything." Defects pre-announced in the brief. Of five planted faults the connectors can fix exactly one. | Build the book: copyfit 32 captions, merge, render interior at spec, export the wraparound cover. |
| **AO-34** | ~1.5s "sizzle" + two coloured rectangles; the lower-third and callout **masks are supplied as inputs**, so the agent pours colour into someone else's shapes. | Explainer launch kit: sequenced master, matched poster frames, real typeset title/lower-third/end cards via .indd merge. |
| **AO-96** | Contracted 90-120s demo video ships as a ~15s cut with a 30s "cutdown" *longer than its master*. Plates are opaque, from supplied masks. Narrative fields describe a different workflow than the one listed. | SaaS collateral: assembled master, matched hero stills, merged multi-page one-pager from the messaging CSV. |
| **AO-37** | All three named damages (scratches, tears, blur) are exactly what the connectors cannot repair. Measured evidence: the studio backdrop carries ~56 levels of falloff and the sky ~26 levels of gradient — the solid `fill_area` "cure" is far worse than the disease. Steps 14-15 target a tear that step 13 already crops off. | Heritage-print package: matched archival grade across a set, duotone treatment, subject cutouts, merged captioned A4 run. **Also re-inspect AO-111 — same conceit.** |
| **AO-89** | Six one-call derivatives off one hub, three of them the same tint tool at different hues. Palette "deliverable" is a markdown note. Source brief was *design a logo* — the connector's banned bucket. | Clean-beauty retail kit: vectorize one approved mark, 4 matched PDP cutouts, duotone texture, 6-SKU label merge with per-SKU accent, print-ready with bleed. |
| **AO-56** | Reaction zooms, on-video call-outs, jump cuts — none connector-doable. The two "callout SVGs" are whole-raster traces of the thumbnail, placeable on nothing. | 6 captures → matched stills, an A/B thumbnail *set* (two art directions, not one filter stack), three reframes, speech enhance, summarize-driven chapters. |

### Tier C — real brief, wrong deliverable (7)

**AO-76** (10-12 CSV rows must land as one table, but merge emits one file *per row* — topologically impossible; plus the convert_pdf_to_indd contradiction) → per-row branch cards with agent-prepped imagery. · **AO-58** (branded reel explicitly not produced; 3+3 logo calls and a folder) → 6-exercise library: cuts, poster frames, merged exercise cards. · **AO-41** (every deliverable one-click; premise fake — nobody traces a photo of a printed proof as an SVG master) → brand-asset production from a real vector master, 8 placements, merged usage guide. · **AO-42** (export-variants chore; two of eight deliverables admitted fakes in the spec's own text) → merch production: burnable seps, 12-row hangtag merge, size-graded placements. · **AO-85** (findings CSV + txt, both local; defects listed in the spec; reading 181 spec cards via `asset_preview_file` is not an inspection path) → ship the parts catalog. · **AO-67** (six banners export with **empty placeholder frames** — nothing can place the hero, SVG or halftone into an .ai; 12 of 28 calls are plumbing) → InDesign-based multi-size banner merge. · **AO-99** (step 3 reframes 1080×1920 → 9:16, a no-op; end card shipped as un-composited layers) → frame-pull + print storyboard package.

### Tier D — realistic but trivial (6)

**AO-117** (junior hour; three of four deliverables blocked by an unbindable merge + unsupported per-artboard export) → six-hero site campaign from three licensed sources, one matched grade, real merge path. · **AO-35** (two straight-line tonal chains on one postcard; every restoration craft excluded) → all 24 postcards + transcribed backs merged into a memorial book. · **AO-112** (36 calls = the same 5-call recipe six times; inputs explicitly de-cluttered, engineering away the one hard part) → cluttered mixed-lit source + numeric margin/scale gate + merged slab comp-cards. · **AO-113** (48 calls = one pipeline ×6; flat hex backdrop, no contact shadow) → measured colour accuracy vs grey card + merged line sheet. · **AO-25** (three independent 4-6 call chains; spec concedes perspective and cloning are "left as the human's finishing pass" — functionally identical to the shipped `adobe-batch-edit-photos` skill) → 12 frames / 3 properties + brochure merge. · **AO-06** (12 calls, 10 of them parameterless auto-ops, one SKU) → 8-10 heterogeneous SKUs with a self-verified pass/fail spec.

---

## 3. THE STRENGTHEN LIST — 66 tasks, by failure pattern

Tasks appear in more than one group; the group names the fix.

### G1 · Broken merge path (18) — *the largest single defect in the set*
AO-01, AO-11, AO-14, AO-62, AO-64, AO-68, AO-69, AO-72, AO-75, AO-78, AO-79, AO-80, AO-81, AO-84, AO-90, AO-105, AO-106, AO-107 (+ PASS-flagged AO-24, AO-74).

Two variants, often both in one spec: (a) the input's own `realism_notes` state that a PDF-converted .indd will not bind merge fields — and the workflow then runs `convert_pdf_to_indd` and merges into it; (b) the CSV has no image column, so every graded photo the agent produced has no route into the layout and the export prints with empty frames.

**Fix (one asset-pipeline change covers all 18):** author genuine .indd/.idml templates carrying live `<<fields>>` **and** `@`-prefixed image-path columns; delete every `convert_pdf_to_indd` step. Add a page-count = row-count and effective-DPI gate on the exported PDF. Where the lane is Illustrator, note that `document_merge_data_vector` is **text-only** — it cannot bind images (this specifically breaks AO-107 and AO-90).

### G2 · Batch amputated to one hero (14)
AO-03, AO-04, AO-08, AO-12, AO-13, AO-20, AO-21, AO-26, AO-27, AO-32, AO-39, AO-84, AO-111, AO-118.

The brief says 20 pieces / 38 shots / 25-30 photos / 49 SKUs; the spec runs one, and calls it "a repeatable recipe." This deletes cross-asset colour consistency — the single hardest, most gradeable thing in the whole corpus.

**Fix:** restore 6-12 assets shot under *deliberately different* light, and make the acceptance criterion cross-image and measurable (common white point, stated black-point/warmth tolerance, a reference card or known-white surface in frame). Require a contact sheet the grader can inspect.

### G3 · Repetition sold as difficulty (10)
AO-18, AO-49, AO-57, AO-60, AO-63, AO-86, AO-97, AO-104, AO-115, AO-116.

40-45 call counts made of one recipe pasted N times, plus upload init/finalize pairs counted as work. AO-104's "18-crop delivery matrix" is one operation with different numbers. AO-116 instructs the agent to apply identical parameters to three differently-exposed frames — which is professionally *wrong* and guarantees they won't match.

**Fix:** collapse the repeats, stop counting plumbing, and buy difficulty with *requirements* instead — per-frame corrective deltas to a shared target, a deliberately-breaking fourth asset, a verification beat the agent must run and can fail.

### G4 · Designed artifact punted to a human (14)
AO-02, AO-22, AO-23, AO-30, AO-31, AO-45, AO-48, AO-52, AO-55, AO-119, AO-120, AO-121, AO-122, AO-123.

The client commissioned an ad, a thumbnail, a lower third, a banner, a poster. The spec delivers a prep folder and writes "the typeset final assembly is explicitly handed off." Several ship an *opaque rectangle painted over a photo* as a "plate."

**Fix:** every one of these gets an authored .indd/.ai template + a copy CSV and a real merge, so type is actually set. Delete the opaque-plate outputs entirely — an asset nobody can place is not a deliverable.

### G5 · Wrong tool for the stated craft (11)
AO-10, AO-38, AO-45, AO-49, AO-51, AO-63, AO-69, AO-87, AO-88, AO-90, AO-123.

`fill_area` solid-fills the whole mask, destroying interior negative space (AO-38's "black logo variant" is a black blob) and flattening texture. `color_overlay` is whole-image with no opacity, so it cannot produce a clean knockout. `image_vectorize` fed a *selection* returns a black silhouette, not a spot plate (AO-87, AO-51). `select_by_prompt` is semantic and cannot select "the top headroom band" or "the red region."

**Fix:** publish a one-page connector-mechanics sheet and re-derive: knockouts via `select_subject → fill_area` on transparency; spot plates by masking-then-flattening *before* vectorize; anchor every selection prompt to a named shape, never a hue or a geometric region. Note the documented anti-pattern: to put a subject on a solid ground, use `remove_background({backgroundColor})` — **not** select→invert→fill (AO-18 prescribes the forbidden chain twice).

### G6 · Consistency asserted, never measurable (14)
AO-11, AO-12, AO-15, AO-17, AO-18, AO-29, AO-47, AO-60, AO-107, AO-109, AO-110, AO-114, AO-116, AO-121.

"Must read as one set" with no tolerance, no reference patch, no verification step — and no eyedropper anywhere in the connector surface. The grader cannot fail it, so it is not being measured. AO-109's spine is outright broken: the hero gets a hand-built grade while seven siblings get a *stock* Lightroom preset, which cannot reproduce it.

**Fix:** put a physical grey/colour card in frame (inputs are generated — this is free), require every image neutralised to it, and require the agent to *report* its final per-image parameters. Then "matched" becomes checkable.

### Borderline — re-audit after rewrite or promote to the kill list (7)
**AO-20, AO-22, AO-27, AO-32, AO-39, AO-46, AO-75, AO-104, AO-118** all carry creative_substance ≤2 or agent_difficulty ≤2 today. They survived on the strength of the underlying job, not the spec. If the rewrite does not lift both axes to ≥3, kill them.

---

## 4. SYSTEMIC PATTERNS

**1. The specs promise capabilities the connectors do not have — and often say so themselves, in the same file.** ~21 tasks contain the `convert_pdf_to_indd` self-contradiction verbatim. ~16 promise compositing (place image A over image B / paint text on a plate). This is the dominant defect class and it is not a judgment call — it is a correctness bug.

**2. Report-only inversion. All 9 `workflow_nature: "analyze"` tasks are on the kill list.** AO-77, AO-82, AO-83, AO-85, AO-91, AO-92, AO-93, AO-95, AO-98. Every one produces a findings file instead of a designed artifact; most produce it via *local, non-Adobe* helpers, so the connector contributes nothing. Worse, all of them **print the defect list in the brief or the input gen_prompt** — an LLM scores full marks without inspecting anything. These items are not merely easy; they are *noisy*, actively corrupting any agent's score.

**3. Difficulty is sourced from step count, not craft.** Upload init/finalize pairs, folder creates, copies, and repeated identical calls routinely make up 30-50% of a "T4_expert" chain. AO-104, AO-115, AO-97, AO-47, AO-55 are all tiered on padding.

**4. The video lane is the weakest vertical.** 19 video-centric tasks; **9 killed (47%), zero PASS.** Root cause: the connectors have no timeline trimming, no motion graphics, no compositing — so every spec either delegates the edit wholesale to `video_create_quick_cut` (the AI makes the creative decision, not the agent) or issues same-length `video_resize` calls and calls them an edit. AO-121 is the only video task doing genuine editorial assembly.

**5. Declared-but-unused inputs.** ≥10 tasks ship licensed, generated, QC'd assets that zero workflow steps consume (AO-13, AO-31, AO-52, AO-54, AO-46, AO-120, AO-123). Wasted asset-pipeline spend and a visible defect to any reviewer.

**6. Internal drift.** ~18 tasks have `chaining_note` / `difficulty_rationale` / `reverify` describing a *different* workflow than `connector_workflow` — off-by-one step numbering, phantom `media_summarize` calls, tool_call_count disagreeing with the array length. An executing agent and a grader would disagree about what was asked.

**7. Deprecated tool names in ≥27 specs** (`image_adjust_color_temperature`, `_highlights`, `_vibrance_and_saturation`, `_brightness_and_contrast`). Staleness, not impossibility — but it is a bad look in a deliverable sold to Adobe, and in AO-18 the deprecated calls constitute the *entire* craft spine.

### The tier picture — T1_simple is a net negative

| Tier (where labelled) | n | REPLACE | STRENGTHEN | PASS |
|---|---|---|---|---|
| T1_simple | 8 | **5 (62%)** | 3 | **0** |
| T2_moderate | ~12 | 2 | 10 | **0** |
| T3_complex | ~12 | 2 | 9 | 1 |
| T4_expert | ~12 | 2 | 10 | **0** |

**Yes — the T1 tier as a whole is pulling the benchmark below the bar.** Five of eight labelled T1s are dead, and the survivors (AO-26, AO-111) are both flagged as *mis-tiered* — AO-26 is a 20-call task labelled simple. Meanwhile several T3/T4 tasks are honestly T1 (AO-112, AO-113, AO-06, AO-104). The tier field is unreliable in both directions and should be re-derived from craft requirements after the rewrite, never from step count.

**Not a single T4_expert task passes.** That is the tier the sale rests on.

---

## 5. WHAT'S GENUINELY STRONG — clone these

**The five PASSes.** AO-110 (Summit & Sable) is the exemplar: six non-uniform grade sub-chains driven to a *common target* — two warmed, two cooled — plus a safety-orange → gunmetal recolour executed as two masked HSL passes riding original luminosity, with a written rationale for why `color_overlay` and `fill_area` are both wrong. It carries the client's own acceptance bar verbatim ("no sloppy masking, flat colors"). AO-74 (Crumb & Co.) is the layout exemplar: a locked preset threaded as a real data dependency through 11 sub-chains into a genuine image+text merge and a 300 dpi press PDF. AO-17 and AO-15 are the colour-matching exemplars. AO-24 is the multi-branch exemplar.

**The transferable design patterns:**
1. **A locked look established on a reference frame, then propagated as a data dependency** to N differently-lit assets (AO-110, AO-74, AO-17, AO-18, AO-106).
2. **Two *different* correct treatments for superficially similar inputs** — AO-80 makes the agent triage sponsor logos: vectorize the flat rasters, but `select_by_prompt → remove_background` the photographed one. Getting it wrong is invisible until you look.
3. **Constraint reasoning around a tool limitation** — AO-52's mirror-image mask-polarity trick (fill the art field flat to vectorize lettering-only; fill the lettering flat to halftone the art field, because neither tool accepts a mask). This is exactly what separates a good agent from a bad one.
4. **Prep-before-trace discipline** — AO-90 and AO-46: straighten, tone, crisp the channel, crop to bounds, knock to transparency *before* `image_vectorize`. A naive agent that traces the raw file fails, and the failure is only visible in the path data.
5. **Ends in a print artifact with a checkable spec** — page-count = row-count, effective DPI at trim, bleed, CMYK.

**High-value near-misses — one blocker from PASS:** AO-122, AO-106, AO-87, AO-52, AO-80, AO-79, AO-14, AO-107, AO-78, AO-10, AO-11, AO-105, AO-29, AO-114, AO-69. AO-122 scores 5/5/5/5 on everything but doability. Fixing these is the cheapest route to a defensible exemplar tier.

---

## 6. RECOMMENDED ACTION PLAN

**95 of 100 need work.** Sequence by leverage, not by task ID.

**Step 1 — Publish a connector-mechanics ground-truth sheet. (0.5 day, blocks everything else.)**
One page: `fill_area` fills the whole mask; `color_overlay` is whole-image; `vectorize` traces rasters not selections; `select_by_prompt` is semantic, never geometric; `document_merge_data_vector` is text-only; `render_layout` exports, never places; use `remove_background({backgroundColor})` instead of select→invert→fill; per-artboard named export does not exist. Every rewrite validates against it. This single document prevents the recurrence of ~40 defects.

**Step 2 — Author the InDesign template library. (3-4 days, unblocks 20 tasks.)**
Real .indd/.idml files with live `<<fields>>` **and** `@`-image columns, ~8 reusable shells (label, flyer, catalog spread, sell sheet, poster, badge, banner, line sheet). Delete every `convert_pdf_to_indd` step in the corpus. This is the highest-leverage single action available: it converts G1's 18 STRENGTHENs from "broken deliverable" to "working deliverable" without touching their creative content.

**Step 3 — Execute the kill list, Tier A first. (~9 days.)**
Replace the 9 analyze/report tasks first — they are the ones that most damage the pitch, and each has a ready-made CREATE replacement in this report that reuses its existing assets. Then Tiers B-D. Budget ~1 day per replacement (brief, spec, workflow, asset regen, QC). **Hard rule going forward: `workflow_nature: "analyze"` is banned as a primary deliverable, and no brief may enumerate its own planted defects.**

**Step 4 — Batch-restore the amputated sets. (G2, 14 tasks, ~4 days.)**
Mostly asset generation, not spec rewriting: 6-12 assets per task under deliberately mixed light, plus a grey/colour reference card in frame, plus a stated tolerance and a required contact sheet. Cheapest large gain in agent_difficulty across the corpus.

**Step 5 — Kill the padding and the punts. (G3 + G4, 24 tasks, ~5 days.)**
Collapse repeated recipes, stop counting upload plumbing, delete every opaque "plate" output, and attach a template merge so the typeset artifact is actually produced.

**Step 6 — Rebuild the video lane. (19 tasks, ~5 days.)**
Accept the connector reality: video contributes *cuts, reframes, frame-pulls, speech enhance, summarize*. Everything typeset must come from the InDesign lane. Nine of these are already on the kill list; the surviving ten need the same treatment. Consider capping the video lane at 12 slots rather than 19.

**Step 7 — Hygiene sweep. (~1 day, scriptable.)**
Deprecated tool names → `image_apply_adjustments`; reconcile `tool_call_count` / `distinct_adobe_tools` / `chaining_note` against the actual `connector_workflow` array; delete or consume every orphaned input; re-derive tier labels from craft requirements.

**Step 8 — Re-challenge the PASS tier and the 7 borderline STRENGTHENs. (1 day.)**
Two of seven original PASSes fell under adversarial re-check. Run the same pressure on AO-15, AO-17, AO-24, AO-74, AO-110 before any of them is shown to Adobe as an exemplar. Promote or kill AO-20, AO-22, AO-27, AO-32, AO-39, AO-46, AO-75, AO-104, AO-118 on the same pass.

**Total: ~28-30 working days to a defensible set.** There is no shortcut that preserves the current 100. Shipping as-is puts a 5% pass rate, 9 non-creative audit tasks, and ~21 self-contradicting specs in front of the buyer.