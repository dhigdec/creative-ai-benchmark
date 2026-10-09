export const meta = {
  name: 'verify-strength-suite-10',
  description: 'Independently verify all 10 finished StudioBench strength-suite runs: trajectory validity + completeness, deliverables, verifier honesty, truth/IP',
  phases: [{ title: 'Verify', detail: 'one agent per finished run' }],
}

const BATCH = '/Users/dhiren/Documents/ChatGPT/Adobe_Gpt/benchmark_runs/batch_10_2026-09-17_strength-suite-01'
const PROTO = '/Users/dhiren/Documents/ChatGPT/Adobe_Gpt/trajectory_protocol'
const REF = BATCH + '/SB3-006-PHO__hollis-family-archive-ada-hollis-archival-restoration'

const RUNS = [
  ['SB3-006-PHO','PHOTO-06','SB3-006-PHO__hollis-family-archive-ada-hollis-archival-restoration'],
  ['SB3-011-PHO','PHOTO-11','SB3-011-PHO__lumora-lip-oil-shade-concept-set'],
  ['SB3-020-PHO','PHOTO-20','SB3-020-PHO__astrid-vellacourt-editorial-portrait-session'],
  ['SB3-035-VEC','VECTOR-05','SB3-035-VEC__isla-verde-monogram-and-wayfinding-pictogram-system'],
  ['SB3-045-VEC','VECTOR-15','SB3-045-VEC__marchfield-exchange-crest-and-engraving-geometry-system'],
  ['SB3-046-LAY','LAYOUT-01','SB3-046-LAY__kantyna-nova-private-dining-menu-and-campaign-system'],
  ['SB3-059-LAY','LAYOUT-14','SB3-059-LAY__lumen-quarterly-autumn-editorial-issue'],
  ['SB3-067-LAY','LAYOUT-22','SB3-067-LAY__cedarline-institute-cohort-credential-system'],
  ['SB3-083-MOT','MOTION-03','SB3-083-MOT__halden-greens-creator-ad-and-social-cutdowns'],
  ['SB3-088-MOT','MOTION-08','SB3-088-MOT__sentinelmesh-product-demo-and-narration-package'],
]

const SCHEMA = {
  type: 'object',
  properties: {
    task_code: { type: 'string' },
    legacy_id: { type: 'string' },
    validator_valid: { type: 'boolean' },
    validator_error_count: { type: 'number' },
    validator_errors: { type: 'array', items: { type: 'string' } },
    trajectory_quality_score: { type: 'number', description: '0-5, how good/complete the trajectory is per Protocol V2' },
    intake_complete: { type: 'boolean', description: 'brief, brand, deliverables, verifiers, input_assets all populated' },
    events_count: { type: 'number' },
    events_meaningful: { type: 'boolean', description: 'events carry real rationale/evidence, not filler' },
    previews_on_every_change: { type: 'boolean', description: 'every artifact-changing event has a preview_ref or explicit not_exposed reason' },
    k_questions_present: { type: 'boolean' },
    phase0_present: { type: 'boolean' },
    professional_review_present: { type: 'boolean' },
    disclosure_honest: { type: 'boolean', description: 'limitations/blocked/pending honestly recorded, matching what actually failed' },
    secrets_found: { type: 'boolean' },
    deliverables_expected: { type: 'number' },
    deliverables_present: { type: 'number' },
    deliverables_all_readable: { type: 'boolean' },
    dimension_or_count_mismatches: { type: 'array', items: { type: 'string' } },
    intermediates_present: { type: 'boolean', description: 'previews/ and intermediate artifacts genuinely present, not just finals' },
    auto_pass: { type: 'number' }, auto_total: { type: 'number' },
    process_pass: { type: 'number' }, process_total: { type: 'number' },
    human_ready: { type: 'number' }, human_total: { type: 'number' },
    verifier_spotcheck_ok: { type: 'boolean', description: 'you re-checked >=2 auto verifiers against the real files and they hold' },
    verifier_discrepancies: { type: 'array', items: { type: 'string' } },
    truth_ip_issues: { type: 'array', items: { type: 'string' } },
    trajectory_contains_everything: { type: 'boolean', description: 'THE KEY QUESTION: does the trajectory fully capture intake, decisions, every connector action, intermediates, verification, and handoff?' },
    overall_verdict: { type: 'string', description: 'PASS | MINOR_FIX | MAJOR_FIX' },
    top_issues: { type: 'array', items: { type: 'string' }, description: 'each prefixed CRITICAL/MAJOR/MINOR' },
    one_line_summary: { type: 'string' },
  },
  required: ['task_code','validator_valid','trajectory_quality_score','deliverables_expected','deliverables_present','overall_verdict','trajectory_contains_everything','one_line_summary'],
}

