# Finishing pass, 2026-09-27: consolidate, resolve, justify

Your task's patch already exists and passed two independent reviews and a repair. Do NOT redo that work. You are
making four targeted changes. Read GUIDE.md (same folder) for the ground rules; everything there still holds.

Patch: `.../scratchpad/feedback/patches/<ID>.json`. Builder: `.../scratchpad/feedback/builders/<ID>.py`
(for PHOTO-04 it is `.../scratchpad/feedback/build_photo04_patch.py`). Prefer editing the builder and re-running it,
so every value stays copied from a file. A frozen copy of the pre-pass patch is in `patches_pre_consolidation/<ID>.json`;
never edit that copy.

## 1. Consolidate type and palette rule checks: ONE check per rule per deliverable (client decision "B")

The client chose: every rule is still checked on every distinct design, but as ONE check per rule per deliverable,
covering every heading, subheading and fine-print line that rule governs. Rules were often split into several
checks on the same deliverable. Merge them.

Merge when two or more K2_Q3 checks on the SAME deliverable state the SAME rule:
- the same face and weight for different text roles ("body is Graphik Regular", "captions are Graphik Regular with
  tabular lining figures", "prices are Graphik Regular tabular lining") becomes one check naming every role:
  "Body copy, captions, specification lines and prices on <deliverable> are Graphik Regular with tabular lining
  figures, never Graphik Bold."
- the facets of one colour rule (panels solid at full opacity, and no scrim over the photograph) become one opacity
  check; the accent colours' allowed uses and their area cap become one accent check; allowed grounds and type
  pairings become one pairing check.
Keep separate: genuinely different rules (a starburst ban, a price-in-sentence rule, the signature move, the measure,
"no gold"). "No gold" stays its own check because the reviewer named it explicitly.

Constraints:
- Never drop a rule. Every rule that had at least one check on a deliverable must still have one there.
- A merged check still states ONE rule, names every text role it covers, stays objective, answerable Yes or No,
  at most 40 words, no em or en dash. If one rule cannot fit in 40 words, split it into the FEWEST checks.
- Existing checks (checks_modify) count. You may fold an added check into an existing one by rewriting the existing
  one; then remove the added one.
- Sampling of templated runs (groups of more than 6 outputs) is now enforced by the tool: K2_Q3 checks stay only on
  the first output, the last output, and outputs carrying a K1_Q5 check. You need not sample by hand.
- Content, record, asset, geometry and hierarchy checks (not K2_Q3) are NOT consolidated and never sampled.

## 2. Duplicate check ids (MOTION-09, -10, -11, -12, -13, -14, -17, -18)

Some tasks carry two different checks under one id; the stale copy came from an earlier reframe of the MOTION tasks
to five-second clips. The tool now REJECTS any task that still has a duplicate id after its patch. For each duplicate:
- decide from the brief (as pinned) and the files which copy is current;
- retire every earlier copy with `checks_retire`: `{"check_id", "occurrence": <1-based, earlier copy>, "check": <its
  exact current text>, "why": <reason>}`;
- if an EARLIER copy is the correct one, rewrite the last copy to it via `checks_modify` and retire the earlier one.

## 3. Unresolved critical findings (only where your prompt lists them)

Fix each exactly, from the files. They came from a fresh adversarial re-check after repair.

## 4. Cleared bindings must be justified

If your patch clears an existing `source_image` or `source_record` (sets it to null or empty), `change_log` must name
the trap that binding exposed (quote asset_plan.json defect_engineered, or the owner or client note). If you cannot
name one, restore the binding by removing that clearing entry. Do not clear anything new.

## Finish

Run `python3 .../scratchpad/feedback/apply_feedback.py --only <ID>`. It must print `accepted: 1` and NO
"duplicate check id" rejection. Then return the structured summary: rule checks before and after consolidation, what
you merged, duplicates retired, criticals fixed, bindings kept or restored.
