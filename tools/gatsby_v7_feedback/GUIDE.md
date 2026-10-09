# Review-feedback pass, 2026-09-25: how to patch one task

You are fixing ONE benchmark task so it satisfies a reviewer's feedback. You do not edit corpus files.
You write one patch file; a deterministic tool (`apply_feedback.py`) applies it to every copy of the task.

## The reviewer's feedback (verbatim)

1. **Briefs**: Need to be specific enough to avoid ambiguity. E.g., the CSV had 3 rates, but the brief didn't
   specify which season/rate to use for the hero image, which led to an arbitrary interpretation.
2. **Colour palette**: Need clearer guidance on colour distribution/mandatory vs optional colours. Opacity
   variations introduced by the model also make some checks difficult to judge.
3. **Typography**: Requirements like "no gold" or specific fonts need to be checked consistently across all
   relevant deliverables/headings/subheadings/fine print, rather than selectively. The task also included
   additional limitations which were not checked either.
4. **Verifier consistency**: If a requirement is important enough to verify (e.g., season-specific content or
   use of specific assets), it should be applied across all relevant deliverables. Some current verifiers
   check this for only one deliverable.
5. **Asset checks**: Where specific assets are referenced, the verifier should clearly identify which asset and
   which deliverable it is referring to, rather than naming the whole group (e.g., instead of "Verranza", say
   "Verranza-pool" or "Verranza-terrace").

## The worked reference: PHOTO-04 (read it before you start)

- Patch: `/private/tmp/claude-501/-Users-dhiren-Downloads-Deccan/e4e5b6fa-8315-4aad-9a2e-58b8b08d9714/scratchpad/feedback/patches/PHOTO-04.json`
- Builder that produced it (shows the reasoning): `.../scratchpad/feedback/build_photo04_patch.py`

What PHOTO-04 did, and why (revision 2, after two independent reviews):
- rates_2027.csv had three seasonal rates per house and nothing said which one a booking hero quotes. The brief
  now says "that house's lowest 2027 nightly rate ... shown as a from price with its season named". It names the
  CRITERION in client voice without naming the season, so the executor still has to find the season word through
  owner_note.txt.
- The hero photograph is deliberately NOT pinned: two terraces are portrait and Oliveto's terrace carries the strongest
  green bounce, so choosing is part of the test. Each hero's asset check names that house's four frames by filename,
  never "the Verranza frames", and a separate check fails any generated or extended pixels.
- No source_record was added: it would have printed the owner's corrections into the register the executor reads.
- The palette got a role and a usage per colour, plus explicit distribution, opacity, forbidden and photography
  rules. The delivered hero had a translucent blue panel whose pixels matched no palette hex; the opacity rule
  (solid only, no scrim over photography) makes that judgeable, and it is grounded in the brand's own values.
- Every type rule (no gold, no numeral in the serif, Light-only serif, the oversized initial, Regular-only rates,
  the 65-character measure) is now checked on all three heroes AND the brochure.
- Checks that existed on one hero (palette, hierarchy, cast correction, geometry, water colour) now exist on every
  hero, each naming ITS OWN source frame.
- The traps were left alone: S1/S2/S3 to season words, Scogliera sleeps 10 not 9, the sold Casa Fienile. Those are
  settled by owner_note.txt, so they are the test, not an ambiguity.

## Files to read for your task `<ID>`

- `/Users/dhiren/Documents/ChatGPT/Adobe_Gpt/publish/creative-ai-benchmark/docs/gatsby-v5/tasks/<ID>/TASK_SPEC.json`
  (client_brief, brand_identity incl. palette and type_system, deliverables with required_content,
  acceptance_requirements, source_record, source_image, deliverable_groups, assets)
- `.../docs/gatsby-v5/tasks/<ID>/VERIFIERS.json` (existing checks and their ids)
- `/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/input_assets_v3/<ID>/asset_plan.json` (defect_engineered per
  asset: these are the deliberate traps)
- EVERY data or text file in `/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/input_assets_v3/<ID>/assets/`
  (csv, txt, md, json, tsv). Read them in full. Every value you put in a check must be copied from these.

## Rules

### 1. Brief specificity (feedback 1)
Find every requirement that depends on a choice among several candidates in the supplied data (several seasonal
rates, several prices or sizes or variants, several photos of one subject, several approved copy lines, several
dates) where NO supplied source settles which one applies. Pin it.

- Pin with a `sentence_edits` entry on the EXACT sentence as it appears in the task text. Copy `find` byte for byte
  from TASK_SPEC.json. Prefer sentences that also appear in `deliverable_groups[].requirements` and
  `deliverables[].required_content`, so the brief, the group and every deliverable stay in sync.
