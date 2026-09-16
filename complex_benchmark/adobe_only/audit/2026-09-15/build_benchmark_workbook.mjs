#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const repo = path.resolve(process.argv[2]);
const outputDir = path.resolve(process.argv[3]);
const auditDir = path.join(repo, "complex_benchmark/adobe_only/audit/2026-09-15");
const specs = JSON.parse(await fs.readFile(path.join(repo, "complex_benchmark/adobe_only/TASKS_V3_ALL100.json"), "utf8")).sort((a, b) => a.global_order - b.global_order);
const s3Index = JSON.parse(await fs.readFile(path.join(auditDir, "S3_ASSET_INDEX_V3_1.json"), "utf8"));
if (process.env.STUDIOBENCH_S3_VERIFIED === "1") {
  s3Index.upload_status = "verified";
  for (const task of s3Index.tasks) task.upload_status = "verified";
  for (const asset of s3Index.assets) asset.upload_status = "verified";
}
const validation = JSON.parse(await fs.readFile(path.join(auditDir, "SPEC_VALIDATION_V3_1.json"), "utf8"));
const assetValidation = JSON.parse(await fs.readFile(path.join(auditDir, "ASSET_VALIDATION_V3.json"), "utf8"));
const s3TaskByCode = new Map(s3Index.tasks.map((task) => [task.task_code, task]));

const workbook = Workbook.create();
const font = "Arial";
const colors = {
  ink: "#1F2937",
  green: "#0F766E",
  greenLight: "#D1FAE5",
  blue: "#1D4ED8",
  blueLight: "#DBEAFE",
  orange: "#C2410C",
  orangeLight: "#FFEDD5",
  violet: "#6D28D9",
  violetLight: "#EDE9FE",
  red: "#B91C1C",
  redLight: "#FEE2E2",
  gray: "#F3F4F6",
  line: "#D1D5DB",
  white: "#FFFFFF",
};

function colName(index) {
  let n = index;
  let result = "";
  while (n > 0) {
    n -= 1;
    result = String.fromCharCode(65 + (n % 26)) + result;
    n = Math.floor(n / 26);
  }
  return result;
}

function addTitle(sheet, title, subtitle, columns, color = colors.ink) {
  const last = colName(columns);
  sheet.mergeCells(`A1:${last}1`);
  sheet.getRange("A1").values = [[title]];
  sheet.getRange(`A1:${last}1`).format = {
    fill: color,
    font: { name: font, size: 18, bold: true, color: colors.white },
    verticalAlignment: "center",
  };
  sheet.getRange(`A1:${last}1`).format.rowHeightPx = 38;
  sheet.mergeCells(`A2:${last}2`);
  sheet.getRange("A2").values = [[subtitle]];
  sheet.getRange(`A2:${last}2`).format = {
    fill: colors.gray,
    font: { name: font, size: 10, color: colors.ink },
    verticalAlignment: "center",
    wrapText: true,
  };
  sheet.getRange(`A2:${last}2`).format.rowHeightPx = 32;
  sheet.showGridLines = false;
}

function addDataTable(sheet, headers, rows, tableName, startRow = 4) {
  const lastCol = colName(headers.length);
  const endRow = startRow + rows.length;
  const range = sheet.getRange(`A${startRow}:${lastCol}${endRow}`);
  range.values = [headers, ...rows];
  range.format.font = { name: font, size: 10, color: colors.ink };
  range.format.verticalAlignment = "top";
  range.format.borders = { preset: "all", style: "thin", color: colors.line };
  const table = sheet.tables.add(`A${startRow}:${lastCol}${endRow}`, true, tableName);
  table.style = "TableStyleMedium2";
  table.showFilterButton = true;
  sheet.freezePanes.freezeRows(startRow);
  return { startRow, endRow, lastCol };
}

function setColumnWidths(sheet, widths, endRow) {
  widths.forEach((width, index) => {
    const col = colName(index + 1);
    sheet.getRange(`${col}1:${col}${endRow}`).format.columnWidthPx = width;
  });
}

