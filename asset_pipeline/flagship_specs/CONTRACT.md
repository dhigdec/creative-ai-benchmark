# Flagship TaskSpec Authoring Contract (round 3)

You are writing ONE python module `spec_<TASKID>.py` in this directory. It defines the
input-asset generation spec for one freelance design task. The module is consumed by the
existing pipeline (`generate.py`); study `../specs.py` for live exemplars (SPEC_5604,
SPEC_502, SPEC_430 are the best references). Your module must be SELF-CONTAINED:

- Do NOT import `specs`, `config`, `util`, or any pipeline module (circular import / path risk).
- Define locally:
  ```python
  NO_TEXT = ("ABSOLUTELY NO text, letters, numbers, watermarks, logos or symbols "
             "anywhere in the image.")
  NO_TM = ("No real-world brands, trademarks, celebrity or athlete likenesses, "
           "or recognizable team logos.")
  ```
- Export exactly: `SPEC` (dict), `BRIEF_MD` (str), and a `__main__` self-test (below).
- Plain python 3.9. No type annotations needed. Stdlib only at module import time.

## SPEC schema (exact)

```python
SPEC = {
  "task_id": <int>, "slug": "<kebab-slug>",
  "persona": {"mode": "invent"|"from_brief", "directives": """<see below>"""},
  "assets": [ <asset dicts in DEPENDENCY ORDER — deps before dependents> ],
  "decisions": [ {"requirement": "<verbatim inputs[] string>", "assumed_value": "...", "why": "..."} ],
}
```

Asset dict fields:
- `key`: snake_case unique.
- `input_requirement`: MUST be a VERBATIM string from the dataset record's `inputs[]` list
  (coverage invariant: every `inputs[]` string must equal the `input_requirement` of ≥1 asset
  OR the `requirement` of ≥1 decision — character-for-character identical, copy-paste them).
  Multiple assets may claim the same string.
- `kind`: `"data"` (JSON via writer LLM) | `"text"` (markdown via writer) | `"image"` | `"program"`
  (deterministic python, no model — see below).
- data/text: `generator: "writer"`, `filename` (e.g. `foo.json` / `foo.md`),
  optional `also_render: "foo.md"|"foo.csv"` (auto-rendered readable copy),
  `prompt` (str.format template), `qc: {"checks": [...]}`.
- image: `generator_role` ∈ `image_hero_text` (Nano Banana Pro — ALL text-bearing designs:
  logos, signs, drafts with wording) | `image_photoreal2` (gpt-image-2 high — ALL photographs,
  especially humans) | `image_cheap2` (gemini-3.1-flash — secondary/simple images, textures,
  deliberately-mediocre drafts, icons), `count` (int), `size` (ONLY `1024x1024`, `1024x1536`,
  `1536x1024` — one size per asset; split into two assets if you need two aspect ratios),
  `format: "png"|"jpg"`, `filename` (use `{i:02d}` when count>1) or `filename_fn(ctx)`,
  `prompt` or `prompt_fn(ctx)`, optional `depends_on: ["data_key", ...]`,
  optional `post_process: [{"op": "soften"}]` (downscale+jpeg roundtrip → low-res AI-draft feel;
  keeps clean copy in originals/), `qc: {"vision": True, "min_score": <6|7>, "criteria": "..."}`.
- program: `program_fn(ctx, paths)` — writes the files deterministically, returns a params dict
  for the manifest; plus `count`, `filename`/`filename_fn`, `program_desc` (short str),
  optional `depends_on`. May `import qrcode` INSIDE the fn (installed in the venv).

## Template rendering rules (bug class #1 — get these right)

- `prompt` strings are rendered with `str.format(**flat_fields, i=<1-based>)`.
  Available placeholders: `{brand_name} {tagline} {industry} {voice} {palette_hexes}
  {palette_hex_list} {fonts_heading} {fonts_body} {logo_style_brief} {photo_style_tokens}
  {no_text} {no_tm} {i}`.
- ANY literal `{` or `}` in a prompt (e.g. JSON shape examples) MUST be doubled `{{ }}`.
  This applies to `prompt`, and to `qc.criteria` (also formatted). Strings returned by
  `prompt_fn` are NOT formatted (use them for content derived from sibling assets).
- `prompt_fn(ctx)` / `filename_fn(ctx)` receive ctx with `.flat` (the fields above),
  `.assets` (dict of loaded data-asset JSON objects you declared in `depends_on`),
  `.persona`, `.record`, `.scratch` (cache dict — see `_5604_listing_prompts` pattern).
  They MUST return exactly `count` items. Deps must be generated EARLIER in the assets list.
- `qc.checks` syntax (data assets): `"json_valid"`, `"field==N"` / `"field>=N"`
  (len of top-level list `obj[field]`), `"field[].sub"` (every item in `obj[field]` must
  have non-empty `sub`). Design your JSON shapes so the critical invariants are checkable
  at top level (lists of objects). These checks are the deterministic backbone the package
  judge trusts — include them for every data asset.

## Persona directives

`mode: "from_brief"` extracts real facts (business name, product domain) into
`facts_from_brief` and invents only what's missing; `mode: "invent"` invents everything.
Directives must pin: palette (with concrete hexes when the brief mandates colors), voice,
`logo_style_brief`, `photo_style_tokens` (a comma phrase injected into every photo prompt
for cross-asset visual consistency). Fonts come from a safe list automatically.

