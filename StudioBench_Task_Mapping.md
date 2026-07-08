# StudioBench — 66-Task Evaluation Mapping
**Every task's input assets, expected outputs, and exact verifier checks — each scored against the shared framework rubrics in Part A.**
*Version 2026-06-26. Brand names are the fictional, licensing-clean versions. Read Part A once; each task in Part B then lists only what is unique to it.*
## Part A — The framework (the shared rubrics, defined once)
Every task is scored the same way. Below are the rubrics that apply to all 66; in Part B each task shows only its own inputs, outputs, and verifier checks.
**A1 · Taxonomy.** Four axes — **Brand** (8 fictional companies, each a locked brand kit) · **Operation** (8 types in 4 families) · **Capability** (K1–K7, scored on every task) · **Horizon** (task length: H1 ≤3 steps → H4 16+).
| Operation family | operations |
|---|---|
| Photo & Image | O1 tonal grade & restore · O2 masked recolor & isolation · O4 preset retouch · O6 stylized & duotone · O8 stock-sourced hero |
| Vector & Print | O7 vector & screen-print |
| Layout & Data | O5 data-merge & layout |
| Motion & Audio | O3 video & audio |

**A2 · Phase 1 — Input-asset admission gate (Pass / Fix / Reject).** Before a task enters the benchmark an expert validates the input package on 8 dimensions; (code) items are automatic. A task enters only when every dimension is Pass.
| dimension | what it certifies |
|---|---|
| 1 Completeness | every referenced asset provided, opens, right format/res; brief states goal, deliverable, dims, brand, content |
| 2 Feasibility integrity | deliverable producible with supplied assets+tools; fonts/colours available; no accidental contradiction |
| 3 Realism / difficulty | inputs look like a real client handoff (dull/tilted where intended); difficulty matches the horizon tier |
| 4 Brand coherence | logo, palette, fonts, imagery belong to one brand; brief's colours/fonts match the kit |
| 5 No-answer leakage | no finished deliverable / near-duplicate in the inputs (code similarity) |
| 6 Provenance / licensing | every asset logged (generator+prompt / origin); SHA-256; commercially-safe flag; third-party rights cleared (code) |
| 7 Decision quality | invented brand/persona details sensible, documented, non-contradictory |
| 8 Hallucination / contradiction | brief references only existing assets; counts/dims/prices internally consistent |

**A3 · Phase 2 — Golden trajectory.** A creative expert completes each task on the same Adobe-connector tools, captured as a step-log (each action + a one-line reason) plus a silent screen recording — producing the golden output and the golden trajectory the agent's 3 runs are measured against.
**A4 · Phase 3 — Output scoring (5 layers).** The seven capabilities (Layer 1) are the headline; the layers below are the evidence.
| layer | what it asks | who |
|---|---|---|
| 1 Capabilities (K1–K7) | how good overall? | roll-up |
| 2 Operation craft | craft good for this job? | expert |
| 3 Verifier checks | delivered what the brief asked? | expert + code |
| 4 Process & honesty | worked sensibly & honestly? | expert + code |
| 5 Professional review | would a pro ship it? | expert |

Roll-up: **Pass = 1 · Minor = 0.5 · Major = 0**; a **dealbreaker** (regenerated logo, wrong format, missing legal text) caps the capability regardless of craft. Each task runs as a batch of 3; scores carry a confidence interval, and a model gap counts only when intervals separate.
**A5 · Layer 2 — Operation-craft checklists.** The expert marks each item Pass / Minor / Major against reference images. One checklist per family; a task uses its family's list.
*Photo & Image*
| craft item | Pass | Minor | Major |
|---|---|---|---|
| Exposure & tone | balanced; detail held | slightly off, recoverable | clipped — detail lost |
| Colour & white balance | neutral / on-brand | slight cast | clear cast / wrong colour |
| Mask & edge quality | clean edges; detail kept | small halo / jaggies | visible halo / clipped |
| Blemish & artefact removal | clean & natural | a few left / over-smooth | artefacts remain / plastic |
| Texture & detail | realistic | slightly soft | smeared / lost |
| Subject fidelity | identity unchanged | minor warp | distorted / altered |
| Look / grade integrity | cohesive, intentional | slightly uneven | artificial / broken |
| Composite realism (stock-hero) | light/scale match | minor mismatch | pasted-on |

*Vector & Print*
| craft item | Pass | Minor | Major |
|---|---|---|---|
| Path & curve quality | smooth Béziers | a few rough curves | kinked / broken |
| Anchor-point efficiency | minimal points | some redundancy | over-pointed |
| Shape precision & symmetry | accurate, balanced | slightly off | distorted |
| Stroke & fill consistency | uniform | minor variance | inconsistent |
| Screen-print readiness | clean, reg-safe seps | minor issues | unprintable as-is |
| Type & line safety | outlined; safe weights | one borderline | hairlines / live type |
| Scalability & export | valid; scales clean | minor issue | rasterized / invalid |

*Layout & Data*
| craft item | Pass | Minor | Major |
|---|---|---|---|
| Grid & alignment | consistent grid | a few off-grid | ragged |
| Visual hierarchy | key element leads | weak | flat / confusing |
| Typographic hierarchy | heading dominant | weak (size only) | indistinguishable |
| Spacing & rhythm | even, consistent | a few slips | crowded / erratic |
| Reading flow & grouping | logical, grouped | minor slips | scattered |
| Data integrity (merge) | every record placed | a couple slips | missing / overflowing |
| Image placement & crop | aligned, correct aspect | loose crop | stretched / mis-cropped |
| Balance & whitespace | balanced | slightly heavy/sparse | cramped / empty |

*Motion & Audio*
| craft item | Pass | Minor | Major |
|---|---|---|---|
| Cut & transition | smooth, motivated | a couple abrupt | jarring |
| Motion & continuity | continuous | minor | visible jumps |
| Timing & pacing | well-paced | slightly off | rushed / dragging |
| Audio sync | in sync | slight drift | out of sync |
| Audio clarity & levels | clean, consistent | minor noise | noisy / clipping |
| Text & lower-thirds | legible, timed | slightly tight | unreadable / mistimed |
| Export integrity | correct format/res | minor miss | wrong / broken |

**A6a · Layer 4 — Process & honesty** (from the step-log; code counts + expert mark).
| check | Pass | Minor | Major | feeds |
|---|---|---|---|---|
| Planning | sensible order, deps first | wasted / out-of-order steps | chaotic, no plan | K6 |
| Tool use | right tool & settings | wrong choice, self-corrected | repeatedly wrong | K6 |
| State management | uses latest files | one stale file | old assets throughout | K6 |
| Recovery | detects & fixes | recovers clumsily | repeats the failure | K6 |
| Verification | checks before submit | partial check | never verifies | K6 |
| Honesty (impossible asks) | flags / refuses / discloses | hedges but proceeds | fabricates / hides | K7 |
| Self-calibration | prediction matches reality | slightly off | confidently wrong | K7 |

**A6b · Layer 5 — Professional review** (each a fixed choice + a one-line reason).
| instrument | what the expert does | produces |
|---|---|---|
| The call | accept / send-back / scrap (+ one-line reason) | commission pass rate |
| Punch-list | notes tagged blocker / fix / nitpick | cost-to-ship number |
| Pin-the-flaw | click the spot, pick the defect, tag severity | localized defect labels |
| Blind face-off | two outputs side by side: which would you send the client? | craft ELO |
| Confidence | High / Medium / Low — one tap | filter / down-weight labels |

**A6c · Layer 1 — Capabilities (K1–K7).** Rolled up from the layers above (nobody grades them directly).
| capability | what it measures | scored by |
|---|---|---|
| K1 Instruction adherence | every explicit requirement — text, sizes, deliverables, formats | code (audited) |
| K2 Asset utilization & fidelity | used the real logo/colours/fonts; never regenerated locked assets | code (audited) |
| K3 Compositional craft | alignment, hierarchy, spacing, finish — pro standard | expert (craft checklist) |
| K4 Creative quality | original & effective, not generic | expert (face-off + range) |
| K5 Communication effectiveness | a fresh viewer recovers the message | expert (round-trip viewer) |
| K6 Agentic competence | planned, used tools well, recovered, verified | code counts + expert |
| K7 Honesty & calibration | flagged impossible asks vs faked; predicted own success | code flags + expert |

**A7 · Task-level metrics & annotator flow.** Per task we report: **commission pass rate** (passes all mandatory verifiers + admission, no dealbreaker), **craft ELO** (blind face-offs), **human-parity** (best-of-3 agent run vs the golden human output), and the **K1–K7 profile** with a confidence interval over the 3 runs. *Annotator flow:* the reviewer opens the output beside the brief, inputs, and golden trajectory → runs the Layer-3 checklist (auto pre-filled, expert confirms the eye-checks) → marks the Layer-2 craft checklist → marks Layer-4 process from the step-log → gives the Layer-5 call + punch-list + pin-the-flaw + confidence; a fresh round-trip viewer recovers the message (K5); an art-director runs the blind face-off and the best-of-3-vs-human pairing. Gold items + Krippendorff's α run in the background to measure agreement.

[[PAGEBREAK]]
## Part B — The 66 tasks
Each task lists its header, one-line ask, input assets, expected outputs, and its **Layer-3 verifier checks** (expert-authored). All other scoring follows Part A — the family-craft checklist (A5), process & review (A6), capability roll-up (A6c), and metrics + annotator flow (A7).

[[PAGEBREAK]]
### AO-00 · White-Background Ecommerce Hero Pack for an Automotive Aftermarket-Parts Marketplace (turbocharger listing: clean studio hero, transparent cutout, vector icon, and outpainted lifestyle banner)
**Brand:** Automotive, Industrial & Agriculture &nbsp;·&nbsp; **Operation:** O2 Masked recolor & isolation (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (17 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Turn a dealer's raw, off-color bench photo of an aftermarket turbocharger into a clean color-accurate #FFFFFF ecommerce hero plus a transparent cutout, a scalable vector icon, and an outpainted 16:9 lifestyle banner, then collect them on a review board.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| raw_turbo_bench.jpg | image | Photoreal candid smartphone photo of a chrome-and-aluminium aftermarket automotive turbocharger sitting on a c |
| brand_palette.json | data | Generate a small JSON brand-palette file for a B2B automotive aftermarket-parts ecommerce platform. Include ke |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| turbo_hero_2048_white.png | image | 2048x2048 square, true #FFFFFF background, straightened + tonally corrected aftermarket turbo, color-accurate (not oversaturated). Primary listing-tile hero. |
| turbo_cutout_transparent.png | image | Background-free transparent PNG of the SAME corrected turbo (alpha channel), for PDP hover-zoom / overlays. |
| turbo_icon.svg | vector | Clean scalable SVG line-art / silhouette of the turbo derived from the transparent cutout, for spec-sheet header and UI category chips. |
| turbo_lifestyle_banner_16x9.png | image | 16:9 category-landing banner: licensed service-bay/garage stock backdrop with the corrected hero AI-outpainted into a wider natural frame. |
| hero_pack_review_board | board | Firefly review board deep-link assembling hero, transparent cutout, vector icon, and lifestyle banner for one-link merchandising sign-off. |

**Layer-3 verifier checks** — expert-authored (16 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| Primary hero deliverable turbo_hero_2048_white.png is exactly 2048x2048 pixels | auto · mandatory · K1 | Image dimensions read from turbo_hero_2048_white.png equal exactly 2048 px wide by 2048 px high (square listing-tile spec) |
| The hero background is genuine pure white #FFFFFF solid fill, not a gray studio sweep | auto · **dealbreaker** · K1 | Sampled background pixels in the non-subject region of turbo_hero_2048_white.png read RGB (255,255,255) / hex #FFFFFF as a flat solid fill, matching brand_palette listing_background_hex '#FFFFFF'; no gray gradient/sweep |
| The turbocharger in the hero is straightened (bench tilt corrected) without warping its true geometry | expert · mandatory · K3 | The ~4-degree tilt of the raw bench photo is corrected so the part sits level, and the turbo's proportions/geometry remain undistorted (straighten only, no warp), per the 'Keep the part's true geometry — straighten, don't warp' constraint |
| The hero is tonally corrected: warm fluorescent cast neutralized, underexposure lifted, blown chrome highlights recovered | expert · mandatory · K4 | Chrome/aluminium reads neutral (no orange/yellow cast), overall brightness lifted to ecommerce-listing levels, and clipped specular highlights on the compressor housing show recovered detail |
| The part is color-accurate and NOT oversaturated, consistent with the B2B operational tone | expert · mandatory · K4 | Saturation is restrained (gentle vibrance only); the turbo reads credible/true-to-color, honoring the brand_palette notes 'do not oversaturate parts; B2B operational tone' |
| Transparent cutout deliverable turbo_cutout_transparent.png is a PNG with a real alpha channel and fully transparent background | auto · mandatory · K1 | turbo_cutout_transparent.png is PNG format, carries an alpha channel, and the non-subject region is fully transparent (background removed) |
| The cutout shows the SAME corrected turbo (inherits the color-corrected master pixels) | expert · mandatory · K2 | The turbo in turbo_cutout_transparent.png matches the corrected master tone/white-balance (correction done before masking), not the raw warm/underexposed pixels |
| The cutout mask edges cleanly follow the turbo silhouette | expert · quality · K3 | Mask edges hug the turbo outline with no leftover bench/clutter halo and no chunks of the part cut away |
| Vector icon deliverable turbo_icon.svg is valid scalable SVG vector line-art/silhouette | auto · mandatory · K1 | turbo_icon.svg parses as valid SVG containing vector path geometry (not an embedded raster image), so it scales crisply for the spec-sheet header and UI category chips |
| The vector icon is recognisably derived from the turbo cutout silhouette | expert · quality · K3 | The SVG line-art/silhouette reads clearly as the same turbocharger from turbo_cutout_transparent.png, clean enough to function as a UI icon |
| Lifestyle banner deliverable turbo_lifestyle_banner_16x9.png is a 16:9 aspect-ratio PNG | auto · mandatory · K1 | turbo_lifestyle_banner_16x9.png is PNG with width:height equal to 16:9 (ratio 1.777...), per the category-landing banner spec |
| The lifestyle banner places the corrected hero in a wider natural frame via AI outpainting | expert · mandatory · K4 | The corrected turbo sits naturally inside an AI-outpainted wider 16:9 frame with the part's pixels preserved and the extended canvas blending plausibly (generative_expand outpaint, per the banner deliverable) |
| All five expected deliverables are present in the hero pack | auto · mandatory · K1 | turbo_hero_2048_white.png, turbo_cutout_transparent.png, turbo_icon.svg, turbo_lifestyle_banner_16x9.png, and hero_pack_review_board are all produced |
| A single shareable Firefly review board collects the four image/vector derivatives for one-link sign-off | auto · mandatory · K6 | hero_pack_review_board is a Firefly board deep-link that assembles the hero (turbo_hero_2048_white.png), transparent cutout (turbo_cutout_transparent.png), vector icon (turbo_icon.svg), and lifestyle banner (turbo_lifestyle_banner_16x9.png) on one board |
| Color correction was applied BEFORE masking so every derivative inherits the corrected pixels | expert · mandatory · K6 | The hero, cutout, icon, and banner all share the same corrected (white-balanced, exposed, highlight-recovered, saturation-restrained) appearance, confirming correction preceded the select/remove-background steps per the 'Color correction must come BEFORE masking' constraint |
| Native delivery formats are honored: transparent PNG for the cutout and SVG for the icon | auto · **dealbreaker** · K1 | The cutout is delivered as a transparent PNG and the icon as an SVG (not flattened/rasterized substitutes), per the 'Deliver native formats where applicable (transparent PNG for the cutout, SVG for the icon)' constraint |


[[PAGEBREAK]]
### AO-01 · Premium Clinical Skincare Brand — Product-Shot Finishing, Logo Vectorization, Per-SKU Label Merge & Print-Ready Packaging Export
**Brand:** Beauty, Cosmetics & Personal Care &nbsp;·&nbsp; **Operation:** O2 Masked recolor & isolation (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (18 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Take our raw skincare hero shot, flat logo mark, texture plate and SKU copy sheet and produce a clinically clean white-background product image set, an editable vector logo, a recommended type system, packaging-safe outpainted canvases, a clinical monochrome variant, per-SKU print labels merged from our label template, and a print-ready packaging PDF — all assembled on one presentation board.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| dermavera_serum_hero_raw.png | image | Photoreal product photograph of a single frosted-glass cosmetic serum bottle with a matte white pump cap, stan |
| dermavera_logo_mark_flat.png | image | A minimal flat clinical skincare logo on a pure white background: a thin-line geometric molecule-meets-droplet |
| dermavera_stone_texture_plate.jpg | image | A flat top-down photograph of a matte pale grey-beige stone / terrazzo surface, very fine natural speckle, sof |
| dermavera_sku_label_copy.csv | data | Generate a 3-row CSV with header exactly: sku_name,claim,volume,inci_line,batch,accent_hex . Row1: 'Vitamin-C |
| label.ai | vector | Hand-authored Illustrator label template, one artboard 70x90mm + 3mm bleed, CMYK. Static art: placed DERMAVERA |
| carton.indd | vector | Hand-authored InDesign unit-carton dieline template, single document with the 5 box panels laid out flat (fron |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| dermavera_hero_whitebg_clinical.png | image | Finished clinical hero: auto-straightened, background swept to pure #FFFFFF, neutral-graded (auto-tone + neutralized color temp + lifted highlights), crisp product. Full- |
| dermavera_hero_1x1_ecom.png | image | 1:1 square e-commerce crop of the finished hero, product centered with clinical whitespace, 2048x2048px PNG on pure white. |
| dermavera_hero_packaging_wide.png | image | Outpainted packaging-safe wide canvas of the finished hero (generative_expand extends the white sweep left/right), ~5000x2800px PNG, white field for carton/hero-plate pla |
| dermavera_hero_mono_variant.png | image | Clinical monochrome brand variant of the finished hero — single deep slate-teal (#16403B) duotone/monochromatic tint, for collateral. Same resolution as hero, PNG. |
| dermavera_logo.svg | vector | Editable vector SVG of the supplied logo mark, clean single-color paths, transparent background — the editable source the brief demands. |
| dermavera_type_system.json | data | Recommended display + text typeface pairing (PostScript names + rationale) from font_recommend, to anchor the visual-identity typography spec. |
| dermavera_labels_merged.pdf | pdf | Print-ready per-SKU label set: 3 label artboards (one per SKU row) produced by merging the copy CSV into label.ai. CMYK, 3mm bleed, crop marks. Vector + editable source = |
| dermavera_carton_print.pdf | pdf | Print-ready unit-carton PDF exported from carton.indd with the finished white-bg hero plate placed in HERO_PLATE, CMYK, 3mm bleed, registration/crop marks. |
| dermavera_brand_board_deeplink | url | Firefly Board deep-link assembling the finished hero, 1:1 crop, wide canvas, mono variant, vector logo and label proofs into one sign-off presentation board. |

**Layer-3 verifier checks** — expert-authored (18 checks, 4 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All 9 named deliverables are present in the output set | auto · mandatory · K1 | Exactly these 9 deliverables exist: dermavera_hero_whitebg_clinical.png, dermavera_hero_1x1_ecom.png, dermavera_hero_packaging_wide.png, dermavera_hero_mono_variant.png, dermavera_logo.svg, dermavera_type_system.json, dermavera_labels_merged.pdf, dermavera_carton_print.pdf, and the dermavera_brand_board_deeplink URL |
| The clinical hero background is swept to pure white | auto · mandatory · K1 | In dermavera_hero_whitebg_clinical.png the sweep/background region sampled away from the product reads #FFFFFF (RGB 255,255,255) with no residual yellow-green cast |
| The clinical hero is delivered at full e-commerce resolution as sRGB PNG | auto · mandatory · K1 | dermavera_hero_whitebg_clinical.png is a PNG in sRGB at approximately 4000x5000px (within ~5% on each side) |
| The 1:1 e-commerce crop is exactly square at the specified pixel dimensions | auto · mandatory · K1 | dermavera_hero_1x1_ecom.png is a PNG measuring exactly 2048x2048px on pure white |
| The packaging-safe wide canvas matches the specified outpainted dimensions with the white sweep extended | auto · mandatory · K1 | dermavera_hero_packaging_wide.png is a PNG at approximately 5000x2800px (within ~5% on each side) with the white sweep extended left/right beyond the original hero frame |
| The monochrome variant is a single deep slate-teal duotone in the exact brand accent at hero resolution | expert · mandatory · K2 | dermavera_hero_mono_variant.png reads as a single-color monochromatic/duotone tint keyed to slate-teal #16403B (not full color, not greyscale), at the same resolution as dermavera_hero_whitebg_clinical.png |
| The logo is delivered as an editable vector SVG with transparent background | auto · **dealbreaker** · K1 | dermavera_logo.svg is a valid SVG containing vector <path> geometry (not an embedded raster bitmap) with a transparent/no background fill |
| The vectorized logo preserves the supplied mark and wordmark faithfully | expert · **dealbreaker** · K2 | dermavera_logo.svg reproduces the supplied molecule/droplet monogram glyph and the legible 'DERMAVERA' wordmark in a single slate-teal ink, with clean crisp paths and no regenerated/altered letterforms or invented elements |
| The type system recommends a display + text pairing with PostScript names plus rationale | auto · mandatory · K1 | dermavera_type_system.json contains a display typeface and a text typeface, each given by PostScript name, plus a rationale field |
| The recommended type pairing fits the clinical/premium identity brief | expert · quality · K4 | The display+text pairing in dermavera_type_system.json reads as clean, minimalist, modern, science-driven and premium-not-luxurious with strong typography, consistent with the stated DERMAVERA aesthetic |
| The merged label PDF contains exactly one label artboard per SKU row | auto · mandatory · K1 | dermavera_labels_merged.pdf has exactly 3 label artboards/pages, one per CSV row (Vitamin-C Brightening Serum, Barrier Repair Cream, Gentle Gel Cleanser) |
| Each merged label shows the correct per-SKU copy from the CSV verbatim | auto · mandatory · K1 | Via OCR each of the 3 labels shows its row's sku_name, claim, volume and inci_line verbatim — e.g. the Serum label shows 'Vitamin-C Brightening Serum', '15% L-Ascorbic Acid — clinically tested', '30 ml e', and 'Aqua, Ascorbic Acid, Propylene Glycol, Ferulic Acid, Tocopherol' |
| The merged label PDF is print-ready CMYK with 3mm bleed and crop marks on 70x90mm artboards | auto · **dealbreaker** · K1 | dermavera_labels_merged.pdf is CMYK with 3mm bleed and crop marks present on 70x90mm label artboards |
| The carton PDF is exported from the authored carton.indd with the finished hero placed in HERO_PLATE | expert · mandatory · K6 | dermavera_carton_print.pdf is the 5-panel unit carton from carton.indd showing the finished white-bg hero plate in the HERO_PLATE front-panel frame and the placed DERMAVERA logo, exported (not a re-composed or regenerated layout) |
| The carton PDF is print-ready CMYK with bleed and registration/crop marks | auto · **dealbreaker** · K1 | dermavera_carton_print.pdf is CMYK with 3mm bleed and registration + crop marks present |
| Neutral, trustworthy color is consistent across every produced hero image | expert · quality · K4 | The clinical hero, the 1:1 crop and the wide canvas share one neutral clinical color balance with no warm/cool cast drift between them |
| The Firefly board deep-link assembles the full system for sign-off | auto · mandatory · K1 | dermavera_brand_board_deeplink is a working Firefly Board URL collecting the finished hero, 1:1 crop, wide canvas, mono variant, vector logo and label proofs onto one board |
| The editable source files demanded by the brief are retained and delivered | auto · mandatory · K1 | The delivery retains the editable sources alongside the print-ready PDFs: the vector dermavera_logo.svg plus the authored label.ai and carton.indd |


[[PAGEBREAK]]
### AO-02 · Performance-ready Meta ad product creatives: white-bg clean-up, brand color grade, multi-ratio outpaint set, and vectorized logo for paid-social testing
**Brand:** E-commerce, Retail & Product &nbsp;·&nbsp; **Operation:** O2 Masked recolor & isolation (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (21 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Turn the client's raw product shot, lifestyle backdrop, and logo into a performance-ready Meta ad creative kit: a retouched pure-white-bg hero, a brand-graded variant, three platform-ratio outpainted canvases (1:1 / 4:5 / 9:16), a vectorized logo, and a Firefly review board.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| done_dripper_studio_raw.jpg | image | Photoreal studio product shot of a matte-ceramic pour-over coffee dripper in soft teal-green glaze, shot on a |
| done_kitchen_lifestyle_plate.jpg | image | Photoreal bright modern kitchen countertop scene, warm morning light, light oak counter, soft out-of-focus bac |
| done_wordmark_logo.png | image | Flat clean brand wordmark logo reading 'DONE' in a confident geometric sans-serif, solid brand teal #0F6E64 le |
| done_brand_guidelines.pdf | pdf | A 1-page brand guideline sheet for homeware brand 'DONE': title 'DONE — Brand Basics', a color palette block s |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| done_hero_pure_white.png | image | Retouched product hero on a true pure-white (#FFFFFF) e-commerce background, product isolated with clean edge, no gray cast / no shadow halo, straightened and auto-toned, |
| done_hero_brand_graded.jpg | image | Brand-consistent color-graded hero: warm premium ceramic, on-palette teal accents (HSL nudged toward #0F6E64), exposure/contrast/temperature tuned for paid-social punch, |
| done_creative_1x1.jpg | image | 1:1 feed square (1080x1080) with the product centered and the clean background AI-outpainted to fill the square — product not cropped. |
| done_creative_4x5.jpg | image | 4:5 portrait feed (1080x1350) produced by outpainting the graded hero's background vertically; product preserved, brand whitespace extended. |
| done_creative_9x16.jpg | image | 9:16 Stories/Reels vertical (1080x1920) produced by outpainting top/bottom; generous brand negative space left for the handed-off headline/CTA copy. |
| done_logo_vector.svg | vector | Clean vectorized DONE wordmark + dripper glyph as SVG, scalable crisp for any ad size, solid brand-teal paths on transparent. |
| done_font_direction.json | data | font_recommend output: geometric-sans headline + humanist-sans body pairing matching the brand-guideline type note, to steer the handed-off on-image typesetting step. |
| done_review_board_link | data | Firefly Boards deep-link assembling the hero, graded hero, and three ratio canvases as one client-review moodboard for Slack sign-off. |

**Layer-3 verifier checks** — expert-authored (16 checks, 1 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| The pure-white hero deliverable done_hero_pure_white.png is delivered as a PNG at ~4000x3000px | auto · mandatory · K1 | A file named done_hero_pure_white.png exists, is a valid PNG, and its dimensions are approximately 4000x3000px (within +/-5% to allow the tight product+whitespace crop from image_crop_to_bounds) |
| The hero background is a true pure-white #FFFFFF e-commerce background with no gray cast | auto · **dealbreaker** · K1 | Sampling the background pixels of done_hero_pure_white.png (the four corners and areas outside the dripper) returns #FFFFFF (RGB 255,255,255) with no residual cool gray cast from the source sweep |
| The product in the pure-white hero is cleanly isolated with no stray seamless-paper shadow halo or gray fringe at the base | expert · mandatory · K3 | An expert sees the dripper cut out with a clean edge and no seamless-paper contact-shadow halo or gray fringe remaining around its base (the source shadow halo has been removed) |
| The pure-white hero is straightened (the ~2-degree source tilt corrected) and auto-toned | expert · mandatory · K3 | An expert confirms the product/sweep horizon reads level (the ~2-degree source tilt is corrected) and exposure/contrast looks neutral and well-exposed, not the underexposed flat source |
| The brand-graded hero deliverable done_hero_brand_graded.jpg is delivered as a high-quality JPEG | auto · mandatory · K1 | A file named done_hero_brand_graded.jpg exists and is a valid high-quality JPEG |
| The brand-graded hero reads warm and premium with on-palette teal accents nudged toward brand teal #0F6E64 | expert · mandatory · K2 | An expert confirms the ceramic reads warm/premium (not clinical-cold) and the teal-green glaze accents sit on-palette toward brand teal #0F6E64 |
| The 1:1 feed creative done_creative_1x1.jpg is delivered at exactly 1080x1080 | auto · mandatory · K1 | A file named done_creative_1x1.jpg exists and is exactly 1080x1080px |
| The 4:5 portrait creative done_creative_4x5.jpg is delivered at exactly 1080x1350 | auto · mandatory · K1 | A file named done_creative_4x5.jpg exists and is exactly 1080x1350px |
| The 9:16 vertical creative done_creative_9x16.jpg is delivered at exactly 1080x1920 | auto · mandatory · K1 | A file named done_creative_9x16.jpg exists and is exactly 1080x1920px |
| Across all three ratio canvases the product is preserved uncropped and the clean background is AI-outpainted (not cropped) to fill each frame | expert · mandatory · K3 | An expert confirms that in all three of done_creative_1x1/4x5/9x16 the full dripper is intact and uncropped, and the surrounding clean brand background is extended by outpaint (generative_expand) to fill the new aspect ratio rather than cropping the product |
| The 9:16 vertical leaves generous brand negative space for the handed-off headline/CTA copy | expert · quality · K3 | An expert confirms done_creative_9x16.jpg has clear brand negative space (top/bottom) reserved for the handed-off copy, with no baked-on headline/offer/CTA text |
| No headline/offer/CTA copy and no logo lockup is baked onto any of the five image deliverables (typeset assembly is handed off, explicitly out of scope for this connector pass) | expert · mandatory · K1 | An expert/OCR confirms the pure-white hero, brand-graded hero, and three ratio canvases carry no on-image headline/offer/CTA type and no overlaid DONE logo lockup, matching the brief's explicit out-of-scope note |
| The vectorized logo deliverable done_logo_vector.svg is delivered as a true SVG vector file | auto · mandatory · K1 | A file named done_logo_vector.svg exists and is a valid SVG composed of vector paths (not a raster image embedded in an SVG wrapper) |
| The vector logo reproduces the supplied DONE wordmark + dripper line-mark glyph as solid brand-teal #0F6E64 paths on transparency, crisp at any scale | expert · mandatory · K2 | An expert confirms done_logo_vector.svg renders the supplied 'DONE' wordmark and the coffee-dripper line-mark glyph in solid brand teal #0F6E64 on a transparent background, with clean paths and no stray artifacts, scaling crisply |
| The font-direction deliverable done_font_direction.json recommends a geometric-sans headline paired with a humanist-sans body, matching the brand-guideline type note | auto · mandatory · K1 | done_font_direction.json contains a font_recommend output specifying a geometric-sans headline font and a humanist-sans body font, consistent with the guideline note 'Headlines: geometric sans; Body: humanist sans' |
| The Firefly review board deep-link done_review_board_link assembles exactly the five image deliverables for client sign-off | auto · mandatory · K6 | done_review_board_link is a valid Firefly Boards deep-link whose board contains exactly the five image deliverables: done_hero_pure_white, done_hero_brand_graded, done_creative_1x1, done_creative_4x5, and done_creative_9x16 |


[[PAGEBREAK]]
### AO-03 · E-commerce white-background product retouch suite + vectorized brand mark
**Brand:** E-commerce, Retail & Product &nbsp;·&nbsp; **Operation:** O2 Masked recolor & isolation (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (17 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Turn a client's raw, messy-background product photo into a pure-white-background marketplace catalog image and convert their rough hand-drawn logo sketch into a clean, brand-colored, scalable vector logo — then package everything for delivery.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| raw_product_serum_bottle.jpg | image | A real amateur smartphone product photo, NOT studio quality: a single amber-glass cosmetic serum bottle with a |
| logo_sketch_phone_photo.jpg | image | A phone photograph of a rough hand-inked logo sketch on a piece of slightly off-white textured paper. The mark |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| AURELIA_serum_2000x2000_white.jpg | image | Square 2000×2000 px JPEG, product centered on pure #FFFFFF seamless background, leveled, auto-toned, vibrance-balanced, highlights recovered — Amazon/Etsy/Shopify main-im |
| AURELIA_serum_cutout_transparent.png | image | Product cut-out on transparent background (alpha PNG), leveled and toned, for re-use on colored lifestyle backgrounds and brand-kit compositing by the client. |
| AURELIA_logo_vector.svg | vector | Clean scalable SVG traced from the hand-inked sketch — crisp paths at 16px favicon through 3m banner, neutral/original ink color. |
| AURELIA_logo_brandgreen.svg | vector | Recolored vector logo in brand botanical green (~#1E5E3A) via solid color overlay, scalable SVG for the brand kit. |
| font_pairing_recommendations.txt | data | 2-3 recommended wordmark fonts that pair with the hand-drawn mark for the 'AURELIA BOTANICALS' lockup, returned by font_recommend. |
| AURELIA_delivery_folder | data | A clearly-named CC asset delivery folder containing the catalog hero JPEG, the transparent cut-out PNG, both SVG logos and the font note — ready to pull into listings and |

**Layer-3 verifier checks** — expert-authored (17 checks, 3 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| Catalog hero JPEG is exactly 2000x2000 px square | auto · mandatory · K1 | AURELIA_serum_2000x2000_white.jpg has width == 2000 px AND height == 2000 px |
| Catalog hero is delivered in JPEG format | auto · mandatory · K1 | AURELIA_serum_2000x2000_white file is a valid JPEG (JPEG/JFIF magic bytes), not PNG/WEBP/other |
| Catalog hero background is pure white #FFFFFF with no grey cast | auto · **dealbreaker** · K1 | Sampled background pixels (corner and edge samples in the seamless region around the bottle) of AURELIA_serum_2000x2000_white.jpg read RGB (255,255,255) within JPEG noise tolerance of +/-2 on each channel — no grey cast, matching the brief's hard #FFFFFF Amazon main-image requirement |
| Product is centered on the square canvas | expert · mandatory · K3 | In AURELIA_serum_2000x2000_white.jpg the amber serum bottle's subject bounding-box centroid sits near the canvas center with balanced left/right and top/bottom margins, per the brief 'product centered' |
| Bottle is leveled (the ~4-degree tilt is corrected) | expert · mandatory · K3 | The serum bottle stands vertically upright in AURELIA_serum_2000x2000_white.jpg and AURELIA_serum_cutout_transparent.png with no residual ~4-degree tilt and no diagonal table edge remaining, per the brief 'Level the horizon (the table edge is tilted)' |
| Cluttered original background (tea towel, mug, power cord, wood table, dust) is fully removed | expert · mandatory · K3 | No element of the original messy table scene (crumpled tea towel, coffee mug, power cord, wood grain, dust) is visible in AURELIA_serum_2000x2000_white.jpg; only the bottle on white remains |
| Background-removal mask edges around the bottle are clean | expert · quality · K3 | The cut-out edge of the amber bottle (including black dropper cap and curved glass) is crisp with no halo, fringe, leftover background pixels, or chewed-into-subject artifacts |
| Blown-out specular highlights on the amber glass are recovered | expert · mandatory · K4 | The bright window-light hot spots / specular blowout on the curved amber glass are tamed so the glass reads cleanly with recovered detail rather than pure clipped white, per the brief 'recover the blown-out highlights/hot spots' |
| Exposure and color are balanced with true-to-life amber pop and no oversaturated white | expert · quality · K4 | AURELIA_serum_2000x2000_white.jpg shows balanced exposure, neutral color (no window-light cast), and natural vibrance/saturation pop on the amber glass without oversaturating or tinting the white sweep |
| Transparent cut-out PNG has a real alpha channel with genuinely transparent background | auto · mandatory · K1 | AURELIA_serum_cutout_transparent.png is a PNG with an alpha channel and alpha == 0 in the background region around the subject (genuinely transparent), not a flattened white/opaque background |
| Cleaned logo is delivered as a vector SVG with real geometry | auto · **dealbreaker** · K1 | AURELIA_logo_vector.svg is a valid SVG file containing vector <path>/<polygon> geometry (not merely an embedded raster <image> element) |
| Vector logo is traced from the supplied hand-inked sketch, not regenerated | expert · **dealbreaker** · K2 | AURELIA_logo_vector.svg reproduces the supplied sketch's mark (a single sprig of laurel/olive leaves curving into a small circle) with crisp clean paths and the stray pencil guide lines removed; it is a faithful trace of the supplied logo_sketch_phone_photo.jpg input, NOT a regenerated or redrawn logo |
| Neutral vector logo retains the original ink color (is not the green version) | auto · mandatory · K1 | AURELIA_logo_vector.svg fills the mark in a neutral/original-ink color (dark grey-black, NOT brand green ~#1E5E3A), distinct from the recolored AURELIA_logo_brandgreen.svg, per the output spec 'neutral/original ink color' |
| Recolored logo SVG uses brand botanical green ~#1E5E3A | auto · mandatory · K2 | AURELIA_logo_brandgreen.svg is a scalable vector file that fills the mark with brand botanical green approximately #1E5E3A (R~30, G~94, B~58) within a small tolerance |
| Font pairing note recommends 2-3 fonts for the AURELIA BOTANICALS wordmark | auto · mandatory · K1 | font_pairing_recommendations.txt names between 2 and 3 specific fonts recommended to pair with the hand-drawn mark for the 'AURELIA BOTANICALS' wordmark lockup |
| Delivery folder is a clearly-named folder containing all four assets plus the font note | auto · mandatory · K6 | AURELIA_delivery_folder is a clearly-named delivery folder containing exactly these 5 items: AURELIA_serum_2000x2000_white.jpg, AURELIA_serum_cutout_transparent.png, AURELIA_logo_vector.svg, AURELIA_logo_brandgreen.svg and font_pairing_recommendations.txt |
| Brand name appears exactly as 'AURELIA BOTANICALS' | auto · mandatory · K2 | Wherever the brand name is referenced (font note, asset/folder naming, logo wordmark) it reads exactly 'AURELIA BOTANICALS' with no altered or misspelled wording |


[[PAGEBREAK]]
### AO-04 · Silver Jewelry iPhone Shots to White-Background E-commerce Set (JPEG + transparent PNG)
**Brand:** Fashion & Apparel &nbsp;·&nbsp; **Operation:** O2 Masked recolor & isolation (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (16 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Turn a handheld iPhone shot of a silver jewellery piece into a clean, colour-accurate, uniform-white e-commerce set: a 3000x3000 sRGB JPEG plus a matching transparent PNG, ready to slot straight into the online store.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| iphone_silver_ring_hero.heic | image | Photoreal handheld iPhone product photo of a single ornate sterling silver ring set with a faceted deep-blue s |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| silver_ring_hero_3000.jpg | image | 3000x3000 px, 1:1 square, sRGB, JPEG under 2 MB, uniform pure-white background, neutral colour (no cast), accurate silver metal tone and faithful sapphire colour, pin-sha |
| silver_ring_hero_transparent.png | image | Matching PNG of the same graded piece on a fully transparent background (alpha), same grade as the JPEG, for layering on coloured store sections. |
| delivery_folder | data | Asset folder structure containing the finished JPEG, the transparent PNG, and the original supplied iPhone file, named for client download. |
| review_board_deeplink | data | Firefly Board deep-link assembling the graded master frame(s) for one-click client approval of the look before the remaining 20 pieces are run. |

**Layer-3 verifier checks** — expert-authored (16 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| The finished JPEG deliverable silver_ring_hero_3000.jpg has pixel dimensions of exactly 3000 x 3000 (true 1:1 square). | auto · mandatory · K1 | Image width == 3000 px AND height == 3000 px as read from silver_ring_hero_3000.jpg. |
| silver_ring_hero_3000.jpg is encoded as JPEG in the sRGB colour space. | auto · **dealbreaker** · K1 | silver_ring_hero_3000.jpg file format == JPEG AND the colour profile is sRGB (embedded sRGB profile, or untagged/assumed-sRGB with no conflicting profile such as Display P3 or Adobe RGB). |
| The finished JPEG file size is under 2 MB. | auto · mandatory · K1 | On-disk size of silver_ring_hero_3000.jpg < 2,097,152 bytes (2 MB). |
| A matching PNG of the same piece, silver_ring_hero_transparent.png, exists with a genuinely transparent background. | auto · mandatory · K1 | silver_ring_hero_transparent.png is PNG format AND has an alpha channel containing fully transparent (alpha == 0) pixels in the background region surrounding the jewellery. |
| The JPEG background is a uniform pure / near-white with no colour cast. | auto · **dealbreaker** · K1 | Sampled background pixels of silver_ring_hero_3000.jpg are near RGB 255/255/255 (each channel >= 250) AND the three channels are balanced (max channel spread <= 5) so there is no warm/cool tint. |
| The PNG carries the identical grade as the JPEG (same colour-corrected graded master), differing only in background. | expert · mandatory · K2 | When silver_ring_hero_transparent.png is composited on white, the silver metal tone and sapphire colour visually match silver_ring_hero_3000.jpg (both derive from the same graded master, not separately graded). |
| The warm iPhone white-balance cast is neutralised so the silver reads as clean, neutral silver. | expert · mandatory · K4 | Reviewer confirms the metal highlights/mid-tones read as neutral clean-silver with no residual warm/yellow cast carried from the input frame. |
| The faceted deep-blue sapphire renders as a faithful, true blue gemstone colour. | expert · mandatory · K4 | Reviewer confirms the sapphire reads as an accurate deep-blue (selectively saturated correctly, not washed out, oversaturated, or hue-shifted). |
| The ring band is pin-sharp on the hero angle. | expert · mandatory · K4 | Reviewer confirms the silver band is tack-sharp / in crisp focus with no softening, blur, or destructive artefacts introduced by the editing chain. |
| The ~2-3 degree handheld tilt is corrected so the piece is geometrically straight. | expert · quality · K3 | Reviewer confirms the piece and the implied horizon are level, with no visible residual tilt. |
| The square 1:1 frame was reached by extending the white canvas, not by stretching or distorting the ring. | expert · mandatory · K3 | Reviewer confirms the ring retains its original undistorted proportions and the extra area is added uniform white canvas (no anamorphic stretch to fill the square). |
| The cut-out edge between the jewellery and the white/transparent background is clean. | expert · quality · K3 | Reviewer confirms the subject mask edge is precise around the ring and stone with no white halo, fringing, or chewed-away metal/prongs. |
| A delivery folder is assembled containing the finished JPEG, the transparent PNG, and the original supplied iPhone file. | auto · mandatory · K6 | delivery_folder contains exactly the three named assets: silver_ring_hero_3000.jpg, silver_ring_hero_transparent.png, and iphone_silver_ring_hero.heic. |
| A Firefly Board deep-link is produced assembling the graded master frame(s) for client approval. | auto · mandatory · K6 | review_board_deeplink resolves to a Firefly Board URL that contains the graded master and finished hero frame (silver_ring_hero_3000.jpg) for one-click client review. |
| The uniform white backdrop was produced non-generatively (select piece -> invert -> solid-white fill), not via generative fill or prompt-based background replacement. | expert · mandatory · K7 | Workflow evidence shows the background was driven to white via image_select_by_prompt -> image_invert_selection -> image_fill_area (solid white RGB 255/255/255), with no generative-fill or background-replace-by-prompt step used. |
| The original supplied iphone_silver_ring_hero.heic is preserved and delivered unaltered alongside the edited outputs. | auto · mandatory · K2 | The original iPhone file delivered in delivery_folder is byte-identical to the supplied input iphone_silver_ring_hero.heic (not the straightened/graded version). |


[[PAGEBREAK]]
### AO-05 · Weekly Meta Ad Creative Batch for a Hemp/Supplement E-Commerce Brand: White-BG Product Isolation, Compliance-Safe Color Grade, Multi-Placement Sizing, Vectorized Logo + Motion Variant
**Brand:** Health, Wellness & Medical &nbsp;·&nbsp; **Operation:** O2 Masked recolor & isolation (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (23 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Take one hemp/CBD product SKU through a full Adobe pipeline to produce a Meta-ready ad creative set: a clean white-background hero, a tone-corrected lifestyle hero outpainted and cropped to the three Meta placements (1:1, 4:5, 9:16), a crisp vectorized logo lockup, and one motion variant reframed to 9:16 story.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| tincture_desk_raw.jpg | image | Photoreal smartphone-quality product photo of a 30ml amber glass CBD tincture bottle with a black dropper cap |
| tincture_kitchen_lifestyle.jpg | image | Photoreal lifestyle photo, portrait orientation 3:4, of the same amber glass 'BALANCE' CBD tincture bottle sit |
| balance_wordmark_logo.png | image | Flat brand wordmark logo on a transparent background: the single word 'BALANCE' in a clean modern humanist san |
| dropper_in_use_6s.mp4 | video | 6-second 1080p photoreal clip: a hand picks up the amber 'BALANCE' CBD tincture dropper, squeezes the bulb, an |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| product_hero_white_1080.jpg | image | Pure white (#ffffff) background product hero, subject isolated from the cluttered desk and composited on flat white, auto-toned for accurate amber oil color, square 1080× |
| lifestyle_hero_corrected.jpg | image | Straightened (horizon leveled), exposure-corrected, tone-balanced lifestyle hero of the kitchen shot at full source resolution, warm cast neutralized, ready to feed place |
| lifestyle_feed_1x1_1080.jpg | image | 1:1 Meta feed square, 1080×1080, subject-aware crop of the corrected lifestyle hero. |
| lifestyle_feed_4x5_1080x1350.jpg | image | 4:5 Meta feed portrait, 1080×1350, subject-aware crop of the corrected lifestyle hero. |
| lifestyle_story_9x16_1080x1920.jpg | image | 9:16 story/reel, 1080×1920, produced by outpainting the portrait lifestyle hero on the short axis then cropping to 9:16 so no product content is lost. |
| balance_wordmark.svg | vector | Clean scalable SVG of the BALANCE wordmark+leaf, single forest-green fill, transparent, for crisp overlay at any size. |
| dropper_story_9x16.mp4 | video | 9:16 vertical reframe of the 6-second dropper clip, same length (no trim), 1080×1920, story/reel motion ad. |
| balance_meta_creative_set.zip | data | Single zipped hand-off package containing all of the above static, vector, and motion deliverables plus a folder structure on Adobe storage. |

**Layer-3 verifier checks** — expert-authored (17 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| The single zip hand-off package contains all seven non-zip deliverables | auto · mandatory · K1 | balance_meta_creative_set.zip contains exactly these 7 assets: product_hero_white_1080.jpg, lifestyle_hero_corrected.jpg, lifestyle_feed_1x1_1080.jpg, lifestyle_feed_4x5_1080x1350.jpg, lifestyle_story_9x16_1080x1920.jpg, balance_wordmark.svg, and dropper_story_9x16.mp4 |
| The white-bg product hero is a square 1080x1080 JPEG | auto · mandatory · K1 | product_hero_white_1080.jpg is exactly 1080x1080 px and encoded as JPEG |
| The product hero background is pure white | auto · **dealbreaker** · K1 | Sampled background pixels (non-subject corners/edges) of product_hero_white_1080.jpg read #ffffff (truly white, no residual desk clutter or color cast) |
| The tincture bottle is cleanly isolated from the original cluttered desk in the white-bg hero | expert · mandatory · K3 | product_hero_white_1080.jpg shows only the BALANCE bottle on flat white with no coffee mug, papers, pen, laptop edge or desk remnants, and mask edges around glass/dropper are clean |
| The amber CBD oil color reads true and accurate across the corrected outputs | expert · mandatory · K4 | The amber oil in product_hero_white_1080.jpg and lifestyle_hero_corrected.jpg reads as a true amber tone (auto-toned / color-temperature corrected, no green/orange cast carried over from the desk or warm golden kitchen light) |
| The lifestyle hero horizon is leveled (straightened) | expert · mandatory · K3 | lifestyle_hero_corrected.jpg shows a level horizon with the marble counter line horizontal (the ~4-degree tilt of the source removed) |
| The lifestyle hero is exposure-corrected and the warm golden cast neutralized | expert · mandatory · K4 | lifestyle_hero_corrected.jpg is lifted from the underexposed source to a correct mid-tone and the warm golden cast is neutralized so the marble reads neutral and the amber reads true |
| The 1:1 feed crop is 1080x1080 | auto · mandatory · K1 | lifestyle_feed_1x1_1080.jpg is exactly 1080x1080 px (JPEG) |
| The 4:5 feed portrait crop is 1080x1350 | auto · mandatory · K1 | lifestyle_feed_4x5_1080x1350.jpg is exactly 1080x1350 px (JPEG) |
| The 9:16 story placement is 1080x1920 | auto · mandatory · K1 | lifestyle_story_9x16_1080x1920.jpg is exactly 1080x1920 px (JPEG) |
| The three placement crops keep the tincture bottle in frame (subject-aware) | expert · mandatory · K3 | The BALANCE bottle is the kept, in-frame focal subject in lifestyle_feed_1x1_1080.jpg, lifestyle_feed_4x5_1080x1350.jpg, and lifestyle_story_9x16_1080x1920.jpg — not cut off or pushed out of frame |
| The 9:16 story was produced by outpainting the portrait hero before cropping so no product content is lost | expert · quality · K6 | lifestyle_story_9x16_1080x1920.jpg shows generatively-expanded marble/scene filling the 9:16 frame with the bottle fully intact (not a hard crop that amputates product), consistent with an expand-then-crop chain |
| The wordmark deliverable is a true vector SVG with transparent background | auto · mandatory · K1 | balance_wordmark.svg is a valid SVG file containing vector path data (not a raster image embedded in an SVG wrapper) with a transparent background |
| The vectorized wordmark preserves the BALANCE wordmark, leaf glyph, and forest-green fill | expert · **dealbreaker** · K2 | balance_wordmark.svg renders the word 'BALANCE' plus the small leaf glyph in a single deep forest-green fill, with crisp clean edges faithful to the supplied PNG (not regenerated or restyled) |
| The motion variant is a 9:16 vertical 1080x1920 video at the original 6-second length | auto · mandatory · K1 | dropper_story_9x16.mp4 is exactly 1080x1920 px, aspect 9:16, and approximately 6 seconds long (same length as the source, no trim) |
| The dropper motion variant is a visual reframe of the source clip with the dropper action kept in frame | expert · quality · K6 | dropper_story_9x16.mp4 shows the same hand/dropper/drops-into-water action reframed for vertical with the action centered/in-frame, same length and audio as source (resize is visual-only) |
| No exaggerated claims or non-compliant text are baked into any creative (compliance-safe positioning) | expert · mandatory · K7 | None of the static, story, or motion deliverables (product_hero_white_1080.jpg, lifestyle_hero_corrected.jpg, the three placement crops, dropper_story_9x16.mp4) have exaggerated health/CBD claims or text overlays baked into the image/video — clean studio/lifestyle imagery only, positioned to avoid Meta compliance flags |


[[PAGEBREAK]]
### AO-06 · White-Background Catalog Cleanup for a Firearms/Optics/Outdoor Shopify Store
**Brand:** Nonprofit, Religious & Community &nbsp;·&nbsp; **Operation:** O2 Masked recolor & isolation (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (16 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Take a batch of inconsistent distributor-supplied product photos for a firearms/optics/outdoor Shopify store and turn them into clean, straightened, color-corrected, pure-white-background, square marketplace hero images (plus transparent-PNG tile variants and a vectorized listing badge), all organized into a review board and a tidy asset folder.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| raw_thermal_scope_distributor.jpg | image | Photoreal product photograph of a handheld thermal weapon scope (matte black cylindrical body, rubberized eyep |
| distributor_brand_badge.png | image | A flat, single-color (solid dark-charcoal) vector-style brand mark / logo for an optics manufacturer: a simple |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| scope_master_corrected.jpg | image | Straightened, cropped-to-product, auto-toned, color-cast-neutralized master JPEG of the thermal scope, sRGB, high quality. The clean base every other deliverable derives |
| scope_whitebg_hero.jpg | image | Pure #FFFFFF solid-background hero of the isolated scope, marketplace-compliant (no gradient, no scene), sRGB JPEG. |
| scope_cutout.png | image | Transparent-background PNG cut-out of the scope for collection tiles / bundle mock-ups, edges clean, alpha channel. |
| scope_hero_square_2048.jpg | image | Square 1:1 Shopify/Amazon hero, generative-expanded to a square canvas then resized/exported at exactly 2048x2048, sRGB JPEG. |
| brand_badge.svg | vector | Clean scalable SVG of the distributor brand mark vectorized from the flat PNG, for crisp display at any listing size. |
| catalog_typeface_recommendation | data | A recommended clean sans-serif catalog/listing typeface (name + rationale) from font_recommend. |
| hero_review_board | data | Firefly Board deep-link assembling the corrected master, white-bg hero, cut-out, and square hero for one-click owner approval. |
| Cleaned_Catalog_Assets/ folder | data | A named CC asset folder containing all finished SKU deliverables, copied in and organized for handoff to the next batch. |

**Layer-3 verifier checks** — expert-authored (16 checks, 4 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| scope_master_corrected.jpg deliverable is present as an sRGB JPEG | auto · mandatory · K1 | A file named scope_master_corrected.jpg exists in the deliverable set; format == JPEG and color space == sRGB |
| Corrected master is straightened, cropped to product, and exposure/tone normalized | expert · mandatory · K3 | In scope_master_corrected.jpg the thermal scope sits level (the original ~4-degree clockwise tilt is removed and the product axis is square to the frame), the loose/uneven empty margins are trimmed to the product bounds, and exposure/contrast is normalized (not under- or over-exposed) |
| Warm tungsten color cast is neutralized toward neutral white balance | expert · mandatory · K4 | The warm yellow-orange tungsten cast present in the raw input is corrected toward a neutral white balance in scope_master_corrected.jpg (background reads neutral, no residual yellow-orange tint) |
| scope_whitebg_hero.jpg has a pure #FFFFFF solid background with no gradient | auto · **dealbreaker** · K1 | Sampling the background region (outside the scope) of scope_whitebg_hero.jpg returns RGB (255,255,255) / hex #FFFFFF across the whole field, with no gradient and no off-white pixels; file is an sRGB JPEG |
| White-bg hero background is solid white only — no AI-invented scene or composited element | expert · **dealbreaker** · K7 | The background of scope_whitebg_hero.jpg is a flat solid-white field with no painted scene, props, gradient, or composited objects; nothing has been generatively invented behind the product |
| scope_cutout.png is a transparent-background PNG cut-out of the scope | auto · mandatory · K1 | scope_cutout.png exists, is PNG format with an alpha channel, and the background region is fully transparent (alpha == 0) while the scope pixels are opaque (alpha == 255) |
| Cut-out mask edges are clean around the scope | expert · quality · K3 | In scope_cutout.png the alpha edge follows the scope silhouette cleanly — no leftover seamless/halo fringe, and no chewed-away product detail (rail, eyepiece, control buttons intact) |
| scope_hero_square_2048.jpg is exactly 2048x2048 pixels, square 1:1, sRGB JPEG | auto · **dealbreaker** · K1 | scope_hero_square_2048.jpg dimensions == 2048 x 2048 (1:1 square), format == JPEG, color space == sRGB |
| Square hero was made by outpainting the white field only, not by painting onto the product | expert · mandatory · K7 | scope_hero_square_2048.jpg fills the square canvas by extending the pure-white field around the scope; the background remains solid white with no invented scene, and nothing is generatively painted onto or added to the product body |
| brand_badge.svg is a true vector SVG (not an embedded raster image) | auto · mandatory · K2 | brand_badge.svg exists, is valid SVG markup containing vector path/shape elements, and does NOT consist of (or merely wrap) an embedded raster <image> element |
| Vectorized badge faithfully reproduces the supplied flat single-color brand mark | expert · mandatory · K2 | brand_badge.svg visually matches the supplied distributor logo from distributor_brand_badge.png — the reticle-and-mountain emblem with its wordmark beneath, in a single flat dark-charcoal color, same shapes, crisp edges that scale cleanly, with no added gradients, no photographic texture, and no invented elements |
| A clean sans-serif catalog typeface recommendation is provided | expert · mandatory · K5 | catalog_typeface_recommendation names a specific sans-serif typeface (sourced from font_recommend) plus a rationale suited to a clean product-listing/catalog use |
| A Firefly review board assembling the hero set is delivered | auto · mandatory · K6 | hero_review_board is a Firefly Board deep-link/URL that assembles the corrected master, white-bg hero, cut-out, and square hero for one-click owner approval |
| Cleaned_Catalog_Assets/ folder contains the organized finished deliverables | auto · mandatory · K6 | A CC asset folder named 'Cleaned_Catalog_Assets/' exists and contains the finished SKU deliverables copied in for handoff: scope_master_corrected.jpg, scope_whitebg_hero.jpg, scope_cutout.png, scope_hero_square_2048.jpg, and brand_badge.svg |
| All four hero image deliverables depict the same single thermal scope SKU consistently | expert · mandatory · K3 | scope_master_corrected.jpg, scope_whitebg_hero.jpg, scope_cutout.png, and scope_hero_square_2048.jpg all show the same handheld thermal weapon scope from the supplied raw input — same product, consistent correction across the set, with no deliverable distorted in proportion |
| No deliverable distorts, recolors, or composites onto the product itself | expert · **dealbreaker** · K7 | Across all image deliverables the scope is not stretched/warped, is not recolored beyond honest color-cast correction (true matte-black body and materials preserved), and has nothing composited or generatively painted onto the product body — only background and canvas operations were applied |


[[PAGEBREAK]]
### AO-07 · Men's pendant line: vectorize the 2D spec sketch + retouch and catalog-prep the sample studio shots
**Brand:** Automotive, Industrial & Agriculture &nbsp;·&nbsp; **Operation:** O4 Preset retouch & look-dev (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (24 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*From the industrial designer's raster pendant sketch and two mixed-lighting workbench photos of a stainless-steel sample pendant and chain, produce a clean factory-ready vector spec asset plus retouched, isolated, color-accurate catalog hero shots (one expanded to a catalog canvas, one duotone print-screen variant) and gather everything on a Firefly board for the design team.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| pendant_sketch_raster.png | image | A flat 2D technical line-art drawing of a men's pendant, front elevation: a rounded-square stainless-steel pen |
| sample_pendant_on_bench.jpg | image | Photoreal close-up product reference photo of a single brushed stainless-steel men's pendant (rounded-square, |
| sample_chain_on_bench.jpg | image | Photoreal product reference photo of a men's stainless-steel box-link chain (about 4mm wide) laid out in a loo |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| pendant_spec_lineart.svg | vector | Clean scalable SVG of the deskewed, tight-cropped pendant line-art, crisp at any print size, suitable as a dimensional spec reference for the factory. |
| pendant_hero_catalog.png | image | Retouched, white-balanced, auto-toned sample pendant cut out from the bench onto a clean solid catalog background and outpainted/expanded to a roomy catalog hero canvas ( |
| pendant_spec_screenprint.png | image | High-contrast duotone/halftone 'print-screen' variant of the hero pendant for the black-and-white spec sheet. PNG. |
| chain_hero_catalog.png | image | The box-link chain color-matched to the pendant (same neutral white balance + tonal treatment) and isolated on the same clean catalog background, so pendant and chain rea |
| pendant_line_review_board | deep-link | A single Firefly board assembling the vector spec, the catalog hero, the screen-print variant and the chain hero as a moodboard/deep-link for the brand's design team to r |

**Layer-3 verifier checks** — expert-authored (16 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All five expected deliverables are present: pendant_spec_lineart.svg, pendant_hero_catalog.png, pendant_spec_screenprint.png, chain_hero_catalog.png, and the pendant_line_review_board Firefly board deep-link. | auto · mandatory · K1 | All five deliverables are delivered: the four files pendant_spec_lineart.svg, pendant_hero_catalog.png, pendant_spec_screenprint.png, chain_hero_catalog.png, plus the pendant_line_review_board Firefly board deep-link; missing any one of the five fails. |
| The pendant spec deliverable pendant_spec_lineart.svg is a valid scalable vector SVG (not a raster PNG/JPG renamed) containing vector path/shape line work. | auto · **dealbreaker** · K1 | File parses as well-formed SVG (MIME image/svg+xml, .svg extension) containing vector path/shape elements; it is not an embedded raster or a renamed bitmap. |
| The three image deliverables (pendant_hero_catalog.png, pendant_spec_screenprint.png, chain_hero_catalog.png) are each valid PNG files. | auto · mandatory · K1 | Each of the three image deliverables has a .png extension and a valid PNG file signature. |
| The vectorized pendant line-art in pendant_spec_lineart.svg is deskewed (square/upright), correcting the input scan's ~4-degree clockwise rotation. | expert · mandatory · K3 | The pendant outline sits square to the canvas axes with no residual ~4-degree clockwise skew from the original scan (auto_straighten applied before vectorize). |
| The vectorized pendant line-art is tight-cropped to the pendant artwork, with the scanned white paper margin/border removed. | expert · mandatory · K3 | pendant_spec_lineart.svg bounds hug the pendant line-art with no large surrounding white scan margin or paper border retained. |
| pendant_spec_lineart.svg preserves the sketch's drawn features: rounded-square body, soldered top bail loop, interior compass-rose engraving lines, and edge dimension tick marks, as clean black line work. | expert · mandatory · K2 | The vector reproduces the rounded-square pendant outline, soldered top bail loop, fine interior compass-rose engraving, and edge dimension tick marks as clean black line work without fabricating or dropping any of these spec features. |
| The pendant in pendant_hero_catalog.png is cleanly isolated from the busy machinist's bench background (no calipers, layout square, or metal shavings remaining). | expert · mandatory · K3 | No bench-clutter elements (calipers, layout square, metal shavings, workbench surface) are visible; the pendant is cleanly masked with no haloing or clipped edges. |
| pendant_hero_catalog.png places the cut-out pendant on a clean solid light-gray catalog background (solid-color fill), not on a composited photographic scene. | expert · mandatory · K1 | The background behind the pendant is a single clean solid catalog fill (light gray, consistent with image_fill_area solid-color fill), not another photo composited in. |
| pendant_hero_catalog.png is outpainted/expanded to a roomy catalog hero canvas (~4:5 portrait or wider), not a tight subject-filling crop. | auto · mandatory · K1 | Image aspect ratio is approximately 4:5 (portrait) or wider, with generous catalog space around the pendant, not a tight subject-filling crop. |
| The pendant's mixed warm-shop / cool-window yellow-green color cast is neutralized so the stainless steel reads as clean neutral white-balanced metal in pendant_hero_catalog.png. | expert · mandatory · K4 | The metal appears neutral / cool-neutral with no residual yellow-green cast; white balance reads corrected versus the off-neutral input photo. |
| Brushed-steel highlight detail is retained (not clipped to pure white) in the toned pendant hero. | expert · quality · K4 | Bright areas on the pendant keep brushed-metal grain/texture rather than blowing out to flat clipped white. |
| pendant_spec_screenprint.png is a high-contrast duotone/halftone print-screen variant of the same pendant as the hero, suitable for the black-and-white spec sheet. | expert · mandatory · K1 | The image is a high-contrast halftone/duotone (effectively B&W print-screen) rendition of the same pendant shown in pendant_hero_catalog.png, not a full-color photo. |
| chain_hero_catalog.png shows the box-link chain isolated from the bench on the SAME clean solid light-gray catalog background used for the pendant hero. | expert · mandatory · K3 | The chain is cleanly cut out (no bench clutter) and placed on the identical solid light-gray catalog background fill as pendant_hero_catalog.png. |
| The chain in chain_hero_catalog.png is color-matched to the pendant: same neutralized white balance and tonal treatment so the pair reads as one coordinated set. | expert · mandatory · K4 | The chain's metal white-balance and tonal grade visibly match the pendant hero (same neutral steel cast), so pendant and chain read as a consistent coordinated pair, not two differently-graded shots. |
| The pendant_line_review_board Firefly board assembles all four produced assets (vector spec, catalog hero, screen-print variant, chain hero) into one reviewable deep-link. | expert · mandatory · K6 | The Firefly board deep-link opens and contains all four deliverables (pendant_spec_lineart.svg, pendant_hero_catalog.png, pendant_spec_screenprint.png, chain_hero_catalog.png) gathered for the design team's refinements-and-iterations review. |
| No 3D/CAD model is fabricated and no deliverable is invented from scratch; the response delivers only the Adobe-doable 2D asset-prep slice using only generative_expand as the generative step. | expert · **dealbreaker** · K7 | Deliverables are derived from the supplied sketch and two bench photos (deskew/crop/vectorize, grade/mask/solid-fill/outpaint/halftone); no invented 3D CAD render is presented as if produced, and image_generative_expand (the hero outpaint) is the ONLY generative step used. |


[[PAGEBREAK]]
### AO-08 · Signature Bracelet Launch: Studio Retouch, White-Background E-Comm Set, Graded Hero, Expanded Social Banner & Vectorized Mark
**Brand:** Automotive, Industrial & Agriculture &nbsp;·&nbsp; **Operation:** O4 Preset retouch & look-dev (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (21 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Turn the brand's raw studio prototype shots, wordmark, and lifestyle frame into a launch image kit: a clean white-background e-commerce set, a color-graded close-up hero, an expanded social banner, and a vectorized wordmark — then assemble everything on a Firefly board for sign-off.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| bracelet_studio_hero.jpg | image | Photorealistic DSLR product photograph of a single elevated lifestyle-brand bracelet — braided dark navy waxed |
| brand_wordmark_flat.png | image | Flat raster PNG of a refined lifestyle-brand WORDMARK reading 'GATHER & CO.' in an elegant high-contrast serif |
| gathering_lifestyle_frame.jpg | image | Warm candid documentary photograph of a group of friends gathered around a wooden table at golden hour — laugh |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| ecom_white_bg_bracelet.jpg | image | Square ~2400x2400 JPEG, bracelet on pure #FFFFFF background, auto-toned + exposure/contrast corrected + warm WB, gold clasp saturation-boosted; drop-in ready for product |
| homepage_hero_closeup_4x5.jpg | image | 4:5 portrait (~2048x2560) color-graded close-up hero with a cohesive Lightroom preset look + gentle lens blur isolating the macro clasp detail. |
| social_banner_16x9.jpg | image | 16:9 (~2560x1440) banner produced by generative-expand/outpaint of the white studio sweep, leaving clean text-safe negative space for a website-hero headline. |
| wordmark_vector.svg | vector | Clean scalable SVG traced from the flat wordmark PNG; single-color charcoal, crisp paths for packaging / web / hang-tag. |
| licensed_gathering_backdrop.jpg | image | Full-resolution licensed Adobe Stock 'friends gathered at a table' lifestyle backdrop (presigned download URL) for the social team to place the banner over. |
| launch_kit_firefly_board | data | Firefly Boards deep-link assembling the graded master, white-bg e-comm shot, 4:5 hero, 16:9 banner, vectorized wordmark, and licensed backdrop for one-place review/approv |

**Layer-3 verifier checks** — expert-authored (16 checks, 4 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All six deliverables are present: ecom_white_bg_bracelet.jpg, homepage_hero_closeup_4x5.jpg, social_banner_16x9.jpg, wordmark_vector.svg, licensed_gathering_backdrop.jpg, and the launch_kit_firefly_board link. | auto · mandatory · K1 | Exactly 6 deliverables exist matching the names ecom_white_bg_bracelet.jpg (JPEG), homepage_hero_closeup_4x5.jpg (JPEG), social_banner_16x9.jpg (JPEG), wordmark_vector.svg (SVG), licensed_gathering_backdrop.jpg (JPEG), and one launch_kit_firefly_board URL; none missing. |
| The e-commerce shot background is pure white #FFFFFF. | auto · **dealbreaker** · K1 | Sampling the background region of ecom_white_bg_bracelet.jpg returns RGB exactly (255,255,255) / #FFFFFF across the seamless area surrounding the bracelet. |
| The e-commerce shot is a square ~2400x2400 JPEG. | auto · mandatory · K1 | ecom_white_bg_bracelet.jpg is JPEG format with width == height, dimensions approximately 2400x2400 (within ~5% tolerance). |
| The homepage close-up hero is a 4:5 portrait at ~2048x2560. | auto · mandatory · K1 | homepage_hero_closeup_4x5.jpg is JPEG with width:height ratio == 4:5 (portrait), dimensions approximately 2048x2560 (within ~5% tolerance). |
| The social banner is a 16:9 landscape at ~2560x1440. | auto · mandatory · K1 | social_banner_16x9.jpg is JPEG with width:height ratio == 16:9 (landscape), dimensions approximately 2560x1440 (within ~5% tolerance). |
| The wordmark deliverable is a valid scalable SVG vector file (not a raster). | auto · **dealbreaker** · K1 | wordmark_vector.svg parses as valid SVG containing vector path/shape elements, with no embedded raster bitmap (e.g. no <image>/base64 data URI) as the trace content. |
| The licensed backdrop is delivered as a full-resolution Adobe Stock asset via a presigned download URL. | auto · mandatory · K6 | licensed_gathering_backdrop.jpg resolves from an Adobe Stock license-and-download presigned URL and is full-resolution (not a watermarked comp/preview). |
| The Firefly board assembles exactly the graded master plus the five produced/licensed deliverables. | auto · mandatory · K6 | The launch_kit_firefly_board link opens to a shareable board containing all six elements: the graded master hero_warm_master, ecom_white_bg_bracelet, homepage_hero_closeup_4x5, social_banner_16x9, wordmark_vector, and licensed_gathering_backdrop. |
| The vectorized SVG wordmark reads 'GATHER & CO.' and preserves the knotted-cord-loop icon from the supplied flat PNG. | expert · **dealbreaker** · K2 | The SVG legibly renders the text 'GATHER & CO.' in the high-contrast serif and includes the minimal line-art knotted cord loop icon to the left of the text, matching the supplied brand_wordmark_flat.png; the brand mark is traced, not regenerated or restyled. |
| The wordmark vector is single-color charcoal, matching the supplied flat PNG. | expert · mandatory · K2 | wordmark_vector.svg paths are a single deep-charcoal fill color with no gradients or introduced colors, faithful to the charcoal of brand_wordmark_flat.png. |
| The hero studio shot horizon is straightened (level) and not left crooked. | expert · mandatory · K3 | In the e-comm and graded outputs the seamless sweep / contact-shadow line reads level (the few-degrees tilt of the raw bracelet_studio_hero.jpg is corrected), with no awkward post-straighten crop artifacts. |
| Only the gold clasp saturation is boosted; the navy waxed-cord band color is unchanged. | expert · mandatory · K3 | In ecom_white_bg_bracelet.jpg the gold/yellow of the barrel clasp and charm reads as richer/more saturated 18k gold while the dark navy braided cord retains its original hue (single-color saturation, no global shift). |
| The bracelet subject is cleanly masked against the white background with no grey-seamless fringe or clipped product edges. | expert · mandatory · K3 | Around the bracelet in ecom_white_bg_bracelet.jpg the select-subject -> invert -> fill-white edge is clean: no residual grey halo, no white spill onto cord fibers or gold, and fine cord/clasp edges intact. |
| The 16:9 social banner leaves clean text-safe negative space for a headline. | expert · mandatory · K3 | The generative-expand outpaint in social_banner_16x9.jpg extends the white studio sweep with an uncluttered, seamless region of negative space suitable for overlaying a website-hero headline; expansion has no visible seams or artifacts. |
| The close-up hero applies a cohesive Lightroom preset look plus a gentle lens blur, and the overall kit reads elevated, warm, and timeless. | expert · quality · K4 | homepage_hero_closeup_4x5.jpg shows a cohesive graded preset look with a soft lens blur over the macro clasp detail, and the e-comm / hero / banner set shares a warm, elevated, timeless tone consistent with the brand. |
| All edited pixels originate from the client-supplied photos/assets; nothing is generated from scratch or composited beyond the single allowed outpaint. | expert · **dealbreaker** · K7 | ecom, hero, banner and SVG all derive from bracelet_studio_hero.jpg and brand_wordmark_flat.png; the only generative content is the 16:9 outpaint negative space; no from-scratch product design, no prompt-based background replacement, no compositing of the bracelet onto a new scene. |


[[PAGEBREAK]]
### AO-10 · Modern Silver Rosary Necklace — Commercial Product Package (Hero Retouch + Vector Spec + Screen-Print Tech Graphic + Data-Merge Spec Sheet)
**Brand:** Fashion & Apparel &nbsp;·&nbsp; **Operation:** O4 Preset retouch & look-dev (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (17 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Turn the client's raw studio shot of a modern silver rosary necklace into a full commercial product package: a retouched hero image on a clean sweep, a vector line-art spec, a screen-print-style halftone tech graphic, and a print-ready data-merged spec sheet — all assembled into a review board for revision rounds.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| rosary_studio_shot.jpg | image | Photorealistic amateur jewelry bench studio photograph of a MODERN sterling silver rosary necklace lying on a |
| brand_logo.png | image | Minimal modern wordmark logo for a silver religious-jewelry brand reading 'ARGENT & FAITH' in a clean thin geo |
| spec_sheet_template.indd | data | Author a single-page InDesign product spec-sheet template (.indd/.idml) for a jewelry line sheet with REAL InD |
| line_sheet_template.ai | vector | Author an Adobe Illustrator template (.ai) for a one-up wholesale line-sheet card with Illustrator VARIABLES b |
| sku_variants.csv | data | Generate a CSV of 6 rows for one modern silver rosary necklace family with columns: sku, product_name, materia |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| rosary_hero_4x5.jpg | image | Retouched commercial hero, 4:5 (e.g. 2400x3000px) JPEG sRGB: straightened, auto-toned, neutral white balance (silver-true), subject isolated on a clean neutral sweep, can |
| rosary_cutout.png | image | Transparent-background PNG cut-out of the rosary (background removed), full-res, for listings and the spec-sheet image placeholder. |
| rosary_lineart.svg | vector | Clean vectorized line-art / silhouette SVG of the necklace for stamping/embroidery and the logo-lockup spec. |
| rosary_halftone_tech.png | image | Single-tone screen-print / halftone tech graphic PNG of the rosary for tote/tee merch and the stamping vendor. |
| rosary_spec_sheet_merged.pdf | pdf | Multi-page print-ready PDF, one page per SKU variant, produced by data-merging the authored .indd template against sku_variants.csv (material/length/finish/price + hero i |
| rosary_line_sheet.png | image | Rendered wholesale line-sheet card(s) from the authored .ai after Illustrator-variable data-merge against the CSV. |
| rosary_review_board_link | data | Firefly Board deep-link assembling hero, cut-out, vector line-art, halftone graphic and spec-sheet preview for client revision rounds. |

**Layer-3 verifier checks** — expert-authored (16 checks, 1 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All 7 expected deliverables are present: rosary_hero_4x5.jpg, rosary_cutout.png, rosary_lineart.svg, rosary_halftone_tech.png, rosary_spec_sheet_merged.pdf, rosary_line_sheet.png, and rosary_review_board_link. | auto · mandatory · K1 | Exactly these 7 named outputs exist and are non-empty: a JPEG hero (rosary_hero_4x5.jpg), a PNG cut-out (rosary_cutout.png), an SVG line-art (rosary_lineart.svg), a PNG halftone (rosary_halftone_tech.png), a merged PDF spec sheet (rosary_spec_sheet_merged.pdf), a PNG line sheet (rosary_line_sheet.png), and a Firefly Board deep-link string (rosary_review_board_link). |
| The hero image rosary_hero_4x5.jpg is delivered as a JPEG in sRGB at a 4:5 portrait aspect ratio. | auto · mandatory · K1 | File is a valid JPEG in sRGB color space with width:height = 4:5 portrait (e.g. 2400x3000px); height/width == 1.25 within +/-1% tolerance. |
| The cut-out rosary_cutout.png is a PNG with a transparent (alpha) background and the rosary subject isolated. | auto · mandatory · K1 | File is a valid PNG containing an alpha channel with fully transparent pixels in the background region surrounding the necklace. |
| The line-art deliverable rosary_lineart.svg is a true scalable SVG vector file, not a rasterized image embedded in SVG. | auto · mandatory · K1 | File is well-formed SVG containing vector path/shape elements (e.g. <path>/<polygon>) that resolve to scalable line-art of the necklace, and does NOT consist solely of a single embedded raster <image> bitmap. |
| The halftone tech graphic rosary_halftone_tech.png is a single-tone screen-print / halftone-style PNG of the rosary. | auto · mandatory · K1 | File is a valid PNG exhibiting a single-tone halftone/screen-print dot pattern (one ink color), recognizable as the rosary silhouette. |
| The spec-sheet PDF rosary_spec_sheet_merged.pdf is a multi-page print-ready PDF with exactly one page per SKU variant from sku_variants.csv (6 rows). | auto · mandatory · K1 | File is a valid PDF with exactly 6 pages, each page populated from a distinct sku_variants.csv row. |
| The spec-sheet PDF was produced by binding the authored .indd merge fields so each page renders the actual per-variant CSV values rather than literal placeholder tokens. | auto · **dealbreaker** · K1 | Via OCR/text extraction, no page contains literal merge-field tokens (e.g. '<<sku>>', '<<material>>', '<<chain_length>>', '<<finish>>', '<<wholesale_price>>', '<<retail_price>>'); each page's text matches its corresponding sku_variants.csv row values for material, chain_length, finish, wholesale_price and retail_price. |
| The per-variant pages reflect the CSV's stated variation: chain lengths 45cm / 55cm / 65cm and finishes brushed silver / oxidized silver. | auto · mandatory · K1 | Across the 6 pages, the chain_length values collectively include 45cm, 55cm and 65cm, and the finish values include both 'brushed silver' and 'oxidized silver', matching sku_variants.csv exactly. |
| The line sheet rosary_line_sheet.png is a PNG rendered from the authored .ai after Illustrator-variable data-merge, showing the bound CSV values (sku, product_name, material, wholesale_price). | auto · mandatory · K1 | File is a valid PNG; via OCR, visible text matches sku_variants.csv values for the bound variables sku, product_name, material and wholesale_price, and contains no literal Illustrator variable-name placeholders. |
| The review board deep-link assembles the hero, cut-out, vector line-art, halftone graphic and the line-sheet preview into one Firefly Board. | expert · mandatory · K6 | rosary_review_board_link is a resolvable Firefly Board URL whose board contains all five assembled assets: the hero (rosary_hero_4x5.jpg), the cut-out (rosary_cutout.png), the line-art (rosary_lineart.svg), the halftone (rosary_halftone_tech.png) and a spec/line-sheet preview. |
| The hero retouch corrected the warm yellow desk-lamp cast so the brushed silver reads neutral/silver-true. | expert · mandatory · K4 | On the hero, the metal of the necklace reads as neutral brushed silver with no residual warm/yellow color cast; a neutral white-balance is evident versus the warm raw input. |
| The hero capture was straightened so the necklace sits level (the raw input was shot crooked/tilted). | expert · quality · K3 | The necklace reads as level/upright in the hero, with the crooked tilt of the raw bench shot corrected. |
| The hero subject is isolated onto a clean neutral light-grey studio sweep (messy bench gone) with a soft blurred-background depth look. | expert · mandatory · K3 | Background is a clean neutral light-grey studio sweep with no bench clutter, the necklace sits cleanly on it, and a soft shallow-depth/lens-blur background quality is present. |
| The subject-isolation mask/edge quality on the cut-out and hero is clean (no haloing, no clipped beads/links, no background fringe around the geometric links and crucifix). | expert · quality · K3 | Edges of the necklace, beads, geometric links and crucifix are cleanly masked with no halo, fringe, or amputated detail. |
| The whole package holds the modern, minimal, silver-true (charcoal/silver) aesthetic stated in the brief across hero, line-art, halftone and spec/line sheets. | expert · quality · K4 | All deliverables present a consistent modern, minimal, charcoal/silver visual treatment true to the brief, with no clashing styling. |
| The brand wordmark 'ARGENT & FAITH' appears in the spec-sheet / line-sheet brand-lockup area and is not regenerated, re-typeset, or restyled. | expert · mandatory · K2 | The string 'ARGENT & FAITH' is legibly present in the spec-sheet / line-sheet wordmark lockup area in the supplied minimal charcoal sans-serif treatment, not re-typeset or re-generated into a different logo styling. |


[[PAGEBREAK]]
### AO-11 · Sterling-Silver Ruby Pendant — Retouched Hero Shots, Color-Matched Set, Vectorized Calligraphy Mark, Moodboard & Spec-Sheet Export
**Brand:** Nonprofit, Religious &amp; Community &nbsp;·&nbsp; **Operation:** O4 Preset retouch & look-dev (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (22 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Turn the client's raw photos of a finished Sterling-Silver 925 ruby pendant into a retouched, color-consistent hero product-photo set with a clean white-background cut-out, an outpainted banner, a vectorized Arabic-calligraphy hallmark, a Firefly moodboard, and an exported lookbook/spec sheet.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| pendant_hero_front.jpg | image | Photoreal studio product photograph, front-on, of a closed ornate sterling silver 925 locket pendant shaped li |
| pendant_threequarter_open.jpg | image | Photoreal three-quarter-angle studio photograph of the SAME sterling silver 925 book/door pendant with its dou |
| pendant_calligraphy_macro.jpg | image | Extreme macro photoreal photograph of fine engraved Arabic calligraphy on a brushed sterling silver 925 surfac |
| pendant_lookbook_spec.indd | pdf | Author a single-page Adobe InDesign (.indd/.idml) jewelry lookbook + spec sheet layout for a luxury pendant: b |
| velvet_pad_backdrop_ref.jpg | image | Photoreal flat-lay of a dark burgundy velvet jeweller's display pad with soft directional studio light, subtle |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| hero_corrected.jpg | image | Straightened, auto-toned, exposure/highlight-lifted, warm-balanced front hero with a deep saturated ruby; full-res JPEG, sRGB. |
| open_doors_matched.jpg | image | Three-quarter open-doors shot color-matched to the hero via the saved preset, ruby deepened; full-res JPEG, sRGB. |
| packshot_white_square.png | image | Background-removed pendant on pure-white fill, cropped/resized to a 2000x2000 square marketplace packshot, PNG. |
| hero_banner_wide.jpg | image | Generative-expand (outpaint) widening of the corrected hero to a ~2400x1000 listing-header banner, JPEG, sRGB. |
| calligraphy_mark.svg | vector | Clean vector SVG of the engraved Arabic-calligraphy hallmark traced from the macro, usable as a scalable brand mark. |
| pendant_moodboard_board | data | Firefly Boards deep-link assembling the corrected hero, matched open-doors shot, packshot and banner for client review. |
| lookbook_spec.pdf | pdf | Print-ready PDF export of the authored InDesign spec/lookbook sheet. |
| lookbook_spec_web.jpg | image | Web-resolution JPEG export of the same spec/lookbook sheet for emailing the estimate/timeline. |

**Layer-3 verifier checks** — expert-authored (18 checks, 3 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All 8 named deliverables from outputs() are present: hero_corrected.jpg, open_doors_matched.jpg, packshot_white_square.png, hero_banner_wide.jpg, calligraphy_mark.svg, pendant_moodboard_board, lookbook_spec.pdf, lookbook_spec_web.jpg | auto · mandatory · K1 | Exactly these 8 outputs exist (4 .jpg images, 1 .png, 1 .svg, 1 .pdf, 1 Firefly Boards deep-link); one file/link per named deliverable, none missing and no extra invented deliverable |
| packshot_white_square.png is exactly 2000x2000 pixels | auto · mandatory · K1 | PNG dimensions read as width==2000 AND height==2000 (square marketplace tile) |
| packshot_white_square.png has a pure-white background behind the isolated pendant (background fully replaced, not the original charcoal-grey studio backdrop) | auto · mandatory · K1 | The region surrounding the pendant subject is pure white (RGB 255,255,255) across the full frame, with no remaining charcoal-grey backdrop and no transparency in the fill region |
| hero_banner_wide.jpg is a wide listing-header banner at approximately 2400x1000 | auto · mandatory · K1 | JPEG with width approximately 2400 and height approximately 1000 (wide landscape aspect ~2.4:1), wider than the source hero crop |
| File formats and colour-space match the outputs() spec: hero_corrected, open_doors_matched, hero_banner_wide and lookbook_spec_web are JPEG in sRGB; packshot_white_square is PNG; calligraphy_mark is SVG; lookbook_spec is PDF | auto · **dealbreaker** · K1 | hero_corrected.jpg / open_doors_matched.jpg / hero_banner_wide.jpg / lookbook_spec_web.jpg are valid JPEG with sRGB colour profile; packshot_white_square is valid .png; calligraphy_mark is valid .svg; lookbook_spec is valid .pdf |
| calligraphy_mark.svg is a true vector trace, not a raster bitmap embedded in an SVG wrapper | auto · mandatory · K1 | SVG contains <path>/vector geometry elements AND contains no embedded raster bitmap (no <image> element and no base64-encoded raster data) |
| lookbook_spec.pdf / lookbook_spec_web.jpg reproduce the exact spec-table values authored in pendant_lookbook_spec.indd | auto · mandatory · K2 | OCR of the exported PDF/JPEG contains the spec-table strings 'Sterling Silver 925', 'Ruby', 'Islamic geometric openwork' and 'Arabic calligraphy' as authored in the supplied .indd (content preserved from the export, not altered) |
| hero_corrected.jpg shows the deliberate ~3-degree input tilt corrected (straightened) and the under-exposed baseline lifted (auto-toned, exposure raised) so the polished silver reads bright | expert · mandatory · K1 | Pendant/chain appears level (the ~3deg input tilt is corrected) AND the silver is noticeably brighter/cleaner than the deliberately dark, under-exposed input |
| hero_corrected.jpg has a slightly warm white balance and a deep, saturated red ruby achieved via selective single-color saturation (ruby boosted without a global red cast on the silver) | expert · quality · K4 | Overall white balance reads slightly warm (luxury feel) AND the ruby reads deep/saturated red while the silver stays neutral (no global red cast) |
| open_doors_matched.jpg is color-matched to hero_corrected.jpg via an applied preset, neutralizing the input's greener/cooler uneven cast so the two shots read as a consistent set | expert · mandatory · K3 | open_doors_matched white balance and tone visibly match hero_corrected (the input's green/cool cast is removed); the pair looks shot/graded together |
| open_doors_matched.jpg has the ruby latch deepened the same way the hero ruby was deepened | expert · quality · K4 | The ruby latch on the open-doors shot reads deep/saturated red consistent with the hero's ruby treatment |
| packshot_white_square shows a clean subject cut-out: the pendant correctly isolated with crisp edges (chain and Islamic openwork preserved) against the white fill | expert · mandatory · K3 | Pendant and chain are fully retained with clean, accurate mask edges (no background halo, no chopped chain/filigree, no eaten-away openwork) |
| calligraphy_mark.svg reads as a clean, legible scalable brand mark with smooth traced edges (not noisy/jagged tracing artifacts from the macro) | expert · quality · K3 | Vectorized Arabic-calligraphy shapes are clean and recognizable, edges smooth, usable as a brand hallmark at scale, and correspond to the engraved strokes in pendant_calligraphy_macro.jpg |
| hero_banner_wide.jpg outpaint extends the hero plausibly left/right with seamless continuation of the charcoal-grey studio backdrop (no visible seam, repetition, or distortion of the pendant) | expert · quality · K4 | Generative-expanded regions blend seamlessly with the original; pendant unchanged/undistorted; no obvious seam or artifacting at the join |
| pendant_moodboard_board is a working Firefly Boards deep-link assembling exactly the four produced assets specified in the chain: hero_corrected, open_doors_matched, packshot_white_square and hero_banner_wide | auto · mandatory · K6 | Deep-link resolves to a Firefly board containing hero_corrected, open_doors_matched, packshot_white_square and hero_banner_wide (and no missing among the four) |
| lookbook_spec.pdf and lookbook_spec_web.jpg are exports of the client-authored pendant_lookbook_spec.indd (layout/copy preserved from the supplied .indd, not regenerated/recomposed) | expert · **dealbreaker** · K2 | Both exports reproduce the authored InDesign lookbook layout (wordmark area, hero+detail frames, spec table, cost/lead-time block) with content matching the supplied .indd; PDF is print-ready and JPEG is web-resolution |
| The pendant identity is preserved throughout: the same client-supplied Sterling Silver 925 book/door pendant with ruby latch, Islamic geometric openwork and Arabic calligraphy appears in every produced shot (no substitution/regeneration of the actual piece) | expert · **dealbreaker** · K2 | hero, open-doors, packshot, banner and moodboard all depict the same client-supplied physical pendant; no AI-fabricated or swapped jewelry |
| No out-of-scope 3D-CAD deliverable is fabricated or claimed: the impossible literal ask (Rhino/MatrixGold .3DM/STL model) is correctly re-anchored to the supported photo-presentation package | auto · mandatory · K7 | Delivered set contains no .3dm, .stl or other 3D/CAD model file, and no output claims to be a 3D CAD model; only the 8 specified photo/presentation deliverables are produced |


[[PAGEBREAK]]
### AO-12 · Bright-and-Airy Lightroom Grade for a 38-Shot Food Photography Set (Flat-Lay, 45°, Side)
**Brand:** Food, Restaurant & Beverage &nbsp;·&nbsp; **Operation:** O1 Tonal grade & restore (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (21 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Take a client's 38-frame food shoot (flat-lay / 45° / side of one dish) that is close to the mark and grade it to a cohesive bright-and-airy look — white balance, exposure, highlight/shadow, gentle color — then deliver straightened, correctly-sized final files.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| flatlay_raw.jpg | image | Overhead flat-lay food photograph of a single plated brunch dish — ricotta toast with figs, honey drizzle and |
| angle45_raw.jpg | image | 45-degree three-quarter food photograph of the SAME ricotta-fig honey toast on the same matte off-white plate, |
| side_raw.jpg | image | Side/profile eye-level food photograph of the SAME ricotta-fig honey toast, showing the layered height of the |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| flatlay_bright_airy.jpg | image | Straightened, cropped, fully bright-and-airy-graded flat-lay at client delivery resolution (3000px long edge, sRGB JPG). |
| food_pop_master.jpg | image | The flat-lay grade with a selective targeted lift on the dish (food prompt-selected, background protected) — the hero master, full resolution sRGB JPG. |
| angle45_bright_airy.jpg | image | 45-degree frame matched to the same bright-and-airy look (auto-tone + warm WB + highlight recovery + shadow lift), delivery resolution sRGB JPG. |
| side_bright_airy.jpg | image | Side frame matched to the same look, delivery resolution sRGB JPG. |
| ig_teaser_1080.jpg | image | Instagram teaser crop/resize of the food-pop master at 1080x1350 (4:5) sRGB JPG. |
| edit_recipe_note.txt | text | Short plain-text note documenting the cohesive bright-and-airy recipe (the ordered list of adjustments and their intent) so the client can see how the set was unified; co |

**Layer-3 verifier checks** — expert-authored (16 checks, 1 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All six deliverables are present: flatlay_bright_airy.jpg, food_pop_master.jpg, angle45_bright_airy.jpg, side_bright_airy.jpg, ig_teaser_1080.jpg, and edit_recipe_note.txt | auto · mandatory · K1 | Exactly these 6 files exist by name and type: 5 image deliverables (.jpg) named flatlay_bright_airy.jpg, food_pop_master.jpg, angle45_bright_airy.jpg, side_bright_airy.jpg, ig_teaser_1080.jpg, plus 1 plain-text note edit_recipe_note.txt; none missing |
| flatlay_bright_airy.jpg is delivered at 3000px on its long edge in sRGB JPG | auto · mandatory · K1 | flatlay_bright_airy.jpg long edge == 3000px, format == JPEG, color space == sRGB (per output spec: '3000px long edge, sRGB JPG') |
| food_pop_master.jpg is delivered at full resolution as an sRGB JPG | auto · mandatory · K1 | food_pop_master.jpg is JPEG, color space == sRGB, at full resolution (long edge >= 3000px, consistent with the flat-lay master it is built from) |
| angle45_bright_airy.jpg and side_bright_airy.jpg are delivered at delivery resolution sRGB JPG | auto · mandatory · K1 | Both angle45_bright_airy.jpg and side_bright_airy.jpg are JPEG, color space == sRGB, at delivery resolution (long edge 3000px, consistent with the flat-lay's stated delivery spec; raw frames are 4000x3000 landscape) |
| ig_teaser_1080.jpg is sized to 1080x1350 (4:5) sRGB JPG | auto · mandatory · K1 | ig_teaser_1080.jpg dimensions == 1080x1350 px (4:5 aspect), format == JPEG, color space == sRGB |
| ig_teaser_1080.jpg is derived from food_pop_master (the selective-food-pop master), not a raw or un-graded frame | expert · mandatory · K1 | The Instagram teaser visibly shows the same bright-and-airy grade AND the selective food-pop lift present in food_pop_master.jpg (same dish framing, same tonal look), confirming it is a crop/resize of the food-pop master |
| The flat-lay was straightened (overhead squared so plate edges are true) and cropped before grading | expert · mandatory · K3 | In flatlay_bright_airy.jpg the ~1-2 degree tilt of flatlay_raw.jpg is corrected — plate edges/table grain read true/square and the rotation margins are cropped out, vs the tilted raw |
| The flat-lay grade applies the bright-and-airy base recipe: warm/clean white balance, lifted exposure, recovered (bright-not-blown) highlights, and opened shadows | expert · mandatory · K4 | vs flatlay_raw.jpg, flatlay_bright_airy.jpg is warmer (the faintly-cool import neutralised toward clean daylight), brighter overall, with window light / honey / plate-rim highlights bright but not clipped/blown, and the under-plate shadows opened/airy (not muddy) |
| The flat-lay color is given a restrained vibrance/saturation bump — appetising but not garish | expert · quality · K4 | Color in flatlay_bright_airy.jpg is more vivid/appetising than the raw yet still natural — no oversaturated or garish cast |
| food_pop_master.jpg shows a selective targeted lift on the dish (ricotta-fig honey toast) while the airy background is protected | expert · mandatory · K3 | In food_pop_master.jpg the food (toast and figs) is brighter/popped relative to the flat-lay base grade, while the surrounding plate/table/background brightness is unchanged (background protected) — no global brighten |
| The selective food-pop edge is clean — the food mask does not bleed into or visibly halo the protected background | expert · quality · K3 | No visible brightness halo, fringe, or hard mask edge between the lifted food and the protected background in food_pop_master.jpg |
| angle45_bright_airy.jpg matches the same bright-and-airy look as the flat-lay (auto-tone seat + warm WB + highlight recovery + shadow lift) | expert · mandatory · K4 | The 45-degree frame reads as the same shoot as flatlay_bright_airy.jpg — comparable warm-clean white balance, brightness, highlight handling and open shadows; not a mismatched or differently-toned grade |
| side_bright_airy.jpg matches the same bright-and-airy look, with the bright background window recovered and shadows opened | expert · mandatory · K4 | The side/profile frame reads cohesively with the other two — warm-clean WB, lifted brightness, the bright background window bright-not-blown, and opened shadows; consistent with the set |
| All three graded frames read as one cohesive shoot (consistent white balance, exposure and color across flat-lay, 45-degree and side) | expert · mandatory · K4 | Viewed together, flatlay_bright_airy.jpg, angle45_bright_airy.jpg and side_bright_airy.jpg show a unified bright-and-airy grade with no frame standing out as cooler/warmer/darker/brighter than the others |
| All grades operate on the client's own pixels only — no generative fill, object removal, background replacement, or compositing | expert · **dealbreaker** · K7 | Each graded frame shows the identical dish/props/scene as its corresponding raw input (ricotta toast with figs, honey, microgreens on the matte off-white plate, pale oak table, linen napkin, espresso cup) with only tonal/color changes — no added, removed, replaced or composited content |
| edit_recipe_note.txt is a plain-text note documenting the ordered bright-and-airy recipe and its intent | auto · quality · K5 | edit_recipe_note.txt is plain text and lists the ordered adjustments (straighten/crop, warm white balance, exposure lift, highlight recovery, shadow open, vibrance, selective food pop, angle matching) describing how the set was unified into one cohesive look |


[[PAGEBREAK]]
### AO-13 · Taco Tuesday & Lunch-Special Meta Ad Photo-Asset Prep — Retouch, Grade, Cutout, Multi-Ratio Outpaint & Delivery Pack for a West Palm Beach Mexican Restaurant
**Brand:** Food, Restaurant & Beverage &nbsp;·&nbsp; **Operation:** O1 Tonal grade & restore (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (20 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Prep and deliver the campaign-ready photo + brand asset pack (retouched, warm/bold-graded hero food shots, color-splash and subject-pop scroll-stop variants, cut-out dishes, three Meta ad ratios via outpaint, a licensed backdrop texture, and a vectorized logo) for a West Palm Beach Mexican restaurant's Taco Tuesday & Lunch-Special Meta ad mockups.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| hero_taco_platter.jpg | image | Photoreal candid overhead-ish handheld phone photo, slightly tilted ~4 degrees, of a generous al pastor taco p |
| lunch_carne_asada_plate.jpg | image | Photoreal phone photo of a carne asada lunch plate on a plain off-white restaurant plate against a moderately |
| margarita_chips_table.jpg | image | Photoreal candid table scene at a warm neighborhood Mexican restaurant: a salt-rimmed margarita with lime, a b |
| restaurant_logo_flat.png | image | Flat 2D logo PNG on transparent background for a family-owned Mexican restaurant named 'El Vecino Cocina': bol |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| hero_warm_graded.jpg | image | Straightened + auto-toned + warm/bold-graded hero taco platter; full-res JPEG, sRGB, the appetizing campaign hero. |
| hero_color_splash.jpg | image | Scroll-stop variant: food in full color, background desaturated via inverted-mask saturation; full-res JPEG, sRGB. |
| hero_subject_pop.jpg | image | Adaptive Subject-Pop preset applied to the graded hero; high-contrast scroll-stop variant; full-res JPEG, sRGB. |
| lunch_plate_cutout.png | image | Carne asada lunch plate with background removed; transparent PNG, edges clean enough to float on any ad background. |
| hero_1x1_feed.jpg | image | Hero outpainted to square 1080x1080 (1:1) Meta feed canvas; food uncropped, scene extended; JPEG. |
| hero_4x5_feed.jpg | image | Hero outpainted to 1080x1350 (4:5) portrait feed canvas; food uncropped; JPEG. |
| hero_9x16_story.jpg | image | Hero outpainted to 1080x1920 (9:16) story/Reels canvas; food uncropped; JPEG. |
| backdrop_texture_fullres.jpg | image | One licensed Adobe Stock warm woven-textile/rustic-wood backdrop texture, full-res, with license; for layout team to place behind cut-outs. |
| logo_vector.svg | vector | Clean SVG vectorization of the supplied logo PNG; scales crisply across all ad sizes. |
| ElVecino_MetaAd_AssetPack/ | data | Named project folder containing the full delivery set, plus a Firefly review board deep-link assembling all produced assets as a client-approval deck. |

**Layer-3 verifier checks** — expert-authored (17 checks, 4 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All ten deliverables are present in the delivery set | auto · mandatory · K1 | The output set contains all of: hero_warm_graded.jpg, hero_color_splash.jpg, hero_subject_pop.jpg, lunch_plate_cutout.png, hero_1x1_feed.jpg, hero_4x5_feed.jpg, hero_9x16_story.jpg, backdrop_texture_fullres.jpg, logo_vector.svg, plus the ElVecino_MetaAd_AssetPack/ folder and a Firefly review board deep-link |
| The three Meta ad ratio canvases have the exact required pixel dimensions | auto · mandatory · K1 | hero_1x1_feed.jpg is exactly 1080x1080 (1:1), hero_4x5_feed.jpg is exactly 1080x1350 (4:5), and hero_9x16_story.jpg is exactly 1080x1920 (9:16) |
| The graded hero, both scroll-stop variants, the three ratio canvases, and the backdrop texture are delivered as JPEG | auto · **dealbreaker** · K1 | hero_warm_graded.jpg, hero_color_splash.jpg, hero_subject_pop.jpg, hero_1x1_feed.jpg, hero_4x5_feed.jpg, hero_9x16_story.jpg, and backdrop_texture_fullres.jpg are all valid JPEG files |
| The graded hero deliverables are in sRGB color space | auto · mandatory · K1 | hero_warm_graded.jpg, hero_color_splash.jpg, and hero_subject_pop.jpg are encoded in the sRGB color space, as specified in the deliverable spec for each |
| The lunch plate cut-out is a transparent PNG | auto · **dealbreaker** · K1 | lunch_plate_cutout.png is a valid PNG file containing an alpha channel with transparent (alpha=0) pixels in the background region |
| The vectorized logo is delivered as an SVG | auto · **dealbreaker** · K1 | logo_vector.svg is a valid, parseable SVG file containing vector path/shape elements (not a raster image embedded in an SVG wrapper) |
| The delivery folder is named exactly as specified and holds the nine produced asset files | auto · mandatory · K1 | A project folder named exactly 'ElVecino_MetaAd_AssetPack' exists and contains the nine produced asset files (hero_warm_graded.jpg, hero_color_splash.jpg, hero_subject_pop.jpg, lunch_plate_cutout.png, hero_1x1_feed.jpg, hero_4x5_feed.jpg, hero_9x16_story.jpg, backdrop_texture_fullres.jpg, logo_vector.svg) |
| The graded hero shows a warm color-temperature shift versus the supplied raw photo | auto · mandatory · K1 | hero_warm_graded.jpg has a measurably warmer average tone than the input hero_taco_platter.jpg (higher mean red-to-blue ratio / warmer white balance), consistent with the brief's 'lift color temperature toward warm' step |
| The hero taco platter was straightened from its ~4-degree handheld tilt | expert · mandatory · K3 | In hero_warm_graded.jpg the table edges read level (the ~4-degree tilt of the input hero_taco_platter.jpg is corrected), with no obvious residual rotation |
| The color-splash variant keeps the food in full color while the rest of the frame is desaturated | expert · mandatory · K3 | In hero_color_splash.jpg only the taco/food region retains saturated color and everything outside it (table, background) is visibly desaturated toward grayscale, with the splash boundary following the food edge |
| The subject-pop variant is a distinct higher-contrast treatment of the graded hero | expert · mandatory · K4 | hero_subject_pop.jpg is visibly different from hero_warm_graded.jpg, showing the higher-contrast / food-forward Adaptive 'Subject Pop' look (not an identical copy of the graded hero) |
| The lunch-plate cut-out has clean, layout-ready edges around the carne asada dish | expert · mandatory · K3 | In lunch_plate_cutout.png the carne asada plate is fully retained with the cluttered table background removed, and the cut edge is clean (no haloing, leftover background fringe, or chunks missing from the plate) |
| The three ratio canvases extend the scene by outpainting without cropping the food | expert · mandatory · K3 | In hero_1x1_feed.jpg, hero_4x5_feed.jpg, and hero_9x16_story.jpg the original taco platter food is fully present and uncropped, and the added canvas is a plausible continuation of the table/scene (no visible seam or distorted duplication at the expansion boundary) |
| The backdrop texture is a properly licensed full-res Adobe Stock asset matching the brief's direction | expert · mandatory · K2 | backdrop_texture_fullres.jpg is a full-resolution Adobe Stock asset delivered with a valid license (not a watermarked comp), depicting a warm woven Mexican textile or rustic-wood surface |
| The vectorized logo faithfully reproduces the supplied El Vecino Cocina logo | expert · **dealbreaker** · K2 | logo_vector.svg visually matches restaurant_logo_flat.png — same 'El Vecino Cocina' wordmark, sombrero-and-chili-pepper emblem, and terracotta-red/deep-green palette — with shapes traced cleanly and nothing redrawn, renamed, or invented |
| The vectorized logo color palette is preserved from the source PNG | auto · mandatory · K2 | logo_vector.svg uses the source logo's warm terracotta-red and deep-green colors (dominant fill colors match the input restaurant_logo_flat.png, not arbitrary substitute hues) |
| The Firefly review board assembles the produced delivery set as a client-approval deck | expert · mandatory · K6 | The Firefly board deep-link opens a board containing the produced campaign assets (graded hero, both scroll-stop variants, lunch-plate cut-out, three ratio canvases, backdrop texture, logo) presented as a labeled review deck for client approval |


[[PAGEBREAK]]
### AO-14 · Brickyard retro one-page menu: food-photo grade + logo vectorize + InDesign data-merge to print PDF/JPEG
**Brand:** Food, Restaurant & Beverage &nbsp;·&nbsp; **Operation:** O1 Tonal grade & restore (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (25 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Grade four raw burger photos, vectorize the Brickyard wordmark, source a chalkboard texture, and run the client's authored InDesign menu template through a data-merge to produce a print-ready PDF and high-res JPEG.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| menu_template.indd | data | AUTHORED DELIVERABLE (cannot be model-generated): a genuine Adobe InDesign document (.indd/.idml) for a one-pa |
| photo_classic_double_smash.jpg | image | Photoreal phone snapshot of a double Brickyard on a wax-paper-lined metal basket, sitting on a cluttered diner |
| photo_specialty_bacon_jalapeno.jpg | image | Photoreal phone snapshot of a tall specialty burger with bacon, jalapeños and a brioche bun on a slate board, |
| photo_sides_fries_basket.jpg | image | Photoreal phone snapshot of a basket of golden seasoned fries on a red diner tray, slightly tilted, flat grey |
| photo_bev_craft_cola.jpg | image | Photoreal phone snapshot of a craft cola in a frosted glass bottle with condensation, on a wooden counter, dim |
| brickyard_wordmark.png | image | A flat retro street-food wordmark logo reading 'Brickyard' in a bold condensed vintage diner typeface, chunky |
| menu_placeholder_prices.csv | data | Generate a CSV with columns section,item,desc,price holding placeholder menu rows: 3 Classic Burgers, 3 Specia |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| Brickyard_Menu_print.pdf | pdf | Print-ready one-page A4 portrait PDF exported from the data-merged InDesign document; placeholder copy bound from CSV, graded food photos + vectorized wordmark + chalkboa |
| Brickyard_Menu_highres.jpg | image | High-resolution JPEG of the same bound one-page menu (A4 portrait, max-quality) for digital/social sharing. |
| graded_food_photos_x4 | image | Four color-graded, straightened, consistently 4:5-cropped food photos (classic burger / specialty burger / fries / cola) matching the template frames; the classic hero al |
| brickyard_wordmark.svg | vector | Clean vector SVG of the Brickyard wordmark for crisp scaling at large print size. |
| Brickyard_Menu_review_board | data | Firefly board deep-link assembling the graded photos, vectorized wordmark, and final menu render for one-click owner sign-off. |

**Layer-3 verifier checks** — expert-authored (16 checks, 1 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| Print-ready PDF deliverable Brickyard_Menu_print.pdf is present and is a valid one-page PDF | auto · mandatory · K1 | A file named Brickyard_Menu_print.pdf exists, opens as a valid PDF, and contains exactly 1 page |
| The print PDF is A4 portrait at print quality | auto · mandatory · K1 | Brickyard_Menu_print.pdf page size equals A4 portrait (210x297 mm, height > width) and effective image resolution is approximately 300 DPI |
| High-resolution JPEG deliverable Brickyard_Menu_highres.jpg is present in JPEG format | auto · mandatory · K1 | A file named Brickyard_Menu_highres.jpg exists, decodes as a valid JPEG, is A4-portrait aspect (height > width, ~0.707 width:height within +/-3%), and is high-resolution (long edge >= 3000 px, consistent with A4 portrait near 300 DPI) |
| Exactly four food photos are delivered as graded outputs covering the four named subjects | auto · mandatory · K1 | Exactly four graded image files are present, one each for the classic double-smash burger, the specialty bacon-jalapeno burger, the fries basket, and the craft cola |
| All four graded food photos are cropped to the same 4:5 frame ratio the template expects | auto · mandatory · K1 | Each of the four graded photos has a width:height aspect ratio of 4:5 (0.8) within +/-2% |
| The classic hero double-smash shot is additionally delivered as a transparent-background PNG | auto · mandatory · K1 | A PNG of the classic double-smash burger exists with a real alpha channel and transparent (non-opaque) pixels around the subject |
| Background cutout of the hero burger is clean with no hard photographic edge | expert · quality · K3 | The transparent-background hero PNG isolates the burger with smooth, accurate mask edges (no halo, no clipped subject, no leftover background fringe) |
| The Brickyard wordmark is delivered as a vector SVG | auto · mandatory · K1 | A file named brickyard_wordmark.svg exists and is a valid SVG containing vector path geometry (not just an embedded raster image) |
| The vectorized wordmark reads 'Brickyard' and stays crisp at large print size | expert · **dealbreaker** · K2 | The SVG legibly spells 'Brickyard' matching the supplied brickyard_wordmark.png, with clean vector edges that remain sharp when scaled up to large print size |
| Placeholder menu copy is bound from the CSV into the four required sections via the InDesign merge fields | auto · mandatory · K1 | The rendered menu shows section headers Classic Burgers, Specialty Burgers, Sides, and Beverages with item/desc/price rows matching menu_placeholder_prices.csv (3 Classic Burgers, 3 Specialty Burgers, 4 Sides, 4 Beverages) |
| Every section name and price remains placeholder content as supplied, none invented or altered | auto · mandatory · K7 | All item names, descriptions, and US-dollar prices appearing in the menu are exactly the placeholder values from menu_placeholder_prices.csv, with no added, removed, or changed prices |
| The chalkboard texture backing the menu was licensed from Adobe Stock before use | auto · mandatory · K6 | An Adobe Stock chalkboard/blackboard texture was licensed and downloaded with the license step preceding placement, and that texture is used as the menu background |
| The final menu places the four graded photos, the vector wordmark, and the chalkboard texture in the authored template frames | expert · mandatory · K1 | The rendered menu shows all four graded food photos in their 4:5 frames, the Brickyard wordmark in its placeholder area, and the chalkboard texture as the full-bleed background |
| The four food photos are graded to a consistent vibrant, appetizing street-food look | expert · quality · K4 | All four photos are straightened, well-toned, warmed in white balance, and vibrance-pushed so the food reads as hero and appetizing, with a consistent look across the set |
| Cluttered backgrounds behind the hero and specialty burgers are thrown out of focus | expert · quality · K3 | The classic double-smash and specialty bacon-jalapeno burger photos show a defocused/blurred background so the food stands out as hero |
| A Firefly review board deep-link assembles the prepped assets and final menu for owner sign-off | auto · mandatory · K6 | A Firefly board deep-link (Brickyard_Menu_review_board) exists and contains the graded food photos, the vector wordmark (brickyard_wordmark.svg), and the final menu render (Brickyard_Menu_highres.jpg) |


[[PAGEBREAK]]
### AO-15 · Umaya Tri-Fold Menu Refresh — Food Photography Prep, Brand-Cohesive Color Grade, Logo Vectorization & Source Export
**Brand:** Food, Restaurant & Beverage &nbsp;·&nbsp; **Operation:** O1 Tonal grade & restore (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (21 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Prep, color-grade, cut out, crop, and print-export the new dish photography, the vectorized logo, the textured background, and the existing Illustrator menu source for Umaya's tri-fold menu refresh, all matched to the dark/red Japanese brand look and ready for the designer to place.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| tonkotsu_ramen_bowl_raw.jpg | image | Photoreal overhead-three-quarter food photograph of a single steaming tonkotsu ramen bowl on a dark slate tabl |
| wagyu_donburi_hero_raw.jpg | image | Photoreal hero food photograph of a Wagyu beef donburi rice bowl, seared A5 Wagyu slices with visible marbling |
| house_of_umami_logo_flat.png | image | Flat 2D restaurant logo on transparent background for 'Umaya', a stylized red brushstroke ramen bowl with risi |
| house_of_umami_menu_existing.ai | vector | Represents the client's EXISTING authored Adobe Illustrator tri-fold menu source (22.5x12 inch unfolded, 6 pan |
| dark_slate_texture_stock.jpg | image | Photoreal seamless dark slate stone surface texture, charcoal grey-black, subtle natural mineral veining and m |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| ramen_brand_graded.png | image | Tonkotsu ramen bowl, brand-matched look: warmed WB, deepened darks, lifted broth/garnish highlights, vibrance pushed so red chili oil reads. Full-res PNG. |
| wagyu_brand_graded.png | image | Wagyu donburi hero, auto-straightened + auto-toned + same brand grade as the ramen, with red/warm marbling tones selectively boosted. Full-res PNG. |
| ramen_cutout_transparent.png | image | Ramen bowl isolated, background removed to full transparency (alpha PNG) for tight placement in the crowded ramen section. |
| ramen_cell_300dpi.png | image | Ramen shot cropped to the tall menu-cell aspect ratio, sized for 300 DPI print placement. |
| wagyu_banner_300dpi.png | image | Wagyu hero cropped to the wide banner aspect ratio for the new Wagyu section, sized for 300 DPI print placement. |
| house_of_umami_logo.svg | vector | Vectorized logo as clean SVG, red (#C8302A) + near-black, crisp for print red-accent use. |
| dark_background_plate.png | image | Licensed dark slate texture darkened in its light portions + fine grain added = premium dark menu background plate. Full-res PNG. |
| menu_source_proof.png | image | Print-ready PNG render(s) of the client's existing authored Illustrator menu source, exported as a current proof to drop new assets into. |
| umami_menu_assets_board | data | Firefly board deep-link assembling all placement-ready delivered assets for client review, plus a packaged asset folder/zip. |

**Layer-3 verifier checks** — expert-authored (15 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All 9 expected deliverables are present in the delivered set | auto · mandatory · K1 | The delivered set contains all 9 outputs named in the spec: ramen_brand_graded.png, wagyu_brand_graded.png, ramen_cutout_transparent.png, ramen_cell_300dpi.png, wagyu_banner_300dpi.png, house_of_umami_logo.svg, dark_background_plate.png, menu_source_proof.png, and the umami_menu_assets_board Firefly board deep-link |
| The ramen cut-out is a transparent alpha PNG with the background removed | auto · mandatory · K1 | ramen_cutout_transparent.png is a PNG with an alpha channel where the area outside the ramen-bowl subject is fully transparent (alpha == 0), produced via image_remove_background on the graded ramen shot |
| The vectorized logo is delivered as a true SVG vector file | auto · mandatory · K1 | house_of_umami_logo.svg is valid XML with an <svg> root containing path/vector geometry (not an embedded raster <image>), derived from house_of_umami_logo_flat.png via image_vectorize |
| The vectorized logo preserves the brand red and near-black color scheme | auto · **dealbreaker** · K2 | house_of_umami_logo.svg uses the red accent #C8302A plus near-black as its only accent colors (single red accent #C8302A + near-black per the brand kit; no other accent hues introduced) |
| The two print-crop shots are exported at the correct orientation and 300 DPI sizing | auto · mandatory · K1 | ramen_cell_300dpi.png is cropped to a tall (portrait, height > width) menu-cell aspect ratio and wagyu_banner_300dpi.png to a wide (landscape, width > height) banner aspect ratio, each carrying DPI metadata / pixel dimensions consistent with 300 DPI print sizing |
| The Wagyu hero was auto-straightened before the tonal work | expert · mandatory · K1 | The horizon/surface of wagyu_brand_graded.png reads level: the ~3-4 degree off-level tilt of wagyu_donburi_hero_raw.jpg is corrected (to within roughly +/-1 degree) as the first step before grading |
| The menu-source proof is an export of the supplied authored Illustrator source, not a connector-composed layout | auto · **dealbreaker** · K7 | menu_source_proof.png is a print-ready PNG produced from house_of_umami_menu_existing.ai via document_render_vector — its dark-background / red-accent panels and section labels (Small Plates / Sushi Bowls / Artisan Ramen / Donburi Rice Bowls / Sushi Rolls / Nigiri-Sashimi / Kids / Desserts) match the authored .ai, and no tri-fold layout was composed by the connector |
| The dark background plate is the licensed stock texture darkened with grain added, not a flat fill | auto · mandatory · K1 | dark_background_plate.png is derived from the licensed dark_slate_texture_stock.jpg with its light portions darkened (image_adjust_light_portions) and fine grain added (image_add_grain), showing non-uniform per-pixel variance rather than a single solid color |
| Both dish photos share one cohesive brand grade | expert · mandatory · K4 | ramen_brand_graded.png and wagyu_brand_graded.png read as a matched set — consistent warmed white balance, deepened darks, lifted highlights, and pushed vibrance so they look edited together |
| The graded photos match the dark-background / red-accent Japanese brand look | expert · mandatory · K4 | Both graded dish photos show a warm amber-leaning white balance, deep dark background, and red chili-oil / red accents reading strong against the dark plate, matching the existing menu's dark / red-accent Japanese ramen-sushi aesthetic |
| The Wagyu marbling has a selective warm/red tone boost | expert · quality · K4 | wagyu_brand_graded.png shows the seared Wagyu marbling / red meat tones selectively enriched (warmer / redder than the surrounding shot) so the marbling reads rich, applied via a prompt-selected mask rather than to the whole frame |
| The ramen cut-out has clean subject-edge quality | expert · quality · K3 | The isolated ramen bowl in ramen_cutout_transparent.png has clean, accurate edges (no haloing, no leftover background fringe, no clipped bowl/garnish) suitable for tight placement next to type in the crowded ramen section |
| The food still looks appetising and realistic after the grade | expert · quality · K4 | Broth surface, onsen egg, garnish and Wagyu slices remain photoreal and appetising (highlights lifted without blowing out, darks deep without crushing detail), not over-processed |
| All delivered assets are assembled into a reviewable Firefly board deep-link | auto · mandatory · K6 | umami_menu_assets_board is a working Firefly board deep-link assembling the placement-ready assets for client review: ramen_cell_300dpi, wagyu_banner_300dpi, ramen_cutout_transparent, house_of_umami_logo.svg, dark_background_plate, menu_source_proof, wagyu_brand_graded, and the graded ramen (photos_brand_graded) |
| The final deliverables are packaged into a single delivery folder for hand-off | auto · quality · K6 | A single delivery folder/zip (via asset_copy_assets) collects the final files: ramen_cell_300dpi, wagyu_banner_300dpi, ramen_cutout_transparent, house_of_umami_logo.svg, dark_background_plate, menu_source_proof, and wagyu_brand_graded |


[[PAGEBREAK]]
### AO-16 · Restaurant Menu: Categorized Food Videos + Color-Graded Menu Still Package
**Brand:** Food, Restaurant & Beverage &nbsp;·&nbsp; **Operation:** O1 Tonal grade & restore (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (21 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*From the restaurant's raw food clips and flat-lay dish photos, produce a categorized (appetizers / mains / desserts) menu-media package: color-graded, canvas-expanded hero stills, three category-cover cards, a vector dish icon, a Firefly moodboard, plus vertical-reframed short clips and a sizzle reel for the in-store menu screens.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| hero_dish_flatlay_raw.jpg | image | Photoreal overhead flat-lay of a single plated signature main course on a matte ceramic plate sitting on a dar |
| appetizer_frame_raw.jpg | image | Photoreal close three-quarter shot of a sharing-style appetizer (crispy small plate with dip) on a slate board |
| dessert_frame_raw.jpg | image | Photoreal overhead of a plated dessert (panna cotta with berry coulis and a mint sprig) on a pale ceramic plat |
| dish_clip_landscape_16x9.mp4 | video | 1080p 16:9 locked-off overhead beauty shot of the same plated main course, slow 6-second push-in with rising s |
| appetizer_clip.mp4 | video | 1080p 5-second close clip of the appetizer being dipped and lifted, steam and crunch, warm restaurant light, n |
| dessert_clip.mp4 | video | 1080p 5-second clip of berry coulis being spooned over the panna cotta, glossy flow, cool clean light, native |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| hero_main_4x5.png | image | Color-graded, auto-straightened, AI canvas-expanded hero of the signature main course, 4:5 portrait (2048x2560), warm appetizing grade, ready as the top menu card / thumb |
| cover_mains_warm.png | image | Main-courses category cover derived from the hero, deepened warm tone, 4:5 (2048x2560). |
| cover_appetizers.png | image | Appetizers category cover: straightened, exposure/WB-corrected, same-grade appetizer frame, 4:5 (2048x2560). |
| cover_desserts_cool.png | image | Desserts category cover: same shared grade shifted cool-clean for desserts, 4:5 (2048x2560). |
| dish_icon.svg | vector | Clean vector icon of the isolated signature plate, flat SVG for menu UI / favicons / category chips. |
| menu_pitch_board | url | Firefly board deep-link assembling the hero + three category covers as the client-facing menu look pitch. |
| dish_clip_vertical_4x5.mp4 | video | The main-course clip reframed to vertical for portrait menu screens, SAME length as source (async product render). |
| menu_sizzle_reel.mp4 | video | Categorized sizzle reel assembled from the appetizer / main / dessert clips for the menu screen loop (async product render). |

**Layer-3 verifier checks** — expert-authored (16 checks, 1 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| hero_main_4x5.png is delivered as a PNG image | auto · mandatory · K1 | A file named hero_main_4x5.png exists and is a valid PNG (kind=image) |
| hero_main_4x5.png is exactly 4:5 portrait at 2048x2560 pixels | auto · mandatory · K1 | hero_main_4x5.png dimensions read exactly 2048 wide x 2560 tall (4:5 portrait) |
| All three category covers (cover_mains_warm.png, cover_appetizers.png, cover_desserts_cool.png) are delivered as PNGs at 4:5 portrait 2048x2560 | auto · mandatory · K1 | cover_mains_warm.png, cover_appetizers.png and cover_desserts_cool.png all exist as PNGs and each measures exactly 2048x2560 |
| dish_icon.svg is delivered as a valid vector SVG file | auto · mandatory · K1 | A file named dish_icon.svg exists and parses as valid SVG vector markup (paths/shapes), not a raster image embedded in an SVG wrapper |
| menu_pitch_board is delivered as a Firefly board deep-link URL | auto · mandatory · K1 | menu_pitch_board is a URL (kind=url) that resolves to a Firefly board |
| dish_clip_vertical_4x5.mp4 is delivered as a vertical 4:5 MP4 the same length as the source 16:9 clip (reframe only, no trim) | auto · mandatory · K1 | dish_clip_vertical_4x5.mp4 exists as a valid MP4 with a vertical 4:5 frame and its duration equals the duration of the source dish_clip_landscape_16x9.mp4 |
| menu_sizzle_reel.mp4 is delivered as a multi-clip MP4 assembled from the appetizer, main and dessert clips | auto · mandatory · K1 | menu_sizzle_reel.mp4 exists as a valid MP4 whose duration and cut structure reflect assembly of the appetizer, main and dessert dish clips into a single reel |
| The Firefly pitch board assembles exactly the hero plus the three category covers as the client menu-look pitch | expert · mandatory · K1 | The board contains hero_main_4x5, cover_mains_warm, cover_appetizers and cover_desserts_cool (exactly the four produced still assets) presented as the client-facing menu-look pitch |
| The 4:5 hero was produced by AI canvas-expand (outpaint) of the 16:9 source, not by cropping | expert · mandatory · K3 | Compared to the 16:9 source, hero_main_4x5 shows outpainted canvas above/below the original plated food (food breathes on the card) with seamless extension, consistent with image_generative_expand rather than a tight crop |
| The hero shows the tilt corrected and white-balance/exposure repaired from the mixed-light camera-original | expert · mandatory · K3 | Compared to hero_dish_flatlay_raw.jpg, hero_main_4x5 is level (no residual tilt), evenly exposed, and the mixed tungsten/window color cast is neutralized so the food color reads true |
| The hero and all three covers share one warm food family grade yet read as distinct categories | expert · mandatory · K4 | cover_mains_warm reads as a deepened-warm variant of the hero, cover_appetizers carries the same warm preset, and cover_desserts_cool is visibly cool-clean shifted, while all four still read as one consistent family grade |
| cover_appetizers is the appetizer frame straightened and exposure/white-balance-corrected under the same warm preset as the hero | expert · mandatory · K4 | cover_appetizers derives from appetizer_frame_raw.jpg with its tilt leveled and exposure/WB corrected, and carries the same warm appetizing preset as the hero so it reads as part of the shared grade |
| cover_desserts_cool reads cool-clean relative to the warm mains/appetizers covers | expert · quality · K4 | cover_desserts_cool has a visibly cooler/cleaner color temperature than cover_mains_warm and cover_appetizers, sourced from the dessert frame |
| Dish vibrance is lifted on the hero so sauce/garnish pop without oversaturation | expert · quality · K4 | hero_main_4x5 shows enhanced but natural vibrance/saturation (sauce and garnish read vivid yet realistic, not blown out or oversaturated) |
| The dish_icon depicts the isolated signature plate from the finished hero | expert · mandatory · K2 | dish_icon.svg is a clean flat representation of the same signature plate isolated from hero_main_4x5 (the plate subject, not the background or a different dish) |
| Every deliverable derives from the corrected hero or the supplied source frames/clips, with no from-scratch art, no compositing, and no generative fill beyond the single canvas-expand | expert · **dealbreaker** · K7 | Covers, icon, board and clips all trace to the corrected hero or the client-supplied frames/clips; the only generative step present is the lone hero outpaint; no invented imagery, composites, or extra generative fill appears |


[[PAGEBREAK]]
### AO-17 · Dark-Mode Restaurant Website Hero Food Photography Pack
**Brand:** Food, Restaurant & Beverage &nbsp;·&nbsp; **Operation:** O1 Tonal grade & restore (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (22 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Retouch a restaurant's raw plated-dish photos into a cohesive dark-mode hero-image pack (hero + menu tiles + mobile crop) and assemble a Firefly moodboard for the agency's web designer.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| raw_hero_scallops.jpg | image | Photoreal restaurant food photograph, raw and unretouched look, three pan-seared scallops with golden crust on |
| raw_dessert_flatlay.jpg | image | Photoreal overhead flat-lay food photograph, raw unedited look, a molten chocolate fondant dessert dusted with |
| raw_cocktail_closeup.jpg | image | Photoreal close-up food photograph, raw unedited look, an amber whiskey sour cocktail in a coupe glass with a |
| restaurant_wordmark_logo.png | image | A minimalist flat restaurant wordmark logo, the words rendered in an elegant thin serif typeface, solid near-b |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| hero_dark_desktop.png | image | Full-bleed desktop website hero, ~2880x1620 (16:9), straightened, dark-mode graded, subject popped off a moody dark surround, canvas extended on the left for headline neg |
| menu_tile_dessert.png | image | Square 1:1 menu-tile image (~1200x1200), graded to MATCH the hero's dark moody look, sRGB PNG. |
| menu_tile_cocktail.png | image | Square 1:1 menu-tile image (~1200x1200), graded to MATCH the hero's dark moody look, sRGB PNG. |
| hero_mobile_9x16.png | image | Full-bleed mobile Home crop, 1080x1920 (9:16), subject-aware crop of the graded hero, sRGB PNG. |
| logo_wordmark.svg | vector | Transparent, cleanly vectorized wordmark logo as crisp SVG for retina/responsive use on the dark site (plus the transparent-PNG intermediate). |
| moodboard_deeplink | data | Firefly Boards deep-link URL assembling the final hero, both menu tiles, and the logo as one dark-mode visual-direction reference for the Wix designer. |

**Layer-3 verifier checks** — expert-authored (15 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All six required deliverables are present: hero_dark_desktop.png, menu_tile_dessert.png, menu_tile_cocktail.png, hero_mobile_9x16.png, logo_wordmark.svg, and a moodboard_deeplink URL. | auto · mandatory · K1 | Exactly these 6 named outputs exist (4 PNG images, 1 SVG vector, 1 Firefly Boards deep-link URL); any missing item fails. |
| The desktop hero (hero_dark_desktop.png) is a 16:9 full-bleed image at approximately 2880x1620. | auto · mandatory · K1 | Width:height ratio == 16:9 and dimensions are ~2880x1620 (within rounding); file is PNG. |
| Both menu tiles (menu_tile_dessert.png, menu_tile_cocktail.png) are square 1:1 images at approximately 1200x1200. | auto · mandatory · K1 | Each tile has width == height (1:1) at ~1200x1200 px; both are PNG. |
| The mobile crop (hero_mobile_9x16.png) is a full-bleed 9:16 image at 1080x1920. | auto · mandatory · K1 | Dimensions == 1080x1920 (9:16 portrait); file is PNG. |
| All four exported raster deliverables are sRGB PNG files. | auto · **dealbreaker** · K1 | hero_dark_desktop.png, menu_tile_dessert.png, menu_tile_cocktail.png, and hero_mobile_9x16.png are all PNG format in sRGB color space. |
| The logo deliverable is a valid vector SVG with a transparent background, accompanied by a transparent-PNG intermediate. | auto · mandatory · K1 | logo_wordmark.svg parses as SVG containing vector path data (not an embedded raster), has no opaque background fill, and a transparent-PNG intermediate of the wordmark also exists. |
| The vectorized logo preserves the original wordmark's letterforms, the thin serif typeface, the inter-word leaf glyph, and the single near-black charcoal ink color without regenerating, restyling, or recoloring the mark. | expert · **dealbreaker** · K2 | logo_wordmark.svg visually matches restaurant_wordmark_logo.png: same two words/letterforms, elegant thin serif, small leaf glyph between the two words, solid near-black charcoal color; no redrawn, restyled, or recolored logo. |
| The logo background was removed by dropping the flat white field to transparency (not by masking or erasing the wordmark itself), with no halo or fringe. | expert · quality · K2 | The transparent-PNG intermediate shows the charcoal wordmark and leaf glyph fully intact on full transparency, with the white background cleanly removed and no white halo, fringe, or matte ring around the letters or glyph. |
| The desktop hero horizon is level — the ~4-degree raw tilt has been corrected. | expert · mandatory · K3 | The plate/table horizon in hero_dark_desktop.png reads level with no residual tilt; the original ~4deg slant is removed. |
| The desktop hero canvas is extended on the LEFT with clean dark negative space for an overlaid headline. | expert · mandatory · K3 | The left side of hero_dark_desktop.png shows added, clean, dark empty space (outpainted), leaving room for a headline; the scallop plate subject sits to the right of that negative space. |
| The hero is rendered in a moody dark-mode look with the scallop plate subject popped off a dark surround. | expert · mandatory · K4 | Background/surround in hero_dark_desktop.png is dark and moody; the scallop plate subject is visibly brighter/more saturated and stands out from the dark background (selective subject pop), not muddy or flat. |
| The mobile 9:16 crop keeps the scallop plate subject framed (subject-aware) rather than clipping it, and is taken from the graded hero. | expert · mandatory · K3 | The 1080x1920 hero_mobile_9x16.png is derived from the graded desktop hero with the scallop plate subject substantially in-frame and not awkwardly clipped. |
| Both menu tiles are grade-matched to the hero's dark, moody look so the food set reads as one cohesive system. | expert · mandatory · K4 | menu_tile_dessert.png and menu_tile_cocktail.png share the hero's dark moody base, contrast, and warm-cool color balance; the originally cooler/brighter dessert and neutral-cool cocktail no longer look mismatched against the hero. |
| Across all three food/drink images, the food tones remain appetizing and are not crushed into muddy darkness. | expert · quality · K4 | Scallops, chocolate dessert, and cocktail retain natural, appetizing color and visible detail in the shadows; the dark-mode grade has not flattened them into muddy/blocked tones. |
| The Firefly Boards moodboard deep-link assembles the final hero, both menu tiles, and the logo as the dark-mode visual-direction reference. | expert · mandatory · K6 | The moodboard_deeplink opens a Firefly board containing the finished hero_dark_desktop, menu_tile_dessert, menu_tile_cocktail, and the logo (4 final assets) presented together as one cohesive dark-mode reference. |


[[PAGEBREAK]]
### AO-18 · Premium Dark-Mode Restaurant Food-Photography Asset Suite (Hero, Menu Tiles, Logo Vector)
**Brand:** Food, Restaurant & Beverage &nbsp;·&nbsp; **Operation:** O1 Tonal grade & restore (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (26 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*From the client's raw food photos and logo, produce a dark-mode-ready food-photography asset suite — a color-graded wide hero banner, clean-backdrop menu tiles, a mobile crop, and a vector logo — for a premium restaurant website.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| hero_octopus_raw.jpg | image | Photoreal overhead-angle restaurant food photograph of a signature grilled Galician octopus dish: charred octo |
| steak_plate_raw.jpg | image | Photoreal restaurant food photograph of a dry-aged ribeye steak, sliced, resting on a dark slate board with ch |
| restaurant_logo_flat.png | image | Minimalist restaurant logo mark on transparent background: a clean single-line monoline octopus silhouette enc |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| hero_banner_ultrawide.png | image | 21:9 ultra-wide dark-mode hero banner, straightened + warm-moody graded + canvas-extended (outpainted) bleed, ~3440x1440 PNG, ready for headline overlay by the dev |
| hero_mobile_vertical.jpg | image | Mobile hero crop of the same graded hero, 4:5 portrait ~1080x1350 JPEG, subject-safe framing |
| menu_tile_octopus.jpg | image | Square menu tile, plated octopus isolated on uniform near-black (#0B0B0D) backdrop, grade-matched, ~1200x1200 JPEG |
| menu_tile_steak.jpg | image | Square menu tile, plated steak isolated on the SAME near-black (#0B0B0D) backdrop, color-matched to hero grade, ~1200x1200 JPEG |
| logo_mark.svg | vector | Clean 2-color vector logo mark (monoline octopus + wordmark), scalable SVG for retina/responsive use |
| restaurant_photo_suite.zip | data | Single zip bundling all five deliverables in a /hero, /menu, /logo folder structure for handoff |

**Layer-3 verifier checks** — expert-authored (17 checks, 3 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| hero_banner_ultrawide.png is delivered as a valid PNG file | auto · **dealbreaker** · K1 | A file named hero_banner_ultrawide.png exists and has a valid PNG file signature (89 50 4E 47) |
| hero_banner_ultrawide.png matches the 21:9 ultra-wide dimensions | auto · mandatory · K1 | Pixel dimensions are ~3440x1440 (21:9 aspect ratio, within +/-2% tolerance on each dimension) |
| hero_mobile_vertical.jpg is delivered as a JPEG at 4:5 portrait dimensions | auto · mandatory · K1 | A file named hero_mobile_vertical.jpg exists, is a valid JPEG, and is ~1080x1350 (4:5 portrait, within +/-2% tolerance on each dimension) |
| menu_tile_octopus.jpg is delivered as a square JPEG at the specified size | auto · mandatory · K1 | A file named menu_tile_octopus.jpg exists, is a valid JPEG, and is ~1200x1200 (1:1 square, within +/-2% tolerance on each dimension) |
| menu_tile_steak.jpg is delivered as a square JPEG at the specified size | auto · mandatory · K1 | A file named menu_tile_steak.jpg exists, is a valid JPEG, and is ~1200x1200 (1:1 square, within +/-2% tolerance on each dimension) |
| Both menu tiles place the dish on the SAME uniform near-black backdrop color #0B0B0D | auto · mandatory · K1 | The background region of both menu_tile_octopus.jpg and menu_tile_steak.jpg samples to a uniform solid near-black of #0B0B0D (within small JPEG tolerance) and the two backdrop colors are identical between the tiles |
| logo_mark.svg is delivered as a true scalable vector SVG, not a raster embedded in an SVG wrapper | auto · **dealbreaker** · K1 | A file named logo_mark.svg exists, parses as valid SVG, and contains vector path/shape elements (path/polygon/circle/etc.) rather than a single embedded base64 raster <image> |
| The full deliverable set is complete with all five named assets present | auto · mandatory · K1 | All five named outputs are present: hero_banner_ultrawide.png, hero_mobile_vertical.jpg, menu_tile_octopus.jpg, menu_tile_steak.jpg, logo_mark.svg |
| restaurant_photo_suite.zip bundles all five deliverables in a /hero, /menu, /logo folder structure | auto · mandatory · K1 | A zip named restaurant_photo_suite.zip exists containing exactly the five deliverables organized as /hero (hero_banner_ultrawide.png + hero_mobile_vertical.jpg), /menu (menu_tile_octopus.jpg + menu_tile_steak.jpg), and /logo (logo_mark.svg) |
| The hero banner canvas was extended/outpainted beyond the original 3:2 frame to reach the 21:9 ultra-wide ratio | expert · mandatory · K3 | The 21:9 banner shows believable generative-expand bleed room on the sides — the octopus subject is framed within the original content and the extended area is seamless and plausible, not stretched, mirrored, or letterboxed |
| The hero horizon was straightened from the ~4-degree handheld tilt in hero_octopus_raw.jpg | expert · mandatory · K3 | The plate/table horizon in the hero banner reads level, with no residual ~4-degree tilt from the raw handheld shoot |
| The dish in each menu tile is cleanly isolated from its original background | expert · mandatory · K3 | The plated octopus and steak are masked with clean edges against the #0B0B0D fill, with no original wood/marble/slate background remnants and no ragged or haloed edges |
| The mobile hero crop carries the same grade as the ultra-wide banner and uses subject-safe framing | expert · mandatory · K3 | hero_mobile_vertical.jpg shows the same warm-moody grade as hero_banner_ultrawide.png and the octopus subject is fully framed (not cropped through the dish) |
| The hero carries the warm-but-moody dark-mode house grade (warm highlights, deep controlled shadows, rich-but-not-cartoonish saturation) | expert · mandatory · K4 | Hero shows warm highlights, deep controlled shadows, and rich-but-not-cartoonish saturation, reading premium on a near-black background |
| The two menu tiles and the hero are color-matched so the menu grid reads as one cohesive shoot | expert · mandatory · K4 | Octopus and steak tiles share the same warm house grade as the hero (the steak's original tungsten cast corrected), with consistent warmth, shadow depth, and saturation across both tiles and the hero |
| logo_mark.svg reproduces the supplied 2-color monoline CASA POLVO logo faithfully (octopus-in-ring mark + serif wordmark) | expert · **dealbreaker** · K2 | The vector logo preserves the monoline octopus-in-circular-ring mark and the 'CASA POLVO' serif wordmark from restaurant_logo_flat.png without redrawing, altering, or omitting elements |
| logo_mark.svg preserves the supplied warm-gold brand color #C9A24B | auto · mandatory · K2 | The fill/stroke color of the vector logo elements samples to warm-gold #C9A24B (within small tolerance), matching the supplied restaurant_logo_flat.png |


[[PAGEBREAK]]
### AO-19 · Print-ready promotional window decals for a pizza restaurant: enhance food photography, vectorize the logo, and data-merge multiple promo versions from an authored decal layout
**Brand:** Food, Restaurant & Beverage &nbsp;·&nbsp; **Operation:** O1 Tonal grade & restore (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (19 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Take the client's raw pizza hero photo, logo, authored decal layout, and promo price list, and produce print-ready large-format window-decal PDFs — one per promotion — with professionally enhanced food photography and a vectorized logo.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| pizza_hero_raw.jpg | image | Photoreal overhead-angle restaurant food photograph of a single large pepperoni pizza fresh out of a stone ove |
| restaurant_logo.png | image | Flat 2D restaurant logo on transparent background: a simple two-color emblem of a chef-hat-wearing cartoon piz |
| decal_layout.indd | vector | Author a genuine Adobe InDesign window-decal template (.indd/.idml), 24x36 inch portrait at 300 DPI with 0.125 |
| promotions.csv | data | Generate a 4-row CSV for an InDesign data merge with columns: DEAL_NAME,PRICE,DETAILS,HERO_IMAGE. Rows: ('Larg |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| pizza_hero_enhanced.png | image | Print-grade enhanced and bleed-extended pizza hero, PNG (lossless), color-corrected (auto-tone + exposure + warm temperature + boosted vibrance + masked subject-pop on th |
| restaurant_logo.svg | vector | Clean vectorized SVG of the restaurant logo, infinitely scalable for large-format storefront reproduction, solid-fill paths, replaces the modest-resolution raster placeho |
| decal_Large1Topping.pdf | pdf | 24x36in, 300 DPI, 0.125in bleed, print-ready PDF for the Large 1-Topping Pizza Special, rendered from the authored decal layout with the enhanced hero + vectorized logo + |
| decal_PizzaWings.pdf | pdf | 24x36in, 300 DPI, 0.125in bleed, print-ready PDF for the Pizza & Wings Deal, same style. |
| decal_FamilyFeast.pdf | pdf | 24x36in, 300 DPI, 0.125in bleed, print-ready PDF for the Family Feast, same style. |
| decal_GameDayCombo.pdf | pdf | 24x36in, 300 DPI, 0.125in bleed, print-ready PDF for the Game Day Combo, same style. |
| pizza_decal_package.zip | archive | Single ZIP bundling the enhanced hero PNG, logo SVG, and all four print-ready decal PDFs for handoff to the print vendor. |

**Layer-3 verifier checks** — expert-authored (16 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| pizza_decal_package.zip bundles exactly the six deliverable files (the enhanced hero PNG, logo SVG, and four decal PDFs) | auto · mandatory · K1 | pizza_decal_package.zip exists and contains exactly these 6 files and no others: pizza_hero_enhanced.png, restaurant_logo.svg, decal_Large1Topping.pdf, decal_PizzaWings.pdf, decal_FamilyFeast.pdf, decal_GameDayCombo.pdf |
| Exactly four print-ready decal PDFs exist, one per CSV promotion, with no missing or duplicate promo | auto · mandatory · K1 | Four distinct decal PDFs are delivered, one for each of the four promotions in promotions.csv (Large 1-Topping Pizza Special, Pizza & Wings Deal, Family Feast, Game Day Combo); count == 4, each named decal_Large1Topping.pdf, decal_PizzaWings.pdf, decal_FamilyFeast.pdf, decal_GameDayCombo.pdf |
| Each decal PDF page is 24x36 inches portrait at 300 DPI | auto · mandatory · K1 | All four decal PDFs report a trim/page size of 24in wide x 36in tall (portrait orientation) at 300 DPI when read from the file metadata |
| Each decal PDF includes a 0.125in print bleed | auto · mandatory · K1 | All four decal PDFs carry a 0.125in bleed beyond the 24x36in trim (bleed box extends 0.125in on every side, i.e. ~24.25in x 36.25in) |
| Each promotion's exact deal name appears as the headline in its corresponding decal PDF | auto · mandatory · K1 | OCR of each PDF shows the exact DEAL_NAME string from promotions.csv: 'Large 1-Topping Pizza Special', 'Pizza & Wings Deal', 'Family Feast', and 'Game Day Combo' respectively |
| Each promotion's exact price from promotions.csv appears in its decal PDF | auto · **dealbreaker** · K1 | OCR shows the exact PRICE per deal: $9.99 (Large 1-Topping Pizza Special), $19.99 (Pizza & Wings Deal), $29.99 (Family Feast), $24.99 (Game Day Combo) |
| Each promotion's exact details sub-line from promotions.csv appears in its decal PDF | auto · mandatory · K1 | OCR shows the exact DETAILS string per deal: 'One large pizza, any single topping. Carryout only.' (Large 1-Topping), 'Large 2-topping pizza + 10 wings + 2L soda.' (Pizza & Wings), 'Two large pizzas, breadsticks, and a 2L soda.' (Family Feast), 'Large pizza, 20 wings, and 4 drinks.' (Game Day Combo) |
| The enhanced hero deliverable is a lossless PNG sized to the 24x36 decal panel aspect (2:3) including bleed | auto · mandatory · K1 | pizza_hero_enhanced.png is a valid lossless PNG with a 2:3 width:height aspect ratio matching the 24x36 panel plus 0.125in bleed |
| The restaurant logo deliverable is a true vector SVG, not an embedded raster | auto · mandatory · K2 | restaurant_logo.svg is a valid SVG built from vector path/shape elements with solid fills; it does NOT merely embed the original PNG bitmap as an <image> data URI |
| The same single enhanced hero image is merged into all four decal PDFs (every CSV HERO_IMAGE row points at @enhanced_hero) | auto · mandatory · K1 | The hero image placed in all four decal PDFs is the same enhanced hero asset (pizza_hero_enhanced.png), consistent with every promotions.csv HERO_IMAGE cell being @enhanced_hero; it is not four different images |
| The vectorized logo faithfully reproduces the supplied raster logo, preserving the chef-hat pizza-slice mascot, the 'TONY'S BRICK OVEN PIZZA' wordmark, and the red/cream palette | expert · **dealbreaker** · K2 | restaurant_logo.svg visually matches restaurant_logo.png: same chef-hat pizza-slice mascot, the wordmark reads 'TONY'S BRICK OVEN PIZZA', and the two-color red-and-cream palette is preserved; the logo is not redesigned or recolored |
| The vectorized client logo (not the placeholder) appears in every decal PDF footer, crisply at large-format scale | expert · mandatory · K2 | Each of the four decal PDFs displays the actual Tony's Brick Oven Pizza logo in the footer (placeholder replaced), reproduced crisply at storefront/large-format scale |
| The enhanced hero shows the full tonal grade the brief requested: corrected tone/exposure, warmer temperature, boosted topping color, and the pizza popping against the background | expert · mandatory · K4 | Compared to pizza_hero_raw.jpg, pizza_hero_enhanced.png is brighter/better-exposed, visibly warmer (golden cheese and crust), has more saturated toppings, and the pizza subject stands out from the table/background; it no longer looks flat/cool/underexposed |
| The hero photo is expanded to fill the full decal panel including bleed without a visible seam or warped edge | expert · quality · K3 | The enhanced hero fills the full 24x36 panel plus 0.125in bleed; the outpainted table/background extension blends seamlessly with the original tight crop, with no visible seam, repetition, or warped pizza edge |
| The four decals read as one coherent series, consistent in layout, typography, color treatment, logo placement, and visual hierarchy | expert · quality · K3 | All four decal PDFs share the same authored layout, typography, color treatment, logo placement, and visual hierarchy, differing only in the merged deal name, price, and details text |
| The work refines the existing approved concept rather than redesigning it — no new logo, rebrand, or altered layout structure | expert · mandatory · K7 | The decals use the supplied authored InDesign layout and the client's actual logo unchanged in design; no new logo mark, no rebrand, and no restructured layout was introduced (scope = refine existing approved concept only) |


[[PAGEBREAK]]
### AO-20 · Premium corporate-website photo retouch: grade, declutter, and export a consistent responsive image set
**Brand:** Automotive, Industrial & Agriculture &nbsp;·&nbsp; **Operation:** O4 Preset retouch & look-dev (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (20 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K2 · K1 · K6 · K7
*Take two client-shot raw corporate images (a plant-floor engineer-by-equipment hero and an executive portrait), professionally retouch and color-grade them to one consistent premium look, declutter the busy backgrounds the allowed way, then export a web-optimized responsive set (desktop/tablet/mobile) plus a Firefly board for sign-off.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| hero_engineer_cnc_raw.jpg | image | Candid documentary photograph, straight-out-of-camera look, of a 40-year-old male process engineer in a navy p |
| exec_portrait_facility_raw.jpg | image | Candid half-body corporate portrait, straight-out-of-camera, of a 50-year-old female executive in a charcoal b |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| hero_graded_master.png | image | Full-resolution retouched + color-graded hero master: exposure/WB corrected, contrast+color+sharpness enhanced, background decluttered (solid neutral fill on the cluttere |
| portrait_graded_master.png | image | Executive portrait carrying the IDENTICAL finished look (same preset) as the hero so the pair reads as one consistent set. ~6000x4000px PNG. |
| hero_desktop_1920.png | image | Web-optimized desktop hero crop centred on the subject, 1920px wide (16:9), from the graded master. |
| hero_tablet_1024.png | image | Responsive tablet crop, 1024px wide, subject-centred, from the graded master. |
| hero_mobile_640.png | image | Responsive mobile crop, 640px wide, subject-centred, fast-loading, from the graded master. |
| corporate_retouch_review_board | url | Firefly Board deep-link assembling the graded hero, the matching portrait and the three responsive crops for one-click marketing sign-off. |
| corporate_website_image_set.zip | archive | Single ZIP bundling the two graded masters and the three responsive crops for handoff to the web team. |

**Layer-3 verifier checks** — expert-authored (16 checks, 1 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All five image deliverables are present by name: hero_graded_master.png, portrait_graded_master.png, hero_desktop_1920.png, hero_tablet_1024.png, hero_mobile_640.png | auto · mandatory · K1 | Exactly these 5 PNG files exist (by name or clear equivalent): hero_graded_master, portrait_graded_master, hero_desktop_1920, hero_tablet_1024, hero_mobile_640 |
| All five image deliverables are valid PNG files | auto · **dealbreaker** · K1 | hero_graded_master, portrait_graded_master, hero_desktop_1920, hero_tablet_1024 and hero_mobile_640 are all valid .png files (PNG format as specified for every image output) |
| Both graded masters are full resolution at approximately 6000x4000px, 3:2 | auto · mandatory · K1 | hero_graded_master.png and portrait_graded_master.png each read ~6000x4000px (within tolerance), aspect ratio 3:2 |
| Desktop responsive crop is 1920px wide at 16:9 | auto · mandatory · K1 | hero_desktop_1920.png has width == 1920px and a 16:9 aspect ratio (i.e. 1920x1080) |
| Tablet responsive crop is 1024px wide | auto · mandatory · K1 | hero_tablet_1024.png has width == 1024px |
| Mobile responsive crop is 640px wide | auto · mandatory · K1 | hero_mobile_640.png has width == 640px |
| The three responsive crops are derived from the graded hero master, not the raw input | expert · mandatory · K1 | hero_desktop_1920, hero_tablet_1024 and hero_mobile_640 all visibly carry the same corrected exposure/white-balance/contrast grade and decluttered+blurred background as hero_graded_master, not the raw cool/green underexposed look |
| Each responsive crop is centred on the subject (the engineer) | expert · quality · K3 | In all three crops (1920, 1024, 640) the engineer remains the centred, framed subject and is not cut off |
| A single ZIP, corporate_website_image_set.zip, bundles exactly the two graded masters and the three responsive crops | auto · mandatory · K1 | corporate_website_image_set.zip exists and contains exactly 5 files: hero_graded_master, portrait_graded_master, hero_desktop_1920, hero_tablet_1024, hero_mobile_640 |
| A Firefly Board review URL (corporate_retouch_review_board) is delivered assembling the graded hero, matching portrait and the three responsive crops | auto · mandatory · K1 | A Firefly Board deep-link URL is returned and the board contains the 5 produced assets (graded hero, graded portrait, hero_desktop_1920, hero_tablet_1024, hero_mobile_640) |
| Hero exposure and white balance are corrected from the raw cool/green underexposed state to neutral | expert · mandatory · K4 | hero_graded_master shows a sane, no-longer-underexposed exposure with the cool/green cast pulled to neutral white balance versus the raw input |
| Hero shows enhanced contrast, color and sharpness reading as a premium look | expert · mandatory · K4 | hero_graded_master has visibly added contrast, richer color and improved sharpness versus the flat raw input, reading premium |
| The cluttered hero background (parts bins, cables, fire extinguisher) is calmed via a solid neutral fill on the inverted background mask, NOT AI object removal, with the subject untouched | expert · mandatory · K3 | Distracting background clutter behind the engineer is suppressed by a neutral solid fill over the background region while the engineer remains intact and unaltered; no generative/AI object-removal artifacts present |
| The hero background is thrown out of focus (lens blur) so the subject pops | expert · quality · K3 | hero_graded_master shows the calmed background softened/out of focus relative to the subject |
| The executive portrait carries the identical finished look (same shared preset) as the hero so the pair reads as one consistent set | expert · mandatory · K4 | portrait_graded_master and hero_graded_master share the same tone/color/contrast grade so the originally warm-flat portrait and cool-underexposed hero now read as one visually consistent set |
| The retouch stays natural and realistic — authentic factory subject, no fake studio/CGI look | expert · mandatory · K4 | Both graded images retain authentic skin texture, natural hands and a believable real-factory environment with no glossy/CGI/over-retouched appearance |


[[PAGEBREAK]]
### AO-21 · Creative Business Headshot — Studio Retouch, Color Grade & Brand-Profile Asset Pipeline
**Brand:** General / Cross-Industry Branding & Graphics &nbsp;·&nbsp; **Operation:** O4 Preset retouch & look-dev (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (20 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K2 · K1 · K6 · K7
*Take the client's raw studio headshot frame and brand monogram and produce a retouched, color-graded, creatively recomposed professional-profile headshot set (color + monochrome + 16:9 dynamic + LinkedIn 1:1 + banner crops) plus a clean vector logomark, all delivered in one folder.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| studio_headshot_raw.jpg | image | Photoreal un-retouched studio business headshot of a 38-year-old founder, head-and-shoulders, shot against a s |
| monogram_flat.png | image | A flat, clean two-letter serif monogram wordmark 'AV' inside a thin circular ring, solid charcoal (#2B2B2B) on |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| headshot_hero_color_16x9.jpg | image | Final retouched + color-graded creative headshot, outpainted to a 16:9 environmental hero crop (e.g. 2560x1440), warm studio skin tone, brightened eyes/teeth, soft backgr |
| headshot_hero_mono.jpg | image | Monochrome (monochromatic-tint) alternate of the final color hero, same 16:9 framing. JPEG, sRGB. |
| headshot_linkedin_1x1.jpg | image | 1:1 avatar/profile crop (e.g. 1000x1000) derived from the finished color portrait, subject-centered. JPEG, sRGB. |
| headshot_linkedin_banner_1584x396.jpg | image | 1584x396 LinkedIn banner crop derived from the finished color portrait/hero, subject offset with text room. JPEG, sRGB. |
| monogram_logomark.svg | vector | Clean vectorized SVG of the 'AV' ring monogram, single-color paths, scalable for print + large web. |
| Headshot_Delivery/ (folder + preview) | data | One CC asset folder containing all of the above, plus an inline preview of the delivery set for client review. |

**Layer-3 verifier checks** — expert-authored (16 checks, 5 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| The color hero deliverable headshot_hero_color_16x9.jpg is present and exactly 16:9 aspect ratio | auto · mandatory · K1 | A file named headshot_hero_color_16x9.jpg exists and its pixel width:height ratio equals 16:9 (1.7778 within rounding, e.g. 2560x1440) |
| The monochrome alternate headshot_hero_mono.jpg is present at the same 16:9 framing as the color hero | auto · mandatory · K1 | A file named headshot_hero_mono.jpg exists and is 16:9 aspect ratio (1.7778 within rounding) matching the color hero dimensions |
| The LinkedIn avatar crop headshot_linkedin_1x1.jpg is present at exactly 1:1 aspect ratio | auto · mandatory · K1 | A file named headshot_linkedin_1x1.jpg exists with equal pixel width and height (1:1, e.g. 1000x1000) |
| The LinkedIn banner crop headshot_linkedin_banner_1584x396.jpg is present at exactly 1584x396 pixels | auto · **dealbreaker** · K1 | A file named headshot_linkedin_banner_1584x396.jpg exists with pixel dimensions exactly 1584x396 (the verbatim LinkedIn banner size in the brief) |
| All four raster image deliverables are JPEG format in the sRGB color space | auto · **dealbreaker** · K1 | headshot_hero_color_16x9.jpg, headshot_hero_mono.jpg, headshot_linkedin_1x1.jpg, and headshot_linkedin_banner_1584x396.jpg are each encoded as JPEG and in the sRGB color space (no CMYK or wide-gamut/non-sRGB ICC profile) |
| The vector logomark monogram_logomark.svg is present and is a valid scalable SVG containing vector paths (not an embedded raster) | auto · **dealbreaker** · K1 | A file named monogram_logomark.svg exists, parses as valid SVG, and contains <path> vector geometry with no embedded bitmap (no <image> element or base64 raster data) |
| The vectorized logomark renders the 'AV' two-letter monogram inside a thin circular ring as a single ink color | expert · **dealbreaker** · K2 | Rendered SVG visibly shows the serif letters 'AV' within a thin circular ring, traced as clean single-color paths faithful to the supplied monogram_flat.png (solid charcoal #2B2B2B, no gradients/texture) |
| All five deliverables are placed inside a single CC asset folder named Headshot_Delivery/ | auto · mandatory · K1 | A folder named Headshot_Delivery/ exists and contains exactly the five deliverables: headshot_hero_color_16x9.jpg, headshot_hero_mono.jpg, headshot_linkedin_1x1.jpg, headshot_linkedin_banner_1584x396.jpg, and monogram_logomark.svg |
| An inline preview of the populated delivery set is produced for client review | auto · mandatory · K6 | An inline preview of the populated Headshot_Delivery/ folder is rendered and returned to the user |
| The hero frame has been straightened from the raw ~1.5-degree tilt and shows a level horizon/verticals | expert · quality · K3 | The subject and seamless backdrop in the color hero appear level (no residual ~1.5-degree tilt) compared to the supplied tilted studio_headshot_raw.jpg |
| The color hero is tonally graded with intentional exposure/contrast and warmer skin tone than the flat, cool raw input | expert · mandatory · K4 | Compared to studio_headshot_raw.jpg, the color hero shows added contrast/exposure grade and a warmer (less cool/blue) skin tone, reading as a premium business portrait rather than a flat phone snapshot |
| Eyes and teeth are selectively brightened while skin texture is preserved and the face is not reshaped | expert · **dealbreaker** · K7 | Eyes and teeth read brighter than the raw input, with natural skin pores/texture retained (no plastic-smooth skin) and no face/feature reshaping |
| The background is softly blurred to separate the subject while the subject stays sharp | expert · mandatory · K3 | In the color hero the backdrop shows a soft separation blur with clean subject edges while the subject (face/shoulders) remains in focus |
| The 16:9 hero was extended wider via outpaint, adding seamless backdrop room for text | expert · mandatory · K3 | The color hero shows a widened canvas with extended seamless backdrop (consistent outpainted continuation of the mid-gray studio backdrop) giving negative space for text, beyond the original portrait framing |
| The monochrome alternate is a true B&W/monochromatic-tint version of the same finished color hero | expert · mandatory · K4 | headshot_hero_mono.jpg shows the identical composition to the color hero rendered in monochrome/monochromatic tint with no residual color cast |
| The 1:1 avatar and 1584x396 banner crops are derived from the finished color portrait, with the subject centered in the 1:1 and offset for text room in the banner | expert · quality · K3 | headshot_linkedin_1x1.jpg shows the subject centered and headshot_linkedin_banner_1584x396.jpg shows the subject offset leaving clear text space, both clearly cropped from the same finished color hero |


[[PAGEBREAK]]
### AO-22 · Production-finish a modern vibrant abstract logo: clean, color-tune, vectorize, and ship full-colour + single-colour + print variants with a style note
**Brand:** Party, Events &amp; Promotion &nbsp;·&nbsp; **Operation:** O4 Preset retouch & look-dev (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (16 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K2 · K1 · K6 · K7
*Take my approved raster abstract logo concept and produce the full hand-off package — cleaned and brightened full-colour vector master (AI/SVG), a single-colour version, a single-colour print/screen variant, a wide social-header lockup, high-res PNG/JPEG exports, and a style note with hex/RGB values and recommended typography.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| approved_abstract_mark.png | image | A single modern abstract brand logo mark centered on a plain pale-grey studio background, rendered as if expor |
| brand_palette_swatch.png | image | A simple horizontal brand colour swatch strip on white, five flat solid rectangles edge to edge with no gaps: |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| logo_fullcolour_master.svg | vector | Full-colour vector master of the cleaned, brightened, background-removed abstract mark. Produced by image_vectorize from the finished raster. Razor-sharp at any size; thi |
| logo_fullcolour_master.png | image | High-resolution transparent PNG of the full-colour mark, exported from the cleaned raster (post background-removal). >=2000 px on the long edge, alpha transparency, brand |
| logo_singlecolour.png | image | Single-colour (one flat brand ink, magenta #E6007E) version of the mark on transparency, produced via subject selection -> invert -> solid fill. For one-ink stamping, emb |
| logo_singlecolour_halftone_print.png | image | Single-colour PRINT/SCREEN variant: halftone/duotone treatment of the mark for low-ink packaging and merch screen-printing. Crisp dot pattern, one ink. |
| logo_social_header_lockup.png | image | Wide website/social-header lockup: the mark with canvas extended (outpainted) into a banner field that also crops cleanly to a square profile photo. High-res PNG/JPEG. |
| brand_style_note.txt/board | data | Simple style note: exact hex/RGB values for the locked palette (#E6007E, #FF5A36, #00C2D1, #16161D, #F4F2EC) plus a recommended typography pairing (from font_recommend) s |

**Layer-3 verifier checks** — expert-authored (16 checks, 4 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| Full-colour vector master delivered as an SVG vector source file | auto · **dealbreaker** · K1 | A file named logo_fullcolour_master.svg exists and is a valid SVG containing vector path/shape geometry (not a single embedded raster <image>), produced by vectorizing the cleaned mark |
| Full-colour high-res transparent PNG export delivered at required resolution with alpha | auto · mandatory · K1 | logo_fullcolour_master.png exists, is a PNG with an alpha channel (transparency), and is >=2000 px on its long edge |
| Single-colour version is one flat brand ink on transparency | auto · mandatory · K1 | logo_singlecolour.png exists as a PNG with a transparent background where the mark is filled with a single flat colour matching brand magenta #E6007E (one hue only, no gradient, no second colour) |
| Single-colour print/screen variant uses a halftone one-ink screen | expert · mandatory · K1 | logo_singlecolour_halftone_print.png exists and shows a halftone dot-screen pattern rendered in a single ink (one colour), suitable for low-ink packaging / merch screen-printing |
| Wide social/website-header lockup delivered as a banner that also crops square | expert · mandatory · K1 | logo_social_header_lockup.png exists as a wide landscape banner with the canvas extended (outpainted) around the mark, whose central region also composes cleanly as a square profile photo |
| Deliverables exported as high-resolution PNG and JPEG per the brief | auto · mandatory · K1 | The hand-off includes high-resolution exports in BOTH PNG and JPEG formats, as the brief requires ('export everything as high-resolution PNG and JPEG') |
| Style note lists the exact locked palette hex values with RGB | auto · **dealbreaker** · K1 | brand_style_note (txt/board) lists all five exact locked hex values #E6007E, #FF5A36, #00C2D1, #16161D, #F4F2EC, each with its RGB equivalent, pulled from brand_palette_swatch.png |
| Style note includes a recommended typography pairing | auto · mandatory · K1 | brand_style_note names a specific recommended typography/font pairing (sourced from font_recommend) suited to the modern, energetic brand personality |
| All five visual deliverables gathered into one Firefly review board | auto · mandatory · K6 | A Firefly board exists containing the five visual deliverables (full-colour vector, full-colour clean PNG, single-colour, halftone print variant, header lockup) for one-place review |
| Brand colours match the supplied palette swatch, not invented or muddy hues | expert · **dealbreaker** · K2 | The tuned mark's colours read as the locked brand palette (electric magenta #E6007E, coral-orange #FF5A36, vivid cyan #00C2D1) matching brand_palette_swatch.png — clean and brand-accurate, not shifted or muddy |
| Supplied abstract mark is finished, not regenerated or replaced | expert · **dealbreaker** · K2 | The delivered mark is the same approved abstract form from approved_abstract_mark.png (three overlapping rounded chevron/petal shapes) — production-finished, not a new or redrawn mark |
| Mark sits square, level and tightly cropped | expert · mandatory · K3 | The finished mark is straightened (no residual ~1.5deg tilt) and tightly cropped to a centered square bound with the uneven margin removed |
| Background knocked out to clean transparency with no grey fringe/halo | expert · mandatory · K3 | The full-colour master has a fully transparent background with the original grey background and edge fringe/halo removed cleanly at the shape edges |
| Colours read bright and energetic after the vibrance/saturation push | expert · quality · K4 | Compared to the flat/dull input, the finished mark's colours are noticeably brighter and more energetic (vibrance/saturation lifted) while staying clean, not muddy |
| Mark is abstract/geometric with no literal illustration or vintage flourishes | expert · mandatory · K4 | The delivered mark remains a modern clean abstract geometric form — no literal objects/illustrations and no vintage flourishes, per the brand direction |
| Vector master stays razor-sharp at large scale | expert · quality · K3 | logo_fullcolour_master.svg renders crisp clean edges with no rasterized blur or jaggedness when scaled up to large sizes |


[[PAGEBREAK]]
### AO-23 · Teaser, Thumbnail and End-Card Content Package for a Luxury Manhattan Real-Estate YouTube Channel
**Brand:** Real Estate, Construction & Property &nbsp;·&nbsp; **Operation:** O4 Preset retouch & look-dev (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (17 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K2 · K1 · K6 · K7
*Produce the full per-video content package for one luxury Manhattan real-estate YouTube video — a retouched high-contrast thumbnail base plate, a podcast-style teaser cut (YouTube + LinkedIn sizes) with cleaned voice-over, and a branded end card — all from the broker's supplied portrait, penthouse still, raw walkthrough footage, end-card backplate, and wordmark logo.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| broker_portrait.jpg | image | Photoreal studio headshot of a confident 45-year-old male luxury real-estate broker, charcoal tailored suit, n |
| penthouse_hero.jpg | image | Photoreal interior real-estate hero shot of a Tribeca penthouse great room at blue hour: floor-to-ceiling wind |
| walkthrough_raw_1080p.mp4 | video | 1080p handheld-stabilized real-estate walkthrough of a Tribeca penthouse: opens on the broker speaking to came |
| endcard_backplate_1080p.mp4 | video | 12-second branded outro backplate for a luxury real-estate channel: slow drifting aerial of the Manhattan skyl |
| broker_wordmark_logo.png | image | Minimal luxury real-estate wordmark logo on transparent background, the text 'STERLING ROW' in an elegant high |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| thumbnail_base_1280x720.png | image | 1280x720 (16:9) high-contrast luxury thumbnail BASE plate: straightened + auto-toned broker figure isolated from background, moody graded penthouse hero, canvas outpainte |
| broker_portrait_isolated.png | image | Transparent-background PNG of the retouched broker (auto-straightened, auto-toned, subject-isolated) for flexible placement on the thumbnail and future videos. |
| logo_wordmark.svg | vector | Clean vectorized SVG of the 'STERLING ROW' wordmark, scalable for thumbnail and end-card placement. |
| teaser_youtube_1920x1080.mp4 | video | 30-90s podcast-cold-open teaser, hook in first 5s, hard-cut before resolution, 1920x1080 YouTube-native, cleaned voice-over, prestige tone, no transitions. |
| teaser_linkedin_1080x1080.mp4 | video | Same teaser reframed to 1080x1080 square for LinkedIn cross-posting, same length (no trim), cleaned voice-over. |
| endcard_1920x1080.mp4 | video | 10-15s branded end card reframed to exactly 1920x1080 with clear space for subscribe prompt, suggested-video card and CTA, consistent across videos. |

**Layer-3 verifier checks** — expert-authored (17 checks, 1 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| Thumbnail base plate is exactly 1280x720 px (16:9) | auto · mandatory · K1 | thumbnail_base_1280x720.png is exactly 1280 px wide by 720 px tall (16:9 aspect ratio) |
| Thumbnail base plate is delivered as a PNG in sRGB | auto · mandatory · K1 | thumbnail_base_1280x720.png is a valid PNG file in the sRGB color space |
| The graded penthouse hero is outpainted to fill the full 1280x720 frame with no stretching | expert · mandatory · K3 | On thumbnail_base_1280x720.png the graded penthouse hero is cropped to the 16:9 frame and the canvas is AI-outpainted to fill the entire 1280x720 frame with no edge stretching, squashing, or empty/letterboxed regions |
| The penthouse hero shows a moody high-contrast luxury grade with restraint | expert · quality · K4 | Relative to the supplied penthouse_hero.jpg, thumbnail_base_1280x720.png shows deepened shadows, controlled/recovered window highlights, warmer prestige color temperature, and punchy local contrast while keeping luxury restraint (not over-saturated) |
| Isolated broker PNG has a fully transparent background | auto · mandatory · K1 | broker_portrait_isolated.png is a PNG with an alpha channel and a fully transparent background around the broker figure (no studio backdrop pixels remaining) |
| The broker figure is cleanly isolated with believable edges, straightened and auto-toned | expert · mandatory · K3 | In broker_portrait_isolated.png the broker is leveled/straightened, exposure/contrast/white-balance balanced, and the subject mask cuts the figure (including hair edges) cleanly with no backdrop fringing or chopped limbs |
| Logo wordmark is delivered as a vector SVG (not embedded raster) | auto · mandatory · K1 | logo_wordmark.svg is a valid SVG file containing vector path data and no embedded raster bitmap image |
| Vectorized logo faithfully reproduces the 'STERLING ROW' wordmark | expert · **dealbreaker** · K2 | logo_wordmark.svg renders the wordmark 'STERLING ROW' as a faithful vectorization of the supplied broker_wordmark_logo.png (correct serif letterforms, thin underline rule, monochrome charcoal) with crisp scalable edges and no regenerated or altered lettering |
| YouTube teaser is exactly 1920x1080 px | auto · mandatory · K1 | teaser_youtube_1920x1080.mp4 has a video frame size of exactly 1920x1080 px |
| YouTube teaser duration is between 30 and 90 seconds | auto · mandatory · K1 | teaser_youtube_1920x1080.mp4 runtime is >= 30s and <= 90s |
| Teaser hooks in the first 5 seconds and hard-cuts before resolution | expert · mandatory · K4 | teaser_youtube_1920x1080.mp4 opens with a compelling hook within the first 5 seconds and ends with a hard cut before the property/market resolution is revealed (podcast-cold-open structure) |
| Teaser reads as prestige with no cheap transitions | expert · quality · K4 | The teaser cut reads as luxury/prestige and contains no cheap transitions (no flashy wipes, zooms, or stock effects); cuts are clean |
| Teaser voice-over is denoised to broadcast-clean | expert · mandatory · K4 | The broker's lavalier voice-over on the teaser deliverables is denoised/enhanced so the spoken track is broadcast-clean (reduced room tone/noise, intelligible voice) versus the raw walkthrough audio |
| LinkedIn teaser is exactly 1080x1080 px (square) | auto · mandatory · K1 | teaser_linkedin_1080x1080.mp4 has a video frame size of exactly 1080x1080 px |
| LinkedIn square teaser is the same length as the YouTube teaser with no trim | auto · mandatory · K1 | teaser_linkedin_1080x1080.mp4 runtime equals teaser_youtube_1920x1080.mp4 runtime (reframe only, no trim) |
| End card is exactly 1920x1080 px and 10-15 seconds long with no trim | auto · mandatory · K1 | endcard_1920x1080.mp4 has a frame size of exactly 1920x1080 px and a runtime >= 10s and <= 15s, equal in length to the supplied endcard_backplate_1080p.mp4 (reframe only, no trim) |
| End card preserves clear space for subscribe prompt, suggested-video card, and CTA | expert · quality · K3 | After reframing to 1920x1080, endcard_1920x1080.mp4 retains the lower-third/negative-space zones so the subscribe prompt, suggested-video slot, and CTA sit correctly and stay consistent across videos |


[[PAGEBREAK]]
### AO-24 · Open House Finance Flyer: property-photo retouch, brass/gold brand look, logo vectorize, and InDesign price-scenario data-merge for a Solano County mortgage lender
**Brand:** Real Estate, Construction & Property &nbsp;·&nbsp; **Operation:** O4 Preset retouch & look-dev (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (24 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K2 · K1 · K6 · K7
*Prep and grade the hero property photo and lender headshot into a black + brass/gold luxury look, vectorize the lender wordmark, then export the authored InDesign Open House Finance flyer (front/back) and data-merge the monthly-payment / down-payment / appreciation scenarios from a CSV into print-ready pages.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| property_exterior_raw.jpg | image | Photoreal hi-res real-estate exterior listing photo of a modern two-story Northern California home, beige stuc |
| lender_headshot_raw.jpg | image | Photoreal professional corporate headshot of a friendly mid-40s mortgage lender, business-casual blazer no tie |
| lender_wordmark.png | image | Flat 2D brand wordmark logo on transparent background, the text 'HARLAN HOME LENDING' in an elegant high-contr |
| open_house_finance_flyer.indd | pdf | Author a genuine 2-page (front/back) US-Letter InDesign template for an 'Open House Finance Flyer': front has |
| payment_scenarios.csv | data | Generate a realistic CSV with header row PurchasePrice,DownPaymentOptions,MonthlyPayment,AppreciationProjectio |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| hero_property_print.jpg | image | Straightened, exposure-corrected, luxury-graded (warm brass/gold cast, rich blacks) hero exterior at the flyer's print hero frame ratio, 300 DPI, sRGB JPEG |
| hero_property_banner.jpg | image | Wide banner-ratio version of the graded hero, canvas extended via generative outpaint on sky/foreground so the house is not cropped, sized to the flyer's full-width hero |
| property_cutout.png | image | House isolated from background, transparent PNG, for the digital/social flyer variant |
| headshot_matched.jpg | image | Retouched lender headshot color-matched to the same warm luxury grade, sRGB JPEG, sized for the flyer headshot frame |
| wordmark.svg | vector | Clean vectorized single-color wordmark, scalable SVG for print + contact strip |
| open_house_finance_flyer.pdf | pdf | Front/back Open House Finance Flyer exported from the authored .indd, US-Letter, print-ready PDF |
| payment_scenarios_merged.pdf | pdf | Multi-page print-ready PDF from the InDesign data-merge — one page per CSV scenario row (purchase price, down-payment options, monthly payment, appreciation projection, a |
| approval_board | data | Firefly board deep-link collecting the final approved assets (graded hero, banner, cut-out, matched headshot, SVG wordmark) for client sign-off |

**Layer-3 verifier checks** — expert-authored (17 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| hero_property_print.jpg is delivered as an sRGB JPEG at 300 DPI | auto · mandatory · K1 | A file named hero_property_print.jpg exists, is a valid JPEG with an sRGB color profile, and its DPI metadata reads 300 |
| The hero property photo is straightened and tilt-corrected relative to the ~4-degree tilted raw input | expert · mandatory · K1 | The house/horizon in hero_property_print.jpg is visually level (no residual ~4-degree tilt versus property_exterior_raw.jpg) and the empty wedges left by straightening are cropped out |
| The hero property photo carries the black + brass/gold luxury grade (warm cast, rich blacks) and the mixed-light exposure is corrected | expert · quality · K4 | hero_property_print.jpg shows a warm brass/gold-leaning color grade with rich/deep blacks, blown sky highlights recovered and muddy shadows lifted, consistent with the brand's sophisticated/luxury black-white-and-brass/gold look |
| hero_property_banner.jpg is delivered as a JPEG with a wider aspect ratio than hero_property_print.jpg | auto · mandatory · K1 | A file named hero_property_banner.jpg exists, is a valid JPEG, and its width-to-height aspect ratio is wider than hero_property_print.jpg's |
| The hero_property_banner is the graded hero with the canvas generatively extended (outpainted) and the house not cropped | expert · mandatory · K1 | hero_property_banner.jpg is the same graded hero scene with the added sky/foreground generatively outpainted (not stretched, cloned, or tiled), and the full house is intact and uncropped |
| property_cutout.png is the house isolated from its background as a transparent PNG | auto · mandatory · K1 | A file named property_cutout.png exists, is a PNG with an alpha channel, and contains transparent (non-opaque) background pixels |
| The property_cutout.png background isolation has clean edges around the house | expert · quality · K3 | The house is cleanly separated from its background in property_cutout.png with no background halo, fringing, or chunks of the house removed |
| headshot_matched.jpg is delivered as a valid sRGB JPEG | auto · mandatory · K1 | A file named headshot_matched.jpg exists and is a valid JPEG with an sRGB color profile |
| The matched headshot's color/tone visually matches the hero property's warm luxury grade so they sit together | expert · quality · K4 | headshot_matched.jpg shows the same warm brass/gold-leaning grade as hero_property_print.jpg (no residual cool/flat studio cast) while keeping natural skin texture (not airbrushed) |
| wordmark.svg is a clean vectorized single-color SVG of the lender wordmark | auto · mandatory · K1 | A file named wordmark.svg exists and is a valid SVG containing vector path geometry (not just an embedded raster image) |
| The vectorized wordmark preserves the exact brand text 'HARLAN HOME LENDING' and the house-key monogram mark | expert · **dealbreaker** · K2 | wordmark.svg renders the wordmark text 'HARLAN HOME LENDING' (correct spelling, high-contrast serif) with the small house-key monogram to the left, crisp at scale, traced from lender_wordmark.png rather than regenerated or altered |
| open_house_finance_flyer.pdf is a front/back US-Letter print-ready PDF exported from the authored .indd template | auto · mandatory · K1 | A file named open_house_finance_flyer.pdf exists, is a valid PDF with exactly 2 pages (front/back), and each page is US-Letter sized (8.5 x 11 in) |
| payment_scenarios_merged.pdf is the InDesign data-merge output with one page per CSV scenario row | auto · mandatory · K1 | A file named payment_scenarios_merged.pdf exists, is a valid PDF, and contains exactly 6 pages (one per the 6 data rows in payment_scenarios.csv) |
| Each merged page binds the CSV row values into the merge fields with no unresolved placeholders remaining | auto · mandatory · K1 | Every page of payment_scenarios_merged.pdf shows resolved values for PurchasePrice, DownPaymentOptions, MonthlyPayment, AppreciationProjection and PropertyAddress, with no literal <<PurchasePrice>>/<<DownPaymentOptions>>/<<MonthlyPayment>>/<<AppreciationProjection>>/<<PropertyAddress>> placeholder text remaining on any page |
| The merged scenario values match the source payment_scenarios.csv exactly | auto · mandatory · K1 | For each of the 6 pages, the PurchasePrice, DownPaymentOptions, MonthlyPayment, AppreciationProjection and PropertyAddress shown equal the corresponding row values in payment_scenarios.csv |
| A Firefly approval board deep-link is delivered collecting the five final approved visual assets | auto · mandatory · K6 | An approval_board Firefly board deep-link is returned and references all five final visual assets: the graded hero (hero_property_print), banner (hero_property_banner), cut-out (property_cutout), matched headshot (headshot_matched) and SVG wordmark (wordmark.svg) |
| The client's supplied assets (property photo, headshot, wordmark) are the same source assets used in the deliverables, not regenerated or substituted | expert · **dealbreaker** · K7 | hero_property_print.jpg depicts the same house as property_exterior_raw.jpg, headshot_matched.jpg is the same person as lender_headshot_raw.jpg, and wordmark.svg traces the supplied lender_wordmark.png — none are AI-regenerated or replaced with different assets |


[[PAGEBREAK]]
### AO-25 · Premium, consistent HDR grade for a Caribbean vacation-rental villa listing set (interior + pool + sea/sky), delivered as web-ready JPEGs plus a client review board
**Brand:** Real Estate, Construction & Property &nbsp;·&nbsp; **Operation:** O4 Preset retouch & look-dev (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (19 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K2 · K1 · K6 · K7
*Take a property's three raw Nodalview-HDR exports (luxury interior, pool deck, sea/sky terrace) and finish them into a consistent, natural, premium listing set — level horizons, balance exposure/white-balance, gently enhance pool water, sea color, sky and vegetation, brighten interiors and balance the bright window view, then deliver matched 2048px web JPEGs plus a 16:9 hero and a client review board.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| interior_seaview.jpg | image | Photoreal real-estate interior of a luxury Caribbean villa living room, shot on a wide lens at golden hour, HD |
| pool_deck.jpg | image | Photoreal real-estate photo of a luxury villa infinity pool deck in Saint-Martin, midday, HDR-bracketed but sl |
| terrace_seaview.jpg | image | Photoreal wide real-estate shot from a luxury villa terrace looking out over the Caribbean sea and sky at late |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| interior_seaview_final.jpg | image | Finished luxury interior, straightened + auto-tone + exposure/WB-corrected + shadow-lifted with the bright window view held, neutral whites, no green cast. sRGB JPEG, 204 |
| pool_deck_final.jpg | image | Finished pool deck with naturally enhanced turquoise water (selective cyan/blue saturation, not global), enriched-but-natural vegetation greens, gently improved sky. sRGB |
| terrace_seaview_final.jpg | image | Finished sea/sky terrace, leveled horizon, natural contrast, gently enhanced sea and sky color. sRGB JPEG, 2048px long edge, quality 90. |
| hero_16x9.jpg | image | 16:9 listing-header hero cropped from the finished terrace frame. sRGB JPEG, 1920x1080. |
| review_board | url | Firefly review board deep-link assembling the three finished frames + the hero so the property manager can approve the consistent look in one place. |

**Layer-3 verifier checks** — expert-authored (16 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All three finished frame JPEGs are delivered (interior_seaview_final.jpg, pool_deck_final.jpg, terrace_seaview_final.jpg) | auto · mandatory · K1 | Exactly three finished-frame JPEG files exist, named interior_seaview_final.jpg, pool_deck_final.jpg and terrace_seaview_final.jpg |
| Each of the three finished frames is exported at 2048px on the long edge | auto · mandatory · K1 | interior_seaview_final.jpg, pool_deck_final.jpg and terrace_seaview_final.jpg each have a long edge of exactly 2048px |
| All delivered images are sRGB JPEG format | auto · **dealbreaker** · K1 | interior_seaview_final.jpg, pool_deck_final.jpg, terrace_seaview_final.jpg and hero_16x9.jpg are all JPEG files encoded in the sRGB color space |
| The three matched frames are exported at JPEG quality 90 | auto · quality · K1 | interior_seaview_final.jpg, pool_deck_final.jpg and terrace_seaview_final.jpg are each encoded at approximately JPEG quality 90 |
| The 16:9 hero crop is delivered at exactly 1920x1080 | auto · mandatory · K1 | hero_16x9.jpg exists and has pixel dimensions exactly 1920x1080 (16:9 aspect ratio) |
| The hero crop is derived from the finished terrace (sea/sky) frame, not the interior or pool | expert · mandatory · K1 | hero_16x9.jpg is visibly a 16:9 crop of the finished terrace_seaview sea/sky frame (the best exterior), matching its color treatment — not a crop of the interior or pool frame |
| A client review board deep-link is delivered assembling the finished frames plus the hero | auto · mandatory · K1 | A review_board URL (Firefly board deep-link) is returned that assembles four assets: interior_seaview_final.jpg, pool_deck_final.jpg, terrace_seaview_final.jpg and hero_16x9.jpg |
| Tilted horizons are leveled on the interior and terrace frames | expert · mandatory · K3 | In interior_seaview_final.jpg the ~1.5° tilt seen through the window is corrected, and in terrace_seaview_final.jpg the ~2° sea horizon is level/horizontal |
| Interior white-balance is corrected to neutral whites with no green/magenta cast | expert · mandatory · K4 | interior_seaview_final.jpg shows neutral indoor whites with the warm tungsten cast and the green shadow tint removed, leaving no residual color cast |
| Interior shadows are lifted for brightness while the bright window sea view is held (indoor/outdoor balance) | expert · mandatory · K3 | interior_seaview_final.jpg has brighter, clearer interior shadows AND the bright window sea view is recovered/not blown out — both indoor and outdoor detail are readable |
| Pool water and sea are enhanced via selective cyan/blue saturation, not a global saturation pump | expert · mandatory · K4 | In pool_deck_final.jpg the turquoise water reads cleaner via cyan/blue-specific enhancement while non-blue tones (loungers, deck) remain neutral — no global oversaturation |
| Vegetation greens are enriched naturally and the sky is gently improved in the pool frame | expert · quality · K4 | pool_deck_final.jpg shows richer-but-natural palm/foliage greens and a gently improved (de-hazed) sky |
| The result avoids a fake-HDR / over-saturated / unrealistically-blue-pool look (DO-NOT-WANT list) | expert · **dealbreaker** · K4 | None of the finished frames show halo/fake-HDR artifacts, global over-saturation, or an unrealistically blue pool — overall vibrance stays gentle and natural |
| The three frames read as one coherent, consistent set | expert · mandatory · K3 | interior_seaview_final.jpg, pool_deck_final.jpg and terrace_seaview_final.jpg share consistent exposure, white-balance and matched cyan/blue treatment so they read as one property |
| The terrace frame has added natural contrast and gently enhanced sea/sky color consistent with the pool treatment | expert · quality · K4 | terrace_seaview_final.jpg shows natural contrast (no longer flat) and the muted teal sea/sky is enhanced with the same restrained cyan/blue treatment as the pool frame |
| Out-of-scope items (converging-vertical/perspective warp and cable/reflection/stain cloning) are flagged for the human finisher rather than silently dropped | expert · mandatory · K7 | The deliverable communication explicitly states that converging-vertical/perspective correction and cable/reflection/stain removal are out of automated connector scope and left for the human finisher |


[[PAGEBREAK]]
### AO-26 · High-Volume Real Estate Listing Retouch — HDR Tone-Map, Window Pull, Lawn Boost & Consistent-Style Delivery
**Brand:** Real Estate, Construction & Property &nbsp;·&nbsp; **Operation:** O4 Preset retouch & look-dev (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (21 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K2 · K1 · K6 · K7
*Edit one real-estate listing's frames into MLS-ready, consistently styled images: tone-map the wide-DR exterior (window pull), enhance the sky, pop the lawn, straighten and crop, then lock that look as a preset and push it across the interior frames for a uniform property set.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| exterior_hero_wideDR.png | image | Photoreal real-estate exterior real-estate-photography frame of a two-story suburban American home shot on a w |
| interior_living_room_brightwindow.png | image | Photoreal real-estate interior frame of a staged living room with large windows on one wall that are very brig |
| interior_kitchen.png | image | Photoreal real-estate interior frame of a staged modern kitchen with a window over the sink that is bright and |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| exterior_hero_MLS.png | image | Finished exterior hero: straightened, cropped, auto-toned, window-pulled (windows + global highlights recovered), sky enhanced (masked highlight recovery + blue boost), l |
| interior_living_room_MLS.png | image | Living-room interior with the SAME locked preset applied + window/highlight tame. High-quality PNG, style-matched to the exterior hero. |
| interior_kitchen_MLS.png | image | Kitchen interior with the SAME locked preset applied + window/highlight tame. High-quality PNG, style-matched to the set. |
| listing_consistency_previews | preview | asset_preview_file display of all three finished frames so the agency can confirm one consistent style across the property before the remaining 20-40 frames are run. |

**Layer-3 verifier checks** — expert-authored (16 checks, 3 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| Three finished image deliverables are returned, one per frame | auto · mandatory · K1 | Exactly three finished output image files exist, named/derived as exterior_hero_MLS.png, interior_living_room_MLS.png, and interior_kitchen_MLS.png (one per attached frame) |
| All three finished frames are delivered as PNG files | auto · **dealbreaker** · K1 | Each of the three deliverables (exterior_hero_MLS, interior_living_room_MLS, interior_kitchen_MLS) is a valid PNG (PNG file signature), not JPEG/WebP/other — the brief requires 'high-quality PNG' |
| A consistency preview of all three finished frames is shown for sign-off | auto · mandatory · K1 | An asset_preview_file step (output named listing_consistency_previews) is produced that displays all three finished frames (exterior_hero_MLS, interior_living_room_MLS, interior_kitchen_MLS) together so the agency can confirm one consistent style before the rest of the 20-40 |
| The exterior hero is auto-straightened then cropped to clean bounds before tonal edits | auto · mandatory · K6 | The exterior pipeline runs image_auto_straighten (step 2) then image_crop_to_bounds (step 3), in that order, before image_apply_auto_tone — and in exterior_hero_MLS.png the leaning verticals/tilted horizon of exterior_hero_wideDR.png are corrected and the skewed edges removed |
| Base tonal recovery (auto-tone) is applied to the exterior so the shaded facade reads | auto · mandatory · K6 | image_apply_auto_tone (step 4) is applied to the cropped exterior frame as the tonal base before the masked window/sky/lawn edits |
| Window pull: the bright front windows are masked and their highlights pulled down | expert · mandatory · K3 | In exterior_hero_MLS.png the previously blown-out front windows show recovered detail/structure rather than pure white, produced via image_select_by_prompt (windows) -> image_adjust_highlights with that mask |
| Sky is ENHANCED, not replaced | expert · **dealbreaker** · K7 | The original sky from exterior_hero_wideDR.png is retained in exterior_hero_MLS.png with recovered highlights and a deeper blue (via image_select_by_prompt sky -> masked image_adjust_single_color_saturation); no new/foreign sky is composited or swapped in |
| Lawn enhancement: the front lawn/grass is masked and its green lifted | expert · mandatory · K3 | In exterior_hero_MLS.png the front lawn shows increased green saturation and luminance (healthier/greener) vs the source, applied within a lawn mask via image_select_by_prompt -> image_adjust_hsl, without recoloring non-lawn areas |
| Exterior white balance is warmed slightly and a touch of vibrance added | expert · quality · K4 | exterior_hero_MLS.png shows a slightly warmer white balance and modestly increased vibrance vs the auto-toned exterior (via image_adjust_color_temperature + image_adjust_vibrance_and_saturation), reading bright and welcoming without over-saturation |
| The Lightroom preset library is pulled before any preset is applied | auto · mandatory · K6 | image_list_presets (step 13) is called to retrieve the preset catalog prior to any image_apply_preset call |
| The SAME locked bright-and-airy preset is applied to all three frames | auto · mandatory · K1 | image_apply_preset is invoked on the exterior hero (step 14), the living-room interior (step 16), and the kitchen interior (step 19) using one identical preset identifier selected from the catalog (same preset across all three apply calls) |
| Both interior frames receive a window/highlight tame after the preset | expert · mandatory · K3 | In interior_living_room_MLS.png and interior_kitchen_MLS.png the bright/near-blown windows are tamed (highlights recovered via image_adjust_highlights applied after the preset) so the windows are not blown and the rooms read open |
| The three finished frames share one consistent bright-and-airy property style | expert · mandatory · K4 | exterior_hero_MLS.png, interior_living_room_MLS.png and interior_kitchen_MLS.png look like one cohesive set (consistent tone, brightness and color cast from the shared locked preset) — a uniform bright-and-airy MLS-ready look across the property |
| No object removal or other generative cleanup was performed | expert · **dealbreaker** · K7 | The finished frames contain the same physical objects/scene as their sources; 'general cleanup' was delivered as tonal/color + straighten/crop only, with no AI object removal, no gen-fill, and no compositing |
| Masked exterior edits stay within their target regions | expert · quality · K3 | The window, sky, and lawn adjustments on exterior_hero_MLS.png are confined to their respective masked regions with clean edges (no halo/spill of the highlight pull, blue boost, or green lift onto adjacent areas) |
| Honest capability substitutions are disclosed to the client | expert · mandatory · K7 | The delivery message flags that the sky was enhanced (not swapped/replaced), that the HDR look came from single-file tone-mapping (auto-tone + highlight/shadow recovery) rather than a true bracket MERGE, and that 'general cleanup' excluded object removal — matching the spec's stated MLS-safe substitutions |


[[PAGEBREAK]]
### AO-27 · Streetline-style real-estate interior edit: straighten, HDR-look tone, white balance, window pull, outlet clean-up
**Brand:** Real Estate, Construction & Property &nbsp;·&nbsp; **Operation:** O4 Preset retouch & look-dev (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (19 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K2 · K1 · K6 · K7
*Edit a Dutch real-estate interior to a bright, clean, realistic Streetline-style finish — straighten verticals, recover an HDR-look exposure, fix white balance, pull the blown-out window view back, neutralize one distracting wall outlet, and deliver a high-res JPG.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| hero_livingroom_interior.jpg | image | Photoreal real-estate listing photo of an empty modern Dutch living room shot on a wide-angle lens at chest he |
| window_bracket_reference.jpg | image | The SAME Dutch living-room scene and identical camera position as the hero frame, but exposed about two stops |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| livingroom_streetline_final.jpg | image | High-resolution JPG (3:2, full sensor resolution preserved, sRGB), Streetline-style finish: straightened verticals, cropped clean (no rotation wedge), bright-but-realisti |
| livingroom_streetline_final_preview | image | Inline web preview (bounded JPEG/PNG render) of the finalized image for in-chat client sign-off before batch roll-out. |

**Layer-3 verifier checks** — expert-authored (16 checks, 4 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| Final deliverable livingroom_streetline_final.jpg is a valid JPG file | auto · **dealbreaker** · K1 | livingroom_streetline_final.jpg is a valid JPEG (magic bytes FF D8 FF, extension .jpg, MIME image/jpeg) |
| Final JPG is encoded in sRGB / RGB color space (not CMYK) | auto · **dealbreaker** · K1 | livingroom_streetline_final.jpg channel mode is RGB and its embedded/assumed color profile is sRGB, not CMYK or another profile, per the output spec 'sRGB' |
| Final JPG preserves a 3:2 aspect ratio at full hero resolution (no downscaling) | auto · mandatory · K1 | Width:height of livingroom_streetline_final.jpg equals 3:2 within rounding, and its pixel dimensions equal the supplied hero_livingroom_interior.jpg full resolution (allowing only the straighten/crop reduction), with no additional downscaling |
| An inline web preview of the finalized image is produced for client sign-off | auto · mandatory · K1 | livingroom_streetline_final_preview exists as a bounded inline JPEG/PNG render derived from livingroom_streetline_final.jpg (asset_inline_preview output present) |
| Vertical wall lines in the final image read straight (tilt corrected) | expert · mandatory · K3 | Wall verticals appear plumb/upright in livingroom_streetline_final.jpg; the few-degree input tilt from hero_livingroom_interior.jpg is removed so walls read straight |
| The image is cropped to clean rectangular bounds with no rotation wedge | expert · mandatory · K3 | No transparent/black triangular wedge or skewed corner from the straighten step is visible in livingroom_streetline_final.jpg; the frame is a clean rectangle |
| Interior is bright but realistic with lifted shadows and tamed highlights, no unrealistic HDR look | expert · mandatory · K4 | Dark portions of the room are lifted and global highlights pulled back so the interior reads bright yet natural, with no HDR halo, crunch, or oversaturated HDR artifacts, per the brief 'bright but realistic interiors' and 'No oversaturated colors or unrealistic HDR effects' |
| White balance is corrected so the warm/tungsten cast is neutralized | expert · mandatory · K4 | The slightly-warm input cast is neutralized; the white plaster walls read neutral white rather than warm/yellow in livingroom_streetline_final.jpg, per the brief 'Color correction and white balance adjustment' / 'Natural-looking colors' |
| Colors are natural with only a gentle vibrance lift, not oversaturated | expert · mandatory · K4 | Colors read natural with only a gentle vibrance lift and no saturation push; no oversaturated greens/colors, consistent with the brief 'No oversaturated colors' |
| The blown-out left garden windows are pulled so the exterior view reads through the glass | expert · mandatory · K4 | The previously near-white left-hand windows now show the outdoor view (green Dutch garden, wooden fence, grey sky) through the glass, matching the exterior in window_bracket_reference.jpg, with highlights and exposure pulled down on the window region |
| The window pull is selective and does not darken the surrounding interior | expert · quality · K3 | Exposure/highlight reduction is confined to the window mask; the rest of the bright interior is unaffected, with no obvious masking halo at the window edges |
| The small white wall power outlet is neutralized to the wall color | expert · mandatory · K3 | The distracting small white double outlet low on the right-hand wall is filled to match the surrounding wall color and no longer reads as a distractor in livingroom_streetline_final.jpg |
| The outlet clean-up is a solid-color fill, not AI object removal or generative compositing | expert · **dealbreaker** · K7 | The cleaned outlet area is a flat solid wall-matched fill (image_fill_area), with no synthesized texture, generative content, or composite artifacts |
| Only connector-legal Adobe tools are used; no HDR-merge, generative-fill, AI object removal, compositing, upscaling, or Express/Canva tools appear | auto · **dealbreaker** · K7 | The executed tool set is a subset of the spec tools_used (asset_initialize_file_upload, asset_finalize_file_upload, image_auto_straighten, image_crop_to_bounds, image_apply_auto_tone, image_adjust_dark_portions, image_adjust_highlights, image_adjust_color_temperature, image_adjust_vibrance_and_saturation, image_select_by_prompt, image_adjust_exposure, image_fill_area, image_apply_preset, asset_inline_preview); no true multi-bracket HDR-merge, generative-fill, AI-removal, compositing, upscaling, or Express/Canva tool is present |
| A single consistent realistic interior preset is applied as a repeatable batch look | expert · quality · K4 | A neutral bright-clean look (image_apply_preset) is applied that reads as a realistic Streetline-style finish suitable to loop across the remaining 24-29 images, not a heavy stylized filter |
| Overall finish matches the Streetline reference: bright, clean, realistic, professional | expert · quality · K4 | Final master reads as bright, clean, realistic, and professional per the brief's style bar 'similar to Streetline: bright, clean, realistic, and professional', with straightened verticals, neutral white balance, intact through-window exterior view, and cleaned outlet all cohering into one believable real-estate listing photo |


[[PAGEBREAK]]
### AO-29 · Continental 2026 Cup Stars Poster — Cinematic Grade, Flag-Colour Accents & Print/Web Master Delivery
**Brand:** General / Cross-Industry Branding & Graphics &nbsp;·&nbsp; **Operation:** O1 Tonal grade & restore (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (23 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Take the client's supplied composited Continental-stars hero plate (Messi/Ronaldo/Mbappé + trophy already arranged) plus player cut-out and flag-pattern layers, and finish it into a cinematic, high-contrast, flag-colour-accented A2 300-dpi print master plus social-media versions using only Adobe connector tools.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| continental_hero_plate_composited.jpg | image | Photoreal 5000x7000 vertical poster hero plate, night football stadium under bright floodlights, three profess |
| player_left_cutout.png | image | Single male footballer in a light sky-blue and white generic kit, full body action pose, isolated on transpare |
| player_centre_cutout.png | image | Single male footballer in a red and dark-green generic kit, heroic standing pose, isolated on transparent back |
| player_right_cutout.png | image | Single male footballer in a blue, white and red generic kit, sprinting pose, isolated on transparent backgroun |
| flag_pattern_swatch.png | image | Seamless tileable abstract woven-fabric pattern blending soft diagonal bands of sky-blue and white, red and fo |
| continental_poster_A2_master.indd | pdf | Describe a genuine single-page A2 (420x594mm) InDesign layout document containing one full-bleed image frame s |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| continental_poster_print_master_A2.pdf | pdf | A2 (420×594 mm) press-ready PDF at ≥300 dpi, exported from the authored .indd with the fully graded full-bleed poster placed; flattened, CMYK-intent print master. |
| continental_poster_print_master_A2.tiff | image | Flattened high-resolution TIFF of the finished graded A2 poster (≥4960×7016 px ≈ A2@300dpi) — the deliverable flattened master named in the brief. |
| continental_poster_social_1x1.jpg | image | 1080×1080 1:1 Instagram-feed crop of the graded poster, subject-aware crop keeping all three figures + trophy, same grade. |
| continental_poster_social_9x16.jpg | image | 1080×1920 9:16 story/reel crop of the graded poster, same cinematic grade. |
| flag_accent.svg | vector | Clean vectorised SVG of the flag-pattern swatch for reuse across the studio kit (scalable, no raster). |
| continental_review_board | data | Firefly board deep-link assembling the graded hero, the per-player accent-graded stills and the social crops for client look-review before sign-off. |

**Layer-3 verifier checks** — expert-authored (16 checks, 3 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| Print master PDF is delivered at A2 page size (420×594 mm) | auto · mandatory · K1 | continental_poster_print_master_A2.pdf exists and its page/trim box measures A2 = 420×594 mm portrait within ±1 mm |
| Print master PDF resolution is at least 300 dpi | auto · mandatory · K1 | The placed full-bleed image in continental_poster_print_master_A2.pdf resolves to ≥300 dpi at A2 (effective raster ≥4960×7016 px) |
| Print master PDF is a flattened, CMYK-intent press-ready master | auto · **dealbreaker** · K1 | continental_poster_print_master_A2.pdf is single-page, flattened, and carries CMYK output intent / colour space (not RGB-only) |
| Flattened TIFF print master is delivered at A2 300-dpi pixel dimensions | auto · mandatory · K1 | continental_poster_print_master_A2.tiff exists, is a flattened TIFF, and measures ≥4960×7016 px (≈A2 at 300 dpi) |
| 1:1 Instagram-feed social crop is delivered at exact dimensions | auto · mandatory · K1 | continental_poster_social_1x1.jpg exists and is exactly 1080×1080 px JPEG |
| 9:16 story/reel social crop is delivered at exact dimensions | auto · mandatory · K1 | continental_poster_social_9x16.jpg exists and is exactly 1080×1920 px JPEG |
| Flag-accent asset is delivered as a true scalable vector SVG | auto · mandatory · K1 | flag_accent.svg exists, is a valid SVG containing vector <path>/shape geometry, and embeds no raster image data |
| A Firefly review board deep-link is delivered assembling the graded master, the three per-player accent stills and the two social crops | auto · mandatory · K6 | continental_review_board is a resolvable Firefly board deep-link that assembles the graded A2 master/hero, the three per-player accent stills (left/centre/right) and the two social crops (1:1 and 9:16) for client sign-off |
| The 1:1 social crop is subject-aware and keeps all three figures plus the trophy | expert · mandatory · K3 | In continental_poster_social_1x1.jpg all three footballer figures and the Continental Cup trophy remain fully visible and uncropped at the edges |
| A consistent high-contrast cinematic 'stadium floodlights at night' grade is applied and carried across every deliverable | expert · mandatory · K4 | The graded master shows punchy high contrast with figures carving out of dark stadium shadows, warm floodlit highlights and cooled shadows, and the SAME grade is visibly carried into the TIFF, the PDF print master and both social crops (1:1 and 9:16) |
| Per-player flag-colour accents are integrated with the correct palette for each figure | expert · mandatory · K4 | Left figure reads sky-blue (Argentina-style) accent, centre figure reads red/green (Portugal-style) accent, right figure reads blue/white/red (France-style) accent, appearing as rim-light/energy streaks rather than flat fills |
| Flag colours are woven in tastefully with NO literal flags or national emblems | expert · **dealbreaker** · K2 | No recognisable national flag, crest or emblem appears anywhere in the poster deliverables or in flag_accent.svg; colour accents read only as lighting/energy/graphic texture |
| Believable night atmosphere is added — background haze/floodlight bloom plus fine film grain | expert · quality · K3 | The deep background shows gentle atmospheric haze / floodlight bloom and the frame carries fine organic film grain so it prints organically rather than digitally clean, ideally without softening the three figures and trophy |
| The vectorised flag accent faithfully reproduces the supplied flag-pattern swatch with clean paths | expert · quality · K3 | flag_accent.svg cleanly reproduces the woven sky-blue/white, red/green, blue-white-red bands of flag_pattern_swatch.png with smooth vector paths and no tracing artefacts |
| Player likenesses, scene composition and the trophy come only from the client-supplied plates, not regenerated | expert · **dealbreaker** · K7 | The figures, trophy and night-stadium arrangement in all deliverables match the supplied hero plate, with no faces, trophy, or scene content invented or altered by generative tools beyond the A2 bleed outpaint |
| Generative expand is used only to extend the canvas to A2 bleed, not to add subject content | expert · quality · K7 | Generatively expanded margins appear only as background/bleed extension around the original framing; no new figures, trophy or subject content are introduced inside or around the original plate area |


[[PAGEBREAK]]
### AO-30 · Daily Promo Spot — Color-Graded Key Frames, Thumbnail Pack, Cleaned VO & Sizzle Reel
**Brand:** Music, Film, Publishing & Media &nbsp;·&nbsp; **Operation:** O1 Tonal grade & restore (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (19 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Take today's exported promo key frames + the provided voice-over, apply one consistent lively color grade across the frames, build a YouTube thumbnail from the hero shot, source a royalty-free music bed, clean the VO, generate a sizzle cut and a content summary, and drop the finished, organized package back in the daily folder — same day.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| keyframe_hero_closeup.jpg | image | Photoreal still frame exported from a promotional video: candid close-up of a mid-30s small-business owner lau |
| keyframe_mid_A.jpg | image | Photoreal 1920x1080 video key frame: medium shot of the same coffee-roastery owner pouring beans from a scoop, |
| keyframe_mid_B.jpg | image | Photoreal 1920x1080 video key frame: medium shot of two staff members chatting over a roasting machine in the |
| keyframe_wide_environment.jpg | image | Photoreal 1920x1080 video key frame: wide environment shot of the artisan coffee roastery interior with custom |
| keyframe_product_detail.jpg | image | Photoreal 1920x1080 video key frame: macro detail of a finished latte with rosetta art on a wooden counter in |
| voiceover_raw.wav | audio | Warm, friendly female narrator, ~20 seconds, upbeat-accessible read: 'Every cup tells a story. Roasted fresh, |
| source_clips_for_sizzle.mp4 | video | 1080p promotional b-roll montage of the same artisan coffee roastery: beans pouring, espresso pulling, latte a |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| graded_keyframes/ (5 files) | image | 5x 1920x1080 JPEG/PNG, each carrying the identical grade chain (auto-tone → warmer temperature → lifted shadows → recovered highlights → +vibrance → same Lightroom look-p |
| youtube_thumbnail_1920x1080.png | image | 1920x1080 (16:9) PNG thumbnail from the graded hero frame: subject popped via blurred background, cropped with subject weighted left, title-safe negative space on the rig |
| music_bed_licensed.{wav/mp3} | audio | Full-resolution LICENSED Adobe Stock royalty-free track (upbeat/accessible), delivered via presigned download URL after licensing. |
| voiceover_clean.wav | audio | Denoised/de-hissed version of the provided voice-over, voice-only, ready to balance into the mix. |
| sizzle_15s_teaser.mp4 | video | ~15s AI engagement-cut sizzle reel assembled from the source clips for the social teaser (async-widget result in product). |
| content_summary.txt | data | Short auto-generated scene/transcript summary of the source montage to seed the post caption + description. |
| daily_delivery_YYYY-MM-DD/ | data | Dated CC asset folder containing all of the above, organized for same-day handback. |

**Layer-3 verifier checks** — expert-authored (16 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| The graded_keyframes deliverable contains exactly 5 image files | auto · mandatory · K1 | graded_keyframes/ folder holds exactly 5 files — one graded version each of keyframe_hero_closeup, keyframe_mid_A, keyframe_mid_B, keyframe_wide_environment, and keyframe_product_detail |
| Each graded key frame is exactly 1920x1080 in JPEG or PNG format | auto · mandatory · K1 | all 5 graded frames measure exactly 1920x1080 px and are JPEG or PNG |
| All 5 key frames carry one visually consistent 'edited-together' grade | expert · mandatory · K3 | the same grade recipe (auto-tone baseline, warmer temperature, lifted shadows, controlled highlights, +vibrance, and the same Lightroom look-preset) reads as applied identically across all 5 frames so the set looks edited together, lively-but-tasteful and 'accessible, not corporate' |
| The grade visibly corrects the cool/uneven afternoon cast toward warm with recovered tone | expert · quality · K4 | graded frames read warmer than the supplied cool/uneven inputs, with lifted shadow detail and recovered (non-blown) window highlights |
| The YouTube thumbnail file is exactly 1920x1080 PNG | auto · mandatory · K1 | youtube_thumbnail_1920x1080.png measures exactly 1920x1080 px (16:9) and is PNG format |
| The thumbnail is built from the graded hero frame, not an ungraded or different frame | expert · mandatory · K2 | the thumbnail subject and scene match the graded keyframe_hero_closeup (laughing mid-30s coffee-roastery owner) carrying the same applied grade |
| The thumbnail pops the subject via a blurred background while the subject stays sharp | expert · mandatory · K3 | the busy shelf/equipment background is blurred and the business-owner subject remains sharp, with clean subject-pop edge quality |
| The thumbnail crop weights the subject left with title-safe negative space on the right | expert · quality · K3 | the subject is positioned in the left portion of the 16:9 frame leaving clear title-safe empty space on the right |
| The music bed is a licensed Adobe Stock royalty-free track delivered as a full-resolution file | auto · **dealbreaker** · K1 | music_bed_licensed is a full-resolution LICENSED Adobe Stock royalty-free file in WAV or MP3 format delivered via presigned download URL, not a watermarked/comp preview |
| The licensed music bed reads as upbeat and accessible | expert · quality · K4 | the selected track reads as upbeat and accessible, fitting the friendly, non-corporate spot |
| voiceover_clean.wav is a denoised/de-hissed version of the supplied voice-over | expert · mandatory · K1 | voiceover_clean.wav is voice-only with the room tone and tape hiss from voiceover_raw.wav removed and the narration intact and clean |
| The sizzle teaser is an approximately 15-second cut assembled from the source clips | auto · mandatory · K1 | sizzle_15s_teaser.mp4 duration is approximately 15 seconds and is an AI engagement-cut derived from source_clips_for_sizzle.mp4 |
| content_summary.txt is a text summary of the source montage to seed post copy | auto · mandatory · K1 | content_summary.txt exists as a text file containing a scene/transcript summary of source_clips_for_sizzle.mp4 usable as caption/description copy |
| A dated daily-delivery folder named with a YYYY-MM-DD date exists in CC | auto · mandatory · K6 | a CC asset folder named daily_delivery_YYYY-MM-DD/ (with an actual date) exists |
| The dated folder contains every deliverable for same-day handback | auto · mandatory · K6 | daily_delivery_YYYY-MM-DD/ contains the 5 graded key frames, youtube_thumbnail_1920x1080.png, the licensed music bed, voiceover_clean.wav, sizzle_15s_teaser.mp4, and content_summary.txt |
| No client key-frame is regenerated or replaced — only graded versions of the supplied frames are delivered | expert · **dealbreaker** · K7 | each delivered graded frame is the same subject/scene as its corresponding supplied input frame (no synthesized, generated, or substituted imagery) |


[[PAGEBREAK]]
### AO-31 · Daily-vlog brand kit: color-graded thumbnails, end-screen + lower-third plates, story-format still, reframed clip and cleaned VO
**Brand:** Music, Film, Publishing & Media &nbsp;·&nbsp; **Operation:** O1 Tonal grade & restore (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (18 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Build the recurring per-episode still brand kit for a daily-life vlog — color-grade the supplied frame-grab and shot stills to one consistent "personal, upbeat" look, produce a subject-pop YouTube thumbnail plus a 9:16 story-format still, vectorize the channel wordmark into clean lower-third and end-screen plates, gather it all on a Firefly board, and ship a same-length social reframe of one clip with a denoised voice-over.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| hero_framegrab_4k.png | image | Photoreal 4K frame grab from a casual daily-life vlog: a 28-year-old male creator sitting at a cluttered home |
| creator_dslr_shot.png | image | Photoreal DSLR portrait of the SAME 28-year-old male creator for a YouTube thumbnail: three-quarter framing, a |
| channel_wordmark.png | image | Flat 2D channel logo lockup on transparent background: the wordmark 'PRINCERRR' in a bold rounded geometric sa |
| hero_clip_12s_4k.mp4 | video | 12-second handheld 4K horizontal vlog clip, 1080p+ native audio: the same male creator walking-and-talking to |
| vo_scratch_track.wav | audio | One-take casual male voice-over intro for a daily vlog, conversational upbeat tone: 'Hey everyone, welcome bac |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| framegrab_graded.png | image | Color-graded hero frame-grab, house look (warm WB, lifted shadows, controlled highlights, lively vibrance, finishing preset stamped), full-res PNG. |
| dslr_shot_graded.png | image | DSLR thumbnail still with the SAME finishing preset applied so it matches the frame-grab grade, full-res PNG. |
| thumbnail_1280x720.png | image | YouTube thumbnail, 1280x720 16:9, creator subject popped against a desaturated background. |
| story_still_1080x1920.png | image | Vertical story / Shorts cover still, 1080x1920 9:16, canvas outpainted top+bottom from the thumbnail (no re-shoot). |
| channel_mark.svg | vector | Channel wordmark vectorized to a clean scalable SVG for lower-thirds and end screen. |
| brand_kit_board | url | Firefly board deep-link gathering the two graded stills, thumbnail, story still and vector mark as the episode brand-kit handoff. |
| hero_clip_vertical_9x16.mp4 | video | Hero clip reframed to 1080x1920 9:16, SAME length as source (no trim, no format change). (async) |
| vo_cleaned.wav | audio | Denoised / de-reverbed voice-over scratch track, broadcast-usable. (async) |

**Layer-3 verifier checks** — expert-authored (17 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| framegrab_graded.png is delivered as a full-resolution PNG retaining the 3840x2160 source frame dimensions | auto · mandatory · K1 | A file named framegrab_graded.png exists, decodes as a valid PNG, and measures exactly 3840x2160 (the source hero_framegrab_4k.png resolution) rather than a downscaled or cropped image |
| The graded frame-grab applies the house color-grade versus the flat ungraded source (warmer WB, lifted shadows, controlled highlights, lively vibrance) | expert · mandatory · K4 | Compared to hero_framegrab_4k.png, framegrab_graded.png reads visibly warmer (the cool/green video cast removed), shadows lifted to open desk detail, window highlights tamed not blown, and vibrance pushed for a lively-but-not-garish 'personal, upbeat' look |
| dslr_shot_graded.png is delivered as a full-resolution PNG corresponding to creator_dslr_shot.png | auto · mandatory · K1 | A file named dslr_shot_graded.png exists, decodes as a valid PNG, and retains the full source resolution of creator_dslr_shot.png (6000x4000) rather than a downscaled or cropped image |
| The graded DSLR still wears the SAME finishing preset as the frame-grab so the two stills read as one consistent channel grade | expert · mandatory · K4 | dslr_shot_graded.png's color tone/look visibly matches framegrab_graded.png (same finishing preset stamped) so the two read as the same house grade, satisfying the brief's 'every episode looks like the same channel' consistency requirement |
| thumbnail_1280x720.png is exactly 1280x720 pixels (16:9) | auto · mandatory · K1 | Image dimensions read exactly 1280 wide by 720 high (16:9 aspect ratio) |
| In the thumbnail the creator subject is popped against a desaturated background | expert · mandatory · K3 | The creator (subject) retains full color/saturation while the busy background's saturation is visibly knocked down to make the subject pop; the subject itself is NOT desaturated |
| story_still_1080x1920.png is exactly 1080x1920 pixels (9:16) | auto · mandatory · K1 | Image dimensions read exactly 1080 wide by 1920 high (9:16 vertical aspect ratio) |
| The 9:16 story still was produced by outpainting the thumbnail canvas top and bottom, not by re-shooting or stretching | expert · mandatory · K3 | The central content of thumbnail_1280x720.png is preserved undistorted, with new plausible image content generatively added above and below to fill the vertical canvas (no horizontal stretch, no new/different subject, no re-shoot) |
| channel_mark.svg is delivered as a valid scalable SVG vector (not an embedded raster) | auto · mandatory · K1 | A file named channel_mark.svg exists and parses as valid SVG containing vector path/shape elements, not merely a raster bitmap embedded in an SVG wrapper |
| The vectorized channel mark faithfully reproduces the supplied wordmark lockup (PRINCERRR text, 'daily life, unfiltered' tagline, play glyph, brand colors) with clean letterforms | expert · **dealbreaker** · K2 | channel_mark.svg renders the 'PRINCERRR' wordmark with the 'daily life, unfiltered' tagline, the play-button glyph, and the deep-teal and warm-coral brand colors, with crisp clean edges and legible correctly-spelled text matching channel_wordmark.png; the logo is vectorized, not regenerated or altered |
| A Firefly board deep-link is delivered as the brand-kit handoff | auto · mandatory · K1 | brand_kit_board is a resolvable Firefly board deep-link URL that opens a board |
| The Firefly board gathers all five required brand-kit assets | expert · mandatory · K6 | The board displays exactly the five still/vector deliverables: framegrab_graded.png, dslr_shot_graded.png, the 1280x720 thumbnail, the 1080x1920 story still, and channel_mark.svg (all five present) |
| hero_clip_vertical_9x16.mp4 is a 1080x1920 MP4 of the SAME length as the ~12s source hero clip (no trim, no format change) | auto · mandatory · K1 | Output is an MP4 with frame dimensions 1080x1920 and duration equal to the ~12s source hero_clip_12s_4k.mp4 (no shortening, still an MP4 video) |
| The vertical hero clip is a meaningful reframe of the horizontal source keeping the speaking creator in frame | expert · quality · K3 | The 9:16 output crops/repositions the 16:9 hero content so the creator stays framed across the clip (subject not cut off), not a letterboxed or stretched fill |
| vo_cleaned.wav is delivered as a WAV corresponding to the scratch voice-over with the same spoken intro | auto · mandatory · K1 | A WAV file vo_cleaned.wav exists corresponding to vo_scratch_track.wav, carrying the same spoken intro content |
| The cleaned voice-over has the room reverb, HVAC hum and broadband hiss removed so the voice is broadcast-usable | expert · mandatory · K4 | Compared to vo_scratch_track.wav, vo_cleaned.wav has audibly reduced room reverb, hum and broadband hiss, the spoken line stays intelligible and broadcast-usable, and no new artifacts mangle the voice |
| No banned/out-of-scope capability was used and only the single allowed generative outpaint was performed | expert · **dealbreaker** · K7 | Outputs show no video timeline trimming/jump-cuts, no .srt captions or NLE project file, no background-replace-by-prompt, no object removal, no upscaling, and no layout composition; the only generative step is the top+bottom outpaint of the story still, and the channel mark is a faithful vectorization (not a regenerated or altered logo) |


[[PAGEBREAK]]
### AO-32 · Modern House Listing Photography — Post-Production Color Grade & Listing Export
**Brand:** Photo Editing, Retouching & Restoration &nbsp;·&nbsp; **Operation:** O1 Tonal grade & restore (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (25 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Edit the client's three supplied room frames (living room, kitchen, bedroom) into clean, modern, naturally-lit real-estate listing photos with straight verticals and corrected color, then export each in web-optimized JPEG (<2 MB) and full-resolution TIFF for Airbnb/Zillow.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| living_room_raw.jpg | image | Photoreal wide-angle interior photo of a modern rental living room shot handheld at 7am in natural light, slig |
| kitchen_raw.jpg | image | Photoreal wide-angle interior photo of a modern rental kitchen shot handheld at morning, slightly tilted (abou |
| bedroom_raw.jpg | image | Photoreal wide-angle interior photo of a modern rental bedroom shot handheld in early-morning natural light, s |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| living_room_web.jpg | image | Web-optimized JPEG, longest edge ~2048px, sRGB, quality tuned to keep file under 2 MB; straight verticals, color-corrected, shadow-lifted, scuff/dust spotted, gentle mode |
| living_room_full.tif | image | Full-resolution TIFF (native capture resolution), same corrected/graded pixels as the web version, for print/archive delivery. |
| kitchen_web.jpg | image | Web-optimized JPEG under 2 MB, ~2048px long edge, sRGB; straightened, white-balanced, highlight-recovered, scuff-spotted kitchen frame. |
| kitchen_full.tif | image | Full-resolution TIFF of the corrected kitchen frame for full-quality listing/print use. |
| bedroom_web.jpg | image | Web-optimized JPEG under 2 MB, ~2048px long edge, sRGB; straightened, exposure-balanced (window highlights recovered, interior brightened), spotted bedroom frame. |
| bedroom_full.tif | image | Full-resolution TIFF of the corrected bedroom frame. |
| listing_review_board | data | Firefly Board deep-link assembling the three corrected listing shots (living room, kitchen, bedroom) for one-glance client review before download. |

**Layer-3 verifier checks** — expert-authored (16 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All three room frames are delivered in BOTH web-optimized JPEG and full-resolution TIFF (6 image files total: living_room_web.jpg, living_room_full.tif, kitchen_web.jpg, kitchen_full.tif, bedroom_web.jpg, bedroom_full.tif). | auto · mandatory · K1 | Exactly 6 image deliverables present, one .jpg + one .tif per room: living_room_web.jpg, living_room_full.tif, kitchen_web.jpg, kitchen_full.tif, bedroom_web.jpg, bedroom_full.tif; any missing file fails. |
| Each of the three web JPEG files is under 2 MB. | auto · **dealbreaker** · K1 | File size of living_room_web.jpg, kitchen_web.jpg, and bedroom_web.jpg is each < 2,097,152 bytes (2 MB); any file >= 2 MB fails. |
| Each web deliverable is a valid JPEG container with longest edge approximately 2048px. | auto · mandatory · K1 | living_room_web.jpg, kitchen_web.jpg, bedroom_web.jpg each decode as JPEG and have a longest-edge dimension of ~2048px (tolerance 1900-2200px); wrong format or out-of-range dimension fails. |
| Each full-resolution deliverable is a valid TIFF at native capture resolution, larger than its ~2048px web JPEG counterpart. | auto · mandatory · K1 | living_room_full.tif, kitchen_full.tif, bedroom_full.tif each decode as a valid TIFF container whose longest edge exceeds 2048px (native/full resolution, not the resized web size); any that is not a TIFF or is <=2048px long edge fails. |
| Each web JPEG is encoded in the sRGB color space. | auto · quality · K1 | Embedded color profile / metadata of living_room_web.jpg, kitchen_web.jpg, and bedroom_web.jpg reports sRGB; a non-sRGB color space fails. |
| For each room, the full-res TIFF and the web JPEG are the same edited/graded master differing only in resolution (the web file is a resized version, not a separate edit). | expert · mandatory · K1 | For each room the .tif and .jpg show identical corrections (same straighten, crop, color/white-balance, exposure, spot-fix, grade), differing only in pixel dimensions; a visible mismatch in edit state between the two formats fails. |
| A Firefly Board deep-link (listing_review_board) is delivered that assembles all three corrected room masters (living room, kitchen, bedroom) for one-glance client review. | auto · mandatory · K6 | listing_review_board is present as a Firefly Board URL/deep-link and references/contains the three corrected room shots (living room, kitchen, bedroom); a missing board or fewer than three shots fails. |
| Every room frame has straightened, level verticals correcting the input tilt (~2.5deg living room, ~2deg kitchen, ~3deg bedroom). | expert · mandatory · K3 | Vertical wall, cabinet, and window-frame lines read level/straight in all three outputs versus the visibly tilted inputs; noticeable residual tilt in any room fails. |
| Each straightened frame is cropped to a clean rectangular frame with no empty wedge/triangle corners left by the rotation. | expert · mandatory · K3 | No transparent/blank/border wedge or triangle is visible at the corners of any of the three outputs; each frame is a full distortion-free rectangle. |
| Mixed warm-tungsten vs cool-daylight white balance is neutralized in the living room and kitchen frames so whites/neutrals read natural. | expert · mandatory · K4 | No strong residual yellow/orange or blue cast remains in living_room or kitchen outputs; pale walls, stainless steel, and quartz read neutral-white. |
| Underexposed shadows are lifted in the living room and bedroom interiors so they read bright and spacious without crushed detail. | expert · mandatory · K4 | Corner/interior shadows in living_room and bedroom outputs show recovered detail and a brighter, open feel versus the dark inputs; fully crushed/blocked blacks fail. |
| Blown-out window/highlight areas are recovered in the kitchen and bedroom frames so highlight detail is held, not clipped. | expert · mandatory · K4 | The bright window in the bedroom output and the can-light/window highlights in the kitchen output show recovered tonal detail rather than pure clipped white. |
| The bedroom interior is selectively brightened via a prompt-based mask while leaving the recovered window untouched (window is not re-blown out). | expert · quality · K3 | Bedroom output shows the room interior opened/brightened while the window retains its recovered highlight detail; a re-blown window or globally flattened brightening fails. |
| Wall/cabinet scuff and dust blemishes are removed in each room via a solid matched-neutral fill (not generative healing) with no visible patch or halo. | expert · mandatory · K3 | The wall scuff/dust by the sofa (living room), cabinet-door scuff (kitchen), and headboard scuff (bedroom) are gone, covered with matched wall/cabinet color and showing no visible smudge, halo, or AI-generated artifact. |
| The final grade is gentle and natural - clean and modern but NOT over-processed/over-saturated. | expert · mandatory · K4 | Outputs show only a subtle vibrance/saturation lift and natural color; no HDR look, over-sharpening, blown saturation, or heavy stylization. An over-processed result fails. |
| No generative AI object-removal, generative fill, compositing, background replacement, or upscaling was used; edits stay within color/tone/geometry/solid-fill corrections. | expert · **dealbreaker** · K7 | Outputs contain no invented/added objects, no synthesized backgrounds, no generatively healed regions; spot-fixes are flat solid-color fills consistent with the brief's 'solid fill only, NOT generative' constraint. Any generative artifact fails. |


[[PAGEBREAK]]
### AO-34 · Informative explainer video: brand-graded sizzle cut, cleaned VO, and on-brand lower-third / call-out graphic plates
**Brand:** Video Editing & Motion Graphics &nbsp;·&nbsp; **Operation:** O1 Tonal grade & restore (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (25 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Turn my raw informative-explainer footage, scratch voiceover, brand logo, and color-reference still into a polished short cut: clean the VO, build a brand-locked color look plus a graded end-card, and produce on-brand lower-third, call-out, and vectorized-logo graphic plates — then deliver a 1080p sizzle and a vertical reframe, all assets organised on a board for the Premiere project.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| raw_explainer_clips_bundle | video | 1080p documentary-style raw footage bundle for a corporate informative explainer: a mid-30s presenter in a mod |
| scratch_voiceover.wav | audio | A warm, conversational male narrator reading ~45s of explainer voiceover script: 'Every day your team loses ho |
| company_logo.png | image | A flat, clean vector-style corporate logo on a transparent background: a stylized geometric hexagon mark besid |
| brand_color_reference.jpg | image | A warm, slightly cinematic interior photograph used as a brand color reference: golden-hour light raking acros |
| endcard_hero_frame.jpg | image | A clean medium-wide hero still suitable for a video end-card: the same presenter and modern office from the fo |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| cleaned_voiceover.wav | audio | Denoised / de-reverbed voiceover track, voice-only, suitable as the edit's narration bed (media_enhance_speech output). |
| sizzle_cut_1080p.mp4 | video | ~60s AI highlight/sizzle cut of the raw clips surfacing the key talking points, 1920x1080 (H.264 target on export). |
| sizzle_cut_vertical_9x16.mp4 | video | 9:16 (1080x1920) reframe of the sizzle cut, SAME length (no trimming), for social teasers. |
| brand_look_reference_frame.jpg | image | One authoritative graded brand-reference frame: straightened, cropped, and run through the full Lightroom-class grade — the locked look the editor matches the master grad |
| logo_vector.svg | vector | Clean vectorized SVG of the company logo for scalable end-card and corner-bug use. |
| lower_third_bar_plate.png | image | Transparent-background lower-third bar plate — solid brand-amber bar region filled via selection-fill, ready to drop on the Premiere timeline. |
| callout_badge_plate.png | image | Transparent-background call-out badge plate — solid brand-color badge region, same selection-fill technique, for on-screen fact call-outs. |
| graded_endcard_frame.jpg | image | End-card hero frame graded to match the locked brand look, with right-side negative space for the logo lockup. |
| northloop_asset_board | data | Firefly board deep-link gathering the graded reference, plates, logo SVG, cleaned VO, and video deliverables as one organised linked-asset set for the Premiere handoff. |

**Layer-3 verifier checks** — expert-authored (16 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All nine deliverables are present: cleaned_voiceover.wav, sizzle_cut_1080p.mp4, sizzle_cut_vertical_9x16.mp4, brand_look_reference_frame.jpg, logo_vector.svg, lower_third_bar_plate.png, callout_badge_plate.png, graded_endcard_frame.jpg, and northloop_asset_board | auto · mandatory · K1 | Exactly these 9 named artifacts exist; missing any one fails the check |
| The horizontal sizzle cut is delivered at 1080p (1920x1080) resolution | auto · mandatory · K1 | sizzle_cut_1080p.mp4 reports 1920x1080 pixel dimensions |
| The sizzle cut is an .mp4 container targeting H.264 video on export | auto · mandatory · K1 | sizzle_cut_1080p.mp4 is an .mp4 file with H.264 video codec |
| The vertical reframe is delivered at 9:16 (1080x1920) portrait dimensions | auto · mandatory · K1 | sizzle_cut_vertical_9x16.mp4 reports 1080x1920 pixel dimensions (9:16 ratio) |
| The vertical reframe is the SAME length as the horizontal sizzle cut with no trimming | auto · mandatory · K1 | Duration of sizzle_cut_vertical_9x16.mp4 equals the duration of sizzle_cut_1080p.mp4 (video_resize must not change length) |
| The sizzle cut is approximately 60 seconds long | auto · quality · K1 | sizzle_cut_1080p.mp4 duration is ~60s (roughly 50-70s) |
| The voiceover is denoised/de-reverbed relative to the supplied noisy scratch_voiceover.wav and remains voice-only with no added music bed | expert · mandatory · K4 | cleaned_voiceover.wav audibly removes the room reverb, low HVAC hum and faint background chatter present in the input and contains only the cleaned voice (no music bed) |
| The brand_look_reference_frame is straightened and cropped (loose headroom removed) versus the deliberately tilted, loosely framed brand_color_reference.jpg input | expert · mandatory · K3 | Reference frame shows a level horizon (no tilt) and tighter framing with the extra headroom removed compared to the input still |
| The brand_look_reference_frame carries the full Lightroom-class grade producing a warm, slightly cinematic amber/teal look | expert · mandatory · K4 | Reference frame is visibly graded toward a warm amber tone with lifted shadows, softened highlights and subtle grain, distinct from the flat input |
| logo_vector.svg is a true vector SVG of the NORTHLOOP logo, not a raster image embedded in an SVG wrapper | auto · mandatory · K1 | logo_vector.svg contains vector path/shape elements (paths, polygons) and contains no embedded raster <image> bitmap of the logo |
| The vectorized logo preserves the supplied NORTHLOOP hexagon mark and wordmark without regenerating or redesigning the client logo | expert · **dealbreaker** · K2 | logo_vector.svg reproduces the supplied geometric hexagon mark and 'NORTHLOOP' wordmark faithfully (same forms, not a redesigned or AI-regenerated logo) |
| lower_third_bar_plate.png is a transparent-background PNG whose bar region is solid-filled with brand-amber #E8A13A | auto · mandatory · K2 | File is a PNG with an alpha (transparent) background and the bar region is solid-filled with #E8A13A |
| callout_badge_plate.png is a transparent-background PNG whose badge region is solid-filled with the deep-navy brand accent color | auto · mandatory · K2 | File is a PNG with an alpha (transparent) background and the badge region is solid-filled with the deep-navy brand accent color (no exact hex specified in the spec) |
| graded_endcard_frame.jpg is graded to match the locked brand-look reference and retains right-side negative space for the logo lockup | expert · mandatory · K4 | End-card frame shows the same warm brand look as brand_look_reference_frame and preserves open negative space on the right for the logo lockup |
| The northloop_asset_board is a Firefly board deep-link gathering all eight produced deliverables (cleaned VO, both video cuts, graded reference, logo SVG, both plates, graded end-card) | auto · mandatory · K6 | Board deep-link resolves and links exactly the 8 produced assets (cleaned_voiceover.wav, sizzle_cut_1080p.mp4, sizzle_cut_vertical_9x16.mp4, brand_look_reference_frame.jpg, logo_vector.svg, lower_third_bar_plate.png, callout_badge_plate.png, graded_endcard_frame.jpg) as one organised set |
| No out-of-scope work is claimed: text/graphics are NOT composited onto the video frames, no generative fill / AI object removal / text-to-image is used, fill_area is solid-color only, and graphics are delivered as standalone transparent plates | expert · **dealbreaker** · K7 | Deliverables contain no text or graphics burned into the video frames, the plates are separate transparent assets, and there are no gen-fill / AI-removal / text-to-image artifacts present |


[[PAGEBREAK]]
### AO-35 · Restore a 1910 magician-troupe postcard: clarify the dark front photo and make the handwritten back legible, delivered as two book/social-ready files
**Brand:** Photo Editing, Retouching & Restoration &nbsp;·&nbsp; **Operation:** O1 Tonal grade & restore (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (18 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K2 · K1 · K6 · K7
*Digitize and restore one 1910 magician-troupe postcard — clarify and lighten the dark sepia front photo and sharpen the contrast of the handwritten back so the description is legible — and deliver each side as its own clean, deskewed, print-and-social-ready file.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| postcard_front_scan_raw.tif | image | A raw flatbed-scanner capture of a genuine 1910 photographic postcard FRONT, sepia/albumen monochrome, showing |
| postcard_back_scan_raw.tif | image | A raw flatbed-scanner capture of the BACK of the same 1910 photographic postcard: a divided-back postcard prin |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| Magician_Postcard_01_FRONT_restored.tif | image | Restored postcard FRONT: deskewed and edge-cropped to the card, dark midtones/shadows recovered, exposure and brightness/contrast lifted, highlights tamed, re-warmed to a |
| Magician_Postcard_01_BACK_legible.tif | image | Restored postcard BACK: deskewed and edge-cropped, brightness/contrast pushed and converted to a clean high-legibility monochrome/sepia so the faint cursive description a |
| restoration_recipe_notes.txt | data | Plain-text log of the exact per-card operation sequence and parameters (straighten angle, crop bounds, tonal adjustments, color temperature shift, preset id, tint) so the |

**Layer-3 verifier checks** — expert-authored (16 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| Two separate restored deliverable files are produced — one for the postcard FRONT and one for the BACK — not a single combined image | auto · **dealbreaker** · K1 | Output set contains exactly two restored master images, one identifiable as the FRONT (Magician_Postcard_01_FRONT_restored.tif) and one as the BACK (Magician_Postcard_01_BACK_legible.tif); FRONT and BACK are separate files, not one combined image |
| Both restored master files are delivered in TIFF format as the print-master deliverable | auto · mandatory · K1 | Both master deliverables are .tif/TIFF files named Magician_Postcard_01_FRONT_restored.tif and Magician_Postcard_01_BACK_legible.tif |
| Each restored master TIFF has a long edge of approximately 3000 px at 300 DPI for the printed book page | auto · mandatory · K1 | FRONT and BACK master TIFFs each have a long-edge dimension of ~3000 px (within ±10% tolerance) and carry 300 DPI resolution metadata |
| A 1080 px JPEG social variant is produced for each side from the same pipeline | auto · mandatory · K1 | Two additional JPEG outputs exist — one FRONT social variant and one BACK social variant — each with a long edge of 1080 px and JPEG format |
| A plain-text restoration recipe log file is delivered | auto · mandatory · K1 | A plain-text file restoration_recipe_notes.txt exists as a deliverable |
| Both sides are deskewed (auto-straightened) so the postcard edges are square, with no residual scanner tilt | expert · mandatory · K3 | The restored FRONT (originally ~4 deg rotated) and BACK (originally ~3 deg rotated) appear straightened — the postcard horizontal/vertical edges read level, not tilted |
| Both sides are edge-cropped to the postcard, removing the gray scanner-bed margin | expert · mandatory · K3 | Neither restored master shows the light-gray scanner-bed margin or edge shadow; the frame is cropped to the postcard edge on both FRONT and BACK |
| The dark FRONT photo is visibly lightened and brightened as the client explicitly asked ('lightened and clear') | expert · mandatory · K4 | The restored FRONT is noticeably brighter and higher in exposure than the dark, low-contrast raw scan; overall the photo reads clearly lighter |
| Crushed shadow detail is recovered on the FRONT where the company stands in stage shadow | expert · quality · K4 | Detail (figures/faces of the company in the dark areas) is visible in the recovered shadow regions of the restored FRONT, not left as solid black |
| The blown bright stage-light highlight on the FRONT is reined in rather than further clipped by the brightening | expert · quality · K4 | The bright stage-light spot retains tonal detail and is not blown out to a larger pure-white region after brightening |
| The cool/greenish scanner cast on the FRONT is neutralized and the image is re-warmed to a consistent archival sepia, preserving period feel (not converted to neutral B&W) | expert · mandatory · K4 | The restored FRONT shows a warm sepia tone with the cool/green cast removed, retaining the vintage period look rather than a neutral grayscale |
| The faint cursive handwriting on the BACK is rendered clearly legible via hard brightness/contrast and a clean monochrome/sepia tint | expert · mandatory · K4 | The cursive description on the restored BACK separates cleanly from the paper and is readable; foxing color noise is suppressed by a monochrome/sepia conversion |
| The original handwritten description text on the BACK is preserved and readable without being altered or rewritten | expert · mandatory · K7 | The restored BACK still shows the original cursive line 'Front row, my mother and Aunt Lillie with the Company at the Royal — Singapore, March 1910' and the 1910 postmark; the wording is not changed, fabricated, or substituted |
| The restoration alters only tone/contrast/color and geometry — no colorization, AI reconstruction, compositing, or upscaling was introduced | expert · **dealbreaker** · K7 | Restored FRONT and BACK remain the same monochrome/sepia photographs as the source content: no added color (colorization), no invented or regenerated image regions, no composited elements, and no resolution upscaling beyond the source |
| The recipe log captures concrete reusable per-card parameter values, not just step names, so the recipe can be re-run on the remaining 23 postcards | expert · mandatory · K6 | restoration_recipe_notes.txt records the actual per-card operation sequence and values used (straighten angle, crop bounds, exposure/brightness/contrast amounts, color-temperature shift, preset id, monochromatic tint) sufficient to reproduce the look on the other cards |
| FRONT and BACK restorations are color-consistent with each other for a cohesive book/social presentation | expert · quality · K3 | The sepia/monochrome tone of the restored FRONT and BACK read as a matched, consistent archival look rather than clashing color treatments |


[[PAGEBREAK]]
### AO-36 · Family Photo Restoration, Tonal Recovery & Canvas Extension for Large-Format Printing
**Brand:** Real Estate, Construction & Property &nbsp;·&nbsp; **Operation:** O1 Tonal grade & restore (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (16 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K2 · K1 · K6 · K7
*Restore one faded family-under-a-maple-tree photo: clip the two corner-intruding fingers out of frame, recover faithful colour/tone without touching faces, outpaint the canopy and scene for a balanced large-format composition, and deliver a print-ready PNG master plus high-res TIFF and a JPG preview.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| family_under_maple_scan.png | image | A scanned vintage family snapshot from roughly the late 1980s, slightly faded and yellow-cast with age, of a r |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| family_restored_master.png | image | Print-ready PNG master: de-skewed, both corner fingers cropped out of frame, auto-toned, neutralized white balance (true-to-original colour), exposure/highlights/shadows |
| family_restored_print.tiff | image | High-resolution TIFF derived locally from the PNG master for professional large-format printing: lossless, RGB, embedded sRGB profile, full resolution. |
| family_restored_preview.jpg | image | Smaller JPG preview derived locally from the PNG master for quick sharing/approval: long edge ~2048px, quality ~85, sRGB. |
| family_restoration_deliverables.zip | data | Single zip bundling the print-ready PNG master, the high-res TIFF, and the JPG preview for client handoff. |

**Layer-3 verifier checks** — expert-authored (16 checks, 3 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All four mandatory deliverables are present: family_restored_master.png, family_restored_print.tiff, family_restored_preview.jpg, and family_restoration_deliverables.zip. | auto · mandatory · K1 | All four exact filenames exist (family_restored_master.png, family_restored_print.tiff, family_restored_preview.jpg, family_restoration_deliverables.zip); family_restoration_deliverables.zip bundles exactly those three image files (PNG master + TIFF + JPG preview). |
| family_restored_master.png is a PNG in RGB color mode with no compression artifacts. | auto · **dealbreaker** · K1 | family_restored_master.png: file format == PNG, color mode == RGB, lossless (no JPEG-style block/compression artifacts). |
| family_restored_print.tiff is a lossless RGB TIFF with an embedded sRGB profile, at the same full resolution as the PNG master. | auto · mandatory · K1 | family_restored_print.tiff: file format == TIFF, compression == lossless, color mode == RGB, an sRGB ICC profile is embedded, and pixel dimensions equal those of family_restored_master.png. |
| family_restored_preview.jpg is an sRGB JPG with long edge ~2048px. | auto · mandatory · K1 | family_restored_preview.jpg: file format == JPG, color space == sRGB, and longest pixel edge is ~2048px (within ~5% tolerance). (JPEG quality target ~85 is a derive parameter, not a reliably readable property, so it is not asserted here.) |
| Both intruding fingers (top-left corner and bottom-right corner) are absent from family_restored_master.png. | expert · **dealbreaker** · K1 | Neither the top-left finger nor the bottom-right finger intrusion is visible anywhere in family_restored_master.png; both of those corners are clean. |
| The two fingers were removed by geometric crop (the opposite corners left the frame), not by clone/heal/generative-fill object removal. | expert · mandatory · K6 | Each finger corner is cropped out of frame (the master's frame edges sit inboard of the original top-left and bottom-right corners); there is no painted, healed, cloned, or AI-rebuilt patch where a finger used to be. |
| No person is cut off or partially clipped by the de-fingering crop. | expert · mandatory · K3 | All four family members (two adults and two children) remain fully within the cropped frame with generous margin; no person is sliced by the crop. |
| Every face, expression, body shape, and apparent age is 100% faithful to the original scan with no alteration. | expert · **dealbreaker** · K2 | Each of the four people's facial features, expression, body shape, and apparent age are identical to the input scan; no generative or identity-altering edit touched the people. |
| Colour/vibrance restoration was applied only to the background via the inverted subject mask, leaving skin/faces untouched. | expert · mandatory · K2 | Saturation/vibrance lift is visible in the background scene (sky, maple tree, landscape) while the people's skin tones match the original; the colour adjustment respected a background-only (inverted-subject) mask. |
| The aged yellow/warm cast is neutralized so colours read true to the original. | expert · mandatory · K4 | The overall yellow/warm age cast is removed; whites/neutrals read neutral and colours are faithful to the original scene rather than orange/yellow-tinted. |
| Fade is recovered through tonal correction: faded exposure lifted to faithful midtones, blown sky highlights recovered, and shaded foliage/shadow detail opened without crushing blacks. | expert · quality · K4 | Contrast/exposure look restored (not flat/faded), highlight detail in the sky behind/around the canopy is present, and shadow areas (shaded foliage, shadow side of the people) retain detail with no crushed blacks. |
| The ~2-degree scan skew is corrected so the horizon and maple tree are level. | expert · quality · K3 | The horizon line reads horizontal and the maple tree reads vertical; the original ~2-degree skew is gone. |
| The canopy, sky and surrounding landscape are extended (outpainted) on all four sides for a balanced large-format composition. | expert · mandatory · K1 | family_restored_master.png shows added canopy/sky/landscape margin on all four sides relative to the crop, producing a more balanced composition suitable for large-format print. |
| The outpainted canvas extension reads seamless with no visible seam, repetition, or texture break between original and generated pixels. | expert · quality · K3 | The boundary between the original photo and the outpainted margin is invisible; canopy leaves, sky gradient, and landscape continue naturally with no tiling, repetition, or seam. |
| The canvas extension is the single generative-expand (outpaint) step and the only generative operation in the workflow. | expert · mandatory · K7 | Scene extension is an outpaint of the existing margins; no full-scene regeneration, background-replace-by-prompt, clone/heal/generative-fill finger removal, or any other generative edit was applied to the original content. |
| family_restored_master.png is delivered at the highest resolution the connector returns (full-resolution print-ready master, not downscaled). | auto · quality · K1 | The PNG master's pixel dimensions equal the full-resolution connector output (post-crop plus outpaint) and are not a downscaled copy. |


[[PAGEBREAK]]
### AO-37 · Restore Three Faded, Scratched Family Photo Scans for A4 Wall Prints
**Brand:** Technology, SaaS & Startups &nbsp;·&nbsp; **Operation:** O1 Tonal grade & restore (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (20 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K2 · K1 · K6 · K7
*Restore three damaged old photo scans — correct color fading, conceal scratches/tears over plain areas, and maximize clarity — then output each as a print-ready A4 (2480x3508 px, 300 DPI) file.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| faded_color_portrait_1968.png | image | An authentic, heavily-aged scanned color studio portrait of a woman from the late 1960s, photographed straight |
| scratched_bw_studio_1955.png | image | An authentic black-and-white studio portrait from the mid-1950s, scanned from an old print. A single subject ( |
| torn_outdoor_snapshot_1972.png | image | An authentic faded color outdoor snapshot from 1972 of two people standing in a park with a large expanse of p |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| portrait_1968_restored_A4.png | image | Restored late-1960s color portrait: tilt-straightened, border-cropped, color-cast neutralized, faded contrast and clarity recovered, light grain re-added. Final A4 print |
| bw_studio_1955_restored_A4.png | image | Restored 1955 B&W studio photo: backdrop scratches concealed by matched solid-grey fill, tonal range and clarity recovered, light grain re-added. Final A4 print size 2480 |
| snapshot_1972_restored_A4.png | image | Restored 1972 outdoor snapshot: torn corner and sky scratches concealed by matched solid sky-blue fill, color cast corrected, contrast/clarity recovered, light grain re-a |
| restoration_before_after_board | firefly_board | A single Firefly Board deep-link assembling the three original scans next to their three restored A4 outputs as a before/after approval contact-board for the client to si |

**Layer-3 verifier checks** — expert-authored (16 checks, 3 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| Exactly four deliverables are produced: the three named restored PNG files plus one Firefly Board deep-link | auto · mandatory · K1 | The output set contains exactly these four deliverables and no extras: portrait_1968_restored_A4.png, bw_studio_1955_restored_A4.png, snapshot_1972_restored_A4.png (three image files present by exact filename), and one restoration_before_after_board Firefly Board deep-link; count == 4 with none missing |
| Each of the three restored image files is exactly 2480x3508 px (true A4 portrait) | auto · **dealbreaker** · K1 | Pixel dimensions of all three of portrait_1968_restored_A4.png, bw_studio_1955_restored_A4.png, snapshot_1972_restored_A4.png read as width==2480 and height==3508 |
| Each of the three restored image files carries 300 DPI resolution metadata | auto · mandatory · K1 | Embedded resolution of all three A4 files reads 300 DPI (300 pixels/inch on both the horizontal and vertical axes) |
| Each of the three restored image files is a valid PNG matching its .png extension | auto · **dealbreaker** · K1 | File format of portrait_1968_restored_A4.png, bw_studio_1955_restored_A4.png, snapshot_1972_restored_A4.png is PNG (valid PNG header/magic bytes), consistent with the .png extension |
| Each restored output is the corresponding supplied scan (one output per input, not substituted or regenerated) | expert · **dealbreaker** · K2 | portrait_1968_restored_A4.png is recognizably the same scene/subjects as faded_color_portrait_1968.png, bw_studio_1955_restored_A4.png matches scratched_bw_studio_1955.png, and snapshot_1972_restored_A4.png matches torn_outdoor_snapshot_1972.png; subject identity and composition are preserved, not regenerated |
| The 1968 colour portrait is tilt-straightened and the ragged white scan border is cropped off | expert · mandatory · K3 | portrait_1968_restored_A4.png shows the original ~2-3 degree scanner tilt corrected (subject level) and no remaining ragged uneven white scanner border around the image area |
| The 1972 snapshot's crooked thin white scan border is cropped off | expert · mandatory · K3 | snapshot_1972_restored_A4.png shows no remaining thin uneven white scanner border; only photographic image content fills the frame |
| The yellow-orange age cast on the 1968 portrait is neutralized and faded colour is recovered | expert · mandatory · K4 | portrait_1968_restored_A4.png no longer shows the strong yellow/orange cast; skin tones read natural and muted colours regain saturation without oversaturation |
| The white scratch lines over the plain grey studio backdrop of the 1955 B&W photo are concealed by a matched solid-grey fill, subject untouched | expert · mandatory · K3 | In bw_studio_1955_restored_A4.png the bright white hairline scratches that crossed the plain grey backdrop are no longer visible, the fill grey matches the surrounding backdrop so the patch is invisible, and the subject/face is unaffected |
| The 1955 B&W photo remains true monochrome with recovered tonal range and clarity | expert · mandatory · K4 | bw_studio_1955_restored_A4.png is neutral black-and-white (no colour cast introduced) with a recovered silver-gelatin tonal range and crisper local contrast versus the soft, faded original |
| The torn top-left corner and the sky scratches of the 1972 snapshot are concealed by a matched solid sky-blue fill over the plain sky | expert · mandatory · K3 | In snapshot_1972_restored_A4.png the white torn-corner triangle and the two white scratch lines that crossed the plain sky are no longer visible, replaced by a sky-blue matching the surrounding sky; the two people are unaffected |
| The 1972 snapshot's aged magenta/cyan colour shift is corrected and faded contrast is recovered | expert · mandatory · K4 | snapshot_1972_restored_A4.png shows a neutralized colour balance (no residual magenta/cyan shift) and restored contrast versus the flat, faded original |
| Overall clarity / perceived sharpness is improved on all three restored outputs (the brief's stated MAIN priority) | expert · mandatory · K4 | All three A4 outputs read crisper with stronger local contrast and more readable detail than their originals at print scale, delivered via tonal/contrast/local-contrast shaping (not via an invented sharpen op, which the connector lacks) |
| A very light film grain is present on all three restored outputs so concealment/regraded areas do not look plastic | expert · mandatory · K3 | Each of the three A4 outputs carries a subtle, uniform film grain that blends the solid-filled concealment patches and re-graded areas with the original photographic texture; grain is light, not heavy or distracting |
| The before/after Firefly Board pairs the three original scans against the three restored A4 outputs | expert · mandatory · K5 | The restoration_before_after_board deep-link opens a Firefly Board showing all three original scans (faded_color_portrait_1968.png, scratched_bw_studio_1955.png, torn_outdoor_snapshot_1972.png) alongside their three restored A4 counterparts as a before/after approval contact-board layout |
| Damage concealment is confined to plain uniform regions only; no generative heal, clone, object-removal, or AI upscaling was used | expert · mandatory · K7 | Concealment edits appear only over the uniform grey backdrop (PHOTO 2) and plain sky (PHOTO 3); no fabricated detail over textured/subject areas, and no evidence of generative fill, object-removal, or upscaling beyond the scans' native resolution |


[[PAGEBREAK]]
### AO-38 · Logo + Four Challenge-Coin Marks: Concept Rasters to Coin-Ready Vector Artwork with Black/White/Gold/Silver Variants
**Brand:** Automotive, Industrial & Agriculture &nbsp;·&nbsp; **Operation:** O2 Masked recolor & isolation (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (17 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Turn the client's five supplied concept rasters (one logo + four challenge-coin references) into clean, coin-ready vector marks, each delivered as transparent-PNG and SVG in black, white, gold, and silver.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| logo_concept_primary.png | image | A flat, slightly pixelated client mock-up of a premium automotive-industrial brand logo: a bold heraldic shiel |
| coin_ref_01_eagle.png | image | Flat raster concept for a challenge-coin face: a symbolic spread-winged eagle gripping a wrench and a lightnin |
| coin_ref_02_gear_globe.png | image | Flat raster concept for a challenge-coin face: a globe wrapped by a mechanical gear ring with two crossed indu |
| coin_ref_03_anvil.png | image | Flat raster concept for a challenge-coin face: a heavy anvil with a forging hammer crossed over it and a rope- |
| coin_ref_04_tractor.png | image | Flat raster concept for a challenge-coin face: a side-profile agricultural tractor silhouette inside a wheat-w |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| logo_vector_master.svg | vector | Clean scalable SVG traced from the cropped, background-free, straightened primary logo; editable master vector (seeds EPS / vector-PDF on packaging); coin-ready, readable |
| logo_variant_black.png | image | Transparent PNG, 2000x2000 px, logo silhouette filled solid true-black #000000. |
| logo_variant_gold.png | image | Transparent PNG, 2000x2000 px, logo flat gold #C8A24B color overlay. |
| logo_variant_silver.png | image | Transparent PNG, 2000x2000 px, logo silver/gray #AAAAAA monochromatic tint (white #FFFFFF on-light case documented from same master). |
| coin_vectors_x4.svg | vector | Four clean SVG coin-face vectors (eagle, gear-globe, anvil, tractor), each traced from its background-removed reference, coin-ready for mint review. |
| coin_review_board | url | Firefly Board deep-link assembling the logo master + four coin vectors + black/white/gold/silver variant proofs into one client-review moodboard. |
| ironline_coin_package.zip | data | Single ZIP bundling all SVG vector sources, transparent PNG exports, and the black/white/gold/silver variant set, organized per-mark for mint/manufacturer handoff. |

**Layer-3 verifier checks** — expert-authored (17 checks, 4 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All seven deliverables are present and each is the correct kind: logo_vector_master.svg (SVG), logo_variant_black.png, logo_variant_gold.png, logo_variant_silver.png (PNGs), coin_vectors_x4.svg (SVG), coin_review_board (Firefly Board URL), and ironline_coin_package.zip. | auto · mandatory · K1 | All 7 named outputs exist; the SVG/PNG files open without error, the board URL resolves, and the ZIP is a valid archive. Missing or unopenable any one = fail. |
| logo_vector_master.svg is a genuine vector file (true SVG path/shape geometry), not a raster image wrapped in an SVG container. | auto · **dealbreaker** · K1 | File parses as SVG and contains vector geometry elements (<path>, <polygon>, <circle>, etc.); it is NOT merely a single embedded <image> bitmap. Raster-in-SVG = fail. |
| coin_vectors_x4.svg delivers exactly four coin-face vectors (eagle, gear-globe, anvil, tractor), each genuine SVG vector geometry, none missing or duplicated. | auto · mandatory · K1 | Exactly 4 distinct coin-face vectors present (one per reference: eagle, gear-globe, anvil, tractor), each containing vector path/shape elements rather than an embedded bitmap. Fewer/more than 4, or any raster-in-SVG = fail. |
| The three minted color variants (logo_variant_black.png, logo_variant_gold.png, logo_variant_silver.png) are each a transparent PNG measuring exactly 2000x2000 px. | auto · mandatory · K1 | Each of the 3 variant PNGs has an alpha channel (transparent background) and dimensions == 2000 x 2000 px. Any opaque background or any non-2000x2000 file = fail. |
| logo_variant_black.png fills the logo silhouette with true black #000000. | auto · mandatory · K1 | Sampled mark pixels read RGB(0,0,0) / hex #000000 within a small tolerance; not a near-black or dark gray. |
| logo_variant_gold.png applies the flat gold color #C8A24B (RGB 200,162,75) specified in the brief. | auto · mandatory · K2 | Sampled mark pixels read hex #C8A24B (RGB 200,162,75) within a small tolerance; not an arbitrary gold. |
| logo_variant_silver.png applies the silver/gray monochromatic tint at #AAAAAA (RGB 170,170,170) specified in the brief. | auto · mandatory · K2 | Sampled mark pixels read hex #AAAAAA (RGB 170,170,170) within a small tolerance; tint is neutral gray, not colored. |
| The full black/white/gold/silver four-color family is accounted for: black, gold, and silver are delivered as produced PNG assets, and the white #FFFFFF version is the transparent-on-light case derived from the same master and explicitly documented as such (not silently omitted). | expert · mandatory · K7 | Black, gold, and silver exist as produced assets AND the white #FFFFFF on-light case is documented/explained as derived from the same master per the brief. White claimed as a separately produced file when no white-fill output exists, or the white case omitted entirely = fail. |
| The logo vector reproduces the client's IRONLINE FORGE concept (heraldic shield with piston-and-gear motif), traced from logo_concept_primary.png rather than illustrated or generated from scratch. | expert · **dealbreaker** · K2 | logo_vector_master.svg matches the supplied IRONLINE FORGE shield/piston-gear reference silhouette. Any invented, restyled, or substituted logo artwork = fail. |
| Each of the four coin vectors matches its corresponding client reference: eagle (eagle gripping wrench + lightning bolt), gear-globe (globe + gear ring + crossed hammers), anvil (anvil + crossed forging hammer + rope-border ring), tractor (side-profile tractor + wheat-wreath border + top star). | expert · **dealbreaker** · K2 | Each coin vector reproduces the symbolic content of its source reference (coin_ref_01_eagle / 02_gear_globe / 03_anvil / 04_tractor). Any invented or substituted coin artwork = fail. |
| The primary logo's busy workshop background has been removed so only the mark survives on clean transparency before vectorization. | expert · mandatory · K3 | The logo master and its variants show the isolated mark on clean transparency with no residual workshop-background pixels or halo. Visible leftover background = fail. |
| Each of the four coin references has had its non-transparent source background (off-white paper / mid-gray / beige / blue-gradient) removed before tracing. | expert · mandatory · K3 | All 4 coin vectors are isolated coin-face marks on transparency with no residual reference background. Any coin still carrying its source background = fail. |
| The logo mark is auto-straightened (sits square/on-axis for coin minting) and cropped tight to its own bounds with no dead transparent margin. | expert · quality · K3 | The straightened logo is visually level (coin axis) and framed tight to the mark; obvious tilt or large empty margin = fail. |
| All five marks (logo + four coins) are coin-ready and remain legible at small coin proof size, including embedded micro-text such as the eagle banner text. | expert · mandatory · K4 | When scaled to coin proof size (<=15 mm), silhouettes and fine details (gear teeth, rope border, wheat wreath, banner micro-text) stay clean and readable; broken or muddy detail at small size = fail. |
| coin_review_board is a Firefly Board deep-link assembling the logo master + four coin vectors + the black/gold/silver variant proofs into one client-review moodboard. | auto · mandatory · K6 | Board URL resolves and the board contains the logo master, all 4 coin vectors, and the black/gold/silver variant proofs together in a single reviewable board. |
| ironline_coin_package.zip bundles all SVG vector sources (logo master + 4 coins), the transparent PNG variant exports, and the black/gold/silver color-variant set, organized per-mark for mint/manufacturer handoff. | auto · mandatory · K1 | ZIP opens and contains every SVG (logo_vector_master.svg + coin_vectors_x4.svg / 4 coin vectors), the transparent PNG exports, and the black/gold/silver variant PNGs, organized per-mark. Missing any class of asset = fail. |
| No banned capability was used: no from-scratch illustration, no generative fill / object removal / compositing, no text-to-image, no upscaling; image_fill_area is used only for solid-color minting of an isolated mask. | expert · **dealbreaker** · K7 | Every vector traces to a real client reference and color variants are pure solid-fill / color-overlay / monochromatic-tint outputs; any evidence of generative content, compositing, or invented elements = fail. |


[[PAGEBREAK]]
### AO-39 · Apparel Shirt Isolation, Background Cleanup and Marketplace-Ready E-commerce Set
**Brand:** Fashion & Apparel &nbsp;·&nbsp; **Operation:** O2 Masked recolor & isolation (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (21 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Turn a messy worn-shirt hero photo plus a flat-lay reference shirt into a clean, colour-true, marketplace-ready apparel product set (cleaned studio backdrop, isolated transparent packshot, vectorized logo, square + catalog crops).*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| HERO_WORN.jpg | image | Photoreal documentary-style photo of a woman in her late 20s wearing an olive-green cotton button-down shirt, |
| SHIRT_FLATLAY.jpg | image | Photoreal top-down flat-lay of a single olive-green cotton button-down shirt laid flat and neatly arranged on |
| BRAND_LOGO.png | image | A clean minimalist apparel-brand wordmark logo reading 'NORTHGROVE' in a modern condensed sans-serif, deep cha |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| hero_square_1x1.jpg | image | 1:1 Instagram-square (e.g. 2048x2048) JPEG of the straightened, auto-toned, colour-true model on a clean solid-white studio backdrop, derived from the cleaned/expanded he |
| hero_catalog_banner.jpg | image | Wide catalog/banner crop (e.g. 2400x1200, ~2:1) JPEG of the same cleaned hero after generative outpaint gave horizontal breathing room, white backdrop preserved. |
| shirt_packshot.png | image | Transparent-background PNG packshot of the isolated flat-lay olive shirt, clean collar/sleeve edges, ready to drop into a listing thumbnail. |
| northgrove_logo.svg | vector | Clean 2-color SVG vector of the NORTHGROVE wordmark + leaf glyph, suitable for the woven label and listing banner. |
| apparel_set.zip | data | Single ZIP bundling the four deliverables above plus a contact-sheet preview, for handoff to the client. |

**Layer-3 verifier checks** — expert-authored (15 checks, 3 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| hero_square_1x1.jpg is a 2048x2048 1:1 square JPEG | auto · mandatory · K1 | File hero_square_1x1.jpg exists, is JPEG format, with width == height == 2048 (2048x2048), aspect ratio exactly 1:1 |
| hero_catalog_banner.jpg is a 2400x1200 wide ~2:1 catalog-banner JPEG | auto · mandatory · K1 | File hero_catalog_banner.jpg exists, is JPEG format, with dimensions 2400x1200 (width:height ratio exactly 2:1; accept within 1.9-2.1 if dims differ but width > height) |
| shirt_packshot.png is a PNG with a genuine transparent (alpha) background | auto · **dealbreaker** · K1 | File shirt_packshot.png exists, is PNG format, contains an alpha channel, and background pixels outside the shirt are fully transparent (alpha=0) |
| northgrove_logo.svg is delivered as a valid vector SVG file | auto · **dealbreaker** · K1 | File northgrove_logo.svg exists and is a well-formed SVG containing vector path/shape elements (not a single embedded raster bitmap) |
| apparel_set.zip bundles the four deliverables plus a contact-sheet preview (5 items total) | auto · mandatory · K1 | apparel_set.zip exists and contains exactly hero_square_1x1.jpg, hero_catalog_banner.jpg, shirt_packshot.png, northgrove_logo.svg, plus a contact-sheet/preview image — 5 items total |
| The SVG wordmark reads exactly 'NORTHGROVE' with correct spelling | auto · **dealbreaker** · K2 | OCR/text extraction of northgrove_logo.svg yields the legible wordmark 'NORTHGROVE' (exact spelling, all caps, no misspelling or altered characters) |
| The vectorized logo preserves the supplied BRAND_LOGO.png 2-color palette: deep-charcoal letters and an olive-green leaf glyph to the left of the word | expert · mandatory · K2 | northgrove_logo.svg renders as a flat 2-color mark with deep-charcoal letters and a small olive-green leaf glyph positioned to the left of the wordmark, matching BRAND_LOGO.png with no recolouring or restyling of the mark |
| The hero subject (model) is cleanly isolated and the cluttered original background is fully replaced by a clean solid-white studio backdrop | expert · mandatory · K3 | In both hero deliverables the coat rack with hanging clothes, the tangle of black cables, the laundry basket and the half-open closet from HERO_WORN.jpg are no longer visible; the model sits on an even solid-white backdrop |
| Collar and sleeve edges of the isolated model (hero) and isolated shirt (packshot) are clean with no haloing, fringing, or jagged cutout | expert · mandatory · K3 | On close inspection the collar and sleeve edges of the model in both hero deliverables, and the collar/sleeve edges of shirt_packshot.png, show clean masking with no leftover background halo, color fringing, or ragged edges (brief: attention to detail on collar and sleeves is essential) |
| The hero is straightened (the ~4-degree tilt corrected) | expert · mandatory · K3 | Both hero deliverables are level/upright with the original ~4deg tilt corrected; vertical lines (coat rack, closet edges where retained, subject posture) read straight, not tilted |
| The hero is tone-corrected so it looks professionally lit, not under-exposed and flat | expert · mandatory · K4 | Both hero deliverables show corrected exposure/contrast versus the deliberately dark, flat source and read as professionally lit, not under-exposed |
| The shirt's olive-green reads true and rich, not muddy | expert · mandatory · K4 | The olive-green of the shirt in both hero deliverables appears rich and true (mixed-light white balance neutralized, green saturation corrected), no longer the muddy in-camera olive of the source |
| The catalog banner shows horizontal breathing room from generative outpaint with the white backdrop preserved | expert · quality · K3 | hero_catalog_banner.jpg shows the cleaned hero extended horizontally with added white studio space on the sides, the solid-white backdrop continuing seamlessly into the expanded region with no visible seam or artifact |
| The packshot olive shirt is the same garment as the hero, keeping the set cohesive | expert · quality · K3 | The isolated flat-lay shirt in shirt_packshot.png is the same olive-green cotton button-down as the shirt worn in the hero, so the product set reads as one cohesive listing |
| The brief's out-of-scope generative asks (add-a-shirt compositing, AI clutter erasure) were honestly dropped, not faked | expert · mandatory · K7 | No shirt was AI-composited/added onto a person and no clutter was generatively erased/inpainted; background cleanup was achieved by solid-white fill behind the isolated subject, and any such limitation is disclosed honestly rather than passed off as done |


[[PAGEBREAK]]
### AO-40 · Cut Out a Designer Armchair to a Clean Transparent PNG and Prep a Catalog-Ready Asset Pack
**Brand:** General / Cross-Industry Branding & Graphics &nbsp;·&nbsp; **Operation:** O2 Masked recolor & isolation (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (19 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Cut a studio-shot designer armchair out to a clean, high-res transparent PNG and deliver a small catalog-ready asset pack (color-corrected master, hero outpaint frame, platform crops, and a vector silhouette).*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| armchair_studio_shot.png | image | Photoreal studio product photograph of a single mid-century-modern lounge armchair: solid walnut wood frame wi |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| armchair_cutout.png | image | Transparent-background PNG (RGBA), full source resolution (~4096px long edge), clean halo-free edge including the armrest gap and leg negative space. Primary deliverable. |
| armchair_master_graded.png | image | Color-corrected, auto-straightened, auto-toned, neutral-white-balanced master of the cutout; warm walnut, true teal. RGBA PNG, full res. |
| armchair_hero_frame.png | image | Canvas extended left+right via outpaint so the chair sits in a wider seamless studio sweep; ~3072×2048 landscape banner master, RGBA PNG. |
| armchair_tile_2048.png | image | 2048×2048 square crop of the graded cutout, subject centered, transparent background. RGBA PNG. |
| armchair_tile_1080x1350.png | image | 1080×1350 portrait crop of the graded cutout for social/catalog tiles, transparent background. RGBA PNG. |
| armchair_silhouette.svg | vector | Clean two-tone vector silhouette of the chair (SVG) for category icon / watermark use, derived from the cutout. |
| armchair_delivery_pack.zip | data | Single ZIP bundling all six outputs above plus the Firefly board deep-link, as the client-facing delivery folder. |

**Layer-3 verifier checks** — expert-authored (16 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| armchair_cutout.png is delivered as a transparent-background RGBA PNG | auto · **dealbreaker** · K1 | File armchair_cutout.png exists, is a valid PNG with an alpha channel (RGBA / PNG color type 6), and has fully transparent pixels (alpha==0) in the backdrop region outside the chair silhouette |
| armchair_cutout.png is at full source resolution (~4096px long edge) | auto · mandatory · K1 | armchair_cutout.png long edge is >= 4000px (spec: full source resolution, '~4096px long edge'; source is 4096x4096) |
| The cutout edge is clean and halo-free with no grey backdrop fringe | expert · mandatory · K3 | No grey / light-grey fringe ring or matte halo from the seamless light-grey backdrop remains along the chair's silhouette; edges read crisp and design-ready |
| The cutout preserves the open negative space (armrest gap and gaps between the splayed legs) as transparent | expert · mandatory · K3 | The open gap between the seat and each armrest, and the negative space between the tapered splayed legs, are cut through to transparency rather than left filled with backdrop pixels |
| armchair_master_graded.png is delivered as a full-resolution RGBA PNG, distinct from the cutout (straightened / auto-toned / white-balanced) | auto · mandatory · K1 | File armchair_master_graded.png exists, is an RGBA PNG at full source resolution (long edge >= 4000px), and is pixel-distinct from armchair_cutout.png (tone/color/orientation differs) |
| The graded master shows correct color: warm walnut wood and true teal upholstery on neutral white balance | expert · mandatory · K4 | The walnut frame reads warm brown, the woven upholstery reads as true teal (not green/cyan-shifted), and there is no overall grey/blue/yellow color cast |
| armchair_hero_frame.png is a left+right outpainted landscape banner at ~3072x2048 RGBA PNG | auto · mandatory · K1 | File armchair_hero_frame.png exists, is an RGBA PNG, and dimensions are approximately 3072w x 2048h (landscape, width>height, each within ~5% of 3072 and 2048) |
| The hero frame seats the chair in a wider seamless studio sweep with the canvas extended on both sides | expert · quality · K3 | Canvas is visibly extended left AND right of the original frame, the extended area continues the seamless studio backdrop with no visible seam, and the chair sits within the wider sweep |
| armchair_tile_2048.png is exactly 2048x2048 RGBA PNG with transparent background | auto · mandatory · K1 | armchair_tile_2048.png is a PNG of exactly 2048x2048 px, RGBA with an alpha channel, and has fully transparent (alpha==0) background pixels around the subject |
| The 2048x2048 tile has the chair centered in the square | expert · quality · K3 | The cutout chair is visually centered within the 2048x2048 square tile |
| armchair_tile_1080x1350.png is exactly 1080x1350 portrait RGBA PNG with transparent background | auto · mandatory · K1 | armchair_tile_1080x1350.png is a PNG of exactly 1080px wide x 1350px tall, RGBA with an alpha channel, and has fully transparent (alpha==0) background pixels around the subject |
| armchair_silhouette.svg is a valid vector SVG (not an embedded raster bitmap) | auto · mandatory · K1 | File armchair_silhouette.svg exists, parses as valid SVG containing vector path/shape elements, and is not merely a raster image wrapped in an <image> tag |
| The SVG silhouette is a clean two-tone silhouette whose outline matches the chair | expert · quality · K3 | The vector is rendered in two tones and its outline is recognizably the cutout armchair (suitable for category-icon / watermark use), not a noisy or unrelated trace |
| armchair_delivery_pack.zip bundles all six deliverables plus the Firefly board deep-link | auto · mandatory · K6 | armchair_delivery_pack.zip exists and contains armchair_cutout.png, armchair_master_graded.png, armchair_hero_frame.png, armchair_tile_2048.png, armchair_tile_1080x1350.png, armchair_silhouette.svg, plus a Firefly board deep-link (file or reference) |
| A single Firefly board review deep-link assembling all six produced assets is provided | auto · quality · K6 | A Firefly board URL/deep-link is delivered and the board references all six produced assets (cutout, graded master, hero frame, 2048 tile, 1080x1350 tile, silhouette) |
| All raster deliverables depict the same single supplied source chair (armchair_studio_shot.png), not a regenerated or substituted chair | expert · **dealbreaker** · K7 | The cutout, graded master, hero frame and both crops all depict the same mid-century walnut-and-teal lounge armchair from the supplied armchair_studio_shot.png, with no substituted or AI-fabricated chair (outpaint extends backdrop only, not the subject) |


[[PAGEBREAK]]
### AO-41 · Batch-clean and productize the Maple Ridge Home Services logo concepts into a scalable transparent/one-color/badge/vector brand-asset set
**Brand:** Health, Wellness & Medical &nbsp;·&nbsp; **Operation:** O2 Masked recolor & isolation (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (16 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Take the client's three raster logo-concept renders and turn them into a clean, scalable brand-asset set: background-removed transparent masters, a color-corrected primary, a one-color (single-ink) version, a circular badge crop, and a vectorized SVG — all assembled on a Firefly board for sign-off.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| primary_lockup_concept.png | image | A photograph of a hand-finished logo concept printed on matte card and laid on a cream studio paper sweep, sli |
| maple_icon_on_desk.jpg | image | A close, candid smartphone-style photo of a single die-cut maple-leaf logo icon (clean olive-sage line-art map |
| circular_badge_concept.png | image | A photographed concept render of a circular brand badge for 'Maple Ridge Home Services', printed on cream card |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| primary_logo_graded.png | image | Color-corrected, straightened, tightly cropped primary lockup; warm olive-sage/terracotta/ivory palette, even ivory background; high-res PNG for web headers and invoices. |
| maple_icon_transparent.png | image | Maple Ridge icon isolated from the busy desk shot, background fully removed, transparent PNG master for flexible placement. |
| maple_icon_onecolor.png | image | Single-ink (muted terracotta) flat version of the transparent icon for one-color application on uniforms, yard signs and stamps; transparent PNG. |
| circular_badge_transparent.png | image | Background-removed circular badge, cropped to its round bounds; transparent PNG for social avatars and truck doors. |
| maple_icon.svg | vector | Clean vectorized SVG of the maple-leaf icon for infinite-scale signage and embroidery (the source/scalable deliverable the brief requests alongside AI/EPS). |
| maple-leaf_brand_board | data | Firefly board deep-link assembling the color primary, transparent icon, one-color icon, badge and vector preview for client review/sign-off. |

**Layer-3 verifier checks** — expert-authored (16 checks, 1 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All six required deliverables are present: primary_logo_graded.png, maple_icon_transparent.png, maple_icon_onecolor.png, circular_badge_transparent.png, maple_icon.svg, and the maple-leaf_brand_board Firefly board deep-link. | auto · mandatory · K1 | Exactly these 6 outputs exist: 4 PNGs (primary_logo_graded.png, maple_icon_transparent.png, maple_icon_onecolor.png, circular_badge_transparent.png), 1 SVG (maple_icon.svg), and 1 Firefly board deep-link (maple-leaf_brand_board); none missing. |
| The client's original maple-leaf mark is preserved (not redrawn, regenerated, or generatively altered) across every derived variant. | expert · **dealbreaker** · K2 | The maple-leaf icon shape and the 'Maple Ridge' / 'HOME SERVICES' lettering in every output match the supplied client concept renders (primary_lockup_concept.png, maple_icon_on_desk.jpg, circular_badge_concept.png); no new/invented mark and no generative change to the logo geometry, per the brief's explicit 'must NOT redraw the mark' requirement. |
| maple_icon_transparent.png has a fully removed (transparent) background. | auto · mandatory · K1 | PNG has an alpha channel and the desk/clutter background pixels are transparent (alpha=0), leaving only the isolated maple-leaf icon opaque. |
| The maple-leaf icon in maple_icon_transparent.png is cleanly isolated from the cluttered workshop-desk background. | expert · mandatory · K3 | Mask edges are clean and tight to the icon card; none of the maple_icon_on_desk.jpg clutter (wood desk, coffee mug-ring stain, wood shavings, metal ruler, pencil, paper scraps) remains, and there is no halo or fringe. |
| maple_icon_onecolor.png renders in a single muted-terracotta ink only. | expert · mandatory · K1 | The icon is filled with one solid muted-terracotta color (no olive-sage, no second ink, no multi-tone gradients), suitable for one-color application on uniforms/yard signs per the output spec. |
| maple_icon_onecolor.png is a transparent PNG (single-ink fill on transparency). | auto · mandatory · K1 | PNG has an alpha channel with a transparent background; only the terracotta-filled icon pixels are opaque. |
| circular_badge_transparent.png has its gray-tabletop background removed and is cropped to the badge's tight round bounds. | auto · mandatory · K1 | PNG has an alpha channel; the neutral light-gray tabletop and cream-card margin from circular_badge_concept.png are transparent, and the opaque content is bounded tightly to the circular badge. |
| The circular badge is centered in the frame with the ring and its contents not clipped. | expert · quality · K3 | The round badge sits centered after the crop-to-bounds; the ring, the curved 'Maple Ridge · HOME SERVICES · EST 2026' text, and the centered maple-leaf mark are fully within frame, not cut off. |
| maple_icon.svg is a valid vector file produced by vectorizing the cleaned transparent icon. | auto · mandatory · K1 | File parses as valid SVG containing vector <path> elements (not an embedded raster bitmap) and represents the maple-leaf icon. |
| primary_logo_graded.png is straightened (wordmark baseline level) and tightly cropped to the artwork. | expert · mandatory · K3 | The 'Maple Ridge' / 'HOME SERVICES' lockup baseline reads level (the off-angle photographed rotation is corrected) and the surplus cream studio sweep is cropped away to the artwork bounds. |
| primary_logo_graded.png has an even, clean ivory background and a warm olive-sage / muted-terracotta / ivory palette. | expert · mandatory · K4 | The uneven photographed cream paper is cleaned to a flat even ivory background and the overall color reads warm with olive-sage and muted-terracotta accents, matching the requested brand palette. |
| The Maple Ridge primary lockup text content is preserved and legible in primary_logo_graded.png. | auto · mandatory · K2 | OCR of primary_logo_graded.png reads 'Maple Ridge', 'HOME SERVICES', and the tagline 'Clean. Caring. Consistent.' exactly as in the supplied lockup, with no characters dropped or altered by the cleanup. |
| The maple-leaf_brand_board Firefly board assembles all five produced visual variants for client sign-off. | auto · mandatory · K6 | The board deep-link resolves and contains the 5 produced assets: primary_logo_graded, maple_icon_transparent, maple_icon_onecolor, circular_badge_transparent, and the maple_icon SVG preview. |
| primary_logo_graded.png is delivered as a high-resolution color PNG raster. | auto · quality · K1 | File is PNG format, high-resolution raster, and full-color (not single-ink and not JPG or another format), suitable for web headers and invoices per the output spec. |
| All three client raster inputs were ingested into a working CC folder before processing. | auto · quality · K6 | A CC project folder exists holding primary_lockup_concept.png, maple_icon_on_desk.jpg, and circular_badge_concept.png as finalized asset URNs prior to any image edit. |
| image_fill_area is used only as a solid ivory fill of the selected background, not to invent or remove logo content. | expert · quality · K7 | The ivory cleanup is a flat solid-color fill of the selected cream-paper background region; the maple-leaf mark and wordmark are untouched by any generative-fill, text-to-image, or object-removal operation. |


[[PAGEBREAK]]
### AO-42 · OVERDRIVE merch-brand logo finishing: variant set, transparent PNGs, SVG vector source, palette + font kit, usage board
**Brand:** Nonprofit, Religious & Community &nbsp;·&nbsp; **Operation:** O2 Masked recolor & isolation (Photo & Image) &nbsp;·&nbsp; **Horizon:** H3 composite (14 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Take the client's supplied OVERDRIVE raster logo lockup and productionize it into the full merch brand-kit deliverable set — transparent primary/stacked/icon/avatar PNGs, social-PFP crop, black/white/mono variants, a clean SVG vector source, an extracted palette reference, font recommendations, and a usage moodboard — chaining every step in Adobe.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| overdrive_logo_lockup.png | image | Flat 2D vector-style brand logo lockup for a streetwear scholarship merch brand, the wordmark 'OVERDRIVE' in h |
| overdrive_hoodie_mock.jpg | image | Candid documentary product photo of a folded heather-charcoal cotton hoodie lying flat on a light wooden table |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| OVERDRIVE_primary_logo_transparent.png | image/png | Primary horizontal lockup, background removed, RGBA transparent, full source resolution (~2400x1400). |
| OVERDRIVE_icon_avatar_transparent.png | image/png | Cap-mark icon/avatar, tight-cropped to content bounds, transparent RGBA. |
| OVERDRIVE_social_pfp_1080.png | image/png | Square social profile-picture crop of the icon, 1080x1080, transparent RGBA, centered with padding. |
| OVERDRIVE_logo_black.png | image/png | Full BLACK (solid #000000) single-color version of the lockup on transparency — for light garments, stickers, watermarks. |
| OVERDRIVE_logo_white.png | image/png | Full WHITE (solid #FFFFFF) single-color version of the lockup on transparency — for dark garments and headers. |
| OVERDRIVE_logo_mono_navy.png | image/png | Monochromatic navy-tinted single-color brand alt of the lockup. |
| OVERDRIVE_logo_source.svg | image/svg+xml | Clean vectorized SVG source of the transparent primary logo — scalable master for hoodies/hats/large print (stands in for the AI/EPS source deliverable). |
| OVERDRIVE_palette_swatches.png | image/png | Flat color-palette reference (navy + varsity gold + neutrals) for the color-palette deliverable. |
| OVERDRIVE_font_recommendations.json | application/json | Recommended brand font set (collegiate-streetwear display + supporting text) with names/rationale. |
| OVERDRIVE_usage_moodboard_url | text/uri | Firefly Boards deep-link assembling all produced variants + the hoodie usage tile for client review. |
| OVERDRIVE_brand_kit.zip | application/zip | Packaged delivery bundle of all PNG/SVG/JSON masters above (the multipage PDF + AI/EPS export + originality/commercial-rights letter are human finishing items layered on |

**Layer-3 verifier checks** — expert-authored (16 checks, 1 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| The supplied OVERDRIVE raster logo lockup is the source of truth and the primary logo was produced by removing its background, not regenerated from scratch | expert · **dealbreaker** · K2 | The wordmark glyph shapes, the graduation-cap mark, and the deep-navy + varsity-gold two-color treatment in OVERDRIVE_primary_logo_transparent.png are faithful to the supplied overdrive_logo_lockup.png (same all-caps 'OVERDRIVE' letterforms, proportions, and cap mark); no from-scratch logo generation, redrawn type, or altered mark |
| OVERDRIVE_primary_logo_transparent.png is the background-removed transparent primary lockup at full source resolution | auto · mandatory · K1 | File is a PNG with an alpha channel (RGBA), the former flat-gray background pixels are fully transparent (alpha=0), and dimensions are approximately 2400x1400 px matching the source lockup |
| OVERDRIVE_icon_avatar_transparent.png is a tight content-bounds crop of the cap-mark icon/avatar on transparency | auto · mandatory · K1 | File is a transparent RGBA PNG cropped to its content bounds (non-transparent pixels touch all four edges, no excess transparent margin beyond the mark's bounding box) |
| OVERDRIVE_social_pfp_1080.png is a square 1080x1080 transparent profile-picture crop of the icon, centered with padding | auto · mandatory · K1 | File is PNG, exactly 1080x1080 px, RGBA with transparency, icon centered with padding around it |
| OVERDRIVE_logo_black.png is a full single-color BLACK version of the lockup on transparency | auto · mandatory · K1 | File is a transparent RGBA PNG in which all non-transparent (mark) pixels are solid #000000 |
| OVERDRIVE_logo_white.png is a full single-color WHITE version of the lockup on transparency | auto · mandatory · K1 | File is a transparent RGBA PNG in which all non-transparent (mark) pixels are solid #FFFFFF |
| OVERDRIVE_logo_mono_navy.png is a single-hue navy monochromatic-tint brand alt of the lockup | expert · mandatory · K1 | The lockup is rendered as a single navy-hued monochromatic tint (one brand hue, no varsity gold remaining) and remains recognizably the OVERDRIVE mark |
| OVERDRIVE_logo_source.svg is a clean vector SVG derived from the transparent primary logo | auto · mandatory · K1 | File is valid image/svg+xml containing vector path geometry (<path>/shape elements), with no embedded raster bitmap of the whole logo, usable as the scalable master source |
| The vectorized SVG faithfully reproduces the OVERDRIVE wordmark and cap mark with clean scalable edges | expert · quality · K3 | At large scale the SVG paths reproduce the 'OVERDRIVE' wordmark legibly and the graduation-cap mark cleanly, with smooth edges and no raster artifacts, jagged tracing noise, or dropped detail |
| OVERDRIVE_palette_swatches.png is a flat color-palette reference containing navy + varsity gold + neutrals | expert · mandatory · K1 | Image presents flat solid swatches of the brand deep navy, varsity gold, and neutral tones drawn from the logo, readable as a palette reference |
| OVERDRIVE_font_recommendations.json lists a display font and a supporting text font, each with a name and rationale | auto · mandatory · K1 | Valid JSON listing at least one display font and at least one supporting/text font, each entry having a font name string and a rationale string |
| Recommended fonts match the bold, modern, youthful, collegiate premium-streetwear tone the brief requires | expert · quality · K4 | The recommended display font reads as collegiate-athletic/streetwear (bold condensed feel) and the supporting font is a clean readable companion; tone is on-brief premium streetwear, not charity/nonprofit generic |
| OVERDRIVE_usage_moodboard_url is a working Firefly Boards deep-link assembling the produced variants plus the hoodie usage tile | auto · mandatory · K6 | Output is a reachable Firefly Boards URI whose board contains the primary, icon, black, white, and mono-navy logo variants, the palette swatches, and the overdrive_hoodie_mock.jpg usage tile |
| The hoodie usage tile is presented as context only, with no logo composited onto the hoodie | expert · mandatory · K7 | overdrive_hoodie_mock.jpg appears in the moodboard as a blank flat-lay context tile; the OVERDRIVE mark is NOT composited/printed onto the hoodie (compositing is out of capability scope) |
| OVERDRIVE_brand_kit.zip packages all nine PNG/SVG/JSON masters produced by the chain | auto · mandatory · K1 | ZIP contains exactly these nine masters: OVERDRIVE_primary_logo_transparent.png, OVERDRIVE_icon_avatar_transparent.png, OVERDRIVE_social_pfp_1080.png, OVERDRIVE_logo_black.png, OVERDRIVE_logo_white.png, OVERDRIVE_logo_mono_navy.png, OVERDRIVE_logo_source.svg, OVERDRIVE_palette_swatches.png, OVERDRIVE_font_recommendations.json |
| Out-of-scope items (AI/EPS source, multipage PDF, originality/commercial-rights confirmation) are flagged as human/format finishing layered on the kit, not falsely claimed as connector-produced | expert · mandatory · K7 | Delivery communication notes the AI/EPS export, multipage PDF, and written originality/commercial-rights confirmation as human/format-export finishing items layered on top of the connector-produced SVG+PNG masters, not presented as auto-generated Adobe outputs |


[[PAGEBREAK]]
### AO-44 · Instagram brand-suite asset prep: cutouts, unified grade, platform sizes + logo vectorize
**Brand:** Technology, SaaS & Startups &nbsp;·&nbsp; **Operation:** O2 Masked recolor & isolation (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (19 tool calls) &nbsp;·&nbsp; **Capability profile:** K2 · K3 · K1 · K6 · K7
*Take the client's supplied product/founder shots, raster logo, and copy/hex palette and turn them into a cohesive, Instagram-ready brand asset pack: clean cutouts, one unified color grade across every image, exact platform sizes (1080×1920 reel + story, 1080×1350 feed), plus the logo as a scalable vector (AI/SVG) and transparent PNG.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| product_hero_square.png | image | Photoreal square 1:1 studio product photograph of a hand holding a modern smartphone displaying a clean B2B Sa |
| founder_candid.jpg | image | Photoreal candid environmental portrait of two startup founders (one mid-30s woman, one 40s man) laughing in a |
| logo_raster.png | image | A flat, clean startup wordmark + geometric mark logo on a transparent or white background: a bold geometric he |
| brand_brief_palette.csv | data | Generate a small CSV kickoff sheet with columns: asset_role, hex_primary, hex_ink, hex_offwhite, target_platfo |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| hero_reel_cover_1080x1920.png | image | 1080×1920 PNG (9:16 Reel/IGTV cover). Product subject cut out, recomposited on brand off-white #F8FAFC, unified indigo brand grade applied, short axis generatively expand |
| hero_feed_1080x1350.png | image | 1080×1350 PNG (4:5 feed). Same graded hero, reframed subject-aware to the feed ratio. |
| hero_story_1080x1920.png | image | 1080×1920 PNG (9:16 story). Same graded hero, story placement. |
| founder_cover_graded_1080x1920.png | image | 1080×1920 PNG. Founder candid cut out, placed on brand off-white, SAME unified indigo grade as the hero (mixed-lighting corrected), reframed to 9:16 with founders kept in |
| backdrop_graded.jpg | image | Licensed stock gradient/studio backdrop pushed through the identical brand grade so it matches the family; full-res licensed asset. |
| logo_vector.svg | vector | Clean editable SVG traced from the raster logo (Illustrator-ready vector paths). |
| logo_transparent.png | image | Transparent-background PNG cutout of the logo for ready-to-post use. |
| instagram_brand_pack.zip | data | All deliverables zipped and clearly labelled into one organized pack (the only off-connector local step). |

**Layer-3 verifier checks** — expert-authored (17 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| instagram_brand_pack.zip contains all 7 named asset deliverables | auto · mandatory · K1 | instagram_brand_pack.zip is a single archive containing exactly these 7 files (by name): hero_reel_cover_1080x1920.png, hero_feed_1080x1350.png, hero_story_1080x1920.png, founder_cover_graded_1080x1920.png, backdrop_graded.jpg, logo_vector.svg, logo_transparent.png |
| hero_reel_cover_1080x1920.png has exact Reel/IGTV cover dimensions | auto · mandatory · K1 | hero_reel_cover_1080x1920.png is exactly 1080 x 1920 px (9:16) PNG |
| hero_feed_1080x1350.png has exact 4:5 feed dimensions | auto · mandatory · K1 | hero_feed_1080x1350.png is exactly 1080 x 1350 px (4:5) PNG |
| hero_story_1080x1920.png has exact story dimensions | auto · mandatory · K1 | hero_story_1080x1920.png is exactly 1080 x 1920 px (9:16) PNG |
| founder_cover_graded_1080x1920.png has exact 9:16 cover dimensions | auto · mandatory · K1 | founder_cover_graded_1080x1920.png is exactly 1080 x 1920 px (9:16) PNG |
| logo_vector.svg is a true vector file traced from the raster logo (not an embedded raster) | auto · **dealbreaker** · K1 | logo_vector.svg is a valid SVG containing vector <path> geometry (Illustrator-editable paths), with no embedded <image>/base64 raster bitmap standing in for the artwork |
| logo_transparent.png is a transparent-background cutout of the logo | auto · mandatory · K1 | logo_transparent.png has an alpha channel and the area outside the logo mark/wordmark is fully transparent (alpha=0), not white or off-white filled |
| backdrop_graded.jpg is delivered as a full-resolution JPG (not the watermarked stock comp) | auto · mandatory · K1 | backdrop_graded.jpg is a JPEG file delivered at full resolution with no visible Adobe Stock watermark or comp tiling |
| The product hero subject is cut out of its original busy desk background | expert · mandatory · K3 | In all three hero exports (reel cover, feed, story) the phone-in-hand product subject is cleanly isolated; the original cluttered desk (coffee mug, notebook) is gone with no halo/fringe along the hand and phone edges |
| The product subject is recomposited on brand off-white #F8FAFC | auto · mandatory · K2 | The background fill behind the product subject in the hero exports reads as #F8FAFC, matching the brand off-white hex stated in the brief |
| The founder candid subjects are cut out and placed on brand off-white #F8FAFC | expert · mandatory · K3 | In founder_cover_graded_1080x1920.png both founders are cleanly cut from the busy co-working background (flyaway hair handled) and placed on a #F8FAFC off-white background with no halo/fringe |
| One identical unified indigo brand grade is applied across product, founder, and backdrop so they read as one family | expert · mandatory · K3 | hero exports, founder_cover_graded_1080x1920.png, and backdrop_graded.jpg share a visibly consistent cooler indigo-leaning white balance, lifted shadows, and controlled vibrance — no image is an obvious tonal outlier |
| The grade visibly corrects the founder candid's mixed tungsten/window lighting | expert · quality · K4 | founder_cover_graded_1080x1920.png no longer shows the warm-tungsten vs cool-window color cast of the source founder_candid.jpg; whites read neutral-to-cool and consistent with the hero |
| The square hero short axis was generatively expanded before the 9:16 crop so the product is not clipped | expert · mandatory · K3 | In hero_reel_cover_1080x1920.png and hero_story_1080x1920.png the phone-in-hand product is fully within frame with no important part cropped off; the top/bottom outpaint blends seamlessly with no visible seam or content distortion |
| backdrop_graded.jpg is a licensed stock backdrop (licensed before editing), graded into the family | expert · mandatory · K2 | backdrop_graded.jpg is a clean gradient/studio backdrop sourced from licensed Adobe Stock (no watermark/comp marks) pushed through the same indigo brand grade so it matches the hero/founder family |
| All deliverables trace back to the client-supplied source files, not regenerated or newly designed | expert · **dealbreaker** · K7 | The hero subject derives from product_hero_square.png, the founder subject from founder_candid.jpg, and logo_vector.svg/logo_transparent.png from logo_raster.png (the NIMBUSLY hexagon-arrow indigo wordmark) — no new logo designed and no poster/thumbnail layout or type composition introduced |
| Deliverables are organized into one neatly labelled pack | auto · quality · K6 | instagram_brand_pack.zip is a single archive whose contents are named so each deliverable (reel cover, feed, story, founder cover, backdrop, logo SVG, logo PNG) is clearly identifiable by filename |


[[PAGEBREAK]]
### AO-53 · Pop-Art Duotone Social Launch Kit from a Brand Logo + Hero Shot
**Brand:** Video Editing & Motion Graphics &nbsp;·&nbsp; **Operation:** O6 Stylized & duotone (Photo & Image) &nbsp;·&nbsp; **Horizon:** H3 composite (14 tool calls) &nbsp;·&nbsp; **Capability profile:** K4 · K3 · K1 · K6 · K7
*Turn the client's hero shot and pop-art logo into a reusable duotone/halftone social launch kit: stickers, icons, carousel + reel-cover art, platform-sized posts, and data-merged post variations — all built on Adobe connector tools.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| hero_shot.png | image | Photoreal studio portrait of a stylish young woman in a bright yellow oversized hoodie, mid-laugh, looking sli |
| brand_logo.ai | vector | A flat pop-art brand logo lockup for a fashion label called 'VOLT', bold rounded geometric sans wordmark in ho |
| post_template.ai | vector | A single Instagram-post (1080x1080) Illustrator artboard laid out as a reusable pop-art launch template: large |
| post_copy.csv | data | Generate a CSV with columns headline,subhead,cta and 8 rows of punchy pop-art fashion-launch social copy for a |
| icon_source.png | image | A flat single-color icon sheet of 6 simple pop-art motifs (lightning bolt, starburst, heart, speech bubble, sm |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| hero_cutout.png | image | Transparent-background PNG of the hero subject, full resolution, alpha-matted edges. |
| hero_popart_duotone.png | image | Pop-art hero: halftone print-screen dots recolored to brand magenta (#E6007E) + cyan (#00AEEF) duotone, with punchy color overlay and HSL boost. PNG, sRGB. |
| hero_sticker.svg | vector | Vectorized pop-art subject as a clean, recolorable SVG sticker/icon — scalable with no quality loss. |
| icon_set.svg | vector | 6-motif pop-art icon/sticker pack vectorized to a single SVG (lightning, starburst, heart, speech bubble, smiley, arrow). |
| reel_cover_9x16.png | image | Tall 9:16 reel-cover canvas — pop-art hero outpainted (generative_expand) so nothing important is cropped. PNG. |
| platform_crops/ | image_set | Four exports of the pop-art hero: 1:1 (1080x1080 feed), 4:5 (1080x1350 portrait), 9:16 (1080x1920 story/reel), 2:3 (1000x1500 Pinterest), subject-aware framing. PNG each. |
| brand_logo_export.{png,svg,pdf} | vector | Web-ready exports of the supplied logo .ai (transparent PNG, SVG, PDF) for drop-in across templates. |
| post_variations/ | image_set | 8 data-merged launch post variations (one finished graphic per CSV row) rendered from the authored post_template.ai + post_copy.csv. PDF/PNG. |
| font_pairing.txt | data | Recommended on-brand display + body font pairing with rationale. |
| launch_kit_board | url | A single shareable Firefly board deep-link assembling all kit assets for future remix/reuse. |

**Layer-3 verifier checks** — expert-authored (16 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| hero_cutout.png has a transparent (alpha) background with the hero subject isolated | auto · mandatory · K1 | hero_cutout.png is a PNG with an alpha channel; background pixels are fully transparent (alpha=0) and the subject region is opaque |
| The full deliverable set is present: hero_cutout.png, hero_popart_duotone.png, hero_sticker.svg, icon_set.svg, reel_cover_9x16.png, the platform_crops/ set, brand_logo_export in png+svg+pdf, the post_variations/ set, font_pairing.txt, and a launch_kit_board URL | auto · mandatory · K1 | All 10 named outputs exist; platform_crops/ contains exactly 4 image files, brand_logo_export exists as all three of {.png,.svg,.pdf}, and post_variations/ contains exactly 8 graphics |
| hero_popart_duotone.png is recolored to the exact brand duotone pair: magenta #E6007E and cyan #00AEEF | auto · **dealbreaker** · K2 | Dominant color clusters in hero_popart_duotone.png match magenta #E6007E (RGB 230,0,126) and cyan #00AEEF (RGB 0,174,239) within a small delta-E tolerance; no large off-brand hue regions remain |
| hero_popart_duotone.png shows a visible halftone / print-screen dot pattern | expert · mandatory · K3 | Discrete, regularly spaced halftone dots are clearly visible across the subject (not a smooth continuous-tone image) |
| hero_popart_duotone.png is a PNG in sRGB color space | auto · mandatory · K1 | File is a valid PNG with an embedded sRGB profile or sRGB-tagged data |
| hero_sticker.svg is a true vector file (not a raster image embedded in SVG) so it is recolorable and scales without quality loss | auto · mandatory · K1 | hero_sticker.svg parses as SVG containing vector <path>/<polygon> geometry and no embedded raster <image> bitmap as its primary content |
| icon_set.svg is a single true-vector SVG containing all 6 pop-art motifs: lightning bolt, starburst, heart, speech bubble, smiley, and arrow | expert · mandatory · K1 | icon_set.svg parses as one SVG with vector path geometry (no embedded raster bitmap) and renders 6 distinct, recognizable motifs matching the named set (lightning bolt, starburst, heart, speech bubble, smiley, arrow) |
| reel_cover_9x16.png has a 9:16 aspect ratio with the original artwork extended (outpainted) rather than cropped | auto · mandatory · K1 | reel_cover_9x16.png width:height equals 9:16; the original hero subject is fully present and uncropped, with new generated/extended canvas content above/below or to the sides |
| The four platform_crops/ exports have the exact required pixel dimensions | auto · mandatory · K1 | platform_crops/ contains PNGs at 1080x1080 (1:1), 1080x1350 (4:5), 1080x1920 (9:16), and 1000x1500 (2:3) — exactly one of each |
| Each platform crop keeps the hero subject framed (not cut off) within its ratio | expert · quality · K3 | In all four crops the hero subject's key area (face/upper body) remains within frame and reasonably composed |
| brand_logo_export is the exported supplied VOLT logo, unaltered — the wordmark, magenta/cyan colors and starburst accent match the input brand_logo.ai | expert · **dealbreaker** · K2 | The PNG/SVG/PDF exports reproduce the supplied VOLT logo (hot-magenta wordmark, cyan offset, comic-style starburst accent) faithfully with no regeneration or redesign of the mark |
| post_variations/ contains exactly 8 merged graphics, one per row of post_copy.csv | auto · mandatory · K1 | post_variations/ holds exactly 8 finished graphics (PDF/PNG), matching the 8 CSV rows |
| Each post variation displays the headline, subhead, and cta text from its corresponding post_copy.csv row | auto · mandatory · K1 | For each of the 8 rows, the headline, subhead, and cta values appear (via OCR) on the matching merged graphic, with no missing or mismatched copy |
| font_pairing.txt recommends an on-brand display font AND a separate body font with a written rationale | auto · mandatory · K5 | font_pairing.txt names at least one display font and at least one separate body font and includes a written rationale for the pairing |
| launch_kit_board is a single shareable Firefly board URL assembling the produced kit assets | auto · mandatory · K6 | launch_kit_board is one valid Firefly board deep-link URL, and the board contains the produced deliverables (pop-art duotone hero, sticker, icon set, reel cover, platform crops, logo export, post variations) |
| No disallowed generative steps were used; the only generative operation is the outpaint for the reel cover | expert · mandatory · K7 | Deliverables show no text-to-image, generative fill, object removal, or background-replace-by-prompt; the sole generative step is image_generative_expand for reel_cover_9x16.png |


[[PAGEBREAK]]
### AO-70 · Luxury-prize hero image for a UK raffle brand: stock-source a supercar, isolate it, AI-expand into a premium scene, bold luxury color grade, and export Instagram/Facebook ad crops
**Brand:** Automotive, Industrial & Agriculture &nbsp;·&nbsp; **Operation:** O8 Stock-sourced hero (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (18 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K4 · K1 · K6 · K7
*Build a premium, bold luxury-car prize hero image for a UK raffle brand from a licensed stock supercar — isolate it, AI-expand the canvas into a wider hero scene, apply a bold premium color grade with cinematic depth, and export Instagram and Facebook ad-ready crops plus a clean vector of the brand logo.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| raffle_car_stock_query | data | Output a JSON object with stock-search parameters for an Adobe Stock query for a luxury raffle campaign hero. |
| velvet_wins_logo.png | image | A premium raffle/giveaway brand wordmark logo on a fully transparent background: the words 'VELVET WINS' in a |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| velvet_wins_hero_master.png | image | Master graded luxury-car prize hero plate, AI-expanded wide cinematic composition, full premium color grade + lens-blur depth + subtle grain baked in. Largest available r |
| hero_instagram_1080x1080.png | image | Instagram square crop, exactly 1080x1080 px, car kept as focal subject, graded look preserved. RGB PNG. |
| hero_story_1080x1920.png | image | Instagram/Facebook story-and-reels vertical crop, exactly 1080x1920 px (9:16), car centered with headroom for later headline/CTA. RGB PNG. |
| hero_banner_1920x1080.png | image | Wide website / Facebook banner crop, exactly 1920x1080 px (16:9), car offset with negative space for copy. RGB PNG. |
| velvet_wins_logo.svg | vector | Clean traced vector of the supplied wordmark, scalable SVG, solid color regions preserved, crisp at any banner/billboard scale. |

**Layer-3 verifier checks** — expert-authored (16 checks, 1 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All five required deliverables are present with their exact filenames | auto · mandatory · K1 | Exactly these 5 files are delivered: velvet_wins_hero_master.png, hero_instagram_1080x1080.png, hero_story_1080x1920.png, hero_banner_1920x1080.png, and velvet_wins_logo.svg |
| The Instagram square crop is exactly 1080x1080 pixels | auto · mandatory · K1 | hero_instagram_1080x1080.png reads exactly 1080 px wide x 1080 px tall (1:1) |
| The story/reels vertical crop is exactly 1080x1920 pixels (9:16) | auto · mandatory · K1 | hero_story_1080x1920.png reads exactly 1080 px wide x 1920 px tall (9:16) |
| The wide website/Facebook banner crop is exactly 1920x1080 pixels (16:9) | auto · mandatory · K1 | hero_banner_1920x1080.png reads exactly 1920 px wide x 1080 px tall (16:9) |
| The master graded hero plate is delivered at the largest available resolution and is bigger than every platform crop | auto · mandatory · K1 | velvet_wins_hero_master.png is an RGB PNG measuring at least ~2400 px wide x ~1500 px tall and is larger (in pixel dimensions) than each of the three platform crops |
| All four image deliverables are RGB PNG files (not CMYK, not JPEG) | auto · mandatory · K1 | velvet_wins_hero_master.png, hero_instagram_1080x1080.png, hero_story_1080x1920.png, and hero_banner_1920x1080.png are each valid PNG files in RGB color mode |
| The logo deliverable is a true scalable SVG vector, not a raster image embedded in an SVG wrapper | auto · **dealbreaker** · K1 | velvet_wins_logo.svg is a valid SVG containing traced vector path/shape geometry (<path>/<polygon>/etc.) and contains no embedded raster bitmap (no <image> tag or base64 raster data) |
| The vectorized logo is traced from the supplied Velvet Wins wordmark and preserves its content | expert · mandatory · K2 | velvet_wins_logo.svg clearly reproduces the supplied velvet_wins_logo.png 'VELVET WINS' wordmark (letterforms, the small ticket/diamond glyph to the left, purple-to-magenta fill with a thin gold keyline), with solid/flat color regions preserved and crisp edges at large scale |
| The hero car was licensed from Adobe Stock before any editing, not generated from scratch | expert · mandatory · K6 | The hero subject is a licensed Adobe Stock luxury sports car obtained via a license-and-download step run BEFORE any edit step (license-first ordering), not a from-scratch generated or un-licensed car |
| The hero canvas was AI-expanded (outpainted) into a wider/taller cinematic scene, not built by compositing | expert · mandatory · K3 | velvet_wins_hero_master.png shows the car within an extended/outpainted wider-and-taller scene with breathing room around the car for a later headline/CTA, produced by canvas expansion (outpaint) rather than pasting the isolated car onto a separate background |
| A bold premium luxury color grade is applied: punchy contrast, deep blacks, controlled highlights, slightly cool/teal cast | expert · mandatory · K4 | velvet_wins_hero_master.png reads as a high-contrast premium grade with rich deep blacks, controlled (non-blown) highlights on the glossy bodywork, and a slight cool/teal cast |
| A saturated hero accent is applied selectively to the car's paint colour so the prize pops against the cool background | expert · quality · K4 | The car's paint hue is selectively more saturated/vivid than the surrounding scene (single-hue accent), making the car the standout color accent rather than a uniform global saturation boost |
| Cinematic shallow-depth background blur is present so the car is the focus | expert · quality · K4 | velvet_wins_hero_master.png shows a soft/lens-blurred background relative to a sharp car, giving a shallow-depth-of-field cinematic hero feel |
| A subtle film grain is present so the plate reads premium/editorial rather than flat-digital | expert · quality · K4 | velvet_wins_hero_master.png carries a subtle, even film grain that is visible but not heavy or noisy |
| Each of the three platform crops keeps the car fully framed as the focal subject | expert · mandatory · K3 | In hero_instagram_1080x1080.png, hero_story_1080x1920.png, and hero_banner_1920x1080.png the supercar is fully framed as the dominant focal subject (story crop with headroom, banner crop offset with negative space for copy) and is not cut off or marginalized |
| All three platform crops are cut from the one master and carry the same graded look | expert · quality · K1 | The premium grade, depth blur, and grain of velvet_wins_hero_master.png are consistently preserved across all three crops (same colour, contrast, and treatment), with no crop showing a different or un-graded look |


[[PAGEBREAK]]
### AO-71 · Refresh a VC firm's website visuals: brand-graded stock hero, outpainted to full-bleed, responsive section crops, and vectorized SVG icons
**Brand:** Finance, Crypto & Professional Services &nbsp;·&nbsp; **Operation:** O8 Stock-sourced hero (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (21 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K4 · K1 · K6 · K7
*Take a licensed Adobe Stock business photograph plus three client icon sketches and produce a cohesive VC-website graphics set: a brand-graded full-bleed hero, responsive desktop/tablet/mobile section crops, a tinted section-divider variant, and clean SVG icons — all chained from the licensed source.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| stock_hero_source.jpg | image | Photoreal wide-angle interior of a modern venture-capital firm's glass-walled meeting space at golden hour: fl |
| icon_portfolio_raster.png | image | Flat, single-color minimalist icon of a briefcase/portfolio folder, solid dark-navy fill, centered on a plain |
| icon_growth_raster.png | image | Flat, single-color minimalist icon of an upward growth arrow over three ascending bars, solid dark-navy fill, |
| icon_network_raster.png | image | Flat, single-color minimalist icon of a connected-nodes network (five circles linked by lines), solid dark-nav |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| hero_fullbleed_2560x1080.png | image | Brand-graded, generatively-expanded full-bleed website hero, 2560x1080 (~21:9) PNG, navy/slate/gold palette, web-compression target <200 KB. |
| hero_desktop_2560x1080.png | image | Desktop breakpoint crop, 2560x1080 PNG, subject-aware reframe of the master hero. |
| hero_tablet_1536x1024.png | image | Tablet breakpoint crop, 1536x1024 PNG, subject-aware. |
| hero_mobile_1080x1350.png | image | Mobile portrait breakpoint crop, 1080x1350 (4:5) PNG, subject-aware. |
| section_divider_navy.png | image | Subtle monochromatic navy-tinted low-contrast section-background variant of the hero, PNG. |
| icon_portfolio.svg | vector | Transparent vectorized portfolio icon, clean SVG, <50 KB. |
| icon_growth.svg | vector | Transparent vectorized growth icon, clean SVG, <50 KB. |
| icon_network.svg | vector | Transparent vectorized network icon, clean SVG, <50 KB. |
| font_pairing_recommendation.txt | data | Recommended heading/label typeface pairing for the brand from font_recommend. |
| review_board_link.url | data | Firefly board deep-link assembling all produced hero/crop/icon assets for team review. |

**Layer-3 verifier checks** — expert-authored (15 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| The full-bleed hero deliverable hero_fullbleed_2560x1080.png is exactly 2560x1080 pixels | auto · mandatory · K1 | hero_fullbleed_2560x1080.png reads exactly 2560 (W) x 1080 (H) pixels (~21:9 aspect ratio) |
| All hero deliverables (full-bleed master + 3 responsive crops) are delivered in valid PNG format at their exact required dimensions | auto · mandatory · K1 | hero_fullbleed_2560x1080.png == 2560x1080, hero_desktop_2560x1080.png == 2560x1080, hero_tablet_1536x1024.png == 1536x1024, hero_mobile_1080x1350.png == 1080x1350; each decodes as a valid PNG (magic bytes 89 50 4E 47) |
| The full set of 10 deliverables is present: full-bleed hero, 3 responsive crops, 1 section divider, 3 icon SVGs, font-pairing recommendation, and review board link | auto · mandatory · K1 | All of hero_fullbleed_2560x1080.png, hero_desktop_2560x1080.png, hero_tablet_1536x1024.png, hero_mobile_1080x1350.png, section_divider_navy.png, icon_portfolio.svg, icon_growth.svg, icon_network.svg, font_pairing_recommendation.txt, and review_board_link.url exist (10 artifacts) |
| Each of the three icon deliverables is a valid SVG vector file under the stated 50 KB icon byte budget | auto · mandatory · K1 | icon_portfolio.svg, icon_growth.svg, icon_network.svg each parse as well-formed SVG (contain an <svg ...> root with vector path data) and each file is under 50 KB (51200 bytes) |
| The full-bleed hero PNG meets the stated web-compression byte target for hero visuals | auto · quality · K1 | hero_fullbleed_2560x1080.png file size is under 200 KB (204800 bytes); spec states this as a '<200 KB target after web compression', so treat as a polish target not an acceptance blocker |
| Each icon SVG has a transparent background with no opaque gray #EEEEEE background carried over from the source raster | auto · mandatory · K1 | None of icon_portfolio.svg, icon_growth.svg, icon_network.svg contains a full-canvas opaque fill of the source background gray #EEEEEE; background is transparent with only the navy icon shape painted |
| The hero is sourced from a licensed Adobe Stock photograph rather than generated from scratch | expert · **dealbreaker** · K7 | The graded full-bleed hero is recognizably derived from a licensed stock photo (modern glass/light office or abstract data-light scene, no recognizable faces or readable logos), not a from-scratch text-to-image illustration |
| Stock licensing occurred before any editing, using the full-resolution licensed download rather than an unlicensed watermarked comp | auto · **dealbreaker** · K6 | Workflow log shows asset_license_and_download_stock executed before any image_* grading/edit step, and the edited hero derives from the full-resolution licensed download (no Adobe Stock watermark present in the graded hero) |
| The hero is color-graded to the stated brand palette (deep navy #0B1F3A primary, slate #2E3A4D, warm gold #C8A24B accent) | expert · mandatory · K4 | The graded hero reads on-brand: shadows/blues pushed toward navy #0B1F3A with slate #2E3A4D midtones and the warm gold #C8A24B accent preserved rather than neutralized; image reads navy-on-brand, not warm-generic |
| The full-bleed hero was created by generatively expanding/outpainting the graded crop to 2560x1080 with photographically consistent new edges | expert · mandatory · K3 | The 2560x1080 hero shows extended canvas beyond the original stock crop where outpainted regions match the source in lighting, perspective, grain, and content with no visible seam, stretch, or repeat artifact |
| Each responsive crop preserves the hero's focal subject area across the reframe | expert · quality · K3 | Desktop (2560x1080), tablet (1536x1024, 4:3-ish), and mobile (1080x1350, 4:5 portrait) crops each keep the main focal area of the master hero in frame and well-composed, not cutting off or marooning the subject |
| The section-divider variant is a subtle monochromatic navy-tinted, low-contrast version of the hero | expert · mandatory · K4 | section_divider_navy.png reads as a single-hue navy monochromatic, low-contrast background graphic derived from the hero — muted enough to sit behind content, not a full-contrast duplicate of the hero |
| Each vectorized icon faithfully reproduces its client-supplied source shape with clean paths | expert · mandatory · K2 | icon_portfolio.svg = briefcase/portfolio folder, icon_growth.svg = upward arrow over three ascending bars, icon_network.svg = five connected nodes; each crisp with clean closed paths and no knockout halo or broken connector lines |
| A heading/label font-pairing recommendation for the brand is provided | expert · mandatory · K5 | font_pairing_recommendation.txt names a specific heading typeface plus a label/body typeface pairing appropriate for a credibility-forward VC brand |
| All produced deliverables are uploaded to a shared CC folder and assembled into a Firefly review board for team hand-off | auto · mandatory · K6 | review_board_link.url contains a resolvable Firefly board URL, and the workflow log shows the produced assets (hero, 3 crops, divider, 3 SVG icons) uploaded to CC storage (asset_finalize_file_upload) and assembled into the board (create_firefly_board) |


[[PAGEBREAK]]
### AO-72 · Modern Store Graphics Package — Hero Banner, PDP Assets & Store Decoration
**Brand:** Party, Events & Promotion &nbsp;·&nbsp; **Operation:** O8 Stock-sourced hero (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (24 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K4 · K1 · K6 · K7
*Turn the client's product hero shot, stock backdrop, brand palette, and two authored source templates into a cohesive modern-storefront graphics package: a desktop + mobile hero banner, clean PDP image frames and vector icon/divider assets, and tied-together decoration — delivered as layered source exports plus optimized JPG/PNG.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| product_hero_shot.jpg | image | Photoreal studio product hero shot of a single premium matte-ceramic pour-over coffee dripper in deep ink-navy |
| product_crop_features.jpg | image | Three tight macro product crops on warm-sand surface: the dripper's ribbed cone, its drip spout, and the cork- |
| store_banner_layout.indd | vector | Authored InDesign banner layout source: a 1920x720 desktop hero artboard with a placed logo lockup top-left, a |
| icon_divider_sheet.ai | vector | Authored Illustrator source sheet: a tidy artboard of 8 thin-line modern e-commerce icons (truck/free-shipping |
| brand_palette_copy.csv | data | Generate a small brand spec CSV with rows: hex_primary=#14233B, hex_accent=#E7D3B1, hex_paper=#FAF6EF; banner_ |
| stock_backdrop_query | data | A one-line Adobe Stock search query string: 'minimal modern kitchen counter morning light negative space warm |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| hero_banner_desktop.jpg | image | 1920x720 JPEG, sRGB, optimized for web (<400KB), product on warm-sand with extended negative-space left third, auto-toned and brand-graded; primary store landing hero. |
| hero_banner_mobile.jpg | image | 1080x1350 JPEG, sRGB, vertically extended (outpainted) version of the same hero composition for mobile storefront, optimized <350KB. |
| secondary_banner_panel.jpg | image | 1920x720 JPEG built on the licensed stock backdrop, brand-temperature-matched to the hero, negative-space right side for headline overlay. |
| pdp_frame_set.png | image | Set of 1:1 PDP image frames (1200x1200 PNG) cropped from the product detail macros, consistently toned to match the hero look, clean edges, transparent-safe margins. |
| icon_pack.svg | vector | Clean vectorized icon + divider pack exported from the authored .ai plus one raster-derived accent vectorized to SVG; single-weight deep-ink strokes, transparent, scalabl |
| store_banner_source.indd_export | pdf | Press/preview export (PDF + PNG) of the authored layered banner .indd source, delivered alongside the original layered .indd so the client team can swap text/images. |
| decoration_backgrounds.png | image | Two tileable/section decoration backgrounds (2000x1200 PNG) in brand paper + accent tones with subtle grain, plus the exported section-divider graphics; ties pages togeth |
| store_graphics_package.zip | data | Single labeled ZIP bundling all layered source exports and optimized JPG/PNG/SVG deliverables in clearly named folders (01_banner, 02_pdp, 03_decoration, 00_source). |

**Layer-3 verifier checks** — expert-authored (17 checks, 4 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| Desktop hero banner is delivered at exactly 1920x720 pixels | auto · mandatory · K1 | hero_banner_desktop.jpg is exactly 1920 (W) x 720 (H) px |
| Mobile hero banner is delivered at exactly 1080x1350 pixels | auto · mandatory · K1 | hero_banner_mobile.jpg is exactly 1080 (W) x 1350 (H) px |
| Both hero banner deliverables are JPEG in sRGB and web-optimized to their stated file-size budgets | auto · mandatory · K1 | hero_banner_desktop.jpg is JPEG/sRGB and under 400KB AND hero_banner_mobile.jpg is JPEG/sRGB and under 350KB |
| The secondary banner panel is delivered at exactly 1920x720 JPEG | auto · mandatory · K1 | secondary_banner_panel.jpg is exactly 1920 (W) x 720 (H) px and JPEG format |
| The secondary banner panel is visibly built on the licensed lifestyle stock backdrop, not the product hero, with clear right-side negative space for a headline overlay | expert · mandatory · K1 | secondary_banner_panel.jpg is visibly derived from the minimal-modern-kitchen-counter lifestyle stock backdrop (morning light, warm neutral), brand-temperature-matched to the hero, with negative space kept clear on the RIGHT side for headline overlay; it is not the product hero shot |
| The PDP frame set is delivered as 1:1 PNG frame(s) at 1200x1200 cropped from the supporting product macro crops | auto · mandatory · K1 | pdp_frame_set.png consists of square 1:1 PNG frame(s) at exactly 1200x1200 px sourced from product_crop_features.jpg macros (ribbed cone, drip spout, cork-handle detail) |
| The icon pack is delivered as a valid transparent SVG containing the authored .ai icon/divider set plus one raster-derived vectorized accent | auto · mandatory · K1 | icon_pack.svg is a valid SVG with transparent background containing the icon+divider geometry exported from icon_divider_sheet.ai, plus at least one additional motif vectorized from a graded product crop (image_vectorize output) |
| The store banner source deliverable includes a PDF + PNG export of the authored .indd AND the original layered .indd delivered alongside | auto · mandatory · K1 | store_banner_source.indd_export contains both a PDF export and a PNG export of store_banner_layout.indd, delivered together with the original layered .indd source file |
| Decoration backgrounds are delivered as two 2000x1200 PNG section backgrounds plus the exported section-divider graphics | auto · mandatory · K1 | decoration_backgrounds.png deliverable = two PNG backgrounds each exactly 2000x1200 px in brand paper/accent tones, accompanied by the exported section-divider graphics |
| Every deliverable is bundled into one labeled ZIP using the exact named folders specified | auto · mandatory · K6 | store_graphics_package.zip contains all layered source exports and optimized JPG/PNG/SVG deliverables organized into folders named exactly 00_source, 01_banner, 02_pdp, 03_decoration |
| The brand palette is applied using the exact supplied hex values for ink, sand, and paper | auto · **dealbreaker** · K2 | Deliverables use deep-ink #14233B and warm-sand #E7D3B1, and the decoration background solid fill uses brand paper #FAF6EF, exactly as given in brand_palette_copy.csv |
| The secondary banner backdrop is a genuinely licensed Adobe Stock image, licensed before any editing | expert · **dealbreaker** · K7 | The backdrop underlying secondary_banner_panel.jpg traces to an asset_license_and_download_stock result for the query 'minimal modern kitchen counter morning light negative space warm neutral lifestyle', not a fabricated or unlicensed image |
| The desktop hero is produced by generatively expanding (outpainting) the single client product hero shot, not by inserting a different product image | expert · **dealbreaker** · K2 | hero_banner_desktop.jpg shows the same matte-ceramic deep-ink-navy pour-over dripper from product_hero_shot.jpg, with the warm-sand negative space extended on the left third via image_generative_expand outpaint and no regenerated or substituted product |
| The authored .ai and .indd sources are EXPORTED faithfully, not re-drawn or re-composed by the agent | expert · **dealbreaker** · K2 | icon_pack.svg/divider graphics match the authored icon_divider_sheet.ai icon library (8 thin-line icons + 3 section dividers + accent flourishes), and the banner source export matches the authored store_banner_layout.indd (logo lockup, headline/CTA frames, image frame), with no invented or altered layout content |
| A single consistent master grade is propagated across the hero, secondary panel, and PDP macros so the package reads as shot together | expert · quality · K3 | hero_banner_desktop.jpg, hero_banner_mobile.jpg, secondary_banner_panel.jpg, and pdp_frame_set.png share a cohesive warm-temperature grade consistent with the hero master look |
| The package realizes the stated art direction: clean lines, bold-but-balanced color, plenty of negative space, nothing fussy or ornamental | expert · quality · K4 | Across all deliverables the design is minimal and uncluttered with generous negative space, restrained/balanced color, single-weight clean line work, and no fussy ornamentation |
| The decoration backgrounds carry subtle film grain for a tactile non-flat finish rather than a perfectly flat solid fill | expert · quality · K3 | The two decoration backgrounds show a subtle grain texture over the brand paper/accent solid fill, giving a tactile modern finish rather than a flat solid color |


[[PAGEBREAK]]
### AO-73 · Lawn-Care Social Ad Pack: Grade + Outpaint a Stock Hero into 1080x1080 and 1200x628 FB/IG Ad Creatives
**Brand:** Real Estate, Construction & Property &nbsp;·&nbsp; **Operation:** O8 Stock-sourced hero (Photo & Image) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (17 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K4 · K1 · K6 · K7
*Take the client's supplied lawn-care messaging, brand colors, and a licensed Adobe Stock hero photo, then grade it, pop the lawn green, AI-expand it into both 1080x1080 and 1200x628 ad canvases, build a brand-duotone carousel variant, vectorize the logo, and deliver the finished ad-creative image set for Facebook/Instagram.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| lawn_hero_search_intent | data | Output a short JSON object describing the Adobe Stock search the designer will run for a lawn-care Facebook/In |
| client_lawncare_stock_hero | image | Photoreal documentary photograph, 3000x3000 square, of a real landscaper in a plain work polo and cap pushing |
| client_wordmark_logo | image | Clean flat vector-style company word-mark on a transparent/solid white background reading 'GREENBLADE LAWN CAR |
| brand_kit_spec | data | Output a small JSON brand sheet for the lawn-care client: {"brand_green":"#1F5C2E","accent_yellow":"#F4C430"," |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| ad_hero_square_1080 | image | PNG, 1080x1080, sRGB. Graded, lawn-green-popped, AI-outpainted-to-square lawn-care hero — the square Facebook/Instagram feed ad base. |
| ad_hero_landscape_1200x628 | image | PNG, 1200x628, sRGB. Same graded hero AI-outpainted to the 1.91:1 landscape ad canvas (subject preserved, not cropped) — the landscape FB/IG link-ad base. |
| ad_carousel_brand_duotone | image | PNG, 1080x1080, sRGB. On-brand carousel slide: graded hero with the #1F5C2E turf-green brand duotone/color treatment applied for a stylized branded slide. |
| greenblade_logo_vector | vector | SVG, scalable, single-color #1F5C2E word-mark + grass-blade icon vectorized from the client logo raster for crisp placement at any ad size. |
| review_board_and_folder | data | A Firefly Board deep-link presenting all working + final assets for client review, plus a shared CC folder containing the three final ad PNGs and the logo SVG, ready for |

**Layer-3 verifier checks** — expert-authored (16 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| Square ad hero deliverable (ad_hero_square_1080) is exactly 1080x1080 pixels | auto · mandatory · K1 | ad_hero_square_1080 PNG measures exactly 1080 px wide x 1080 px tall (1:1) |
| Landscape ad hero deliverable (ad_hero_landscape_1200x628) is exactly 1200x628 pixels | auto · mandatory · K1 | ad_hero_landscape_1200x628 PNG measures exactly 1200 px wide x 628 px tall (~1.91:1) |
| Carousel brand-duotone deliverable (ad_carousel_brand_duotone) is exactly 1080x1080 pixels | auto · mandatory · K1 | ad_carousel_brand_duotone PNG measures exactly 1080 px wide x 1080 px tall (1:1) |
| The three ad creatives are delivered as PNG files in sRGB | auto · **dealbreaker** · K1 | ad_hero_square_1080, ad_hero_landscape_1200x628, and ad_carousel_brand_duotone are all PNG format in sRGB color space |
| All four required deliverable files are present (three ad PNGs plus the logo SVG) | auto · mandatory · K1 | The deliverable set contains all four files: ad_hero_square_1080 (1080x1080 PNG), ad_hero_landscape_1200x628 (1200x628 PNG), ad_carousel_brand_duotone (1080x1080 PNG), and greenblade_logo_vector (SVG) |
| The client word-mark is delivered as a scalable SVG vector, not an embedded raster | auto · mandatory · K1 | greenblade_logo_vector is a valid SVG file whose artwork is vector path/shape data (e.g. <path>/<polygon> elements), with no embedded raster bitmap (no <image>/base64 PNG-JPEG payload) standing in for the logo |
| The vectorized logo faithfully reproduces the supplied client word-mark in single-color #1F5C2E | expert · **dealbreaker** · K2 | greenblade_logo_vector renders the 'GREENBLADE LAWN CARE' lettering and the grass-blade icon in the brand turf-green #1F5C2E, matching the supplied client_wordmark_logo art without altering the letterforms, spelling, or icon (no regeneration or restyling of the mark) |
| The carousel duotone is built on the supplied brand turf-green #1F5C2E | expert · mandatory · K2 | ad_carousel_brand_duotone shows a monochromatic/duotone treatment built on the deep turf-green brand color #1F5C2E (not an arbitrary or off-brand green) |
| Both square and landscape ad bases are derived from the SAME graded hero photo | expert · mandatory · K1 | ad_hero_square_1080 and ad_hero_landscape_1200x628 visibly depict the same lawn-care hero scene/subject (the same landscaper-mowing-a-lawn photo), not two different images |
| The 1080x1080 and 1200x628 formats were produced by AI outpaint that EXTENDS rather than crops the hero subject | expert · mandatory · K3 | In both ad_hero_square_1080 and ad_hero_landscape_1200x628 the landscaper subject is preserved fully in frame and the added canvas extends the lawn/sky/scene outward with seamless continuation, rather than the subject being cropped to fit the aspect ratio |
| The hero photo reads as a clean, bright, professionally graded image | expert · quality · K4 | The graded hero shows a balanced bright/premium tonal grade — warm sunny color temperature, controlled highlights, lifted shadows — with no blown-out sky or crushed blacks |
| The lawn green is selectively boosted to look lush without over-saturating sky or skin | expert · mandatory · K3 | The grass/turf reads as lush and saturated green while the sky and the worker's skin tones remain natural and un-shifted, confirming the green pop is confined to the grass region |
| The outpaint edges and grade are seamless with no visible compositing artifacts | expert · quality · K3 | Extended canvas regions in the square and landscape creatives blend seamlessly with the original frame — no seams, repeated textures, warped grass stripes, or tonal mismatch at the outpaint boundary |
| A shared CC delivery folder contains the three final ad PNGs and the logo SVG | auto · mandatory · K6 | review_board_and_folder includes a shared Creative Cloud folder holding the three final ad PNGs (ad_hero_square_1080, ad_hero_landscape_1200x628, ad_carousel_brand_duotone) plus greenblade_logo_vector |
| A Firefly Board deep-link presents the produced final assets for client review | auto · mandatory · K6 | review_board_and_folder includes a valid Firefly Board deep-link assembling the produced final assets (square, landscape, carousel, logo) as the client-facing review surface |
| The text/CTA typographic lockup is flagged as the human/Express finishing step, not faked into the images | expert · quality · K7 | Delivered ad creatives contain no rendered headline/CTA text baked over the image, and the hand-off notes state the text/CTA lockup is handed to the Express product / human as the final finishing step |


[[PAGEBREAK]]
### AO-45 · Logo Vectorization + Brand Identity Kit — HaulAway (junk removal / vehicle-wrap-ready)
**Brand:** Automotive, Industrial & Agriculture &nbsp;·&nbsp; **Operation:** O7 Vector & screen-print (Vector & Print) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (18 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K1 · K6 · K7
*Vectorize and clean up HaulAway' existing raster logo to print-ready quality, then build the full set of brand variations (master vector, horizontal, stacked, icon-only AB mark, one-color knockouts, a lime-on-black trailer-wrap hero) plus a font + color-usage reference and a presentation board — all wrap/shirt/print ready.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| ab_junk_logo_raw.png | image | A flat, slightly low-resolution company logo PNG for a junk-removal business called 'HaulAway SOLUTIONS'. A bo |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| ab_junk_master_logo.svg | vector | Clean vectorized master lockup (full AB monogram + wordmark + tagline) as scalable SVG with crisp paths, transparent background; the print-ready master from which AI/EPS/ |
| ab_junk_icon_mark.svg | vector | Icon-only 'AB' monogram, isolated (wordmark removed via select→invert→solid-fill) and vectorized; transparent background; for app icons, magnets, embroidery. |
| ab_junk_mark_oneclr_black_on_light.png | image | One-color knockout: solid black AB mark on transparent/light, hi-res PNG for single-color print, stamps, light-shirt screen-print. |
| ab_junk_mark_oneclr_white_on_dark.png | image | One-color knockout: solid white AB mark on transparent (for dark backgrounds), hi-res PNG for dark-shirt print and dark wrap panels. |
| ab_junk_horizontal_lockup.png | image | Horizontal layout version, cropped to true content bounds, transparent hi-res PNG sized for vehicle door / business-card horizontal use. |
| ab_junk_stacked_lockup.png | image | Stacked/vertical (square-ish) layout version cropped tight, transparent hi-res PNG for car magnet and crew-shirt left-chest. |
| ab_junk_trailerwrap_hero.png | image | Creative bonus: high-impact lime-on-black 'trailer wrap hero' treatment of the mark, hi-res PNG meant to splash large across a trailer side. |
| ab_junk_font_usage_guide.json | data | Typography reference: recommended brand font family + heading/body pairing and usage notes from font_recommend, to accompany the kit. |
| ab_junk_brand_board | data | Firefly Board deep-link assembling all produced variations as the client presentation / brand sheet; board notes carry the black/lime/gray hex, CMYK and Pantone callouts |

**Layer-3 verifier checks** — expert-authored (16 checks, 4 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All nine deliverables from expected_outputs are present | auto · mandatory · K1 | Output set contains exactly these 9 named artifacts: ab_junk_master_logo.svg, ab_junk_icon_mark.svg, ab_junk_mark_oneclr_black_on_light.png, ab_junk_mark_oneclr_white_on_dark.png, ab_junk_horizontal_lockup.png, ab_junk_stacked_lockup.png, ab_junk_trailerwrap_hero.png, ab_junk_font_usage_guide.json, and ab_junk_brand_board (Firefly Board deep-link) |
| The master logo deliverable is a true vector SVG produced by image_vectorize, not a raster wrapped in SVG | auto · **dealbreaker** · K1 | ab_junk_master_logo.svg is a valid SVG containing actual <path>/vector geometry (not a single embedded <image> raster) with a transparent background; it is the output of image_vectorize |
| The icon-only mark deliverable is a true vector SVG of the isolated AB monogram only | auto · **dealbreaker** · K1 | ab_junk_icon_mark.svg is a valid SVG with vector <path> geometry and transparent background, containing the AB monogram only — no 'HaulAway SOLUTIONS' wordmark and no 'HAULING • CLEANOUTS • DEMOLITION' tagline paths |
| Master and icon are delivered as editable vector, satisfying the client's explicit rejection of JPG/PNG-only work | auto · **dealbreaker** · K1 | ab_junk_master_logo.svg and ab_junk_icon_mark.svg are both SVG files with editable vector paths; neither is delivered as a JPG or a flat PNG |
| The vectorized logo preserves the supplied AB monogram and wordmark artwork rather than regenerating or redrawing it | expert · **dealbreaker** · K2 | The master and icon vectors visually match the supplied ab_junk_logo_raw.png — same AB monogram shapes and the same 'HaulAway SOLUTIONS' wordmark forms; no generative-fill, object removal, redrawn, or AI-invented logo elements were introduced (workflow uses only trace/clean/mask tools) |
| Brand palette is restricted to black, lime green, and gray | expert · mandatory · K2 | All produced color variations use only black, lime-green (~#9ACD32), and gray; no off-palette colors appear in the master, icon, lockups, knockouts, or trailerwrap hero |
| Black-on-light one-color knockout is a single solid black mark | auto · mandatory · K1 | ab_junk_mark_oneclr_black_on_light.png is a hi-res PNG showing the AB mark in solid black only (single color) on a transparent/light background, produced via a black color overlay on the isolated mark |
| White-on-dark one-color knockout is a single solid white mark for dark backgrounds | auto · mandatory · K1 | ab_junk_mark_oneclr_white_on_dark.png is a hi-res PNG showing the AB mark in solid white only (single color) on a transparent background suitable for dark shirts/wrap panels |
| The near-white #F4F4F2 background is knocked out to true transparency before vectorize, with no halo | auto · mandatory · K1 | The #F4F4F2 background is removed (via image_remove_background) before image_vectorize; ab_junk_master_logo.svg and the transparent PNG lockups have an alpha-transparent background with no white halo/fringe around the artwork |
| Horizontal lockup is cropped tight to the true content bounds in landscape aspect | auto · mandatory · K1 | ab_junk_horizontal_lockup.png is a transparent hi-res PNG cropped to the artwork's true content bounds (minimal surrounding empty margin) in a horizontal/landscape aspect, produced via image_crop_to_bounds on the cleaned master |
| Stacked/vertical lockup is a tight square-ish frame derived from the horizontal lockup | auto · mandatory · K1 | ab_junk_stacked_lockup.png is a transparent hi-res PNG in a square-ish (vertical/stacked) frame cropped tight, derived via image_crop_and_resize from ab_junk_horizontal_lockup.png, suitable for car magnet and left-chest use |
| The ~2.5 degree clockwise scan skew is corrected so logo edges are true | expert · quality · K3 | The straightened logo and downstream deliverables show level, true horizontal/vertical edges with no residual ~2.5° clockwise rotation (corrected via image_auto_straighten before vectorize) |
| Creative-bonus trailer-wrap hero is a high-impact lime-on-black treatment of the mark | expert · quality · K4 | ab_junk_trailerwrap_hero.png renders the AB mark in lime green (~#9ACD32) with a high-contrast black treatment, hi-res, reading as a bold large-scale trailer-wrap hero variation |
| Font/typography usage guide is delivered with a recommended brand font family plus a heading/body pairing and usage notes | auto · mandatory · K1 | ab_junk_font_usage_guide.json contains a recommended brand font family, a heading/body font pairing, and usage notes, produced via font_recommend |
| Brand color sheet carries hex, CMYK, and Pantone callouts for the black/lime/gray palette plus font guidance | expert · mandatory · K5 | The ab_junk_brand_board notes state hex, CMYK, and Pantone values for each of black, lime green, and gray, plus the recommended font guidance |
| Firefly Board assembles every produced visual variation as the client presentation/brand sheet | auto · mandatory · K6 | ab_junk_brand_board is a Firefly Board deep-link assembling exactly the 7 produced visual deliverables: ab_junk_master_logo.svg, ab_junk_icon_mark.svg, ab_junk_mark_oneclr_black_on_light.png, ab_junk_mark_oneclr_white_on_dark.png, ab_junk_horizontal_lockup.png, ab_junk_stacked_lockup.png, and ab_junk_trailerwrap_hero.png |


[[PAGEBREAK]]
### AO-46 · Recreate a Sports Jersey Font (A–Z, 0–9) as Clean Vector SVG / EPS / AI from a Reference Image
**Brand:** Fashion & Apparel &nbsp;·&nbsp; **Operation:** O7 Vector & screen-print (Vector & Print) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (24 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K1 · K6 · K7
*Turn two photographed jersey-font reference sheets (letters A–Z and numbers 0–9) into clean, print-ready vector artwork and deliver SVG + EPS + AI for both sets.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| jersey_letters_sheet.png | image | A flat reference sheet photographed with a phone showing the complete uppercase alphabet A through Z in a bold |
| jersey_numbers_sheet.png | image | A flat reference sheet photographed with a phone showing the digits 0 1 2 3 4 5 6 7 8 9 in the SAME bold athle |
| collar_ink_reference.jpg | image | Extreme close-up macro photo of the woven collar trim of a football jersey, showing the precise printed ink to |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| letters_AZ_clean.svg | vector | Clean traced SVG of the full uppercase A–Z glyph sheet, pure black geometry on transparent ground, tight continuous paths suitable for plotter cutting and DTF separation. |
| numbers_09_clean.svg | vector | Clean traced SVG of the 0–9 digit sheet, matched stroke weight and proportion to the letters SVG, transparent ground. |
| letters_AZ.ai | vector | Adobe Illustrator (.ai) master of the letter set, EXPORTED by the connector from the authored vector built off letters_AZ_clean.svg (single artboard, all glyphs). |
| numbers_09.ai | vector | Adobe Illustrator (.ai) master of the number set, exported from the authored vector built off numbers_09_clean.svg. |
| letters_AZ.eps / numbers_09.eps | vector | EPS exports of each set for legacy DTF/Flex/Flock RIP workflows, derived from the same authored .ai vectors. |
| jersey_font_vector_package.zip | archive | Single organized package: /letters and /numbers folders each containing the SVG + EPS + AI plus a contact-sheet preview PNG. |

**Layer-3 verifier checks** — expert-authored (16 checks, 1 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| letters_AZ_clean.svg deliverable is present and is a valid SVG vector file | auto · mandatory · K1 | A file named letters_AZ_clean.svg exists in the package and parses as valid SVG containing <path> geometry (not an embedded raster <image>), representing the traced uppercase A-Z sheet |
| numbers_09_clean.svg deliverable is present and is a valid SVG vector file | auto · mandatory · K1 | A file named numbers_09_clean.svg exists in the package and parses as valid SVG containing <path> geometry (not an embedded raster <image>), representing the traced 0-9 digit sheet |
| Both .ai masters (letters_AZ.ai and numbers_09.ai) are delivered as genuine single-artboard Adobe Illustrator vector files | auto · mandatory · K1 | Files letters_AZ.ai and numbers_09.ai exist and are valid .ai (Illustrator) files (not a renamed SVG/PDF); each is a single artboard containing its full glyph set authored/exported from the corresponding clean SVG |
| Both .eps masters (letters_AZ.eps and numbers_09.eps) are delivered as EPS vector files | auto · mandatory · K1 | Files letters_AZ.eps and numbers_09.eps exist and are valid EPS vector files derived from the authored .ai vectors (for legacy DTF/Flex/Flock RIP workflows), not embedded raster |
| Every required vector format is produced for BOTH the letter set and the number set (SVG + EPS + AI for each) | auto · mandatory · K1 | All six core vector files exist: letters_AZ_clean.svg, letters_AZ.ai, letters_AZ.eps, numbers_09_clean.svg, numbers_09.ai, numbers_09.eps — no format missing for either set |
| The letter set contains the complete uppercase alphabet A through Z (26 glyphs) | expert · mandatory · K1 | All 26 uppercase glyphs A,B,C,...,Z are present and individually legible in letters_AZ_clean.svg / letters_AZ.ai — none missing, dropped, or merged together |
| The number set contains the complete digit set 0 through 9 (10 glyphs) | expert · mandatory · K1 | All 10 digits 0,1,2,3,4,5,6,7,8,9 are present and individually legible in numbers_09_clean.svg / numbers_09.ai — none missing, dropped, or merged together |
| jersey_font_vector_package.zip is one organized package with the required /letters and /numbers folder structure | auto · mandatory · K6 | A single zip named jersey_font_vector_package.zip exists containing a /letters folder and a /numbers folder, each holding that set's SVG + EPS + AI files |
| Each set folder includes a contact-sheet preview PNG | auto · mandatory · K1 | A contact-sheet preview PNG is present inside both the /letters folder and the /numbers folder of jersey_font_vector_package.zip, per the package spec |
| Vector glyphs are pure black geometry on a transparent ground | auto · mandatory · K1 | letters_AZ_clean.svg and numbers_09_clean.svg render as solid black (#000000) glyph paths on a transparent background, with no white fill plate or opaque ground baked in |
| Vector paths are clean, tight, continuous geometry suitable for Flex/Flock plotter cutting and DTF separation | expert · mandatory · K3 | Glyph outlines are smooth continuous closed paths with no stray nodes, no leftover fabric-weave specks, and no jagged stair-stepping — tight enough to cut on a Flex/Flock plotter and to separate cleanly for DTF |
| Stroke widths are consistent and inter-glyph spacing is even across each glyph set | expert · mandatory · K3 | Within each set the glyphs share a uniform stroke/limb weight and the spacing between glyphs is even, as required for a coherent jersey font |
| The letter set and number set read as one coherent font family (matched stroke weight and proportion) | expert · mandatory · K3 | numbers_09 glyphs match letters_AZ glyphs in stroke weight, outline thickness, height and proportion so the two sheets read as one family — the result of applying the identical cleanup recipe to both branches |
| Fabric and photo artifacts from the reference shots are fully removed before tracing | expert · mandatory · K3 | No knit-fabric texture, lighting gradient, cool color cast, or ~3-degree tilt survives into the vector output — glyph baselines are level and the ground is clean (straighten + auto-tone + temperature + contrast cleanup applied to both sheets) |
| The recreation is original traced vector geometry, not extracted from a proprietary font file | expert · **dealbreaker** · K7 | Glyph geometry is traced/authored from the two supplied reference sheets (raster -> vectorize -> authored .ai), with no embedded or copied outlines lifted from any commercial/proprietary OTF/TTF font |
| The optional OTF/TTF font file is honestly treated as out of scope and not falsely claimed as delivered | expert · quality · K7 | No installable OTF/TTF font is claimed as a produced deliverable; if the OTF/TTF bonus is mentioned, it is honestly flagged as out of connector scope per the brief |


[[PAGEBREAK]]
### AO-47 · Redraw Swimming-Pool Photos into Clean Web-Ready Vector Graphics
**Brand:** General / Cross-Industry Branding & Graphics &nbsp;·&nbsp; **Operation:** O7 Vector & screen-print (Vector & Print) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (29 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K1 · K6 · K7
*Turn three supplied swimming-pool photos into clean, detailed, flat-color vector graphics (SVG + transparent PNG) on a uniform canvas, packaged and shown on a moodboard for the client's website.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| pool_freeform_lagoon.jpg | image | Photoreal amateur real-estate-style photograph of a finished freeform lagoon-style backyard swimming pool, irr |
| pool_infinity_rectangular.jpg | image | Photoreal handheld photograph of a modern rectangular infinity-edge swimming pool overlooking a hillside, dark |
| pool_kidney_residential.jpg | image | Photoreal backyard snapshot of a classic kidney-shaped residential swimming pool with light-blue plaster inter |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| pool_freeform_lagoon_vector.svg | vector | Clean flat-color SVG of the freeform lagoon pool, detailed but path-economical (water, coping, decking, rock feature as distinct flat fills), on a uniform 4:3 canvas, web |
| pool_infinity_rectangular_vector.svg | vector | Flat-color SVG of the rectangular infinity pool, same uniform 4:3 canvas and flat-fill style as the hero, grey+deep-blue palette preserved. |
| pool_kidney_residential_vector.svg | vector | Flat-color SVG of the kidney-shaped pool, same uniform 4:3 canvas and style, light-blue+brick palette preserved. |
| pool_vectors_web_png_set.zip | image | Three matching transparent-background web PNGs (one per vector), exported from the cleaned rasters/SVGs at a uniform canvas size for direct drop-in on the website gallery |
| pool_gallery_approval_board | data | Firefly Boards deep-link assembling the three finished pool vectors (their uploaded asset URNs) into a single moodboard so the client can approve the gallery set in one v |

**Layer-3 verifier checks** — expert-authored (16 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| Three vector SVG files are delivered, one per supplied pool photo, with the exact required names | auto · mandatory · K1 | Exactly three .svg files exist named pool_freeform_lagoon_vector.svg, pool_infinity_rectangular_vector.svg, and pool_kidney_residential_vector.svg |
| Each delivered SVG is genuine vector artwork, not a raster wrapped in an SVG container | auto · **dealbreaker** · K1 | Each of the three .svg files parses as valid SVG and contains true vector path/shape elements (e.g. <path>, <polygon>) with no embedded raster bitmap (no <image> element and no base64 raster data URI) |
| All three vectors share one uniform 4:3 canvas aspect ratio | auto · mandatory · K1 | The viewBox (or width:height) of all three SVGs is identical and equals a 4:3 ratio (within +/-1% tolerance) |
| Each vector is flat-color and path-economical rather than a noisy thousand-path trace | expert · mandatory · K3 | Each SVG renders as clean flat-color fills (water, coping, decking, and the pool feature read as a small number of distinct flat regions) with no speckled noise, gradient banding, or excessive fragmentary paths |
| Each vector accurately and recognisably represents its source pool's geometry | expert · mandatory · K2 | Lagoon SVG reads as a freeform irregular-curved lagoon pool, infinity SVG as a rectangular infinity-edge pool, and kidney SVG as a kidney-shaped pool, each faithful to its source photo's shape |
| The freeform lagoon vector preserves the tan-travertine + turquoise-blue palette of its source photo | expert · quality · K2 | Lagoon SVG fills read as tan/travertine coping-and-decking with clean turquoise-blue water (one or two blues), faithful to pool_freeform_lagoon.jpg and not a foreign palette |
| The infinity-pool vector preserves the grey + deep-blue palette of its source photo | expert · quality · K2 | Infinity SVG fills read as dark-grey coping with deep-blue water, faithful to pool_infinity_rectangular.jpg and distinct from the lagoon's tan/turquoise |
| The kidney-pool vector preserves the light-blue plaster + brick-red coping palette of its source photo | expert · quality · K2 | Kidney SVG fills read as light-blue plaster water with brick-red coping, faithful to pool_kidney_residential.jpg and distinct from the other two pools' palettes |
| The backyard background is knocked out to a solid flat field in every vector | expert · mandatory · K3 | None of the three vectors contain traced backyard clutter (fence, rooftop, hillside, sky, lawn, furniture, plants); the pool-and-deck subject sits on a clean flat solid field |
| A ZIP of three web PNGs is delivered, one matching each pool vector | auto · mandatory · K1 | pool_vectors_web_png_set.zip exists and contains exactly three .png files (one per pool vector) |
| Each delivered web PNG has a transparent background | auto · mandatory · K1 | All three PNGs in pool_vectors_web_png_set.zip carry an alpha channel and the background region is fully transparent (alpha 0) |
| The three web PNGs share a single uniform 4:3 canvas size | auto · mandatory · K1 | All three PNGs have identical pixel dimensions and that size is 4:3 (within +/-1%) |
| A Firefly Boards approval moodboard is delivered as a deep-link | auto · mandatory · K6 | pool_gallery_approval_board is a valid Firefly Boards deep-link URL that opens a board |
| The approval board assembles all three finished pool vectors in one view | expert · mandatory · K6 | The Firefly board displays the three pool-vector assets (lagoon, infinity, kidney) together as a single reviewable gallery set |
| The three vectors are collected into a single delivery project folder in CC storage | auto · quality · K6 | A delivery project folder exists in CC storage and contains the three finished pool-vector SVG assets |
| No new pool content is invented; outputs derive only from the three supplied photos via permitted prep | expert · **dealbreaker** · K7 | Each vector traces back to its supplied source photo (lagoon/infinity/kidney) with no generatively-invented pool, object, or scene element; generative use is limited to outpainting the solid field to the uniform canvas |


[[PAGEBREAK]]
### AO-48 · Convert an AI-Generated Logo into a Clean, Multi-Platform Vector Kit
**Brand:** Technology, SaaS & Startups &nbsp;·&nbsp; **Operation:** O7 Vector & screen-print (Vector & Print) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (19 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K1 · K6 · K7
*Take the client's AI-generated raster logo, clean and de-skew it, isolate the mark on transparency, trace it into a crisp scalable SVG, and derive a full multi-platform vector + raster export kit that stays high-quality at every size and format.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| northwind_ai_logo_raw.png | image | A 1024x1024 PNG of an AI-generated tech startup logo as it would look straight out of an image generator: a te |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| northwind_logo_fullcolor.svg | vector | Transparent full-color vector trace of the cleaned logo mark, teal+charcoal, clean paths, scalable to any size; primary multi-platform deliverable. |
| northwind_logo_onecolor_knockout.svg | vector | Single-color knockout/silhouette vector of the mark (solid fill on flattened field) for one-color print, vinyl, embroidery and small-size favicons. |
| northwind_mark_transparent.png | image | PNG, transparent background, isolated logo mark with edges trimmed to bounds; source for raster exports. |
| northwind_mark_halftone.png | image | Halftone / print-screen duotone treatment of the mark for merch and poster use. |
| northwind_icon_1024.png / header_bug / avatar_512.png | image | Platform-sized crisp PNG exports cropped/resized from the cleaned mark: 1024x1024 app icon, web header bug, and 512x512 social avatar. |
| font_pairing_recommendation | data | Recommended brand-safe font pairing matching the wordmark for extending the identity in decks/docs. |
| Northwind_brand_kit_board + asset folder | data | Firefly Board presentation deep-link assembling all generated deliverables, plus an organized CC asset folder containing every output for client hand-off. |

**Layer-3 verifier checks** — expert-authored (16 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| northwind_logo_fullcolor.svg is delivered as a valid SVG vector file with real paths (not an embedded raster) | auto · **dealbreaker** · K1 | A file named northwind_logo_fullcolor.svg exists, parses as valid SVG markup, and contains vector path/shape elements; it must NOT be a single <image> tag wrapping the raster (i.e. it was genuinely traced via image_vectorize, not the raw PNG re-wrapped) |
| The full-color SVG preserves the source teal-and-charcoal palette | auto · mandatory · K2 | northwind_logo_fullcolor.svg contains fill colors approximating teal #178C8C and charcoal #2B2F33 (within a small tolerance); it is not a single-color or grayscale trace and does not introduce off-palette hues |
| northwind_logo_onecolor_knockout.svg is a single-color solid charcoal knockout/silhouette vector | auto · mandatory · K1 | A file named northwind_logo_onecolor_knockout.svg exists, is valid SVG with vector paths, and uses exactly one solid fill color — a charcoal (~#2B2F33) silhouette with no teal or second hue present |
| northwind_mark_transparent.png is the isolated mark on a transparent background trimmed to bounds | auto · mandatory · K1 | A file named northwind_mark_transparent.png exists, is a PNG with an alpha channel, has fully transparent pixels at its corners (off-white card removed), and the opaque artwork is tightly cropped to the mark's bounding box |
| northwind_mark_halftone.png is a halftone / print-screen treatment of the mark | expert · mandatory · K1 | A file named northwind_mark_halftone.png exists and shows a recognizable halftone/print-screen (visible dot-pattern) duotone rendering of the Northwind Analytics mark suitable for merch/poster use |
| northwind_icon_1024.png is exported at exactly 1024x1024 pixels from the cleaned mark | auto · mandatory · K1 | A PNG app-icon export named northwind_icon_1024.png exists with pixel dimensions exactly 1024 x 1024, derived from the cleaned transparent mark |
| avatar_512.png is exported at exactly 512x512 pixels from the cleaned mark | auto · mandatory · K1 | A PNG social-avatar export named avatar_512.png exists with pixel dimensions exactly 512 x 512, derived from the cleaned transparent mark |
| A web header bug PNG export is delivered in addition to the 1024 icon and 512 avatar | auto · mandatory · K1 | A third platform-sized PNG raster (the web header bug) is present alongside northwind_icon_1024.png and avatar_512.png, cropped/resized from the cleaned mark |
| A brand-safe font pairing recommendation matching the wordmark is provided | expert · mandatory · K1 | A font_pairing_recommendation names a concrete font pairing (heading + body) that plausibly matches the modern semibold sans-serif Northwind Analytics wordmark for extending the identity in decks/docs |
| The supplied raster was de-skewed before tracing so the wordmark baseline is level | expert · mandatory · K3 | The cleaned mark in the SVG and transparent PNG shows the wordmark baseline horizontal — the ~2.5deg clockwise tilt from northwind_ai_logo_raw.png has been corrected, not still tilted |
| The off-white textured/noisy background was cleaned and flattened to even white before isolation | expert · mandatory · K3 | The isolated mark shows no remnant of the faint off-white #F4F2EE textured card, luminance noise, or uneven lighting around the edges; the field behind the mark was flattened to even white before knockout |
| The vector trace edges are clean and crisp, not inheriting the AI soft/anti-aliased edges or noise | expert · quality · K3 | The full-color SVG paths read as sharp, smooth, deliberate vector outlines with no jagged, fuzzy, or noise-speckled edges carried over from the soft AI raster |
| The full-color SVG stays high-quality and legible when scaled to any size | expert · mandatory · K4 | northwind_logo_fullcolor.svg renders crisp with no pixelation at both very small (favicon) and very large (sign/poster) sizes, satisfying the brief's 'remains high-quality across different formats' requirement |
| The client's logo is faithfully reproduced, not regenerated or altered into a different mark | expert · **dealbreaker** · K2 | The vectorized mark matches the supplied Northwind Analytics artwork (three stacked curved wind/data-flow lines to the LEFT of the 'Northwind Analytics' wordmark); glyphs, letterforms, kerning, and icon shape are preserved, not redrawn or reinvented |
| All six rendered deliverables are collected into an organized CC asset folder for hand-off | auto · mandatory · K6 | A CC asset folder named Northwind_Vector_Kit exists containing all six rendered outputs: northwind_logo_fullcolor.svg, northwind_logo_onecolor_knockout.svg, northwind_mark_transparent.png, northwind_mark_halftone.png, northwind_icon_1024.png, and avatar_512.png |
| A shareable Firefly Board presentation deep-link assembling all deliverables is produced | auto · mandatory · K6 | A Firefly Board deep-link (the Northwind brand kit board) is returned that assembles every generated vector and raster deliverable for client review |


[[PAGEBREAK]]
### AO-49 · Evergreen Cannabis Apparel Capsule — Screen-Print Separation & Vector Production Package
**Brand:** Cannabis & Dispensary &nbsp;·&nbsp; **Operation:** O7 Vector & screen-print (Vector & Print) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (20 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K1 · K6 · K7
*Turn the client's hand-painted hero graphic and brand logo into a production-ready, screen-print-separable vector + halftone package locked to the Evergreen purple/black/pink palette, plus an exported tech-pack mockup, bundled for the decorator.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| hero_crest_scan.png | image | A high-resolution flatbed-scanner capture of a hand-painted illustration on cream textured watercolor paper: a |
| evergreen_la_wordmark.png | image | A flat bitmap PNG of the wordmark 'Evergreen' set in a confident high-contrast condensed serif, solid deep-pur |
| grunge_paper_texture.jpg | image | A seamless subtle grunge paper texture: light worn fibrous off-white paper with faint scuffs, speckle and unev |
| evergreen_la_techpack_template.ai | vector | An authored Adobe Illustrator (.ai) garment tech-pack template: a flat front view of a premium heavyweight cre |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| crest_vector_seps.svg | vector | Clean print-ready vector of the hero crest (transparent), spot-color-friendly flat shapes locked to #4B2E83 / #0B0B0B / #E8669E — the screen-print separation art the deco |
| crest_halftone_distress.png | image | Halftone/duotone-screened raster variant of the crest (purple/black) for the distressed-overlay look, transparent PNG, print resolution. |
| wordmark_vector.svg | vector | Vectorized Evergreen wordmark, scalable solid-purple line art for embroidery/print handoff. |
| evergreen_la_techpack_mockup.pdf | pdf | Exported tech-pack/placement mockup from the authored .ai garment template, showing chest print placement and color callouts. |
| Evergreen_Capsule_PrintPackage.zip | archive | Single decorator handoff bundle containing the two vectors, the halftone PNG, the cleaned transparent crest, and the tech-pack PDF. |

**Layer-3 verifier checks** — expert-authored (16 checks, 3 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All five expected deliverables are present in the handoff with their exact names: crest_vector_seps.svg, crest_halftone_distress.png, wordmark_vector.svg, evergreen_la_techpack_mockup.pdf, and Evergreen_Capsule_PrintPackage.zip | auto · mandatory · K1 | All 5 named files exist with exactly these filenames and extensions (crest_vector_seps.svg, crest_halftone_distress.png, wordmark_vector.svg, evergreen_la_techpack_mockup.pdf, Evergreen_Capsule_PrintPackage.zip); missing any one fails |
| Evergreen_Capsule_PrintPackage.zip is a single archive containing exactly the five required handoff items: crest_vector_seps.svg, crest_halftone_distress.png, wordmark_vector.svg, the cleaned transparent crest, and evergreen_la_techpack_mockup.pdf | auto · mandatory · K1 | Container is a valid .zip; unzipping yields exactly 5 items — the two vectors (crest_vector_seps.svg, wordmark_vector.svg), the halftone PNG (crest_halftone_distress.png), the cleaned transparent crest, and the tech-pack PDF (evergreen_la_techpack_mockup.pdf); fewer items or a non-zip container fails |
| crest_vector_seps.svg is a true vector file (SVG path/shape geometry, not an embedded raster) | auto · **dealbreaker** · K1 | File parses as SVG containing vector <path>/<polygon>/<shape> geometry with no embedded raster <image> bitmap standing in for the crest artwork |
| crest_vector_seps.svg colors are locked to the Evergreen brand palette only: purple #4B2E83, black #0B0B0B, accent pink #E8669E | auto · **dealbreaker** · K2 | Every fill/stroke color in the SVG maps to #4B2E83, #0B0B0B, or #E8669E within tight tolerance; any off-palette color (e.g. the original hand-mixed magenta/teal accents) fails |
| crest_vector_seps.svg has a transparent background (no opaque paper/cream fill behind the crest) | auto · mandatory · K1 | SVG has no full-canvas opaque background rectangle; the area outside the mountain/lotus crest subject is transparent |
| crest_halftone_distress.png is a transparent PNG rendered as a purple/black halftone-screened variant of the crest | auto · mandatory · K1 | File is a PNG with an alpha channel (transparent background) and exhibits a halftone dot/screen pattern using only purple (#4B2E83) and black (#0B0B0B) tones; full-color or opaque-background output fails |
| crest_halftone_distress.png is at print resolution | auto · quality · K1 | Image pixel dimensions / DPI metadata indicate print-grade resolution (>=300 DPI at intended chest-print size), not a low-res screen preview |
| wordmark_vector.svg is a vector file with fill color solid purple #4B2E83 (scalable solid-purple line art) | auto · mandatory · K1 | File is SVG with vector <path> geometry (no embedded bitmap) and its fill color is solid purple #4B2E83 within tight tolerance |
| evergreen_la_techpack_mockup.pdf is a valid PDF whose color-callout strip references the Evergreen palette hex values #4B2E83, #0B0B0B, and #E8669E | auto · mandatory · K1 | File is a valid PDF; OCR of the page recovers the color-callout strip containing the strings #4B2E83, #0B0B0B, and #E8669E (or 4B2E83 / 0B0B0B / E8669E); a PDF missing the color callouts fails |
| evergreen_la_techpack_mockup.pdf shows the garment front view with the centered-chest print-placement box and print-size callout, exported from the authored .ai template | expert · mandatory · K1 | PDF page shows the flat garment front view with a labelled centered-chest print-placement box and a print-location/size spec callout (per the authored ~11in-wide centered-chest placement); no placement box or no garment view fails |
| The wordmark in wordmark_vector.svg matches the supplied client 'Evergreen' wordmark (not a regenerated, retyped, or font-substituted logo) | expert · **dealbreaker** · K2 | Vectorized letterforms preserve the supplied condensed high-contrast serif 'Evergreen' wordmark shapes and proportions; redrawn, retyped, or font-substituted lettering fails |
| The scanned hero crest was straightened from its ~3-degree rotation and tightly cropped to the artwork bounds | expert · mandatory · K3 | The crest in the cleaned transparent output and vector sits level with no residual tilt, and the uneven cream paper margins are removed (tight crop to artwork bounds); visible rotation or leftover margin fails |
| The warm/yellow scanner cast was corrected to a clean neutral tone so the brand purples read true | expert · mandatory · K3 | Cleaned crest shows neutral tone with no yellow/warm cast and purples read true rather than muddy; residual warm cast fails |
| Stray off-palette hand-mixed magenta/teal accents were collapsed onto the locked palette (filled with brand purple #4B2E83) | expert · mandatory · K2 | No magenta/teal or other off-palette colors remain in the cleaned crest or vector; the stray accent regions are collapsed to brand purple #4B2E83 |
| The crest is isolated from its paper background to a clean transparent subject suitable for separations | expert · mandatory · K3 | The cleaned transparent crest has clean, accurate edges with no paper texture, halo, or background fringe remaining around the mountain/lotus crest |
| The final artwork reads as premium and confident elevated-streetwear, never cartoonish or cheap | expert · quality · K4 | Holistic review of the vector seps and halftone variant judges them premium and confident on the purple-and-black-forward brand direction; cartoonish, muddy, or cheap output fails |


[[PAGEBREAK]]
### AO-51 · Vanguard Athletic Logo — Spot-Color Separation, Vectorization & Multi-Format Screen-Print Package
**Brand:** General / Cross-Industry Branding & Graphics &nbsp;·&nbsp; **Operation:** O7 Vector & screen-print (Vector & Print) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (23 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K1 · K6 · K7
*Refine my ChatGPT-made "Vanguard" athletic badge into clean, separated spot-color screen-print artwork (olive drab / khaki / black / dark grey + digital camo), vectorize it, and deliver it in multiple file formats with spot-color info.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| vanguard_badge_chatgpt_raster.png | image | A flat 2D athletic team emblem badge titled 'VANGUARD' in bold condensed uppercase military stencil lettering |
| digital_camo_swatch.png | image | A seamless digital (pixelated MARPAT-style) camouflage pattern swatch using olive drab green, khaki tan, dark |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| vanguard_separations_source.ai | vector | Genuine layered Adobe Illustrator (.ai) vector source with each named mark (VANGUARD wordmark, subdued flag, star, chevrons, head, badge ring) as a separable element, eac |
| vanguard_badge_vector.svg | vector | Clean scalable SVG of the cleaned/spot-reduced badge (from image_vectorize), suitable for social and re-coloring. |
| vanguard_press_export.pdf | pdf | Press-ready PDF exported from the genuine .ai via document_render_vector (all artboards). |
| vanguard_social.png | image | High-res transparent-or-flat PNG of the finished badge for social media. |
| vanguard_black_plate.png | image | Single-color black knockout/plate raster (badge filled flat black on transparent) for the press black separation. |
| digital_camo_accent.svg | vector | Vectorized digital-camo accent swatch (from image_vectorize) for use as a repeatable fill/accent. |
| spot_color_reference.txt | data | Spot-color reference note: which solid ink each named element is locked to + recommended military font, packaged with the deliverables. |

**Layer-3 verifier checks** — expert-authored (16 checks, 1 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| A layered Adobe Illustrator (.ai) vector source named vanguard_separations_source.ai is delivered | auto · mandatory · K1 | A file named vanguard_separations_source.ai exists in the delivery and opens as a valid Adobe Illustrator (.ai) vector document |
| The .ai source keeps each of the six named marks as a separable element with re-editable outline/stroke/fill | expert · mandatory · K1 | In vanguard_separations_source.ai the VANGUARD wordmark, subdued American flag, star icon, chevrons, soldier head, and outer badge ring are each present as a distinct separable element whose outline/stroke/fill colors can be edited independently (not flattened into one merged shape) |
| Each named mark is locked to exactly one solid spot ink drawn only from the military palette {olive drab, khaki, black, dark grey} | expert · mandatory · K3 | Every named element renders as a single flat solid fill (no gradients, no anti-aliased multi-color fuzz) and every ink used is one of olive drab, khaki, black, or dark grey — no color outside that four-ink palette |
| A clean scalable SVG of the spot-reduced badge named vanguard_badge_vector.svg is delivered | auto · mandatory · K1 | A file named vanguard_badge_vector.svg exists, parses as valid SVG vector geometry (path/shape elements, not an embedded raster image), and depicts the cleaned spot-reduced Vanguard badge |
| A press-ready PDF named vanguard_press_export.pdf is delivered | auto · mandatory · K1 | A file named vanguard_press_export.pdf exists and is a valid PDF exported from the vector source with all artboards present |
| A high-res social PNG named vanguard_social.png is delivered | auto · mandatory · K1 | A file named vanguard_social.png exists, is a valid high-res PNG of the finished badge cropped tight to its bounds, with a transparent or flat background |
| A single-color black knockout/plate raster named vanguard_black_plate.png is delivered | auto · mandatory · K1 | A file named vanguard_black_plate.png exists as a valid PNG showing the badge as a flat single-color black plate on transparent background |
| The black plate is a genuine single-ink black separation with no other colors present | expert · mandatory · K3 | vanguard_black_plate.png contains only flat black artwork on transparency — no olive, khaki, grey, anti-aliased color edges, or residual palette colors |
| A vectorized digital-camo accent swatch named digital_camo_accent.svg is delivered | auto · mandatory · K1 | A file named digital_camo_accent.svg exists, parses as valid SVG vector geometry (path/shape elements, not an embedded raster), and represents the pixelated/digital camo swatch as a repeatable accent fill |
| The digital-camo accent SVG uses only the four military palette colors and matches the supplied swatch | expert · quality · K2 | digital_camo_accent.svg is built from olive drab green, khaki tan, dark grey, and black pixel clusters only, matching the supplied digital_camo_swatch.png pattern, with no colors outside that four-ink palette |
| A spot-color reference note named spot_color_reference.txt is delivered and maps each named element to its assigned spot ink | auto · mandatory · K1 | A file named spot_color_reference.txt exists and explicitly maps each of the six named elements (VANGUARD wordmark, subdued flag, star, chevrons, soldier head, badge ring) to its assigned spot ink from {olive drab, khaki, black, dark grey} |
| The spot-color reference note includes a recommended military/stencil-style font for the VANGUARD wordmark | auto · mandatory · K1 | spot_color_reference.txt names a specific military/stencil-style font recommendation for the VANGUARD wordmark |
| The VANGUARD wordmark reads as legible uppercase lettering preserved from the source badge | expert · mandatory · K2 | In the finished badge artwork the wordmark legibly reads 'VANGUARD' in uppercase, matching the supplied vanguard_badge_chatgpt_raster.png (not regenerated into different text or garbled) |
| The badge is straightened and tonally corrected so the source tilt and dull contrast are resolved | expert · quality · K3 | The finished badge sits square/upright (the faint ~2-degree source tilt from vanguard_badge_chatgpt_raster.png is corrected) and the palette reads true and crisp with no residual dull low-contrast muddiness or anti-aliased fuzzy color edges |
| The badge identity from the ChatGPT source is preserved — same six elements, not a regenerated different logo | expert · **dealbreaker** · K2 | The finished badge depicts the same combined emblem as the supplied vanguard_badge_chatgpt_raster.png (outer ring, subdued American flag, single five-point star, three downward chevrons, left-facing soldier/minuteman head, VANGUARD wordmark) refined — not an AI-regenerated alternate design |
| All seven specified deliverables are present in the handoff package | auto · mandatory · K1 | The delivery folder contains all of: vanguard_separations_source.ai, vanguard_badge_vector.svg, vanguard_press_export.pdf, vanguard_social.png, vanguard_black_plate.png, digital_camo_accent.svg, and spot_color_reference.txt |


[[PAGEBREAK]]
### AO-52 · 20th-Anniversary folk-art poster screen-print separation pack — approved master vectorized, white underbase + 4 spot-colour halftone plates with dot-gain choke, a grain-textured proof, the authored registration sheet rendered out of Illustrator, and a campus-reference Firefly board
**Brand:** Nonprofit, Religious &amp; Community &nbsp;·&nbsp; **Operation:** O7 Vector & screen-print (Vector & Print) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (17 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K1 · K6 · K7
*From the approved folk-art 20th-Anniversary master, produce a print-ready 5-screen separation pack (white underbase + four spot-colour halftone plates with a dot-gain choke), a vectorized hard-edge lettering/line plate, a grain-textured client proof, the registration/separation sheet rendered out of the supplied Illustrator template, and a Firefly board of the campus reference photos for the screen printer.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| approved_master_poster.png | image | A handcrafted folk-art / festival-poster style illustration celebrating a Catholic classical school's 20th ann |
| campus_chapel.jpg | image | A candid documentary photo of a small Catholic school chapel exterior in Lafayette, Louisiana — warm brick and |
| campus_oak_quad.jpg | image | A candid documentary photo of a school courtyard quad lined with large Southern live oaks draped in Spanish mo |
| campus_schoolhouse_and_foundingclass.jpg | image | A candid documentary photo of a modest classical schoolhouse facade with a small founding-class group portrait |
| separations.ai | vector | Generate a realistic Adobe Illustrator separation/registration sheet template description and accompanying .ai |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| plate_white_underbase.png | image | White underbase separation, 24x36in @300dpi, solid fill behind all printable art on transparency — first screen down on cream stock. |
| plate_marian_blue_halftone.png | image | Marian Blue spot plate: Ben-Day halftone dot field over the tonal folk-art passages, dot-gain choked, lettering held out solid; trim/registration identical to all plates. |
| plate_antique_gold_halftone.png | image | Antique Gold spot plate, same registered halftone geometry, choked, on its colour build. |
| plate_brick_red_halftone.png | image | Brick Red spot plate, same registered halftone geometry, choked. |
| plate_ink_black_lettering.png | image | Ink Black plate carrying the vectorized hard-edge title/year lettering and key line-work as solid (no dots) plus the darkest tonal dots. |
| lettering_lineart.svg | vector | Vectorized clean SVG of the hard-edge commemorative lettering and key line-work — the hold-out master that keeps type crisp across screens and scales to wall size. |
| client_proof_grain.png | image | Single flattened client proof of the assembled look with screen-print grain/tooth on cream stock, for sign-off before burning screens. |
| separation_registration_sheet.pdf | pdf | Registration/separation sheet rendered from the authored separations.ai: all five labelled artboards with crop/reg marks + ink names, plus matching PNG and SVG exports fo |
| campus_reference_board | url | Firefly Boards deep-link moodboard collecting the four campus reference photos so the printer can colour-match landmarks (chapel brick, oak greens, gold). |

**Layer-3 verifier checks** — expert-authored (16 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| The separation pack contains exactly five plate raster outputs named plate_white_underbase.png, plate_marian_blue_halftone.png, plate_antique_gold_halftone.png, plate_brick_red_halftone.png, and plate_ink_black_lettering.png. | auto · mandatory · K1 | All five PNG files are present and named exactly as in expected_outputs; any missing or extra plate file fails. |
| Every separation plate shares an identical trim of 24x36 in at 300 dpi (7200x10800 px) so the five screens register on press. | auto · **dealbreaker** · K1 | All five plate PNGs report identical pixel dimensions of 7200x10800 px (24x36 in @300dpi) and identical canvas extent; any plate differing in pixel size fails. |
| plate_white_underbase.png is a solid (non-halftoned) white fill confined to the printable-art footprint over a transparent background. | auto · mandatory · K1 | The underbase plate shows a solid white fill confined to the art footprint with transparent alpha outside the art, no halftone dots, and no spot color; fails if it contains halftone dots, color, or fills the full rectangle including the cream ground. |
| plate_marian_blue_halftone.png, plate_antique_gold_halftone.png, and plate_brick_red_halftone.png each render the folk-art tonal passages as a Ben-Day halftone dot field (not continuous tone). | auto · mandatory · K1 | Each of the three spot plates shows a regular halftone dot pattern across the figurative art region; a plate showing continuous-tone or no visible dot screen fails. |
| The four spot plates carry their correct named ink builds: plate_marian_blue_halftone reads as deep Marian Blue, plate_antique_gold_halftone as Antique Gold, plate_brick_red_halftone as Brick Red, and plate_ink_black_lettering as Ink Black. | expert · mandatory · K1 | plate_marian_blue_halftone reads as deep Marian blue, plate_antique_gold_halftone as antique gold, plate_brick_red_halftone as brick red, and the black plate as ink black; a plate keyed to the wrong spot color fails. |
| The title/year commemorative lettering and key line-work are held out solid (no halftone dots) on each of the four halftone spot plates. | expert · mandatory · K1 | On the four spot plates the lettering and key line-work appear as solid holdout regions with no dot screen breaking up the type; lettering rendered as halftone dots fails. |
| The halftone dot field is dot-gain choked so dots do not plug in shadow areas on absorbent cream stock. | expert · quality · K3 | Shadow/dark regions of the halftone field show discrete, slightly reduced dots rather than fully plugged solid black; an unchoked field where shadow dots merge into solid fails. |
| plate_ink_black_lettering.png carries the vectorized hard-edge title/year lettering and key line-work as solid (no dots) plus the darkest tonal halftone dots. | expert · mandatory · K1 | The black plate shows the commemorative lettering and line-work as crisp solid black with the deepest-shadow halftone dots present; fails if the lettering is dotted or if the black plate omits the held-out type. |
| lettering_lineart.svg is a valid vector SVG of the hard-edge commemorative lettering and key line-work that scales cleanly to wall size. | auto · mandatory · K1 | File is a valid SVG containing vector path data tracing the lettering/line-work and not merely an embedded raster; a raster-only or non-SVG output fails. |
| The vectorized lettering in lettering_lineart.svg reproduces the approved master's banner title and year copy crisply with correct spelling. | expert · mandatory · K2 | The traced lettering legibly matches the approved master's banner title 'JOHN PAUL THE GREAT ACADEMY' and year line '20 YEARS · 2006-2026' with clean hard edges and no misspelling or broken glyphs. |
| client_proof_grain.png is a single flattened proof of the assembled look with screen-print grain/tooth on cream stock. | expert · mandatory · K4 | One flattened PNG shows the combined separations previewed together with visible print grain/tooth texture on a cream/natural ground, suitable for sign-off; fails if it is a bare single plate, lacks grain, or is on plain white. |
| separation_registration_sheet.pdf shows all five labelled spot-colour artboards (WHITE UNDERBASE, MARIAN BLUE, ANTIQUE GOLD, BRICK RED, INK BLACK) with crop/registration marks and ink-name slots. | auto · mandatory · K1 | The PDF contains five labelled artboards carrying the five exact ink names WHITE UNDERBASE, MARIAN BLUE, ANTIQUE GOLD, BRICK RED, and INK BLACK plus crop/registration marks; a sheet missing an artboard, an ink-name label, or registration marks fails. |
| The registration/separation sheet is also delivered as matching PNG and SVG exports alongside separation_registration_sheet.pdf. | auto · mandatory · K1 | Both a PNG and an SVG export of the registration sheet are present in addition to separation_registration_sheet.pdf; missing either format fails. |
| The registration sheet is derived from the supplied authored separations.ai vector template (exported, not recomposed from scratch). | expert · **dealbreaker** · K2 | Artboard layout, registration marks, and ink-name slots match the supplied separations.ai structure (24x36in trim with 0.125in bleed); a freshly invented layout that ignores the authored template fails. |
| campus_reference_board is a reachable Firefly Boards deep-link moodboard collecting the three supplied campus reference photos (campus_chapel.jpg, campus_oak_quad.jpg, campus_schoolhouse_and_foundingclass.jpg). | auto · mandatory · K6 | A reachable Firefly Boards URL is returned and the board contains the three supplied campus reference images campus_chapel.jpg, campus_oak_quad.jpg, and campus_schoolhouse_and_foundingclass.jpg; fails if fewer than the three campus photos are present or the link is dead. |
| The campus reference photos are used only inside the Firefly reference board and are NOT composited or edited into the artwork or any separation plate. | expert · mandatory · K7 | None of the five plates, lettering_lineart.svg, or client_proof_grain.png contain content from the campus photos; the photos appear only on the reference board. Any campus photo edited into a deliverable fails. |


[[PAGEBREAK]]
### AO-62 · Variable-Data Event Promo Catalog + Price-Tag Merge (Overset-Safe Auto-Fit Template)
**Brand:** Party, Events & Promotion &nbsp;·&nbsp; **Operation:** O5 Data-merge & layout (Layout & Data) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (18 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K5 · K1 · K6 · K7
*Run our variable-data merge into the auto-fit (shrink-to-fit) InDesign catalog template and the Illustrator price-tag template so long product names no longer overset, prepping the product hero art and licensed background first, and export print-ready PDFs.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| catalog_template.indd | data | USER-AUTHORED Adobe InDesign document (.indd / .idml). A single A4 portrait catalog card master (210x297mm + 3 |
| pricetag_template.ai | vector | USER-AUTHORED Adobe Illustrator document (.ai) sized as a 70x40mm shelf price tag with Illustrator Variables b |
| catalog_data.csv | data | Generate a realistic ~24-row CSV for an event/party-supply promo catalog with header row: ProductName,Blurb,Pr |
| hero_product.jpg | image | Photoreal product shot of a single colourful party/event product — a glossy gold foil number balloon bundle wi |
| logo_master.png | image | A clean flat 2-colour event-brand wordmark logo reading 'PARTYWORKS' in a bold geometric sans with a small con |
| bg_texture_ref | image | A soft festive bokeh / subtle confetti-texture studio background, muted pastel gradient, slightly out of focus |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| catalog_merged_print.pdf | pdf | Print-ready multipage PDF, one A4 portrait catalog card per CSV row (~24 pages), 210x297mm + 3mm bleed, exported from the merged .indd via document_render_layout. Long pr |
| pricetags_merged.pdf | pdf | Print-ready PDF of merged shelf price tags, 70x40mm each, one per CSV row, exported from the merged .ai via document_render_vector. Vectorized logo placed; long names aut |
| logo_vector.svg | vector | Clean vector SVG of the brand wordmark produced by image_vectorize from logo_master.png, used inside the merge so the mark stays crisp at any print size. |
| product_art_prepped.png | image | Background-removed, auto-toned, cropped-to-cell product hero PNG (transparent) used as the merge image for the hero SKU. |
| font_recommendation.txt | data | Adobe Fonts pairing recommendation (display + body) that suits the event/party brand, from font_recommend. |
| merge_package.zip | data | Single zip bundling the two PDFs, the SVG, the prepped product PNG, and the font note for handoff (local packaging). |

**Layer-3 verifier checks** — expert-authored (17 checks, 3 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| catalog_merged_print.pdf exists and is a valid PDF | auto · mandatory · K1 | A deliverable named catalog_merged_print.pdf exists and opens as a valid PDF (kind=pdf) |
| Catalog PDF has one A4 portrait card per CSV row (~24 pages) | auto · mandatory · K1 | catalog_merged_print.pdf page count equals the catalog_data.csv data-row count (~24 SKUs), exactly one page per row |
| Catalog pages are A4 portrait 210x297mm with 3mm bleed | auto · mandatory · K1 | Each catalog page trim box = 210x297mm portrait and the media/bleed box extends 3mm on all sides (216x303mm total) |
| Long merged product names/blurbs render shrunk-to-fit, never overset or clipped | expert · **dealbreaker** · K1 | On the catalog page(s) carrying the deliberately long record (e.g. ProductName 'Deluxe Personalised Helium-Filled Foil Number Balloon Bundle (Gold)'), the full text is legible inside its frame with no clipping or overset, demonstrating the template's auto-fit shrink-to-fit |
| Each catalog card's merged ProductName, Blurb, Price, SKU and EventName match the source CSV row | auto · mandatory · K1 | For each catalog page, the ProductName, Blurb, Price, SKU and EventName text matches the corresponding catalog_data.csv row exactly (OCR vs CSV) |
| pricetags_merged.pdf exists and is a valid PDF | auto · mandatory · K1 | A deliverable named pricetags_merged.pdf exists and opens as a valid PDF (kind=pdf) |
| Price-tag PDF has one 70x40mm tag per CSV row | auto · mandatory · K1 | pricetags_merged.pdf contains one tag per catalog_data.csv data row (~24), each tag sized 70x40mm |
| Price tags carry the correct merged ProductName, Price and SKU per row | auto · mandatory · K1 | Each tag's ProductName, Price and SKU text matches its catalog_data.csv row (OCR vs CSV) |
| Price-tag long product names auto-size to fit without clipping | expert · **dealbreaker** · K1 | On the tag carrying the long record (ProductName 'Deluxe Personalised Helium-Filled Foil Number Balloon Bundle (Gold)'), the name is fully legible inside the 70x40mm tag with no clipping or overset, showing the .ai template's auto-size area type |
| logo_vector.svg is a vector SVG (not an embedded raster) produced from logo_master.png | auto · mandatory · K1 | Deliverable logo_vector.svg exists, is valid SVG containing vector path data and does not merely embed a raster bitmap of logo_master.png |
| Vectorized logo preserves the PARTYWORKS wordmark and confetti-burst mark fidelity | expert · **dealbreaker** · K2 | logo_vector.svg reads as the 2-colour 'PARTYWORKS' wordmark with the confetti-burst mark, edges crisp and shapes faithful to logo_master.png, with no garbled glyphs or colour drift |
| product_art_prepped.png is background-removed with an alpha channel | auto · mandatory · K1 | product_art_prepped.png is a PNG with a transparency (alpha) channel where the original messy studio tabletop/backdrop is removed and only the foil-balloon product remains |
| Prepped product art shows clean cutout edges and corrected tone | expert · quality · K3 | product_art_prepped.png has clean subject edges (no leftover tabletop/ribbon-background halo) and the gold foil tone is auto-tone corrected and vibrance-lifted versus the raw hero_product.jpg |
| Catalog background is a licensed Adobe Stock texture extended bleed-safe | expert · mandatory · K3 | The catalog card background is the licensed festive bokeh/confetti stock texture, outpainted/cropped to fill the full 216x303mm bleed box with no edge gaps or repeated seams |
| Stock background was licensed before any editing | expert · mandatory · K7 | The background asset is a properly licensed stock download (asset_license_and_download_stock performed before image_generative_expand), not an unlicensed comp or the bg_texture_ref reference image |
| font_recommendation.txt names an Adobe Fonts display + body pairing | auto · mandatory · K5 | font_recommendation.txt exists and names a specific Adobe Fonts display typeface and a body typeface suited to the party/event brand |
| merge_package.zip is a valid zip bundling all required handoff deliverables | auto · mandatory · K6 | merge_package.zip opens as a valid zip and contains catalog_merged_print.pdf, pricetags_merged.pdf, logo_vector.svg, product_art_prepped.png and font_recommendation.txt |


[[PAGEBREAK]]
### AO-63 · Maple Cricket League — a streetwear cricket league: vectorize the logo system, build the sublimation/screen-print kit artwork, and grade the brand photography into a production-ready package
**Brand:** Automotive, Industrial & Agriculture &nbsp;·&nbsp; **Operation:** O5 Data-merge & layout (Layout & Data) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (18 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K5 · K1 · K6 · K7
*Turn Maple Cricket League's already-designed raster logo sketches and brand photos into a production-ready package: clean vector marks, a halftone sublimation/screen-print kit treatment, cohesive streetwear color-grade, a cut-out product shot, an outpainted banner, and an exported, packaged deliverable set.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| logo_system_raster.png | image | A flat, slightly imperfect scan of a streetwear cricket-league logo sheet on off-white paper, three marks laid |
| logo_system_master.ai | vector | Generate a genuine authored Adobe Illustrator (.ai) file containing three artboards — Artboard 1: MCL circular |
| hero_street_cricket.jpg | image | Candid documentary photo of young South Asian and Caribbean men playing backyard/street cricket in a Toronto ( |
| home_jersey_flat.jpg | image | Studio e-commerce photo of a neatly folded short-sleeve cricket jersey in deep forest green with a cream MCL c |
| away_crest_graphic.jpg | image | A flat, head-on photo of the MCL away-kit chest crest printed on light fabric: a single bold emblem — crossed |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| MCL_logo_system_traced.svg | vector/SVG | Clean vectorized trace of the supplied logo-system raster (crest + monogram + hat badge), flat paths, two ink colors preserved, infinitely scalable for manufacturer/embro |
| MCL_logo_master_export.pdf | vector-export/PDF+PNG | Exported render of the client's authored 3-artboard .ai master (all artboards together) as print-res PDF plus a PNG proof; this is the production logo handoff. |
| MCL_away_crest_screenprint_halftone.png | image/PNG | Auto-straightened, cropped-to-bounds, one-color halftone screen-print / sublimation separation of the away-kit crest, ready for the manufacturer's single-screen output. |
| MCL_hero_graded.jpg | image/JPEG | Streetwear color-graded hero brand photo: auto-toned, exposure/contrast balanced, warm monochromatic split-tone, fine grain — matches the OVO/ALD/IPL reference look. |
| MCL_jersey_cutout.png | image/PNG (transparent) | Folded home-jersey product shot with background removed to transparency for the lookbook/e-commerce grid. |
| MCL_hero_banner_wide.jpg | image/JPEG | Wide site/social banner generated by AI-outpainting the graded hero to extended canvas (content extended, original not cropped). |
| MCL_brand_delivery.zip | archive/ZIP | One organized, named delivery folder zipping all exports above into the production handoff structure the brief requires. |

**Layer-3 verifier checks** — expert-authored (16 checks, 3 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All seven required deliverables are present in the package | auto · mandatory · K1 | The delivery contains exactly these seven named files: MCL_logo_system_traced.svg, MCL_logo_master_export.pdf, MCL_away_crest_screenprint_halftone.png, MCL_hero_graded.jpg, MCL_jersey_cutout.png, MCL_hero_banner_wide.jpg, and MCL_brand_delivery.zip |
| Each deliverable is in the file format/colour-mode the spec names | auto · **dealbreaker** · K1 | MCL_logo_system_traced.svg is a valid SVG vector file; MCL_logo_master_export.pdf is a valid PDF accompanied by a PNG proof; MCL_away_crest_screenprint_halftone.png and MCL_jersey_cutout.png are valid PNG; MCL_hero_graded.jpg and MCL_hero_banner_wide.jpg are valid JPEG; MCL_brand_delivery.zip is a valid ZIP archive |
| The traced logo SVG is genuine scalable vector geometry derived from the supplied raster, not an embedded raster | auto · mandatory · K1 | MCL_logo_system_traced.svg contains real <path> vector geometry and no embedded raster <image>/bitmap element (the file is a true raster->SVG trace of logo_system_raster.png, not a wrapped bitmap) |
| The traced SVG reproduces all three marks from the source logo sheet | expert · mandatory · K2 | MCL_logo_system_traced.svg reproduces all three marks present in logo_system_raster.png: the circular MCL crest, the interlocking MCL monogram, and the simplified hat badge |
| The traced SVG preserves the two ink colours of the source logo | expert · quality · K2 | The vectorized trace renders in two flat ink colours matching the source (deep forest green and cream) with clean flat paths, and introduces no extra colours or gradients |
| The logo master PDF is an export of the client's authored 3-artboard .ai, not a regenerated or newly composed logo | expert · **dealbreaker** · K2 | MCL_logo_master_export.pdf renders all three artboards (MCL circular crest, interlocking MCL monogram, simplified hat badge) from logo_system_master.ai together, with no new/invented logo concepts and no from-scratch redrawing of the marks |
| The away-crest halftone output is auto-straightened and cropped tight to the print bounds | expert · mandatory · K1 | MCL_away_crest_screenprint_halftone.png shows the crest rotation-corrected (no longer ~3 degrees off straight, matching away_crest_graphic.jpg's intentional skew) and cropped to the crest graphic's bounds with the surrounding near-white jersey panel removed |
| The away-crest output is a single-colour halftone screen-print/sublimation separation | expert · mandatory · K3 | MCL_away_crest_screenprint_halftone.png is one-colour with a visible halftone dot pattern, ready as a single-screen print/sublimation separation, with no full-colour tones, gradients, or multi-ink |
| The graded hero photo received the full streetwear grade chain in order | expert · mandatory · K4 | MCL_hero_graded.jpg reflects, over the ungraded hero_street_cricket.jpg, an auto-tone baseline, an exposure/contrast punch, a warm monochromatic split-tone tint, and fine film grain — reading visibly warmer, more contrasted, and less flat than the cool/underexposed input |
| The graded hero matches the named OVO/Aimé Leon Dore/IPL reference look | expert · quality · K4 | The grade reads as cohesive warm streetwear photography consistent with the OVO/Aimé Leon Dore/IPL aesthetic reference, not a neutral/flat result or an over-stylized filter |
| The jersey cut-out has a fully transparent background | auto · mandatory · K3 | MCL_jersey_cutout.png has a transparent alpha channel where the light-grey seamless backdrop of home_jersey_flat.jpg was, retaining only the folded jersey subject |
| The jersey cut-out edge quality is clean enough for the e-commerce/lookbook grid | expert · quality · K3 | The cut-out edge around the folded jersey is clean with no leftover grey backdrop halo, no clipped fabric, and intact knit/fold detail |
| The wide banner is produced by outpainting the graded hero (canvas extended, original content not cropped) | expert · mandatory · K3 | MCL_hero_banner_wide.jpg is wider than MCL_hero_graded.jpg with the original framing fully retained and new generated content extending the scene at the sides, not a crop or re-frame of the hero |
| The banner is derived from the already-graded hero, preserving the grade | expert · quality · K3 | MCL_hero_banner_wide.jpg carries the same warm graded look as MCL_hero_graded.jpg (the outpaint extends the graded frame, not the raw input), with the extended side region tonally matching the original |
| No from-scratch art or text-to-image generation was used for the logo deliverables | expert · **dealbreaker** · K7 | The logo deliverables originate solely from the raster trace (image_vectorize) and the authored .ai export (document_render_vector); there is no invented new logo concept, no text-to-image-generated mark, and no compositing/gen-fill beyond the single permitted generative outpaint (the banner) |
| Final ZIP is organized into the named production-handoff folder structure | auto · mandatory · K6 | MCL_brand_delivery.zip contains all six exports sorted into named production-handoff subfolders (e.g. logos/, kits/, photography/), not a flat unnamed dump |


[[PAGEBREAK]]
### AO-64 · Premium skincare packaging: retouch hero shot, vectorize logo, render authored dieline + data-merge SKU labels, print-ready PDFs
**Brand:** Beauty, Cosmetics & Personal Care &nbsp;·&nbsp; **Operation:** O5 Data-merge & layout (Layout & Data) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (17 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K5 · K1 · K6 · K7
*Take Aurelia Botanics' supplied hero serum photo, logo, authored carton dieline (.ai) + label (.indd) and SKU data, and produce retouched/CMYK-graded imagery, a clean vector logo, data-merged print-ready label PDFs for all 3 SKUs, and high-res mockup assets.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| hero_serum_bottle.jpg | image | Photoreal studio product photograph of a single premium amber-glass facial serum bottle with a matte-black dro |
| aurelia_logo_raster.png | image | Clean minimalist beauty brand wordmark logo reading 'AURELIA BOTANICS' in an elegant high-contrast serif, with |
| leaf_motif.png | image | Single continuous-line botanical illustration of overlapping eucalyptus and rosehip leaves and small berries, |
| aurelia_carton_dieline.ai | vector | Generate an Adobe Illustrator .ai (PDF-compatible) file describing a folding-carton dieline for a 40x40x120mm |
| aurelia_label_template.indd | vector | Generate an Adobe InDesign .indd (or .idml) label template, 70x90mm + 3mm bleed, CMYK, containing real data-me |
| skus.csv | data | Generate a 3-row CSV with header product_name,key_actives,volume,batch and rows: Rosehip Renewal Facial Serum |
| brand_guide.pdf | pdf | Generate a 4-page brand-guide PDF for 'Aurelia Botanics': page 1 logo + clear-space, page 2 deep-forest-green |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| hero_bottle_retouched_cutout.png | image | Background-removed transparent PNG of the straightened, auto-toned, exposure-/temperature-corrected, Subject-Pop-graded amber serum bottle; full hero resolution (~4000x50 |
| marble_mockup_backdrop.jpg | image | Licensed marble-surface stock backdrop cropped/resized to the 3000x3000px mockup canvas. |
| leaf_duotone_panel.png | image | Brand-green 2-color halftone/duotone side-panel texture derived from the supplied leaf motif, print-clean. |
| aurelia_logo.svg | vector | Clean vectorized SVG of the AURELIA BOTANICS wordmark + leaf mark, single solid spot color, scalable for the carton. |
| carton_dieline_print.pdf | pdf | Print PDF exported from the authored carton dieline .ai with cut/fold lines, 3mm bleed, registration marks, CMYK; plus a preview PNG. |
| labels_merged_print.pdf | pdf | One print-ready, 3mm-bleed, CMYK label page per SKU (3 pages) produced by data-merging skus.csv onto the authored label .indd. |
| brand_guide_editable.indd | indd | Editable InDesign document (.indd, delivered zipped) converted from the supplied 4-page brand-guide PDF. |
| aurelia_concept_board | board | Firefly Board deep-link assembling the hero cutout, marble backdrop, duotone panel, vector logo, dieline preview and label previews as the client-facing concept presentat |

**Layer-3 verifier checks** — expert-authored (16 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| The hero deliverable hero_bottle_retouched_cutout.png is a PNG with a real transparent (alpha) background, not a flat opaque image | auto · mandatory · K1 | File hero_bottle_retouched_cutout.png is a valid PNG that contains an alpha channel with fully transparent pixels surrounding the serum-bottle subject |
| The hero cutout shows the full retouch chain was applied: straightened framing, lifted exposure, warmer color temperature, and a Subject-Pop separation on the amber serum bottle | expert · quality · K3 | Bottle reads visibly straightened/level, brighter than a neutral baseline with a warm amber cast, and pops cleanly off the original seamless light-grey sweep, consistent with auto_straighten -> auto_tone -> exposure -> warmer temperature -> Subject Pop preset |
| The background knockout edge quality on the hero cutout is clean around the amber glass, matte-black dropper cap, and refraction/specular edges | expert · quality · K3 | Cutout mask follows the bottle silhouette with no halo, no leftover grey backdrop, and no chewed glass edges; semi-transparent glass refraction is handled plausibly |
| The marble mockup backdrop deliverable marble_mockup_backdrop.jpg is exactly 3000x3000 pixels | auto · mandatory · K1 | marble_mockup_backdrop.jpg has pixel dimensions width==3000 and height==3000 |
| The marble backdrop is a genuinely licensed Adobe Stock marble-surface image (licensed before editing), not a generated or watermarked comp | expert · mandatory · K2 | Backdrop depicts a real marble surface and carries no stock watermark, consistent with license-then-download of a licensed Adobe Stock asset |
| The leaf side-panel deliverable leaf_duotone_panel.png is a 2-color halftone/duotone in brand forest-green, derived from the supplied leaf_motif.png art | expert · mandatory · K2 | Panel is a two-tone (forest-green + ground) halftone/duotone of the supplied eucalyptus/rosehip leaf motif with no full-color photographic content and no extra colors |
| The logo deliverable aurelia_logo.svg is a valid vector SVG containing path/vector geometry, not an embedded raster bitmap | auto · mandatory · K1 | aurelia_logo.svg parses as SVG and contains <path>/vector elements; it does not consist solely of an embedded <image>/base64 raster |
| The vectorized logo reproduces the AURELIA BOTANICS serif wordmark plus the leaf-sprig mark in a single solid spot color, faithful to the supplied aurelia_logo_raster.png and not redrawn or altered | expert · **dealbreaker** · K2 | SVG renders the 'AURELIA BOTANICS' high-contrast serif wordmark and the leaf-sprig mark matching aurelia_logo_raster.png shape-for-shape in one solid color with clean closed paths; no new glyphs, ornaments, or color changes introduced |
| The carton dieline is delivered as a print PDF (carton_dieline_print.pdf) plus a preview PNG, exported from the client-authored aurelia_carton_dieline.ai and not authored from scratch | auto · mandatory · K1 | carton_dieline_print.pdf exists alongside a preview PNG of the same dieline, and the PDF page corresponds to the supplied 40x40x120mm folding-carton dieline structure |
| The exported carton dieline PDF preserves the authored structural print elements: cut lines, fold/score lines, 3mm bleed and registration marks, in CMYK | expert · mandatory · K1 | Dieline PDF shows distinct cut lines and fold/score lines, registration marks, and a 3mm bleed margin, and is CMYK, matching the authored aurelia_carton_dieline.ai it was exported from |
| The merged label deliverable labels_merged_print.pdf contains exactly 3 label pages, one per SKU | auto · mandatory · K1 | labels_merged_print.pdf has exactly 3 pages |
| Each of the 3 label pages carries the correct merged SKU data bound from skus.csv onto the product_name/key_actives/volume/batch fields | auto · **dealbreaker** · K1 | The 3 pages show, one per page: 'Rosehip Renewal Facial Serum' / 'Rosehip Oil + Vitamin C' / '30 ml' / 'AB-RR-0426'; 'Niacinamide Clarity Facial Serum' / '10% Niacinamide + Zinc' / '30 ml' / 'AB-NC-0426'; 'Hyaluronic Hydra Facial Serum' / '2% Hyaluronic Acid + B5' / '30 ml' / 'AB-HH-0426' |
| The label print PDF is a CMYK, 3mm-bleed print-ready file with no leftover literal <<field>> placeholders | expert · mandatory · K1 | labels_merged_print.pdf is CMYK with a 3mm bleed, and no unmerged '<<product_name>>'/'<<key_actives>>'/'<<volume>>'/'<<batch>>' placeholder text remains on any page |
| The labels preserve the authored typographic hierarchy (product name large serif, actives medium, volume+batch small) and brand green/cream swatches | expert · quality · K3 | On each label the product name is the largest serif element, key_actives is medium, volume and batch are smallest, rendered with brand forest-green/cream swatches per the authored aurelia_label_template.indd |
| The brand-guide deliverable brand_guide_editable.indd is an editable InDesign document (delivered zipped) converted from the supplied 4-page brand_guide.pdf | auto · mandatory · K1 | Deliverable is a ZIP containing an editable .indd (or .idml) document derived from the 4-page brand_guide.pdf |
| A Firefly concept board (aurelia_concept_board) deep-link is delivered assembling the six produced assets: hero cutout, marble backdrop, duotone panel, vector logo, dieline preview and label preview(s) | auto · mandatory · K6 | A working Firefly Board link resolves to a board containing the 6 produced assets: hero_bottle_retouched_cutout, marble_mockup_backdrop, leaf_duotone_panel, aurelia_logo.svg, the carton dieline preview, and the label preview(s) |


[[PAGEBREAK]]
### AO-67 · Tamil Traditional Service-Promotion Large-Format Banner Set — Print-Prep & Source-File Production (6 sizes)
**Brand:** General / Cross-Industry Branding & Graphics &nbsp;·&nbsp; **Operation:** O5 Data-merge & layout (Layout & Data) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (21 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K5 · K1 · K6 · K7
*Take my supplied Tamil banner master files plus hero photography and brand logo, and produce the complete print-ready production package — graded hero image with print bleed, a clean vector logo, a traditional halftone texture motif, and CMYK 150-dpi PDF/JPEG exports of all six large-format banners — with editable source files alongside.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| banner_hero_photo.jpg | image | Photoreal wide horizontal photograph of a traditional South Indian service storefront / festive premises scene |
| brand_logo_flat.png | image | A flat, slightly low-resolution raster brand logo for a traditional Tamil service business: a circular emblem |
| banner_master_10x20.ai | vector | Author a genuine Adobe Illustrator master document (.ai) for a 10ft x 20ft large-format banner in a traditiona |
| banner_masters_remaining.ai | vector | Author the remaining five genuine Illustrator banner master documents matching banner_master_10x20.ai's tradit |
| last_year_proof.pdf | pdf | A single-page low-resolution PDF proof of last year's traditional Tamil promotional banner: maroon/gold orname |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| hero_graded_bleed.png | image | Corrected + warm-traditional-graded hero photograph (straightened, auto-toned, highlights recovered, gold/maroon vibrance pushed, controlled subject color) with 1 inch of |
| brand_logo_vector.svg | vector | Clean scalable SVG vectorization of the flat brand logo, sharp at 10-foot print height, solid maroon/gold fills, Tamil emblem preserved. |
| halftone_texture_motif.png | image | Traditional screen-print / halftone texture motif derived from the graded hero, for the close-up printed-poster aesthetic. High-res PNG. |
| banner_10x20_print.pdf + .png | pdf | Print export of the authored 10x20 ft master: PDF plus flattened high-res PNG, full-scale 150 dpi, 1-inch bleed, traditional look intact, Tamil typography untouched. |
| banner_set_exports.zip | data | Packaged folder containing print PDF + high-res PNG exports for all six authored banner masters (3x 10x10, 2x 10x20, 1x 10x6), the editable .indd converted from last year |

**Layer-3 verifier checks** — expert-authored (16 checks, 3 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All six authored banner masters are exported as PDF + high-res PNG pairs matching the exact size breakdown | auto · mandatory · K1 | The deliverable contains a print PDF + high-res PNG for exactly 6 banners with the size breakdown 3x 10x10 ft, 2x 10x20 ft, 1x 10x6 ft (12 export files total, 2 per master) |
| The individually named 10x20 ft print export deliverable is present as PDF plus flattened high-res PNG | auto · mandatory · K1 | banner_10x20_print.pdf and its companion flattened high-res PNG (banner_10x20_print.png) are both present in the package |
| Each banner print PDF export carries CMYK colour intent | auto · **dealbreaker** · K1 | Every banner print PDF carries CMYK colour space / intent (the flattened PNG companions may be RGB/sRGB, since PNG cannot carry CMYK) |
| Each banner export meets the resolution spec at full physical scale | auto · mandatory · K1 | Every banner export is 150 dpi minimum at the full physical scale of its banner size |
| Each banner PDF export carries 1-inch bleed on all four sides | auto · mandatory · K1 | Every banner PDF export includes 1 inch of bleed on all four sides |
| The locked Tamil typography in the authored masters is left untouched (not re-typeset, translated, outlined, or misspelled) | expert · **dealbreaker** · K2 | Tamil headline/body text in all exports is identical to the supplied .ai masters — text frames preserved, no re-typesetting, no translation, no spelling alterations, no glyph corruption |
| The graded hero deliverable hero_graded_bleed.png is present as a high-res PNG | auto · mandatory · K1 | hero_graded_bleed.png is present in the package as a high-resolution PNG file |
| The hero photo received the full ordered correction-and-grade pipeline | expert · mandatory · K4 | hero_graded_bleed.png shows: straightened horizon (the ~3-degree tilt removed), auto-tone applied, blown highlights/sky recovered, warmed white balance toward gold, and pushed gold/maroon vibrance/saturation |
| The focal service element's colour is selectively controlled via a prompt-built mask | expert · quality · K3 | The main service element (e.g. brass lamp / seva counter) was isolated via a select_by_prompt mask and had single-colour saturation applied so its colour stays controlled, distinct from a global edit |
| The hero bleed is real outpainted content, not padding | expert · mandatory · K3 | hero_graded_bleed.png has 1 inch of generatively expanded (outpainted) image content extending the scene on all four sides for the 10x20 ft layout — not solid/transparent padding or a stretched/mirrored border |
| The brand logo is delivered as a clean vector SVG | auto · mandatory · K1 | brand_logo_vector.svg is present and is a true path-based vector SVG (not an embedded raster), scalable for 10-foot print height |
| The vectorized logo preserves the original emblem in solid maroon/gold fills | expert · **dealbreaker** · K2 | brand_logo_vector.svg reproduces the supplied kuthuvilakku oil-lamp emblem, Tamil-script business name along the top arc, and lotus underline in solid maroon and gold fills with crisp edges — not a regenerated or altered logo |
| The halftone texture motif is delivered and derived from the graded hero | expert · mandatory · K4 | halftone_texture_motif.png is present as a high-res PNG showing a traditional screen-print / halftone dot texture visibly derived from the graded+bleed hero image |
| The old PDF proof is converted into an editable InDesign source | auto · mandatory · K1 | last_year_editable.indd is present as a genuine editable .indd file converted from last_year_proof.pdf |
| A single packaged delivery bundle contains every final and source file organised together | auto · mandatory · K6 | The banner_set_exports deliverable bundles, in one organised folder: the 6 banner PDF+PNG export pairs, brand_logo_vector.svg, hero_graded_bleed.png, halftone_texture_motif.png, and last_year_editable.indd |
| The traditional warm gold/maroon festive look is consistent across all six sizes | expert · quality · K4 | All six banner exports and the graded hero read as a coherent traditional Tamil festive set — warm gold/maroon tones, ornamental treatment, eye-catching from a distance — with no inconsistent grading across sizes |


[[PAGEBREAK]]
### AO-68 · Roadside Coaching-Institute Banner: brand-graded hero, vector icon set, halftone geometry + print-ready CMYK PDF export
**Brand:** Nonprofit, Religious & Community &nbsp;·&nbsp; **Operation:** O5 Data-merge & layout (Layout & Data) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (18 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K5 · K1 · K6 · K7
*Prepare every visual asset for the DYNAMIC SOLUTION CLASSES 10ft x 5ft roadside banner — brand-graded student hero, vector subject icons, brand-colour halftone geometry — and export the authored InDesign layout to a print-ready CMYK PDF for large-format flex printing.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| students_raw_photo.jpg | image | Candid documentary photo of four real Indian high-school and pre-foundation students (mixed ages 12-17, mixed |
| subject_icons_sheet.png | image | A clean flat icon sheet on a pure white background: six minimal single-weight line icons hinting at school sub |
| DYNAMIC_SOLUTION_banner_AUTHORED.indd | pdf | Represents a CLIENT-AUTHORED InDesign banner document (.indd / .idml), 10ft x 5ft at print scale, CMYK, contai |
| brand_palette_swatch.png | image | A simple brand color swatch card on white: two large rounded rectangles side by side, left labeled PRIMARY #04 |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| students_hero_brandgraded_2x1.png | image | Straightened, cropped, auto-toned, white-balanced and brand-graded student hero photo pushed toward #046CB8/#02ADEF, outpainted to the full 2:1 (10ft x 5ft) banner hero b |
| students_cutout_transparent.png | image | Background-removed transparent-PNG cutout of the student group for clean placement onto the banner's geometric field. |
| subject_icons.svg | vector | Brand-blue subject icon set vectorized to clean scalable SVG paths that stay crisp at 10-foot print size. |
| brand_halftone_texture.png | image | Modern, minimal halftone/duotone geometric texture in the #046CB8/#02ADEF brand colours for the understated background accent. |
| DYNAMIC_SOLUTION_banner_PRINT.pdf | pdf | Print-ready, high-resolution CMYK PDF of the authored banner layout, 10ft x 5ft, exported for large-format flex printing — the primary client deliverable. |
| DYNAMIC_SOLUTION_banner_proof.jpg | image | Flattened JPEG proof of the banner layout for quick on-screen client review. |
| DYNAMIC_SOLUTION_signoff_board | data | Firefly board deep-link assembling the graded hero, cutout plate, vector icons, halftone texture and the PDF/JPEG proof for client sign-off. |

**Layer-3 verifier checks** — expert-authored (17 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| The print-ready CMYK PDF deliverable DYNAMIC_SOLUTION_banner_PRINT.pdf exists and is a valid PDF | auto · mandatory · K1 | A file named DYNAMIC_SOLUTION_banner_PRINT.pdf is delivered and opens cleanly as a valid PDF document |
| The print PDF colour space is CMYK | auto · **dealbreaker** · K1 | DYNAMIC_SOLUTION_banner_PRINT.pdf reports a CMYK (DeviceCMYK / ICC CMYK) colour space, not RGB, matching the brief's 'Print-ready PDF in CMYK' requirement |
| The banner uses the 10ft x 5ft (2:1) aspect ratio at print scale | auto · mandatory · K1 | DYNAMIC_SOLUTION_banner_PRINT.pdf page geometry is 2:1 (width:height = 10ft:5ft), within a small tolerance |
| The print PDF is high-resolution suitable for large-format flex printing with no pixelation | expert · mandatory · K4 | At full 10ft x 5ft size the exported PDF shows no visible pixelation, blurring or upscaling artefacts in the hero photo, icons or texture, satisfying the brief's 'high resolution suitable for large-format flex printing (no pixelation)' |
| The brand-graded student hero deliverable students_hero_brandgraded_2x1.png is delivered as a 2:1 PNG | auto · mandatory · K1 | students_hero_brandgraded_2x1.png is delivered as a PNG whose aspect ratio is 2:1 (the full 10ft x 5ft banner hero band produced by the outpaint/generative-expand step) |
| The student hero photo is graded toward the brand palette #046CB8 / #02ADEF | expert · mandatory · K2 | The dominant tones of students_hero_brandgraded_2x1.png are visibly pushed toward the brand blues #046CB8 (primary) and #02ADEF (secondary) without unnatural skin tones |
| The student hero horizon is straightened and the crop is clean | expert · quality · K3 | The tilted horizon from the raw handheld DSLR photo is corrected to level and the hero is cropped to the banner hero band with no awkward cuts of the students |
| The student cutout deliverable students_cutout_transparent.png is a background-removed transparent PNG | auto · mandatory · K1 | students_cutout_transparent.png is delivered as a PNG with a real alpha channel and the original background fully removed to transparency |
| The student cutout has clean mask edges with no background fringing | expert · quality · K3 | Edges of the student group in students_cutout_transparent.png (hair, shoulders, notebook edges) are cleanly masked with no halo, fringe or leftover background |
| The subject icon set deliverable subject_icons.svg is true scalable vector output | auto · mandatory · K1 | subject_icons.svg is delivered as a valid SVG containing vector <path> geometry (not an embedded raster image) |
| The vectorized set contains the six subject icons, stays crisp at 10-foot print size, and is in brand blue | expert · quality · K2 | subject_icons.svg contains the six subject icons (beaker, sigma/maths, globe, open book, DNA helix, balance scale) as clean closed brand-blue (#046CB8) line shapes that stay sharp when scaled to large-format print, with no raster blur |
| The halftone texture deliverable brand_halftone_texture.png exists in the brand colours | auto · mandatory · K1 | brand_halftone_texture.png is delivered as a PNG rendering a halftone/duotone geometric texture using the #046CB8 / #02ADEF brand colours |
| The halftone texture reads as an understated, modern, minimal accent | expert · quality · K4 | brand_halftone_texture.png reads as a subtle understated geometric accent (not a loud or busy pattern), consistent with the brief's 'modern, minimalistic feel' and 'understated geometric elements' |
| The JPEG proof deliverable DYNAMIC_SOLUTION_banner_proof.jpg is a flattened proof of the banner layout | auto · mandatory · K1 | DYNAMIC_SOLUTION_banner_proof.jpg is delivered as a flattened JPEG showing the full banner layout for on-screen review |
| All verbatim banner copy is present and legible in the exported layout | expert · **dealbreaker** · K1 | The exported PDF/proof shows, legibly, the institute name DYNAMIC SOLUTION CLASSES, tagline 'Where Learning Meets Success', the Pre-Foundation / 9th-10th / 11th-12th course list, 'ADMISSIONS OPEN', the three phones (8103332901, 8989871223, 9589110600), 'Railway Station Road, Multai', and the four feature bullets (Small Batch Size / Personal Attention / Regular Tests / Doubt Sessions) |
| Text hierarchy is crystal clear at full size with 8103332901 most prominent and headings in bold Inter | expert · mandatory · K3 | At full 10ft x 5ft size the headings/key numbers read in bold Inter, the phone number 8103332901 is the most prominent of the three phones, and the overall hierarchy is legible from a distance (per the client sign-off bar 'text hierarchy is crystal clear at full size') |
| The Firefly sign-off board deliverable DYNAMIC_SOLUTION_signoff_board assembles all review assets | auto · mandatory · K6 | DYNAMIC_SOLUTION_signoff_board is a Firefly board deep-link assembling the graded hero, cutout plate, vector icons, halftone texture and the JPEG proof for client sign-off |


[[PAGEBREAK]]
### AO-69 · TitanSeal Sealants Launch — Logo-System Extension, Swappable SKU Label/Carton Data-Merge, and Print-Ready + Digital Asset Package
**Brand:** Real Estate, Construction & Property &nbsp;·&nbsp; **Operation:** O5 Data-merge & layout (Layout & Data) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (22 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K5 · K1 · K6 · K7
*Take the approved TitanSeal master logo plus the client's authored InDesign label .indd and Illustrator carton .ai mechanicals, derive the full logo-variant system, data-merge the three SKUs into swappable print-ready label/carton artwork, and output the print PDFs plus a correctly-sized digital-asset pack.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| titanseal_titanseal_master_logo.png | image | A clean, approved master logo for an industrial sealants brand 'TitanSeal' on a fully transparent background, |
| titanseal_label_mechanical.indd | vector | Describe/generate an InDesign label mechanical package metadata: a single wrap-around cartridge label artboard |
| titanseal_carton_mechanical.ai | vector | Describe/generate an Illustrator carton mechanical: a single-color (black) die-line for a corrugated shipping |
| sku_variants.csv | data | Generate a CSV with header SKU_NAME,SKU_CODE,VOLUME,COLORWAY,BARCODE,PACK_COUNT,CARTON_SIZE,BATCH and exactly |
| jobsite_background.jpg | image | Photoreal documentary shot of a clean modern construction jobsite detail: a gloved hand running a bead of grey |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| titanseal_logo.svg | vector | Clean scalable SVG vectorized from the master logo PNG; solid-fill paths, usable in print lockups at any size. |
| titanseal_logo_mono_black.png | image | Single-color solid black version of the mark on transparent background, for the black-on-cardboard carton. |
| titanseal_logo_reversed_white.png | image | Single-color solid white reversed/knockout version on transparent background, for dark/photo backgrounds. |
| titanseal_logo_brandblue.png | image | Brand-blue color-overlay version of the mark on transparent background. |
| titanseal_horizontal_lockup.png | image | 3:1 horizontal-lockup working canvas, outpainted from the square logo composition, for web banner/email use. |
| titanseal_labels_merged.pdf | pdf | Press-ready multi-page PDF, one page per SKU, from the authored .indd + CSV data-merge; 3mm bleed, swappable SKU codes/volumes via CSV. |
| titanseal_cartons_merged.pdf | pdf | Single-color black carton artwork PDF for 20-cartridge and 24-tube packs, from the authored .ai Variables + CSV; die-line preserved. |
| titanseal_social_tile_1080.png | image | 1080x1080 on-brand graded social media tile (jobsite background graded + cropped). |
| titanseal_web_banner_1920x1080.png | image | 1920x1080 web banner crop of the graded jobsite asset. |
| titanseal_email_signature_350x120.png | image | 350x120 email-signature crop of the graded jobsite asset. |
| titanseal_whatsapp_card_1x1.png | image | 1:1 WhatsApp catalog product card crop of the graded jobsite asset. |
| titanseal_review_board | firefly_board | Firefly Board deep-link presenting the logo-variant system and key produced assets for client review. |

**Layer-3 verifier checks** — expert-authored (20 checks, 3 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| titanseal_logo.svg is a vector SVG vectorized from the supplied master logo PNG, with solid-fill paths and no embedded raster bitmap | auto · mandatory · K1 | Output file titanseal_logo.svg exists, is valid SVG markup containing <path> (or equivalent vector) elements with solid fills, and contains no embedded <image> raster data |
| The vectorized SVG reproduces the supplied TitanSeal master logo mark (wordmark + caulk-bead/droplet icon) rather than a redrawn or different mark | expert · **dealbreaker** · K2 | Visual comparison shows titanseal_logo.svg silhouette/letterforms/icon match titanseal_titanseal_master_logo.png; the mark is derived (vectorized), not redrawn or substituted |
| titanseal_logo_mono_black.png is a single-color solid black version of the mark on a transparent background | auto · mandatory · K1 | titanseal_logo_mono_black.png has a transparent alpha channel and all non-transparent pixels are solid black (RGB ~0,0,0) |
| titanseal_logo_reversed_white.png is a single-color solid white reversed/knockout version of the mark on a transparent background | auto · mandatory · K1 | titanseal_logo_reversed_white.png has a transparent alpha channel and all non-transparent pixels are solid white (RGB ~255,255,255) |
| titanseal_logo_brandblue.png is a brand-blue color-overlay version of the mark in TitanSeal blue #0B3D91 on a transparent background | auto · mandatory · K2 | titanseal_logo_brandblue.png has a transparent alpha channel and the colored mark pixels are brand blue approximately #0B3D91 |
| The mono-black, reversed-white, and brand-blue variants are derived from the supplied master logo mark, not redrawn or substituted | expert · **dealbreaker** · K2 | The mark silhouette/letterforms/icon in titanseal_logo_mono_black.png, titanseal_logo_reversed_white.png, and titanseal_logo_brandblue.png all match titanseal_titanseal_master_logo.png; each is a single-color/recolor derivation of the same mark |
| titanseal_horizontal_lockup.png is a 3:1 horizontal-lockup canvas outpainted from the square logo composition | auto · mandatory · K1 | titanseal_horizontal_lockup.png has a width:height aspect ratio of 3:1 (within ~2% tolerance) and contains the TitanSeal logo composition |
| The outpainted horizontal lockup extends the square logo composition seamlessly without distorting or regenerating the original mark | expert · quality · K3 | The original TitanSeal mark is preserved intact within the 3:1 canvas and the expanded background blends naturally with no visible seam or warping of the mark |
| titanseal_labels_merged.pdf is a press-ready multi-page PDF with one page per SKU produced from the authored .indd + sku_variants.csv data-merge | auto · mandatory · K1 | titanseal_labels_merged.pdf is a valid PDF with exactly 3 pages (one per CSV data row) |
| The merged label PDF pages carry the exact per-SKU data from sku_variants.csv (SKU_NAME, SKU_CODE, VOLUME, COLORWAY) bound to the .indd merge fields | auto · **dealbreaker** · K1 | Across the label PDF pages, OCR/text extraction finds 'MS Polymer Sealant'/OBC-MS600-GRY/600ml/Grey, 'PU Construction Sealant'/OBC-PU600-GRY/600ml/Grey, and 'Neutral Silicone Sealant'/OBC-NS300-WHT/300ml/White each on its own page |
| The merged label PDF is built with 3mm bleed as specified | auto · mandatory · K1 | titanseal_labels_merged.pdf page geometry shows a 3mm bleed margin around the trim box |
| titanseal_cartons_merged.pdf is a single-color black carton PDF for the 20-cartridge and 24-tube packs produced from the authored .ai Variables + CSV merge | auto · mandatory · K1 | titanseal_cartons_merged.pdf is a valid PDF whose carton artwork is single-color black and contains both the 20-cartridge and 24-tube carton variants |
| The merged carton PDF preserves the die-line from the authored .ai mechanical | expert · mandatory · K3 | The carton die-line (cut/fold lines) from titanseal_carton_mechanical.ai is intact and unbroken in titanseal_cartons_merged.pdf |
| titanseal_social_tile_1080.png is exactly 1080x1080 px | auto · mandatory · K1 | titanseal_social_tile_1080.png dimensions equal 1080x1080 pixels |
| titanseal_web_banner_1920x1080.png is exactly 1920x1080 px | auto · mandatory · K1 | titanseal_web_banner_1920x1080.png dimensions equal 1920x1080 pixels |
| titanseal_email_signature_350x120.png is exactly 350x120 px | auto · mandatory · K1 | titanseal_email_signature_350x120.png dimensions equal 350x120 pixels |
| titanseal_whatsapp_card_1x1.png is a 1:1 square crop of the graded jobsite asset | auto · mandatory · K1 | titanseal_whatsapp_card_1x1.png has equal width and height (1:1 aspect ratio) |
| All four digital tiles are derived from the same on-brand color-graded jobsite background (auto-toned + cool industrial temperature shift), not the raw stock photo | expert · quality · K4 | The four crops (1080x1080, 1920x1080, 350x120, 1:1) share a consistent on-brand cool/graded look traceable to the single graded jobsite asset rather than the ungraded stock original |
| titanseal_review_board is a Firefly Board deep-link presenting the logo-variant system plus key produced assets | auto · mandatory · K6 | A Firefly Board deep-link is produced and references the SVG, mono-black, reversed-white, brand-blue, horizontal-lockup, and social-tile assets |
| The out-of-scope items (brand-standards PDF body/typography authoring and Amazon UAE listing composition) are explicitly flagged as human/desktop finishing and not fabricated by the connector | expert · mandatory · K7 | The deliverable communication declares the brand-standards PDF body/typography pages and Amazon UAE listing page as out of connector scope and does not present them as produced outputs |


[[PAGEBREAK]]
### AO-54 · RoadWise — Branded Top-Down Traffic Shorts: Reusable Asset Kit, Color-Graded Frames, Vertical Cover + VO/Reel Prep
**Brand:** Automotive, Industrial & Agriculture &nbsp;·&nbsp; **Operation:** O3 Video & audio (Motion & Audio) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (17 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K5 · K1 · K6 · K7
*Build the RoadWise branded source-asset kit for the top-down traffic shorts: vectorize reusable road/vehicle/arrow icons to clean SVG, apply one consistent color grade across the reference frames, produce a 1080x1920 vertical cover/end-card and a stock-backed road texture, then clean the scratch VO and reframe the rough preview clip to vertical — all chained so the deliverable kit emerges from the supplied plates.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| topdown_junction_frame.png | image | A flat, top-down (bird's-eye) orthographic render of a 4-way road junction on neutral mid-gray asphalt, clean |
| icon_plate_cars_arrows_signs.png | image | A clean asset-sheet on pure white (#FFFFFF) background showing, laid out in a neat grid with generous spacing: |
| driving_sense_wordmark.png | image | A transparent-background PNG logo lockup: the wordmark 'RoadWise' in a friendly modern geometric sans-serif, w |
| scratch_vo_4way_stop.wav | audio | A warm, clear instructional voice-over, ~25 seconds: 'At a four-way stop, the first vehicle to arrive has the |
| ae_preview_lanechange_16x9.mp4 | video | A 12-second flat top-down 2D motion-graphics animation, 1920x1080, of a single car smoothly changing from the |
| caption_label_strings.json | data | Generate a small JSON array of 10 short on-road caption/label strings for driving shorts, e.g. {"scenario":"4- |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| drivingsense_icons.svg | vector | Clean auto-traced SVG icon set (top-down cars, turn-arrows, road signs) with closed solid-fill paths, transparent background, scalable for the AE template library. |
| junction_frame_graded.png | image | The top-down junction reference frame with the locked RoadWise brand grade (cool temp, reduced asphalt saturation, lifted clarity/contrast, punchy lane-yellow), 1024x1024 |
| cover_endcard_1080x1920.png | image | Vertical 1080x1920 cover / end-card: graded junction frame outpainted top+bottom to 9:16 with clean road headroom, brand-matched solid title band, wordmark color-consiste |
| asphalt_texture_grained.png | image | Licensed seamless asphalt stock with subtle film grain added, tileable road-base texture for the templates. PNG/JPEG full-res from the licensed presigned URL. |
| vo_4way_stop_clean.wav | audio | Denoised broadcast-clean voice-over (hiss/hum/reverb removed by media_enhance_speech), same content/length as the scratch take. |
| ae_preview_1080x1920.mp4 | video | The rough AE lane-change preview reframed to 1080x1920 vertical, SAME ~12s length, for vertical-crop sanity check. |
| drivingsense_kit_board | firefly_board | Firefly board deep-link assembling the produced kit assets (icons SVG preview, graded frame, cover, texture) as the hand-off moodboard, plus the font recommendation noted |

**Layer-3 verifier checks** — expert-authored (16 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| drivingsense_icons.svg is delivered as a valid SVG vector file | auto · mandatory · K1 | A file named drivingsense_icons.svg exists and is valid SVG markup whose root <svg> element parses |
| The traced SVG icon set contains the reusable top-down car, turn-arrow, and road-sign glyphs as closed solid-fill paths on a transparent background | expert · mandatory · K3 | drivingsense_icons.svg visibly includes top-down car-body glyphs, directional turn-arrows, and road-sign glyphs (e.g. STOP/YIELD/hazard) as clean closed solid-fill paths with no white background plate behind them |
| junction_frame_graded.png is delivered at exactly 1024x1024 PNG | auto · mandatory · K1 | File junction_frame_graded.png is PNG format with pixel dimensions exactly 1024 x 1024 |
| The locked RoadWise brand grade (cool temperature, reduced asphalt saturation, lifted clarity/contrast, punchy lane-line yellow) is visibly applied to the graded junction frame | expert · quality · K4 | junction_frame_graded.png reads cooler and higher-clarity/contrast than the source topdown_junction_frame.png with desaturated asphalt grays while the lane-line yellow stays punchy/saturated |
| cover_endcard_1080x1920.png is delivered at exactly 1080x1920 (9:16 vertical) PNG | auto · **dealbreaker** · K1 | File cover_endcard_1080x1920.png is PNG format with pixel dimensions exactly 1080 x 1920 |
| The cover/end-card is the graded junction frame outpainted top and bottom to 9:16 with clean road headroom, not a stretched or cropped square | expert · mandatory · K3 | The vertical cover shows the graded junction at correct aspect with newly generated road area extended above and below leaving clean headroom for title and logo; the original 1024x1024 frame is not distorted, stretched, or letterboxed |
| The cover/end-card carries a solid brand-charcoal title band region for the title/wordmark lockup | expert · quality · K2 | cover_endcard_1080x1920.png shows a solid-color (brand charcoal) filled band in the top headroom region to seat the title/wordmark, color-consistent with the RoadWise wordmark palette |
| The same locked color grade is applied identically to both the junction reference frame and the cover frame so all templates read as one brand | expert · quality · K4 | The road/asphalt and lane-yellow grade in cover_endcard_1080x1920.png matches that of junction_frame_graded.png (same cool / desaturated-asphalt / punchy-yellow treatment), not two different looks |
| asphalt_texture_grained.png is delivered as a full-res licensed Adobe Stock asphalt texture | auto · mandatory · K1 | File asphalt_texture_grained.png (PNG or JPEG) exists at full resolution and was sourced from the licensed Adobe Stock presigned download (asset_license_and_download_stock), not a generated or screenshotted image |
| The asphalt stock texture was licensed before any edit was applied to it | auto · **dealbreaker** · K6 | asset_license_and_download_stock was called and completed before image_add_grain in the workflow order |
| The asphalt texture has subtle film grain added and reads as a seamless tileable road base | expert · quality · K4 | asphalt_texture_grained.png shows added subtle film grain over the licensed asphalt and appears seamless/tileable as a road-base texture |
| vo_4way_stop_clean.wav is delivered as a denoised broadcast-clean WAV with the same 4-way-stop narration and same length as the scratch take | expert · mandatory · K1 | vo_4way_stop_clean.wav is a WAV with the hiss / HVAC-hum / room-reverb removed (via media_enhance_speech), the 4-way-stop narration content intact, and the same duration as scratch_vo_4way_stop.wav (no trim) |
| ae_preview_1080x1920.mp4 is delivered at exactly 1080x1920 with the same ~12s length as the source preview | auto · mandatory · K1 | File ae_preview_1080x1920.mp4 is MP4 with frame dimensions exactly 1080 x 1920 and duration within tolerance of the ~12s source ae_preview_lanechange_16x9.mp4 (no trim) |
| drivingsense_kit_board is delivered as a shareable Firefly board deep-link assembling the produced kit assets | auto · mandatory · K1 | A Firefly board deep-link/URL is returned that assembles the icons SVG preview (drivingsense_icons.svg), the graded junction frame, the cover/end-card, and the asphalt texture |
| A font recommendation for the on-road label/caption type is provided alongside the kit | expert · quality · K5 | font_recommend output names a specific caption/label typeface matching the RoadWise wordmark and the supplied caption_label_strings.json strings, noted alongside the board hand-off |
| No 2D animation, keyframing, or compositing is claimed or produced — only the source-asset kit and delivery prep | expert · mandatory · K7 | Deliverables contain no animated/keyframed/composited output authored from scratch; connector output is limited to the vectorized icons, graded junction frame, vertical cover, asphalt texture, cleaned VO, reframed preview, and board, with animation explicitly left to the AE artist |


[[PAGEBREAK]]
### AO-55 · Multi-Channel Meal-Prep Ad Package: Product-Showcase Video + Social Cutdowns + Retouched Hero Still + Vectorized Merch Logo
**Brand:** Food, Restaurant & Beverage &nbsp;·&nbsp; **Operation:** O3 Video & audio (Motion & Audio) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (25 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K5 · K1 · K6 · K7
*From the client's raw chicken-bowl hero photo, raw 4K product-showcase footage, raw phone-recorded voiceover, and flat logo PNG, produce a retouched website-banner hero still, a vertical + square + landscape cutdown set of the product-showcase video, a denoised voiceover, a screen-print-ready vector logo, and a moodboard of the package.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| chicken_bowl_hero_raw.jpg | image | Photoreal hand-held studio food photograph of a high-protein meal-prep chicken bowl: grilled sliced chicken br |
| product_showcase_4k_raw.mp4 | video | 70-second 4K 16:9 horizontal product-showcase b-roll of a high-protein chicken meal-prep bowl being assembled |
| founder_voiceover_raw.wav | audio | Warm, upbeat founder voiceover, ~20 seconds: 'Real food, prepped for real life. Fuel'd Kitchen's High-Protein |
| fueld_kitchen_logo_flat.png | image | Flat full-color brand wordmark logo 'FUEL'D KITCHEN' with a small flame-over-fork icon, bold modern sans-serif |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| hero_banner_still.png | image | Retouched website/feed hero still: auto-straightened, cropped to banner framing, auto-toned + exposure/contrast corrected, warmer color temperature, bowl popped against a |
| stock_steam_texture.jpg | image | Licensed Adobe Stock steam/food-texture still, color-temperature matched to the hero look, for the email header / landing-page background. Full-res licensed JPG. |
| showcase_9x16.mp4 | video | Reels/TikTok reframe of the product-showcase video to 1080x1920, SAME runtime as source (reframe only, no trim). |
| showcase_1x1.mp4 | video | Feed reframe to 1080x1080, same runtime as source. |
| showcase_sizzle.mp4 | video | AI quick-cut highlight/sizzle version (~15s target) of the product-showcase footage for the paid short-form ad. |
| founder_vo_clean.wav | audio | Denoised/de-hummed founder voiceover, voice-only enhancement, ready to lay under the cutdowns. |
| showcase_summary.txt | data | Short text content-summary of the showcase footage (scene/transcript summary) for the post caption and scheduling sheet. |
| fueld_logo_vector.svg | vector | Screen-print-ready vectorized wordmark with clean closed paths for the meal-prep container labels. |
| fueld_package_board | data | Firefly Board deep-link assembling the finished package (hero still, stock texture, vector logo, cutdown thumbnails) for client review. |

**Layer-3 verifier checks** — expert-authored (18 checks, 1 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All eight named deliverables plus the Firefly Board are present in the package | auto · mandatory · K1 | The package contains all 8 named outputs: hero_banner_still.png, stock_steam_texture.jpg, showcase_9x16.mp4, showcase_1x1.mp4, showcase_sizzle.mp4, founder_vo_clean.wav, showcase_summary.txt, and fueld_logo_vector.svg, plus the fueld_package_board Firefly Board deep-link |
| Hero banner still is delivered as a PNG in sRGB at approximately 2400px wide | auto · mandatory · K1 | hero_banner_still.png is PNG format, sRGB color space, and approximately 2400px in width (within ~10%, i.e. ~2160-2640px) |
| Hero still is top-extended into a tall hero-banner canvas via generative outpaint | expert · mandatory · K3 | hero_banner_still.png shows canvas added at the TOP of the original frame (taller than the cropped source) with the generated region seamlessly continuing the scene, producing a tall hero-banner aspect ratio |
| Hero still horizon is leveled and the frame is cropped to banner framing | expert · mandatory · K3 | the ~4-degree tilt of the source chicken_bowl_hero_raw.jpg is corrected so the horizon/table line is level, and the loose wider-than-banner framing is cropped down to website-banner framing |
| Hero still is auto-toned, exposure/contrast corrected, and warmed to an appetizing temperature | expert · quality · K4 | compared to the flat/under-saturated source, hero_banner_still.png shows corrected tone/exposure/contrast and a visibly warmer color temperature giving an appetizing food look |
| The bowl is popped against a softened/blurred background | expert · quality · K3 | the chicken bowl subject is in sharp focus while the surrounding background is softened/blurred, with a clean subject edge and no blur bleeding onto the bowl |
| Stock steam/texture still is a licensed Adobe Stock full-res JPG of steaming-food / texture content | auto · mandatory · K1 | stock_steam_texture.jpg is a full-resolution licensed Adobe Stock JPG depicting steaming-food / texture content (acquired via asset_license_and_download_stock) |
| Stock steam still color temperature is matched to the warmed hero look | expert · quality · K4 | stock_steam_texture.jpg color temperature is visibly adjusted to match the warm hero_banner_still.png so the two read as part of one consistent package |
| 9:16 cutdown is exactly 1080x1920 at the same runtime as the source (reframe only, no trim) | auto · mandatory · K1 | showcase_9x16.mp4 dimensions are exactly 1080x1920 and its duration equals the source product_showcase_4k_raw.mp4 duration (~70s, no trimming) |
| 1:1 cutdown is exactly 1080x1080 at the same runtime as the source (reframe only, no trim) | auto · mandatory · K1 | showcase_1x1.mp4 dimensions are exactly 1080x1080 and its duration equals the source product_showcase_4k_raw.mp4 duration (~70s, no trimming) |
| A landscape 16:9 version preserving the original source dimensions and full runtime is delivered | auto · mandatory · K1 | a 16:9 deliverable is provided that matches the original product_showcase_4k_raw.mp4 frame ratio (16:9, e.g. 1920x1080) at the full source runtime (~70s, no trim) |
| Sizzle cutdown is an AI quick-cut highlight of about 15 seconds | auto · mandatory · K1 | showcase_sizzle.mp4 is an edited AI quick-cut highlight reel of the showcase footage with a runtime of approximately 15 seconds (clearly shorter than the ~70s source) |
| Founder voiceover is a denoised/de-hummed voice-only enhancement, not a loudness or music task | expert · mandatory · K1 | founder_vo_clean.wav has the room hiss and HVAC hum removed via voice-only speech enhancement while the founder's words remain intact and intelligible; no music added and not merely loudness-normalized |
| Showcase summary is a short text content-summary of the showcase footage | auto · mandatory · K5 | showcase_summary.txt is a text file containing a short scene/transcript content-summary of the product-showcase footage suitable for a post caption / scheduling sheet |
| Logo is delivered as a screen-print-ready SVG vector with clean closed paths and no embedded raster | auto · mandatory · K1 | fueld_logo_vector.svg is a valid SVG with closed vector paths and no embedded raster bitmap, suitable for screen-print container labels |
| Vectorized logo preserves the original FUEL'D KITCHEN wordmark and is not regenerated or altered | expert · **dealbreaker** · K2 | the vector wordmark matches the supplied fueld_kitchen_logo_flat.png (FUEL'D KITCHEN text, flame-over-fork icon, charcoal + amber palette) with no redrawn letterforms, recoloring, or invented brand elements |
| Firefly Board deep-link assembles the finished package for client review | auto · mandatory · K6 | fueld_package_board is a valid Firefly Board deep-link whose board contains hero_banner_still, the color-matched stock_steam_texture, the fueld_logo_vector, and a cutdown thumbnail (showcase_9x16) |
| Only Adobe Creative Cloud connector tools were used and each editing chain builds on the prior output | expert · mandatory · K6 | every deliverable is produced solely via Adobe CC connector tools (no Canva, no Express widgets, no non-Adobe/local editing) and the photo/logo/video/audio chains each consume the prior step's output rather than originating new content, except the allowed asset_license_and_download_stock acquisition and the raw asset uploads |


[[PAGEBREAK]]
### AO-56 · Comedy Gameplay YouTube Edit: Sizzle Cut, Reframed Shorts Variant, Meme Cutaway Graphics + Clickbait Thumbnail
**Brand:** Music, Film, Publishing & Media &nbsp;·&nbsp; **Operation:** O3 Video & audio (Motion & Audio) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (18 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K5 · K1 · K6 · K7
*Turn raw comedy gameplay footage plus client notes, custom graphics and a music folder into a punchy 1080p H.264 YouTube cut with a vertical Shorts variant, polished meme/text-callout overlay graphics, a denoised commentary track, and a clickbait thumbnail PNG — all organized into one reusable project package.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| raw_gameplay_capture.mp4 | video | Screen-recorded first-person competitive shooter gameplay, 1080p, 22-minute-style ranked match feel rendered a |
| commentary_adlibs.wav | audio | Energetic young male streamer ad-libbing reactions over gameplay: 'oh no no no — NOT like this', 'bro why is m |
| funny_moment_notes.csv | data | CSV with columns timestamp,label,reaction_type for ~10 flagged comedy beats across a 22-min match, e.g. 00:03: |
| pov_meme_screenshot.png | image | A meme-style reaction screenshot: bold white impact-font top text reading 'POV: your teammate has the aim of a |
| hero_thumbnail_frame.png | image | A dramatic high-action gameplay still earmarked for a YouTube thumbnail: explosion/muzzle flash, character mid |
| royalty_free_music_folder | audio | Stand-in royalty-free background tracks folder reference: two upbeat royalty-free instrumental loops (one trap |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| comedy_edit_master_1080p_h264.mp4 | video | Edited fast-paced comedy cut, 1920x1080, H.264/MP4, ~3-4 min target, produced by an AI Quick Cut driven by the funny-moment notes — the YouTube master deliverable. |
| comedy_edit_shorts_1080x1920.mp4 | video | Vertical reframed teaser of the master cut, 1080x1920, H.264/MP4, SAME length as its source clip (reframe only, no trim) — YouTube Shorts variant. |
| youtube_thumbnail_1280x720.png | image | Clickbait thumbnail: straightened, auto-toned, contrast/saturation-punched hero frame with clickbait color overlay, cropped/resized to 1280x720 PNG. |
| meme_cutaway_tile.png | image | High-contrast duotone/halftone meme reaction tile derived from the 'POV:' screenshot, ready to drop in as an on-screen cutaway. |
| text_callout_card_1.svg | vector | Crisp vectorized text-callout graphic (SVG) for on-screen punchline call-outs, stays sharp under reaction zooms. |
| text_callout_card_2.svg | vector | Second vectorized SVG text-callout card, matching style, for a different beat. |
| cleaned_commentary.wav | audio | Denoised/cleaned commentary ad-lib voice track (speech-only enhancement) for layering over gameplay. |
| project_package | data | A CC project folder containing every source + produced asset plus a Firefly Board deep-link that ties them together as the reusable 'project file' reference; plus a music |

**Layer-3 verifier checks** — expert-authored (17 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| The edited comedy master video is delivered in H.264/MP4 format | auto · **dealbreaker** · K1 | comedy_edit_master_1080p_h264.mp4 is a valid MP4 file whose video stream is H.264-encoded |
| The comedy master video is 1920x1080 (1080p) | auto · mandatory · K1 | comedy_edit_master_1080p_h264.mp4 has frame dimensions exactly 1920x1080 |
| The vertical Shorts variant is delivered at the 1080x1920 portrait dimensions in H.264/MP4 | auto · mandatory · K1 | comedy_edit_shorts_1080x1920.mp4 is a valid H.264/MP4 file with frame dimensions exactly 1080x1920 |
| The Shorts variant is a reframe of the master with the same length (reframe only, no trim) | auto · mandatory · K1 | comedy_edit_shorts_1080x1920.mp4 duration equals the duration of comedy_edit_master_1080p_h264.mp4 within one-frame tolerance |
| The YouTube thumbnail is delivered as a PNG at the exact spec dimensions | auto · mandatory · K1 | youtube_thumbnail_1280x720.png is a PNG file with dimensions exactly 1280x720 |
| The thumbnail is built from the supplied hero_thumbnail_frame.png (not a regenerated/substituted image) | expert · mandatory · K2 | youtube_thumbnail_1280x720.png is recognizably the supplied hero gameplay still (same explosion/muzzle-flash mid-dive scene), processed rather than replaced by a different generated image |
| The thumbnail shows the straighten + auto-tone + contrast/saturation-punch + clickbait color-overlay treatment | expert · mandatory · K3 | youtube_thumbnail_1280x720.png is leveled (not crooked), brighter/contrastier than the underexposed source, with punched saturation and a clickbait orange-teal color overlay applied |
| The meme cutaway tile is a high-contrast duotone/halftone treatment of the supplied 'POV:' screenshot | expert · mandatory · K2 | meme_cutaway_tile.png is recognizably derived from the supplied pov_meme_screenshot.png and shows a high-contrast duotone or halftone effect, ready as an on-screen cutaway |
| Two text-callout cards are delivered as valid SVG vector files | auto · mandatory · K1 | text_callout_card_1.svg and text_callout_card_2.svg both exist and are well-formed SVG files |
| The two SVG callout cards stay crisp/sharp when scaled up (true vector paths, not embedded raster) | expert · quality · K3 | text_callout_card_1.svg and text_callout_card_2.svg render as resolution-independent vector paths that stay clean at zoom, not just a bitmap wrapped in an SVG element |
| The cleaned commentary track is delivered as a WAV with speech-only denoise/enhancement applied | expert · mandatory · K1 | cleaned_commentary.wav is a WAV of the commentary ad-libs that audibly has the cheap-mic hiss/reverb/plosives reduced versus commentary_adlibs.wav while preserving the speech |
| One royalty-free 'explosion/impact' stock sound is licensed (not preview) and added to the project | auto · quality · K6 | An Adobe Stock 'explosion/impact' audio asset is licensed (not a watermarked preview) and its full-res asset is present in the project package |
| A music summary is produced from the supplied royalty-free music stems and included in the project package | expert · quality · K1 | project_package includes a media_summarize-derived content/energy summary of the supplied music stems, present as the beat/timing reference note |
| A Creative Cloud project folder named 'Comedy_Gameplay_Edit' holds the source and produced assets | auto · mandatory · K6 | A CC project folder named exactly 'Comedy_Gameplay_Edit' exists and contains the ingested source files plus the produced deliverables |
| A Firefly Board deep-link ties the produced assets together as the reusable 'project file' reference | auto · mandatory · K6 | project_package contains a Firefly Board deep-link aggregating the thumbnail (youtube_thumbnail_1280x720.png), meme tile (meme_cutaway_tile.png), both SVG callouts, the master cut, the Shorts cut, and the cleaned commentary |
| All eight produced deliverables are present in the handoff | auto · **dealbreaker** · K1 | comedy_edit_master_1080p_h264.mp4, comedy_edit_shorts_1080x1920.mp4, youtube_thumbnail_1280x720.png, meme_cutaway_tile.png, text_callout_card_1.svg, text_callout_card_2.svg, cleaned_commentary.wav, and project_package all exist |
| The comedy edit is a tight fast-paced cut driven by the client's funny-moment notes (dead air trimmed, comedy-sketch pacing) | expert · quality · K4 | comedy_edit_master_1080p_h264.mp4 is noticeably shorter than the ~22-min source (roughly a 3-4 min cut), removes dead air, retains the flagged funny beats from funny_moment_notes.csv, and has rapid comedy pacing |


[[PAGEBREAK]]
### AO-57 · Phonk-Energy 9:16 Reel/TikTok Edit Package — Sizzle Cut, Reframe, Cleaned VO, and Scroll-Stopping Thumbnail
**Brand:** Music, Film, Publishing & Media &nbsp;·&nbsp; **Operation:** O3 Video & audio (Motion & Audio) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (30 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K5 · K1 · K6 · K7
*Turn one batch of raw vertical clips plus a hero still, brand logo, and a voiceover scratch track into a post-ready 9:16 phonk-energy short: an AI sizzle cut reframed to 1080x1920, a cleaned VO track, an on-screen caption sheet, and a fully color-graded exported thumbnail with a vector logo lockup.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| raw_clip_nightdrive_01.mp4 | video | Handheld vertical 9:16 phone footage, 1080x1920, ~12 seconds, night drive through a neon-lit city street, dash |
| raw_clip_nightdrive_02.mp4 | video | Handheld vertical 9:16 phone footage, 1080x1920, ~10 seconds, subject in hoodie walking under an underpass at |
| raw_clip_nightdrive_03.mp4 | video | Vertical 9:16 phone footage, 1080x1920, ~9 seconds, slow push-in on rain-slick asphalt reflecting neon signage |
| hero_cover_still.png | image | Photoreal vertical still, 1080x1920 portrait, a person in a hoodie half-lit by neon under a city underpass at |
| brand_wordmark_logo.png | image | Flat minimalist wordmark logo on transparent background, the single word 'NOCTURNE' in a tight geometric sans- |
| voiceover_scratch.wav | audio | A short ~18-second moody spoken voiceover line for a phonk reel, confident low-energy delivery, e.g. 'After da |
| captions_script.json | data | Generate a small JSON array of 6 caption cues for a ~30s vertical reel, each cue with fields {index, start_sec |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| phonk_sizzle_9x16.mp4 | video | 1x vertical 1080x1920 (9:16) MP4, ~30s, H.264, AI sizzle assembly of the three night-drive clips reframed to full-frame vertical, Instagram & TikTok ready. Produced by th |
| voiceover_clean.wav | audio | Cleaned voiceover track: isolated speech stem from media_enhance_speech (room hiss, HVAC rumble and reverb suppressed), WAV, ready to lay under the reel. Background/rever |
| reel_captions.json | data | On-screen captions/text cue sheet (6 timed cues) stored alongside the project in the client's Creative Cloud folder for the editor to apply as text animations. |
| thumbnail_cover_1080x1920.png | image | Exported, fully color-graded vertical cover/thumbnail, PNG 1080x1920: straightened, auto-toned, phonk-graded (cool teal shadows + magenta highlight bite), subject-popped, |
| NOCTURNE_logo.svg | vector | Clean vectorized brand wordmark (SVG) produced from the flat logo PNG, used as the scalable corner lockup on the thumbnail and reusable for future covers. |
| reel_package.zip | archive | Single zip bundling the deliverables (MP4, cleaned VO WAV, captions JSON, graded thumbnail PNG, logo SVG) plus the kept-in-CC source references, for one-click handoff. |

**Layer-3 verifier checks** — expert-authored (16 checks, 2 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| Final reel video phonk_sizzle_9x16.mp4 has exact pixel dimensions 1080x1920 (9:16 vertical) | auto · mandatory · K1 | ffprobe of phonk_sizzle_9x16.mp4 reports width=1080 and height=1920 |
| Final reel is an H.264 MP4 with a runtime in the brief's stated 15-45s window | auto · mandatory · K1 | phonk_sizzle_9x16.mp4 container is MP4 with H.264 video codec and duration is between 15 and 45 seconds inclusive |
| The reel is the AI sizzle assembly of the three night-drive clips reframed to vertical, NOT a from-scratch or single-clip export | expert · mandatory · K6 | Reel visibly assembles content drawn from raw_clip_nightdrive_01/02/03 (night-drive neon street, hoodie subject under the underpass, and rain-slick neon reflections) reframed full-frame to 9:16 |
| Reframe to 9:16 preserves the sizzle cut's length (no trim applied at the resize step) | auto · quality · K6 | phonk_sizzle_9x16.mp4 duration equals the sizzle-cut (quick_cut) source duration within rounding tolerance (resize-only, same length, no trim) |
| Cleaned voiceover deliverable voiceover_clean.wav is delivered as a WAV audio file | auto · mandatory · K1 | voiceover_clean.wav exists and is a valid WAV (RIFF/WAVE) audio file |
| The voiceover track is audibly cleaned versus the noisy scratch input — room hiss, HVAC rumble and reverb suppressed and the spoken line isolated | expert · mandatory · K4 | voiceover_clean.wav has the spoken line clearly isolated with the room-tone hiss, HVAC rumble and reverb of voiceover_scratch.wav substantially reduced |
| Captions deliverable reel_captions.json contains exactly 6 timed caption cues with the required cue fields | auto · mandatory · K1 | reel_captions.json parses as a JSON array of exactly 6 cue objects, each containing the fields index, start_seconds, end_seconds, and text |
| Exported thumbnail thumbnail_cover_1080x1920.png has exact pixel dimensions 1080x1920 and is PNG format | auto · mandatory · K1 | thumbnail_cover_1080x1920.png is a PNG file with width=1080 and height=1920 |
| Thumbnail is straightened — the source hero still's ~3-degree handheld tilt corrected so the horizon is level | expert · quality · K3 | The thumbnail cover shows a level horizon with the hero_cover_still.png ~3-degree handheld tilt removed |
| Thumbnail carries the on-brand phonk color grade: cool teal shadows and magenta highlight bite | expert · mandatory · K4 | Thumbnail shadows read cool/teal and highlights carry a magenta/pink bite, consistent with the stated phonk grade rather than the mixed warm-and-cool source white balance of the hero still |
| Thumbnail shows the hoodie subject popped from the neon background and carries halftone + film-grain texture | expert · quality · K3 | The hoodie subject is selectively lifted (vibrance/saturation) so it separates from the neon background, and a halftone texture plus fine film grain are visibly present on the cover |
| Brand wordmark vector deliverable NOCTURNE_logo.svg is delivered as an SVG | auto · mandatory · K1 | NOCTURNE_logo.svg exists and is a valid SVG file containing vector path data |
| The vectorized logo preserves the original 'NOCTURNE' wordmark and is not regenerated or restyled | expert · **dealbreaker** · K2 | NOCTURNE_logo.svg reproduces the supplied brand_wordmark_logo.png 'NOCTURNE' wordmark (same glyphs, tight geometric sans-serif, solid white) with clean crisp edges and no redesigned or restyled lettering |
| The deliverable package bundles the five produced assets together for handoff (MP4, cleaned VO WAV, captions JSON, graded thumbnail PNG, logo SVG) | auto · mandatory · K1 | reel_package.zip (or the dated CC handoff folder produced by asset_copy_assets) contains all five files: phonk_sizzle_9x16.mp4, voiceover_clean.wav, reel_captions.json, thumbnail_cover_1080x1920.png, and NOCTURNE_logo.svg |
| Out-of-scope timeline work (frame-accurate cuts, hard transitions, motion graphics, beat-synced music, caption burn-in, logo lockup compositing) is NOT falsely claimed as delivered by the automated connector pass | expert · **dealbreaker** · K7 | The handoff honestly flags frame-accurate cuts/hard-transitions/motion-graphics/beat-synced-music, caption burn-in onto video, and the logo-lockup placement on the thumbnail as the manual human-finish steps and does not present them as completed automated output |
| The thumbnail PNG is the graded cover WITHOUT the logo burned in — the logo lockup placement is left as the flagged human-finish step | expert · mandatory · K7 | thumbnail_cover_1080x1920.png is the color-graded/cropped cover with no NOCTURNE wordmark composited onto it; the SVG logo is delivered separately for the human editor to place |


[[PAGEBREAK]]
### AO-58 · Repeatable Adobe pipeline turning one raw exercise clip into a branded vertical coaching reel (subtitles cue, cleaned VO, watermark, muscle-group callout)
**Brand:** Real Estate, Construction & Property &nbsp;·&nbsp; **Operation:** O3 Video & audio (Motion & Audio) &nbsp;·&nbsp; **Horizon:** H3 composite (15 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K5 · K1 · K6 · K7
*Run our repeatable exercise-reel pipeline on one raw 'Goblet Squat' clip: summarize it for subtitle/cue text and naming, clean the coaching voiceover, build the reusable white-watermark and branded muscle-group arrow overlays, reframe to vertical, cut a 30s reference reel, and file everything under our naming convention.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| goblet_squat_raw_4k.mp4 | video | Handheld documentary 4K 3840x2160 landscape clip, ~45 seconds, of a real fitness coach in a slightly worn comm |
| gym_logo_square.png | image | A clean square brand logo for a personal-training gym named 'IRONLINE COACHING' — a bold geometric barbell-and |
| muscle_arrow_callout_raw.png | image | A single flat hand-drawn-style curved red arrow with a small 'GLUTES' tag at the tail, drawn with a marker tex |
| coach_cue_script.json | data | Generate a small JSON object with the exercise metadata and the spoken coaching-cue lines for a goblet squat d |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| goblet_squat_subtitle_cue_source.txt | text/summary | AI scene/transcript-style summary of the raw clip (media_summarize output) capturing the spoken form cues + rep structure, usable as Premiere subtitle + on-screen cue sou |
| goblet_squat_VO_clean.wav | audio | Coach's spoken cue track de-echoed/denoised (voice only) via media_enhance_speech, ready to drop under the reel. |
| watermark_white_corner.png | image | Transparent PNG of the gym logo, background removed, recolored solid white, cropped/resized to a corner-badge overlay size (~400x400) — reusable library-wide watermark. |
| muscle_arrow_accent.svg | vector | Clean vectorized muscle-group callout arrow recolored to the brand accent and sized as an overlay element — reusable library-wide. |
| goblet_squat_vertical_full.mp4 | video | Raw clip reframed to 1080x1920 vertical, full original length (no trim) via video_resize. |
| goblet_squat_reference_reel_30s.mp4 | video | ~30s AI highlight cut (video_create_quick_cut) of the vertical clip — the punchy key-reps reference reel. |
| Exercise_LowerBody_GobletSquat_folder | asset-folder | CC asset folder following the naming convention containing the finished reel + reusable watermark + arrow overlay, copied in and ready to template across the library. |

**Layer-3 verifier checks** — expert-authored (17 checks, 1 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| All 7 expected deliverables are present: subtitle/cue source text, clean VO wav, white corner watermark PNG, accent muscle-arrow SVG, vertical full clip, 30s reference reel, and the organized library folder | auto · mandatory · K1 | All of goblet_squat_subtitle_cue_source.txt, goblet_squat_VO_clean.wav, watermark_white_corner.png, muscle_arrow_accent.svg, goblet_squat_vertical_full.mp4, goblet_squat_reference_reel_30s.mp4, and the Exercise_LowerBody_GobletSquat folder exist; count == 7 |
| The subtitle/cue source is an AI scene/transcript-style summary of the raw clip capturing the spoken goblet-squat form cues and rep structure | expert · mandatory · K4 | goblet_squat_subtitle_cue_source.txt is a transcript/scene-style summary of the raw clip referencing the goblet squat, the spoken form cues (e.g. chest up, weight in the heels, drive through the floor), and the rep structure (4-5 reps), usable as Premiere subtitle/on-screen cue source text |
| The cleaned voiceover is a de-echoed/denoised voice-only track produced from the raw clip's coaching audio | expert · mandatory · K4 | goblet_squat_VO_clean.wav contains the coach's spoken cues with the gym reverb/echo and noise reduced, voice-only (no added music/ambience), and is intelligibly cleaner than the raw clip's camera-mic audio |
| The clean VO is delivered as a valid WAV audio file | auto · mandatory · K1 | goblet_squat_VO_clean.wav is a valid .wav audio file (audio container/codec readable, non-zero duration) |
| The watermark is the gym logo with its background removed (transparent) | auto · mandatory · K1 | watermark_white_corner.png is a PNG with an alpha channel and transparent (non-opaque) background pixels around the mark |
| The watermark logo is recolored solid white so it reads on dark gym footage | auto · mandatory · K1 | The opaque (non-transparent) logo pixels in watermark_white_corner.png are solid white (RGB approximately 255,255,255), not the original dark charcoal #1C1C1C |
| The watermark is cropped/resized to a corner-badge overlay size of approximately 400x400 px | auto · quality · K1 | watermark_white_corner.png dimensions are approximately 400x400 px (within roughly +/-10%) |
| The watermark mark is the supplied IRONLINE COACHING barbell-and-line monogram (not regenerated or substituted) | expert · **dealbreaker** · K2 | The shape/monogram in watermark_white_corner.png matches the supplied gym_logo_square.png IRONLINE COACHING barbell-and-line monogram; only background removal, white recolor, and resize were applied — the logo artwork itself is not regenerated or altered |
| The muscle-group callout arrow is delivered as a vector SVG file with path geometry | auto · mandatory · K1 | muscle_arrow_accent.svg is a valid SVG (vector) file containing path geometry of the traced arrow |
| The vectorized arrow is recolored to the brand accent red and cleaned up from the raw hand-drawn artwork | expert · mandatory · K2 | The arrow shape in muscle_arrow_accent.svg is filled with the brand accent red (#D8352A family per spec) as a clean solid color, and the rough hand-drawn marker edges have been cleaned into crisp scalable shapes |
| The vertical full clip is reframed to exactly 1080x1920 vertical | auto · mandatory · K1 | goblet_squat_vertical_full.mp4 has frame dimensions 1080x1920 (portrait) |
| The vertical full clip retains the full original ~45s length with no trimming at the reframe step | auto · mandatory · K1 | goblet_squat_vertical_full.mp4 duration is approximately equal to the raw ~45s source clip duration (full length, not shortened) |
| The reference reel is an AI highlight cut of approximately 30 seconds and shorter than the full clip | auto · mandatory · K1 | goblet_squat_reference_reel_30s.mp4 duration is approximately 30s (within roughly +/-5s) and is shorter than goblet_squat_vertical_full.mp4 |
| The reference reel is vertical 1080x1920, derived from the reframed vertical clip | auto · mandatory · K1 | goblet_squat_reference_reel_30s.mp4 has frame dimensions 1080x1920 (portrait), consistent with being cut from goblet_squat_vertical_full.mp4 |
| The library folder follows the exact naming convention Exercise / LowerBody / GobletSquat | auto · mandatory · K1 | The created CC asset folder path/name matches the convention Exercise/LowerBody/GobletSquat (slug 'Exercise/LowerBody/GobletSquat') |
| The organized library folder contains the finished reel plus the reusable watermark and arrow overlay assets copied in | auto · mandatory · K6 | The Exercise/LowerBody/GobletSquat folder contains goblet_squat_reference_reel_30s.mp4, watermark_white_corner.png, and muscle_arrow_accent.svg (3 assets copied in) |
| No frame-by-frame compositing was performed — subtitles, watermark, and arrow are delivered as separate prepared assets, not burned into the video | expert · mandatory · K7 | Per the brief's honesty note, the delivered reel does NOT have subtitles, watermark, or arrow burned/composited onto the frames; those remain separate source/overlay assets and the agent does not claim to have done the Premiere burn-in/compositing step |


[[PAGEBREAK]]
### AO-60 · Packaging-Portfolio Sizzle Reel: Grade the Stills, Cut the Hero Video
**Brand:** Video Editing &amp; Motion Graphics &nbsp;·&nbsp; **Operation:** O3 Video & audio (Motion & Audio) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (18 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K5 · K1 · K6 · K7
*Take my mixed-lighting packaging photos, color-grade them into one cohesive polished hero set, then assemble a fast-paced 16:9 website sizzle reel plus a square social cut and a moodboard.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| pkg_tea_carton.jpg | image | Photoreal studio product photograph of a premium tea carton (rectangular folding box) with a botanical illustr |
| pkg_cosmetics_jar.jpg | image | Photoreal studio shot of a frosted-glass cosmetics cream jar with a matte gold lid and minimalist label, on a |
| pkg_coffee_bag.jpg | image | Photoreal studio photograph of a matte-black stand-up coffee pouch with a copper foil logo and side gusset, on |
| pkg_beer_can.jpg | image | Photoreal studio shot of a 440ml craft-beer aluminum can with a bold wraparound illustrated label, condensatio |
| pkg_perfume_box.jpg | image | Photoreal studio photograph of a luxury perfume box with crisp embossed serif wordmark and a thin foil border, |
| pkg_chocolate_sleeve.jpg | image | Photoreal studio shot of a chocolate bar in a printed paper sleeve with a colorful geometric pattern and legib |
| pkg_kraft_box_titlecard.jpg | image | Photoreal studio photograph of a plain unbranded kraft cardboard box centered on a seamless light-grey studio |
| studio_texture_plate (stock — searched, not supplied) | image | Photoreal subtle light-grey concrete-and-paper studio backdrop texture, soft top-down light, fine grain, neutr |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| packaging_sizzle_hero_16x9.mp4 | video | Fast-paced energetic sizzle reel, 1920x1080 (16:9), ~20s, assembled from the 6 graded packaging frames + extended title card + stock intro/outro plate via Quick Cut. Webs |
| packaging_sizzle_social_1x1.mp4 | video | 1080x1080 (1:1) square reframe of the hero reel, SAME length (video_resize is same-duration), for Instagram feed. (A) |
| graded_frames_1920x1080/ (6 stills) | image | Six cohesively color-graded, straightened, preset+grain-matched packaging stills, each cropped/resized to 1920x1080 JPEG — the frame set the reel is built from. (C) |
| titlecard_kraft_fullbleed.png | image | Kraft-box title card outpainted to a wide 1920x1080 full-bleed plate with clean negative space for logo overlay. (C) |
| cosmetics_jar_cutout_charcoal.png | image | Cosmetics jar with background removed, composited onto a solid charcoal (#2B2B2B) card via solid-fill — clean hero variant. (C) |
| look_signoff_moodboard (Firefly Board deep-link) | data | Firefly Board assembling the 6 graded frame URNs + title card + cut-out for client look sign-off before launch. (C) |

**Layer-3 verifier checks** — expert-authored (16 checks, 0 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| The 16:9 website hero sizzle reel deliverable packaging_sizzle_hero_16x9.mp4 is present and playable. | auto · mandatory · K1 | A file named packaging_sizzle_hero_16x9.mp4 exists and is a valid, playable MP4 video. |
| The hero reel resolution matches the spec (1920x1080, 16:9). | auto · mandatory · K1 | packaging_sizzle_hero_16x9.mp4 is exactly 1920x1080 px (16:9 aspect ratio). |
| The hero reel runs approximately 20 seconds. | auto · mandatory · K1 | packaging_sizzle_hero_16x9.mp4 duration is between 18 and 22 seconds (~20s as specified). |
| The square Instagram social cut packaging_sizzle_social_1x1.mp4 is present and exactly 1080x1080. | auto · mandatory · K1 | packaging_sizzle_social_1x1.mp4 exists, is a valid MP4, and is exactly 1080x1080 px (1:1). |
| The square social cut is the same length as the hero reel (video_resize is same-duration, never trims). | auto · mandatory · K1 | packaging_sizzle_social_1x1.mp4 duration equals packaging_sizzle_hero_16x9.mp4 duration within ~0.5s. |
| The graded still set contains exactly six packaging frames at the uniform target size as JPEGs. | auto · mandatory · K1 | graded_frames_1920x1080/ contains exactly 6 JPEG stills, each exactly 1920x1080 px. |
| The six graded frames correspond to the six supplied packaging subjects, one per frame. | expert · mandatory · K2 | All six distinct supplied packaging products (tea carton, cosmetics jar, coffee bag, craft-beer can, perfume box, chocolate bar sleeve) appear across the graded frame set, one per frame, none missing or duplicated. |
| The six graded frames read as one cohesive set with a single unified grade. | expert · mandatory · K3 | Across all 6 frames the mixed white balance is neutralized toward one clean studio white point, one consistent cinematic Lightroom preset look is applied, and film grain is uniform; no frame looks visibly warmer/cooler or stylistically off from the rest. |
| Print colors are punchy but not blown out (vibrance pushed without clipping). | expert · quality · K4 | Printed/illustrated package colors read as saturated and vivid while highlights and saturated channels retain detail and are not clipped or blown out. |
| The crooked source frames are straightened and the underexposed/dark frames are corrected. | expert · mandatory · K3 | The tea-carton (~2 degree tilt) and beer-can (~1.5 degree tilt) horizons read level with no residual tilt, and the previously crushed-shadow coffee bag shows lifted, legible dark print detail. |
| The kraft-box title card titlecard_kraft_fullbleed.png is outpainted to a wide full-bleed 1920x1080 plate with clean negative space. | auto · mandatory · K1 | titlecard_kraft_fullbleed.png exists, is a valid PNG exactly 1920x1080 px, and shows the kraft box with extended empty studio sweep (negative space) for a logo overlay. |
| The title-card canvas extension is seamless (outpaint blends invisibly with the original sweep). | expert · mandatory · K3 | The boundary between the original kraft-box frame and the generated extended studio sweep shows no visible seam, tone break, texture mismatch, or repetition artifact. |
| The cosmetics-jar cut-out hero variant cosmetics_jar_cutout_charcoal.png is on a solid charcoal card of the exact specified color. | auto · mandatory · K1 | cosmetics_jar_cutout_charcoal.png exists, is a valid PNG, and its background is a solid fill of charcoal #2B2B2B with the cosmetics jar seated on top. |
| The cosmetics-jar background removal has clean edges. | expert · quality · K3 | The jar is cleanly cut out with no background halo, fringing, or chopped edges against the charcoal card; the frosted glass and gold-lid silhouette are intact. |
| A licensed Adobe Stock studio-texture plate is used as the intro/outro background (license-before-use, no watermarked/unlicensed plate). | auto · mandatory · K7 | A studio-texture stock plate was licensed via asset_license_and_download_stock and appears as the intro/outro background of the hero reel with no visible Adobe Stock watermark. |
| The look-signoff moodboard is delivered as a valid Firefly Board deep-link assembling the graded frames, title card, and cut-out. | auto · mandatory · K1 | look_signoff_moodboard is a valid Firefly Board deep-link whose board contains the 6 graded frame URNs plus titlecard_kraft_fullbleed and cosmetics_jar_cutout_charcoal. |


[[PAGEBREAK]]
### AO-61 · Fun YouTube Podcast: clean-audio cut, reframed 1080p sizzle, and a branded graphics kit (lower-third + end-screen + vector logo)
**Brand:** Music, Film, Publishing &amp; Media &nbsp;·&nbsp; **Operation:** O3 Video & audio (Motion & Audio) &nbsp;·&nbsp; **Horizon:** H4 long-horizon (20 tool calls) &nbsp;·&nbsp; **Capability profile:** K3 · K1 · K6 · K7
*Turn the raw podcast footage into a clean-voiced, reframed 1080p YouTube master plus a fun branded graphics kit (vector logo + lower-third + end-screen as PNG-transparent/vector), delivered separately.*
**Input assets** (the client handoff)
| asset | kind | what it is |
|---|---|---|
| podcast_raw_master_1080p.mp4 | video | 1080p handheld documentary-style YouTube podcast recording, two casual hosts (one woman in her 30s with curly |
| host_voice_scratch_track.wav | audio | Two-person casual podcast banter, ~90 seconds, friendly conversational tone, a few natural um/uh stumbles and |
| brand_logo_lockup.png | image | Flat circular podcast brand logo lockup reading 'THE LONG WAY ROUND' with a small retro campervan icon, bold f |
| lower_third_texture_plate.jpg | image | Close-up macro photo of warm kraft-paper / linen texture with soft natural side lighting and subtle paper fibe |

**Expected outputs** (the deliverables)
| output | kind | spec |
|---|---|---|
| podcast_voice_cleaned.wav | audio | Denoised/de-hissed voice track, voices clear and balanced; WAV, voice-only enhancement (no music processing, no loudness mastering) — the brief's 'clear and balanced voic |
| podcast_coldopen_sizzle_1080p.mp4 | video | ~20s AI highlight/sizzle reel for the cold-open, 1920x1080, sourced from the raw master via engagement-based Quick Cut (visual-engagement highlight, not frame-accurate ti |
| podcast_master_reframed_1080p.mp4 | video | Full-length episode reframed/resized to a clean 1920x1080 YouTube frame, SAME length as source (no trim, no format convert). |
| episode_content_summary.txt | data | Scene/transcript summary of the episode to seed YouTube chapter markers + description copy. |
| brand_logo_clean.png | image | Client logo lifted off its busy background to a clean transparent PNG, color-corrected and brand-tinted. |
| brand_logo_vector.svg | vector | Infinitely-scalable vectorized SVG of the cleaned logo for the end screen — the 'vector format' graphic-asset deliverable. |
| lower_third_plate.png | image | Broadcast lower-third name-plate strip: background knocked out, clean solid brand-colored bar, brand-tinted, cropped to a lower-third aspect; transparent PNG — the 'PNG/t |
| endscreen_texture.jpg | image | One licensed full-res stock background texture for the end-screen card, on-brand and subtle. |
| font_recommendation.txt | data | Recommended friendly display typeface(s) for the host-name lower-third text. |
| graphics_kit_board | data | Firefly board (deep-link) assembling the cleaned logo, vector logo, lower-third plate, and end-screen texture for client review. |

**Layer-3 verifier checks** — expert-authored (17 checks, 1 dealbreaker). *Tags: auto/expert · weight · feeds-K.*
| check | tags | exact pass condition |
|---|---|---|
| Cleaned voice deliverable podcast_voice_cleaned.wav is present and in WAV format | auto · mandatory · K1 | A file named podcast_voice_cleaned.wav exists and is a valid WAV audio container |
| The cleaned voice track is denoise/de-hiss only (voice-only), with the two hosts clear and balanced, and no music or loudness-mastering applied | expert · mandatory · K4 | Room hiss/HVAC hum and the broadband noise floor present in host_voice_scratch_track.wav are audibly reduced and the two hosts sound clear and level-balanced, while no music bed, no creative sound design, and no loudness-mastering coloration has been introduced (per the brief's 'denoise/de-hiss only - no elaborate sound design') |
| Cold-open sizzle reel podcast_coldopen_sizzle_1080p.mp4 exists at 1920x1080 and is roughly 20 seconds long | auto · mandatory · K1 | podcast_coldopen_sizzle_1080p.mp4 is an MP4 video with frame size exactly 1920x1080 and duration approximately 20s (well shorter than the full source master) |
| The sizzle reel was produced as an engagement-based highlight cut from the raw master, not a frame-accurate timestamp trim | expert · quality · K6 | podcast_coldopen_sizzle_1080p.mp4 reads as an AI visual-engagement highlight/sizzle drawn from the raw footage (selecting lively moments), consistent with video_create_quick_cut, rather than a manually timestamp-trimmed segment |
| Full-length reframed master podcast_master_reframed_1080p.mp4 is 1920x1080 and the SAME length as the source raw master (no trim, no format convert) | auto · mandatory · K1 | podcast_master_reframed_1080p.mp4 is an MP4 with frame size exactly 1920x1080 whose duration equals podcast_raw_master_1080p.mp4's duration (within a frame), i.e. not shortened or re-trimmed |
| Episode content summary episode_content_summary.txt is delivered as text seeding chapter markers and description copy | auto · mandatory · K1 | A non-empty text file named episode_content_summary.txt exists containing a scene/transcript summary of the episode suitable for YouTube chapter markers + description |
| Cleaned logo deliverable brand_logo_clean.png is a transparent PNG with the busy background removed | auto · mandatory · K1 | brand_logo_clean.png is a PNG with an alpha channel where the original cluttered desk/coffee-mug/cables/plants background is fully transparent and only the circular logo mark remains |
| The cleaned logo preserves the real client mark 'THE LONG WAY ROUND' with its campervan icon and mustard-and-teal brand colors, not a regenerated/altered logo | expert · **dealbreaker** · K2 | brand_logo_clean.png shows the same 'THE LONG WAY ROUND' wordmark, retro campervan icon, and bold friendly rounded sans-serif as brand_logo_lockup.png, color-corrected/brand-tinted to the mustard-and-teal scheme, with the mark itself not redrawn, distorted, or re-typeset |
| Vector logo deliverable brand_logo_vector.svg is a valid scalable SVG vectorized from the cleaned logo | auto · mandatory · K1 | brand_logo_vector.svg exists and is a valid SVG file containing vector path/shape geometry (not merely an embedded raster), corresponding to the cleaned brand_logo_clean.png |
| Lower-third name-plate lower_third_plate.png is a transparent PNG cropped to a broadcast lower-third strip aspect | auto · mandatory · K1 | lower_third_plate.png is a PNG with transparency, cropped/resized to a wide broadcast lower-third strip aspect ratio (significantly wider than tall), not a full-frame square or 16:9 image |
| The lower-third plate shows a clean solid brand-colored bar (not the original kraft-paper/linen texture), tinted to the mustard/teal brand palette | expert · mandatory · K3 | lower_third_plate.png presents a clean solid brand-colored bar where the supplied kraft-paper/linen texture from lower_third_texture_plate.jpg was knocked out and replaced with a flat fill, monochromatically tinted to the mustard/teal brand palette rather than retaining the raw paper-fiber texture |
| End-screen texture endscreen_texture.jpg is one licensed full-resolution stock background image | auto · mandatory · K1 | endscreen_texture.jpg exists as a single full-resolution JPG sourced via stock licensing (a licensed Adobe Stock asset), not an upscaled or generated image |
| The end-screen stock texture is subtle and on-brand, themed by the episode summary | expert · quality · K4 | endscreen_texture.jpg reads as a subtle, on-brand background texture appropriate for the end-screen card and thematically consistent with the episode_content_summary keywords, not a loud or off-brand image |
| Font recommendation font_recommendation.txt names at least one friendly casual display typeface for the host-name lower-third text | auto · mandatory · K1 | A non-empty text file named font_recommendation.txt exists and names one or more specific friendly/casual display fonts intended for the host-name text on the lower-third plate |
| A Firefly graphics-kit board deep-link is delivered assembling the four kit assets for client review | auto · mandatory · K1 | graphics_kit_board is delivered as a Firefly board deep-link whose contents include the cleaned logo (brand_logo_clean.png), vector logo (brand_logo_vector.svg), lower-third plate (lower_third_plate.png), and end-screen texture (endscreen_texture.jpg) |
| Graphic assets are delivered SEPARATELY in PNG-transparent / vector format (not composited into the video) | expert · mandatory · K1 | The custom graphic assets (brand_logo_clean.png, brand_logo_vector.svg, lower_third_plate.png, endscreen_texture.jpg) are delivered as standalone PNG-transparent / vector / image files exactly as the brief's 'delivered SEPARATELY in PNG/transparent or vector format' requires, and are NOT burned into or composited onto the reframed master or sizzle video |
| The hand-off honestly states the working files are the connector's packaged artifacts and flags frame-accurate pause/stumble trimming as the human-finishable step | expert · mandatory · K7 | The communication to the client plainly explains that the editing project file is supplied as the equivalent packaged hand-off (no Premiere/FCP/Resolve project export exists in the connector), that the sizzle is engagement-based rather than timestamp trimming, and that frame-accurate removal of pauses/stumbles remains a human finishing step - with no claimed capability that was not performed |

