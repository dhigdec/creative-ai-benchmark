# In-house creative expert feedback on the 10-task pilot (2026-10-07)

Status: **assessed, plan proposed, NOT implemented.** Waiting on Dhiren for the 3 decisions at the bottom.

## The feedback (verbatim)

1. Deliverables
   * Sharing the details within each deliverable in a checklist or bulleted format would make it easier for the
     annotators/QCs to evaluate and ensure every aspect is covered.
   * This can be done at the beginning or at the end of the task at the "requested deliverable" section within each file.
   * The end goal of the deliverable should be more defined. For ex. currently the tasks say "a six-page A4 comparison
     brochure" but it's purpose and export version is unclear. If it's for print, the export will need to be in PDF
     (CMYK) format meant for printing or if it is for digital purpose, then it should be clear if it is for social media
     (Instagram post/ story/ reel, etc.), website, presentation, advertisement, etc. These details help in analysing the
     final output through a more defined evaluated lens.
2. Typography
   * There should be someway to give feedback on the typography aspect of the task, which is currently missing. Our
     instruction doc says- "Required fonts and colours are actually available, or derivable from the kit." but the fonts
     files are not accessible in tasks to evaluate.
   * Either within the assets or as an individual entity but if we don't include it within the evaluation then
     annotators/ QC will not even read it
3. Logo asset
   * Industry standard for logos/ wordmarks is to have PNGs/ SVGs with transparent background in order to be used across
     different visual collaterals
   * Sometimes, it is possible that clients do not have any of these, or the quality of the logo is not in a usable
     capacity, then creating a version of the logo that can be used is an additional task for the designer (which needs
     to be discussed with the clients first)
4. Other points
   * Unsure of this question overall- "8. Is it clear which requirements are mandatory and which decisions are left to
     the freelancer?". The creative freedom for the designer isn't defined or mentioned in any of the tasks so far.
     What's to be done and not done sometimes is. So my best guess is, the answer to this will mostly always be yes based
     on the current tasks. Not sure of the impact or the objective for this one.
   * The "Decision Quality" rubric in the instruction doc. deals more with the brand or persona details (tone, audience,
     constraints). But this is coming at an asset level rather than brand/ overall tone level. Unsure about this one too.

## Assessment (checked against the 10 live pilot pages and files)

**Mostly right.** Fonts and deliverable purpose are the must-fixes; checklist and logo are presentation/scoping; the two
rubric points are fair.

1. **Checklist: agree, with a twist.** The pilot briefs were deliberately made client prose and checklist bullets were
   removed on 2026-09-29/30 (commits `44c32ae`, `2fc7945`). Keep the prose (it is what the agent receives) and add an
   annotator-only panel of 5 to 10 bullets per deliverable. The per-output checklist exists as the verifier bank, but at
   110 to 878 items per task it is not readable as a checklist.
2. **Purpose/export: agree fully, strongest point.** None of the 10 tasks states CMYK, bleed, or print vs screen per
   deliverable. PHOTO-04's "six-page A4 comparison brochure" never says whether it is printed for agents or a download.
