# Round-5 Mega-Spec Authoring Contract (definitive long-horizon tasks)

You write ONE self-contained module `spec_<ID>.py` in this dir. It generates the CLIENT-supplied
INPUT ASSETS for one long-horizon Adobe task. Study `../flagship_specs/CONTRACT.md` (the base
contract — schema, str.format rules, qc.checks syntax, self-test) and `../specs.py` exemplars
(SPEC_5604/SPEC_502/SPEC_430). This contract ADDS: a self-contained RECORD, video/audio asset
kinds, and template-as-decision handling. The full task definition (workflow, input_assets,
templates_to_author) is in `../../complex_benchmark/definitive_10_tasks.json` — find your task by
its title; your input_assets list there is authoritative for WHAT to generate.

Connector feasibility (what the downstream Adobe agent will run) is in
`../../complex_benchmark/FEASIBILITY.md` — you only GENERATE inputs, but read it so your assets are
the right shape (e.g. photos with genuinely blown windows for the HDR task, messy/tilted frames for
straighten, blank label areas for product, transparent logos to vectorize).

## Module exports (exact)
`RECORD` (dict), `SPEC` (dict), `BRIEF_MD` (str), and the mandatory `__main__` self-test.
Self-contained: define `NO_TEXT`/`NO_TM` locally; NO pipeline imports.

### RECORD (the dataset row — merged into the pipeline dataset)
```python
RECORD = {
  "id": <int>,                    # your assigned id
  "source": "upwork"|"freelancer"|"composite"|"web",
  "vertical": "<industry>",
  "title": "<task title>",
  "url": "<source url or ''>",
  "date": "2026-06-15",
  "category": "<e.g. Photo Retouching & Enhancement>",
  "task_type": "<short>",
  "family": "<e.g. Photo & Image Editing>",
  "feasibility": "full"|"template"|"partial",
  "mcp_workflow": "<the ordered connector chain as a string — from definitive_10_tasks.json workflow>",
  "inputs": [ <verbatim input-asset requirement strings — see coverage invariant> ],
  "note": "<connector-limit / honest note>",
  "desc": "<the rich client brief — reuse/condense BRIEF_MD prose>",
}
```
COVERAGE INVARIANT: every string in `RECORD["inputs"]` MUST be claimed (character-identical) by some
asset's `input_requirement` OR some decision's `requirement`. You CONTROL both the inputs list and
the asset input_requirements — keep them in lockstep. Put each generatable asset (image/data/video/
audio/program) as an asset; put USER-AUTHORED TEMPLATES (.indd/.ai) and OUTPUT-spec lines as decisions.

## Asset kinds
- data/text/image/program: exactly as in the base contract. Image roles: `image_photoreal2`
  (gpt-image-2 — photoreal people/products, REALISM DOCTRINE mandatory), `image_hero_text`
  (gemini-3-pro-image NBP — text-bearing logos/artwork/moodboards), `image_cheap2`
  (gemini-3.1-flash-image — textures/swatches/secondary/reference plates).
- CSV: a `data` asset with `also_render: "<name>.csv"`; the writer emits JSON that render_csv turns
  into a CSV. For data-merge CSVs, the JSON top-level key holds a LIST OF ROW OBJECTS whose keys are
  the EXACT column/Variable names the user's template will bind (state them in the prompt). Use
  qc.checks like `"rows==510"`, `"rows[].name"`.
- **video** (NEW): `{"key":..., "input_requirement":..., "kind":"video", "generator":"veo"|"sora",
  "count":N, "seconds":8, "aspect":"16:9"|"9:16", "filename"/"filename_fn", "prompt"/"prompt_fn",
  "depends_on":[...], "qc":{"technical":true}}`. Veo 3 fast = 8s 720p with native ambient audio;
  use "sora" for one establishing/cinematic clip if desired. Prompts: documentary realism doctrine,
  concrete scene + camera move; no on-screen text. Keep counts SMALL (cost ~\$1.2/Veo clip).
- **audio** (NEW): `{"key":..., "input_requirement":..., "kind":"audio", "generator":"tts",
  "voice":"alloy"|"onyx"|"nova"|...,"filename","text"|"text_fn", "roughen":true?, "qc":{...}}`.
  `text` is a str.format template OR `text_fn(ctx)` returns a list of narration strings (e.g. read a
  script from a sibling data asset). `roughen:true` adds hiss+reverb so media_enhance_speech has
  something to clean (keeps a clean copy in originals/). A `<name>.txt` transcript is auto-saved.

## Templates → decisions (NOT generated)
For every `templates_to_author` entry in your task, add a `decision` whose `requirement` is the
matching `inputs[]` string, `assumed_value` = "USER-AUTHORED in desktop InDesign/Illustrator (Data
Merge / Variables panel): <exact field names + layout spec>", `why` = one line. We do NOT generate
.indd/.ai; the user authors them. Stock-sourced inputs are also decisions (sourced live at execution
via asset_search+license) UNLESS you choose to generate a stand-in — prefer decision + note.

## REALISM DOCTRINE (the user's #1 requirement — "perfect, no faults")
Every photoreal `image_photoreal2` prompt AND its qc.criteria must demand: natural skin texture with
visible pores (no airbrush), individual hair strands with flyaways (not painted/plastic),
anatomically correct hands, candid documentary framing, believable lived-in detail, NOT CGI-glossy,
NOT over-saturated. For interiors/exteriors needed by the HDR task: genuinely BLOWN-OUT windows +
slightly crooked verticals (so the agent has real work to do). For products: real label embossing,
slightly off-level, the blank/clean areas the workflow needs. For logos/artwork (NBP): quote exact
wording, demand flawless spelling, flat/transparent where needed for vectorize.

## QC + judge
Every image asset: `qc:{vision:true, min_score:7 (6 for secondary/reference), criteria:"..."}`.
Every data asset: `qc:{checks:[...]}` with the real invariants. Video/audio: technical QC is
automatic (valid file + ffprobe). The package judge runs after generation — design so it passes
(complete, coherent, executable, realistic).

## BRIEF_MD
The rich client work-order (350-700 words): who the client is, the deliverables (exact sizes/specs
from the task), the input assets you're handing over (reference the filenames), style direction,
acceptance criteria. No job-ad language.

## Self-test (mandatory) — adapt the base-contract __main__ pattern, and ALSO assert:
- every RECORD["inputs"] string is claimed by an asset input_requirement or decision requirement;
- video/audio assets render filenames == count and prompts/texts == count.
Run `/usr/bin/python3 spec_<ID>.py` — must print `SELF-TEST OK <ID>`.
