# StudioBench — Creative-Agent Benchmark & Data Product
**Taxonomy · Rubrics · Data Tracks · Go-to-Market**
*Master document. Version 2026-06-23.*

---

## 0. What this is, and the goal

We are building a **benchmark that measures whether an AI agent can do real freelance creative work** — take a real client brief plus the client's brand assets, use professional design tools across many steps, and produce a deliverable a client would accept and pay for.

But the benchmark is the *vehicle*, not the product. **We are a data company. The goal is to produce top-quality, unique, licensing-clean data that we can sell** to AI labs and creative-software companies. Everything the benchmark generates — expert demonstrations, agent trajectories, human-vs-agent comparisons, expert scores, defect labels, and a runnable reward — is a sellable artifact.

So this document defines three things together:
1. **The taxonomy** — how we organize the tasks and what we measure.
2. **The rubrics** — how we score (5 computer-based checks + 1 human-based, plus what designers score on).
3. **The three data tracks** — how we run it to manufacture sellable data — and **where and how we sell it.**

---

## 1. The taxonomy (the map of the work)

### 1.1 The core principle — measurement-first, "tag, don't bucket"
Real freelance jobs are messy: one task might retouch a photo *and* lay out an ad *and* write copy. Instead of forcing each task into one category, we **decide what skills to measure, score every task on the same rubric, and tag each task with what it exercises.** A messy composite task still gives clean, comparable signal.

### 1.2 Four axes over a brand grounding
- **Grounding — 8 companies (data-derived).** We classified our 66 real tasks by true industry and made one fictional brand per well-populated vertical, each with a frozen brand kit (logo, palette, fonts, voice, asset pool). Every task uses only its company's assets, so a generic default loses.
  - V1 Hearthstone (Real Estate) · V2 NIGHTSHIFT (Content/Media/Music) · V3 Maison Rouge (Food) · V4 Apex Goods (Retail/Industrial) · V5 VOLT (Apparel/Sports) · V6 Aurelle (Jewelry/Luxury) · V7 Northwind (Corporate/Tech) · V8 LUMA (Beauty/Wellness).
- **Axis A — 8 Creative Operations** (discovered by clustering real tasks by their tool fingerprints, not asserted), in 4 super-families:
  - *Photo & Image:* O1 tonal grade & restore · O2 masked recolor & isolation · O4 preset retouch & look-dev · O6 stylized & duotone · O8 stock-sourced hero
  - *Vector & Print:* O7 vector & screen-print
  - *Layout & Data:* O5 data-merge & layout
  - *Motion & Audio:* O3 video & audio
- **Axis B — Capabilities (the scoring rubric).** What we score on *every* task: K1 instruction adherence · K2 asset utilization & fidelity · K3 compositional craft · K4 creative quality · K5 communication effectiveness · K6 agentic competence · **K7 honesty/calibration** (new).
- **Axis C — Horizon tiers (the agentic axis).** H1 atomic (≤3 tool calls) · H2 standard (4–8) · H3 composite (9–15) · H4 long-horizon (16+). The headline analysis is **how performance degrades as the horizon grows.**
- **Tags (per task):** tool-coverage + modality (image/vector/data/pdf/video/audio).

### 1.3 The matrix — companies × operations × number of doable tasks
The 8 companies (rows) × 8 operations (columns), populated with the 66 tasks; each cell is the number of tasks living in that space. It is **sparse by design** — each brand uses only the operations realistic for it (NIGHTSHIFT is video-heavy O3; VOLT is vector/print O6–O7; Maison Rouge is photo O1). The column totals equal the data-derived operation-cluster sizes, so the matrix is internally consistent with the clustering.

| Company (vertical) | O1 | O2 | O3 | O4 | O5 | O6 | O7 | O8 | n |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| V1 Hearthstone · Real Estate & Home | 2 | 2 | 1 | 3 | 1 | 1 | · | · | 10 |
| V2 NIGHTSHIFT · Content, Media & Music | · | · | 8 | · | 1 | · | · | 1 | 10 |
| V3 Maison Rouge · Food & Restaurant | 4 | 1 | 1 | 1 | 2 | · | · | · | 9 |
| V4 Apex Goods · Retail, E-comm & Industrial | 1 | 2 | · | 1 | 2 | · | 1 | 2 | 9 |
| V5 VOLT · Apparel, Streetwear & Sports | · | 1 | · | · | · | 3 | 3 | 1 | 8 |
| V6 Aurelle · Jewelry & Luxury | 2 | 2 | · | 1 | 1 | · | · | 1 | 7 |
| V7 Northwind · Corporate, Tech & Finance | 1 | 3 | · | 3 | · | 2 | 1 | · | 10 |
| V8 LUMA · Beauty, Skincare & Wellness | 1 | · | · | · | 1 | · | 1 | · | 3 |
| Total | 11 | 11 | 10 | 9 | 8 | 6 | 6 | 5 | 66 |