3. **Typography: agree, but the gap is not scoring.** Output scoring already covers type heavily (e.g. 98 of 215 bank
   items on PHOTO-04). The real gaps:
   - no font files in any of the 10 kits; the type-card samples are drawn in stand-in fonts (the card says the samples
     are not the licensed outlines), so annotators have no true reference;
   - many named faces are probably retail-only and, as far as known, not in Adobe Fonts (Canela Deck, Untitled Sans,
     Financier, Publico, GT Super, Suisse Int'l, Druk, Monument Extended, Basis Grotesque). Free/open ones are fine
     (Source Sans 3, Piazzolla, Instrument Serif, Lexend, IBM Plex Sans, Boska). Freight, Neue Haas Grotesk Text and Miller
     Text need checking. This likely affects about 8 of 10 tasks;
   - every type card says "If a named font is unavailable, ask us before substituting it", so the agent is blocked,
     which breaks Phase 0 "startable without client clarification".
   Fonts named per task: PHOTO-04 Canela Deck Light / Untitled Sans; PHOTO-06 Financier Display / Freight Text Pro
   (+Untitled Sans); PHOTO-08 Publico Banner / Source Sans 3; PHOTO-10 GT Super Display / Freight Sans Pro; PHOTO-19
   Piazzolla / Suisse Int'l (+Mono); PHOTO-20 Instrument Serif / Neue Haas Grotesk Text; PHOTO-24 Boska / Suisse Int'l;
   PHOTO-26 Druk / Publico Text; PHOTO-28 Monument Extended / Basis Grotesque; LAYOUT-15 Lexend / Miller Text (+IBM Plex Sans).
4. **Logo: agree on the standard; keep the skill test.** Five tasks deliberately supply the mark only in unusable form
   (planned traps per `asset_plan.json`): PHOTO-04 photo of a wrought-iron gate plate; PHOTO-08 roundel whose inner ring
   fills solid under a one-call knockout; PHOTO-10 low-res picture with two disjoint marks; PHOTO-20 blind ink-less deboss;
   PHOTO-28 600 px web export with a white square baked in. Real-world situation, but the briefs never say "please make a
   clean version", so it is hidden extra work.
5. **Q8: agree it carries no signal.** Freedom is implicit (anything unstated), so answers will be uniform. Strictly, if
   freedom is not stated, the honest answer is "not clear", not "yes".
6. **Decision Quality: agree.** It is one of the 8 Phase 1 input-asset dims but describes the kit as a whole (audience,
   tone, constraints, which source wins). Rating it per photo yields N/A noise.

## Plan (proposed 2026-10-07)

Build as `docs/gatsby-v7/annotation-pilot-v2/` for the same 10 tasks (V7 and pilot v1 stay untouched because annotators
used them). After the expert signs off, roll the same changes to all 100 as Gatsby V8.

1. **Fonts.** Check each of the 19 named faces (Adobe Fonts / open / retail-only). Replace retail-only faces with the
   closest available face, drop "ask us before substituting", render type-card samples in the real fonts
   (Adobe connector `font_preview`), update every check naming a swapped font, add an auto check on PDF embedded font names.
2. **Purpose per deliverable.** One client-voice sentence per deliverable in the brief ("printed for our travel agents",
   "runs on our booking site"), a "Use" line + export spec on each card. For print PDFs, first test whether the connector
   can export CMYK with bleed; only then make it pass/fail (code-checkable: colour space, bleed box, embedded fonts).
3. **Annotator checklist panel.** 5 to 10 bullets per deliverable on annotator pages only; every bullet cites the brief
   sentence it comes from, so it adds no new requirement.
4. **Logos.** For the 5 degraded-mark tasks, the brief says plainly there is no usable logo file and asks for a clean
   version; the clean mark becomes a named deliverable (SVG + transparent PNG) with checks (present, transparent,
   faithful to source). Traps stay. For the other 5 tasks, check whether outputs need a mark; if so supply a clean file.
5. **Rubric wording.** Add a "Left to you" line per brief (2 to 4 open decisions, checked against existing checks so it
   cannot contradict them). New Q8 wording: "Name one mandatory requirement and one decision left open." Decision Quality
   rated once per task. The instruction doc is not in this repo, so this is delivered as text to paste.

Not changing: engineered traps, existing auto checks. PHOTO-04's completed run will lack the new logo files; flag it.
Verification: integrity guards (page == files, no dashes, 40 words, no duplicate ids), browser pass on all 10 pages, one
reviewer pass over the diffs only.

## Decisions pending from Dhiren

1. **Fonts:** replace retail-only fonts with available lookalikes (recommended), or keep names + an approved fallback.
2. **Logos:** clean mark as a named deliverable (recommended, keeps the skill test), or simply supply a clean logo.
3. **Scope:** pilot-v2 for these 10 first (recommended), or all 100 now.
Also: the Adobe connector must be re-authorised (`/mcp`) to run font search and previews.