const overview = workbook.worksheets.add("Overview");
overview.tabColor = colors.green;
addTitle(overview, "Creative AI Benchmark Task Catalog", "Canonical task registry, briefs, deliverables, auto and human verifiers, and S3 asset publication status", 8, colors.ink);
overview.getRange("A4:H4").values = [["Upload status", s3Index.upload_status, "Tasks", specs.length, "Assets", s3Index.asset_count, "Corpus fingerprint", s3Index.corpus_fingerprint_sha256]];
overview.getRange("A4:H4").format = { fill: colors.gray, font: { name: font, size: 10, bold: true, color: colors.ink }, wrapText: true, verticalAlignment: "center", borders: { preset: "all", style: "thin", color: colors.line } };
overview.getRange("B4").format.fill = s3Index.upload_status === "verified" ? colors.greenLight : colors.orangeLight;
overview.getRange("A6:F6").values = [["Family", "Tasks", "Deliverables", "Assets", "Auto verifiers", "Human verifiers"]];
overview.getRange("A6:F6").format = { fill: colors.green, font: { name: font, size: 10, bold: true, color: colors.white }, borders: { preset: "all", style: "thin", color: colors.line } };
const familyNames = ["Photo & Image", "Vector & Print", "Layout & Data", "Motion & Audio"];
const familySummary = familyNames.map((family) => {
  const familySpecs = specs.filter((spec) => spec.family === family);
  return [
    family,
    familySpecs.length,
    familySpecs.reduce((sum, spec) => sum + spec.deliverables.length, 0),
    familySpecs.reduce((sum, spec) => sum + s3TaskByCode.get(spec.task_code).asset_count, 0),
    familySpecs.reduce((sum, spec) => sum + spec.verifiers_auto.length + spec.verifiers_process.length, 0),
    familySpecs.reduce((sum, spec) => sum + spec.verifiers_human.length, 0),
  ];
});
overview.getRange("A7:F10").values = familySummary;
overview.getRange("A11:F11").values = [["Total", ...familySummary[0].slice(1).map((_, index) => familySummary.reduce((sum, row) => sum + row[index + 1], 0))]];
overview.getRange("A7:F11").format = { font: { name: font, size: 10, color: colors.ink }, borders: { preset: "all", style: "thin", color: colors.line } };
overview.getRange("A11:F11").format = { fill: colors.gray, font: { name: font, size: 10, bold: true, color: colors.ink }, borders: { preset: "all", style: "thin", color: colors.line } };
overview.getRange("A13:B17").values = [
  ["Publication field", "Value"],
  ["S3 root", `s3://${s3Index.bucket}/${s3Index.root_prefix}/`],
  ["AWS region", s3Index.region],
  ["Specification validation", `${validation.status}; ${validation.errors.length} errors; ${validation.warnings.length} warnings`],
  ["Asset validation", `${assetValidation.valid_asset_count} of ${assetValidation.asset_count} valid; ${assetValidation.issue_count} issues`],
];
overview.getRange("A13:B13").format = { fill: colors.orange, font: { name: font, size: 10, bold: true, color: colors.white } };
overview.getRange("A13:B17").format.borders = { preset: "all", style: "thin", color: colors.line };
overview.getRange("A13:B17").format.wrapText = true;
overview.getRange("A13:B17").format.font = { name: font, size: 10, color: colors.ink };
overview.getRange("A13:B13").format.font = { name: font, size: 10, bold: true, color: colors.white };
setColumnWidths(overview, [200, 170, 105, 110, 120, 115, 115, 260], 17);
overview.freezePanes.freezeRows(2);

const register = workbook.worksheets.add("Task Register");
register.tabColor = colors.green;
addTitle(register, "Task Register", "SB3 codes are the primary references; legacy IDs remain for source and historical-run traceability", 14, colors.green);
const registerHeaders = ["Task code", "Task name", "Family", "Legacy ID", "Marketplace title", "Budget", "Revision structure", "Deliverables", "Assets", "Auto verifiers", "Human verifiers", "S3 prefix", "S3 console", "Upload status"];
const registerRows = specs.map((spec) => {
  const task = s3TaskByCode.get(spec.task_code);
  return [spec.task_code, spec.task_name, spec.family, spec.new_id, spec.marketplace_listing.title, spec.project_terms.modeled_marketplace_budget, spec.project_terms.revision_structure, spec.deliverables.length, task.asset_count, spec.verifiers_auto.length + spec.verifiers_process.length, spec.verifiers_human.length, task.s3_prefix, task.console_url, task.upload_status];
});
addDataTable(register, registerHeaders, registerRows, "TaskRegisterTable");
register.getRange("H5:K104").format.numberFormat = "#,##0";
register.getRange("A5:N104").format.rowHeightPx = 34;
register.getRange("B5:G104").format.wrapText = true;
register.getRange("L5:N104").format.wrapText = true;
setColumnWidths(register, [115, 310, 125, 85, 310, 125, 290, 85, 70, 105, 110, 420, 260, 150], 104);