- Pin the criterion in the client's voice, not a bare answer, and never in the vocabulary of a trap. PHOTO-04's pin
  says "that house's lowest 2027 nightly rate", NOT "Spring": the season word is a trap (the sheet says S1 and the
  owner note maps it), so naming it in the brief would give it away. Pick a criterion that lands on the same answer
  without revealing any mapping, correction or exclusion.
- If something is checked but nothing in the brief requires it (PHOTO-04's gate monogram was checked in the brochure
  but placed nowhere), pin where it goes, again without naming a trap.
- DO NOT pin anything a supplied source already settles. A conflict between files that one file resolves (an owner
  note overriding a sheet, a sold or withdrawn item, a renamed label, a corrected figure, an excluded row, a
  permission restriction) is a deliberate trap. Leave it, and list it in `traps_preserved`.
- Never remove difficulty that asset_plan.json declares as defect_engineered.
- If the brief is already unambiguous, make no sentence edit. Do not rewrite for style.

### 2. Bindings (UPDATED: read carefully)
**Do NOT add `source_record`.** The executor reads the output register ("The output register defines exact filenames,
pages, sizes and record bindings"), so a bound row with its approved values printed next to its raw values hands the
executor every correction the task is testing (an owner's corrected figure, a mapped label). An independent review
caught exactly this in the first PHOTO-04 draft. The apply tool now rejects any new source_record whose values differ
from its raw values.
- You MAY add `source_image` only when the brief already implies exactly one photograph for that deliverable AND the
  binding removes no choice that asset_plan.json marks as a trap. When in doubt, do not bind: write the check so it
  names the candidate files instead ("built from one of oliveto_pool.jpg, oliveto_terrace.jpg, oliveto_bedroom.jpg
  or oliveto_living.jpg").
- Leave existing bindings alone.

### 3. Palette (feedback 2)
For EACH existing palette colour (match by hex; never add, drop or rename a colour) give:
- `role`: "mandatory", "optional accent", or a scoped mandatory such as "mandatory where type sits on Lime Wash".
- `usage`: where it goes (grounds, type, panels, rules, buttons, accents), concretely.
Then `palette_rules` with four strings:
- `distribution`: which colours may be grounds, which may be type colours and on which grounds, and a cap for accents
  (for example "together no more than 5% of the designed, non-photographic area, never a ground").
- `opacity`: default "every palette colour is used solid, at 100% opacity; no tint, transparency, gradient, shadow or
  blend mode; no scrim, gradient or overlay of any colour, black and white included, laid over a photograph". Allow a
  tint ONLY if the brand identity already implies one, and then give its exact value and the one place it may be used.
- Check the supplied brand files (existing cards, labels, sheets, PDFs) for the colours they actually use and derive
  the hierarchy from them. PHOTO-04's agent card sets the house name in Verranza Blue on Lime Wash, which a first draft
  had wrongly forbidden. A rule that contradicts a supplied brand file is wrong.
- Scope colour prohibitions to the design (type, panels, rules, buttons, icons). "No gold anywhere" wrongly reaches
  into photographs, which may legitimately hold golden light.
- `forbidden`: whatever the brand identity or type rules forbid (gold, metallic, a colour it rejects), plus "no colour
  outside the palette hexes for type, panels, rules, buttons or icons".
- `photography`: photographs keep their own corrected colour and are not recoloured toward the palette; name any
  engineered colour trap that must not be pushed toward the palette.
Ground every role in the brand identity text (about, voice, values, type_system, notes). Invent no brand facts.

### 4. Typography coverage (feedback 3)
Take every rule in `brand_identity.type_system.rules`, the `signature_move`, and the faces and weight limits in the
scale. Each becomes checks on the deliverables it governs (see the sampling policy below): display face and weight
for headings, text face for body and fine print, numeral rules, colour prohibitions such as "no gold", measure
(maximum characters), case and tracking rules that a grader can see, the signature move.
Refresh stale evidence: any existing check whose evidence quotes old typography prose (for example "an elegant
serif ... a quiet humanist sans") must be rewritten to cite the current type_system.

### 5. Palette checks
On the deliverables the sampling policy selects: colours only from the palette hexes; the opacity rule; the mandatory
colours present where the palette rules require them; forbidden colours absent.

### 6. Consistency (feedback 4)
For every requirement already checked on one deliverable (season or label wording, a corrected record value, an
exclusion, a specific asset treatment, hierarchy, cast or colour correction, geometry preservation, a required
line of copy), add the equivalent check to EVERY other deliverable where the same requirement applies. Content
checks go on every output, never sampled. Engineered-defect checks stay specific to the asset that carries the
defect, but each sibling deliverable gets its own check for its own source asset (each hero gets a cast check for
its own frame).

### 7. Asset naming (feedback 5)
Every check that refers to a supplied asset names the exact filename(s) and the exact deliverable file. Never a group
("the supplied photos", "the verranza frames", a brand or villa name alone). Rewrite existing checks that do this
with `checks_modify` (same check_id), including evidence and `reference_assets` (specific filenames only; drop long
group lists). Name people, places and products by their full record names ("Casa Verranza", never "Verranza").

### 8. Sampling policy for rule checks (decided by the client)
- A **distinct design** is an output with its own layout or role (a hero, a poster, a brochure, a film, a cover).
  Every distinct design gets EVERY applicable type and palette rule. Any group with 6 or fewer outputs is treated as
  distinct designs: all of its outputs get every rule.
- A **templated run** is a group of more than 6 outputs produced from one layout across rows of a data table (for
  example 39 cold-case labels). In a templated run, every type and palette rule goes on this fixed, NAMED set:
  the first output, the last output, and every output whose record carries a trap or an edge case (a corrected or
  owner-overridden value, a special character, the longest text value that risks overflow, a missing optional
  field). Record which outputs you chose and why in `change_log`.
- Content and record checks are never sampled: they go on every output they apply to.

### 9. Check style
- One observable fact, answerable Yes or No, objective. At most 40 words; aim for 30 or fewer.
- Deliverable written as `“<deliverable name>” (<file>)`. No brand prefix like “Brand / Deliverable”.
- No em dash or en dash anywhere in anything you write. Use a comma, a colon, or a plain hyphen.
- `k_id` from: K1_Q1 content completeness, K1_Q2 specification accuracy, K1_Q3 constraint compliance, K1_Q4
  deliverable completeness, K1_Q5 critical failure, K2_Q1 asset selection, K2_Q2 asset preservation, K2_Q3
  brand-system compliance, K2_Q4 identity fidelity, K5_Q1 primary-message recovery, K5_Q2 information hierarchy.
  Type and palette rules are K2_Q3. Record values K1_Q1. Label and wording rules K1_Q3. Trap failures K1_Q5.
- Values are copied from the records, never typed from memory.
- Evidence that presents itself as a quote from a file ("owner_note.txt: ...") must be VERBATIM. Paraphrase without
  the "file:" framing, or quote exactly.
- Every file an evidence line cites must also appear in reference_assets.
- A colour-correction check must not contradict another requirement: after a cast is removed, water hue moves, so
  write "still reads deep blue as in verranza_pool.jpg, not pale turquoise, grey or green", not "no shift at all".
- Never modify an automatic check (ids ending A###). Never duplicate an existing check. Never contradict the brief.
  Never change a filename, S3 key, output id or record.

## Process

1. Read the reference patch and builder. Read every file listed above for your task.
2. Write a small builder script at `.../scratchpad/feedback/builders/<ID>.py` that reads the records and emits the
   patch, the way build_photo04_patch.py does, so every value is copied from a file. Run it to write
   `.../scratchpad/feedback/patches/<ID>.json`.
3. Validate: `python3 /private/tmp/claude-501/-Users-dhiren-Downloads-Deccan/e4e5b6fa-8315-4aad-9a2e-58b8b08d9714/scratchpad/feedback/apply_feedback.py --only <ID>`
   It must print `accepted: 1`. Fix every guard it reports and re-run until it does. It is a dry run and writes nothing.
4. Never edit anything under docs/gatsby-v5. The tool does that later, for all tasks at once.

## Patch schema (same as PHOTO-04.json)

```
{
 "task_id": "<ID>",
 "sentence_edits": [{"find": "<exact existing sentence>", "replace": "<pinned sentence>", "why": "<the ambiguity>"}],
 "brief_insertions": [{"after": "<exact unique brief substring>", "insert": " <new text>"}],
 "deliverable_bindings": [{"output_id": "...", "source_image": "...", "source_record": {...}}],
 "palette": [{"hex": "#RRGGBB", "role": "...", "usage": "..."}],
 "palette_rules": {"distribution": "...", "opacity": "...", "forbidden": "...", "photography": "..."},
 "checks_modify": [{"check_id": "<existing human id>", "k_id": "...", "check": "...", "evidence": "...", "reference_assets": ["<filename>"]}],
 "checks_add": [{"output_id": "...", "k_id": "...", "check": "...", "evidence": "...", "reference_assets": ["<filename>"]}],
 "traps_preserved": ["..."],
 "change_log": ["..."]
}
```
