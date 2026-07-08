# Creative-Agent Benchmark — Proposed Taxonomy
*A plain-English proposal of what we want to measure and how we're organizing it.*

---

## 1. What we're trying to find out
**Can an AI agent do real creative work — like a freelance designer — well enough that a real client would be happy with the result?**

We test this by giving the AI a real-style brief plus the brand's assets, letting it do the work using design tools (Adobe / Canva), and then judging the output. The headline comparison is **Claude vs OpenAI** — which model is the better creative agent.

---

## 2. The core idea (and the problem it solves)
A fair concern was raised: **our tasks mix many things at once.** One task might retouch a photo *and* lay out an ad *and* write the caption — so you can't neatly sort tasks into clean categories.

**Our fix: don't build the categories *out of* the tasks. Decide what we want to measure first, and then simply *label* each task with what it touches.**

> Think of grading students. A single essay can test grammar, logic, *and* creativity all at once. You don't invent a new category for every essay — you grade every essay against the *same set of skills*. We do the same: define the skills (what we measure), then tag each task with the skills it uses.

This means a messy, realistic task is fine — we just tag it with everything it exercises, and we can still measure each skill cleanly.

---

## 3. How the benchmark is organized — 4 layers
Each layer does a different job.

### Layer 1 — 10 companies (the grounding)
We create **10 imaginary companies in 10 different industries**, each with a deliberately *different visual style* so no single "look" wins:

| Company | Industry | Style |
|---|---|---|
| LUMA | clean-beauty skincare | calm, minimal, premium |
| NIGHTSHIFT | tech-house music label | bold, dark, high-energy |
| Hearthstone | boutique real estate | elegant, editorial |
| Cedar & Co | craft coffee roaster | warm, artisanal |
| Northwind | B2B fintech / SaaS | corporate, clean |
| VOLT | streetwear apparel | loud, graphic, youthful |
| Stillwater | wellness / yoga studio | soft, serene |
| Maison Rouge | boutique hotel / restaurant | luxe, moody |
| Sproutly | kids ed-tech | playful, colorful |
| Terra | outdoor / sustainability | rugged, earthy |

Each company comes with its **own brand kit** (logo, colors, fonts, brand voice, product photos) and its **own set of tasks**. Every task uses *only* that company's assets — so the AI must actually use what we give it, not make up something generic.

### Layer 2 — 4 types of creative work (what to make)
- **Create** — make something new (a logo, a brand kit)
- **Edit** — change an existing asset (a Diwali version of the logo, resize an ad)
- **Communicate** — a customer-facing piece (an ad, flyer, Instagram post, brochure)
- **Write** — the words (captions, ad copy)

*(Our main focus is **Communicate** and its combinations, e.g. Edit-then-Communicate — but the other types are still exercised inside those tasks.)*

### Layer 3 — 6 capabilities (what we actually score, on *every* task)
This is the **rubric** — the real "what we want to measure":

| # | Capability | Plain-English question |
|---|---|---|
| 1 | **Instruction-following** | Did it do everything asked, at the right size / format / count? |
| 2 | **Asset fidelity** | Did it use the *given* logo, colors and photos, and stay on-brand? |
| 3 | **Craft** | Is the layout, typography and quality genuinely good and clean? |
| 4 | **Creativity** | Is it original and tasteful — or a boring, safe default? |
| 5 | **Communication** | Does it actually *work* (would this ad sell)? Is the copy good? |
| 6 | **Agentic skill** | Did it use the tools well and handle multi-step work sensibly? *(judged from its steps)* |

### Layer 4 — tags (extra labels on each task)
Each task is also tagged with its **deliverable type** (ad / logo / brochure…), its **complexity** (see below), and the **tools** it uses. These let us slice the results later.

---

## 4. Two kinds of tasks: atomic vs composite
- **Atomic task** — does *one* thing, so it gives a clean read on a single capability.
  *e.g. "Resize this ad to 3 social formats" → mainly tests instruction-following + asset fidelity.*
- **Composite task** — a realistic, end-to-end job that does several things at once.
  *e.g. "Make a festive logo variant, then design the launch ad and write the caption."*

We use **both**: atomic tasks for clean measurement, composite tasks for realism. Because every task is tagged with the capabilities it touches, even a messy composite task tells us *which* capability the model got right or wrong.

---

## 5. How each task is scored
1. Run the **same task** through both **Claude** and **OpenAI**.
2. Show the two results to a **human design expert**, **side-by-side and blind** (they don't know which is which).
3. They pick **which is better** (the headline result), and give the **6 capability sub-scores** to explain *why*.
4. We add it all up into a **win-rate**, plus breakdowns by capability, by company, and by difficulty.

*(We also note when a model refuses a task, and we track how much effort/time each took, so a model can't "win" just by doing more.)*

---

## 6. A few worked examples (to make it concrete)

**Example A — LUMA (skincare), "Communicate" task**
> *Brief:* "Design the launch Instagram ad for our Balancing Botanical Serum using the attached product photo, logo and palette. Headline: 'Balance, in one botanical drop.'"
- **Type:** Communicate · **Complexity:** standard
- **Capabilities tested:** instruction-following, asset fidelity, craft, communication, agentic skill

**Example B — VOLT (streetwear), "Edit" task**
> *Brief:* "Make a Diwali-themed variant of the VOLT logo using the brand's existing logo and colors."
- **Type:** Edit · **Complexity:** atomic
- **Capabilities tested:** instruction-following, asset fidelity, creativity

**Example C — Cedar & Co (coffee), composite task**
> *Brief:* "We're launching a winter blend. Create a small seasonal sub-palette, design an Instagram post and a shelf flyer using the attached bag photo, and write 3 captions in our voice."
- **Type:** Create + Communicate + Write · **Complexity:** composite
- **Capabilities tested:** all six

**Example D — Northwind (fintech), "Write" task**
> *Brief:* "Write 5 LinkedIn ad headlines + body copy for our new payments product, in Northwind's confident, professional voice."
- **Type:** Write · **Complexity:** atomic
- **Capabilities tested:** instruction-following, communication

In every case: same task to both models, blind A/B, same 6-capability rubric, tagged with what it exercises.

---

## 7. Why this approach is good
- **Measurement-first:** we decide what matters, then build tasks to fit — not the other way around.
- **No messy categories:** we tag tasks instead of forcing each one into a single box, so realistic tasks still give clean signal.
- **Comparable + sliceable:** every task scored the same way, so we can say *"Model X is better at craft, Model Y is better at following instructions,"* not just an overall number.
- **Grounded + varied:** 10 distinct brands stop a model winning by one default style and test real brand-consistency.

---

## 8. What we'd love the design / SME team to help shape
1. **Wording of the rubric** for the more subjective capabilities (craft, creativity, communication) — designers will say this better than engineers.
2. **Rating setup** — how many expert raters per task, and whether to keep all 6 sub-scores or just the A/B choice.
3. **The 10 companies + their brand kits** — confirm the industries and approve the brand assets.
4. **How many tasks** per company / per type for a first version (we're thinking ~6 each, ~60 total — enough for a credible first report, not an oversized benchmark).

---

### In one sentence
**10 companies give the grounding, 4 work-types are the task buckets, 6 capabilities are what we score on every task — and we *tag* tasks instead of forcing them into one box, so real-world (messy) tasks still give clean, comparable measurements of Claude vs OpenAI.**