*Operation codes: O1 tonal grade & restore · O2 masked recolor & isolation · O3 video & audio · O4 preset retouch & look-dev · O5 data-merge & layout · O6 stylized & duotone · O7 vector & screen-print · O8 stock-sourced hero. Dataset stats: 66 tasks · avg ~20 connector calls (14–30) · 48/50 connectors exercised · output→input chaining ≥80% of steps.*

---

## 2. The rubrics (how we score) — the "creative gym"

### 2.1 The reframe that makes us unique
The other benchmarks (Contra's Human Creativity Benchmark; Lica's GDB) treat the rubric as a *grading sheet you fill in after the fact*, and both only grade the **final picture**. We treat the benchmark as a **gym** — a place where a creative agent trains and earns a reward — and **the rubric is that reward function.** This forces every check to be measurable, lets most of it run automatically (so it scales), and makes the output usable as training data.

### 2.2 The six "drills" — 5 computer-based + 1 human-based

| # | Drill | What it checks | Who |
|---|---|---|---|
| 1 | **Brief contract** | the hard must-haves: exact size, the brand's real colors, the *real* logo file (not regenerated), required text, file types/DPI | computer |
| 2 | **Round-trip recovery** | show the output to a fresh judge with no brief — can it recover what the design is *for*? If yes, it communicated | computer |
| 3 | **Honesty probe** | on deliberately impossible asks: did the agent refuse / escalate / disclose, or **fake a result**? | computer |
| 4 | **Self-calibration** | the agent predicts whether its own work will be accepted; we check if it was right | computer |
| 5 | **Creative range** | run the brief a few times — distinct good ideas, or one safe default? | computer |
| 6 | **The studio bar (craft)** | the one thing only a designer's eye can judge — is the craft clean and good enough to ship? | human |

Five of six run automatically (cheap, scale, run every time); a human is needed only for craft.

### 2.3 The human-based feedback — what the designers actually score on
The reframe for the human part: **the annotator does not rate beauty with stars — they act as the art director / client deciding whether to ship the work.** Four instruments:

1. **The call:** accept / send-back / scrap. One forced professional decision (replaces the mushy "is it a 7 or 8").
2. **The punch-list:** the actual revision notes a designer would send, each tagged blocker / fix / nitpick (red / amber / green severity). Length × severity = **how far from done it is** (a real cost-to-ship number).
3. **Pin-the-flaw:** click the exact spot and pick from a short defect library (off-brand color, illegible text, bad cutout/halo, misaligned, generic/cliché, low-res). A precise, localized label.
4. **The blind face-off:** two outputs side by side — "which would you actually send to the client?" — stacked into a ranking.

Reliability + efficiency tricks (better than plain Likert): designers agree far more on "what's wrong" than "how pretty" (so fewer raters per item); every call needs a one-line reason; hidden "gold" items measure each rater's reliability; genuine taste-splits are flagged and routed to a senior tie-breaker instead of averaged away.

### 2.4 How the new rubrics fit into the taxonomy (kitty.md)
The drills are simply the **measurement instruments for the taxonomy's capabilities (K1–K7)** — they slot directly into Axis B:

| Capability (Axis B) | Measured by | Locus |
|---|---|---|
| K1 instruction adherence | brief contract (auto) | output |
| K2 asset utilization & fidelity | brief contract — logo provenance, asset use (auto) | input→output |
| K3 compositional craft | the studio bar (human) | output |
| K4 creative quality | creative range (auto) + studio bar (human) | output |
| K5 communication effectiveness | round-trip recovery (auto) | output |
| K6 agentic competence | trajectory metrics + self-calibration (auto) | process |
| **K7 honesty/calibration** | honesty probe + self-calibration (auto) | process |

Everything rolls up to two headline numbers that stay common across all 66 tasks (so results compare): a **commission pass rate** ("would a client accept and pay?") and a **craft ELO** (the blind face-offs). The per-task must-haves are auto-generated from each brief, so adding a task is cheap.

---

## 3. The three data tracks (how we manufacture sellable data)

