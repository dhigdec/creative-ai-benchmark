export const meta = {
  name: 'type-system-cards',
  description: 'Rewrite all 100 brand typography specs into an explicit numbered type scale, keeping each brand its own faces',
  phases: [
    { title: 'Author', detail: 'one agent per 5 tasks: build the numbered scale from each brand existing faces' },
    { title: 'Check', detail: 'verify faces unchanged, sizes sane, no dashes, nothing invented' },
  ],
}

const G5 = '/Users/dhiren/Documents/ChatGPT/Adobe_Gpt/publish/creative-ai-benchmark/docs/gatsby-v5'
const OUT = '/private/tmp/claude-501/-Users-dhiren-Downloads-Deccan/aa9e6dfc-7579-493e-a3a8-45be309ed406/scratchpad/typesys'

const SCHEMA = {
  type: 'object',
  properties: {
    tasks: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          task_id: { type: 'string' },
          brand_name: { type: 'string' },
          tagline: { type: 'string' },
          display_face: { type: 'string' },
          text_face: { type: 'string' },
          scale: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                step: { type: 'string' },
                role: { type: 'string' },
                family: { type: 'string' },
                size: { type: 'string' },
                leading: { type: 'string' },
                weight: { type: 'string' },
                tracking: { type: 'string' },
                sample: { type: 'string' },
                note: { type: 'string' },
              },
              required: ['step', 'role', 'family', 'size', 'leading', 'weight', 'tracking', 'sample'],
            },
          },
          signature_move: { type: 'string' },
          rules: { type: 'array', items: { type: 'string' } },
          prose: { type: 'string' },
          faces_kept: { type: 'boolean' },
        },
        required: ['task_id', 'brand_name', 'display_face', 'text_face', 'scale', 'signature_move', 'rules', 'prose', 'faces_kept'],
      },
    },
  },
  required: ['tasks'],
}

const CHECK = {
  type: 'object',
  properties: {
    checked: { type: 'number' },
    problems: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          task_id: { type: 'string' },
          problem: { type: 'string' },
          severity: { type: 'string' },
        },
        required: ['task_id', 'problem', 'severity'],
      },
    },
    verdict: { type: 'string' },
  },
  required: ['checked', 'problems', 'verdict'],
}

function authorPrompt(ids) {
  return `You are restating each brand's typography as an explicit, numbered TYPE SCALE, in the house format below. You are NOT redesigning anything: every typeface a brand already uses stays exactly as it is.

TASKS: ${ids.join(', ')}
For each, read ${G5}/tasks/<TASK_ID>/TASK_SPEC.json and use its "brand_identity" object: brand_name, tagline, typography (prose), display_face, signature_type_move, personality, voice, sector.

THE FORMAT you are producing, per brand:

  // Type system
  <Brand name>
  <tagline>                                  <display face>   <text face>

  01  Display / H1       <family> · <size> / <leading>    <weight> · tracking <value>    "<sample line>"
  02  Subheading / H2    <family> · <size> / <leading>    <weight> · tracking <value>    "<sample line>"
  03  Body               <family> · <size> / <leading>    <weight> · max 65 characters   "<sample line>"
  04  Fine print         <family> · <size> / <leading>    <weight> · tracking <value>    "<sample line>"

ABSOLUTE RULES:
1. KEEP THE BRAND'S OWN FACES. Use only the typeface names already named in that task's existing typography prose and display_face. Never substitute Playfair Display, Inter, or any other face that is not already that brand's. If the brand names two faces, use the display one for steps 01 and 02 and the text one for 03 and 04, unless the existing prose clearly assigns them otherwise. If the brand genuinely uses one family throughout, use it for all four steps and vary weight.
2. KEEP SIZES THAT ALREADY EXIST. The prose already states sizes for most roles. Reuse those numbers. Only invent a size where the prose gives none, and then keep it proportionate to the ones that exist.
3. FILL IN WHAT IS MISSING. Most tasks currently state no line-height and no tracking. Supply both, appropriate to the face and the role: display sizes take tight leading (about 1.05 to 1.15 of size) and slightly negative tracking; body takes open leading (about 1.4 to 1.6) and tracking 0; fine print takes slightly positive tracking. Express size and leading as plain numbers with the unit stated once, e.g. size "44 pt", leading "48 pt", or "28 px" / "34 px" for a screen deliverable.
4. PRESERVE THE SIGNATURE MOVE. Each brand has a signature_type_move, the thing that makes it recognisable without its logo. Carry it through into the scale, and restate it in signature_move. If it is a tracked-out caps line, a specific weight pairing, tabular figures, an italic rule, that behaviour must still be visible in the scale rows.
5. SAMPLE LINES must be real short copy in that brand's own voice, about its own products or services. Not lorem, not the Meridian coffee examples, and never another brand's words.
6. NO EM DASHES AND NO EN DASHES anywhere in any string you write. Use a middle dot, a comma, or a plain hyphen. This is a hard house rule.
7. rules[] carries the brand's prohibitions and constraints already present in the prose, such as "never colour or embolden a price" or "never set the wordmark on one line". Keep every one you find, verbatim in meaning.
8. prose is a single readable paragraph restating the scale, for consumers that cannot render a table. It must agree exactly with the scale rows.
9. Set faces_kept true only if every family you used was already that brand's. If you had to invent a family because the spec named none, set it false and say so in rules.

Write your result for every task to ${OUT}/<TASK_ID>.json as a single object (the per-task object, not the wrapper), and also return all of them in the structured wrapper.`
}

