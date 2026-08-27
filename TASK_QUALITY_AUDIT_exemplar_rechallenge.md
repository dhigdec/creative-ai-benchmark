# EXEMPLAR-TIER DECISION MEMO

## 1. THE DEFENSIBLE EXEMPLAR SET

**Zero.** Not one of the 14 re-challenged tasks survived all three lenses. `adobe_showable` is `false` across the board. The best any task reached was 2/3 (AO-17, AO-110, AO-27).

Plainly: **we have nothing to put in front of Adobe today** that is simultaneously hard-for-the-agent, connector-doable, and creatively-authored. The exemplar tier is empty. The pitch's central claim — "a HARD, creative benchmark the agent can actually execute" — is currently unbacked by a single proof task. Do not demo from this set; every candidate fails at least one lens a sharp Adobe reviewer will find in minutes.

The one reusable fragment worth naming: **AO-110 steps 21–27** (the masked-HSL recolor kernel — isolate orange hardware against orange webbing, then luminosity-preserving hue/desat/luminance choice). It survived doability AND creative-substance; it only drowned because 26 of 33 calls around it were batch-grade padding. That kernel is the shape of a real exemplar. Everything else is packaging.

## 2. PASS-TIER CASUALTIES (all 5 fell)

- **AO-15** — agent-triviality + creative-substance: brief is a 1:1 recipe→tool map; the only real design (tri-fold typesetting) is disclaimed to a human designer. STRENGTHEN.
- **AO-17** — agent-triviality: grade-MATCH sold as the hard part, but no verification loop; open-loop params can't fail. Survived the other two. STRENGTHEN.
- **AO-24** — all three: two-preset pick, and the data-merge binds into a `convert_pdf_to_indd` output that won't bind. STRENGTHEN.
- **AO-74** — **connector-doability KILL**: merges into a PDF-converted `.indd` (won't bind) AND wants a multi-record-per-page grid `document_merge_data_layout` can't produce (one file per row). **REPLACE**.
- **AO-110** — agent-triviality: 6-way batch fan-out + identical repeats inflate a 32-call "flagship"; real craft is a 7-call slice. Survived the other two. STRENGTHEN.

## 3. BORDERLINE DISPOSITIONS (9)

- **AO-20 — KILL** (connector-doability): `select_subject` is person-only; invert+fill erases the CNC machine the hero exists to showcase.
- **AO-22 — KILL** (creative-substance): supplied mark + supplied palette + font choice delegated to `font_recommend` = zero agent art-direction.
- **AO-27 — KILL** (agent-triviality): spoon-fed 1–7 recipe with the legality workaround handed over verbatim; hard parts stripped to one-shot equivalents.
- **AO-32 — KEEP-STRENGTHEN** (agent-triviality / creative-substance): doable, but it's invisible corrective retouch toward a right answer, no authored look, no fail-gate.
- **AO-39 — KILL** (creative-substance): asset-prep only; no composed endpoint and connectors structurally can't lay one out.
- **AO-46 — KILL** (connector-doability): `.ai` masters and `.eps` exports aren't connector-producible; SVG→.ai is laundered human work in `inputs[]`.
- **AO-75 — KILL** (connector-doability): badge merge into a PDF-converted `.indd` won't bind; the QR data-merge image field can't exist in a converted PDF.
- **AO-104 — KEEP-STRENGTHEN** (agent-triviality / creative-substance): doable, but `auto_tone` can't transfer the "reference grade the others must match" — the sold hard part is a non-decision.
- **AO-118 — KILL** (creative-substance): endpoint is a folder of filtered assets; layout/type/logo all disclaimed to devs; structural, not fixable in-spec.

Tally: **7 KILL, 2 KEEP-STRENGTHEN, 0 PROMOTE.**

## 4. WHAT A DEFENSIBLE EXEMPLAR HAS (the rebuild bar)

Every casualty missed at least one of these. An exemplar must clear **all** of them:

1. **A failure gate the agent can actually trip** — a verification loop, a measurable target to hit, or a branch where a wrong intermediate must be caught. Open-loop "apply slider in the stated direction" is disqualifying (every casualty's core).
2. **A brief that states GOALS, not METHODS** — sentences must NOT map 1:1 onto tool names. If the agent can transcribe the brief into calls, it's Failure Mode A.
3. **An agent-AUTHORED look, built from primitives** — masked HSL/split-tone/curves the agent must reason to. Not a preset pick, not `auto_tone`, not `quick_cut`, not a supplied `.xmp`/palette the agent merely matches.
4. **Every artifact producible AS WRITTEN** — no PDF→`.indd` merge, no image-frame merge column, no SVG→`.ai` smuggled as input, no `.eps`, no interior-negative-space fill, no image-into-template placement, no opaque plate disclaimed to a human.
5. **Difficulty from DEPTH, not breadth or plumbing** — adaptive reasoning across dependent steps. Strip uploads, folder-creates, repeated identical calls, and auto-ops before counting; what remains must still be hard.
6. **A designed endpoint the agent owns** — a finished artifact whose distinctive quality is the agent's decision, not the client's template and not a canned tool's default.

Template to build against: **AO-110's recolor kernel** — real semantic selection, failable masked color craft, no delegation, a crafted output. Scale that up; don't pad it with batch fan-out.

## 5. THE HONEST HEADLINE NUMBER

**Adobe-ready today: 0 of 100 proven.**

These 14 were the *curated best of the set* — the 5 proposed PASS exemplars plus the 9 strongest borderlines. If the top 14 yield zero survivors, the realistic Adobe-ready fraction of the full 100 is **at or near zero**, not the handful the earlier plan treated as done.

**Impact on the plan:** the earlier plan booked the exemplar tier as effectively finished — ~5 shippable PASSes plus light polish on borderlines. That assumption is dead. Replace it with author-from-scratch:

- **8 REPLACE** (AO-74 + 7 borderline KILLs) = net-new tasks. Five of these (AO-20/39/46/75/118) can't be strengthened inside the connector set at all — new task designs required, not edits.
- **6 STRENGTHEN** (AO-15/17/24/110 + AO-32/104) — but each needs a de-recipe'd goal-brief AND a new failable creative core, i.e. closer to a rebuild than a tweak.
- **Every rebuilt task must re-run the 3-lens challenge** before it counts.

Budgeting ~1–1.5 days to author a genuinely 3/3 task plus a re-audit cycle, and needing a minimum-credible exemplar set of ~5–8, this converts roughly **0–2 planned "polish" days into ~10–15 authoring days plus re-audit** — call it **two-plus working weeks added**, and the Adobe demo must be **gated behind that work**. Do not schedule the pitch against the old timeline; the exemplar tier is a rebuild, not a finish.