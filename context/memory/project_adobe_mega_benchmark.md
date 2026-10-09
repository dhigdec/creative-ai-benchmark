---
name: project-adobe-mega-benchmark
description: Round-4 complex long-horizon mega-task benchmark (7 tasks) maxing the full Adobe connector suite + video/audio; built 2026-06-14
metadata: 
  node_type: memory
  type: project
  originSessionId: 32deee17-7cef-4cd9-a898-2dd5e9832c61
---

# Adobe MEGA-benchmark — long-horizon, full-suite tasks (2026-06-14)

Follows [[project-adobe-flagship-executions]]. User feedback: prior tasks used only ~7 of ~50
connectors (the trivial ones); wanted COMPLEX long-horizon tasks with MANY connectors each,
iterative output→input chaining, many input assets used across most steps, AND video/audio
tasks (generate the video as input assets too). "Maximum utilization of the Adobe creativity suite."

## Feasibility resolved (probed live on the keys)
- **Video gen works**: Veo 3 fast (`veo-3.0-fast-generate-001`, google-genai 1.47, `generate_videos`
  + `client.operations.get` polling) → 8s 720p H.264 with NATIVE AAC audio, ~90s/clip, photoreal.
  OpenAI **Sora-2** (`client.videos.create/retrieve/download_content`) → short clips, photoreal.
- **Audio**: OpenAI TTS `gpt-4o-mini-tts` → voiceover mp3.
- **ffmpeg**: not on PATH; use `imageio-ffmpeg` (`get_ffmpeg_exe()`) — installed in the venv.
- Probe frames + scripts saved under `complex_benchmark/probes/`; probe scripts `/tmp/veo_probe.py`,
  `/tmp/oai_probe.py`.

## Connector audit
Used so far (7): remove_background, apply_auto_tone, vectorize, crop_and_resize,
adjust_color_temperature, adjust_vibrance_and_saturation, generative_expand. **34 advanced tools
NEVER used** (masking, lens/gaussian blur, fine tonal adjusts, single_color_saturation, presets,
auto_straighten, crop_to_bounds, halftone/duotone/glitch/grain/noise, fill_area, stock
search+license, data-merge layout+vector + renders, font_recommend, all 4 video/audio).

## The benchmark: `complex_benchmark/mega_benchmark.json` (7 mega-tasks)
Each 13–19 connectors, iterative chains, 6–33 inputs across image/data/video/audio. Built by the
`mega-benchmark-mining` workflow (8 scrape agents over real campaign briefs + 7 DB anchors +
curator). GROUNDING + miner in `complex_benchmark/`.
1. **Luxury Shopify hamper line** (db-4478) — 18 conn, 17 img. masking+badge select_by_prompt+lens_blur
   +full tonal+presets+select_subject→invert→fill_area(grey)→remove_bg→crop. Image-only.
2. **Real-estate listing stills** (db-6004) — 18 conn, 33 in (img+data). 5-bracket HDR window-pull
   (exposure/highlights/light/dark/brightness/hsl)+straighten+crop_to_bounds+preset + Illustrator
   data-merge rider labels (font_recommend+merge_data_vector+render_vector).
3. **Reality-show key-art rebuild** (db-1847) — 17 conn, 8 in. Adobe **Stock** search+license →
   select_subject/by_prompt+invert+gaussian/lens_blur+tonal+generative_expand → 24x36 poster.
4. **Tech-house single release** (composite) — 19 conn, 14 in. CREATIVE-FX cover (monochromatic_tint
   +halftone+color_overlay+grain+vectorize) + selective-color (select_by_prompt+single_color_saturation
   +invert) + Illustrator merch data-merge.
5. **4-colour screen-print seps** (db-2919) — 16 conn, 6 in. halftone+single_color_saturation+
   color_overlay+select→fill white underbase+add_noise+glitch+vectorize+render_vector.
6. **Conference badge+certificate suite** (scraped, 510 rows) — 16 conn, 20 in. InDesign **data-merge
   LAYOUT**: headshot crop/retouch/select→fill backdrop/preset + merge_data_layout+render_layout+
   convert_pdf + font_recommend.
7. **Real-estate tour VIDEO + reels** (composite db-366/1885/641) — 13 conn, 12 in (video+audio+img).
   media_summarize+video_create_quick_cut+media_enhance_speech(clean TTS VO)+video_resize(9:16/1:1).

## Coverage: 44 headless tools mapped, **0 uncovered**. Honestly excluded (human/unavailable):
change_background_color (Express-only → substituted select→invert→fill_area), search_design/fill_text/
animate_design (Express needs human click), generative fill/text-to-image/bg-replace-by-prompt/
upscale/video-trim/PDF-text-edit (unavailable per init doc).

