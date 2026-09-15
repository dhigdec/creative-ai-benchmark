# StudioBench V3 Pre-Freeze Audit

Date: 2026-09-15

## Verdict

StudioBench V3 is strong raw material, but it is not ready to freeze as a fair ChatGPT-versus-Claude Adobe benchmark.

Almost every brief is recognizable as a credible expert freelance engagement when read alone. The assets are generally coherent, high-resolution, and rich enough to require real selection, repair, hierarchy, and production decisions. The corpus-level construction is the weakness: most tasks have been expanded into the same multi-surface campaign pattern, and their acceptance contracts assume connector operations that are not available on the current ChatGPT Adobe surface.

The correct conclusion is:

- Task-level realism: strong.
- Asset quality: strong overall; five broken tabular inputs were repaired during this audit, and six truth-sensitive image cases still need contract changes.
- Portfolio realism and diversity: needs rebalancing.
- Current cross-host comparability: blocked.
- Freeze readiness: no, until the P0 and P1 work below is complete.

## Audited Scope

- 100 individual V3 specifications read in full.
- Families: 30 Photo, 15 Vector, 35 Layout, 20 Motion.
- 1,841 manifest assets, 4,410,753,086 bytes total after the Alderwood table split.
- 1,841 assets decoded or parsed successfully, with zero remaining validation issues.
- 100 per-task contact sheets and 11 family overview sheets visually inspected.
- 951 automatic verifiers and 733 human verifiers inspected structurally.
- 320 emergent checkpoints across the corpus.
- Current corpus fingerprint: `e3dcd8e1e64b2c0dcf4e1c174362f34329e328e6c193bf4e244e58fb9e23331e`.
- Current remediation tiers: 16 P0, 36 P1, and 48 P2.

## What Is Already Strong

1. The briefs usually contain a real commercial context, buyer, audience, production constraint, supplied material, and failure cost. They do not read like toy prompts.
2. The asset packs are visually coherent within a task and cover credible client material: phone photography, product frames, portraits, venue footage, scans, printer PDFs, CSVs, copy decks, and identity remnants.
3. The strongest tasks force irreversible or consequential choices instead of merely asking for attractive output. Examples include reconciling financial data, preserving an honour roll, deciding whether a source frame is usable, rebuilding a mark from a physical artifact, and validating a data-merged print run.
4. Human verifiers generally inspect the right qualities: legibility at use size, identity fidelity, coherence, honest disclosure, and whether a finished piece serves the stated audience.
5. The specifications already contain useful decision gates and rework checkpoints. Those are valuable for studying agent behavior and should be retained in a shorter, host-neutral form.

## P0: Blocking Corrections

### 1. Connector Contract Mismatch

All 100 tasks are blocked as written on the current ChatGPT Adobe connector profile. This does not mean every creative operation is impossible. It means at least one required deliverable or verifier in every task depends on an unavailable operation.

The current surface exposes 99 Adobe-prefixed callable names, representing roughly 79 distinct operations after aliases are removed. Strong available families include raster imaging, PDF and InDesign conversion/merge/rendering, Adobe Stock search and licensing, Firefly Boards, template-based Express editing, audio enhancement, Quick Cut, and JSON-timeline video rendering.

The following hard dependencies named in the current specs are not exposed here:

- `create_visual_design_express_skill`
- `export_html_to_express`
- `html_export_readiness_skill`
- `find_fonts`
- `font_styles`
- `get_fontkit_embed_url`
- `get_account_type`

The present Express workflow is template search and template editing. It requires a template-selection step and does not provide the from-scratch HTML-to-editable-Express path assumed by the specs. That conflicts with the zero-human-intervention requirement.

Required fix: make the client brief describe outcomes and editable-source requirements, not connector function names. Maintain a separate, versioned execution profile for each host.

### 2. Five Invalid CSV Inputs, Repaired In This Audit

The following inputs are syntactically malformed, not merely intentionally messy:

