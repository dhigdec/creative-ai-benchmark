import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";

const repo = process.argv[2];
if (!repo) throw new Error("Usage: node remediate_specs_v3_1.mjs <repo-root>");

const specsDir = path.join(repo, "complex_benchmark/adobe_only/specs_v3");
const assetsRoot = path.join(repo, "input_assets_v3");
const auditDir = path.join(repo, "complex_benchmark/adobe_only/audit/2026-09-15");
const files = fs.readdirSync(specsDir).filter((name) => name.endsWith(".json")).sort();
let aggregateSource = JSON.parse(fs.readFileSync(path.join(repo, "complex_benchmark/adobe_only/TASKS_V3_ALL100.json"), "utf8"));
if (aggregateSource[0]?.schema_version === "3.1") {
  aggregateSource = JSON.parse(execFileSync("git", ["show", "HEAD:complex_benchmark/adobe_only/TASKS_V3_ALL100.json"], { cwd: repo, encoding: "utf8", maxBuffer: 64 * 1024 * 1024 }));
}
const sourceById = new Map(aggregateSource.map((spec) => [spec.new_id, spec]));

const sets = (text) => new Set(text.trim().split(/\s+/).filter(Boolean));

const flagship = sets(`
  PHOTO-02 PHOTO-04 PHOTO-05 PHOTO-07 PHOTO-09 PHOTO-12 PHOTO-15 PHOTO-17 PHOTO-19 PHOTO-25
  VECTOR-01 VECTOR-05 VECTOR-07 VECTOR-15
  LAYOUT-01 LAYOUT-05 LAYOUT-10 LAYOUT-14 LAYOUT-17 LAYOUT-20 LAYOUT-23 LAYOUT-27 LAYOUT-29 LAYOUT-33 LAYOUT-35
  MOTION-01 MOTION-04 MOTION-08 MOTION-13 MOTION-20
`);

const specialist = sets(`
  PHOTO-03 PHOTO-06 PHOTO-08 PHOTO-10 PHOTO-11 PHOTO-16 PHOTO-18 PHOTO-21 PHOTO-22 PHOTO-24
  VECTOR-03 VECTOR-04 VECTOR-06 VECTOR-12 VECTOR-14
  LAYOUT-07 LAYOUT-15 LAYOUT-21 LAYOUT-25 LAYOUT-28
  MOTION-06 MOTION-09 MOTION-11 MOTION-15 MOTION-19
`);

const dataMerge = sets(`
  LAYOUT-01 LAYOUT-02 LAYOUT-04 LAYOUT-06 LAYOUT-07 LAYOUT-08 LAYOUT-10 LAYOUT-11 LAYOUT-15 LAYOUT-16 LAYOUT-17
  LAYOUT-20 LAYOUT-21 LAYOUT-22 LAYOUT-23 LAYOUT-24 LAYOUT-25 LAYOUT-26 LAYOUT-27 LAYOUT-28 LAYOUT-29 LAYOUT-31 LAYOUT-32 LAYOUT-33 LAYOUT-34 LAYOUT-35
  MOTION-04 MOTION-13 PHOTO-02 PHOTO-17 VECTOR-05 VECTOR-14 VECTOR-15
`);

const express = sets(`
  LAYOUT-01 LAYOUT-03 LAYOUT-05 LAYOUT-09 LAYOUT-12 LAYOUT-13 LAYOUT-14 LAYOUT-18 LAYOUT-19 LAYOUT-20
  PHOTO-11 PHOTO-20 PHOTO-28 VECTOR-07 MOTION-01 MOTION-03 MOTION-11 MOTION-13 MOTION-18 MOTION-20
`);

const stock = sets(`
  LAYOUT-03 LAYOUT-07 LAYOUT-10 LAYOUT-13 LAYOUT-19 LAYOUT-20 LAYOUT-30
  PHOTO-03 PHOTO-04 PHOTO-05 PHOTO-09 PHOTO-16 PHOTO-27 PHOTO-28 PHOTO-29 PHOTO-30
  MOTION-03 MOTION-06 MOTION-14 MOTION-18
`);

const boards = sets(`
  LAYOUT-01 LAYOUT-05 LAYOUT-10 LAYOUT-14 LAYOUT-20
  PHOTO-04 PHOTO-11 PHOTO-20 PHOTO-27 MOTION-03 MOTION-13 VECTOR-07
`);

const acrobat = sets(`
  LAYOUT-01 LAYOUT-07 LAYOUT-10 LAYOUT-14 LAYOUT-20 LAYOUT-22 LAYOUT-25 LAYOUT-26 LAYOUT-27 LAYOUT-35
  PHOTO-03 PHOTO-06 PHOTO-11 PHOTO-16 PHOTO-17 VECTOR-02 VECTOR-05 VECTOR-15 MOTION-10 MOTION-19
`);

const vectorOps = sets(`
  VECTOR-01 VECTOR-02 VECTOR-03 VECTOR-04 VECTOR-05 VECTOR-06 VECTOR-07 VECTOR-08 VECTOR-09 VECTOR-10
  VECTOR-11 VECTOR-12 VECTOR-13 VECTOR-14 VECTOR-15 LAYOUT-02 LAYOUT-10 LAYOUT-14 PHOTO-02 PHOTO-04 PHOTO-05 PHOTO-20 PHOTO-25 MOTION-08 MOTION-14
`);

const cutoutOps = sets(`
  PHOTO-01 PHOTO-05 PHOTO-07 PHOTO-09 PHOTO-10 PHOTO-11 PHOTO-12 PHOTO-13 PHOTO-14 PHOTO-15 PHOTO-16 PHOTO-19 PHOTO-20 PHOTO-22 PHOTO-24 PHOTO-25 PHOTO-26 PHOTO-27 PHOTO-28 PHOTO-29 PHOTO-30
  LAYOUT-02 LAYOUT-03 LAYOUT-04 LAYOUT-05 LAYOUT-17 LAYOUT-18 LAYOUT-19 MOTION-03 MOTION-08 MOTION-11 MOTION-13 VECTOR-04
`);

const imageCrop = sets(`
  PHOTO-01 PHOTO-02 PHOTO-03 PHOTO-04 PHOTO-05 PHOTO-06 PHOTO-07 PHOTO-08 PHOTO-09 PHOTO-10
  PHOTO-11 PHOTO-12 PHOTO-13 PHOTO-14 PHOTO-15 PHOTO-16 PHOTO-17 PHOTO-18 PHOTO-19 PHOTO-20
  PHOTO-21 PHOTO-22 PHOTO-23 PHOTO-24 PHOTO-25 PHOTO-26 PHOTO-27 PHOTO-28 PHOTO-29 PHOTO-30
  VECTOR-01 VECTOR-02 VECTOR-03 VECTOR-04 VECTOR-05 VECTOR-06 VECTOR-07 VECTOR-08 VECTOR-09 VECTOR-10
  VECTOR-11 VECTOR-12 VECTOR-13 VECTOR-14 VECTOR-15
  LAYOUT-01 LAYOUT-03 LAYOUT-05 LAYOUT-06 LAYOUT-07 LAYOUT-10 LAYOUT-14 LAYOUT-17 LAYOUT-19 LAYOUT-20 LAYOUT-23 LAYOUT-27 LAYOUT-29
  MOTION-01 MOTION-03 MOTION-04 MOTION-05 MOTION-08 MOTION-13 MOTION-14 MOTION-17
`);

const imageAdjust = sets(`
  PHOTO-01 PHOTO-02 PHOTO-03 PHOTO-04 PHOTO-05 PHOTO-06 PHOTO-07 PHOTO-08 PHOTO-09 PHOTO-10
  PHOTO-11 PHOTO-12 PHOTO-13 PHOTO-14 PHOTO-15 PHOTO-16 PHOTO-17 PHOTO-18 PHOTO-19 PHOTO-20
  PHOTO-21 PHOTO-22 PHOTO-23 PHOTO-24 PHOTO-25 PHOTO-26 PHOTO-27 PHOTO-28 PHOTO-29 PHOTO-30
  LAYOUT-01 LAYOUT-03 LAYOUT-05 LAYOUT-06 LAYOUT-07 LAYOUT-10 LAYOUT-12 LAYOUT-14 LAYOUT-17 LAYOUT-19 LAYOUT-20 LAYOUT-23 LAYOUT-27 LAYOUT-29
  MOTION-01 MOTION-03 MOTION-04 MOTION-05 MOTION-08 MOTION-13 MOTION-14 MOTION-17 MOTION-20
  VECTOR-01 VECTOR-02 VECTOR-07 VECTOR-08 VECTOR-13
`);

const straighten = sets(`
  VECTOR-01 VECTOR-02 VECTOR-03 VECTOR-04 VECTOR-05 VECTOR-06 VECTOR-07 VECTOR-08 VECTOR-09 VECTOR-10 VECTOR-11 VECTOR-12 VECTOR-13 VECTOR-14 VECTOR-15
  PHOTO-02 PHOTO-03 PHOTO-04 PHOTO-06 PHOTO-07 PHOTO-12 PHOTO-15 PHOTO-18 PHOTO-20 PHOTO-25
  LAYOUT-02 LAYOUT-07 LAYOUT-10 LAYOUT-14 LAYOUT-27
`);

const quickCut = sets(`MOTION-01 MOTION-03 MOTION-05 MOTION-17 MOTION-20`);
const summarize = sets(`MOTION-01 MOTION-03 MOTION-05 MOTION-06 MOTION-08 MOTION-10 MOTION-14 MOTION-16 MOTION-17 MOTION-20`);
const speechAudio = sets(`MOTION-04 MOTION-05 MOTION-08 MOTION-14 MOTION-15`);

const fonts = new Set([...express, ...sets(`VECTOR-01 VECTOR-05 VECTOR-07 VECTOR-13 VECTOR-15 LAYOUT-10 LAYOUT-14 LAYOUT-22 LAYOUT-27 LAYOUT-35 MOTION-01 MOTION-04 MOTION-08 MOTION-14 MOTION-20`)]);