## SMOKE TEST DONE 2026-06-14 (full results: complex_benchmark/SMOKE_RESULTS.md):
- ✅ WORKS: masking (select_subject/by_prompt/invert), fill_area (studio-grey recipe visually verified),
  lens_blur, halftone, monochromatic_tint, adjust_exposure, crop_to_bounds, list_presets (80+ Lightroom
  presets), font_recommend, Adobe Stock (search+license+download). + earlier-proven image tools. The
  whole Photoshop/Lightroom/Stock family (~28 connectors) is GO and subagent-safe.
- ❌ BLOCKED (account not entitled): document_merge_data_vector/render_vector (Illustrator sub required),
  document_merge_data_layout (InDesign CC required) → ALL data-merge + native vector/layout/convert OUT.
  image_vectorize still works (Sensei, →SVG). So data-merge tasks must use LOCAL PIL merge (honest label).
- ⏳ UNCONFIRMED: video/audio (video_resize/media_summarize return async status:"working" + a pollTool
  the model can't load; widget never delivered headlessly). Input gen (Veo/Sora/TTS) proven; the
  CONNECTOR video tools need the interactive widget or an entitled setup — confirm before building T7.
- Net: T1/T3 fully runnable; T2/T4/T5 runnable with their Illustrator/InDesign bits done LOCALLY; T6
  (pure InDesign data-merge) needs rework or a different account; T7 (video) pending widget confirmation.

## DEFINITIVE 10-task benchmark (2026-06-15, after CC Pro): complex_benchmark/definitive_10_tasks.json
CC Pro (dhirengshetty@gmail.com) unlocked Illustrator+InDesign — re-smoke-tested ALL connectors
(complex_benchmark/SMOKE_RESULTS_v2.md + FEASIBILITY.md). 38 [C] connector-confirmed tools. Built 10
long-horizon tasks (definitive-mega-benchmark workflow: refine 7 + 3 new + curate). Each 18-31 distinct
connectors, 25-38 steps, iterative output→input chaining, wide inputs (image/data/video/audio/template).
**Collectively cover ALL 38 confirmed connectors, 0 uncovered.** The 10:
1 Luxury hamper retouch (22C, 0 templates) — masking+tonal+FX+preset, FULLY runnable now.
2 Real-estate HDR stills (19C) — +rider_label.ai data-merge [T].
3 Reality-show key-art rebuild (31C!, 0 templates) — Stock+masking+blur+grade+expand, FULLY runnable.
4 Tech-house single release (22C) — FX cover + selective-color + merch_card.ai merge [T].
5 4-colour screen-print seps (21C) — FX+vectorize + sep_sheet.ai render [T].
6 Conference badge+cert suite (18C) — headshot retouch + badge.indd+certificate.indd data-merge [T][T].
7 Real-estate tour VIDEO (22C, 5 [L] ffmpeg) — clips/VO generated; video edit local; graded thumbnail [C].
8 LUMA full brand-launch kit (27C, 5 [T]!) — ALL-APPS: logo vectorize+products+Stock+duotone+business
  cards/letterhead/brand-guide via InDesign data-merge. The flagship.
9 Editorial magazine 6pp spread (27C) — duotone portraits+color-splash+Stock+contributor merge+FeatureSpread_6pp.indd.
10 VOIDRUNNER comic variant-cover pack (21C) — ink→vectorize→halftone/duotone/grain/glitch+voidrunner_variant_covers.ai merge.
**Template-authoring required** (7 tasks): user authors the .indd/.ai with real Data-Merge/Variables
fields in desktop apps (now available) — these are legitimate client-supplied inputs. T1/T3 need NONE
(fully connector-runnable now); T7 video uses local ffmpeg. Next: user picks → generate inputs (incl.
video/audio) → author templates for [T] tasks → execute with trajectories → rubrics HTML (same pipeline).

## (historical) risks we smoke-tested:
data-merge (document_merge_data_layout/vector need a real .indd/.ai template + CSV — unproven headless),
video tools (async with a progress widget — behavior in workflow/headless unknown), Adobe Stock
license, the masking chain (select_subject/by_prompt→invert→fill_area). Did an upload+op smoke-test of
each new tool family first (like the image_remove_background smoke-test before round 3). THEN author
specs → generate inputs (incl. video/audio) → judge → execute with trajectories → rubrics HTML.

## ROUND-5 INPUT-ASSET GENERATION (2026-06-15) — DONE, all 10 ready
Pipeline extended for video/audio: asset_pipeline/adapters/media_gen.py (Veo 3 fast + Sora-2 + OpenAI
TTS + roughen_audio via imageio-ffmpeg); new "video"/"audio" asset kinds in generate.py; config roles
video/video_sora/audio_vo. Specs in asset_pipeline/mega_specs/ (spec_<id>.py, self-contained RECORD+
SPEC+BRIEF_MD, auto-merged into specs.py via MEGA_RECORDS/MEGA_SPECS). IDs: 4478 hamper, 6004 re-stills,
1847 reality, 9001 techhouse, 2919 screenprint, 9002 conference(510-row roster), 9003 video, 9004 LUMA,
9005 magazine, 9006 comic. All input_assets/<id>_<slug>/ ready=True. ~$33 gen.
Judge scoreboard (calibrated): 9004 10.0, 2919 8.8, 9001 8.7, 9005 8.3, 4478 8.0, 9002 7.8, 9006 7.6,
1847 7.4, 9003 7.1, 6004 (framing re-aligned, re-judging — was 6.7).
**10 faults caught+fixed from our end** (the value of the QC/judge loop): (1) custom {placeholder} bug
class that passed agent self-tests but crashes at gen — render-tested all 10; (2) pipeline image→image
depends_on; (3) bg-process cwd reset (always `cd asset_pipeline &&`); (4) 6004 over-gen 30 un-mergeable
brackets→6 merged-base (connector has NO HDR-merge tool); (5) judge mis-calibrated for [T] tasks (added
CLIENT-SUPPLIED-INPUTS rule: templates/stock are user-authored decisions, not missing); (6) flat-swatch
near-uniform QC false-positive → PIL program asset; (7) QR program_fn passed paths-list to one save();
(8) 6004 stale-state incomplete regen (delete state.json+assets); (9) judge skipped .render so couldn't
see the data-merge .csv → keep .csv renders; (10) 6004 brief still said "5-bracket/30" after 30→6 fix →
aligned RECORD inputs+input_requirement+BRIEF_MD to "6 merged-base, one per scene".
Known LIMITATION (not fixable): image models cap ~1536px; judge flags print-res for comic/print
deliverables — mitigated for vectorized artwork (image_vectorize → scale-independent). Templates: 12
.indd/.ai the USER authors (complex_benchmark/TEMPLATE_AUTHORING_GUIDE.md); CSV columns already match.
NEXT: connector execution (mega_executions/ like flagship_executions/) → trajectories → rubrics HTML.

## ROUND-5 EXECUTION + REVIEW SITE COMPLETE (2026-06-15)
All 10 tasks executed end-to-end → mega_executions/<id>_<slug>/ (input_assets/work/steps/outputs +
trajectory.json + outputs/README.md). ~280 real Adobe connector ops (every one a logged requestId),
~370 trajectory steps, ~340 before/after step images, ~230 deliverable files. Honest actor labels:
adobe_connector / local_compositor / local_datamerge / local_video / local_verify. Data-merge done
LOCALLY (compose_lib.data_merge — 510 badges+510 certs for 9002, 12 merch cards for 9001, etc.) because
the Adobe data-merge connector needs a desktop-authored template (confirmed unusable headless even with
CC Pro: convert_pdf→indd gives literal <<field>> text that won't bind; tested twice). Video edited
locally with ffmpeg (connector video tools async-unretrievable headless); inputs gen'd via Veo/Sora/TTS.
Adversarial verify caught+fixed: 4478 (only 1/13 cutouts → re-ran all 13), 9005 (PULL-QUOTE placeholder
in page-2 header → FEATURE), + a compose_lib.paste(anchor='center') bug ('e' in 'center' misfire).
Build/serve: mega_executions/build_presentation.py → presentation_data.js (recurses output subdirs;
video poster-frames + pdf thumbs via ffmpeg); Mega_Review.html (adapted from Flagship_Review: window.
MEGA_DATA, video/audio/pdf thumbnails, local-actor trajectory tags, data-merge chips). serve_review.js
on :8802; preview config "mega" in BOTH .claude/launch.json (root + project). 410 scorable rubric items
(10 agents viewed real pixels; structure {input_assets,outputs,task_level}[].items{id,type,question,
guidance,reference}). Browser-QA'd: 0 broken thumbs, scoring/autosave(localStorage mega_scores_v1)/
export/lightbox all work. THE WHOLE BENCHMARK (find→generate→judge→execute→rubrics→HTML) IS DONE.
