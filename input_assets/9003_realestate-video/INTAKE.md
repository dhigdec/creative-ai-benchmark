# INTAKE — Real-estate lead-gen listing-media package — narrated property tour cut from room clips + cleaned agent VO scored to a licensed bed, plus a graded hero still, twilight composite cover, branded lower-third, and Feed/Stories/Reels exports

**Task 9003** · Video, Audio & Social Media · Video & Social Media Production · feasibility: **partial** · source: [composite posting](https://www.freelancer.com/projects/voice-over/Lead-Generating-Real-Estate-Video)

## The simulated client
**Solstice Properties** — Modern residential real estate brokerage. *Your Home, Elevated.*
Palette: Soft White `#F7F6F2` (primary), Warm Oak `#C8A675` (secondary), Deep Ink Navy `#1F2A3C` (primary), Fresh Sage `#7E9C7A` (accent)  
Fonts: headings **Libre Franklin**, body **Inter**  
Voice: We approach every client relationship with genuine warmth and expertise, guiding you confidently through your real estate journey. Our focus is always on your unique benefits and discovering the perfect home that elevates your lifestyle.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/campaign_brief.json` | Campaign brief / spec sheet: target platforms + sizes (Feed 1:1, Stories 9:16, Reels 9:16) | gemini/gemini-2.5-flash |
| 2 | `assets/campaign_brief.md` | Campaign brief / spec sheet: target platforms + sizes (Feed 1:1, Stories 9:16, Reels 9:16) | gemini/gemini-2.5-flash |
| 3 | `assets/walkthrough_01_exterior-approach.mp4` | Six room-by-room property walkthrough clips (kitchen, living room, primary suite, primary  | openai/sora-2 |
| 4 | `assets/walkthrough_02_kitchen.mp4` | Six room-by-room property walkthrough clips (kitchen, living room, primary suite, primary  | gemini/veo-3.0-fast-generate-001 |
| 5 | `assets/walkthrough_03_living-room.mp4` | Six room-by-room property walkthrough clips (kitchen, living room, primary suite, primary  | gemini/veo-3.0-fast-generate-001 |
| 6 | `assets/walkthrough_04_primary-suite.mp4` | Six room-by-room property walkthrough clips (kitchen, living room, primary suite, primary  | gemini/veo-3.0-fast-generate-001 |
| 7 | `assets/walkthrough_05_hallway.mp4` | Six room-by-room property walkthrough clips (kitchen, living room, primary suite, primary  | gemini/veo-3.0-fast-generate-001 |
| 8 | `assets/walkthrough_06_primary-bath_vertical.mp4` | Six room-by-room property walkthrough clips (kitchen, living room, primary suite, primary  | gemini/veo-3.0-fast-generate-001 |
| 9 | `assets/agent_vo_rough.mp3` | Agent voiceover narration recorded over a rough music bed and roomy reverb (deliberately n | openai/gpt-4o-mini-tts+roughen |
| 10 | `assets/hero-interior-living-room.jpg` | Listing stills (photoreal): hero interior living room with genuinely blown-out windows to  | openai/gpt-image-2 |
| 11 | `assets/exterior-front-overcast.jpg` | Listing stills (photoreal): hero interior living room with genuinely blown-out windows to  | openai/gpt-image-2 |
| 12 | `assets/twilight-reference-frame.jpg` | Listing stills (photoreal): hero interior living room with genuinely blown-out windows to  | openai/gpt-image-2 |
| 13 | `assets/brokerage-badge-detail.jpg` | Listing stills (photoreal): hero interior living room with genuinely blown-out windows to  | openai/gpt-image-2 |
| 14 | `assets/brokerage_logo.png` | Brokerage logo/agent badge artwork to background-remove and vectorize for the lower-third  | gemini/gemini-3-pro-image |

## Decisions & assumptions (items the brief left open)
- **Licensed royalty-free music bed for the tour mix (Adobe Stock, contentType audio)** → Sourced LIVE from Adobe Stock at execution via asset_search (entityScope StockAsset, contentType audio) + asset_license_and_download_stock — an upbeat-but-warm royalty-free instrumental bed (~60-90s, light acoustic/ambient) ducked under the cleaned VO; not pre-generated.  
  *why:* Music is a licensed Stock input, sourced at runtime — we don't synthesize it.
- **Licensed twilight/dusk sky plate to composite behind the listing exterior (Adobe Stock, landscape orientation)** → Sourced LIVE from Adobe Stock at execution via asset_search (entityScope StockAsset, image, landscape orientation) + asset_license_and_download_stock — a high-res twilight/dusk sky plate (warm horizon to indigo) composited behind the masked exterior; the generated twilight reference frame only sets the colour target.  
  *why:* The hero sky is a licensed Stock plate sourced at runtime, not generated.
- **Platform-ready exports: narrated tour MP4/H.264 + matching cover stills in Facebook Feed 1:1, Stories 9:16 and Reels 9:16, plus a 1280x720 video thumbnail; one consistent grade shared across thumbnail and every still** → Output spec recorded for the Adobe agent: tour MP4 H.264 + matching cover stills in Feed 1080x1080 (1:1), Stories 1080x1920 (9:16) and Reels 1080x1920 (9:16), plus a 1280x720 video thumbnail; the graded hero preset + white balance are reused across the thumbnail and every cover for one consistent look. Tour mux/reframe is local ffmpeg; covers + lower-third are local PIL.  
  *why:* These are deliverable sizes/formats, not an input asset — recorded for the downstream agent rather than generated.

## Next step — the Adobe workflow the agent runs
```
asset_initialize_file_upload -> asset_finalize_file_upload -> media_summarize [L] -> media_enhance_speech [L] -> asset_search (music bed + twilight sky) -> asset_license_and_download_stock -> video_create_quick_cut [L] -> video_resize [L] (mux VO+music, Feed/Stories/Reels) -> image_auto_straighten -> image_crop_to_bounds -> image_apply_auto_tone -> image_adjust_color_temperature -> image_adjust_exposure -> image_select_by_prompt (windows) -> image_adjust_highlights -> image_invert_selection -> image_adjust_dark_portions -> image_adjust_light_portions -> image_adjust_hsl -> image_adjust_vibrance_and_saturation -> image_list_presets -> image_apply_preset -> image_generative_expand -> image_crop_and_resize -> image_select_by_prompt (sky) -> image_fill_area -> image_remove_background -> image_vectorize -> font_recommend -> asset_inline_preview -> PIL_compose_local
```

Coverage: 8 client inputs — 5 supplied as assets, 3 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> A boutique residential brokerage hands over six raw room walkthrough clips and one rough, reverberant agent voiceover and needs a lead-gen Facebook/Reels property tour plus a matched still package: a story-ordered cut with a 3-second hook, a cleaned VO scored to a licensed music bed, a fully graded hero interior (blown windows recovered, levelled, one shared listing look), a twilight composite exterior cover, a vectorized brokerage logo bug with recommended lower-third type, and platform-ready Feed 1:1 / Stories 9:16 / Reels 9:16 exports sharing one grade.