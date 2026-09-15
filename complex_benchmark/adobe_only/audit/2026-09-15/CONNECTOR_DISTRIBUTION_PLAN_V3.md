# StudioBench V3 Adobe Connector Distribution Plan

Date: 2026-09-15

## Objective

Use the breadth of the Adobe connector where the work genuinely calls for it, without turning every client engagement into the same tool demonstration.

The benchmark should measure three things separately:

1. Model judgment: interpretation, selection, sequencing, tradeoffs, revision, and disclosure.
2. Connector execution: whether the chosen Adobe operations complete the intended transformation.
3. Final craft: whether the deliverables are correct, coherent, useful, and professionally finished.

## Current Diagnosis

The live ChatGPT environment exposes 99 Adobe-prefixed callable names. After aliases, status helpers, UI wrappers, and administrative operations are removed, this is roughly 79 distinct operations. Not all 79 are autonomous creative actions and not all should be benchmark targets.

The current V3 specifications overuse a narrow set:

| Current requirement | Tasks |
| --- | ---: |
| Express HTML authoring operations not exposed on ChatGPT | 100 |
| Font operations not exposed on ChatGPT | 100 |
| `asset_search` | 100 |
| `image_apply_adjustments` | 100 |
| `image_crop_and_resize` | 100 |
| Boards create/add | 93 |
| InDesign conversion, merge and render chain | 92 |
| Stock licensing | 90 |
| `image_vectorize` | 82 |
| `image_remove_background` | 80 |

That distribution is not credible for 100 independent freelance jobs. It also hides connector breadth because the same routes dominate nearly every trajectory.

## Governing Rules

### Per Task

- Give every task one primary craft surface.
- Permit zero to two supporting surfaces for ordinary tasks.
- Reserve four or more surfaces for 20 to 30 flagship integrated engagements.
- Require two to seven meaningful creative operations per task. Transport, initialization, polling, preview, and download helpers do not count.
- Every operation must be justified by an input defect, a deliverable requirement, or a required quality-control step.
- Never add Stock, Boards, data merge, vectorization, generative editing, or Express merely to increase tool coverage.
- Keep client-facing briefs host-neutral. Tool names belong in versioned execution profiles.
- Preserve an honest exception path when source truth cannot support the requested result.

### Across The Portfolio

- Measure canonical operations, not aliases. For example, Acrobat-prefixed and unprefixed wrappers for the same PDF operation count once.
- Exercise 45 to 55 meaningful distinct operations across the full benchmark.
- Use common operations broadly only when naturally common, such as crop, resize, preview, and output inspection.
- Exercise specialist effects in a small number of tasks where the visual language supports them.
- Exclude account, migration, upload UI, polling, and duplicate low-level wrapper calls from creative-coverage scoring.
- Exclude UI-confirmed PDF operations from the zero-human parity track unless the connector gains an autonomous route.

## Target Usage Bands

These are portfolio bands, not quotas. A task should never call a tool solely to make a number pass.

### Asset And Collaboration

| Canonical operation | Target tasks | Appropriate use |
| --- | ---: | --- |
| Creative Cloud asset retrieval/search | 25-40 | Existing brand libraries or prior client files |
| Upload/finalize/presigned URL chain | As required | Transport only, excluded from creative score |
| Adobe Stock search and license | 15-25 | A real, declared content gap with licensing relevance |
| Firefly Boards | 8-15 | A shortlist, review board, or visual evidence board is a real deliverable |

### Imaging

| Canonical operation | Target tasks | Appropriate use |
| --- | ---: | --- |
| Crop and resize | 55-70 | Required aspect ratios, subject framing, print/social dimensions |
| Manual adjustments | 45-60 | Deliberate cross-frame grading or product correction |
| Auto straighten | 20-35 | Handheld architecture, documents, artwork, or product captures |
| Auto tone | 15-25 | Triage or baseline normalization, followed by review |
| Select subject | 18-30 | Cleanly separable foreground subjects |
| Select by prompt | 20-35 | Specific garments, labels, marks, regions, or materials |
| Invert selection | 8-15 | Background-only corrections after a verified selection |
| Fill area | 12-20 | Small, non-factual cleanup or controlled repair |
| Remove background | 15-25 | Product cutouts and simple marks with inspectable edges |
| Remove blemishes | 6-12 | Portrait or product cleanup that preserves identity and material truth |
| Generative expand | 8-15 | Composition extension where no factual product/architecture claim is introduced |
| Instruct edit | 5-10 | Controlled semantic change with explicit truth constraints |
| Image generation | 4-8 | Conceptual campaign material, never a fabricated product or documentary fact |
| Vectorize | 15-22 | Initial trace, followed by inspectable geometry checks |
| Apply preset | 8-15 | A repeatable look is part of the client workflow |
| Monochromatic tint | 8-15 | Duotone, archival, screenprint, or identity-led output |
| Grain or noise | 4-10 | Deliberate finish matching, not generic decoration |
| Halftone | 3-6 | Screenprint, editorial, or event-poster grammar |
| Blur or lens blur | 3-8 | Depth control, privacy, or a specified visual treatment |
| Color overlay | 4-8 | Brand tinting, proof overlays, or campaign systems |
| Glitch effect | 1-3 | Only briefs whose identity explicitly calls for it |

