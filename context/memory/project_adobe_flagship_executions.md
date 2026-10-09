---
name: project-adobe-flagship-executions
description: "Flagship executions + presentation review site (5366/3437/3252/5388/1559) — connector runs, trajectories, rubrics HTML, built 2026-06-11"
metadata: 
  node_type: memory
  type: project
  originSessionId: 09201e3d-eb58-45af-860b-50daa011f950
---

# Adobe flagship EXECUTIONS + presentation site (2026-06-11)

Follows [[project-adobe-flagship-round3]] (the 5 generated input-asset packages). Here the 5 tasks
were RUN end-to-end through the Adobe connector + local composition, then wrapped in a scorable
review website. Composition decision resolved = **hybrid**: connector does element ops, local PIL
compositor assembles finished layouts (connector has no headless composition tool).

## Where it lives: `Adobe-Freelance-Leads/flagship_executions/`
- `<id>_<slug>/` per task: `input_assets/` (client files), `work/` (intermediates), `steps/`
  (numbered snapshot trail), `outputs/` (deliverables), `TASK.md` (work order), `PLAN.md` (op plan),
  `compose_<id>.py` (parametric layout script = the "editable source"), `trajectory.json` (audit),
  `rubrics.json` (expert scoring items), `outputs/README.md` (asked→produced map + honest limits).
- `lib/compose_lib.py` (print typography lib: macOS fonts Hoefler/Baskerville/Snell/Futura/Didot/
  AvenirNext/HelveticaNeue, leaders, crop marks, 300dpi units) + `lib/traj.py` (trajectory logger:
  `init|add --snap|finish`).
- `EXECUTION_CONTRACT.md` (binding protocol: Adobe upload/chain/download, trajectory rules, honest
  actor labels), `build_presentation.py` (assembles presentation_data.json/.js + web/ thumbs),
  `Flagship_Review.html` (the deliverable site), `serve_review.js` (node static server, port 8801;
  python http.server is sandbox-blocked → use node). Preview config "flagship" in BOTH
  `.claude/launch.json` (project + session root).

## Results (all 5 PASS adversarial verify; 1559 needed+passed a fix round for a crest-cutout defect)
- 47 real connector ops (every one has a logged requestId), 250 trajectory step images, 40 output
  files. Per task: 5366 wedding 14 outputs/4 ops; 3437 Blausweta 3+SVG/9 ops; 3252 THC 3/15 ops;
  5388 TeenTalk 9/13 ops; 1559 George Inn 9+SVG/6 ops. Exact px asserted on all.
- Adobe protocol that works headlessly (egress on): adobe_mandatory_init → asset_initialize_file_upload
  {path:"flagship/<f>"} → dd|curl PUT each block href → asset_finalize_file_upload {transfer_document
  VERBATIM} → edit tool with presignedAssetUrl → chain outputUrl→next imageURI → curl -L download.
  image_remove_background sometimes drops white interior letterforms of logos (use original on white
  bg for placement); image_crop_and_resize 7:2 may pillarbox if subject spans full height (retry with
  onSubjectClipping:ignore).

## The presentation site (what the user asked for, delivered)
`Flagship_Review.html` (open via the "flagship" preview / node serve_review.js on 8801). Left sidebar
= 5 tasks with live progress bars + annotator name + Export-scores(JSON) + localStorage autosave.
Click a task → full page: at-a-glance (1-line ask, 1-line deliverables, source+listing URL, task
type) · verbatim brief (expandable) · Adobe workflow chain + executed-ops line · input-asset groups
(thumbnails, generator model + pipeline QC badge per asset) each with 2-3 scorable rubric items ·
output groups ("Fulfils:" mapping, exact px) each with 3-4 items · 6 task-level items · collapsible
trajectory gallery (every step: actor tag adobe/local/verify, action, note, requestId, before/after
snapshot). 185 rubric items total (96 likert5 / 60 yesno / 29 text), content-specific (cite real
strings: "The Clementine", "DANKE5", "CURRNT 6 letters no E"), each with guidance + answer-key.
Rubrics authored by agents that VIEWED every pixel; coverage 100% (every in/out file grouped),
browser-QA'd (scoring/autosave/lightbox/export all work, zero console errors).

## Known minor cosmetic polish NOT done (user redirected to HTML before the polish workflow ran)
- 5366 rose-cluster garnish on table signs/menu-back/program-cover is a square crop of
  floral_cluster_sq.png that still shows green LAWN bg (sticker look) — fix = derive transparent
  garnish from work/floral_arch_cutout.png. - 3437 back benefit grid uses numbered circles (4,5) for
  the shield/package rows (no supplied icons) — fix = draw simple navy shield + parcel glyphs.
Both disclosed in trajectories/READMEs; a `flagship-polish` workflow was authored to fix them if asked.

## Next ideas: wire judge to pre-score outputs alongside human rubrics; the cosmetic polish above.
