#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";

const OUT = path.dirname(new URL(import.meta.url).pathname);
const PROJECT = path.resolve(process.argv[2] || path.join(OUT, "../../../.."));
const ROOT = path.join(PROJECT, "input_assets_v3");

const IMAGE_EXTS = new Set(["jpg", "jpeg", "png", "webp", "gif", "tif", "tiff"]);
const MEDIA_EXTS = new Set(["mp4", "mov", "m4v", "avi", "webm", "mkv", "wav", "mp3", "m4a", "aac", "flac"]);

function run(command, args) {
  const result = spawnSync(command, args, { encoding: "utf8", maxBuffer: 32 * 1024 * 1024 });
  return {
    ok: result.status === 0,
    stdout: (result.stdout || "").trim(),
    stderr: (result.stderr || "").trim(),
    status: result.status
  };
}

function sha256(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const c = text[i];
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') {
        field += '"';
        i += 1;
      } else if (c === '"') {
        quoted = false;
      } else {
        field += c;
      }
    } else if (c === '"') {
      quoted = true;
    } else if (c === ",") {
      row.push(field);
      field = "";
    } else if (c === "\n") {
      row.push(field.replace(/\r$/, ""));
      rows.push(row);
      row = [];
      field = "";
    } else {
      field += c;
    }
  }
  if (quoted) throw new Error("unterminated quoted field");
  if (field.length || row.length) {
    row.push(field.replace(/\r$/, ""));
    rows.push(row);
  }
  return rows;
}

function inspectImage(file) {
  const result = run("identify", ["-quiet", "-format", "%m\t%w\t%h\t%z\t%[colorspace]", `${file}[0]`]);
  if (!result.ok) return { ok: false, error: result.stderr || result.stdout || "identify failed" };
  const [format, width, height, depth, colorspace] = result.stdout.split("\t");
  return { ok: true, format, width: Number(width), height: Number(height), depth: Number(depth), colorspace };
}

function inspectMedia(file) {
  const result = run("ffprobe", ["-v", "error", "-show_entries", "format=duration,format_name:stream=index,codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels", "-of", "json", file]);
  if (!result.ok) return { ok: false, error: result.stderr || result.stdout || "ffprobe failed" };
  try {
    const parsed = JSON.parse(result.stdout);
    if (!parsed.streams?.length) return { ok: false, error: "no decodable media streams" };
    return { ok: true, ...parsed };
  } catch (error) {
    return { ok: false, error: `invalid ffprobe JSON: ${error.message}` };
  }
}

function inspectPdf(file) {
  const result = run("pdfinfo", [file]);
  if (!result.ok) return { ok: false, error: result.stderr || result.stdout || "pdfinfo failed" };
  const info = {};
  for (const line of result.stdout.split("\n")) {
    const match = line.match(/^([^:]+):\s*(.*)$/);
    if (match) info[match[1].trim()] = match[2].trim();
  }
  const pages = Number(info.Pages || 0);
  return pages > 0 ? { ok: true, pages, page_size: info["Page size"], version: info["PDF version"] } : { ok: false, error: "PDF has no pages" };
}

const tasks = fs.readdirSync(ROOT).filter((name) => fs.statSync(path.join(ROOT, name)).isDirectory()).sort();
const rows = [];
const issues = [];
const taskSummaries = [];