## PHOTOREALISM DOCTRINE (the user's #1 priority — bake into every photo prompt AND its QC criteria)

Every `image_photoreal2` prompt must read like a brief to a documentary photographer, and
must include this language (adapted to the scene):
- Camera: "candid documentary photograph, shot on a 35mm lens at f/2.0, available natural
  light, subtle film grain, realistic depth of field" (vary sensibly: 50mm/85mm for portraits).
- Skin/hair (when people appear): "natural skin texture with visible pores, no beauty
  retouching, individual hair strands with natural flyaways — hair must NOT look painted,
  helmet-like or plastic", "anatomically correct hands".
- Anti-AI-look: "imperfect, lived-in detail; believable fabric wrinkles; asymmetric
  composition; NOT a staged stock photo, NOT CGI-glossy, NOT over-saturated".
- Always end people/photo prompts with {no_text} and (where brands could sneak in) {no_tm}.
- QC criteria for photos must explicitly test: "natural hair with individual strands and
  flyaways (not painted/plastic), realistic skin texture (not airbrushed), correct hands,
  genuine candid emotion (not stock-posed), looks like a real photograph, no text/watermarks".
  min_score 7 for hero/people photos.

For text-bearing designs (logos, signs): quote the EXACT wording in double quotes, demand
"reading EXACTLY \"...\"", list colors with hexes, "flat ... no gradients, no other text",
white background (cutouts are the Adobe connector's job later — inputs stay on white unless
the plan says otherwise). QC criteria must demand flawless spelling of the quoted text.

For deliberately-mediocre AI drafts (assets that simulate the client's existing bad drafts):
generator_role `image_cheap2`, `post_process: [{"op": "soften"}]`, min_score 5-6, criteria
accepts "minor text garbling acceptable — it is a draft being replaced, not a final".

## Decisions

Every `inputs[]` string that is an OUTPUT spec (deliverable sizes/formats), a commercial term
(budget, revisions, deadlines), or something resolved by assumption goes into `decisions` with
honest `assumed_value` + `why` (see SPEC_5604 decisions for tone). Output-spec strings are
"recorded for the Adobe agent", not generated.

## BRIEF_MD — the rewritten client work-order

A markdown string: the task rewritten as the rich, specific work order the client would hand
a freelancer. Structure: `# <Title>` / client context paragraph (who the client is, why now) /
`## Deliverables` (numbered, EVERY exact dimension/format from the original brief preserved) /
`## Content` (what goes on each piece — reference the actual generated asset filenames) /
`## Style direction` (palette hexes, typography mood, references) / `## Acceptance criteria`
(checkable list). 350-650 words. No job-posting language (no "we are seeking", no portfolio
asks). Use the persona's facts where the brief names a real business; keep every constraint
from the original brief (sizes, bleeds, codes, counts, prohibitions).

## Self-test (mandatory, must pass before you finish)

End the module with EXACTLY this pattern, adapted with stub data matching your depends_on
shapes (every data asset a prompt_fn/filename_fn reads must have a plausible stub):

```python
if __name__ == "__main__":
    class _Stub: pass
    ctx = _Stub()
    ctx.flat = {k: "Stub-X" for k in (
        "brand_name", "tagline", "industry", "voice", "palette_hexes", "palette_hex_list",
        "fonts_heading", "fonts_body", "logo_style_brief", "photo_style_tokens",
        "no_text", "no_tm")}
    ctx.persona, ctx.scratch = {}, {}
    ctx.assets = { ... stubs for every depends_on data asset ... }
    for a in SPEC["assets"]:
        n = a.get("count", 1)
        if a["kind"] == "program":
            names = a["filename_fn"](ctx) if a.get("filename_fn") else (
                [a["filename"]] if n == 1 else [a["filename"].format(i=i + 1) for i in range(n)])
            assert len(names) == n, a["key"]
            continue
        ps = a["prompt_fn"](ctx) if a.get("prompt_fn") else \
            [a["prompt"].format(**dict(ctx.flat, i=i + 1)) for i in range(n)]
        assert len(ps) == n, a["key"]
        names = a["filename_fn"](ctx) if a.get("filename_fn") else (
            [a["filename"]] if n == 1 else [a["filename"].format(i=i + 1) for i in range(n)])
        assert len(names) == n == len(set(names)), a["key"]
        crit = (a.get("qc") or {}).get("criteria")
        if crit:
            crit.format(**dict(ctx.flat, i=1))
    for d in SPEC["decisions"]:
        assert d.get("requirement") and d.get("assumed_value") and d.get("why")
    print("SELF-TEST OK", SPEC["task_id"])
```

Run it: `/usr/bin/python3 spec_<TASKID>.py` (from this directory) — it must print SELF-TEST OK.
Also verify coverage yourself: every string in the record's `inputs[]` appears verbatim as an
`input_requirement` or decision `requirement`.

## Hard rules

1. Generation uses ONLY gemini/openai roles listed above — never Claude (Claude judges only).
2. No real-world trademarks in IMAGERY beyond names the brief itself supplies (names from the
   brief are simulated with invented stand-in designs — like the existing 2335/502 specs).
3. Realistic content: realistic prices/INCI/names per locale, correct language (task plan says
   if non-English), plausible URLs on the persona's invented domain.
4. People in photos: invented, diverse, dignified; emotional truth without exploitation.
5. Keep total image counts EXACTLY as the per-task plan dictates (cost-gated).
6. Filenames: lowercase, hyphens/underscores, descriptive, correct extension for format.
