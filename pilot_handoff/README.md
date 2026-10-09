# StudioBench Pilot — Expert Handoff Package (OPS 4-STAGE MODEL)

Dry run of the full 4-stage Creative AI Benchmark pipeline on **2 image tasks**. Two warm-contact
freelancers each take one task end-to-end; the AI agent (Claude via Adobe connectors) runs the same
tasks separately for the Stage-4 human-vs-agent comparison.

## The 2 pilot tasks (image modality)
| Task | Title | Family | Difficulty | Tool calls | Deliverables | Golden verifiers |
|---|---|---|---|---|---|---|
| AO-13 | Taco Tuesday & Lunch-Special Meta Ad Photo-Asset Prep — Retouch, G | Photo & Image | T3_complex | 19 | 10 | 11 |
| AO-115 | Rukmini Silverworks 925 jewelry catalog: batch isolate-on-pure-whi | Photo & Image | T4_expert | 45 | 2 | 12 |


## The 4 stages (ops model — 2026-07-14 sync)
1. **Stage 1 — Metadata verification:** confirm the task's taxonomy/metadata tags are correct and
   the task is valid (7 Yes/No). -> `stage1_metadata_verification.csv`
2. **Stage 2 — Asset validation + verifier writing:** validate the input package (8 dims,
   Pass/Fix/Reject) AND the freelancer *writes the task verifiers* themselves (atomic checks with
   type / pass-condition / capability / weight). -> `stage2_asset_validation.csv` +
   `stage2_write_verifiers_TEMPLATE.csv`
3. **Stage 3 — Human SFT (creative execution):** actually produce the deliverables. Log every step
   (tool + one-line reason) and capture the trajectory — screen-record (no audio) OR a
   before/after screenshot at each tool call (one freelancer does each, to compare). ->
   `stage3_trajectory_steplog.csv`
4. **Stage 4 — Agent-vs-human comparison & scoring:** binary Pass/Fail on the verifiers, craft +
   process/honesty checks, the professional call (accept / send-back / scrap), the
   **"would people actually buy this?"** question, and the A/B human-vs-agent comparison. ->
   `stage4_comparison_scoring.csv`

## Files per task folder
`BRIEF.md` (verbatim brief + input list + deliverables + suggested workflow) · `assets/` (client
input files) · the four stage sheets above.

## For OPS (not shown to the freelancer before Stage 2)
`pilot_verifier_mapping.csv` = the **golden/reference verifier set** for both tasks (task list +
verifier mapping ops requested: check, type, pass condition, capability, weight). Used to (a) compare
against the verifiers the freelancer writes in Stage 2, and (b) drive the Stage-4 binary scoring.
> Note: verifiers currently exist for 67 of the 100 tasks; both pilot tasks are covered
> (AO-104 authored 2026-07-15; AO-32 reconciled — a stale Firefly-board verifier was removed).