const effects = {
  image_apply_preset: sets(`PHOTO-02 PHOTO-04 PHOTO-07 PHOTO-09 PHOTO-12 PHOTO-15 PHOTO-19 LAYOUT-06 LAYOUT-12 MOTION-14`),
  image_apply_monochromatic_tint: sets(`PHOTO-15 PHOTO-21 PHOTO-23 VECTOR-02 VECTOR-07 VECTOR-08 VECTOR-13 LAYOUT-06 LAYOUT-14 MOTION-12`),
  image_add_grain: sets(`PHOTO-15 PHOTO-18 PHOTO-21 VECTOR-02 LAYOUT-14 MOTION-12`),
  image_add_noise: sets(`PHOTO-16 VECTOR-01 VECTOR-07 LAYOUT-12 MOTION-17`),
  image_apply_halftone: sets(`VECTOR-01 VECTOR-07 LAYOUT-12 MOTION-17`),
  image_apply_gaussian_blur: sets(`PHOTO-03 PHOTO-19 LAYOUT-20 MOTION-08`),
  image_apply_lens_blur: sets(`PHOTO-05 PHOTO-20 LAYOUT-05`),
  image_apply_color_overlay: sets(`PHOTO-11 PHOTO-21 VECTOR-04 LAYOUT-12 MOTION-11 MOTION-17`),
  image_apply_glitch_effect: sets(`MOTION-09 MOTION-11`),
  image_instruct_edit: sets(`PHOTO-05 PHOTO-11 LAYOUT-12 MOTION-11 MOTION-17`),
  image_generate: sets(`LAYOUT-12 PHOTO-21 MOTION-03 MOTION-11 MOTION-17`),
  image_generative_expand: sets(`PHOTO-03 PHOTO-04 PHOTO-09 PHOTO-20 PHOTO-27 LAYOUT-03 LAYOUT-13 MOTION-03 MOTION-11 MOTION-18`),
  image_remove_blemishes: sets(`PHOTO-06 PHOTO-18 PHOTO-19 PHOTO-20 LAYOUT-15 LAYOUT-23 MOTION-04 MOTION-14`),
};

const currentTools = sets(`
  adobe_acrobat_document_upload adobe_acrobat_markdown_to_pdf adobe_acrobat_pdf_combine adobe_acrobat_pdf_compress
  adobe_acrobat_pdf_create adobe_acrobat_pdf_delete_pages adobe_acrobat_pdf_edit_ui adobe_acrobat_pdf_export
  adobe_acrobat_pdf_ocr adobe_acrobat_pdf_operation_status adobe_acrobat_pdf_page_organize adobe_acrobat_pdf_properties
  adobe_acrobat_pdf_redact adobe_acrobat_pdf_reorder_pages adobe_acrobat_pdf_rotate_pages adobe_acrobat_pdf_split
  adobe_acrobat_pdf_to_image adobe_acrobat_pdf_to_markdown adobe_acrobat_pdf_viewer adobe_mandatory_init animate_design
  asset_add_file asset_add_file_check_status asset_copy_assets asset_create_folders asset_finalize_file_upload
  asset_get_presigned_urls asset_initialize_file_upload asset_inline_preview asset_license_and_download_stock
  asset_migrate_guest_storage asset_openai_file_upload asset_preview_file asset_search boards_add_items_to_board
  boards_create_new_board change_background_color convert_pdf_to_indd document_convert_pdf document_merge_data_layout
  document_merge_data_vector document_render_layout document_render_vector download_design export_idml express_animate_design
  express_change_background_color express_download_design express_fill_text express_next_design_actions express_replace_image
  express_search_design fill_text font_recommend generate_indd_mapping_prompt image_add_grain image_add_noise
  image_apply_adjustments image_apply_auto_tone image_apply_color_overlay image_apply_gaussian_blur image_apply_glitch_effect
  image_apply_halftone image_apply_lens_blur image_apply_monochromatic_tint image_apply_preset image_auto_straighten
  image_crop_and_resize image_crop_to_bounds image_fill_area image_generate image_generative_expand image_instruct_edit
  image_invert_selection image_list_presets image_remove_background image_remove_blemishes image_select_by_prompt
  image_select_subject image_vectorize markdown_to_pdf media_enhance_speech media_summarize pdf_compress pdf_create
  pdf_export pdf_ocr pdf_operation_status pdf_properties pdf_to_image pdf_to_markdown prepare_indd_merge_template replace_image
  search_design video_create_quick_cut video_metadata video_render video_render_frame video_resize
`);

const series = {
  "PHOTO-02": ["CORNER_CURE", "Phase 1: food image system and seasonal launch assets", "Brooklyn, New York"],
  "LAYOUT-02": ["CORNER_CURE", "Phase 2: counter refit, cold-case labels and signage", "Brooklyn, New York"],
  "PHOTO-10": ["NORTHGROVE", "Phase 1: apparel colour and ecommerce proofing", "Burlington, Vermont"],
  "LAYOUT-04": ["NORTHGROVE", "Phase 2: wholesale lookbook, hang tags and launch collateral", "Burlington, Vermont"],
  "PHOTO-04": ["VERRANZA", "Phase 1: villa image system and booking imagery", "Liguria, Italy"],
  "LAYOUT-08": ["VERRANZA", "Phase 2: booking collateral and in-villa season cards", "Liguria, Italy"],
  "LAYOUT-11": ["LANTERNWOOD", "Phase 1: performer passes and on-sale campaign", "outside Burlington, Vermont"],
  "LAYOUT-26": ["LANTERNWOOD", "Phase 2: keepsake programme and venue wayfinding", "outside Burlington, Vermont"],
  "LAYOUT-15": ["ALDERVALE_MUTUAL", "Phase 1: producer sales and compliance kit", "central Vermont"],
  "LAYOUT-25": ["ALDERVALE_MUTUAL", "Phase 2: personalised renewal mailer", "central Vermont"],
  "LAYOUT-16": ["ANVIL_OAK", "Phase 1: studio opening identity and member cards", "Providence, Rhode Island"],
  "MOTION-15": ["ANVIL_OAK", "Phase 2: coached movement video library", "Providence, Rhode Island"],
  "PHOTO-25": ["APEXGUARD", "Phase 1: rebrand photography and product rollout", "Charlotte, North Carolina"],
  "LAYOUT-17": ["APEXGUARD", "Phase 2: dealer labels and channel collateral", "Charlotte, North Carolina"],
  "PHOTO-12": ["KILNMORE", "Phase 1: ecommerce product image system", "Portland, Maine"],
  "LAYOUT-18": ["KILNMORE", "Phase 2: wholesale line sheets and storefront launch", "Portland, Maine"],
  "PHOTO-17": ["CONTINENTAL_CUP", "Phase 1: collector-card portrait finishing", "touring competition, Western Europe and North America"],
  "LAYOUT-33": ["CONTINENTAL_CUP", "Phase 2: squad press run and partner files", "touring competition, Western Europe and North America"],
  "PHOTO-14": ["GIRDERMARK", "Phase 1: components photography and technical sheets", "Cleveland, Ohio"],
  "LAYOUT-27": ["GIRDERMARK", "Phase 2: data-sheet and bin-label library", "Cleveland, Ohio"],
  "PHOTO-11": ["LUMORA", "Phase 1: pre-production lip-oil colour concepts", "Los Angeles, California"],
  "LAYOUT-03": ["LUMORA", "Phase 2: skincare counter launch for the parent range", "Los Angeles, California"],
};

const tiers = {
  flagship: { label: "Flagship integrated engagement", deliverables: 5, timeline: "4 to 6 weeks", revisions: "Direction approval, first-production proof, and two consolidated revision rounds" },
  expert: { label: "Expert standard engagement", deliverables: 4, timeline: "2 to 4 weeks", revisions: "One direction checkpoint and two consolidated revision rounds" },
  specialist: { label: "Specialist stress test", deliverables: 3, timeline: "7 to 15 business days", revisions: "One technical proof and two consolidated revision rounds" },
};

const budgets = {
  "Photo & Imaging": { flagship: "$4,000-$8,500 fixed", expert: "$1,800-$4,500 fixed", specialist: "$900-$2,400 fixed" },
  "Vector & Identity": { flagship: "$5,000-$10,000 fixed", expert: "$2,500-$6,000 fixed", specialist: "$1,200-$3,200 fixed" },
  "Layout & Data": { flagship: "$6,000-$12,000 fixed", expert: "$3,000-$7,000 fixed", specialist: "$1,400-$3,800 fixed" },
  "Motion & Video": { flagship: "$5,000-$12,000 fixed", expert: "$2,500-$6,500 fixed", specialist: "$1,000-$3,000 fixed" },
};

function familyKey(spec) {
  if (spec.new_id.startsWith("PHOTO")) return "Photo & Imaging";
  if (spec.new_id.startsWith("VECTOR")) return "Vector & Identity";
  if (spec.new_id.startsWith("LAYOUT")) return "Layout & Data";
  return "Motion & Video";
}

function tierKey(id) {
  if (flagship.has(id)) return "flagship";
  if (specialist.has(id)) return "specialist";
  return "expert";
}

function cleanText(value) {
  return String(value || "").replace(/\s+/g, " ").trim();
}

function sentence(value, max = 260) {
  const text = cleanText(value);
  const first = text.match(/^.*?[.!?](?:\s|$)/)?.[0] || text;
  if (first.length <= max) return first;
  const cut = first.slice(0, max - 3);
  return `${cut.slice(0, cut.lastIndexOf(" ")).trim()}...`;
}

function shortName(name, brand) {
  let value = cleanText(name).replace(new RegExp(`^${brand.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\s*`, "i"), "");
  value = value.split(/,| plus | as one /i)[0].trim();
  if (value.length <= 72) return value;
  const cut = value.slice(0, 72);
  return cut.slice(0, cut.lastIndexOf(" ")).trim();
}

function marketplaceTitle(spec, deliverable, family) {
  const brand = spec.brand_identity.brand_name;
  const prefix = `${roleFor(family)} for ${brand}: `;
  const subject = shortName(deliverable.name, brand);
  if (`${prefix}${subject}`.length <= 120) return `${prefix}${subject}`;
  const cut = subject.slice(0, Math.max(1, 120 - prefix.length));
  return `${prefix}${cut.slice(0, cut.lastIndexOf(" ")).trim()}`;
}

