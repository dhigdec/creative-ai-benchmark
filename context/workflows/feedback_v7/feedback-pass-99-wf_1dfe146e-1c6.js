export const meta = {
  name: 'feedback-pass-99',
  description: 'Apply the 2026-09-25 review feedback to 99 tasks: pin unresolvable brief ambiguities, palette roles and rules, type-rule coverage, verifier consistency, specific asset naming',
  phases: [
    { title: 'Author', detail: 'one agent per task writes a builder, emits a patch, validates it' },
    { title: 'Verify', detail: 'two independent lenses per task: grounding and traps; coverage, naming and form' },
    { title: 'Repair', detail: 'fix every reported problem, re-validate' },
    { title: 'Re-verify', detail: 'fresh adversarial check wherever a critical problem was found' },
  ],
}

const FB = '/private/tmp/claude-501/-Users-dhiren-Downloads-Deccan/e4e5b6fa-8315-4aad-9a2e-58b8b08d9714/scratchpad/feedback'
const GUIDE = `${FB}/GUIDE.md`
const VALIDATE = (id) => `python3 ${FB}/apply_feedback.py --only ${id}`

const AUTHOR = {
  type: 'object',
  properties: {
    task_id: { type: 'string' },
    validator: { type: 'string' },
    sentence_edits: { type: 'number' },
    bindings: { type: 'number' },
    modified: { type: 'number' },
    added: { type: 'number' },
    pins: { type: 'array', items: { type: 'string' } },
    traps_preserved: { type: 'array', items: { type: 'string' } },
    sampled_groups: { type: 'array', items: { type: 'object', properties: {
      group_id: { type: 'string' }, total: { type: 'number' },
      full_rule_outputs: { type: 'array', items: { type: 'string' } }, why: { type: 'string' } },
      required: ['group_id', 'total', 'full_rule_outputs', 'why'] } },
    concerns: { type: 'array', items: { type: 'string' } },
  },
  required: ['task_id', 'validator', 'sentence_edits', 'bindings', 'modified', 'added', 'pins', 'traps_preserved', 'concerns'],
}

const VERIFY = {
  type: 'object',
  properties: {
    task_id: { type: 'string' },
    lens: { type: 'string' },
    problems: { type: 'array', items: { type: 'object', properties: {
      severity: { type: 'string', enum: ['critical', 'major', 'minor'] },
      where: { type: 'string' }, problem: { type: 'string' }, fix: { type: 'string' } },
      required: ['severity', 'where', 'problem', 'fix'] } },
    verdict: { type: 'string' },
  },
  required: ['task_id', 'lens', 'problems', 'verdict'],
}

const REPAIR = {
  type: 'object',
  properties: {
    task_id: { type: 'string' },
    fixed: { type: 'array', items: { type: 'string' } },
    not_fixed: { type: 'array', items: { type: 'object', properties: { problem: { type: 'string' }, why: { type: 'string' } }, required: ['problem', 'why'] } },
    validator: { type: 'string' },
  },
  required: ['task_id', 'fixed', 'not_fixed', 'validator'],
}

const REVERIFY = {
  type: 'object',
  properties: {
    task_id: { type: 'string' },
    still_broken: { type: 'array', items: { type: 'string' } },
    new_critical: { type: 'array', items: { type: 'string' } },
    verdict: { type: 'string' },
  },
  required: ['task_id', 'still_broken', 'new_critical', 'verdict'],
}

function authorPrompt(id) {
  return `You are patching task ${id} of a creative benchmark so it satisfies a reviewer's feedback.

Read the guide FIRST and follow it exactly: ${GUIDE}
It holds the feedback verbatim, the rules, the client's sampling policy for rule checks, the patch schema, and the process.
Then study the worked reference for PHOTO-04: ${FB}/patches/PHOTO-04.json and the builder that produced it, ${FB}/build_photo04_patch.py.

Then, for ${id}:
1. Read every file the guide lists for your task, including EVERY data or text file in /Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/input_assets_v3/${id}/assets/ and ${id}'s asset_plan.json.
2. Write ${FB}/builders/${id}.py that reads the records and emits ${FB}/patches/${id}.json, so every value in a check, pin or binding is copied from a file. Run it.
3. Run the validator: ${VALIDATE(id)}  It must print "accepted: 1". Fix every guard it reports and re-run until it does.

Non-negotiable, because getting these wrong damages the benchmark:
- Pin only what NO supplied source settles. Anything a source resolves (an owner or client note overriding a sheet, a sold or withdrawn item, a corrected figure, a renamed or mapped label, an excluded row, a permission rule) is a deliberate trap: leave it and list it in traps_preserved. Never remove an engineered defect declared in asset_plan.json.
- Every value is copied from the files. Invent no prices, names, claims, brand facts or figures.
- Never touch an automatic check (ids ending A###). Never edit anything under docs/gatsby-v5.
- No em dash or en dash in anything you write.

Return the structured summary. In sampled_groups list every templated run (a group of more than 6 outputs) with the outputs that received the full rule set and why.`
}