const brandSheet = workbook.worksheets.add("Brand Identity");
brandSheet.tabColor = colors.violet;
addTitle(brandSheet, "Brand Identity", "One complete written brand reference per task, including positioning, audience, palette, typography, voice, values, and the status of supplied brand assets", 16, colors.violet);
const brandRows = specs.map((spec) => {
  const brand = spec.brand_identity;
  return [
    spec.task_code,
    spec.task_name,
    spec.family,
    brand.brand_name,
    brand.tagline,
    brand.sector,
    brand.founded_place_size,
    brand.about,
    brand.audience,
    brand.price_positioning,
    brand.personality.join(", "),
    brand.palette.map((color) => `${color.name} ${color.hex}`).join("\n"),
    brand.typography,
    brand.voice,
    brand.values,
    brand.brand_assets_status,
  ];
});
const brandInfo = addDataTable(brandSheet, ["Task code", "Task name", "Family", "Brand", "Tagline", "Sector", "Founded / place / size", "About", "Audience", "Price positioning", "Personality", "Palette", "Typography", "Voice", "Values", "Brand assets status"], brandRows, "BrandIdentityTable");
brandSheet.getRange(`A5:P${brandInfo.endRow}`).format.rowHeightPx = 96;
brandSheet.getRange(`B5:P${brandInfo.endRow}`).format.wrapText = true;
setColumnWidths(brandSheet, [115, 300, 125, 190, 230, 330, 340, 560, 420, 440, 240, 230, 500, 450, 420, 560], brandInfo.endRow);

const familyConfig = [
  ["Photo Tasks", "Photo & Image", colors.blue, colors.blueLight],
  ["Vector Tasks", "Vector & Print", colors.orange, colors.orangeLight],
  ["Layout Tasks", "Layout & Data", colors.violet, colors.violetLight],
  ["Motion Tasks", "Motion & Audio", colors.red, colors.redLight],
];
for (const [sheetName, family, tabColor] of familyConfig) {
  const sheet = workbook.worksheets.add(sheetName);
  sheet.tabColor = tabColor;
  const familySpecs = specs.filter((spec) => spec.family === family);
  addTitle(sheet, `${family} Briefs`, "Each row contains the full client brief, scoped deliverables, auto and human verifiers, and task-level S3 folder", 8, tabColor);
  const headers = ["Task code", "Task name", "Client brief", "Deliverables", "Auto verifiers", "Human verifiers", "Assets", "S3 folder"];
  const rows = familySpecs.map((spec) => {
    const task = s3TaskByCode.get(spec.task_code);
    const formatChecks = (checks) => checks.map((check) => `${check.id}. ${check.text}`).join("\n\n");
    return [
      spec.task_code,
      spec.task_name,
      spec.client_brief,
      spec.deliverables.map((deliverable, index) => `${index + 1}. ${deliverable.name}\n${deliverable.spec}`).join("\n\n"),
      formatChecks([...spec.verifiers_auto, ...spec.verifiers_process]),
      formatChecks(spec.verifiers_human),
      task.asset_count,
      task.console_url,
    ];
  });
  const tableInfo = addDataTable(sheet, headers, rows, `${sheetName.replaceAll(" ", "")}Table`);
  sheet.getRange(`A5:H${tableInfo.endRow}`).format.rowHeightPx = 132;
  sheet.getRange(`B5:H${tableInfo.endRow}`).format.wrapText = true;
  setColumnWidths(sheet, [115, 300, 650, 520, 620, 560, 70, 300], tableInfo.endRow);
}

const deliverablesSheet = workbook.worksheets.add("Deliverables");
deliverablesSheet.tabColor = colors.blue;
addTitle(deliverablesSheet, "Deliverables", "One row per scoped creative output; handover requirements are recorded in the task specifications", 7, colors.blue);
const deliverableRows = specs.flatMap((spec) => spec.deliverables.map((deliverable, index) => [spec.task_code, spec.task_name, spec.family, index + 1, deliverable.deliverable_class, deliverable.name, deliverable.spec]));
const deliverableInfo = addDataTable(deliverablesSheet, ["Task code", "Task name", "Family", "Sequence", "Deliverable class", "Deliverable", "Specification"], deliverableRows, "DeliverablesTable");
deliverablesSheet.getRange(`A5:G${deliverableInfo.endRow}`).format.rowHeightPx = 70;
deliverablesSheet.getRange(`B5:G${deliverableInfo.endRow}`).format.wrapText = true;
setColumnWidths(deliverablesSheet, [115, 300, 125, 75, 160, 340, 720], deliverableInfo.endRow);

