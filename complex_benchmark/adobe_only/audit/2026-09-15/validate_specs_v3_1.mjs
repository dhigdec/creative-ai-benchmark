import fs from "node:fs";
import path from "node:path";

const repo = process.argv[2];
if (!repo) throw new Error("Usage: node validate_specs_v3_1.mjs <repo-root>");

const specsDir = path.join(repo, "complex_benchmark/adobe_only/specs_v3");
const files = fs.readdirSync(specsDir).filter((name) => name.endsWith(".json")).sort();
const specs = files.map((name) => JSON.parse(fs.readFileSync(path.join(specsDir, name), "utf8")));
const errors = [];
const warnings = [];
const addError = (id, text) => errors.push(`${id}: ${text}`);

if (specs.length !== 100) addError("CORPUS", `expected 100 tasks, found ${specs.length}`);

const tierCounts = {};
const familyCounts = {};
const opCounts = {};
const toolInventory = JSON.parse(fs.readFileSync(path.join(repo, "complex_benchmark/adobe_only/audit/2026-09-15/ADOBE_CHATGPT_TOOL_INVENTORY_2026-09-15.json"), "utf8"));
const allowedTools = new Set(toolInventory.tools);
const deliverableNames = new Map();
const marketplaceTitles = new Map();
const bannedClientTerms = /export_html_to_express|html_export_readiness_skill|create_visual_design_express_skill|find_fonts|get_fontkit_embed_url|image_vectorize|video_render|asset_search/i;
const processPattern = /tradeoff|tool response|connector response|success message|returned field|raw response/i;

for (const spec of specs) {
  const id = spec.new_id;
  tierCounts[spec.complexity_tier] = (tierCounts[spec.complexity_tier] || 0) + 1;
  familyCounts[spec.family] = (familyCounts[spec.family] || 0) + 1;
  if (spec.schema_version !== "3.1") addError(id, "schema_version is not 3.1");
  if (!spec.marketplace_listing?.title || spec.marketplace_listing.title.length > 120) addError(id, "marketplace title missing or too long");
  const marketplaceTitle = (spec.marketplace_listing?.title || "").toLowerCase();
  if (!marketplaceTitles.has(marketplaceTitle)) marketplaceTitles.set(marketplaceTitle, []);
  marketplaceTitles.get(marketplaceTitle).push(id);
  const words = spec.client_brief.trim().split(/\s+/).length;
  if (words < 180 || words > 760) addError(id, `client brief has ${words} words; expected 180-760`);
  if (bannedClientTerms.test(spec.client_brief)) addError(id, "client brief leaks connector implementation language");
  if (!spec.asset_readiness || spec.asset_readiness.physical_file_count < 1) addError(id, "asset readiness missing or empty");
  if (!Array.isArray(spec.asset_use_plan) || spec.asset_use_plan.length !== spec.assets_supplied.length) addError(id, "asset use plan does not cover every supplied asset group");
  if (!spec.asset_use_plan?.some((asset) => asset.expected_role === "production_input")) addError(id, "asset use plan has no production input");
  if (!Array.isArray(spec.truth_constraints) || spec.truth_constraints.length < 4) addError(id, "truth constraints incomplete");
  if (!Array.isArray(spec.allowed_exception_states) || spec.allowed_exception_states.length < 3) addError(id, "allowed exception states incomplete");
  if (!Array.isArray(spec.deliverables) || spec.deliverables.length < 2 || spec.deliverables.length > 5) addError(id, `invalid deliverable count ${spec.deliverables?.length}`);
  const max = spec.complexity_tier.startsWith("Flagship") ? 5 : spec.complexity_tier.startsWith("Expert") ? 4 : 3;
  if (spec.deliverables.length > max) addError(id, `tier allows at most ${max} deliverables`);
  if (spec.complexity_tier.startsWith("Flagship") && spec.deliverables.length < 3) addError(id, "flagship engagement requires at least three linked deliverables");
  for (const d of spec.deliverables) {
    if (!d.name || !d.spec || !d.deliverable_class) addError(id, "deliverable missing name, class, or spec");
    const key = d.name.toLowerCase();
    if (!deliverableNames.has(key)) deliverableNames.set(key, []);
    deliverableNames.get(key).push(id);
  }
  if (!spec.verifier_contract || spec.verifier_contract.artifact_checks.length < 3 || spec.verifier_contract.human_craft_checks.length < 3) addError(id, "verifier contract incomplete");
  for (const check of spec.verifier_contract.artifact_checks) if (processPattern.test(`${check.text} ${check.how}`)) addError(id, `artifact check ${check.id} depends on process evidence`);
  const profile = spec.connector_profile;
  if (!profile || profile.autonomy?.startsWith("zero-human") !== true) addError(id, "zero-human connector profile missing");
  for (const tool of [...(profile.required_operations || []), ...(profile.conditional_operations || []), ...(profile.transport_and_inspection_helpers || [])]) {
    if (!allowedTools.has(tool)) addError(id, `unknown current-host tool ${tool}`);
    opCounts[tool] = (opCounts[tool] || 0) + 1;
  }
  if (id.startsWith("VECTOR") && !spec.truth_constraints.some((line) => /inspectable path evidence/.test(line))) addError(id, "vector task lacks path-evidence constraint");
  if (id.startsWith("MOTION")) {
    const metadataPath = path.join(repo, "input_assets_v3", id, "assets/motion_source_metadata.json");
    if (!fs.existsSync(metadataPath)) addError(id, "motion source metadata missing");
    if (!spec.truth_constraints.some((line) => /measured file duration/.test(line))) addError(id, "motion task lacks measured-duration truth rule");
    const fact = fs.existsSync(metadataPath) ? JSON.parse(fs.readFileSync(metadataPath, "utf8")) : null;
    if (fact && spec.asset_readiness.motion_truth.total_video_seconds !== fact.summary.total_video_seconds) addError(id, "motion facts differ from canonical metadata");
    if ((profile.required_operations || []).includes("video_create_quick_cut") && /speech|claim|dialogue|transcript|spoken/.test(spec.primary_craft_problem)) addError(id, "Quick Cut is assigned to a semantic edit");
  }
}

