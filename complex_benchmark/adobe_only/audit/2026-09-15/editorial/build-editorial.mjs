import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(process.argv[2]);
const out = path.resolve(process.argv[3] || path.join(here, 'staged'));
const sourcePath = path.join(repo, 'complex_benchmark/adobe_only/TASKS_V3_ALL100.json');
const sourceText = fs.readFileSync(sourcePath, 'utf8');
const source = JSON.parse(sourceText);
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
const asJson = value => `${JSON.stringify(value, null, 2)}\n`;
const drafts = new Map();

for (const file of fs.readdirSync(here).filter(name => /^\d\d-.*\.md$/.test(name)).sort()) {
  const content = fs.readFileSync(path.join(here, file), 'utf8');
  for (const match of content.matchAll(/^@@ (\d+) \| (.+)\n([\s\S]*?)(?=^@@ |$(?![\s\S]))/gm)) {
    const order = Number(match[1]);
    assert(!drafts.has(order), `Duplicate draft ${order}`);
    drafts.set(order, { title: match[2], body: match[3].trim(), file });
  }
}
assert.equal(drafts.size, 100, 'Every task needs an individually authored draft');

function productionText(value) {
  return value
    .replace('One professionally selected Adobe Express template adapted to the supplied brand, copy, and approved imagery. The agent is pre-authorized to choose the strongest fitting template, replace its content, correct the background where needed, and deliver both the editable design link and requested export. This is a supporting asset, not a substitute for the primary custom craft deliverable.', 'Choose and adapt an Adobe Express template for these supporting pieces, using the supplied brand, approved copy and imagery. Select the strongest fit, replace the template content and correct its background as needed. Supply the editable design link and the requested export, in addition to the commissioned custom production work.')
    .replaceAll('Vectorization is a starting operation, not proof of production readiness:', 'Do not treat a trace alone as production approval:')
    .replaceAll('Quick Cut may choose visually engaging moments; it must not be credited with understanding speech or claims.', 'Any automated highlight selection is a visual aid, not evidence that speech or claims have been understood.')
    .replaceAll('Quick Cut may choose the visually strongest span inside each short clip; it must not combine the two brands or imply speech.', 'Select the strongest visual span within each short clip; do not combine the two brands or imply speech.')
    .replaceAll('one call per frame with a parameter log', 'each frame processed separately with a parameter log')
    .replaceAll('whose identity is guaranteed per call rather than by position in a returned list', 'whose record identity is guaranteed by explicit selection rather than inferred from export order')
    .replaceAll('every resize any tool reported', 'every reported resize')
    .replaceAll('every crop or resize tradeoff the tools reported transcribed', 'all reported crop and resize limitations recorded')
    .replaceAll('every crop tradeoff the tools reported transcribed', 'all reported crop limitations recorded')
    .replace(/\bper frame\b/g, 'per-frame')
    .replace(/\bcamera scale\b/g, 'camera-scale')
    .replace(/\bcolour accurate\b/g, 'colour-accurate')
    .replace(/\bprint resolution\b/g, 'print-resolution')
    .replace(/\s{2,}/g, ' ')
    .trim();
}

function contract(task) {
  const t = task.project_terms;
  const amount = t.modeled_marketplace_budget.replace(/ fixed$/, '');
  const clauses = [
    `Budget: ${t.modeled_marketplace_budget}. Target: ${t.delivery_window}. Reviews: ${t.revision_structure}.`,
    `This is a fixed-price commission at ${amount}, with a target of ${t.delivery_window}. The agreed review allowance is ${t.revision_structure.toLowerCase()}.`,
    `Fee range: ${t.modeled_marketplace_budget}\nDelivery target: ${t.delivery_window}\nIncluded reviews: ${t.revision_structure}.`,
    `Please work within ${t.modeled_marketplace_budget} and the ${t.delivery_window} target. Allow for ${t.revision_structure.toLowerCase()}.`,
    `${t.modeled_marketplace_budget}; ${t.delivery_window}. Review structure: ${t.revision_structure}.`,
    `The commission is budgeted at ${t.modeled_marketplace_budget}. We have allowed ${t.delivery_window}, including ${t.revision_structure.toLowerCase()}.`,
  ];
  return `${clauses[(task.global_order - 1) % clauses.length]} ${t.scope_change_policy}`;
}

