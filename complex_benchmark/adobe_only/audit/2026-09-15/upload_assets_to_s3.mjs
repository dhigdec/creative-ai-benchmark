#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";

const repo = path.resolve(process.argv[2]);
const awsCli = path.resolve(process.argv[3]);
const profile = process.argv[4] || "874846752452_S3FullAccess";
if (!repo || !awsCli || !fs.existsSync(awsCli)) throw new Error("Usage: node upload_assets_to_s3.mjs <repo-root> <aws-cli-path> [profile]");

const auditDir = path.join(repo, "complex_benchmark/adobe_only/audit/2026-09-15");
const indexPath = path.join(auditDir, "S3_ASSET_INDEX_V3_1.json");
const index = JSON.parse(fs.readFileSync(indexPath, "utf8"));
const specs = JSON.parse(fs.readFileSync(path.join(repo, "complex_benchmark/adobe_only/TASKS_V3_ALL100.json"), "utf8"));
const specByCode = new Map(specs.map((spec) => [spec.task_code, spec]));
const baseArgs = ["--region", index.region, "--profile", profile];
const csvCell = (value) => `"${String(value ?? "").replaceAll('"', '""')}"`;

function aws(args, options = {}) {
  const result = spawnSync(awsCli, [...args, ...baseArgs], { encoding: "utf8", maxBuffer: 128 * 1024 * 1024, ...options });
  if (result.status !== 0) throw new Error((result.stderr || result.stdout || `AWS command failed: ${args.join(" ")}`).trim());
  return (result.stdout || "").trim();
}

aws(["sts", "get-caller-identity", "--output", "json"]);

for (const task of index.tasks) {
  const spec = specByCode.get(task.task_code);
  if (!spec) throw new Error(`Missing task specification for ${task.task_code}`);
  const sourceAssets = path.join(repo, "input_assets_v3", task.legacy_id, "assets");
  const destination = `${task.s3_prefix}assets/`;
  aws(["s3", "sync", sourceAssets, destination, "--only-show-errors", "--no-progress"]);
  aws(["s3", "cp", path.join(repo, "complex_benchmark/adobe_only/specs_v3", `${task.legacy_id}.json`), `${task.s3_prefix}metadata/task_spec.json`, "--only-show-errors", "--no-progress"]);
  aws(["s3", "cp", path.join(repo, "input_assets_v3", task.legacy_id, "manifest.json"), `${task.s3_prefix}metadata/source_manifest.json`, "--only-show-errors", "--no-progress"]);
  process.stdout.write(`Uploaded ${task.task_code} (${task.asset_count} assets)\n`);
}

const indexPrefix = `s3://${index.bucket}/${index.root_prefix}/index/`;
for (const filename of [
  "TASK_NAMING_REGISTRY_V3_1.csv",
  "TASK_NAMING_REGISTRY_V3_1.json",
  "S3_ASSET_INDEX_V3_1.csv",
  "S3_ASSET_INDEX_V3_1.json",
  "FREEZE_MANIFEST_V3.json",
  "SPEC_VALIDATION_V3_1.json",
  "ASSET_VALIDATION_V3.json",
]) {
  aws(["s3", "cp", path.join(auditDir, filename), `${indexPrefix}${filename}`, "--only-show-errors", "--no-progress"]);
}

const listingText = aws(["s3api", "list-objects-v2", "--bucket", index.bucket, "--prefix", `${index.root_prefix}/tasks/`, "--output", "json"]);
const listing = JSON.parse(listingText);
const remoteAssets = new Map((listing.Contents || []).filter((item) => item.Key.includes("/assets/")).map((item) => [item.Key, item.Size]));
const missing = [];
const wrongSize = [];
for (const asset of index.assets) {
  if (!remoteAssets.has(asset.s3_key)) missing.push(asset.s3_key);
  else if (remoteAssets.get(asset.s3_key) !== asset.bytes) wrongSize.push({ key: asset.s3_key, expected: asset.bytes, actual: remoteAssets.get(asset.s3_key) });
}
const unexpected = [...remoteAssets.keys()].filter((key) => !index.assets.some((asset) => asset.s3_key === key));
const verification = {
  verified_at: new Date().toISOString(),
  status: missing.length || wrongSize.length || unexpected.length ? "FAIL" : "PASS",
  expected_asset_count: index.asset_count,
  remote_asset_count: remoteAssets.size,
  expected_asset_bytes: index.asset_bytes,
  remote_asset_bytes: [...remoteAssets.values()].reduce((sum, bytes) => sum + bytes, 0),
  missing,
  wrong_size: wrongSize,
  unexpected,
};
fs.writeFileSync(path.join(auditDir, "S3_UPLOAD_VERIFICATION_V3_1.json"), `${JSON.stringify(verification, null, 2)}\n`);
if (verification.status !== "PASS") throw new Error(`S3 verification failed: ${JSON.stringify(verification)}`);

for (const task of index.tasks) task.upload_status = "verified";
for (const asset of index.assets) asset.upload_status = "verified";
index.upload_status = "verified";
fs.writeFileSync(indexPath, `${JSON.stringify(index, null, 2)}\n`);
const assetHeaders = Object.keys(index.assets[0]);
const assetCsv = [assetHeaders.map(csvCell).join(","), ...index.assets.map((row) => assetHeaders.map((header) => csvCell(row[header])).join(","))].join("\n");
fs.writeFileSync(path.join(auditDir, "S3_ASSET_INDEX_V3_1.csv"), `${assetCsv}\n`);
for (const filename of ["S3_ASSET_INDEX_V3_1.csv", "S3_ASSET_INDEX_V3_1.json", "S3_UPLOAD_VERIFICATION_V3_1.json"]) {
  aws(["s3", "cp", path.join(auditDir, filename), `${indexPrefix}${filename}`, "--only-show-errors", "--no-progress"]);
}

console.log(JSON.stringify(verification, null, 2));
