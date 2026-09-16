import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const repo = path.resolve(process.argv[2]);
const base = 'complex_benchmark/adobe_only';
const readHead = file => execFileSync('git', ['show', `HEAD:${file}`], { cwd: repo, encoding: 'utf8', maxBuffer: 30 * 1024 * 1024 });
const read = file => JSON.parse(fs.readFileSync(path.join(repo, file), 'utf8'));
const current = read(`${base}/TASKS_V3_ALL100.json`);
const original = JSON.parse(readHead(`${base}/TASKS_V3_ALL100.json`));
const protectedCopy = task => {
  const copy = structuredClone(task);
  delete copy.client_brief;
  delete copy.marketplace_listing.title;
  delete copy.marketplace_listing.overview;
  return copy;
};
assert.equal(current.length, 100);
const oldById = new Map(original.map(task => [task.new_id, task]));
for (const task of current) {
  assert.deepEqual(protectedCopy(task), protectedCopy(oldById.get(task.new_id)));
  assert.deepEqual(read(`${base}/specs_v3/${task.new_id}.json`), task);
  assert.notEqual(task.client_brief, oldById.get(task.new_id).client_brief);
}
if (process.argv.includes('--restore-format')) {
  for (const file of [`${base}/TASKS_V3_ALL100.json`, ...current.map(task => `${base}/specs_v3/${task.new_id}.json`)]) {
    const indent = readHead(file).match(/\n([ \t]+)\S/)?.[1] || 2;
    const value = read(file);
    fs.writeFileSync(path.join(repo, file), `${JSON.stringify(value, null, indent)}\n`);
  }
}
const freezePath = `${base}/audit/2026-09-15/FREEZE_MANIFEST_V3.json`;
const oldFreeze = JSON.parse(readHead(freezePath));
const newFreeze = read(freezePath);
const assets = freeze => freeze.tasks.map(task => ({ id: task.task_id, manifest: task.asset_manifest_sha256, assets: task.assets }));
assert.deepEqual(assets(newFreeze), assets(oldFreeze), 'Asset bytes or manifests changed');
if (process.argv.includes('--sync-audit')) {
  const here = path.dirname(fileURLToPath(import.meta.url));
  const dest = path.join(repo, base, 'audit/2026-09-15/editorial');
  for (const name of ['build-editorial.mjs', 'publish-editorial.mjs', 'verify-editorial.mjs', 'SOURCE_ISSUES.md']) fs.copyFileSync(path.join(here, name), path.join(dest, name));
  fs.copyFileSync(path.join(here, 'staged/SHEET_VERIFICATION.json'), path.join(dest, 'SHEET_VERIFICATION.json'));
}
console.log(JSON.stringify({ briefs_changed: 100, protected_fields_unchanged: true, individual_specs_match: true, asset_hashes_unchanged: newFreeze.asset_count, original_format_restored: process.argv.includes('--restore-format') }, null, 2));
