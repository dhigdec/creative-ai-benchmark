---
name: project-adobe-flagship-round3
description: "Round-3 flagship complex tasks (5366/3437/3252/5388/1559) — specs, generated packages, judge/loop state as of 2026-06-11"
metadata: 
  node_type: memory
  type: project
  originSessionId: 09201e3d-eb58-45af-860b-50daa011f950
---

# Adobe flagship round 3 (2026-06-11) — complex multi-deliverable tasks

Supersedes the "5 executed tasks too trivial" state in [[project_adobe_execution_survey]]. User direction:
complex creative workflows with composed final deliverables, work-order briefs (not job ads), realistic
(non-AI-looking) input assets, judge + closed-loop verification, multi-agent parallelism approved.

**The 5 flagship tasks** (picked from 1,260 by specificity/complexity ranking; shortlist + 5 alternates with
full records in `Adobe-Freelance-Leads/flagship_shortlist.json`; dupes: 2689=5366, 4928=4929):
- 5366 wedding-signage — 6-piece print suite, exact dims (20x30in…47.2x35.4in), persona Maren & Elliot Hartwell, anchor = signature_drinks_sign.png (kept untouched)
- 3437 blausweta-insert — real German retailer Blausweta-Rasur, 2-sided DIN A5, SHOP7/DANKE5 codes, German Sie-form copy, PDF/X-4 specs
- 3252 thc-postcard — distributor persona "Arch & Prairie Beverage Co.", verbatim copy deck, 9 brand stand-in logos, REAL scannable QR pngs (new `program` asset kind)
- 5388 teentalk-ads — 3 concepts × 3 formats, 6 candid mother/teen photos (gpt-image-2, realism doctrine: pores/hair flyaways/hands), purple round stamp
- 1559 george-inn-menus — 3 tri-folds, 25 exact sections (11/8/6), 104 priced UK items, crest logo

**Infrastructure added** (in `asset_pipeline/`):
- `flagship_specs/` package: CONTRACT.md (authoring contract incl. photorealism doctrine) + spec_<id>.py × 5
  (each self-contained, exports SPEC + BRIEF_MD + self-test); merged into specs.py via FLAGSHIP_SPECS;
  FLAGSHIP_ORDER = [1559, 3437, 5366, 5388, 3252]
- generate.py: new asset kind `"program"` (deterministic python render, e.g. qrcode lib; `program_fn(ctx, paths)`)
- contact_sheet.py: handles program-kind/binary files (was crashing on QR pngs)
- TASK.md (rewritten work-order brief) written into each input_assets/<task>/ folder
- venv has `qrcode` lib now

**Generation results** (~$9 total incl. retries; 38 images): all 5 packages generated.
QC scores mostly 8-10; realism photos (5388, 3252 patio, 1559 pub, 5366 floral, 3437 warehouse) verified
excellent by direct viewing. Organic defect caught by deterministic checks: 3437 insert_copy.json has 5/6
back_benefits (missing the truck/shipping row) → ready_for_agent=False, left deliberately for the judge
--improve loop to repair as a live demo. Manually fixed via feedback.json surgical patch: 3252 trailing
period on "Don't Be That Dude." (6s, verbatim check now PASS) + SUP logo regen (was reading "SUR").

**Vision-QC lesson:** generic per-asset criteria that NAME specific spellings (CURRNT, HiSide…) confuse the
single-image judge on multi-image assets — it compares every image against all names (false 3s). Verify
visually before regenerating on low multi-image scores; or write membership-style criteria.

**Judge recheck (2026-06-11, all evidenced):**
- Found+fixed 3 judge-HARNESS bugs the bigger flagship packages exposed (judge.py load_package):
  (1) text assets truncated at 4k chars with NO marker → panel called 25KB drink_menus.json "malformed,
  menus missing" → 1559 scored 3.5; fix = compact JSON + 12k cap + parser-verified excerpt marker;
  (2) program-kind files invisible to panel ("QR codes missing") + MAX_IMAGES=10 overflowed 3252's 13
  images ("no lifestyle photos") → fix = include program images (flagged deterministic) + MAX_IMAGES=16;
  (3) .render duplicates wasted tokens → skipped. Also: true source dims now shown per image (thumbnails
  misread as low-res), and a SCOPE RULE added to the completeness band (inputs = what the client's own
  brief promises; deliverables are the workflow's job — don't demand per-piece drafts).
- After fixes: 1559 3.5→10.0, 3252 6.3→8.4, 5388 10.0, 5366 6.9 (panel-contested: gpt 4.4 / claude 6.8 /
  gemini 10 — strict judges over-index on input-res vs 300dpi print targets, a real workflow constraint).
- Sabotage test on NEW spec 5366: intact 6.9 → delete 2nd signature drink → deterministic_defects fires
  (signature_drinks==2) → 3.5 REJECT (gated cap overrules Gemini's 9.05) → restore → defects NONE, back
  to exactly 6.9. Crisp, reproducible.
- Closed loop on 3437's ORGANIC defect (writer produced 5/6 back_benefits twice; honestly marked FAILED):
  judge --improve ran 2 rounds → surgical patch + icon regen → 3.5→8.1, loop_success=True. Follow-up
  manual patch swapped the 6th benefit to the truck/shipping one so icon_set pairing is exact.
- Other manual fixes via feedback.json surgical patches: 3252 "Don't Be That Dude." trailing period
  (6s, verbatim PASS), SUP logo regen (was reading "SUR" — wave merged into P).
- judge.py all_task_ids() now includes FLAGSHIP_ORDER (was only the old 10).

**Next steps:** EXECUTION phase — composition decision still open (hybrid HTML/PIL compositor vs
connector-only vs Canva MCP probing — see [[project_adobe_execution_survey]] §0); then run the 5 flagship
Adobe workflows end-to-end and extend the annotation survey.
