#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const repo = path.resolve(process.argv[2] || path.join(path.dirname(new URL(import.meta.url).pathname), "../../../.."));
const auditDir = path.join(repo, "complex_benchmark/adobe_only/audit/2026-09-15");
const bucket = "annotationprod";
const region = "ap-south-1";
const rootPrefix = "creative-ai-benchmark/v3.1";
const uploadStatus = process.argv[3] || "pending_authentication";

const specs = JSON.parse(fs.readFileSync(path.join(repo, "complex_benchmark/adobe_only/TASKS_V3_ALL100.json"), "utf8"));
const freeze = JSON.parse(fs.readFileSync(path.join(auditDir, "FREEZE_MANIFEST_V3.json"), "utf8"));
const specByLegacyId = new Map(specs.map((spec) => [spec.new_id, spec]));

const encodeKey = (key) => key.split("/").map(encodeURIComponent).join("/");
const csvCell = (value) => `"${String(value ?? "").replaceAll('"', '""')}"`;
const typeFor = (filename) => {
  const ext = path.extname(filename).slice(1).toLowerCase();
  if (["jpg", "jpeg", "png", "webp", "gif", "tif", "tiff"].includes(ext)) return "image";
  if (["mp4", "mov", "m4v", "avi", "webm", "mkv"].includes(ext)) return "video";
  if (["wav", "mp3", "m4a", "aac", "flac"].includes(ext)) return "audio";
  if (ext === "pdf") return "pdf";
  if (["csv", "json", "txt"].includes(ext)) return ext;
  return ext || "file";
};

const assets = [];
const tasks = [];
for (const frozenTask of freeze.tasks) {
  const spec = specByLegacyId.get(frozenTask.task_id);
  if (!spec) throw new Error(`Missing specification for ${frozenTask.task_id}`);
  const taskPrefix = `${rootPrefix}/tasks/${spec.storage.folder}`;
  const taskAssets = frozenTask.assets.map((asset, index) => {
    const key = `${taskPrefix}/assets/${asset.filename}`;
    const row = {
      task_code: spec.task_code,
      task_name: spec.task_name,
      global_order: spec.global_order,
      family: spec.family,
      legacy_id: spec.new_id,
      asset_number: index + 1,
      filename: asset.filename,
      asset_type: typeFor(asset.filename),
      bytes: asset.bytes,
      sha256: asset.sha256,
      s3_key: key,
      s3_uri: `s3://${bucket}/${key}`,
      https_url: `https://${bucket}.s3.${region}.amazonaws.com/${encodeKey(key)}`,
      console_url: `https://${region}.console.aws.amazon.com/s3/object/${bucket}?region=${region}&prefix=${encodeURIComponent(key)}`,
      upload_status: uploadStatus,
    };
    assets.push(row);
    return row;
  });
  tasks.push({
    task_code: spec.task_code,
    task_name: spec.task_name,
    global_order: spec.global_order,
    family: spec.family,
    legacy_id: spec.new_id,
    storage_folder: spec.storage.folder,
    s3_prefix: `s3://${bucket}/${taskPrefix}/`,
    console_url: `https://${region}.console.aws.amazon.com/s3/buckets/${bucket}?region=${region}&prefix=${encodeURIComponent(`${taskPrefix}/`)}&showversions=false`,
    asset_count: taskAssets.length,
    asset_bytes: taskAssets.reduce((sum, asset) => sum + asset.bytes, 0),
    upload_status: uploadStatus,
  });
}

tasks.sort((a, b) => a.global_order - b.global_order);
assets.sort((a, b) => a.global_order - b.global_order || a.asset_number - b.asset_number);

const report = {
  schema_version: "1.0",
  generated_at: "2026-09-15",
  bucket,
  region,
  root_prefix: rootPrefix,
  upload_status: uploadStatus,
  task_count: tasks.length,
  asset_count: assets.length,
  asset_bytes: assets.reduce((sum, asset) => sum + asset.bytes, 0),
  corpus_fingerprint_sha256: freeze.corpus_fingerprint_sha256,
  tasks,
  assets,
};

fs.writeFileSync(path.join(auditDir, "S3_ASSET_INDEX_V3_1.json"), `${JSON.stringify(report, null, 2)}\n`);
const headers = Object.keys(assets[0]);
const csv = [headers.map(csvCell).join(","), ...assets.map((row) => headers.map((header) => csvCell(row[header])).join(","))].join("\n");
fs.writeFileSync(path.join(auditDir, "S3_ASSET_INDEX_V3_1.csv"), `${csv}\n`);

console.log(JSON.stringify({
  task_count: report.task_count,
  asset_count: report.asset_count,
  asset_bytes: report.asset_bytes,
  upload_status: report.upload_status,
  root: `s3://${bucket}/${rootPrefix}/`,
}, null, 2));