const canonicalTaskNames = {
  "PHOTO-01": "Aurelian Skin - Ecommerce skincare image system",
  "PHOTO-02": "Corner and Cure - Spring dish launch photography",
  "PHOTO-03": "Cedarline and Vale - Ridgeway Lane listing image system",
  "PHOTO-04": "Verranza Coastal Retreats - Villa collection image system",
  "PHOTO-05": "Halcyon Quarter - Mixed-use launch photography",
  "PHOTO-06": "Hollis Family Archive - Ada Hollis archival restoration",
  "PHOTO-07": "Gable and Grove - Home services before-and-after library",
  "PHOTO-08": "Meridian Motors - Showroom vehicle image system",
  "PHOTO-09": "OSTRA - Restaurant plate photography system",
  "PHOTO-10": "Northgrove - Apparel colorway image system",
  "PHOTO-11": "Lumora - Lip oil shade concept set",
  "PHOTO-12": "Kilnmore - Ceramic ecommerce image system",
  "PHOTO-13": "Argent and Faith - Spring jewelry capsule photography",
  "PHOTO-14": "Girdermark - Industrial component image system",
  "PHOTO-15": "Summit and Sable - Watch campaign master set",
  "PHOTO-16": "SlabVault - Collectible card marketplace image system",
  "PHOTO-17": "Continental Cup - Player portrait card system",
  "PHOTO-18": "Fernwell and Rowe - Hartley wedding gallery finishing",
  "PHOTO-19": "Cascadia Founders Summit - Executive portrait set",
  "PHOTO-20": "Astrid Vellacourt - Editorial portrait session",
  "PHOTO-21": "Quill and Kiln - Autumn ceramics signature look",
  "PHOTO-22": "Nordhaven - Outerwear signature image system",
  "PHOTO-23": "Ironline Forge - Blacksmith editorial image set",
  "PHOTO-24": "Lunara Chronometry - Autumn watch campaign",
  "PHOTO-25": "Apexguard - Industrial surfaces launch photography",
  "PHOTO-26": "Thornmere Home - Autumn interiors image system",
  "PHOTO-27": "Fennhollow - Botanical soda summer campaign",
  "PHOTO-28": "Verda Reformer Studio - Fitness campaign image system",
  "PHOTO-29": "Cape Marren - Shoulder-season tourism campaign",
  "PHOTO-30": "Palewell Health - Licensed care image campaign",
  "VECTOR-01": "Cordwain Overland - Identity master graphics",
  "VECTOR-02": "Redecker Machine Works - Restored mark system",
  "VECTOR-03": "Apex Rally Club - Motorsport face and livery system",
  "VECTOR-04": "Meridian and Ash - Sticker artwork production masters",
  "VECTOR-05": "Isla Verde - Monogram and wayfinding pictogram system",
  "VECTOR-06": "Ridgeway Rovers - Football crest master system",
  "VECTOR-07": "Wharfside Folk Festival - Restored festival identity",
  "VECTOR-08": "Coble and Vane - One-color mark system",
  "VECTOR-09": "Halcyon Grid - Production logo family",
  "VECTOR-10": "Evergreen Provisions - Restored crest system",
  "VECTOR-11": "Cedar Commons - Farmers market identity restoration",
  "VECTOR-12": "Static Union - Manufacturing artwork system",
  "VECTOR-13": "Maison Serault - Wordmark and monogram master set",
  "VECTOR-14": "Ironway Run Club - Numbering and club mark system",
  "VECTOR-15": "Marchfield Exchange - Crest and engraving geometry system",
  "LAYOUT-01": "Kantyna Nova - Private dining menu and campaign system",
  "LAYOUT-02": "Corner and Cure - Cold-case label system",
  "LAYOUT-03": "Lumora Laboratories - Retail launch and paid social system",
  "LAYOUT-04": "Northgrove - Wholesale lookbook and hang-tag system",
  "LAYOUT-05": "Maison Valcere - Brand story deck and campaign document",
  "LAYOUT-06": "Nordheim Atelier - Showroom line-card system",
  "LAYOUT-07": "Harbor Crest Realty - Open-house card campaign",
  "LAYOUT-08": "Verranza Coastal Retreats - In-villa seasonal collateral",
  "LAYOUT-09": "Nimbadesk - B2B sell-sheet system",
  "LAYOUT-10": "Alderwood Scholars Fund - Multi-center appeal campaign",
  "LAYOUT-11": "Lanternwood Folk Fest - Performer credential system",
  "LAYOUT-12": "Umbra Loft - After Dark event campaign",
  "LAYOUT-13": "Marisol Cove - Shoulder-season hospitality campaign",
  "LAYOUT-14": "Lumen Quarterly - Autumn editorial issue",
  "LAYOUT-15": "Aldervale Mutual - District insurance counter-card run",
  "LAYOUT-16": "Anvil and Oak - Gym opening member collateral",
  "LAYOUT-17": "Apexguard - Product label and dealer collateral system",
  "LAYOUT-18": "Kilnmore - Wholesale relaunch campaign",
  "LAYOUT-19": "Northwind Advisory - Team page and recruitment collateral",
  "LAYOUT-20": "Walter Fernwood Memorial - Service print and remembrance set",
  "LAYOUT-21": "Harborline Realty - Weekly listing sheet system",
  "LAYOUT-22": "Cedarline Institute - Cohort credential system",
  "LAYOUT-23": "Meridian Summit - Conference badge and wayfinding system",
  "LAYOUT-24": "Halden and Roe - Marlow trade catalog",
  "LAYOUT-25": "Aldervale Mutual - Personalized autumn renewal mailer",
  "LAYOUT-26": "Lanternwood Folk Fest - Festival programme and wayfinding",
  "LAYOUT-27": "Girdermark - Technical data-sheet and bin-label library",
  "LAYOUT-28": "SEVE Botanicals - Cosmetic launch label system",
  "LAYOUT-29": "Rivermeadow Trust - Year-end donor acknowledgement system",
  "LAYOUT-30": "Emberwell Brew House - Live insert and taproom collateral",
  "LAYOUT-31": "Cellar and Cru - Autumn shelf-talker campaign",
  "LAYOUT-32": "Vanguard Motors - Forecourt sales card system",
  "LAYOUT-33": "Continental Cup - Squad press and partner kit",
  "LAYOUT-34": "Ferncroft Nursery - Spring plant tag system",
  "LAYOUT-35": "Marrow and Vane - Exhibition wall-label system",
  "MOTION-01": "Ember and Oak - Restaurant launch reel system",
  "MOTION-02": "Ironwood Kitchen - Product launch video package",
  "MOTION-03": "Halden Greens - Creator ad and social cutdowns",
  "MOTION-04": "Sable and Finch Realty - Property listing tour package",
  "MOTION-05": "Sterling Row - Venue opening film and teaser",
  "MOTION-06": "Meridian Academy - Lesson video package",
  "MOTION-07": "Norvant - Product explainer motion system",
  "MOTION-08": "SentinelMesh - Product demo and narration package",
  "MOTION-09": "Voltcast - Podcast short and audio treatment",
  "MOTION-10": "DAYDRIFT - Vertical interview short series",
  "MOTION-11": "STATIC FOX - Thumbnail and animated channel package",
  "MOTION-12": "NIGHTFORM - Low Beam music release package",
  "MOTION-13": "Emberline - Food channel thumbnail and motion package",
  "MOTION-14": "Halden Diaries - Season recap video package",
  "MOTION-15": "Anvil and Oak Strength - Movement coaching clip library",
  "MOTION-16": "Vitale Labs - Wellness editorial video package",
  "MOTION-17": "Pulsevault - Event recap package",
  "MOTION-18": "Velvet Hour - Social film and story cutdowns",
  "MOTION-19": "Milepost Driving Academy - Scenario clip training library",
  "MOTION-20": "FOLD and GRAIN Studio - Dual-client sizzle and service package",
};

function canonicalTaskIdentity(spec, deliverable) {
  const [legacyFamily, legacySequenceText] = spec.new_id.split("-");
  const legacySequence = Number(legacySequenceText);
  const familyConfig = {
    PHOTO: { offset: 0, code: "PHO" },
    VECTOR: { offset: 30, code: "VEC" },
    LAYOUT: { offset: 45, code: "LAY" },
    MOTION: { offset: 80, code: "MOT" },
  }[legacyFamily];
  if (!familyConfig || !Number.isInteger(legacySequence)) throw new Error(`Cannot assign canonical identity to ${spec.new_id}`);

  const globalOrder = familyConfig.offset + legacySequence;
  const taskCode = `SB3-${String(globalOrder).padStart(3, "0")}-${familyConfig.code}`;
  const taskName = canonicalTaskNames[spec.new_id];
  if (!taskName) throw new Error(`Canonical task name missing for ${spec.new_id}`);
  const slug = taskName.normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/&/g, " and ").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 96).replace(/-+$/g, "");
  const storageFolder = `${taskCode}__${slug}`;
  return {
    task_code: taskCode,
    task_name: taskName,
    global_order: globalOrder,
    family_code: familyConfig.code,
    legacy_id: spec.new_id,
    storage_folder: storageFolder,
    s3_prefix: `s3://annotationprod/creative-ai-benchmark/v3.1/tasks/${storageFolder}/`,
  };
}

function roleFor(family) {
  return {
    "Photo & Imaging": "Senior photo retoucher",
    "Vector & Identity": "Production vector designer",
    "Layout & Data": "Editorial and production designer",
    "Motion & Video": "Video editor and motion designer",
  }[family];
}

function measuredMotion(id) {
  const dir = path.join(assetsRoot, id, "assets");
  if (!fs.existsSync(dir)) return null;
  const media = fs.readdirSync(dir).filter((name) => /\.(mp4|mov|wav)$/i.test(name)).sort().map((name) => {
    const file = path.join(dir, name);
    const output = execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate,channels", "-of", "json", file], { encoding: "utf8" });
    const probe = JSON.parse(output);
    return {
      filename: name,
      duration_seconds: Number(Number(probe.format?.duration || 0).toFixed(3)),
      streams: (probe.streams || []).map((stream) => ({
        codec_type: stream.codec_type,
        codec_name: stream.codec_name,
        ...(stream.width ? { width: stream.width, height: stream.height, frame_rate: stream.r_frame_rate } : {}),
        ...(stream.channels ? { channels: stream.channels } : {}),
      })),
    };
  });
  const video = media.filter((entry) => entry.streams.some((stream) => stream.codec_type === "video"));
  const audioOnly = media.filter((entry) => entry.streams.some((stream) => stream.codec_type === "audio") && !entry.streams.some((stream) => stream.codec_type === "video"));
  const fact = {
    generated_at: "2026-09-15",
    authority: "ffprobe measurements of the supplied files; these values override narrative duration labels",
    files: media,
    summary: {
      video_file_count: video.length,
      total_video_seconds: Number(video.reduce((sum, entry) => sum + entry.duration_seconds, 0).toFixed(3)),
      video_files_with_audio_streams: video.filter((entry) => entry.streams.some((stream) => stream.codec_type === "audio")).length,
      separate_audio_file_count: audioOnly.length,
      total_separate_audio_seconds: Number(audioOnly.reduce((sum, entry) => sum + entry.duration_seconds, 0).toFixed(3)),
    },
  };
  const metadataName = "motion_source_metadata.json";
  fs.writeFileSync(path.join(dir, metadataName), `${JSON.stringify(fact, null, 2)}\n`);

  const manifestPath = path.join(assetsRoot, id, "manifest.json");
  const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  const metadataEntry = {
    filename: metadataName,
    type: "json",
    role: "authoritative source metadata",
    status: "ok",
    generated_at: "2026-09-15",
    provenance: "ffprobe measurements of supplied motion files",
  };
  const existingIndex = (manifest.assets || []).findIndex((asset) => asset.filename === metadataName);
  if (existingIndex >= 0) manifest.assets[existingIndex] = metadataEntry;
  else manifest.assets = [...(manifest.assets || []), metadataEntry];
  const serializedManifest = JSON.stringify(manifest, null, 1).replace(/[^\x00-\x7f]/g, (char) => `\\u${char.charCodeAt(0).toString(16).padStart(4, "0")}`);
  fs.writeFileSync(manifestPath, serializedManifest);
  return fact;
}