function handoff(task) {
  const labels = {
    'delivery manifest': 'a delivery manifest',
    'scoped editable sources': 'the editable sources specified above',
    'final exports': 'final exports',
    'production and exception note': 'a short production and exceptions note',
    'normalized data file and mapping record': 'the normalised data and field-mapping record',
    'final EDL and measured source metadata': 'the final edit decision list and measured source metadata',
  };
  const parts = task.handover_requirements.contents.map(item => labels[item] || item);
  const required = parts.slice(0, -1).join(', ') + ' and ' + parts.at(-1);
  const variations = [
    `Please deliver ${required}. Account for every supplied file and identify anything used only as reference, superseded or rejected.`,
    `Handover: ${required}. Include an inventory showing how every supplied file was used or why it was set aside.`,
    `The final package should contain ${required}, with every source file accounted for, including references and rejected or superseded material.`,
    `Alongside the finished work, we need ${required}. Keep a clear record of the supplied files used, retained for reference, superseded and rejected.`,
  ];
  const truth = [
    'Stay with approved facts and copy. Do not silently replace weak assets; use only the stated stock or concept allowances, and record omissions, substitutions, reconciliations and material compromises.',
    'Keep factual content tied to the approved inputs. Any missing coverage, substituted asset, reconciliation or quality compromise must be declared; a weak source is not permission to invent or silently replace it.',
    'Use the approved information without inventing missing facts. Only the stated stock or concept exceptions permit substitution; document every omission, replacement, reconciliation and material quality compromise.',
    'Approved source information remains authoritative. Record omissions, substitutions, reconciliations and quality limits, and do not use an undeclared replacement or invented fact to conceal a source problem.',
  ];
  let result = `${variations[(task.global_order - 1) % variations.length]} ${truth[(task.global_order - 1) % truth.length]}`;
  if (task.family === 'Vector & Print') result += ' Include inspectable paths and small-size proofs; unverified fabrication tolerances remain subject to supplier review.';
  if (task.family === 'Motion & Audio') result += ' Keep runtime within measured source duration and the stated cap; do not invent footage or dialogue.';
  return result;
}

function protectedData(task) {
  const value = structuredClone(task);
  delete value.client_brief;
  delete value.marketplace_listing.title;
  delete value.marketplace_listing.overview;
  return value;
}

