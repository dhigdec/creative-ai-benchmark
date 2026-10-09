---
name: project-adobe-ip-sweep
description: "StudioBench v3.1 IP-leak sweep (2026-09-21) — 77 leaks found; whole-frame regeneration destroys engineered defects, masked inpaint is the only viable fix"
metadata: 
  node_type: memory
  type: project
  originSessionId: aa9e6dfc-7579-493e-a3a8-45be309ed406
  modified: 2026-09-21T22:29:18.103Z
---

Sweep of all 100 v3.1 tasks on 2026-09-21 (1,405 images + 229 sampled video frames).

**Found:** 67 image leaks in 64 images across 27 tasks; 10 video leaks in 9 of 46 clips
(MOTION-03/08/15/19); 4 brand-integrity defects. Real marks include Nike, adidas, Under Armour,
Gymshark, Rogue Fitness, SBD, Volkswagen, Ford, LG, Verizon, Apple, Microsoft Windows/IE,
Quechua, Matrixyl(R), Pokemon, Yu-Gi-Oh!, Magic: The Gathering, Topps, Upper Deck, plus named
real athletes. Worst single asset: PHOTO-16 `slabvault_results_reference.png`.

**The inventory is a floor, not a total.** Agents incidentally found unswept marks in the
ORIGINALS: Boar's Head on LAYOUT-02 counter_shot_11, Nike + The North Face on LAYOUT-10
waterman_row_04, Nike on LAYOUT-16 athlete_portrait_04, Under Armour on olneyville_green_02.
A dedicated re-scan for undeclared apparel logos and background signage is still owed.

**Hard-won lesson: never fix these by regenerating the frame.** Both `images.generate` and
`images.edit` WITHOUT a mask re-synthesise the whole image (measured SSIM 0.13-0.50, edge-NCC
0.05-0.47, 21-87% of pixels changed). Six independent verifier agents rejected 63 of 64 outputs.
Failure modes: engineered defects polished out (grades neutralised, an 8 degree lean straightened
to 1, a specular value-collision trap erased, a low-res proxy sharpened 2.7x), garbled text in
~9 of 11 per batch, subject/object identity swapped, a systematic warm-cast drift, and in two
cases NEW real IP introduced ("The Call of the Wild" appearing where the original had an
invented title).

**What works:** masked local inpaint compositing a native-resolution patch back through a
feathered mask onto the original raster. Validated on LAYOUT-21: all 5 marks painted with only
0.11% of pixels changed, so defects survive by construction. Tooling in the session scratchpad
`ipsweep/`: `inpaint_fix.py` (the good one), `refresh_asset_records.py`, `upload_accepted.py`.
Open issues: per-box-type instructions needed (a number plate needs "blank the characters, keep
the plate", not "continue the surface behind"); marks wider than the tile (full-width taskbars)
need tiling; safety refusals on tiles cropping people, and on any image containing real
likenesses (PHOTO-16 cannot use the edit endpoint at all).

**Published so far:** only LAYOUT-02 counter_shot_01/06/10 (regenerated, uploaded, sha-verified,
records refreshed). Defensible because their declared defects are standalone, but they ARE
re-synthesised frames. Everything else staged and unshipped; all 64 originals on disk untouched.

**Root cause:** only 406 of 1,522 generation prompts (27%) carry a no-brand guardrail and 46 of
100 tasks have none. Guardrails alone are insufficient: PHOTO-16 leaked WITH one, because
prompts that invite real-world content ("graded cards", "a photograph of a monitor") defeat it.

See [[feedback_verify_against_what_user_sees]] and [[project_studiobench_v3_corpus]].