function checkPrompt(ids, res) {
  return `Check the type systems just authored for tasks ${ids.join(', ')}. Be strict and specific.

Authored output: ${JSON.stringify(res).slice(0, 14000)}

For EACH task, read ${G5}/tasks/<TASK_ID>/TASK_SPEC.json and compare against brand_identity:
1. FACE SUBSTITUTION, the critical one: every family named in the scale must already appear in that task's existing typography prose or display_face. If any row introduces a face the brand did not have, especially Playfair Display or Inter, report it as severity "critical".
2. Sizes that existed in the prose must still be present in the scale, not silently changed. Report changed sizes as "major".
3. Every row must have a size, a leading, a weight and a tracking value. A missing one is "major".
4. Any em dash or en dash in any string is "major". Report the exact string.
5. The signature_type_move must still be recognisable in the scale or signature_move. If it was dropped, "major".
6. Sample lines must be that brand's own voice, not coffee-roaster filler and not another brand's words. Generic filler is "minor".
7. prose must agree with the scale rows. Contradiction is "major".

Report only real problems. An empty problems array is the right answer if the work is clean.`
}

phase('Author')
log(`authoring type systems for ${args.length * 5} tasks, keeping every brand its own faces`)

const results = await pipeline(
  args,
  (ids) => agent(authorPrompt(ids), { label: `author:${ids[0]}`, phase: 'Author', schema: SCHEMA }),
  (res, ids) => {
    if (!res) return null
    return agent(checkPrompt(ids, res), { label: `check:${ids[0]}`, phase: 'Check', schema: CHECK })
      .then(chk => ({ ids, authored: res, check: chk }))
  }
)

const good = results.filter(Boolean)
const authored = good.flatMap(r => r.authored.tasks || [])
const problems = good.flatMap(r => (r.check && r.check.problems) ? r.check.problems : [])
const critical = problems.filter(p => p.severity === 'critical')
const major = problems.filter(p => p.severity === 'major')
const facesLost = authored.filter(t => t.faces_kept === false)

log(`authored ${authored.length} type systems; ${critical.length} critical, ${major.length} major problems; ${facesLost.length} tasks could not keep their faces`)
if (good.length < args.length) log(`WARNING: ${args.length - good.length} batch(es) returned nothing`)

return {
  batches_done: good.length,
  batches_requested: args.length,
  tasks_authored: authored.length,
  critical: critical,
  major: major,
  minor_count: problems.length - critical.length - major.length,
  faces_not_kept: facesLost.map(t => t.task_id),
}