All agent execution runs through the **Claude Adobe connectors** (plus local composition where the connector can't compose headlessly) — *not* the direct APIs. Two producers feed the tracks: a **human creator** (who does the task on our assets, logged step-by-step into a **golden trajectory** + output) and the **agent** (which runs the task in batches).

### Track A — Human vs Agent (who did it better)
**Definition:** give the creators the task + the assets and ask them to do it. The agent does the **same** task. Compare both outputs — who did it better.
**Produces:** a head-to-head (human output vs agent output) + an expert preference + reason.
**Why it's valuable:** the human output is an **SFT target** ("the ideal answer"), and the comparison is **preference data** (for reward models / DPO). It also gives the **credible human baseline** — the "AI vs human freelancer" headline that makes the whole dataset trustworthy and gives you a marketing story.

### Track B — Batch runs vs the Golden Trajectory
**Definition:** run the same task with the agent in **batches of 3**. Separately, capture the **golden trajectory** — the step-by-step way the creator did it. Compare all 3 agent runs against the golden trajectory.
**Produces:** the **golden trajectory** (the rarest, highest-value asset) + 3 agent trajectories scored for how close their *process* comes to the expert's.
**Why it's valuable:** the golden trajectory is **premium SFT / demonstration data** — expert *process* on real creative tools barely exists anywhere. The 3-vs-golden comparison yields **process-reward signal** (which steps/decisions matched the expert) — exactly what agentic-RL teams need. This is the most differentiated track.

### Track C — Best-of-Batch vs the Human task
**Definition:** run **batches of 3**, pick the **best output** of the three (using a judge), then compare that best one against the human-done task.
**Produces:** a judge-selected best-of-3 + its comparison to the human result.
**Why it's valuable:** it's the **efficient quality engine** — you only spend expert attention on the best candidate, not all three. The selection gives **reward-model data** (what "best" looks like); the best-vs-human comparison is the **"is the top AI attempt at human level?"** headline; and the 2 rejected runs become **DPO negatives** for near-free. The best run is also a **rejection-sampling SFT positive**.

### What I think of the three (honest assessment)
- They are not competing options — they are **one pipeline** that outputs **complementary** data. Run all three on the same tasks and you get SFT targets (A + B), process data (B), and preference/reward data (A + C) from one effort.
- **Track B is the crown jewel** (rarest data: expert process). **Track C is the scale engine** (cheap, high-volume preference/reward). **Track A is the credibility anchor** (the human baseline everyone will ask for).
- **Watch-outs:** human creators + logged golden trajectories are the expensive part — reserve them for a **gold core** of ~20–30 tasks and let the agent batches scale the rest. Capturing the golden trajectory *with a one-line rationale per step* matters enormously — bare clicks are worth far less than "clicks + why."

---

## 4. A worked example — one task through all three tracks

**Task (real, AO-14 from our set): SmashBurger retro one-page menu.** The client hands over an InDesign menu template, 4 dull/tilted phone photos of food, a flat PNG wordmark, and a CSV of placeholder prices. The job (25 tool calls, 16 distinct tools): grade the 4 photos to look appetizing, cut the hero burger onto transparency, vectorize the wordmark to SVG, license a chalkboard texture from Adobe Stock, run the template's data-merge, and export a print-ready PDF + hi-res JPEG.

- **Track A:** a freelance designer does the menu; the agent does the menu. Experts blind-compare → "the human's photo grade is warmer and more appetizing; the agent's layout alignment is tighter." → human output banked as SFT target; the pairwise pick + reasons banked as preference data.
- **Track B:** the creator's **golden trajectory** is logged — *straighten → auto-tone → warm white balance → vibrance → food preset → background blur → cut hero → vectorize wordmark → license texture → data-merge → export* — each step with a one-line rationale. The agent runs the menu 3 times. We compare each run's process to the golden one: run 1 matched 9/11 steps but skipped the background blur; run 2 reordered the grade badly; run 3 matched 10/11. → golden trajectory = premium demonstration data; the 3 comparisons = process-reward data.
- **Track C:** of the 3 runs, a judge picks run 3 as best (cleanest cutout, correct DPI). We compare run 3 against the human menu: "near-parity on the photos; the human's typography hierarchy is still better." → best-vs-human = the human-parity headline; runs 1 & 2 = DPO negatives; run 3 = a rejection-sampling SFT positive.

One task, run through three tracks, has now produced: an SFT target, a golden demonstration trajectory, 3 process-comparisons, a best-of-3 reward signal, a DPO pair set, and a human-parity datapoint — all licensing-clean.

---

## 5. The sellable outputs (what comes out of the whole thing)

| Raw material | Becomes | Used for |
|---|---|---|
| Golden trajectory (steps + rationale) | expert tool-use demonstrations | SFT / imitation of long-horizon agents |
| Human final output | ideal input→output targets | SFT |
| Best agent run of batch | rejection-sampling positives | SFT at scale |
| Human fixes the agent's output (repair) | bad→good edit pairs | editing/refinement models |
| Human-vs-agent + expert pick (Track A) | preference pairs | reward models / RLHF |
| Best-vs-worst of batch + defect-pins | DPO pairs with "why" | DPO / critique models |
| 3 runs vs golden trajectory (Track B) | process preferences | process reward models (PRM) |
| Expert rubric scores | reward signal | reward-model / LLM-judge training |
| Tasks + connector harness + runnable reward | a creative-agent **gym** | agentic RL / verifiable rewards |
| Honesty slice (infeasible asks) | refuse/escalate vs fabricate labels | alignment / safety |
| Punch-lists + pinned defects | localized critique labels | critique / defect-detector models |
| Rubric + held-out tasks + human baseline | eval suite + "AI vs human" report | benchmarking / model cards |

**Value multipliers (why it prices above scraped data):** licensing-clean provenance (assets AI-generated on our own briefs + commercially-safe Firefly) · expert *process + rationale* (rare) · a *runnable* reward (an environment, not a static file) · a credible human baseline · long-horizon, multi-format coverage.

---

## 6. Where and how we sell it

### 6.1 Where (buyers)
1. **Frontier / foundation-model labs** — creative + long-horizon tool use is a known model weak spot; biggest checks.
2. **Creative-software companies shipping AI agents** (Adobe, Canva, Figma, Microsoft, Picsart, Recraft, Photoroom) — train + benchmark their own design agents.
3. **Agent-environment & eval startups** — license verifiable gyms.
4. **AI data / labeling vendors** (Scale, Surge, Mercor, Turing, Snorkel, Toloka, Defined.ai) — sell as a premium sub-supplier / co-sell.
5. **Enterprise in-house AI teams** (brands, agencies, marketing orgs) · **vertical creative-AI startups** · **reward-model / verifier companies.**

### 6.2 How (channels & pricing model)
- **Direct licensing / enterprise deals** with labs and tool companies — biggest revenue, with a first-look / exclusivity premium.
- **Data marketplaces** for discovery — AWS Data Exchange, Hugging Face (paid), Snorkel, Defined.ai, Kaggle.
- **Sub-supplier** to labeling vendors (they bundle and resell).
- **Subscription "living dataset"** — recurring refreshes so it stays uncontaminated; labs pay extra for eval data that hasn't leaked into training.
- **Hosted environment / metered API access** — sell the gym *as a service*, not a one-time file.

**Highest-value:** direct licensing to frontier labs + creative-tool companies, sold as a **recurring/hosted product** (environment + refresh), not a one-off file.

### 6.3 How we make the whole benchmark output sellable (the moves that matter)
1. **Ship the reward as code (RLVR).** Make the brief-contract checks runnable so buyers can use them as an automatic RL reward — this turns a dataset into an *environment*, which is the hottest, highest-priced category.
2. **Capture rationale, not just clicks** in every golden trajectory — multiplies SFT value.
3. **Harvest DPO pairs for free** from the best-of-3 (chosen/rejected + the "why" from the defect-pins).
4. **Add repair pairs** (creator fixes the agent's output → bad→good).
5. **Keep it a living dataset** — regenerate tasks from a template engine so the eval split can't leak; sell the refresh as a subscription.
6. **Lead with the human baseline** (Track A) — "how close is AI to a human freelancer" is the headline that opens doors and is itself a sellable report.
7. **Stay licensing-clean** — never scrape; our own briefs + AI-generated assets + commercially-safe generation = data labs can actually train on.

---

## 7. The pipeline in one line, and next steps

**One brief + one brand kit → a human creator (golden trajectory + output) and an agent (3 batch runs) → three comparisons (human-vs-agent, runs-vs-golden, best-vs-human) → expert judging (accept/send-back/scrap + punch-list + pin-the-flaw) → a stack of licensing-clean datasets + a runnable reward → sold to labs and creative-tool companies as files, a subscription, or a hosted gym.**

**Next steps to stand it up:** (1) extend the trajectory logger to capture per-step tool I/O + rationale for both human and agent; (2) pick the ~20–30 gold-core tasks; (3) define the human step-capture method; (4) build the batch-runner over the Claude Adobe connectors; (5) make the rubric runnable; (6) extend the existing review-site UI with accept/send-back/scrap + punch-list + pin-the-flaw. Prove it end-to-end on one task (e.g. the SmashBurger menu) so a single task demonstrates every sellable dataset before scaling.

---

*Companion files: the formal taxonomy spec (`StudioBench_Spec.docx`), the full project context (`PROJECT_FULL_CONTEXT.md`), and the data-pipeline plan (`~/.claude/plans/ok-so-i-have-peppy-emerson.md`).*
