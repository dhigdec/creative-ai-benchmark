# asset_pipeline — AI input-asset generation (5-task pilot)

Simulates the *client* for 5 verified freelance tasks: generates every input asset
(photos, logos, copy, menu data) via **Gemini + OpenAI**, stores them under
`../input_assets/<task_id>_<slug>/`, with a `manifest.json` contract the
Adobe-connector agent reads to execute the task.

## Setup

```bash
cd asset_pipeline
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env && chmod 600 .env     # then paste your keys into .env
.venv/bin/python generate.py --check        # key/model matrix + spec coverage lint
```

`.env` keys: `GEMINI_API_KEY`, `OPENAI_API_KEY` (both recommended; one is enough —
routing collapses to it). Optional `ANTHROPIC_API_KEY` as a third text/QC provider.
**Never commit `.env`.**

## Run

```bash
.venv/bin/python generate.py --task 440 --dry-run   # plan + cost, zero API calls
.venv/bin/python generate.py --task 440             # cheapest end-to-end (~$0.20)
.venv/bin/python generate.py --all-pilot            # all 5 (est ~$6-7)
.venv/bin/python validate.py                        # offline checks incl. coverage invariant
open ../input_assets/index.html                     # visual contact sheets
```

Flags: `--force` (regen), `--asset KEY` (regen one asset), `--images-provider openai|gemini`,
`--skip-vision-qc`, `--yes` (skip cost gate), `--check --deep` (ping writer model).

## The 5 pilot tasks

| id | slug | what gets generated |
|---|---|---|
| 440 | logo-vectorize | 1 flat logo → softened raster + brand_colors.json |
| 5272 | doordash-menu | brand persona, logo, menu.json/md, 7 dish photos |
| 239 | social-media-graphics | logo (transparent), brand_guide.md, 6 photos, post_copy.json |
| 1097 | photo-retouch-batch | 10 pristine photos → originals/, degraded copies → assets/ |
| 5649 | shopify-card-photos | products.json (fictional, handle-named) + 8 messy iPhone-style photos |

## Per-task output contract

```
input_assets/<id>_<slug>/
├── assets/            # what the "client" hands over (the agent's inputs)
├── originals/         # pristine ground truth (1097; pre-soften logo for 440)
├── prompts/           # final rendered prompt per asset (audit trail)
├── persona.json       # the simulated client (brand, palette, voice)
├── manifest.json      # THE CONTRACT: assets ↔ verbatim client inputs, decisions, QC, coverage
├── INTAKE.md          # human-readable handoff
├── contact_sheet.html # visual review (thumbs, prompts, QC scores, before/after pairs)
└── run.log
```

Key invariant: every verbatim string in the dataset task's `inputs[]` is claimed by an
asset or a recorded decision — `validate.py` fails otherwise, and `ready_for_agent`
flips true only when coverage is complete and nothing failed QC.

Safety rails: cost estimate + gate (>$10 asks), `MAX_IMAGES_PER_RUN=60`, vision-QC
regen loop (≤2, judged by the *other* provider), content-policy sanitize-retry,
resume-on-rerun (cached assets skipped), no real trademarks/likenesses in any prompt.