for (const taskId of tasks) {
  const taskDir = path.join(ROOT, taskId);
  const manifestPath = path.join(taskDir, "manifest.json");
  const assetsDir = path.join(taskDir, "assets");
  let manifest;
  try {
    manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  } catch (error) {
    issues.push({ task_id: taskId, code: "manifest-invalid", detail: error.message });
    continue;
  }
  if (manifest.task_id !== taskId) issues.push({ task_id: taskId, code: "manifest-task-mismatch", detail: manifest.task_id });
  const listed = new Set((manifest.assets || []).map((asset) => asset.filename));
  const actual = fs.existsSync(assetsDir)
    ? fs.readdirSync(assetsDir).filter((name) => fs.statSync(path.join(assetsDir, name)).isFile()).sort()
    : [];
  for (const filename of actual) {
    if (!listed.has(filename)) issues.push({ task_id: taskId, filename, code: "unmanifested-file" });
  }
  let validCount = 0;
  for (const asset of manifest.assets || []) {
    const filename = asset.filename;
    const file = path.join(assetsDir, filename);
    const ext = path.extname(filename).slice(1).toLowerCase();
    const base = { task_id: taskId, filename, declared_type: asset.type || "", ext, bytes: 0, sha256: "", inspection: null };
    if (!fs.existsSync(file)) {
      issues.push({ task_id: taskId, filename, code: "missing-file" });
      rows.push(base);
      continue;
    }
    const stat = fs.statSync(file);
    base.bytes = stat.size;
    if (!stat.size) {
      issues.push({ task_id: taskId, filename, code: "empty-file" });
      rows.push(base);
      continue;
    }
    base.sha256 = sha256(file);
    if (IMAGE_EXTS.has(ext)) {
      base.inspection = inspectImage(file);
      if (base.inspection.ok && Array.isArray(asset.target_px) && asset.target_px.length === 2) {
        const [expectedW, expectedH] = asset.target_px.map(Number);
        if (base.inspection.width !== expectedW || base.inspection.height !== expectedH) {
          issues.push({ task_id: taskId, filename, code: "target-dimension-mismatch", detail: `${base.inspection.width}x${base.inspection.height} != ${expectedW}x${expectedH}` });
        }
      }
    } else if (MEDIA_EXTS.has(ext)) {
      base.inspection = inspectMedia(file);
    } else if (ext === "pdf") {
      base.inspection = inspectPdf(file);
    } else if (ext === "json") {
      try {
        JSON.parse(fs.readFileSync(file, "utf8"));
        base.inspection = { ok: true };
      } catch (error) {
        base.inspection = { ok: false, error: error.message };
      }
    } else if (ext === "csv") {
      try {
        const csvRows = parseCsv(fs.readFileSync(file, "utf8"));
        const width = csvRows[0]?.length || 0;
        const ragged = csvRows.map((r, index) => ({ index: index + 1, width: r.length })).filter((r) => r.width !== width);
        const headers = csvRows[0] || [];
        const duplicateHeaders = headers.filter((h, index) => headers.indexOf(h) !== index);
        base.inspection = { ok: csvRows.length >= 2 && width > 0 && !ragged.length, rows: Math.max(0, csvRows.length - 1), columns: width, duplicate_headers: [...new Set(duplicateHeaders)], ragged_rows: ragged };
      } catch (error) {
        base.inspection = { ok: false, error: error.message };
      }
    } else {
      const fileResult = run("file", ["-b", file]);
      base.inspection = { ok: fileResult.ok, description: fileResult.stdout, error: fileResult.stderr || undefined };
    }
    if (!base.inspection?.ok) {
      issues.push({ task_id: taskId, filename, code: "decode-failed", detail: base.inspection?.error || "inspection failed" });
    } else {
      validCount += 1;
    }
    rows.push(base);
  }
  taskSummaries.push({ task_id: taskId, manifest_assets: listed.size, actual_assets: actual.length, valid_assets: validCount });
}

const report = {
  generated_at: new Date().toISOString(),
  project: PROJECT,
  task_count: taskSummaries.length,
  asset_count: rows.length,
  valid_asset_count: rows.filter((r) => r.inspection?.ok).length,
  issue_count: issues.length,
  issues,
  tasks: taskSummaries,
  assets: rows
};

fs.writeFileSync(path.join(OUT, "ASSET_VALIDATION_V3.json"), `${JSON.stringify(report, null, 2)}\n`);
const summary = [
  "# StudioBench V3 Asset Validation",
  "",
  `Generated: ${report.generated_at}`,
  "",
  `- Tasks: ${report.task_count}`,
  `- Manifest entries checked: ${report.asset_count}`,
  `- Decodable/valid files: ${report.valid_asset_count}`,
  `- Issues: ${report.issue_count}`,
  "",
  "## Issues",
  "",
  ...(issues.length ? issues.map((issue) => `- ${issue.task_id}/${issue.filename || "manifest"}: ${issue.code}${issue.detail ? ` (${issue.detail})` : ""}`) : ["- None"]),
  ""
].join("\n");
fs.writeFileSync(path.join(OUT, "ASSET_VALIDATION_V3.md"), summary);

console.log(JSON.stringify({
  task_count: report.task_count,
  asset_count: report.asset_count,
  valid_asset_count: report.valid_asset_count,
  issue_count: report.issue_count,
  issues: issues.slice(0, 25)
}, null, 2));