function lensPrompt(id, lens) {
  const common = `Independently review the feedback patch for task ${id}. Read the guide first: ${GUIDE}
Then read the patch ${FB}/patches/${id}.json (and its builder ${FB}/builders/${id}.py if present), the task's files (docs/gatsby-v5/tasks/${id}/TASK_SPEC.json and VERIFIERS.json under /Users/dhiren/Documents/ChatGPT/Adobe_Gpt/publish/creative-ai-benchmark), its asset_plan.json, and EVERY data or text file in /Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/input_assets_v3/${id}/assets/.
You are a skeptic. Do not trust the author's summary; re-derive from the files. Report only real problems, each with severity (critical, major, minor), where it is (a check_id, an output_id, or a patch field), what is wrong, and the exact fix. Return an empty problems list if the patch is clean. Do not edit any file.`
  if (lens === 'grounding') {
    return `${common}

YOUR LENS: GROUNDING AND TRAPS.
- Every value in every check, pin and binding: confirm it is copied correctly from the supplied files. Quote file and row for anything wrong. A wrong value is critical.
- Every sentence edit: does it resolve an ambiguity that NO supplied source settles? Flag any pin that gives away a trap a source settles (owner or client overrides, sold or excluded items, corrected figures, label mappings) or that removes difficulty declared in asset_plan.json as defect_engineered. Giving away a trap is critical.
- Is a genuine unresolvable ambiguity left UNPINNED (the reviewer's complaint: which season, which rate, which variant, which photo, which copy line)? Missing pin is major.
- Bindings: row_number counts the header as row 1; values are the approved values after any owner or client correction; raw_values match the file exactly; source_image is the right file.
- Palette roles and rules: grounded in the brand identity text; no invented brand facts; opacity rule judgeable.
- No check contradicts the brief, the pinned brief, or another check.`
  }
  return `${common}

YOUR LENS: COVERAGE, NAMING AND FORM.
- Build the matrix and report every missing cell as major: each type rule in brand_identity.type_system.rules, the signature move, the faces and weight limits, and each palette rule (palette-only colours, opacity, mandatory colours, forbidden colours), crossed with every deliverable the sampling policy selects (every output of a group of 6 or fewer; for a templated run of more than 6, the first, the last, and every trap or edge-case output). Count existing checks as coverage.
- Consistency: every requirement checked on one deliverable must be checked on every other deliverable it applies to. Content and record checks go on every output. Missing ones are major.
- Asset naming: every check that refers to a supplied asset names exact filenames; no group lists; full record names ("Casa Verranza", never "Verranza"). Existing checks that still name a group must have been rewritten via checks_modify. Violations are major.
- Stale evidence: checks whose evidence quotes old typography prose must cite the current type_system. Major.
- Form: one observable fact, Yes or No, objective, at most 40 words, deliverable written as “<name>” (<file>), no em or en dash, correct k_id, no duplicate, no automatic check modified.
- Run the validator yourself: ${VALIDATE(id)}  If it does not print "accepted: 1", that is critical.`
}

function repairPrompt(id, problems) {
  return `Repair the feedback patch for task ${id}. Read the guide first: ${GUIDE}
Patch: ${FB}/patches/${id}.json. Builder: ${FB}/builders/${id}.py (prefer fixing the builder and re-running it, so values stay copied from files).

Two independent reviewers reported these problems. Fix every one that is real. If you judge one is not real, do not change it, and explain why in not_fixed with evidence from the files.
${JSON.stringify(problems, null, 1).slice(0, 24000)}

Do not undo correct work, do not touch automatic checks, do not edit anything under docs/gatsby-v5, no em or en dashes.
Finish by running ${VALIDATE(id)} until it prints "accepted: 1". Return what you fixed, what you did not fix and why, and the final validator line.`
}

