export const meta = {
  name: 'v4-deep-task-audit',
  description: 'Deep independent audit of all 100 v4 tasks: brief realism/hardness, deliverable quality, verifier scoreability; confirm/refute/extend ChatGPT repair flags',
  phases: [{ title: 'Audit', detail: '20 agents x 5 tasks each = 100-task coverage' }],
}

const DIR = '/private/tmp/claude-501/-Users-dhiren-Downloads-Deccan/aa9e6dfc-7579-493e-a3a8-45be309ed406/scratchpad/v4audit'
const pad = n => String(n).padStart(2, '0')
const IDS = []
for (let i = 1; i <= 30; i++) IDS.push('PHOTO-' + pad(i))
for (let i = 1; i <= 15; i++) IDS.push('VECTOR-' + pad(i))
for (let i = 1; i <= 35; i++) IDS.push('LAYOUT-' + pad(i))
for (let i = 1; i <= 20; i++) IDS.push('MOTION-' + pad(i))
const BATCHES = []
for (let i = 0; i < IDS.length; i += 5) BATCHES.push(IDS.slice(i, i + 5))

const TASK_SCHEMA = {
  type: 'object',
  properties: {
    task_id: { type: 'string' },
    task_name: { type: 'string' },
    family: { type: 'string' },
    brief_realism_score: { type: 'number', description: '1-5: is this a real, hard, industry-standard freelance commission (5) or a thin/toy/atomic op dressed up (1)?' },
    brief_is_real_hard_commission: { type: 'boolean' },
    brief_note: { type: 'string' },
    deliverables_score: { type: 'number', description: '1-5: are the deliverables real finished professional client outputs (5) or generic-template / proof-sheet-as-deliverable / vague (1)?' },
    deliverables_are_real_professional: { type: 'boolean' },
    deliverable_issues: { type: 'array', items: { type: 'string' } },
    verifier_scoreability_score: { type: 'number', description: '1-5: from the sample+counts, are checks binary/objective/answerable by an expert, at a sane volume?' },
    verifier_issues: { type: 'array', items: { type: 'string' }, description: 'e.g. subjective wording, unanswerable, too many checks per output, missing a needed check' },
    chatgpt_flags_confirmed: { type: 'array', items: { type: 'string' }, description: "ChatGPT repair flags for this task you independently CONFIRM are real (name them)" },
    chatgpt_flags_refuted: { type: 'array', items: { type: 'string' }, description: "ChatGPT flags you think are WRONG/overstated, with why" },
    missed_issues: { type: 'array', items: { type: 'string' }, description: "real defects ChatGPT's repair audit did NOT flag for this task" },
    overall_verdict: { type: 'string', description: 'READY | MINOR_REPAIR | MAJOR_REPAIR' },
    one_line: { type: 'string' },
  },
  required: ['task_id', 'brief_realism_score', 'deliverables_score', 'verifier_scoreability_score', 'overall_verdict', 'one_line'],
}
const SCHEMA = { type: 'object', properties: { tasks: { type: 'array', items: TASK_SCHEMA } }, required: ['tasks'] }

function prompt(ids) {
  return `You are a rigorous, skeptical benchmark auditor. Independently judge whether these ${ids.length} StudioBench **v4** creative-AI tasks are genuinely ready — real hard client briefs, real professional deliverables, and verifiers an expert can actually score. Do NOT rubber-stamp; ground every judgment in the actual text you read.

CONTEXT — what v4 is supposed to be:
- Each task is a real, hard, industry-standard freelance creative commission (poster/campaign/product-page/editorial/identity/packaging/credential/film, etc.) — NOT a toy or a single atomic op ("remove background") dressed up.
- Deliverables should be FINISHED client outputs (a composed ad, a laid-out menu, a data-merged card run, a playable film). Supporting production assets (graded photos, masks, crop sheets, recovered marks, approval/proof sheets) are legitimate ONLY when the client explicitly hired a specialist for them — otherwise counting a proof sheet or a lone template PDF as a deliverable is a defect.
- Verifiers are "atomic": each is one binary Yes/No check bound to one exact deliverable path. Auto checks assert bytes (exists/decodes/dimensions/pages/duration/transparency/geometry); human checks judge meaning/brand/hierarchy in plain answerable language.
- Known systemic issues ChatGPT already flagged corpus-wide (check if YOUR tasks are affected and whether the flag is correct): 19 generic-template tasks (one template paragraph standing in for a whole collateral set); 14 tasks that inflate the deliverable list with a proof/approval/crop sheet; logo/graphic PNGs delivered fully opaque (no real transparency); 12 MOTION tasks whose human checks expect audio/voice their silent source packs don't contain; a few wrong display names (e.g. PHOTO-15 labelled watches but describes overlanding gear; PHOTO-22 labelled outerwear but describes a harbour hotel).

For EACH task id ${JSON.stringify(ids)}:
1. Read its file with the Read tool: ${DIR}/<TASK_ID>.json — it contains {spec, chatgpt_repair_audit, verifier_summary}. spec has client_brief, brand_identity, production_requirements, truth_constraints, deliverables, deliverable_groups, assets_summary, readiness, verifier counts. chatgpt_repair_audit has ChatGPT's flags (priority, scope_action, generic_template_groups, support_proof_groups, silent_audio_conflict, asset_repairs, task_specific_issue, verifier_action, proposed_client_outputs). verifier_summary has atomic counts + sample_auto + sample_human.
2. Judge the three axes on 1-5, grounded in the text:
   - BRIEF: real, hard, industry-standard commission? (read client_brief + production_requirements). Is it genuinely hard freelance work, or thin/generic/toy?
   - DELIVERABLES: real finished professional outputs? Or generic-template / proof-as-deliverable / vague / mislabeled? Inspect deliverables + deliverable_groups against the brief. List concrete issues.
   - VERIFIER SCOREABILITY: from verifier_summary sample_auto/sample_human + counts, can an expert answer each as a clean Yes/No against a named file? Flag any subjective/unanswerable wording, and flag if checks_per_output is unreasonably high (an expert scoring burden).
3. Cross-check ChatGPT's repair audit: list which of its flags you CONFIRM (chatgpt_flags_confirmed), which you REFUTE as wrong/overstated with why (chatgpt_flags_refuted), and any real defect it MISSED (missed_issues).
4. overall_verdict: READY (no repair needed) | MINOR_REPAIR (small fixes) | MAJOR_REPAIR (brief/deliverable/verifier substantively broken). Give a one_line.

Return ONLY the structured object with a "tasks" array holding one verdict per task, in the given id order.`
}

phase('Audit')
const results = await parallel(BATCHES.map((ids, bi) => () =>
  agent(prompt(ids), { label: `audit:${ids[0]}..${ids[ids.length-1]}`, phase: 'Audit', agentType: 'general-purpose', schema: SCHEMA })
))

const all = results.filter(Boolean).flatMap(r => (r && r.tasks) || [])
return { batches: results.length, null_batches: results.filter(r => !r).length, task_verdicts: all.length, tasks: all }
