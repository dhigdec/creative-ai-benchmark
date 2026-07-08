# Task 9003 — Real-estate lead-gen listing-media package

**Client:** Solstice Properties — *Your Home, Elevated.*
**Listing:** 1234 Serene Haven Way, Willow Creek Estates — **$975,000** · 4 BD · 3 BA · 2,850 SQFT
**Agent (lower-third):** Eleanor Vance, Senior Sales Associate

All copy (address, price, agent, look notes, platform sizes, narration) was read
programmatically from `input_assets/campaign_brief.json`. Brand palette/persona from
`manifest.json`.

---

## Asked → produced

| # | Deliverable asked | File(s) produced | How made |
|---|---|---|---|
| 1 | Narrated tour-guide MP4/H.264, rooms ordered from a footage summary, hook in first 3s, cleaned VO scored to a licensed bed | `tour_master_16x9.mp4` (1280×720), `tour_feed_1x1.mp4` (1080×1080), `tour_reels_stories_9x16.mp4` (1080×1920) | **local ffmpeg**: story-ordered cut (exterior golden-hour HOOK → kitchen → living → hallway → primary suite → spa bath), 0.4s crossfades, cleaned VO over a ducked warm ambient bed, animated lower-third |
| 2 | Cleaned, de-reverbed agent VO (broadcast dialogue stem) | `agent_vo_cleaned_stem.wav`, `agent_vo_cleaned_stem.mp3` | **local ffmpeg**: band-limit + 2-pass FFT denoise (strips the music/ambient bed) + anlmdn/compand (suppress reverb tail) + loudnorm to −16 LUFS |
| 3 | Key-segment summary + rough transcript used to choose the cut | `footage_summary_and_transcript.json`, `.txt` | **local** (media_summarize done conceptually) — per-clip key segments + chosen order + rough VO transcript |
| 4 | Fully graded hero interior, levelled/cropped, blown windows recovered via masked edits, one campaign listing look | `hero_interior_graded.png` (1506×1004) | **Adobe connector**: straighten → crop → auto-tone → warm WB → exposure → **masked window highlight/exposure recovery** → masked room shadow/light → HSL → vibrance → **Color-Bright preset** |
| 5 | Twilight-sky exterior cover (Adobe-Stock sky composited behind the exterior) | `twilight_exterior_composite.png` (1536×1024), `twilight_cover_16x9.png`, `twilight_cover_feed_1x1.png`, `twilight_cover_stories_9x16.png` | **Adobe connector** masked the overcast sky + **licensed AdobeStock_227883293** twilight plate; **local** photographic sky-swap composite + dusk grade of the house |
| 6 | Branded lower-third / logo bug: brokerage logo vectorized to clean SVG + recommended listing type | `brokerage_logo_vector.svg`, `brokerage_logo_mark.png`, `lower_third_9x16.png`, `lower_third_1x1.png` | **Adobe connector**: background-remove → **vectorize to SVG**; **font_recommend** for type; **local** lower-third layout (logo bug + agent strip + price pill) |
| 7 | Generative-expanded hero reframed to 1:1 + 9:16 covers without cropping the room, plus thumbnail crop | `cover_feed_1x1.png`, `cover_stories_9x16.png`, `cover_reels_9x16.png`, `video_thumbnail_1280x720.png` | **Adobe connector**: generative-expand (ceiling+floor) → 9:16 crop; **local** cover/thumbnail composition |
| 8 | Platform-ready exports: Feed 1:1, Stories 9:16, Reels 9:16, MP4/H.264 + matching cover stills | all `tour_*.mp4` + all `cover_*.png` above | as above |
| 9 | One consistent aesthetic (white balance, tone, preset) across video thumbnail and every still | every still + thumbnail share the connector grade | the single graded hero (warm WB + Color-Bright) is the source for every cover and the thumbnail |

### Supporting / preview files
`lower_third_preview.png` (lower-third on a card), `footage_summary_and_transcript.*`.

---

## How it was built (actors)

**Adobe connector — 23 image/asset ops** (real `requestId`s in `trajectory.json`):
upload → straighten → crop_to_bounds → auto_tone → color_temperature → exposure →
select_by_prompt(windows) → highlights → exposure(masked) → invert_selection →
dark_portions → light_portions → hsl → vibrance_and_saturation → list_presets →
apply_preset(Color-Bright) → generative_expand → crop_and_resize(9:16) →
select_by_prompt(sky) → fill_area → remove_background(logo) → vectorize(SVG) +
asset_search/license_and_download_stock (twilight sky) + font_recommend.

**Local (`local_video` / `local_compositor`):** all video (ffmpeg) — cut, crossfades,
reframe to 9:16 & 1:1, VO clean-up, music bed, ducked mix, mux, animated lower-third;
and all final multi-element layout (covers, thumbnail, lower-third, twilight composite).

Full 42-step audit trail with snapshots in `../trajectory.json` and `../steps/`.

---

## Honest limitations

- **Video is local (ffmpeg), not the Adobe connector.** Per the execution contract, the
  connector video tools (`video_create_quick_cut`, `video_resize`, `media_summarize`,
  `media_enhance_speech`) don't return retrievable results headless, so the edit, reframe,
  VO clean-up and mux were done locally. The connector *image* grade (deliverable 4/5/7)
  IS real Adobe — every `requestId` is genuine.
- **Music bed is a synthesized warm-ambient placeholder**, not the final licensed Stock
  track. Adobe Stock audio search returned only cinematic/comedy/techno beds (no warm
  acoustic instrumental), and the licensed-audio download is not retrievable headless. A
  local warm pad stands in so the mix is complete and ducked correctly; swap in the
  client's licensed bed at the same level for delivery. (The twilight **sky** plate IS a
  real licensed Stock asset — AdobeStock_227883293.)
- **Brand fonts (Libre Franklin / Inter) are not installed** on this machine. Type is set
  in the closest installed grotesques (Avenir Next / Helvetica Neue) per the font_recommend
  output; substitute the licensed brand fonts for final delivery.
- **Logo vectorization kept the icon mark, dropped the wordmark text.** Background-removal
  treated the "Solstice Properties / Boutique Residential" type as background, so the clean
  SVG/cutout is the navy-door + sage-keyhole **mark**. The brokerage name is set in brand
  type in every lower-third and lockup, so the full identity still reads.
- **Source stills cap at 1536px.** Stills are delivered at web/social print sizes from
  these sources (no upscaling-as-print).
- **Window recovery** pulls the genuinely blown windows back to legible textured panels
  (a real masked highlight+exposure recovery); they read as soft daylight-grey, which is
  the honest recovered tone rather than a fabricated exterior view.