function scoreDeliverable(spec, d) {
  const family = familyKey(spec);
  const text = `${d.deliverable_class || ""} ${d.name || ""}`.toLowerCase();
  const classText = (d.deliverable_class || "").toLowerCase();
  const nameText = (d.name || "").toLowerCase();
  const isData = /data.?merge/.test(text);
  const isExpress = /express/.test(text);
  const isVector = /vector/.test(classText) || /^(recovered|.* mark system|.* crest system|.* monogram|.* wordmark|.* glyph system)/.test(nameText);
  const isHandover = (!/express/.test(classText) && /handover/.test(classText)) || /^(handover|brand basis|printer note|production note|delivery note)/.test(nameText);
  if (isHandover) return -100;
  if (isData && !dataMerge.has(spec.new_id)) return -90;
  if (isExpress && !express.has(spec.new_id)) return -90;
  if (isVector && !vectorOps.has(spec.new_id)) return -80;
  if (/isolation|cutout/.test(text) && !cutoutOps.has(spec.new_id)) return -70;
  if (family === "Photo & Imaging") {
    if (/graded|stylized/.test(text)) return 110;
    if (/isolation|cutout/.test(text)) return 100;
    if (isData) return 90;
    if (isExpress) return 80;
    if (isVector) return 75;
  }
  if (family === "Vector & Identity") {
    if (/vector|artwork|plate|separation|cut layer/.test(text)) return 115;
    if (isData) return 95;
    if (/laid.out|spec|signage|sheet/.test(text)) return 90;
    if (/graded|photography/.test(text)) return 75;
    if (isExpress) return 70;
  }
  if (family === "Layout & Data") {
    if (isData) return 115;
    if (/laid.out|print document|programme|report|catalog|book/.test(text)) return 105;
    if (isExpress) return 95;
    if (/graded|photography/.test(text)) return 85;
    if (isVector) return 80;
    if (/isolation|cutout/.test(text)) return 70;
  }
  if (family === "Motion & Video") {
    if (/video|motion|cut|reel|film|recap|clip/.test(text)) return 120;
    if (/graded|photography|still|frame/.test(text)) return 95;
    if (isData) return 90;
    if (isExpress) return 85;
    if (isVector) return 75;
    if (/isolation|cutout/.test(text)) return 70;
  }
  return 50;
}

function makeProofDeliverable(spec, lead, integrated = false) {
  const family = familyKey(spec);
  const brand = spec.brand_identity.brand_name;
  const n = Number(spec.new_id.split("-")[1]);
  if (family === "Photo & Imaging") {
    const variants = [
      ["delivery-size crop matrix", "placement crop matrix", "A client-facing matrix showing each approved master at its actual placement ratios and sizes, with source dimensions, crop decisions, rejected frames, and no-upscale checks."],
      ["source-to-final retouch contact sheet", "retouch comparison sheet", "A source-to-final contact sheet at matched scale that proves set consistency, identity or material preservation, and the disposition of every outlier."],
      ["placement and edge proof set", "placement and edge proof", "A proof set on the real light and dark destination grounds, including full-resolution edge inspections, delivery-size previews, and explicit pass/fail notes."],
      ["color-continuity approval sheet", "color continuity proof", "A calibrated side-by-side approval sheet showing white point, black point, skin or material color, and crop consistency across the finished set."],
    ];
    const [suffix, deliverable_class, specText] = variants[n % variants.length];
    return { name: `${brand} ${suffix}`, deliverable_class, spec: `${specText} It must reference ${lead.name} and function as approval evidence rather than decoration.` };
  }
  if (family === "Layout & Data") {
    return {
      name: `${brand} ${n % 2 ? "record-integrity press proof" : "page-size and overflow proof pack"}`,
      deliverable_class: n % 2 ? "record integrity and press proof" : "layout preflight proof pack",
      spec: "A client-facing preflight package showing representative first, middle, last, longest, and exception records at true output size, with page count, dimensions, overflow, image binding, naming, and record identity checks.",
    };
  }
  if (family === "Vector & Identity") {
    return {
      name: `${brand} small-size geometry evidence sheet`,
      deliverable_class: "vector geometry and reproduction proof",
      spec: `An inspectable proof of ${lead.name} at every claimed reproduction size and on light/dark grounds, with open-path, closure, transparency, contour, and unsupported-feature findings stated plainly.`,
    };
  }
  return {
    name: `${brand} platform reframe and continuity proof`,
    deliverable_class: "motion continuity and platform QC proof",
    spec: `A timecoded client proof for ${lead.name} showing selected source ranges, representative transition frames, horizontal-to-vertical crop comparisons, and pass/fail findings for continuity and subject retention.`,
  };
}

function normalizeDeliverable(spec, d, motionFact) {
  const out = structuredClone(d);
  const text = `${out.deliverable_class || ""} ${out.name || ""}`.toLowerCase();
  if (/express/.test(text)) {
    out.deliverable_class = "editable Express template adaptation";
    out.spec = `One professionally selected Adobe Express template adapted to the supplied brand, copy, and approved imagery. The agent is pre-authorized to choose the strongest fitting template, replace its content, correct the background where needed, and deliver both the editable design link and requested export. This is a supporting asset, not a substitute for the primary custom craft deliverable.`;
  }
  if (/vector artwork|mark|crest|wordmark|monogram|glyph|plate art|cut layer/.test(text)) {
    out.spec = `${sentence(out.spec, 520)} Vectorization is a starting operation, not proof of production readiness: deliver transparent SVG, rendered small-size proofs, and an inspectable geometry report. Any unverified contour or fabrication tolerance must be labeled for supplier review.`;
  }
  if (spec.new_id === "PHOTO-11" && /shade range|cut.?out/.test(text)) {
    out.name = out.name.replace(/shade range/i, "concept shade range");
    out.spec = `${sentence(out.spec, 420)} Every output and comparison sheet must state CONCEPT COLOR - SAMPLE APPROVAL REQUIRED. The work may show relative direction only and must not claim production-accurate product or on-lip color.`;
  }
  if (familyKey(spec) === "Motion & Video" && /video|motion/.test((out.deliverable_class || "").toLowerCase())) {
    const count = motionFact?.summary.video_file_count || 0;
    const total = motionFact?.summary.total_video_seconds || 0;
    if (count === 0) {
      out.name = `${spec.brand_identity.brand_name} animated channel package`;
      out.deliverable_class = "template-based motion design";
      out.spec = "One 5 to 8 second animated title/end-card treatment and a static thumbnail system derived from the supplied still artwork. Animation must be created from the actual design assets; no source video or speech is implied.";
    } else if (spec.new_id === "MOTION-20") {
      out.spec = "Two visually led 4-second sizzles, one per supplied client clip, plus one vertical reframe of each. Quick Cut may choose the visually strongest span inside each short clip; it must not combine the two brands or imply speech. Inspect both outputs for product continuity and keep the two client looks deliberately distinct.";
    } else if (quickCut.has(spec.new_id)) {
      const target = Math.max(4, Math.min(15, Math.floor(total * 0.55)));
      out.spec = `A visually led highlight no longer than ${target} seconds assembled only from the ${count} supplied short clip${count === 1 ? "" : "s"}, plus one platform reframe. Quick Cut may choose visually engaging moments; it must not be credited with understanding speech or claims. Inspect the returned edit for subject continuity, crop safety, and repeated shots before delivery.`;
    } else {
      const target = Math.max(4, Math.min(24, Math.floor(total * 0.72)));
      out.spec = `A deliberate ${target}-second-or-shorter edit assembled from the ${count} supplied short clip${count === 1 ? "" : "s"} using an explicit timeline, plus one platform reframe and three checked poster frames. Source time ranges must come from motion_source_metadata.json and a task-specific edit decision list. The supplied video files contain no audio streams; use a separate supplied WAV only where one exists and never infer dialogue from silent footage.`;
    }
  }
  return out;
}

function chooseDeliverables(spec, tier, motionFact) {
  const scored = (spec.deliverables || [])
    .map((d, index) => ({ d, index, score: scoreDeliverable(spec, d) }))
    .sort((a, b) => b.score - a.score || a.index - b.index);
  const ranked = scored.filter((entry) => entry.score > 0);
  let selected = ranked.slice(0, tiers[tier].deliverables).map((entry) => normalizeDeliverable(spec, entry.d, motionFact));
  if (spec.new_id === "MOTION-11") {
    selected = [
      {
        name: "STATIC FOX six-title thumbnail system",
        deliverable_class: "thumbnail and raster design set",
        spec: "Six platform thumbnails built from the supplied episode titles, mascot render, channel patch, and competitor reference sheet. The family must be recognizably STATIC FOX without copying a competitor's character, claims, composition, or typography; each title must remain readable at feed size.",
      },
      {
        name: "Scrap mascot cutout and fox-emblem proof",
        deliverable_class: "isolation and cutout set",
        spec: "A clean transparent mascot cutout, a one-color raster proof of the fox emblem recovered only as far as the photographed patch supports, and light/dark application tests. No claim of production vector readiness is permitted.",
      },
      {
        name: "STATIC FOX animated channel package",
        deliverable_class: "editable Express template adaptation",
        spec: "One 5 to 8 second animated title/end-card treatment adapted from a professionally selected Adobe Express template, using the approved STATIC FOX title, mascot, and palette. Deliver the editable design and final export; no source video or speech is implied.",
      },
    ];
  }
  if (selected.length === 0) {
    const fallback = scored.find((entry) => entry.score > -100);
    if (!fallback) throw new Error(`${spec.new_id} has no usable creative deliverable`);
    selected.push(normalizeDeliverable(spec, fallback.d, motionFact));
  }
  if (selected.length < 2) {
    const lead = selected[0];
    selected.push(makeProofDeliverable(spec, lead));
  }
  if (tier === "flagship" && selected.length < 3) {
    const lead = selected[0];
    selected.push(makeProofDeliverable(spec, lead, true));
  }
  return selected;
}

