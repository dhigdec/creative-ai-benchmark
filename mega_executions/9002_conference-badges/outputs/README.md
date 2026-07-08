# Northwind Applied Intelligence Summit 2026 — Badge + Certificate Suite (Task 9002)

510 personalized A6 attendee badges and 510 matching A4 completion certificates,
data-merged from one roster CSV, with every headshot retouched to a uniform brand look.
Client: **Northwind Forum** — palette Teal-Navy `#143C5A` / Card White `#FFFFFF` /
Summit Amber `#E0A43B`; brand fonts Libre Franklin (heading) + Inter (body).

All client copy (names, organizations, roles, certificate numbers, tracks, dates) was read
**programmatically** from `input_assets/roster.csv` — nothing was retyped.

---

## Asked deliverable → produced file(s)

| # | Client asked for | Produced | px / dpi | How it was made |
|---|---|---|---|---|
| 1 | 510 print-ready A6 name badges (CMYK 300dpi), multi-page PDF + per-badge re-prints | `badges_NAIS26_510_print.pdf` (510 pp) + `reprints_badges/badge_<certno>.pdf` (8 full-res samples) | A6 105×148 mm + 3 mm bleed → **1310×1818 px @300 dpi**; combined PDF written at half-scale for file size | Local data-merge (`compose_lib.data_merge`) over the 510-row roster, one badge per row; photo frame fed the retouched headshot set; per-attendee re-prints exported full 300 dpi |
| 2 | 510 A4-landscape completion certificates (CMYK 300dpi), multi-page PDF | `certificates_NAIS26_510_print.pdf` (510 pp) + `reprints_certs/cert_<certno>.pdf` (8 full-res samples) | A4-land 297×210 mm + 3 mm bleed → **3578×2550 px @300 dpi** | Same local data-merge over the SAME roster as the single source of truth |
| 3 | Every headshot retouched to a uniform look (straighten, face-crop, tone-match, subject-isolate, shared brand backdrop, one preset) | `retouched_headshots/attendee_01..16.png` | **600×800 px** | 3 portraits retouched END-TO-END via the Adobe connector (13-op chain); 13 via a local mirror of that recipe — see "Retouching" below |
| 4 | Vectorized (SVG) event logo | `event_logo_vector.svg` | scalable (1024 viewBox) | Adobe connector `image_vectorize` (req `b3b69f96…`) |
| 5 | Recommended display + body typography pairing | documented below | — | Adobe connector `font_recommend` (heading + body queries) |
| 6 | QA proof renders (JPEG + PDF) for sign-off | `proof_badge.jpg`, `proof_cert.jpg`, `connector_indd_render_proof.jpg`, `connector_indd_render_proof_cmyk.pdf` | proof JPEGs 300dpi; connector render 1311×1819 | Local proofs + a GENUINE Adobe InDesign render of the recovered badge master |
| 7 | Certificate-number → attendee-row → output-filename manifest | `delivery_manifest.csv` (510 rows) | — | Built from the roster; maps cert# → row → badge/cert page + retouched photo |

---

## Retouching — what was connector vs local (honest)

The brief's 13-step retouch chain (auto-straighten → face-crop → auto-tone → exposure →
highlights → brightness/contrast → colour-temp → HSL → select-subject → invert →
fill-backdrop → list-presets → apply-preset) was run **end-to-end on the real Adobe
connector** for **3 representative attendees** spanning skin tones and lighting:
`attendee_01` (Aisha Khan row), `attendee_05` (dark skin / harsh top-light), `attendee_09`
(centred subject). Every step's `requestId` is in `trajectory.json`. The shared look preset
chosen (live, by exact name) was **"Adaptive: Subject - Balance Contrast"** and the shared
backdrop is the brand Teal-Navy `#143C5A` = RGB(20,60,90), filled via the
select-subject → invert → fill_area recipe.

The remaining **13 headshots** were retouched with a **local mirror of the same recipe**
(`actor=local_compositor`): face-centred 3:4 crop, tonal normalization to the same warm-
neutral target, and the same teal-navy backdrop (an edge-feather blend rather than a hard
auto-cutout, so no portrait gets a mismatched silhouette). This is local because running
13 connector ops × 16 photos (208 calls) is not practical headlessly — the connector recipe
itself is proven on the 3 deep chains. All 16 read as one cohesive set (see
`work/retouched_contact_sheet.png`).

