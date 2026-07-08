# AO-85 — Ironclad parts catalog pre-press audit: merge-proof render, spec-row extraction + CSV cross-check, overset/missing-field findings report

**Ask:** Render our authored InDesign parts-catalog template against the master parts CSV into a proof, then audit it page by page — read back every printed spec row, cross-check it against the source data, and hand back a flagged-pages findings note (each defective page keyed to its issue) plus a findings report calling out overset/clipped part numbers, blank spec cells, and section-count mismatches before we send ~100 pages to print.

**Ready for agent:** True

## Assets handed to the designer/agent
- `catalog_logo.png` — gemini/gemini-3-pro-image 1024x1024, QC min 9
- `parts_catalog_template.indd` — data (proxy)
- `catalog_parts.csv` — data
- `brand_kit_note.txt` — data