function operationRationale(tool, spec) {
  const map = {
    image_apply_adjustments: "Build the task-specific tonal or color target from the supplied images.",
    image_apply_auto_tone: "Create a reviewable baseline before deliberate per-image correction.",
    image_auto_straighten: "Correct handheld artwork, architecture, document, or product capture before cropping.",
    image_crop_and_resize: "Produce required placements at their actual dimensions without silent enlargement.",
    image_crop_to_bounds: "Remove unused capture area around isolated artwork or products.",
    image_select_subject: "Create a controlled foreground selection for a genuine isolation deliverable.",
    image_select_by_prompt: "Target the specific material, mark, label, or region described in the brief.",
    image_invert_selection: "Confine background-only correction after the foreground selection is inspected.",
    image_fill_area: "Repair a small non-factual gap or prepare a controlled solid ground.",
    image_remove_background: "Produce transparent product or artwork files with edge inspection.",
    image_vectorize: "Create an initial SVG trace that is subsequently checked at delivery size.",
    convert_pdf_to_indd: "Recover the supplied legacy printer PDF as an editable production starting point.",
    generate_indd_mapping_prompt: "Identify and verify true variable fields before data merge.",
    prepare_indd_merge_template: "Build a reusable template from verified fields and client records.",
    document_merge_data_layout: "Generate the required record-per-page production run.",
    document_render_layout: "Render proofs at the required physical dimensions and density.",
    document_merge_data_vector: "Bind variable vector artwork where the record set genuinely requires it.",
    document_render_vector: "Inspect variable vector output rather than trusting merge completion.",
    export_idml: "Provide an editable professional handoff for a repeatable production job.",
    pdf_properties: "Verify page count, dimensions, and orientation against the printer requirement.",
    pdf_ocr: "Recover text from an image-only or scanned source before reuse.",
    pdf_to_markdown: "Extract approved copy or table content for reconciliation.",
    pdf_to_image: "Create page proofs for visual comparison with the reconstructed file.",
    pdf_compress: "Meet the client-specified screen-delivery size without replacing the press master.",
    search_design: "Find an appropriate professional template for the explicitly template-based supporting asset.",
    fill_text: "Replace template copy exactly with approved client text.",
    replace_image: "Replace template imagery with the supplied or licensed approved image.",
    change_background_color: "Bring the chosen template onto the approved brand ground.",
    animate_design: "Produce the requested lightweight animated social or title variant.",
    download_design: "Export the approved template adaptation in the requested delivery format.",
    font_recommend: "Make a documented typography choice appropriate to the audience and reproduction size.",
    asset_search: "Search Adobe Stock only for the declared content gap in this task.",
    asset_license_and_download_stock: "License the selected full-resolution asset and preserve provenance.",
    boards_create_new_board: "Create a real shortlist or approval board required by this engagement.",
    boards_add_items_to_board: "Place only the final candidates and comparison evidence on the approval board.",
    video_metadata: "Measure every supplied video before planning duration or framing.",
    video_create_quick_cut: "Create a visually selected first-pass highlight where speech meaning is not required.",
    media_summarize: "Orient to visual content; the summary is not treated as a timecoded transcript.",
    media_enhance_speech: "Clean the separately supplied narration or cue recording.",
    video_render: "Assemble the approved source ranges through an explicit JSON timeline.",
    video_render_frame: "Inspect representative final frames for crop, continuity, and title safety.",
    video_resize: "Create the required platform aspect-ratio variant from the approved master.",
  };
  return map[tool] || `Apply ${tool.replaceAll("_", " ")} only because the task's visual language or production requirement calls for it.`;
}

function operationsFor(spec, deliverables, motionFact) {
  const id = spec.new_id;
  const family = familyKey(spec);
  const text = JSON.stringify(deliverables).toLowerCase();
  const labels = deliverables.map((d) => `${d.deliverable_class || ""} ${d.name || ""}`).join(" ").toLowerCase();
  const required = [];
  const optional = [];
  const add = (...tools) => tools.forEach((tool) => { if (!required.includes(tool)) required.push(tool); });
  const opt = (...tools) => tools.forEach((tool) => { if (!optional.includes(tool) && !required.includes(tool)) optional.push(tool); });
  const hasData = /data.?merge/.test(labels);
  const hasExpress = /express template|express collateral/.test(labels);
  const hasVector = /vector artwork|\bmark\b|\bcrest\b|\bwordmark\b|\bmonogram\b|\bglyph\b|plate art|cut layer/.test(labels);
  const hasCutout = /isolation|cutout/.test(labels);

  if (imageAdjust.has(id)) add("image_apply_adjustments");
  if (imageCrop.has(id)) add("image_crop_and_resize");
  const n = Number(id.split("-")[1]);
  if (family === "Photo & Imaging" || /graded|photography|still/.test(text)) {
    if (n % 2 === 0) add("image_apply_auto_tone");
  }
  if (straighten.has(id)) add("image_auto_straighten");
  if (hasCutout && cutoutOps.has(id)) add("image_select_subject", "image_remove_background", "image_crop_to_bounds");
  if (/background|ground/.test(text) && hasCutout && cutoutOps.has(id) && n % 2 === 0) add("image_invert_selection", "image_fill_area");
  if (hasVector && vectorOps.has(id)) add("image_select_by_prompt", "image_crop_to_bounds", "image_vectorize");
  for (const [tool, taskSet] of Object.entries(effects)) if (taskSet.has(id)) add(tool);

  if (hasData) {
    add("convert_pdf_to_indd", "generate_indd_mapping_prompt", "prepare_indd_merge_template", "document_merge_data_layout", "document_render_layout", "export_idml");
    if (family === "Vector & Identity" && n % 2 === 1) add("document_merge_data_vector", "document_render_vector");
  }
  if (acrobat.has(id)) {
    add("pdf_properties");
    const mode = n % 4;
    if (mode === 0) add("pdf_ocr", "pdf_to_markdown");
    if (mode === 1) add("pdf_to_markdown");
    if (mode === 2) add("pdf_to_image");
    if (mode === 3) add("pdf_compress");
  }
  if (hasExpress) {
    add("search_design", "fill_text", "replace_image", "download_design");
    if (n % 2 === 0) add("change_background_color");
    if (family === "Motion & Video" || n % 5 === 0) add("animate_design");
  }
  if (fonts.has(id)) add("font_recommend");
  if (stock.has(id)) opt("asset_search", "asset_license_and_download_stock");
  if (boards.has(id)) add("boards_create_new_board", "boards_add_items_to_board");
  if (family === "Motion & Video") {
    if ((motionFact?.summary.video_file_count || 0) > 0) {
      add("video_metadata");
      if (quickCut.has(id)) add("video_create_quick_cut");
      else add("video_render");
      if (id !== "MOTION-02" && id !== "MOTION-12" && id !== "MOTION-18") add("video_render_frame");
      add("video_resize");
      if (summarize.has(id)) add("media_summarize");
    }
    if (speechAudio.has(id)) add("media_enhance_speech");
    if ((motionFact?.summary.video_file_count || 0) === 0 && /express template/.test(text)) add("search_design", "fill_text", "replace_image", "animate_design", "download_design");
  }
  const transport = ["adobe_mandatory_init", "asset_initialize_file_upload", "asset_finalize_file_upload", "asset_inline_preview"];
  for (const tool of [...required, ...optional, ...transport]) if (!currentTools.has(tool)) throw new Error(`${id} uses unavailable tool ${tool}`);
  return {
    profile_id: "chatgpt-adobe-2026-09-15",
    autonomy: "zero-human; the agent is pre-authorized to make aesthetic and template choices within the brief",
    primary_surface: family,
    required_operations: required,
    conditional_operations: optional,
    transport_and_inspection_helpers: transport,
    operation_rationale: Object.fromEntries(required.map((tool) => [tool, operationRationale(tool, spec)])),
    ...(hasExpress ? { template_selection_authority: "The agent chooses the strongest fitting Adobe Express template and records the chosen template URN; no human chooser step is required." } : {}),
    ...(stock.has(id) ? { stock_policy: "Use only for the declared content gap. License before final use, preserve the asset ID, and disclose that the image is representative." } : {}),
  };
}

function surfaceGroups(profile) {
  const groups = [
    ["Imaging", /^(image_)/],
    ["InDesign production", /^(convert_pdf_to_indd|generate_indd|prepare_indd|document_|export_idml)/],
    ["Acrobat", /^(pdf_|adobe_acrobat_)/],
    ["Adobe Express", /^(search_design|fill_text|replace_image|change_background_color|animate_design|download_design)/],
    ["Adobe Stock", /^(asset_search|asset_license_and_download_stock)/],
    ["Firefly Boards", /^boards_/],
    ["Fonts", /^font_/],
    ["Video and audio", /^(video_|media_)/],
  ];
  return groups.map(([surface, regex]) => {
    const tools = profile.required_operations.filter((tool) => regex.test(tool));
    const conditional = profile.conditional_operations.filter((tool) => regex.test(tool));
    if (!tools.length && !conditional.length) return null;
    return { surface, tools, conditional_tools: conditional, role: [...tools, ...conditional].map((tool) => profile.operation_rationale[tool] || operationRationale(tool, {})).join(" ") };
  }).filter(Boolean);
}

function relevanceScore(line, deliverables) {
  const hay = cleanText(line).toLowerCase();
  const words = new Set(cleanText(deliverables.map((d) => `${d.name} ${d.deliverable_class}`).join(" ")).toLowerCase().split(/[^a-z0-9]+/).filter((word) => word.length > 4));
  let score = 0;
  for (const word of words) if (hay.includes(word)) score += 1;
  return score;
}

function referencesExcluded(line, spec) {
  const text = cleanText(line).toLowerCase();
  if (!express.has(spec.new_id) && /express|editable file|one editable|native editable/.test(text)) return true;
  if (!boards.has(spec.new_id) && /board/.test(text)) return true;
  if (!stock.has(spec.new_id) && /stock|licensed frame|licensed image/.test(text)) return true;
  if (!dataMerge.has(spec.new_id) && /merge|record per page|roster/.test(text)) return true;
  if (!vectorOps.has(spec.new_id) && /vector|viewbox|scalable artwork/.test(text)) return true;
  return false;
}

function acceptanceFor(spec, deliverables) {
  const ranked = (spec.acceptance_bar || []).filter((line) => !referencesExcluded(line, spec)).map((line, index) => ({ line, index, score: relevanceScore(line, deliverables) })).sort((a, b) => b.score - a.score || a.index - b.index);
  const chosen = ranked.slice(0, 5).map((entry) => cleanText(entry.line));
  chosen.push("Every supplied asset is listed in the delivery manifest as used, reference-only, superseded, or rejected with a concrete reason; no input disappears silently.");
  chosen.push("Final files open successfully, use unambiguous names, match the stated dimensions and formats, and include editable sources only where the scoped deliverable requires them.");
  if (familyKey(spec) === "Motion & Video") chosen.push("The edit never claims more source duration or source audio than motion_source_metadata.json records, and every delivered time range is traceable to the final EDL.");
  if (familyKey(spec) === "Vector & Identity" || vectorOps.has(spec.new_id)) chosen.push("Production-readiness claims are limited to geometry that can be inspected; vectorization alone is never accepted as evidence of fabrication readiness.");
  return [...new Set(chosen)].slice(0, 8);
}

