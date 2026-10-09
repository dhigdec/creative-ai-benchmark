export const meta = {
  name: 'reauthor-merge-pdfs-2',
  description: 'Re-author the remaining 16 tasks\' stub merge/press PDFs as real press-PDF HTML (real fields, placed photo, structural trap, trim no bleed)',
  phases: [{ title: 'Author PDF HTML' }],
}
const BASE = '/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads'
const IDS = args
const SCHEMA = {
  type: 'object',
  properties: {
    task_id: { type: 'string' },
    pdfs: { type: 'array', items: { type: 'object', properties: {
      pdf_filename: { type: 'string' }, html_written: { type: 'boolean' },
      placed_image_file: { type: 'string' }, trap_baked: { type: 'string' }, real_fields_used: { type: 'boolean' } },
      required: ['pdf_filename', 'html_written', 'placed_image_file'] } },
    bleed_overclaim_in_spec: { type: 'boolean' },
    summary: { type: 'string' },
  },
  required: ['task_id', 'pdfs', 'bleed_overclaim_in_spec', 'summary'],
}
const results = await parallel(IDS.map((id) => () => agent(
  `Re-author the broken stub press/merge PDF(s) for task ${id} as REAL press-PDF HTML. Current PDFs are placeholder stubs ("The Vesper / [PIECE IMAGE]", no placed image, non-embedded fonts) that break convert_pdf_to_indd. Write faithful HTML; a central step Chrome-prints it.\n\n` +
  `READ:\n` +
  `- ${BASE}/input_assets_v3/${id}/asset_plan.json — every asset with "type":"pdf"; its "content" is the LAYOUT SPEC (trim mm, printed blocks, fonts, hex, the reverse-engineering TRAP).\n` +
  `- ${BASE}/complex_benchmark/adobe_only/specs_v3/${id}.json — brand_identity (palette hex, brand name) + emergent_checkpoints the PDF must trigger.\n` +
  `- The task's CSV in ${BASE}/input_assets_v3/${id}/assets/ (if any) — use a REAL representative record's actual values, never "The Vesper".\n` +
  `- List ${BASE}/input_assets_v3/${id}/assets/ and pick ONE existing photoreal image the card would show (product/piece/graphic/scene photo — NOT a logo/csv/txt/pdf). If the card genuinely shows NO photograph (a pure text sticker/tag), you may omit the image, but PREFER placing one where the layout has any picture area.\n\n` +
  `For EACH pdf asset, WRITE ${BASE}/input_assets_v3/${id}/pdfsrc/<pdf-basename>.html (create pdfsrc dir) as a self-contained single-record press card:\n` +
  `- <style>@page{size:<W>mm <H>mm;margin:0} html,body{margin:0}</style>, one card div exactly <W>mm×<H>mm at the spec's trim. NO bleed.\n` +
  `- Show ONE real record with the task's ACTUAL field values.\n` +
  `- PLACE the photo with <img src="file://${BASE}/input_assets_v3/${id}/assets/<file>" ...> sized to the picture area (MANDATORY where the layout has a picture area — convert_pdf_to_indd needs a real graphic frame).\n` +
  `- BAKE THE STRUCTURAL TRAP from the layout spec: single continuous text story where "one flow"; a decorative roundel/sunburst as inline <svg>/CSS (NOT an <img>) where specified; any stale/wrong baked value; media box = trim (no bleed).\n` +
  `- Real font stack (Georgia/Times or Arial/Helvetica), brand palette hex. Faithful printer's proof, realistic.\n\n` +
  `Report each pdf's exact filename, html_written, placed_image_file, and the trap baked. Set bleed_overclaim_in_spec=true if the spec claims 3mm bleed / press-ready-with-bleed from this PDF-derived template. Touch ONLY the HTML(s) you write.`,
  { agentType: 'general-purpose', phase: 'Author PDF HTML', label: `pdf:${id}`, schema: SCHEMA }
)))
const r = results.filter(Boolean)
return {
  tasks: r.length,
  htmls_written: r.reduce((s, x) => s + (x.pdfs || []).filter(p => p.html_written).length, 0),
  bleed_overclaim_tasks: r.filter(x => x.bleed_overclaim_in_spec).map(x => x.task_id),
  per_task: r.map(x => ({ id: x.task_id, n: (x.pdfs || []).length })),
}
