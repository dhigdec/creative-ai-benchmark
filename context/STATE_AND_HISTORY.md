# What happened, in order (June to October 2026)

For June to mid-September in depth, read `PROJECT_FULL_CONTEXT.md` and `PROJECT_CONTEXT_HANDOFF.md` (repo root) and the
notes in `context/memory/`. This file is the short version plus everything after 2026-09-17.

## June to August: from freelance-task research to the AO-* corpus
- Mined real freelance creative jobs, kept the ones the Adobe connector can actually do (verified doable set: 1,170).
  Mapped connector execution modes (truly headless vs interactive Express vs async video/audio vs authored template).
- Built flagship and "mega" long-horizon tasks and executed several live through the connector.
- StudioBench AO-* corpus: 100 tasks with generated client input assets (multi-model generation + 4-layer QC),
  July pilot of AO-13 and AO-115 (`docs/pilot/`).
- Late August quality audit: only 5 tasks passed; rebuild waves to make every task non-trivial, connector-doable and
  IP-safe (`remediation/audit-fixes-2026-08-24`, guidance docs now on the codex branch).

## September 10 to 15: StudioBench V3
- 100 new deep-orchestration specs: PHOTO 30, VECTOR 15, LAYOUT 35, MOTION 20; 4 to 6 Adobe surfaces per task, 3 runtime
  traps each, engineered defects in the supplied assets.
- 1,807 input assets generated for all 100 tasks (images, press PDFs, CSVs, notes, Seedance video, TTS).
- Lives on branch `codex/studiobench-v3-audit-rebalance` (briefs rewritten with distinct client voices, canonical names).

## September 17 to 21: review site V4 then V5
- V5 (2026-09-19): objective-only verifiers, K-sectioned, 18,118 atomic checks, plain language, no dashes.
- 2026-09-21: IP-leak sweep (77 real-mark leaks across 27 tasks; masked inpaint is the only safe fix), type-system cards
  on all 100 tasks, banner removed, PHOTO-04 and PHOTO-13 completed runs + trajectories published into V5.
- MOTION tasks were reframed to five-second short-form clips (workflow `motion-5s-reframe`).

## September 25 to 28: reviewer feedback applied to all 100 tasks, Gatsby V7
- Reviewer feedback (Verranza PHOTO-04 as the worked example): specific briefs, palette mandatory/optional with
  distribution and opacity rules, typography rules on every deliverable, verifier consistency, asset checks naming the
  exact file and deliverable.
- Pipeline: per-task patch authored by agents → two independent reviews → repair → finalize (consolidation, duplicate ids,
  justified binding changes) → deterministic apply to every copy. Policy B sampling; register trap leaks stripped.
- Built as `docs/gatsby-v7` because `docs/gatsby-v6` had meanwhile been published by a separate effort.
  Pushed 2026-09-28; media had to be force-added (gitignore) to stop 404s.

## September 28: assessment set for the ops team
- Picked 10 mostly-PHOTO tasks; ops review flagged 4 (PHOTO-12, 22, 25, 27); vetted 13 more candidates with 6 lenses;
  8 rejected for source-asset authoring flaws. Final 10: PHOTO-04, 06, 08, 10, 19, 20, 24, 26, 28, LAYOUT-15.
  Details in `PILOT_10.md`.

## September 29 to 30: annotation pilot pages
- `docs/gatsby-v7/annotation-pilot/` built for the 10 (client-facing briefs, full typography cards, answer-free verifier
  bank, PDF previews). Briefs and typography synchronized back into the V7 task files.

## October 7: in-house creative expert feedback
- Points on deliverable checklists and purpose, typography/font availability, logo files, rubric Q8 and Decision Quality.
- Assessed and planned (`EXPERT_FEEDBACK_2026-10-07.md`); waiting on 3 decisions. Nothing implemented yet.

## October 9: context consolidation
- This `context/` folder, root `CLAUDE.md`, recovered V7 tooling (`tools/gatsby_v7_feedback/`), workflow archives, and the
  V3 working files that existed only on disk (committed to the codex branch, commit `2ad5cf9`).
