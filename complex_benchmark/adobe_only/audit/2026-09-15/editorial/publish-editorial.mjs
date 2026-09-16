import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(process.argv[2]);
const publish = process.argv.includes('--publish');
const staged = path.join(here, 'staged');
const base = path.join(repo, 'complex_benchmark/adobe_only');
const audit = path.join(base, 'audit/2026-09-15');
const sha = value => crypto.createHash('sha256').update(value).digest('hex');
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const stringify = value => `${JSON.stringify(value, null, 2)}\n`;
const sourceFormat = (text, value) => `${JSON.stringify(value, null, text.match(/\n([ \t]+)\S/)?.[1] || 2)}\n`;
const report = read(path.join(staged, 'EDITORIAL_AUDIT.json'));
const currentText = fs.readFileSync(path.join(base, 'TASKS_V3_ALL100.json'), 'utf8');
assert.equal(sha(currentText), report.source_sha256, 'Source changed since staging; re-read before publishing');
const before = JSON.parse(currentText);
const after = read(path.join(staged, 'TASKS_V3_ALL100.json'));
const oldById = new Map(before.map(task => [task.new_id, task]));
const unchanged = task => {
  const copy = structuredClone(task);
  delete copy.client_brief;
  delete copy.marketplace_listing.title;
  delete copy.marketplace_listing.overview;
  return copy;
};
for (const task of after) {
  const original = oldById.get(task.new_id);
  assert.deepEqual(read(path.join(base, 'specs_v3', `${task.new_id}.json`)), original, `${task.new_id}: aggregate and individual file disagree`);
  assert.deepEqual(unchanged(task), unchanged(original), `${task.new_id}: unexpected field change`);
}

// Run the existing validator against staged specs and read-only source assets before publication.
const validationRoot = path.join(staged, 'validation-repo');
const validationAudit = path.join(validationRoot, 'complex_benchmark/adobe_only/audit/2026-09-15');
fs.mkdirSync(validationAudit, { recursive: true });
for (const [target, link] of [
  [path.join(staged, 'specs_v3'), path.join(validationRoot, 'complex_benchmark/adobe_only/specs_v3')],
  [path.join(repo, 'input_assets_v3'), path.join(validationRoot, 'input_assets_v3')],
]) if (!fs.existsSync(link)) fs.symlinkSync(target, link, 'dir');
fs.copyFileSync(path.join(audit, 'ADOBE_CHATGPT_TOOL_INVENTORY_2026-09-15.json'), path.join(validationAudit, 'ADOBE_CHATGPT_TOOL_INVENTORY_2026-09-15.json'));
const result = spawnSync(process.execPath, [path.join(audit, 'validate_specs_v3_1.mjs'), validationRoot], { encoding: 'utf8' });
assert.equal(result.status, 0, result.stdout + result.stderr);
const validation = read(path.join(validationAudit, 'SPEC_VALIDATION_V3_1.json'));
const counts = {
  tasks: after.length,
  deliverables: after.reduce((n, task) => n + task.deliverables.length, 0),
  verifiers: after.reduce((n, task) => n + task.verifiers_auto.length + task.verifiers_process.length + task.verifiers_human.length, 0),
  validation: validation.status,
};
if (!publish) {
  console.log(JSON.stringify({ mode: 'dry-run', ...counts, changed_fields: report.changed_fields }, null, 2));
  process.exit(0);
}

const editorialDest = path.join(audit, 'editorial');
fs.mkdirSync(editorialDest, { recursive: true });
fs.writeFileSync(path.join(base, 'TASKS_V3_ALL100.json'), sourceFormat(currentText, after));
for (const task of after) {
  const file = path.join(base, 'specs_v3', `${task.new_id}.json`);
  fs.writeFileSync(file, sourceFormat(fs.readFileSync(file, 'utf8'), task));
}
fs.writeFileSync(path.join(audit, 'TASKS_V3_ALL100_CURRENT.json'), stringify(after));
fs.writeFileSync(path.join(audit, 'SPEC_VALIDATION_V3_1.json'), stringify(validation));
for (const name of fs.readdirSync(here).filter(name => /^\d\d-.*\.md$/.test(name) || ['build-editorial.mjs', 'publish-editorial.mjs', 'SOURCE_ISSUES.md'].includes(name))) {
  fs.copyFileSync(path.join(here, name), path.join(editorialDest, name));
}
for (const name of ['EDITORIAL_AUDIT.json', 'CLIENT_BRIEFS_100.md']) fs.copyFileSync(path.join(staged, name), path.join(editorialDest, name));

const freezeResult = spawnSync(process.execPath, [path.join(audit, 'build_freeze_manifest.mjs'), repo], { encoding: 'utf8' });
assert.equal(freezeResult.status, 0, freezeResult.stdout + freezeResult.stderr);
const freeze = read(path.join(audit, 'FREEZE_MANIFEST_V3.json'));
const s3Path = path.join(audit, 'S3_ASSET_INDEX_V3_1.json');
const s3 = read(s3Path);
s3.corpus_fingerprint_sha256 = freeze.corpus_fingerprint_sha256;
fs.writeFileSync(s3Path, stringify(s3));
console.log(JSON.stringify({ mode: 'published', ...counts, asset_files_unchanged: freeze.asset_count, corpus_fingerprint: freeze.corpus_fingerprint_sha256 }, null, 2));
