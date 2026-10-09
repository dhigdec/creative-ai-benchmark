# Gatsby V7 feedback-patch tooling (recovered snapshot)

These files produced `docs/gatsby-v7` from `docs/gatsby-v5` (2026-09-25 to 28). They originally lived in a Claude session
scratchpad that macOS cleared on 2026-10-08; these copies were recovered from Claude Code's file history, so they are the
**last saved snapshot, possibly one edit behind** the version that ran.

| File | Role |
|---|---|
| `apply_feedback.py` | Deterministic applier: reads `patches/<ID>.json`, applies sentence edits, brief insertions, deliverable bindings, palette roles/rules, checks_modify/add/retire to every copy of a task; guards (no dashes, 40 words, valid K ids, verbatim quotes, no new trap-exposing source_record, auto checks untouched, duplicate ids); Option B sampling; register leak stripping. Dry run by default, `--go` to write, `--only <ID>`. `G5_DIR` env var points at the target version folder. |
| `GUIDE.md` | Instructions given to the per-task patch-authoring agents (the feedback, ground rules, patch schema). |
| `FINALIZE.md` | Instructions for the finishing pass (consolidate rule checks, resolve duplicate ids, justify cleared bindings). |
| `build_photo04_patch.py` | Reference patch for PHOTO-04 (Verranza), revision 2; every value read from the task's own files. |
| `patch_palette_renderer.py` | Patches the page renderer to show palette roles (mandatory/optional) and colour rules on the Brand tab. |

**Not recovered:** the 100 per-task `patches/*.json` and `builders/*.py`. The authoritative record of what each patch did
is the diff `docs/gatsby-v5/tasks/<ID>` vs `docs/gatsby-v7/tasks/<ID>`, plus the per-task summaries in
`context/workflows/feedback_v7/wf_1dfe146e-1c6.json` (authoring/review/repair) and `wf_ebb4f703-494.json` (finalize).

Paths inside the scripts point at the old scratchpad and at `~/Documents/ChatGPT/Adobe_Gpt/publish/creative-ai-benchmark`;
adjust before reuse. Never point it at `docs/gatsby-v6` (another team's build) or at a published version folder; copy to a
new folder first.