- LAYOUT-05: `valcere_book.csv`
- LAYOUT-10: `alderwood_programme_numbers.csv`
- LAYOUT-12: `umbra_nights_autumn.csv`
- MOTION-02: `ironwood_skus.csv`
- MOTION-08: `sentinelmesh_messaging.csv`

Corrected replacements are staged under `remediation_assets/` and installed in the source corpus. For LAYOUT-10, the source is now two valid tables because it previously combined two different schemas in one CSV. The original files are preserved under `studiobench_source_archive_2026-09-15/` in the source project.

Validation result: 1,841 of 1,841 assets pass. The LAYOUT-10 spec and manifest, aggregate, validation report, remediation matrix, and fingerprint were regenerated. This item is resolved and now needs to be committed with the rest of V3.

### 3. Ten Motion Tasks Need Timecoded Evidence

MOTION-06, MOTION-07, MOTION-08, MOTION-09, MOTION-10, MOTION-15, MOTION-16, MOTION-17, MOTION-19, and MOTION-20 require word- or topic-precise editorial decisions.

The current Quick Cut operation is visual-engagement based and explicitly does not perform semantic or speech-based trimming. Media summary is not a timecoded transcript. Timeline rendering can execute known cuts but cannot infer the necessary source times.

Required fix: add a timecoded transcript or source EDL to each task. Score the agent's editorial selection, ordering, pacing, and compliance, rather than whether a host happens to expose speech-to-timecode.

### 4. Fifteen Vector Tasks Overclaim Production Capability

All VECTOR-01 through VECTOR-15 are credible professional briefs, but raster vectorization alone cannot establish screen separations, closed cut contours, engraving geometry, trapping, optical reductions, or manufacturing-ready path cleanup.

Required fix: either allow an auditable SVG/path-authoring route for both systems or narrow the acceptance contract to what the connector can actually produce and inspect. Do not award production-readiness points from a vectorization success response alone.

### 5. Six Truth-Sensitive Image Promises

- PHOTO-03: one source window is clipped to pure white and cannot be recovered.
- PHOTO-05: dusk treatment must distinguish tonal relighting from generated architecture or sky.
- PHOTO-10: colorways derived from one photographed garment are concept proofs, not production color approvals.
- PHOTO-11: seven product and on-lip shades derived from one physical sample are concept proofs and require sample or reshoot approval.
- PHOTO-16: glare-obscured grading labels require a reject/reshoot disposition.
- PHOTO-27: the missing flavor image must remain a declared content gap, not a generated product claim.

Required fix: add explicit truth constraints and acceptable exception states to briefs, automatic checks, and human rubrics.

## P1: Benchmark Quality Corrections

### 1. The Portfolio Is Over-Bundled

Current task-level patterns are unusually uniform:

- 100/100 require editable Express collateral.
- 95/100 require graded imagery.
- 92/100 require data merge.
- 79/100 require vector artwork.
- 97/100 require a handover deliverable.
- 74/100 combine Express, grading, and vector work.
- 92/100 use at least five operation families.

This is hard, but it is not representative of 100 independent freelance commissions. The recurring shape is: normalize a photo set, recover a lost mark, rebuild a printer file, create an editable campaign system, merge records, use Stock or Boards, and document the handoff.

Hardness should come from constrained judgment, revision, production risk, and client-specific tradeoffs. It should not come from forcing nearly every connector family into nearly every task.

Recommended portfolio bands, not quotas:

| Operation | Current | Recommended |
| --- | ---: | ---: |
| Mark recovery | 61 | 15-25 |
| Image grading | 95 | 45-60 |
| Data merge | 92 | 25-40 |
| Vector production | 79 | 20-30 |
| Editable-source deliverable | 100 | 50-70 |
| Adobe Stock | varies | 15-25 |
| Firefly Boards as scored evidence | common | 10-20 |

Keep roughly 30-40 flagship integrated engagements. Re-scope the rest around a dominant expert craft problem with only the secondary outputs a client would plausibly commission at the same time.

### 2. Repeated Client Identities Need Governance

Twenty-four tasks participate in twelve collision groups:

