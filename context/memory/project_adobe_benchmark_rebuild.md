---
name: project_adobe_benchmark_rebuild
description: "Ongoing rebuild of all 100 Adobe StudioBench tasks to be non-trivial (hard for humans AND the agent), connector-doable, and IP-safe; wave/verify state + the connector-limit rules"
metadata: 
  node_type: memory
  type: project
  originSessionId: d469daaa-e33b-4c81-a609-3bdc7c1f159d
  modified: 2026-09-01T10:53:03.355Z
---

Dhiren's directive (this session): **make every one of the 100 Adobe tasks non-trivial — hard for a skilled human AND hard for Claude — while staying 100% connector-doable and IP-safe.** Triggered by the quality audit (see [[project_adobe_v21_dataset]] context): [TASK_QUALITY_AUDIT.md] found only 5 PASS / 66 STRENGTHEN / 29 REPLACE, and the exemplar re-challenge found **0 defensible exemplars**. Specs were unchanged since 2026-08-26, so the audit is current.

## Where things live (repo: /Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads)
- **Guidance (read before every rebuild):** `complex_benchmark/adobe_only/REBUILD_GROUND_TRUTH.md` (connector CAN/CANNOT boundary) and `REBUILD_HARDNESS_BAR.md` (6 gates + human-hard + measurability + IP rule). These accreted every lesson below.
- **Rebuilt specs:** `complex_benchmark/adobe_only/specs_rebuilt/` (originals in `specs/` are UNTOUCHED — diff before any swap). Not a git repo, so the separate dir is the only safety net.
- **Per-task dossiers:** `complex_benchmark/adobe_only/rebuild_dossiers/<AO-ID>.json`.

## Method (per wave)
A `Workflow` pipeline: `general-purpose` agents at effort:high rebuild each spec (read guidance + dossier + audit + current spec + a passing sibling), write it to `specs_rebuilt/`, self-check. Then an **adversarial skeptic** agent tries to break each on 6 lenses (agent-triviality, connector-doability, creative-substance, human-hard, ip_safe, no_agent_measurement). Revise until `holds_up`. Nothing counts as done until a skeptic fails to break it.

## Wave plan + confirmed count (update as waves land)
- **Wave 1 = 14 exemplar-tier: DONE 14/14.**
- **Wave 2 = 29 REPLACE: DONE 29/29** (Tier A+B wave2a 16 ✓; Tier C+D wave2b 13 ✓, AO-06 was the last).
- **Wave 3 = 57 STRENGTHEN.** 3a DONE 15/15. 3b DONE 10/15; 5 stragglers still failing (fixes known below). 3c/3d hit the SESSION USAGE LIMIT mid-run (resets 4:20pm Asia/Calcutta) — partial.
- **Confirmed (passed a skeptic): 68/100. Written-to-disk-but-unverified: 21. NOT rebuilt (11): AO-86,87,88,90,97,105,111,120,121,122,123.**
- **RESUME PLAN after limit reset:** (1) rebuild the 11 missing (STRENGTHEN, use wave3c/3d script via scriptPath resume or fresh); (2) fix the 5 wave-3b stragglers with these KNOWN issues → AO-29: 2:3 source is narrower than A3 so full-bleed A3 upscales on WIDTH — declare source short-edge ≥~3579px (also "Continental Cup" collides w/ real events; one_line_ask softly leaks crest triage); AO-45: full_brief still leaks the hi-vis-tee "do not chase a cast" answer → move to realism_notes; AO-49: decoy named `_photo.jpg` among `_scan.png` (filename+ext telegraph) + CSV says "halftone" → neutral same-ext names + drop "halftone" from roster; AO-51: "Vanguard" is a real trademark → coin a distinctive name; AO-52: uses image_apply_color_overlay (whole-image,no opacity) to key 2 halftone plates → flattens dots to a solid rectangle → use image_apply_monochromatic_tint for all inks; (3) run ONE final full-corpus adversarial sweep over all 100 (also catches latent early-pass issues like AO-74's original upscaling); (4) restore AO-23 YouTube/LinkedIn (over-laundered before the social-yes rule); (5) regenerate derived artifacts (task_tags_v3, docs site, Quality_QA_Report) from specs_rebuilt; (6) hand-off list of ASSET-PIPELINE production still owed.
- **IP policy (owner's decision "social yes, marketplaces no"):** name freely = Adobe's own apps (Photoshop/Lightroom/InDesign/…) + social/video PLATFORMS as format descriptors (Instagram/YouTube/TikTok/LinkedIn/Facebook). Launder = marketplaces (Shopify/Amazon/eBay/Etsy → "online store") + every real company/person/athlete/org/school/product/model/standard (a "fictional" brand must be a coined name not a real trademark, e.g. DermaVera turned out real). gen_model exempt.

## The connector-limit rules the skeptics forced out (all now in the guidance)
- **Agent NEVER measures pixels** (no eyedropper/hex/channel/luminance read). It neutralises a grey card BY EYE and reports only the params it APPLIED; numeric tolerances are the GRADER's check.
- **Grade the card where it still exists:** if the grey card is cropped out of the deliverable, grade neutrality on a RETAINED card-bearing master (a named output), check card-exclusion on the crop separately.
- **No per-record named export** — `document_render_layout` exports the WHOLE merged doc; a "hero" is just page 1.
- **InDesign merge = one record per page**, exported to one PDF; page-count=row-count is a valid gate; cannot put multiple records on one page; `convert_pdf_to_indd` banned as merge target; `document_merge_data_vector` is text-only.
- **Agent-produced SVG marks into a layout ONLY via a merge @-image column** (AO-75 binds two: @Portrait+@TierBadge). Never free-form placement.
- **Print/high-DPI ⇒ camera-scale inputs** (~3000-4500px); `image_crop_and_resize` never upscales.
- **`image_adjust_hsl` ≤ ~90° hue rotation** (desaturate-to-metal or adjacent shift; NOT amber→teal or red→green).
- **Brief states GOALS not methods** — never disclose the triage answer / trap / per-frame correction; keep the trap in inputs+hardness_rationale only.
- **Video:** `video_create_quick_cut` only SHORTENS one clip (no assemble/lengthen; source>target); `video_resize` never upscales (a 9:16 vertical needs a 4K source, not a 1080p master); no motion-graphics/compositing.
- **`image_remove_background` can't punch enclosed interior holes** (die-cut slots, letter counters).
- Passing siblings to clone: AO-74 (datamerge print), AO-17/AO-20 (grade-to-one-look batch), AO-39/AO-75 (triage+merge), AO-110 (masked-HSL recolor kernel).

## Still pending after the waves
Regenerate derived artifacts from the rebuilt specs (task_tags_v3, docs site, QA report); run one FINAL full-corpus adversarial sweep with mature guidance (early wave-1 passes like AO-74 had latent defects caught only on re-open, so a uniform final pass matters); then flag the ASSET-PIPELINE production that must follow (real authored .indd templates with @-image columns, regenerated camera-scale/batch/video source assets) — that is production, NOT spec design, and must not be claimed as done. See [[project_studiobench_input_assets]] for the asset pipeline.