function prompt(code, legacy, dir) {
  const RUN = BATCH + '/' + dir
  return `You are independently verifying ONE finished StudioBench benchmark run. Be a rigorous, skeptical auditor — the run was produced by a different agent and claims success; your job is to confirm it honestly, especially whether the TRAJECTORY is good and contains everything.

RUN DIR: ${RUN}
TASK: ${code} (legacy ${legacy})
PROTOCOL DIR: ${PROTO}
REFERENCE (a known-good completed run to compare shape/density against): ${REF}

Do all of this with Read/Bash/Grep (read-only — DO NOT modify any file in the run dir):

1. TRAJECTORY VALIDITY: run \`node ${PROTO}/validate_trajectory.mjs ${RUN}/trajectory.json\` and capture its JSON (valid + errors[]). Report validator_valid, validator_error_count, and the errors verbatim. NOTE: the validator only enforces deliverable/verifier completeness when run.status === "completed"; for "completed_with_declared_connector_limitations" those completeness checks are skipped by the validator, so you MUST check completeness yourself in steps 3-4.

2. TRAJECTORY QUALITY & COMPLETENESS (Protocol V2 — this is the user's priority). Read ${RUN}/trajectory.json fully. Judge:
   - intake_complete: task.client_brief, acceptance_bar, brand_identity, expected_deliverables, task_verifiers, and input_assets[] (with hashes/roles/dispositions) all populated.
   - events: count them; are they MEANINGFUL (real intent + rationale_summary with evidence/decision/tradeoffs/alternatives, real tool_call params, before/after previews) or thin/filler? Compare density vs the REFERENCE run (22 events, dense rationale).
   - previews_on_every_change: every event whose output_state.artifact_versions_created is non-empty must have preview_refs OR a preview_unavailable_reason. Grep/scan for violations (the validator also checks this).
   - k_questions_present (28 K1-K6 questions), phase0_present (7 task Qs + 8 asset dimensions), professional_review_present (verdict + pin_the_flaw + confidence), disclosure honest (do limitations/blocked_work match what actually failed?), no secrets (validator checks; also eyeball).
   - trajectory_contains_everything: your holistic verdict on whether the trajectory captures intake→decisions→every connector action→intermediates→verification→handoff.

3. DELIVERABLES: read ${RUN}/artifacts/DELIVERY_MANIFEST.json and ${RUN}/TASK_SPEC.json (deliverables[]). Confirm every scoped deliverable name from TASK_SPEC appears in the manifest with a terminal status and real files. Then actually inspect the files on disk (ls ${RUN}/artifacts, open a sample) — are they present, non-empty, readable, and matching declared format/dimensions/COUNTS (e.g. "8 speaker cards" => 8 files; "9 masters" => 9)? Use python3/sips or the Read tool to confirm dimensions on 2-3 key raster deliverables. List any missing/mismatch in dimension_or_count_mismatches. Confirm intermediates_present (previews/ populated with before/after/revision states, not only finals).

4. VERIFIER HONESTY: read ${RUN}/verifier-results.json. Record auto_pass/total, process_pass/total, human_ready/total. Then RE-CHECK at least 2 auto verifiers yourself against the real files (e.g. "every input has a disposition", "N outputs exist", "files match declared dims", "ground-free files carry real alpha" => check for an alpha channel). If a claimed auto-pass does not actually hold on the files, record it in verifier_discrepancies. Human verifiers should be "ready"/unscored, NOT self-passed — flag if any human verifier was self-scored as passed.

5. TRUTH / IP: grep the produced text artifacts (${RUN}/artifacts/**/*.csv, *.md, *.json, *.txt) for invented records or real brand/trademark leaks (real company names, product trademarks, real people, real venues/addresses). The V3.1 corpus is supposed to be IP-laundered. Spot-check 2-3 produced deliverable IMAGES with the Read tool for obvious real-brand text/logos. List concrete findings in truth_ip_issues (empty array if clean).

6. VERDICT: overall_verdict = PASS (trajectory valid + complete, deliverables all present/correct, verifiers honest, no IP issues), MINOR_FIX (small gaps), or MAJOR_FIX (validator fails, missing deliverables, dishonest verifiers, or IP leaks). Put the most important problems in top_issues (prefix each CRITICAL/MAJOR/MINOR). Give a one_line_summary.

Return ONLY the structured object. Base every boolean and count on something you actually opened — do not trust the run's own STATUS claims.`
}

phase('Verify')
const results = await parallel(RUNS.map(([code, legacy, dir]) => () =>
  agent(prompt(code, legacy, dir), { label: `verify:${code}`, phase: 'Verify', agentType: 'general-purpose', schema: SCHEMA })
))

return { verified: results.filter(Boolean), null_count: results.filter(r => !r).length }