- Corner & Cure: PHOTO-02, LAYOUT-02
- Northgrove: PHOTO-10, LAYOUT-04
- Verranza: PHOTO-04, LAYOUT-08
- Lanternwood: LAYOUT-11, LAYOUT-26
- Aldervale: LAYOUT-15, LAYOUT-25
- Anvil & Oak: LAYOUT-16, MOTION-15
- Apexguard: PHOTO-25, LAYOUT-17
- Kilnmore: PHOTO-12, LAYOUT-18
- Continental Cup: PHOTO-17, LAYOUT-33
- Meridian Summit: PHOTO-19, LAYOUT-23
- Girdermark: PHOTO-14, LAYOUT-27
- Lumora: PHOTO-11, LAYOUT-03

Some are legitimate linked-client engagements. Others are close enough to become leakage or contradictory identity evidence. Lanternwood is the clearest conflict because the two tasks use the same client name with incompatible geography and currency.

Required fix: add `client_series_id` plus a no-co-sampling rule for genuine series. Rename and re-scope contradictory or near-duplicate cases.

### 3. Automatic Verifiers Are Host-Biased

- 276 automatic verifiers across 95 tasks depend on process or tool-return evidence.
- 147 automatic verifiers across 92 tasks directly reference host-specific capabilities or return structures.

Examples include checking a connector's `tradeoffs` field, returned markup, font-style response, board item list, or InDesign mapping readout. Those may be useful trajectory evidence, but they should not be mixed into the host-neutral artifact score.

Required verifier architecture:

1. Artifact checks: dimensions, counts, file integrity, text presence, content reconciliation, color/profile facts, safe areas, page counts, SVG structure, media duration, and other facts visible in the deliverables.
2. Process checks: normalized events such as asset opened, crop decision recorded, licensed asset used, exception declared, test record rendered, revision triggered, and final export verified.
3. Human checks: identity fidelity, hierarchy, coherence, audience fit, motion rhythm, craft finish, and whether the work feels professionally usable.

Each automatic check needs a deterministic fixture, expected pass case, expected fail case, and a host-neutral evidence path.

### 4. Source Provenance Is Overstated

The defensible repository claim is not "all 100 are scraped from Upwork."

The current anchors mention both Upwork and Freelancer.com, often as composites. The older tracked source set has direct source URLs for only part of the collection, and several Upwork references are search URLs rather than direct job-post URLs.

Required fix: describe the set as source-derived composite briefs from a mixed Upwork/Freelancer corpus, rewritten to fictional clients. Maintain a private ledger with platform, source record ID, direct URL where available, title, capture date, source hash, and the task elements derived from it.

### 5. Reproducibility Is Not Yet Protected

The current V3 specs and assets are untracked in the inspected Git worktree. At audit start, `TASKS_V3_ALL100.json` was stale: 49 individual specs differed from it, including 19 substantive differences and 30 verifier-only differences. It has now been regenerated from the authoritative individual specs and installed. The repository-root `ASSET_MANIFEST.csv` inventories an older asset collection and contains no V3 task rows, so the new audit installs a separate V3 manifest rather than overwriting that historical inventory.

A current aggregate and hash manifest have been generated and installed with the audit artifacts:

- `TASKS_V3_ALL100_CURRENT.json`
- `FREEZE_MANIFEST_V3.json`
- `ASSET_MANIFEST_V3.csv`

Required fix: commit the regenerated aggregate, specs, repaired assets and immutable asset manifest; tag the connector capability snapshot by host and date; and freeze only after remediation.

## Asset Review

The visual review found no broad quality crisis. The packs are attractive, coherent, and generally contain enough alternates and defects to support difficult professional decisions. They are often cleaner and more art-directed than a random freelance handoff, so the benchmark should preserve some truly awkward inputs: inconsistent white balance, poor framing, low resolution, duplicate records, missing coverage, contradictory copy, and legally unusable claims.

Do not regenerate the collection wholesale. That would spend money while making the benchmark less realistic. Regenerate only when an asset is unusable, creates identity leakage, contradicts the brief, or cannot support the intended decision. Every generated asset should carry model, version, prompt hash, seed if available, date, and a declaration that it is synthetic benchmark material.