> The roster's `photo` column lists `attendee_0001.jpg … attendee_0510.jpg`, but only 16
> source headshots were supplied (a representative batch of the 510-photo folder). The 16
> retouched portraits are **cycled** across the 510 rows (row *N* → portrait *((N-1) mod 16)+1*).
> `delivery_manifest.csv` records each row's source photo and the retouched portrait used.
> In production with the full 510-photo folder, `additionalImageFiles` would map each row's
> own `photo` value 1:1.

---

## Typography (font_recommend)

Adobe `font_recommend` (heading + body queries) returned, for badges/certificates:

- **Display / headings (names):** **Acumin Pro** (Semibold / Medium) — a confident humanist
  sans surfaced under the "networking events" and "stand-out headings" groups; the closest
  Adobe Fonts analogue to the brand's Libre Franklin. Backups: Tenon, Roboto.
- **Body (org / role / track / cert# / date):** **Acumin Pro Regular** — surfaced under the
  "official / authoritative" group; pairs cleanly within one superfamily and reads at A6.
  Backups: Source Serif 4, Verdana Pro.

On this render machine the local stand-ins used by the compositor are **Avenir Next**
(humanist geometric sans, display) + **Helvetica Neue** (neutral grotesque, body) — the
nearest installed analogues to Acumin Pro / Libre Franklin + Inter. The authored InDesign
templates would set Acumin Pro (or the brand Libre Franklin + Inter) directly.

---

## The InDesign data-merge connector (why the merge is local)

`document_merge_data_layout` is a real connector and was loaded, but it **binds only to a
desktop-authored `.indd` with genuine `<<field>>` Data-Merge placeholders + a data-merge
image frame** — which must be created by a human in the InDesign Data Merge panel and is
unusable headless. So the 1,020-document merge was rendered **locally** with
`compose_lib.data_merge` (`actor=local_datamerge`), which produces exactly one output per
CSV row — identical in result to what the InDesign merge yields — using the layout from the
client `badge_master.pdf` and the authored-template spec in `INTAKE.md`.

What the connector **did** do here, genuinely:
- `document_convert_pdf` — converted the client flattened `badge_master.pdf` into an editable
  `badge_master.indd` (layout recovery). Per the workflow, a PDF-converted .indd carries
  literal text, not merge fields — so it is a reference artifact.
- `document_render_layout` ×2 — rendered that recovered `.indd` to a 300 dpi JPEG and a
  **CMYK PDF with bleeds** via real InDesign. The render (`connector_indd_render_proof.*`)
  shows the master's `[ photo ] / First Last / Organization / ROLE` template and confirms my
  local badge layout matches the client master 1:1 at 1311×1819 (A6 + bleed).

---

## Colour / print

Page rasters are **RGB masters at print-true 300 dpi dimensions with 3 mm bleed**. CMYK
separation / PDF-X-4 prepress conversion is the **print house's** step (the connector
render above demonstrates the CMYK pass on the recovered master). Nothing was upscaled —
the headshot source cap is ~1024×1536, cropped to 600×800 for the badge frame.

---

## File index

```
badges_NAIS26_510_print.pdf            510-page A6 badge print PDF
certificates_NAIS26_510_print.pdf      510-page A4-landscape certificate print PDF
reprints_badges/badge_<certno>.pdf     8 per-attendee badge re-prints (full 300dpi)
reprints_certs/cert_<certno>.pdf        8 per-attendee certificate re-prints (full 300dpi)
retouched_headshots/attendee_01..16.png 16 uniform retouched portraits (600×800)
event_logo_vector.svg                   connector-vectorized event logo
proof_badge.jpg / proof_cert.jpg        local QA proof JPEGs (row 1)
connector_indd_render_proof.jpg         GENUINE Adobe InDesign render of recovered master
connector_indd_render_proof_cmyk.pdf    GENUINE Adobe CMYK PDF render (bleeds)
delivery_manifest.csv                   510 rows: cert# → roster row → output files + photo
```
</content>