const checks = [];
const updated = source.map(task => {
  const draft = drafts.get(task.global_order);
  assert(draft, task.task_code);
  const active = [...new Set(task.asset_use_plan.filter(a => a.expected_role !== 'out_of_scope_reference').map(a => a.name))];
  const archive = [...new Set(task.asset_use_plan.filter(a => a.expected_role === 'out_of_scope_reference').map(a => a.name))];
  const tokens = {
    files: active.join('; ') + '.',
    archive: archive.length ? `Also in the archive, for background only: ${archive.join('; ')}. These do not add deliverables to this commission.` : '',
    terms: contract(task),
    handoff: handoff(task),
  };
  if (task.family === 'Motion & Audio') {
    const media = task.asset_readiness.motion_truth;
    tokens.files += `\n\nMedia inventory: ${media.video_file_count} video files, ${media.total_video_seconds} seconds in total; ${media.video_files_with_audio_streams} with embedded audio; ${media.separate_audio_file_count} separate audio files (${media.total_separate_audio_seconds} seconds). These measured sources set the production limits.`;
  }
  task.deliverables.forEach((d, index) => {
    const label = /One professionally selected Adobe Express template/.test(d.spec) ? `${d.name}: ` : '';
    tokens[`d${index + 1}`] = label + productionText(d.spec);
  });
  for (let index = 1; index <= task.deliverables.length; index++) {
    assert.equal(draft.body.split(`{{d${index}}}`).length - 1, 1, `${task.task_code}: scope ${index} must appear exactly once`);
  }
  const body = draft.body.replace(/\{\{(\w+)\}\}/g, (_, key) => {
    assert(key in tokens, `Unknown token ${key}`);
    return tokens[key];
  }).replace(/\n{3,}/g, '\n\n');
  const brief = `${draft.title}\n\n${body}`;
  const copy = structuredClone(task);
  copy.client_brief = brief;
  copy.marketplace_listing.title = draft.title;
  copy.marketplace_listing.overview = draft.body.split('\n\n').find(p => p.length > 50 && !p.includes('{{') && !p.includes('\n'));
  assert.deepEqual(protectedData(copy), protectedData(task), `${task.task_code}: non-editorial drift`);
  assert(!/\{\{|\.\.\.|benchmark series|We are hiring an expert to turn|Project overview|What we will provide|Scope and deliverables|Non-negotiables|Working process/.test(brief), `${task.task_code}: unfinished or legacy prose`);
  assert(draft.title.length <= 120, `Title too long: ${task.task_code}`);
  assert(!/\bthe agent\b|connector implementation/i.test(brief), `${task.task_code}: internal language`);
  task.deliverables.forEach((d, index) => assert(brief.includes(tokens[`d${index + 1}`]), `${task.task_code}: missing complete scope`));
  for (const name of [...active, ...archive]) assert(brief.includes(name), `${task.task_code}: missing asset ${name}`);
  checks.push({
    task_code: task.task_code,
    draft: draft.file,
    words: brief.trim().split(/\s+/).length,
    before_brief_sha256: hash(task.client_brief),
    after_brief_sha256: hash(brief),
    protected_data_sha256: hash(JSON.stringify(protectedData(task))),
    complete_delivery_specs: task.deliverables.length,
    asset_roles_retained: true,
    non_editorial_fields_unchanged: true,
  });
  return copy;
});

const sorted = [...updated].sort((a, b) => a.global_order - b.global_order);
assert.equal(new Set(sorted.map(t => t.client_brief)).size, 100);
assert.equal(new Set(sorted.map(t => t.marketplace_listing.title)).size, 100);
const report = {
  date: '2026-09-15',
  source_sha256: hash(sourceText),
  task_count: updated.length,
  revised_briefs: checks.filter(c => c.before_brief_sha256 !== c.after_brief_sha256).length,
  complete_deliverable_specs_retained: checks.reduce((sum, c) => sum + c.complete_delivery_specs, 0),
  changed_fields: ['client_brief', 'marketplace_listing.title', 'marketplace_listing.overview'],
  unchanged: ['task codes and canonical names', 'asset lists and roles', 'brand identities', 'deliverable contracts', 'verifier contracts and all checks', 'connector profiles', 'project terms', 'source provenance', 'handover requirements'],
  length_outliers: checks.filter(c => c.words < 180 || c.words > 760).map(c => ({ task_code: c.task_code, words: c.words })),
  notes: [
    'Editorial review is not execution or proof of creative output quality.',
    'Technical schedules are retained in full, with limited readability substitutions recorded in productionText().',
    'Existing naming/scope defects are recorded separately rather than silently changing benchmark contracts.',
  ],
  checks,
};
fs.mkdirSync(path.join(out, 'specs_v3'), { recursive: true });
fs.writeFileSync(path.join(out, 'TASKS_V3_ALL100.json'), asJson(updated));
fs.writeFileSync(path.join(out, 'EDITORIAL_AUDIT.json'), asJson(report));
fs.writeFileSync(path.join(out, 'CLIENT_BRIEFS_100.md'), '# Creative AI Benchmark: Client Briefs\n\n' + sorted.map(t => `## ${t.task_code} | ${t.task_name}\n\n${t.client_brief}`).join('\n\n---\n\n') + '\n');
for (const t of updated) fs.writeFileSync(path.join(out, 'specs_v3', `${t.new_id}.json`), asJson(t));
fs.writeFileSync(path.join(out, 'SHEET_EDITORIAL_VALUES.json'), asJson(sorted.map(t => ({ code: t.task_code, family: t.family, title: t.marketplace_listing.title, brief: t.client_brief }))));
console.log(JSON.stringify({ task_count: report.task_count, revised_briefs: report.revised_briefs, complete_deliverable_specs_retained: report.complete_deliverable_specs_retained, length_outliers: report.length_outliers, output: out }, null, 2));
