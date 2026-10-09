---
name: project_studiobench_gatsby_v6
description: My feedback-applied build is Gatsby V7 (docs/gatsby-v7, live, commit 4fe816a, 2026-09-28); docs/gatsby-v6 is a DIFFERENT team's build (d5acf70) and must not be touched
metadata:
  type: project
---

docs/gatsby-v7 = v5 copy + all 100 feedback patches (briefs pinned, palette mandatory/optional + distribution/opacity, "no gold"/type rules per deliverable, asset checks name exact file + deliverable). Live: https://dhigdec.github.io/creative-ai-benchmark/gatsby-v7/ . 44,532 checks (auto 11,217 unchanged, human 33,315). index.html 84 MB (GitHub >50 MB warning; limit 100 MB).

docs/gatsby-v6 was committed Sep 27 by someone else ("task-contract review", tools/gatsby_v6/task-decisions.json). I had accidentally overwritten it locally, restored via git checkout. Its PHOTO-04 pin (High Summer 680/740/780) differs from V7's (lowest 2027 rate, season named).

Open in V7: LAYOUT-24–35 + all MOTION not consolidated; no final audit; PHOTO-02/07, MOTION-15–19 never independently reviewed; PHOTO-02 A009 vs H004 price conflict; 68 MOTION register-only stills kept.

Ops assessment set (after Sep 28 ops review + my 6-lens vetting): PHOTO-04, 06, 08, 10, 19, 20, 24, 26, 28 + LAYOUT-15. Dropped: PHOTO-12 (A4 overload), 22 (room cards bound to detail shots), 25 (unverifiable film claim), 27. Vetted and REJECTED as replacements: PHOTO-03 (house no. 27), 05 (two different buildings), 14, 15, 18 (different couples), 21, 23, VECTOR-02 (two different marks). Most PHOTO tasks have source-asset authoring flaws not in defect_engineered; vet with those lenses before picking. Fixes live in commit 7a8a137. Excluded for IP marks: PHOTO-01, 11, 16, 29, 30.

Gotchas: repo .gitignore blocks *.png/*.jpg/*.pdf/*.zip, so git add -f media (289 files) or the page 404s. JSON files are indent=1, ensure_ascii False; re-dump with that or the diff explodes.

**How to apply:** never write into docs/gatsby-v6; next version goes to a new folder. See [[project_studiobench_gatsby_v5]], [[project_adobe_ip_sweep]].