function reverifyPrompt(id, critical) {
  return `Adversarially confirm a repair for task ${id}. Read ${GUIDE}, then the CURRENT patch ${FB}/patches/${id}.json and the task's files, including every data or text file in /Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/input_assets_v3/${id}/assets/.
These critical problems were reported before the repair:
${JSON.stringify(critical, null, 1).slice(0, 12000)}
For each, check from the files whether it is now genuinely fixed. Then look for any NEW critical problem: a wrong value, a pin that gives away a trap, a removed engineered defect, a check contradicting the brief. Also run python3 ${FB}/apply_feedback.py --only ${id} and report whether it prints "accepted: 1". Do not edit any file.`
}

phase('Author')
log(`patching ${args.length} tasks; PHOTO-04 is the hand-built reference`)

const results = await pipeline(
  args,
  (id) => agent(authorPrompt(id), { label: `author:${id}`, phase: 'Author', schema: AUTHOR }),
  async (authored, id) => {
    if (!authored) return { id, authored: null }
    const lenses = await parallel(['grounding', 'coverage'].map(l => () =>
      agent(lensPrompt(id, l), { label: `verify-${l}:${id}`, phase: 'Verify', schema: VERIFY })))
    return { id, authored, lenses: lenses.filter(Boolean) }
  },
  async (r, id) => {
    if (!r.authored) return r
    const problems = r.lenses.flatMap(v => (v.problems || []).map(p => ({ ...p, lens: v.lens })))
    if (!problems.length) return { ...r, problems, repair: null }
    const repair = await agent(repairPrompt(id, problems), { label: `repair:${id}`, phase: 'Repair', schema: REPAIR })
    return { ...r, problems, repair }
  },
  async (r, id) => {
    if (!r.authored) return r
    const critical = (r.problems || []).filter(p => p.severity === 'critical')
    if (!critical.length) return { ...r, reverify: null }
    const rv = await agent(reverifyPrompt(id, critical), { label: `reverify:${id}`, phase: 'Re-verify', schema: REVERIFY })
    return { ...r, reverify: rv }
  }
)

const done = results.filter(r => r && r.authored)
const failed = results.filter(r => !r || !r.authored).map(r => (r && r.id) || '?')
const unresolved = done.filter(r => r.reverify && ((r.reverify.still_broken || []).length || (r.reverify.new_critical || []).length))
const notAccepted = done.filter(r => {
  const v = (r.repair && r.repair.validator) || r.authored.validator || ''
  return !/accepted:\s*1/.test(v)
})
const sev = { critical: 0, major: 0, minor: 0 }
done.forEach(r => (r.problems || []).forEach(p => { sev[p.severity] = (sev[p.severity] || 0) + 1 }))

log(`authored ${done.length}/${args.length}; problems found critical ${sev.critical}, major ${sev.major}, minor ${sev.minor}; repaired ${done.filter(r => r.repair).length}; unresolved after re-verify ${unresolved.length}; validator not accepted ${notAccepted.length}`)
if (failed.length) log(`WARNING: no patch from ${failed.join(', ')}`)

return {
  authored: done.length, failed,
  problems_found: sev,
  repaired: done.filter(r => r.repair).map(r => r.id),
  unresolved: unresolved.map(r => ({ id: r.id, still_broken: r.reverify.still_broken, new_critical: r.reverify.new_critical })),
  validator_not_accepted: notAccepted.map(r => r.id),
  not_fixed: done.filter(r => r.repair && (r.repair.not_fixed || []).length).map(r => ({ id: r.id, not_fixed: r.repair.not_fixed })),
  per_task: done.map(r => ({ id: r.id, added: r.authored.added, modified: r.authored.modified, edits: r.authored.sentence_edits,
    bindings: r.authored.bindings, pins: r.authored.pins, traps: r.authored.traps_preserved, sampled: r.authored.sampled_groups || [],
    concerns: r.authored.concerns, problems: (r.problems || []).length })),
}