for (const [name, ids] of deliverableNames) if (ids.length > 1) addError("CORPUS", `duplicate deliverable name '${name}' in ${ids.join(", ")}`);
for (const [title, ids] of marketplaceTitles) if (title && ids.length > 1) addError("CORPUS", `duplicate marketplace title '${title}' in ${ids.join(", ")}`);

const expectedTiers = { "Flagship integrated engagement": 30, "Expert standard engagement": 45, "Specialist stress test": 25 };
for (const [tier, count] of Object.entries(expectedTiers)) if (tierCounts[tier] !== count) addError("CORPUS", `tier ${tier} expected ${count}, found ${tierCounts[tier] || 0}`);

const counts = (tool) => opCounts[tool] || 0;
const bands = {
  asset_license_and_download_stock: [15, 25], boards_create_new_board: [8, 15], image_crop_and_resize: [55, 85],
  image_apply_adjustments: [45, 90], image_remove_background: [15, 30], image_vectorize: [15, 25],
  convert_pdf_to_indd: [18, 34], document_merge_data_layout: [22, 34], search_design: [8, 20],
  font_recommend: [20, 35], video_metadata: [15, 20], video_create_quick_cut: [5, 7], video_render: [12, 18],
  media_enhance_speech: [5, 12], video_resize: [15, 20],
};
for (const [tool, [min, max]] of Object.entries(bands)) {
  const count = counts(tool);
  if (count < min || count > max) addError("DISTRIBUTION", `${tool} expected ${min}-${max} tasks, found ${count}`);
}

const meaningful = Object.keys(opCounts).filter((tool) => !/^adobe_mandatory_init|^asset_(initialize|finalize|inline)/.test(tool));
if (meaningful.length < 45 || meaningful.length > 60) addError("DISTRIBUTION", `expected 45-60 distinct meaningful operations, found ${meaningful.length}`);

const report = {
  generated_at: "2026-09-15",
  status: errors.length ? "FAIL" : "PASS",
  task_count: specs.length,
  tier_counts: tierCounts,
  family_counts: familyCounts,
  distinct_meaningful_operations: meaningful.length,
  operation_counts: Object.fromEntries(Object.entries(opCounts).sort((a, b) => a[0].localeCompare(b[0]))),
  exact_duplicate_deliverable_names: [...deliverableNames.entries()].filter(([, ids]) => ids.length > 1).map(([name, ids]) => ({ name, ids })),
  exact_duplicate_marketplace_titles: [...marketplaceTitles.entries()].filter(([, ids]) => ids.length > 1).map(([title, ids]) => ({ title, ids })),
  errors,
  warnings,
};
const outPath = path.join(repo, "complex_benchmark/adobe_only/audit/2026-09-15/SPEC_VALIDATION_V3_1.json");
fs.writeFileSync(outPath, `${JSON.stringify(report, null, 2)}\n`);
console.log(JSON.stringify(report, null, 2));
if (errors.length) process.exit(1);
