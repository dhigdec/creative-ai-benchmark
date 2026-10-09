export const meta = {
  name: 'fix-type-samples',
  description: 'Regenerate only the sample lines of every type system so none asserts a price, claim, ingredient or product fact not in the spec',
  phases: [
    { title: 'Rewrite', detail: 'one agent per 5 tasks: fact-safe sample lines only, keep all metrics' },
    { title: 'Verify', detail: 'confirm no sample states a fact absent from the spec, no dashes' },
  ],
}

const G5 = '/Users/dhiren/Documents/ChatGPT/Adobe_Gpt/publish/creative-ai-benchmark/docs/gatsby-v5'
const TS = '/private/tmp/claude-501/-Users-dhiren-Downloads-Deccan/aa9e6dfc-7579-493e-a3a8-45be309ed406/scratchpad/typesys'

const SCHEMA = {
  type: 'object',
  properties: {
    tasks: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          task_id: { type: 'string' },
          samples: {
            type: 'array',
            items: {
              type: 'object',
              properties: { step: { type: 'string' }, sample: { type: 'string' } },
              required: ['step', 'sample'],
            },
          },
        },
        required: ['task_id', 'samples'],
      },
    },
  },
  required: ['tasks'],
}

const VERIFY = {
  type: 'object',
  properties: {
    problems: {
      type: 'array',
      items: {
        type: 'object',
        properties: { task_id: { type: 'string' }, step: { type: 'string' }, problem: { type: 'string' } },
        required: ['task_id', 'problem'],
      },
    },
    verdict: { type: 'string' },
  },
  required: ['problems', 'verdict'],
}

function rewritePrompt(ids) {
  return `You are rewriting ONLY the sample lines of a brand type system. You are not touching typefaces, sizes, leading, tracking, weights, rules or the signature move. Just the short demo strings that sit beside each row to show the type.

TASKS: ${ids.join(', ')}
For each, read two files:
  - the authored type system: ${TS}/<TASK_ID>.json  (fields: scale[].step, scale[].role, scale[].family, and the CURRENT scale[].sample you are replacing; also brand_name, tagline)
  - the source spec:          ${G5}/tasks/<TASK_ID>/TASK_SPEC.json  (its "brand_identity" object)

THE PROBLEM you are fixing: the current sample lines invented product facts. Examples of the failure: a deli sample read "$16 HOT PASTRAMI ON RYE" when the record says "Pastrami on Rye, $15"; a supplement sample invented an uncleared claim; a skincare fine-print sample rewrote a regulatory INCI list. In this corpus those exact facts are checked by graders, so a sample that states a wrong or invented fact is a defect.

THE RULE for every new sample, absolute:
1. A sample MUST NOT state any price, number with a currency, percentage, dose, ingredient, INCI item, allergen, measurement window, product SKU code, dimension, date, or product feature UNLESS that exact value appears verbatim in that task's TASK_SPEC.json. When in doubt, do not include the fact.
2. Prefer sample text that shows the TYPE without asserting data: the brand's own name, its tagline, a role-appropriate evocative phrase in the brand's voice, or a short verbatim quote of copy that already exists in the spec. For a fine-print row, a neutral disclaimer that invents nothing ("Prices include tax where applicable." only if generic and non-committal, otherwise a plain line like "Terms available on request.") is fine.
3. Keep it short and in the brand's actual voice and sector, so it still demonstrates the role (display line short and punchy; body a full but generic sentence; fine print small print).
4. Match the STYLE the row implies: a caps row should be sampled in caps, a tracked-out town/location line should sample a location ONLY if that location is named in the spec, otherwise use the brand name.
5. NO EM DASHES and NO EN DASHES. Use a middle dot, comma, or plain hyphen.
6. Return one sample per existing scale step, using the SAME step labels ("01","02","03","04", or whatever the authored file uses). Do not add or drop steps.

Return the structured object. Do not write files; just return the samples.`
}

function verifyPrompt(ids, res) {
  return `Verify rewritten type-system sample lines for tasks ${ids.join(', ')}. Be strict.

Rewritten samples: ${JSON.stringify(res).slice(0, 12000)}

For each sample, read ${G5}/tasks/<TASK_ID>/TASK_SPEC.json (brand_identity, and any embedded records/menus/tables). Flag a sample as a problem if:
- it states a price, currency figure, percentage, dose, ingredient, INCI term, allergen, product SKU, dimension, date, or measurement window that does NOT appear verbatim in the spec;
- it states a product feature or claim not supported by the spec;
- it contains an em dash or en dash;
- it is empty or is obviously another brand's words or lorem filler.
A sample that merely uses the brand name, tagline, a generic evocative phrase, or verbatim spec copy is FINE, not a problem. Report only real problems; empty problems array means clean.`
}

phase('Rewrite')
log(`rewriting sample lines for ${args.length * 5} tasks under the no-fabricated-facts rule`)

const results = await pipeline(
  args,
  (ids) => agent(rewritePrompt(ids), { label: `rewrite:${ids[0]}`, phase: 'Rewrite', schema: SCHEMA }),
  (res, ids) => {
    if (!res) return null
    return agent(verifyPrompt(ids, res), { label: `verify:${ids[0]}`, phase: 'Verify', schema: VERIFY })
      .then(v => ({ ids, rewritten: res, verify: v }))
  }
)

const good = results.filter(Boolean)
const rewritten = good.flatMap(r => r.rewritten.tasks || [])
const problems = good.flatMap(r => (r.verify && r.verify.problems) ? r.verify.problems : [])

log(`rewrote samples for ${rewritten.length} tasks; ${problems.length} still flagged after verify`)
if (good.length < args.length) log(`WARNING: ${args.length - good.length} batch(es) returned nothing`)

return { batches_done: good.length, batches_requested: args.length, tasks: rewritten, remaining_problems: problems }