function verifierContract(spec, deliverables, acceptance) {
  const uniqueChecks = (items) => {
    const seen = new Set();
    return items.filter((item) => {
      const key = `${cleanText(item.text).toLowerCase()}|${cleanText(item.how).toLowerCase()}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  };
  const processPattern = /tradeoff|tool|call|returned|response|run log|parameter log|operation record|success message|connector/i;
  const artifactSafe = (spec.verifiers_auto || []).filter((item) => !processPattern.test(`${item.text} ${item.how}`) && !referencesExcluded(`${item.text} ${item.how}`, spec)).slice(0, 5);
  const process = (spec.verifiers_auto || []).filter((item) => processPattern.test(`${item.text} ${item.how}`) && !referencesExcluded(`${item.text} ${item.how}`, spec)).slice(0, 4);
  const expected = deliverables.map((d) => d.name);
  const baseline = [
    { id: "A0-1", text: "The delivery manifest contains every scoped deliverable and no undeclared substitute.", how: `Match the manifest against these exact deliverable names: ${expected.join("; ")}.` },
    { id: "A0-2", text: "Every supplied input has a recorded disposition.", how: "Compare the input inventory with the manifest and require one of used, reference-only, superseded, or rejected-with-reason for every file." },
    { id: "A0-3", text: "Every final file is readable and matches its declared format and dimensions.", how: "Open each file with a format-aware parser and compare measured properties with the deliverable manifest." },
  ];
  const processBaseline = [
    { text: "Every required connector operation has a normalized execution record.", how: "Record the operation name, input asset IDs, output artifact IDs, completion state, retry count, and any exception without relying on host-specific response wording." },
    { text: "Material creative decisions are traceable to evidence and alternatives.", how: "For each decision gate, record the alternatives compared, the selected option, the evidence used, and the condition that would trigger a revisit." },
    { text: "The revision loop closes every failed production or craft gate.", how: "Link each failed check to a corrective action, a new artifact version, and the subsequent passing result; unresolved failures must remain declared exceptions." },
  ];
  const auto = uniqueChecks([...baseline, ...artifactSafe]).slice(0, 7).map((item, index) => ({ ...item, id: `A${index + 1}` }));
  const processChecks = uniqueChecks([...processBaseline, ...process]).slice(0, 7).map((item, index) => ({ ...item, id: `P${index + 1}` }));
  const humanCandidates = (spec.verifiers_human || []).filter((item) => !referencesExcluded(`${item.text} ${item.how}`, spec)).map((item, index) => ({ item, index, score: relevanceScore(`${item.text} ${item.how}`, deliverables) })).sort((a, b) => b.score - a.score || a.index - b.index).map(({ item }) => item);
  const humanFallback = [
    { text: "The scoped deliverables read as one deliberate professional system rather than unrelated outputs.", how: "Review the final package side by side at the sizes and in the sequence the audience will encounter it." },
    { text: "The work remains clear and credible at its actual delivery sizes.", how: "Judge hierarchy, edge quality, legibility, pacing, and reproduction behavior in the final contexts rather than only at full-canvas zoom." },
    { text: "The creative direction fits the stated client, audience, and price position.", how: "Compare the final system with the supplied brand references and business context, then identify any generic or off-brand choice." },
  ];
  const humanRanked = uniqueChecks([...humanCandidates, ...humanFallback]).slice(0, 5).map((item, index) => ({ ...item, id: `H${index + 1}` }));
  return {
    version: "3.1",
    ranking_rule: "Rank agents first on host-neutral final artifacts. Report connector completion and normalized process quality as separate dimensions.",
    scoring: { artifact_checks: 35, human_craft_review: 35, connector_completion: 15, normalized_process_quality: 15 },
    artifact_checks: auto,
    human_craft_checks: humanRanked,
    normalized_process_checks: processChecks,
    acceptance_snapshot: acceptance,
  };
}

function truthConstraints(spec, deliverables) {
  const family = familyKey(spec);
  const scoped = JSON.stringify(deliverables).toLowerCase();
  const lines = [
    "Do not invent names, prices, claims, product features, locations, credentials, records, or documentary events that are absent from the approved inputs.",
    "Do not silently replace a weak supplied asset. Use it honestly, reject it with a reason, or take only the brief's declared Stock or concept exception.",
    "Record every omission, substitution, reconciliation, and material quality compromise in the delivery manifest.",
  ];
  if (family === "Photo & Imaging") lines.push("Preserve identity, product geometry, material behavior, and documentary truth; retouching may improve presentation but may not change what the subject is.");
  if (family === "Layout & Data" && /data.?merge/.test(scoped)) lines.push("Reconcile records before merge and prove page, row, name, and amount completeness from the delivered artifacts.");
  if (family === "Layout & Data" && !/data.?merge/.test(scoped)) lines.push("Preserve approved copy, dimensions, hierarchy, and reproduction requirements; do not imply a data merge or editable system that is outside the scoped deliverables.");
  if (family === "Vector & Identity") lines.push("Recover only features supported by the references; do not describe an automatic trace as engraving, cutting, embroidery, or press ready without inspectable path evidence.");
  if (family === "Motion & Video") lines.push("Treat measured file duration and stream metadata as authoritative. Do not infer spoken content from silent clips or use a visual summary as a transcript.");
  if (spec.new_id === "PHOTO-03") lines.push("A clipped white window contains no recoverable view; recompose or disclose it instead of generating a fictitious exterior.");
  if (spec.new_id === "PHOTO-05") lines.push("Generated sky or architecture may be presented only as a clearly labeled concept, never as truthful property photography.");
  if (spec.new_id === "PHOTO-10" || spec.new_id === "PHOTO-11") lines.push("Color variants are approval concepts until physical samples are photographed and signed off.");
  if (spec.new_id === "PHOTO-16") lines.push("An obscured grading or compliance label must be rejected for reshoot, not reconstructed from guesswork.");
  if (spec.new_id === "PHOTO-27") lines.push("A missing flavor or packshot remains a declared content gap; do not fabricate a sellable product image.");
  return lines;
}

function allowedExceptions(spec) {
  const list = [
    "Reject an unusable source file with a precise reason and continue with the remaining scoped package.",
    "Deliver a type-led or layout-led fallback when imagery cannot support a truthful result.",
    "Defer printer, fabricator, color, legal, accessibility, or physical-sample approval when the supplied evidence cannot establish it.",
  ];
  if (stock.has(spec.new_id)) list.push("License one or more representative Adobe Stock assets only for the gap named in the brief, with asset IDs and representative-use disclosure.");
  if (spec.new_id === "PHOTO-11" || spec.new_id === "PHOTO-10") list.push("Deliver clearly watermarked concept-color proofs pending physical sample approval.");
  return list;
}

function primaryProblem(spec, deliverables) {
  const family = familyKey(spec);
  const base = {
    "Photo & Imaging": "Create a coherent, truthful image system from inconsistent source photography and prove it at the actual delivery sizes.",
    "Vector & Identity": "Recover production artwork from imperfect physical references while separating faithful reconstruction from unsupported fabrication claims.",
    "Layout & Data": "Turn legacy artwork and structured client data into an accurate, editable production system without silent record, overflow, or output errors.",
    "Motion & Video": "Build a deliberate short-form edit from the finite supplied media and verify pacing, framing, and audio against the final aspect ratios.",
  }[family];
  return `${base} The lead output is ${deliverables[0].name}.`;
}

function budgetAndTimeline(spec, tier) {
  const family = familyKey(spec);
  return {
    engagement: "One-off fixed-price expert commission",
    modeled_marketplace_budget: budgets[family][tier],
    delivery_window: tiers[tier].timeline,
    revision_structure: tiers[tier].revisions,
    scope_change_policy: "New deliverable classes, new source creation, extra records, and client copy changes after approval are quoted separately.",
  };
}

function assetUsePlan(spec, deliverables) {
  const scope = JSON.stringify(deliverables).toLowerCase();
  const needsRaster = /graded raster|photography|image set|thumbnail|cutout|isolation/.test(scope);
  const needsVector = /vector artwork|\bmark\b|\bcrest\b|\bwordmark\b|\bmonogram\b|\bglyph\b|emblem/.test(scope);
  const needsData = /data.?merge/.test(scope);
  const needsExpress = /express template/.test(scope);
  const needsMotion = /video|motion|animated/.test(scope);
  const imagePattern = /photos?|images?|frames?|shots?|captures?|stills?|portraits?|\.jpe?g|\.png|\.tiff?|\.svg|scan|sign|stamp|patch|plaque|mark|crest|wordmark|monogram|render/i;
  const vectorPattern = /mark|crest|wordmark|monogram|glyph|stamp|sign|plaque|patch|logo|emblem|artwork/i;
  const dataPattern = /\.csv|\.xlsx?|roster|schedule|rates|register|bookings|listings|records|data|merge/i;
  const legacyLayoutPattern = /\.pdf|press|print|printer|template|card|sheet|label|programme|catalog/i;
  const copyPattern = /\.txt|\.md|copy|note|brief|style|brand|spec|requirements|placements|caption|rundown|shotlist/i;
  const motionPattern = /source_video|source_audio|motion_source_metadata|\.mp4|\.mov|\.wav/i;

  const plan = spec.assets_supplied.map((asset) => {
    const text = `${asset.name} ${asset.kind}`;
    let expected_role = "required_reference";
    let rationale = "Supplies approved context, copy, brand direction, placement rules, or comparison evidence for the scoped work.";
    if (needsMotion && motionPattern.test(text)) {
      expected_role = "production_input";
      rationale = "Provides the measured picture, audio, or timing evidence used by the scoped motion deliverable.";
    } else if (needsMotion && (copyPattern.test(text) || dataPattern.test(text) || legacyLayoutPattern.test(text))) {
      expected_role = "required_reference";
      rationale = "Supplies approved copy, timing, shot, claim, placement, or brand guidance for the scoped motion package.";
    } else if (needsData && (dataPattern.test(text) || legacyLayoutPattern.test(text))) {
      expected_role = "production_input";
      rationale = "Provides the records or legacy production artwork required for the scoped merge run.";
    } else if (needsVector && vectorPattern.test(text)) {
      expected_role = "production_input";
      rationale = "Provides visual evidence for the scoped artwork recovery; unsupported features may not be invented.";
    } else if (needsRaster && imagePattern.test(text)) {
      expected_role = "production_input";
      rationale = "Provides source pixels for the scoped image system, isolation, restoration, or placement output.";
    } else if (needsExpress && (copyPattern.test(text) || imagePattern.test(text))) {
      expected_role = "production_input";
      rationale = "Provides approved copy, imagery, or brand direction for the scoped template adaptation.";
    } else if ((dataPattern.test(text) || legacyLayoutPattern.test(text)) && !needsData && !needsExpress) {
      expected_role = "out_of_scope_reference";
      rationale = "Belongs to a deliverable class removed during scope correction; retain for provenance but do not transform or score it.";
    }
    return { name: asset.name, expected_role, rationale };
  });
  if (!plan.some((item) => item.expected_role === "production_input")) {
    plan[0].expected_role = "production_input";
    plan[0].rationale = "Primary supplied source for the lead scoped deliverable.";
  }
  return plan;
}

function projectOverview(spec, deliverables) {
  const brand = spec.brand_identity.brand_name;
  const names = deliverables.map((d) => d.name);
  const list = names.length === 2 ? `${names[0]} and ${names[1]}` : `${names.slice(0, -1).join(", ")}, and ${names.at(-1)}`;
  return `${sentence(spec.brand_identity.about, 210).trim()} We are hiring an expert to turn the supplied working files into ${list}.`;
}

function marketplaceBrief(spec, deliverables, tier, constraints, terms, motionFact, assetPlan) {
  const family = familyKey(spec);
  const brand = spec.brand_identity.brand_name;
  const overview = projectOverview(spec, deliverables);
  const requiredAssets = assetPlan.filter((asset) => asset.expected_role !== "out_of_scope_reference").map((asset) => asset.name).join("; ");
  const referenceAssets = assetPlan.filter((asset) => asset.expected_role === "out_of_scope_reference").map((asset) => asset.name);
  const referenceNote = referenceAssets.length ? `\n\nAdditional archive files\n${referenceAssets.join("; ")}. These files are supplied for provenance only because their former deliverable class is outside this commission. Do not silently turn them into extra scope.` : "";
  const scope = deliverables.map((d) => `- ${d.name}: ${sentence(d.spec)}`).join("\n");
  const prioritizedConstraints = [constraints[0], constraints[1], constraints[3], constraints.at(-1)].filter(Boolean);
  const keyConstraints = [...new Set(prioritizedConstraints)].slice(0, 4).map((line) => `- ${line}`).join("\n");
  const audioCount = motionFact?.summary.separate_audio_file_count || 0;
  const videoCount = motionFact?.summary.video_file_count || 0;
  const mediaNote = family === "Motion & Video" ? `\n\nSource-media note\nThe supplied package contains ${videoCount} video file${videoCount === 1 ? "" : "s"} totaling ${motionFact?.summary.total_video_seconds || 0} seconds, ${motionFact?.summary.video_files_with_audio_streams || 0} with embedded audio, and ${audioCount} separate audio file${audioCount === 1 ? "" : "s"}. These measured values are the production limits.` : "";
  return `${brand}: ${shortName(deliverables[0].name, brand)}\n\nProject overview\n${overview}\n\nWhat we will provide\n${requiredAssets}. Every file must be accounted for in the final manifest; it may be used, retained as reference, superseded, or rejected with a reason.${referenceNote}\n\nScope and deliverables\n${scope}\n\nNon-negotiables\n${keyConstraints}${mediaNote}\n\nWorking process\nPlease begin with an inventory and risk pass, submit the first proof or direction at the stated checkpoint, then revise against consolidated feedback. We are hiring for judgment: flag contradictions early, make the strongest defensible choice, and document any source limitation rather than hiding it.\n\nContract\n${terms.modeled_marketplace_budget}; target delivery ${terms.delivery_window}; ${terms.revision_structure.toLowerCase()}. Final handoff includes the delivery manifest, editable sources where scoped, final exports, and a concise production note.`;
}

function trajectoryFor(spec, profile, motionFact) {
  const family = familyKey(spec);
  const steps = [
    { step: 1, phase: "Intake and evidence", action: "Inventory every supplied file, measure formats and dimensions, and record an intended disposition before editing.", decision: "Resolve contradictions between filenames, visible content, client data, and measured properties before committing to a direction.", evidence: "Input inventory, risk register, and source-of-truth decision." },
    { step: 2, phase: "Direction", action: "Choose the visual or editorial target from the brief, brand identity, audience, and actual source quality.", decision: "Make one explicit lead-direction choice and state what the work must avoid at the client's price position.", evidence: "Direction note and representative proof." },
    { step: 3, phase: "Primary craft pass", action: `Execute the lead craft problem through ${profile.required_operations.slice(0, 5).join(", ")}.`, decision: "Use only operations justified by a source defect or a scoped deliverable, keeping the first pass reversible and reviewable.", evidence: "First-pass master assets and operation record." },
    { step: 4, phase: "Reconciliation", action: family === "Layout & Data" ? "Reconcile client records, legacy artwork, field mapping, and page structure before generating the production run." : family === "Motion & Video" ? "Reconcile measured clip durations, EDL ranges, aspect ratios, and any separate narration before rendering." : family === "Vector & Identity" ? "Compare recovered geometry with every reference and separate evidence-based contours from assumptions." : "Compare the set at delivered size and reconcile outliers, edge failures, identity drift, and unsupported corrections.", decision: "Stop, disclose, or take an allowed exception when the source cannot support the requested truth claim.", evidence: "Reconciliation table and exception decisions." },
    { step: 5, phase: "Production build", action: "Build the remaining scoped deliverables from approved masters, preserving exact copy, records, naming, and output dimensions.", decision: "Keep derivatives traceable to approved masters and prevent a supporting output from changing the primary craft decision.", evidence: "Complete first-production package." },
    { step: 6, phase: "Artifact QA and loop", action: "Open and inspect every final artifact with format-aware checks and at real viewing or reproduction size; correct failures and repeat the checks.", decision: "A successful connector response is not acceptance evidence. The delivered artifact itself must pass.", evidence: "QA report with before/after failure disposition." },
    { step: 7, phase: "Handoff", action: "Package final exports, scoped editable sources, manifest, licensing or provenance records, EDL or mapping evidence where relevant, and the production note.", decision: "Name every remaining limitation and do not overstate press, fabrication, legal, color, or documentary approval.", evidence: "Final delivery package and signed-off manifest." },
  ];
  if (family === "Motion & Video") steps[2].action += ` The source authority is motion_source_metadata.json (${motionFact?.summary.total_video_seconds || 0} total video seconds).`;
  return steps;
}

function remapCheckpoints(spec, trajectory) {
  const existing = (spec.emergent_checkpoints || []).slice(0, 3);
  const targets = [3, 5, 6];
  return existing.map((checkpoint, index) => ({ ...checkpoint, fires_after_step: targets[index] || trajectory.length - 1 }));
}

function motionCheckpoints(spec, motionFact) {
  const hasAudio = (motionFact?.summary.separate_audio_file_count || 0) > 0;
  return [
    {
      fires_after_step: 3,
      what_can_only_be_learned_by_running: "Which visible beats in the measured short clips actually cut together without a continuity jump, duplicate action, or missing subject.",
      why_unavoidable: "Filenames and source duration do not establish visual continuity. The first assembled proof is the earliest reliable evidence.",
      likely_rework: "Replace or reorder source ranges, shorten the piece, and rebuild the EDL around the strongest continuous action.",
      failure_if_undetected: "A technically valid render feels accidental or implies an action that the source never completes.",
    },
    {
      fires_after_step: 5,
      what_can_only_be_learned_by_running: "Whether the approved horizontal composition survives the required vertical or square reframe with the subject and essential interface or product detail still visible.",
      why_unavoidable: "The crop depends on the actual chosen ranges and subject position inside each rendered frame.",
      likely_rework: "Choose a different source range for the platform version or use fit instead of fill and revise the surrounding design treatment.",
      failure_if_undetected: "The platform export is correctly sized but loses the person, product, or interface that gives the shot meaning.",
    },
    {
      fires_after_step: 6,
      what_can_only_be_learned_by_running: hasAudio ? "Whether the separately supplied audio remains intelligible and appropriately synchronized after the final duration and crop decisions." : "Whether the silent final piece still communicates clearly without implying dialogue, ambience, or music that was never supplied.",
      why_unavoidable: "This can be judged only on the final rendered sequence, not from a successful operation response.",
      likely_rework: hasAudio ? "Rebalance or shorten the selected audio passage and render again against the locked picture." : "Strengthen visual sequencing or approved on-screen copy without fabricating a soundtrack.",
      failure_if_undetected: hasAudio ? "The picture is polished but the spoken information is clipped, mistimed, or inconsistent." : "The deliverable relies on absent sound and fails when viewed as supplied.",
    },
  ];
}

function motionDecisionGates(motionFact) {
  return [
    `How much finished runtime the ${motionFact?.summary.total_video_seconds || 0} measured source seconds can honestly support.`,
    "Which source ranges carry complete visible actions rather than attractive but contextless fragments.",
    "Whether the primary edit needs an explicit timeline or qualifies for visually led Quick Cut selection.",
    "Which shots survive the platform reframe without enlargement or loss of the subject.",
    "Whether a separate audio file is usable for the scoped duration, and what must remain silent when no source audio exists.",
    "Which poster frames remain legible and representative at feed size.",
  ];
}

function normalizeMotionAssets(spec, motionFact) {
  const isLegacyMotionEntry = (asset) => /\.mp4|\.mov|\.wav|\bclips?\b|\btakes?\b|recordings?|episodes?|b[ -]?roll|walkthrough|gameplay captures/i.test(asset.name);
  const kept = spec.assets_supplied.filter((asset) => !isLegacyMotionEntry(asset) && asset.name !== "motion_source_metadata.json");
  const video = motionFact.files.filter((entry) => entry.streams.some((stream) => stream.codec_type === "video"));
  const audio = motionFact.files.filter((entry) => entry.streams.some((stream) => stream.codec_type === "audio") && !entry.streams.some((stream) => stream.codec_type === "video"));
  const canonical = [];
  if (video.length) canonical.push({
    name: `source_video_files/ (${video.length} measured short file${video.length === 1 ? "" : "s"})`,
    kind: "Short supplied video rushes; exact durations, dimensions, frame rates, codecs, and stream presence are recorded in motion_source_metadata.json.",
    visible_description: video.map((entry) => entry.filename).join(", "),
    hidden_defect: "Coverage is finite and every source video is silent. The edit must be planned from measured media rather than legacy narrative labels.",
  });
  if (audio.length) canonical.push({
    name: `source_audio_files/ (${audio.length} measured WAV file${audio.length === 1 ? "" : "s"})`,
    kind: "Separately supplied audio; exact durations and stream properties are recorded in motion_source_metadata.json.",
    visible_description: audio.map((entry) => entry.filename).join(", "),
    hidden_defect: "Separate audio may be longer than the available picture and must be deliberately excerpted or reported as unused.",
  });
  canonical.push({
    name: "motion_source_metadata.json",
    kind: "machine-readable source inventory",
    visible_description: "Measured duration, stream, dimensions, frame-rate and audio-presence facts for every supplied motion file. This file is authoritative for edit planning.",
    hidden_defect: "",
  });
  return [...canonical, ...kept];
}

function alignSeries(spec) {
  const entry = series[spec.new_id];
  if (!entry) return null;
  const [seriesId, commissionRole, canonicalContext] = entry;
  return {
    series_id: seriesId,
    relationship: "Distinct commission in a repeat-client series; score independently and do not reuse deliverables from the companion task.",
    commission_role: commissionRole,
    canonical_client_context: canonicalContext,
  };
}

function assetReadiness(spec, motionFact) {
  const dir = path.join(assetsRoot, spec.new_id, "assets");
  const names = fs.existsSync(dir) ? fs.readdirSync(dir).filter((name) => !name.startsWith(".")).sort() : [];
  return {
    status: "validated and ready with intentional production edge cases",
    physical_file_count: names.length,
    validation_date: "2026-09-15",
    file_integrity: "All supplied files passed format-aware validation in the freeze audit.",
    visual_review: "Image and document packs were contact-sheet reviewed; apparent limitations are retained only where they create a realistic expert decision.",
    accountability_rule: "Every physical input must receive a final disposition: used, reference-only, superseded, or rejected with reason.",
    ...(motionFact ? { motion_truth: motionFact.summary, canonical_motion_metadata: "motion_source_metadata.json" } : {}),
  };
}

const rewritten = [];
const matrix = [];
const allocation = [];
const namingRegistry = [];

for (const file of files) {
  const filePath = path.join(specsDir, file);
  const fileId = path.basename(file, ".json");
  const spec = structuredClone(sourceById.get(fileId));
  if (!spec) throw new Error(`Aggregate source is missing ${fileId}`);
  const id = spec.new_id;
  const family = familyKey(spec);
  const tier = tierKey(id);
  const motionFact = family === "Motion & Video" ? measuredMotion(id) : null;
  const seriesInfo = alignSeries(spec);
  if (seriesInfo) {
    spec.brand_identity.about = `${spec.brand_identity.brand_name} is the repeat client for this benchmark series. The canonical client context is ${seriesInfo.canonical_client_context}, and this commission covers ${seriesInfo.commission_role.toLowerCase()}.`;
    spec.brand_identity.founded_place_size = `${seriesInfo.canonical_client_context}; canonical context for the repeat-client series.`;
  }
  if (motionFact) spec.assets_supplied = normalizeMotionAssets(spec, motionFact);
  const deliverables = chooseDeliverables(spec, tier, motionFact);
  const identity = canonicalTaskIdentity(spec, deliverables[0]);
  const constraints = truthConstraints(spec, deliverables);
  const acceptance = acceptanceFor(spec, deliverables);
  const profile = operationsFor(spec, deliverables, motionFact);
  const terms = budgetAndTimeline(spec, tier);
  const assetPlan = assetUsePlan(spec, deliverables);
  const title = marketplaceTitle(spec, deliverables[0], family);
  const trajectory = trajectoryFor(spec, profile, motionFact);
  const verifiers = verifierContract(spec, deliverables, acceptance);

  const out = {
    schema_version: "3.1",
    revision_date: "2026-09-15",
    new_id: id,
    task_code: identity.task_code,
    task_name: identity.task_name,
    global_order: identity.global_order,
    family_code: identity.family_code,
    legacy_id: identity.legacy_id,
    storage: {
      bucket: "annotationprod",
      region: "ap-south-1",
      folder: identity.storage_folder,
      s3_prefix: identity.s3_prefix,
    },
    family: spec.family,
    complexity_tier: tiers[tier].label,
    engagement_title: `${identity.task_code}: ${identity.task_name}`,
    marketplace_listing: {
      title,
      experience_level: "Expert",
      project_type: "One-off project",
      engagement_model: "Fixed price with milestone approvals",
      overview: projectOverview(spec, deliverables),
      deliverables: deliverables.map((d) => d.name),
      terms,
      applicant_signal: `Show directly comparable ${family.toLowerCase()} work and explain one source limitation you would test before production. Generic portfolios without production evidence are not sufficient.`,
    },
    vertical: spec.vertical,
    primary_craft_problem: primaryProblem(spec, deliverables),
    client_one_liner: family === "Motion & Video" ? `${spec.brand_identity.brand_name} needs a polished short-form package built only from the supplied short clips, stills, and separate audio where present.` : cleanText(spec.client_one_liner),
    client_brief: marketplaceBrief(spec, deliverables, tier, constraints, terms, motionFact, assetPlan),
    project_terms: terms,
    source_provenance: {
      type: "source-derived composite marketplace brief",
      statement: "The scenario is synthesized from the repository's laundered Upwork and Freelancer source anchors. It is not represented as a verbatim live listing.",
      original_anchor: spec.real_brief_anchor,
    },
    real_brief_anchor: spec.real_brief_anchor,
    price_band_and_audience: spec.price_band_and_audience,
    brand_identity: spec.brand_identity,
    ...(seriesInfo ? { client_series: seriesInfo } : {}),
    assets_supplied: spec.assets_supplied,
    asset_use_plan: assetPlan,
    asset_readiness: assetReadiness(spec, motionFact),
    truth_constraints: constraints,
    allowed_exception_states: allowedExceptions(spec),
    deliverables,
    handover_requirements: {
      required: true,
      contents: ["delivery manifest", "scoped editable sources", "final exports", "production and exception note", ...(stock.has(id) ? ["Stock license and asset IDs"] : []), ...(family === "Motion & Video" ? ["final EDL and measured source metadata"] : []), ...(dataMerge.has(id) ? ["normalized data file and mapping record"] : [])],
      note: "Handover is a professional completion requirement and is not counted as a separate creative deliverable class.",
    },
    acceptance_bar: acceptance,
    connector_profile: profile,
    adobe_surfaces: surfaceGroups(profile),
    trajectory,
    emergent_checkpoints: family === "Motion & Video" ? motionCheckpoints(spec, motionFact) : remapCheckpoints(spec, trajectory),
    decision_gates: family === "Motion & Video" ? motionDecisionGates(motionFact) : (spec.decision_gates || []).filter((line) => !referencesExcluded(line, spec)).slice(0, 8),
    verifier_contract: verifiers,
    verifiers_auto: verifiers.artifact_checks,
    verifiers_process: verifiers.normalized_process_checks,
    verifiers_human: verifiers.human_craft_checks,
    why_not_vlm: family === "Motion & Video" ? "A generated video would replace the supplied people, products, interfaces, locations, and finite recorded actions rather than edit them. This task is scored on traceability to measured source ranges, final framing, and truthful use of separate audio, which a newly generated clip cannot satisfy." : spec.why_not_vlm,
    doability_proof: {
      status: "doable with the current ChatGPT Adobe connector profile and declared exception paths",
      host_profile: profile.profile_id,
      proof: ["Every required operation is present in the captured 99-tool ChatGPT Adobe inventory.", "The client brief is host-neutral; connector-specific scoring is isolated in connector_profile and verifier_contract.", "Artifact acceptance never depends on a raw connector response field.", "Unsupported truth, fabrication, press, legal, or color claims have an explicit defer or disclose state."],
      residual_limits: ["Express work is template adaptation, not unrestricted canvas authoring.", "Quick Cut is used only for visually led selection and never as semantic speech editing.", "Automatic vectorization does not independently establish fabrication readiness.", "Interactive Acrobat page-organization operations are excluded from zero-human execution."],
    },
    acceptance_bar_note: "The acceptance bar applies only to the scoped deliverables above. Hidden defects and connector quirks remain benchmark-internal and are not leaked into the client-facing brief.",
  };

  fs.writeFileSync(filePath, `${JSON.stringify(out, null, 1)}\n`);
  rewritten.push(out);
  namingRegistry.push(identity);
  allocation.push({ task_code: identity.task_code, task_name: identity.task_name, legacy_id: id, s3_prefix: identity.s3_prefix, tier: tiers[tier].label, primary_surface: family, required_operations: profile.required_operations, conditional_operations: profile.conditional_operations });
  matrix.push({
    task_code: identity.task_code,
    task_name: identity.task_name,
    global_order: identity.global_order,
    family_code: identity.family_code,
    legacy_id: id,
    s3_prefix: identity.s3_prefix,
    tier: tiers[tier].label,
    title,
    deliverable_count: deliverables.length,
    deliverables: deliverables.map((d) => d.name).join(" | "),
    physical_asset_count: out.asset_readiness.physical_file_count,
    required_operation_count: profile.required_operations.length,
    conditional_operation_count: profile.conditional_operations.length,
    uses_stock: stock.has(id),
    uses_boards: boards.has(id),
    uses_express: express.has(id),
    uses_data_merge: dataMerge.has(id),
    client_series: seriesInfo?.series_id || "",
  });
}

fs.writeFileSync(path.join(repo, "complex_benchmark/adobe_only/TASKS_V3_ALL100.json"), `${JSON.stringify(rewritten, null, 1)}\n`);
fs.writeFileSync(path.join(auditDir, "ADOBE_CONNECTOR_ALLOCATION_V3_1.json"), `${JSON.stringify({ generated_at: "2026-09-15", host_profile: "chatgpt-adobe-2026-09-15", tasks: allocation }, null, 2)}\n`);
fs.writeFileSync(path.join(auditDir, "TASK_PORTFOLIO_MATRIX_V3_1.json"), `${JSON.stringify(matrix, null, 2)}\n`);
fs.writeFileSync(path.join(auditDir, "TASK_NAMING_REGISTRY_V3_1.json"), `${JSON.stringify(namingRegistry.sort((a, b) => a.global_order - b.global_order), null, 2)}\n`);

const csvCell = (value) => `"${String(value ?? "").replaceAll('"', '""')}"`;
const headers = Object.keys(matrix[0]);
const csv = [headers.map(csvCell).join(","), ...matrix.map((row) => headers.map((header) => csvCell(row[header])).join(","))].join("\n");
fs.writeFileSync(path.join(auditDir, "TASK_PORTFOLIO_MATRIX_V3_1.csv"), `${csv}\n`);
const namingHeaders = Object.keys(namingRegistry[0]);
const namingCsv = [namingHeaders.map(csvCell).join(","), ...namingRegistry.map((row) => namingHeaders.map((header) => csvCell(row[header])).join(","))].join("\n");
fs.writeFileSync(path.join(auditDir, "TASK_NAMING_REGISTRY_V3_1.csv"), `${namingCsv}\n`);
fs.writeFileSync(path.join(auditDir, "ADOBE_CHATGPT_TOOL_INVENTORY_2026-09-15.json"), `${JSON.stringify({ captured_at: "2026-09-15", count: currentTools.size, tools: [...currentTools].sort() }, null, 2)}\n`);

console.log(`Rewrote ${rewritten.length} tasks to schema 3.1.`);
