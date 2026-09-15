# StudioBench V3 Brief Rewrite Examples

Date: 2026-09-15

These examples demonstrate the intended remediation style. They retain difficult expert work while removing unrelated connector requirements and unsupported promises.

## Example 1: LAYOUT-10 Alderwood Scholars Fund

### Current Problem

The task combines annual-report design, donor presentation, five banners, two posters, three social formats, photo grading, Stock sourcing, crest reconstruction, typography research, data reconciliation, InDesign conversion, data merge, Express authoring, and a Board. It is credible as an agency campaign, but too broad for the stated small nonprofit budget and too similar to many other V3 tasks.

### Rewritten Client Brief

> Alderwood Scholars Fund needs its 2026 year-end donor package. Build a 12 to 16 page impact report and five center-specific outdoor banners using the supplied photographs, approved copy, center roster, outcome table, spend table, photographed crest, and last year's printer PDF.
>
> The report must explain student outcomes, reconcile the spend lines to the audited total, include all three approved stories, and reproduce the complete donor honor roll without omissions. The five banners must reuse the printer's dimensions and show the correct name, address, hours, and coordinator for each center.
>
> Our Eastgate photography is too thin for a banner. You may license one suitable Adobe Stock photograph, but it must be disclosed and must not imply that the pictured children attend our program. If it cannot sit honestly beside the volunteer photography, use a type-led Eastgate banner and explain the decision.
>
> Recover the existing crest only as far as the supplied enamel-sign photograph supports. Do not redesign it. Deliver the editable report source, editable banner source, print PDFs, a screen PDF under 12 MB, and a one-page production note.

### Why It Is Still Hard

- Financial lines do not reconcile to the audited total.
- One outcome covers a different reporting period.
- The donor list cannot lose a name.
- The source photography silently represents four centers, not five.
- The printer PDF must become a verified five-record run.
- Stock use has a documentary-truth constraint.

### Intended Adobe Profile

- Imaging: preview, straighten, adjustments, crop and resize.
- Stock: search and license only if the type-led exception is rejected.
- Vectorization: initial crest trace with geometry and small-size inspection.
- InDesign: convert legacy PDF, map fields, prepare template, merge five records, render, export IDML.
- Acrobat: inspect properties and compress the screen PDF.
- Boards and Express: not required.

## Example 2: PHOTO-11 Lumora Shade Visualization

### Current Problem

The task risks presenting seven generated lip-oil and on-lip shades from one physical sample as commercially accurate product photography. No image model or connector can establish production color from a single reference.

### Rewritten Client Brief

> Lumora is preparing an internal retailer sell-in meeting before the remaining shade samples arrive. Using the supplied clear-product photography and the one approved physical shade, create seven clearly labeled concept visualizations that show relative shade direction, not production-accurate color.
>
> Preserve the bottle, applicator, reflections, fill level, label geometry, and skin identity. Place `CONCEPT COLOR - SAMPLE APPROVAL REQUIRED` on every comparison sheet. Do not make wear-time, opacity, finish, or skin-result claims that are not present in the approved copy.
>
> Deliver seven transparent-background bottle concepts, three on-lip concepts using the provided model frame, one retailer comparison sheet, and a decision log identifying which visual properties require a physical sample or reshoot before public release.

### Why It Is Still Hard

- The bottle material and reflections must stay physically convincing.
- Selection edges and transparent product behavior are difficult.
- The shade system must remain differentiable without claiming accuracy.
- Identity and skin texture must be preserved.
- The correct professional answer includes explicit limits.

### Intended Adobe Profile

- Imaging: select subject or prompt region, invert where needed, apply adjustments, controlled color overlay or instruct edit, remove background, crop and resize.
- Express: one pre-authorized comparison-sheet template may be filled and downloaded in the full-system track.
- Image generation, Stock, Boards, vectorization, and data merge: not required.

## Example 3: MOTION-08 SentinelMesh Launch Edit

### Current Problem

The task asks the connector to cut by claim and topic, but Quick Cut uses visual engagement rather than speech meaning. A summary is not a timecoded transcript, so exact editorial compliance cannot be verified fairly.

### Rewritten Client Brief

> Create a 60-second launch film and a 15-second vertical cutdown from the supplied interview and product footage. Use only claims marked `Cleared` in the messaging table. The supplied transcript includes source timecodes; use it to select the approved spoken beats and preserve the speaker's meaning.
>
> Open with the risky moment, move to the in-context coaching demonstration, show the reporting view, and finish on the approved existing-stack claim. Do not use the 60 percent reduction claim, which remains in legal review. Remove long pauses without creating jump-cut speech, and keep music under dialogue.
>
> Deliver the 16:9 master, 9:16 cutdown, a clean speech stem, three approved poster frames, the final EDL, and a claim-use report matching each spoken or on-screen claim to its clearance row.

### Why It Is Still Hard

- It requires editorial selection, legal compliance, pacing, audio cleanup, and two aspect ratios.
- The model must reconcile transcript, claim table, footage, and final render.
- Rendered frames and dialogue continuity must be checked after editing.
- A prohibited but attractive claim is present as a trap.

### Intended Adobe Profile

- Video: metadata, timeline render from supplied timecodes, render-frame checks, resize.
- Audio: enhance speech; summarize only for orientation.
- Imaging: crop/resize poster frames if necessary.
- Quick Cut, Stock, Boards, Express, vectorization, and data merge: not required.

## Example 4: VECTOR-08 Coble & Vane Mark Recovery

### Current Problem

The current vector family treats `image_vectorize` as if it can independently guarantee production-ready engraving and print geometry. Vectorization can create a starting SVG, but it does not prove contour quality, closed paths, optical correction, or manufacturing suitability.

### Rewritten Client Brief

> Recover the existing Coble & Vane sail mark from the supplied bottle cap, etched glass, label, and archival card. The references disagree slightly because they were produced at different sizes. Establish the master from the most repeatable structural features rather than averaging every distortion.
>
> Deliver a one-color SVG master, reverse SVG, 12 mm and 6 mm optical reductions, and a proof sheet comparing each result with the supplied references. Paths must be closed where the shape requires closure, the background must be transparent, and no full-canvas rectangle may remain. Do not claim engraving readiness unless the delivered geometry can be inspected and passes the stated contour checks.
>
> Include a discrepancy note explaining which reference governed each disputed feature and which manufacturing checks remain for the fabricator.

### Why It Is Still Hard

- The references contain substrate distortion and inconsistent reductions.
- The agent must decide which evidence is authoritative.
- Small-size optical behavior matters more than full-screen similarity.
- Production claims must match inspectable geometry.

### Intended Adobe Profile

- Imaging: straighten, crop to bounds, select by prompt, monochromatic tint.
- Vector: vectorize as a starting point, then use an approved auditable path-authoring route if available.
- Vector render: inspect the master and optical reductions.
- Boards, Stock, Express, data merge, and generative editing: not required.

## Rewrite Pattern For All 100

Every revised brief should answer, in client language:

1. What business event or operational need caused the commission?
2. What exactly did the client supply?
3. What are the required deliverables, dimensions, formats, and editability expectations?
4. Which facts, identities, products, claims, or records must not be invented?
5. What can be rejected, disclosed, or deferred when the source is insufficient?
6. What makes the work difficult for an expert?
7. What evidence will prove the final files are usable?

Connector instructions, known API quirks, hidden defects, and verifier implementation belong outside the client-facing prose.
