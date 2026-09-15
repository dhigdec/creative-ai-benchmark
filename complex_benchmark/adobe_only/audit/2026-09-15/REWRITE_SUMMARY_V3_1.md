# StudioBench V3.1 Corpus Rewrite

Date: 2026-09-15

## Result

All 100 Adobe benchmark specifications were rewritten as source-derived composite marketplace briefs. They are not represented as verbatim live Upwork or Freelancer listings. The revised client-facing briefs now use a consistent freelance-post structure while retaining task-specific business context, brand identity, source assets, production constraints, and acceptance evidence.

The corpus validator passes with no errors or warnings.

The format-aware asset audit also passes: 1,861 of 1,861 manifest-listed files are present, non-empty, and decodable, with no unmanifested files or declared-dimension mismatches. The frozen corpus contains 4,410,789,346 asset bytes and has SHA-256 fingerprint `c642fcd80d142c3dcff0a01cef879750ad52624c4c4b2779bb7e3ac68eef5ef7`.

## Canonical Naming And Storage

Every task now has a globally sortable reference code, a curated client-and-commission name, its original family ID, and a deterministic S3 prefix. The order is Photo `SB3-001-PHO` through `SB3-030-PHO`, Vector `SB3-031-VEC` through `SB3-045-VEC`, Layout `SB3-046-LAY` through `SB3-080-LAY`, and Motion `SB3-081-MOT` through `SB3-100-MOT`. Legacy IDs remain in every record so historical runs and source manifests stay traceable.

Asset storage is rooted at `s3://annotationprod/creative-ai-benchmark/v3.1/tasks/`, with one sortable task folder per canonical code. `TASK_NAMING_REGISTRY_V3_1.csv` is the authoritative code-to-name-to-prefix crosswalk.

## Portfolio Shape

| Measure | Result |
| --- | ---: |
| Tasks | 100 |
| Flagship integrated engagements | 30 |
| Expert standard engagements | 45 |
| Specialist stress tests | 25 |
| Tasks with 2 deliverables | 56 |
| Tasks with 3 deliverables | 38 |
| Tasks with 4 deliverables | 5 |
| Tasks with 5 deliverables | 1 |
| Exact duplicate deliverable names | 0 |
| Exact duplicate marketplace titles | 0 |
| Distinct deliverable classes | 20 |
| Client brief length | 323-524 words; median 376 |

Narrow tasks remain hard through precision, consequence, restoration, truth, small-size reproduction, record integrity, or timing. Flagship tasks carry three to five connected outputs. Handover is required on every task but is no longer counted as a decorative extra deliverable.

## Asset Contract

The 597 client-facing asset groups are explicitly assigned:

| Asset role | Groups |
| --- | ---: |
| Direct production input | 443 |
| Required reference | 114 |
| Out-of-scope archive reference | 40 |

Every supplied asset must be recorded in the final manifest as used, reference-only, superseded, or rejected with a concrete reason. Files tied only to removed deliverable classes remain available for provenance but cannot silently become extra scope.

All 20 motion packs now contain `motion_source_metadata.json`, measured directly from the supplied files. The metadata is authoritative for duration, dimensions, frame rate, codec, and audio-stream presence. This corrects older narrative labels that described long recordings although the supplied benchmark clips are short, silent rushes. Motion briefs were narrowed to outputs the actual files can support.

## Adobe Distribution

The current ChatGPT Adobe inventory contains 99 callable names. V3.1 uses 55 distinct meaningful operations across the portfolio and keeps tool names outside client-facing prose.

Key task counts:

| Operation family | Tasks |
| --- | ---: |
| Crop and resize | 66 |
| Deliberate image adjustments | 58 |
| Auto straighten | 30 |
| Subject selection and background removal | 30 |
| Vectorize as an inspected starting point | 24 |
| InDesign conversion and data merge | 33 |
| Express template adaptation | 20 |
| Adobe Stock search and licensing | 20 |
| Firefly Boards | 12 |
| Video metadata | 19 |
| Exact timeline render | 14 |
| Visually led Quick Cut | 5 |
| Speech enhancement on separate audio | 5 |

Specialist image operations are intentionally sparse: halftone 4, glitch 2, grain 6, noise 5, monochrome 10, generative expand 10, instruction edit 5, and image generation 5. Stock, Boards, Express, vectorization, and merge operations are present only when a brief-level need justifies them.

## Truth And Verification

Every task now has:

- A marketplace title, project overview, expert level, fixed-price range, delivery window, revision structure, and scope-change policy.
- A primary craft problem, bounded deliverable package, asset-use plan, truth constraints, and allowed exception states.
- A current-host Adobe connector profile with required and conditional operations plus per-operation rationale.
- A seven-phase trajectory built around evidence, first proof, reconciliation, artifact QA, correction, and handoff.
- Separate artifact checks, normalized process checks, and human craft review. Final artifact quality is host-neutral and does not depend on raw connector response fields.
- At least three unique checks in each verifier category. Shared artifact checks cover scope, input disposition, and file integrity; shared process checks cover normalized execution evidence, creative-decision traceability, and closed revision loops.
- Explicit limits for generated truth, physical-sample color, documentary imagery, legal claims, print readiness, and manufacturing readiness.

Vectorization is never accepted by itself as proof of engraving, cutting, embroidery, or press readiness. Quick Cut is used only for visually led selection, never for semantic speech editing. Interactive Acrobat page-organization routes are excluded from the zero-human profile.

## Repeat Clients

Apparent brand collisions were converted into explicit repeat-client series with separate commission phases and a canonical client context. Companion tasks are scored independently and may not reuse deliverables from one another.

## Important Limit

The asset packs are production-valid benchmark inputs, not full commercial shoots. In particular, motion files are compact proxy rushes. V3.1 makes the briefs honest about that constraint instead of overstating the available footage. A future media expansion can replace the proxies without changing the task architecture, provided the new files receive fresh measured metadata and the corpus fingerprint is updated.