Adobe Stock should be used only when the brief makes sourcing part of the professional job. Stock selection must be judged on licensing, relevance, finish match, and truthful use, not merely on whether an asset was licensed.

Firefly Boards should be optional collaboration or trajectory evidence unless maintaining a shortlist is a real client deliverable. A board is not evidence that the final design is good.

## Recommended Evaluation Design

Run two related tracks:

### Parity Track

Use the intersection of capabilities available to both ChatGPT and Claude. Give both systems the same host-neutral brief, assets, output contract, timecoded evidence where required, and scoring rubric. This track supports direct model comparison.

### Full-System Track

Allow each host to use its strongest native connector routes. Score equivalent final outcomes and normalized process evidence, not identical tool calls. This track measures the product-plus-model system a freelancer could actually use.

Do not combine these scores into one unlabeled leaderboard. A model score, connector execution score, and final craft score answer different questions.

Suggested score decomposition:

- 40% final artifact correctness and production readiness
- 25% human-rated creative quality and audience fit
- 15% identity and source fidelity
- 10% revision quality after an emergent checkpoint
- 10% process discipline, disclosure, and evidence completeness

## Required Schema Additions

Each task should include:

- `primary_craft_problem`
- `required_deliverables`
- `optional_stretch_deliverables`
- `host_neutral_acceptance`
- `host_execution_profiles`
- `client_series_id`
- `source_provenance_ids`
- `truth_constraints`
- `known_asset_defects`
- `allowed_exception_states`
- `scoring_weights`
- `estimated_expert_hours`
- `expected_revision_loop`

Tool names belong in `host_execution_profiles`, not in the client-facing brief or host-neutral artifact contract.

## Remediation Order

1. Rotate all credentials that were shared in chat. Do not place them in specs, logs, reports, or Git.
2. Commit the installed CSV repairs, the LAYOUT-10 two-table spec/manifest update, and the archived source evidence.
3. Preserve the clean validation result of 1,841 of 1,841 assets after every subsequent corpus edit.
4. Create versioned ChatGPT and Claude connector capability profiles from live tool introspection.
5. Rewrite the output contracts to be host-neutral and move tool-specific steps into execution profiles.
6. Add timecoded transcripts or EDLs to the ten semantic motion tasks.
7. Decide the common vector-authoring route and revise all fifteen vector acceptance contracts.
8. Add truth constraints to the six image-sensitive tasks.
9. Resolve the twelve identity collision groups and add sampling exclusions.
10. Re-scope the 92 over-bundled tasks, retaining only the multi-surface combinations a client would plausibly buy as one engagement.
11. Split automatic verifiers into artifact and normalized-process layers, then unit-test every verifier.
12. Build the private source-provenance ledger and correct the public corpus description.
13. Regenerate the authoritative aggregate, commit the corpus, freeze hashes, and run a small human pilot before the full benchmark.

## Freeze Gates

Do not declare V3 final until all of the following pass:

- Every manifest asset exists and decodes or parses.
- Every required deliverable is executable under its declared host profile.
- Every parity-track task is executable on both hosts without human template selection.
- No artifact score depends on a vendor-specific response field.
- Every process event uses the shared trajectory schema.
- Every vector production claim has inspectable geometry evidence.
- Every semantic motion cut has timecoded source evidence.
- Every truth-sensitive task permits an honest reject, reshoot, or concept-proof outcome.
- No conflicting client identity can leak across train, development, or test samples.
- The aggregate, individual specs, manifests, and hashes agree.
- At least two experienced creative professionals pilot a stratified sample and agree that the brief, supplied assets, budget band, and deliverables form a plausible engagement.

## Bottom Line

The collection is substantially better than a generic creative benchmark and is worth preserving. It is not yet "perfect," and freezing it now would measure connector availability and specification overreach as much as creative intelligence. The path to the best version is targeted repair and portfolio rebalancing, not wholesale asset generation.
