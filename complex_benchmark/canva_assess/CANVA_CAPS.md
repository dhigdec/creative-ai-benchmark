CANVA CONNECTOR (server 979c02d8) — what it CAN and CANNOT do:
CAN: generate-design (compose a design from a text brief), create-design-from-candidate, create-design-from-brand-template,
  perform-editing-operations (replace/insert/format TEXT and media in a fixed-page design; position/resize elements),
  autofill-design (DATA-MERGE: fill a brand template's fields from structured data rows -> many designs),
  resize-design (reflow to a new ratio), merge-designs, export-design (PNG/PDF/JPG/MP4/PPTX), upload-asset-from-url
  (bring an EXTERNAL image/video URL in as an asset), search-brand-templates, create/publish-brand-template.
  => Canva is a COMPOSITION / LAYOUT / TEMPLATE / DATA-MERGE / EXPORT engine. Strong at: social graphics, flyers,
     brochures, multi-page layouts, badges/cards via autofill, brand-template data-merge, multi-format export.
CANNOT (no tool exposed via the connector): pixel photo editing — NO background removal, NO masked tonal/exposure
  grading, NO HDR/bracket blend, NO duotone/Ben-Day halftone/glitch/grain FX, NO screen-print colour separations,
  NO raster->vector (vectorize), NO perspective/vertical straighten, NO depth/lens blur, NO audio cleanup, NO
  frame-accurate video edit/VO-sync (export MP4 yes, but not edit raw clips). It composes PREPPED elements; it does
  not process the pixels of a photo. (Canva's app has a bg-remover, but the MCP connector does NOT expose it.)
