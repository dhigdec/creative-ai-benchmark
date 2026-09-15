#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const OUT = path.dirname(new URL(import.meta.url).pathname);
const PROJECT = path.resolve(process.argv[2] || path.join(OUT, "../../../.."));
const SPEC_DIR = path.join(PROJECT, "complex_benchmark/adobe_only/specs_v3");
const ASSET_DIR = path.join(PROJECT, "input_assets_v3");

function hashBuffer(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

function hashFile(file) {
  return hashBuffer(fs.readFileSync(file));
}

function canonical(value) {
  if (Array.isArray(value)) return value.map(canonical);
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonical(value[key])]));
  }
  return value;
}

function csvCell(value) {
  const text = String(value ?? "");
  return /[",\n\r]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

const specs = fs.readdirSync(SPEC_DIR).filter((name) => name.endsWith(".json")).sort().map((name) => {
  const file = path.join(SPEC_DIR, name);
  return { name, file, spec: JSON.parse(fs.readFileSync(file, "utf8")) };
});

const taskEntries = [];
for (const { name, file, spec } of specs) {
  const taskId = spec.new_id;
  const manifestPath = path.join(ASSET_DIR, taskId, "manifest.json");
  const assetsPath = path.join(ASSET_DIR, taskId, "assets");
  const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  const assets = (manifest.assets || []).map((asset) => {
    const assetPath = path.join(assetsPath, asset.filename);
    const stat = fs.statSync(assetPath);
    return {
      filename: asset.filename,
      bytes: stat.size,
      sha256: hashFile(assetPath)
    };
  });
  taskEntries.push({
    task_id: taskId,
    spec_file: name,
    spec_sha256: hashFile(file),
    canonical_spec_sha256: hashBuffer(JSON.stringify(canonical(spec))),
    asset_manifest_sha256: hashFile(manifestPath),
    asset_count: assets.length,
    asset_bytes: assets.reduce((sum, asset) => sum + asset.bytes, 0),
    assets
  });
}

const aggregate = specs.map(({ spec }) => spec);
fs.writeFileSync(path.join(OUT, "TASKS_V3_ALL100_CURRENT.json"), `${JSON.stringify(aggregate, null, 2)}\n`);

const corpusFingerprint = hashBuffer(taskEntries.map((entry) => [
  entry.task_id,
  entry.canonical_spec_sha256,
  entry.asset_manifest_sha256,
  ...entry.assets.map((asset) => `${asset.filename}:${asset.sha256}`)
].join("\n")).join("\n"));

const freeze = {
  schema_version: "1.0",
  generated_at: new Date().toISOString(),
  project: PROJECT,
  corpus_fingerprint_sha256: corpusFingerprint,
  task_count: taskEntries.length,
  asset_count: taskEntries.reduce((sum, task) => sum + task.asset_count, 0),
  asset_bytes: taskEntries.reduce((sum, task) => sum + task.asset_bytes, 0),
  tasks: taskEntries
};
fs.writeFileSync(path.join(OUT, "FREEZE_MANIFEST_V3.json"), `${JSON.stringify(freeze, null, 2)}\n`);
const assetCsv = [
  ["task_id", "filename", "bytes", "sha256", "spec_sha256", "asset_manifest_sha256"],
  ...taskEntries.flatMap((task) => task.assets.map((asset) => [
    task.task_id,
    asset.filename,
    asset.bytes,
    asset.sha256,
    task.spec_sha256,
    task.asset_manifest_sha256
  ]))
].map((row) => row.map(csvCell).join(",")).join("\n");
fs.writeFileSync(path.join(OUT, "ASSET_MANIFEST_V3.csv"), `${assetCsv}\n`);
console.log(JSON.stringify({
  task_count: freeze.task_count,
  asset_count: freeze.asset_count,
  asset_bytes: freeze.asset_bytes,
  corpus_fingerprint_sha256: freeze.corpus_fingerprint_sha256
}, null, 2));