### InDesign And Structured Production

| Canonical operation | Target tasks | Appropriate use |
| --- | ---: | --- |
| Convert PDF to INDD | 18-28 | The client supplies legacy printer artwork that must be reused |
| Generate and verify mapping | 22-32 | Actual variable fields or repeated records |
| Prepare and merge layout data | 22-32 | Catalogs, labels, cards, tickets, directories, or branch runs |
| Merge vector data | 4-8 | Variable vector marks, badges, numbers, or codes |
| Render layout | 22-32 | Print/output verification at required dimensions and density |
| Render vector | 4-8 | Inspecting merged vector output and geometry behavior |
| Export IDML | 15-25 | A genuinely editable professional handoff is required |

### Acrobat And PDF Production

| Canonical operation | Target tasks | Appropriate use |
| --- | ---: | --- |
| PDF properties | 15-25 | Page count, dimensions, orientation, or preflight evidence matters |
| OCR | 6-10 | Scanned copy, archive material, or image-only printer files |
| PDF to Markdown | 8-15 | Extracting approved copy, tables, or archive text |
| Create PDF | 10-18 | Converting supplied Office/image material into a controlled PDF workflow |
| Export PDF | 4-8 | Editable Office output is an explicit handoff requirement |
| PDF to image | 8-12 | Page-by-page visual review or downstream image treatment |
| Compress PDF | 10-20 | A client delivery-size constraint exists |
| Combine, split, reorder, rotate, redact | Assisted track only | Current entry route is UI-confirmed and conflicts with zero-human runs |

### Express And Fonts

| Canonical operation | Target tasks | Appropriate use |
| --- | ---: | --- |
| Search Express templates | 8-12 full-system tasks | The client asked for template adaptation and autonomous choice is explicitly authorized |
| Fill text | 12-18 | Existing template text must be replaced accurately |
| Replace image | 8-15 | One visual in an existing Express design needs replacement |
| Change background color | 5-10 | Solid background change in an existing design |
| Animate design | 5-8 | Animated social or event collateral is a required output |
| Download design | 12-18 | Export from a completed Express adaptation |
| Font recommend | 20-35 | Typography is a meaningful design decision |

The unavailable HTML-to-Express and full fontkit chain must not appear in the current ChatGPT profile. If Claude exposes those operations, place them only in the Claude full-system profile and score equivalent outcomes.

### Audio And Video

| Canonical operation | Target tasks | Appropriate use |
| --- | ---: | --- |
| Video metadata | 20 | Validate every motion source before editing |
| Quick Cut | 5-7 | Visual highlight reels with no word/topic precision requirement |
| Media summarize | 8-12 | Orientation and content inventory, not timecoded editing evidence |
| Enhance speech | 8-12 | Interviews, testimonials, lectures, or noisy spoken footage |
| Timeline render | 12-18 | Exact edits based on supplied timecodes or an EDL |
| Render frame | 10-15 | Title-safe, crop, transition, and visual-continuity inspection |
| Video resize | 15-20 | Required platform aspect-ratio variants |

## Portfolio Shape

Use three complexity tiers:

| Tier | Tasks | Typical shape |
| --- | ---: | --- |
| Flagship integrated engagement | 30 | One primary craft problem, three to five connected deliverables, three to five surfaces, genuine revision loop |
| Expert standard engagement | 45 | One primary craft problem, two to four deliverables, one to three surfaces |
| Specialist stress test | 25 | Narrow deliverable set with a difficult production, truth, restoration, data, or timing constraint |

Every tier remains hard. Narrow tasks are made hard through precision and consequence, not through unrelated deliverables.

## Validation Rules

The repository should fail its distribution audit when:

- A current-host profile names a tool not present in that host's capability snapshot.
- More than 30 tasks require Boards, Stock, data merge, or vectorization without a documented client need.
- More than 30 flagship tasks use four or more creative surfaces.
- A specialist effect appears in a task without a brief-level visual rationale.
- A motion task asks for semantic cutting without a timecoded transcript or EDL.
- A vector task claims manufacturing readiness without inspectable path evidence.
- A zero-human task requires an interactive chooser or confirmation UI.
- A task's automatic artifact score depends on a connector response field.

## Implementation Sequence

1. Canonicalize the 99 callable names into creative operations, helpers, aliases, UI-only operations, and unavailable legacy operations.
2. Give every task a primary craft problem and complexity tier.
3. Remove unrelated deliverables before allocating tools.
4. Assign an outcome-level surface profile and a host-specific execution profile.
5. Rewrite trajectories around decisions and evidence rather than predetermined calls.
6. Rewrite automatic verifiers against artifacts and normalized events.
7. Run the distribution audit and revise any saturated or unsupported operation.
8. Pilot a stratified set before freezing all 100.

## Principle

A strong benchmark does not prove that an agent can call many tools. It proves that the agent knows which tool the job needs, when to revisit a decision, and when not to use a capability that would make the deliverable less truthful or less professional.