const verifiersSheet = workbook.worksheets.add("Verifiers");
verifiersSheet.tabColor = colors.orange;
addTitle(verifiersSheet, "Verifier Register", "Auto verifiers combine artifact and normalized process checks; human verifiers judge professional craft", 6, colors.orange);
const verifierRows = [];
for (const spec of specs) {
  const groups = [
    ["Auto", spec.verifiers_auto, spec.verifier_contract.scoring.artifact_checks],
    ["Auto", spec.verifiers_process, spec.verifier_contract.scoring.normalized_process_quality],
    ["Human", spec.verifiers_human, spec.verifier_contract.scoring.human_craft_review],
  ];
  for (const [category, checks, categoryWeight] of groups) {
    for (const check of checks) verifierRows.push([spec.task_code, spec.task_name, spec.family, category, check.id, check.text]);
  }
}
const verifierInfo = addDataTable(verifiersSheet, ["Task code", "Task name", "Family", "Verifier type", "Verifier ID", "Check"], verifierRows, "VerifiersTable");
verifiersSheet.getRange(`A5:F${verifierInfo.endRow}`).format.rowHeightPx = 58;
verifiersSheet.getRange(`B5:F${verifierInfo.endRow}`).format.wrapText = true;
setColumnWidths(verifiersSheet, [115, 300, 125, 100, 75, 680], verifierInfo.endRow);

const assetsSheet = workbook.worksheets.add("Assets");
assetsSheet.tabColor = colors.red;
addTitle(assetsSheet, "Asset Register", "One row per validated source asset, with deterministic S3, HTTPS, and authenticated AWS console destinations", 12, colors.red);
const assetRows = s3Index.assets.map((asset) => [asset.task_code, asset.task_name, asset.family, asset.asset_number, asset.filename, asset.asset_type, asset.bytes, asset.sha256, asset.s3_uri, asset.https_url, asset.console_url, asset.upload_status]);
const assetInfo = addDataTable(assetsSheet, ["Task code", "Task name", "Family", "Asset #", "Filename", "Type", "Bytes", "SHA-256", "S3 URI", "HTTPS object", "S3 console", "Upload status"], assetRows, "AssetsTable");
assetsSheet.getRange(`D5:G${assetInfo.endRow}`).format.numberFormat = "#,##0";
assetsSheet.getRange(`A5:L${assetInfo.endRow}`).format.rowHeightPx = 26;
assetsSheet.getRange(`B5:L${assetInfo.endRow}`).format.wrapText = true;
setColumnWidths(assetsSheet, [115, 300, 125, 70, 330, 80, 105, 470, 620, 480, 520, 150], assetInfo.endRow);

workbook.recalculate();
const sheetSummary = await workbook.inspect({ kind: "sheet", include: "id,name", maxChars: 5000 });
const formulaErrors = await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options: { useRegex: true, maxResults: 100 }, summary: "final formula error scan", maxChars: 5000 });

await fs.mkdir(outputDir, { recursive: true });
const previewDir = path.join(outputDir, "previews");
await fs.mkdir(previewDir, { recursive: true });
const previewRanges = {
  "Overview": "A1:H17",
  "Task Register": "A1:N22",
  "Brand Identity": "A1:P12",
  "Photo Tasks": "A1:H12",
  "Vector Tasks": "A1:H12",
  "Layout Tasks": "A1:H12",
  "Motion Tasks": "A1:H12",
  "Deliverables": "A1:G20",
  "Verifiers": "A1:F20",
  "Assets": "A1:L24",
};
for (const [sheetName, range] of Object.entries(previewRanges)) {
  const preview = await workbook.render({ sheetName, range, scale: 1, format: "png" });
  await fs.writeFile(path.join(previewDir, `${sheetName.toLowerCase().replaceAll(" ", "-")}.png`), new Uint8Array(await preview.arrayBuffer()));
}

const outputPath = path.join(outputDir, "Creative_AI_Benchmark_Task_Catalog.xlsx");
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
const saved = await FileBlob.load(outputPath);
const reopened = await SpreadsheetFile.importXlsx(saved);
const reopenedSheets = await reopened.inspect({ kind: "sheet", include: "id,name", maxChars: 5000 });
const reopenedErrors = await reopened.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options: { useRegex: true, maxResults: 100 }, summary: "saved workbook formula error scan", maxChars: 5000 });

console.log(JSON.stringify({
  output: outputPath,
  sheets: specs.length ? 10 : 0,
  tasks: specs.length,
  deliverables: deliverableRows.length,
  verifiers: verifierRows.length,
  assets: assetRows.length,
  upload_status: s3Index.upload_status,
  sheet_inspection_chars: sheetSummary.ndjson.length,
  formula_error_scan: formulaErrors.ndjson,
  reopened_sheet_inspection_chars: reopenedSheets.ndjson.length,
  reopened_formula_error_scan: reopenedErrors.ndjson,
}, null, 2));
