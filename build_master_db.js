// Builds Adobe_Upwork_Master.docx from db_tasks.json (exported from the pipeline DB).
// Polished, navigable: cover, about, snapshot table, clickable TOC, tasks grouped by industry.
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, ExternalHyperlink, InternalHyperlink,
  Bookmark, HeadingLevel, BorderStyle, PageBreak, PageNumber, Footer, Table, TableRow, TableCell,
  WidthType, ShadingType, VerticalAlign, LevelFormat, TableOfContents
} = require("docx");

const INK = "16243F", ACCENT = "1A7A5E", ACCENT2 = "0F5C46", BAND = "E7F1EC", CARD = "F2F8F5",
      GREY = "6B7280", DARK = "23303F", LINE = "D9DEE8";
const SRC = process.argv[2] || "./db_tasks.json";
const OUT = process.argv[3] || "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/Adobe_Upwork_Master.docx";
const TITLE = process.argv[4] || "Upwork — Adobe Task Library";
let TASKS = JSON.parse(fs.readFileSync(SRC, "utf8"));
const slug = s => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");

// group by vertical, largest first
const byVert = {};
TASKS.forEach(t => (byVert[t.vertical] = byVert[t.vertical] || []).push(t));
const verticals = Object.keys(byVert).sort((a, b) => byVert[b].length - byVert[a].length);
const toolCount = {};
TASKS.forEach(t => (t.tools || []).forEach(x => toolCount[x] = (toolCount[x] || 0) + 1));
const topTools = Object.entries(toolCount).sort((a, b) => b[1] - a[1]).map(([k, v]) => k + " (" + v + ")").join("   ·   ");

const children = [];
function banner(text, id) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 220, after: 140 },
    shading: { type: ShadingType.CLEAR, fill: BAND },
    border: { left: { style: BorderStyle.SINGLE, size: 26, color: ACCENT, space: 8 }, bottom: { style: BorderStyle.SINGLE, size: 6, color: INK, space: 4 } },
    children: [id ? new Bookmark({ id, children: [new TextRun(text)] }) : new TextRun(text)] });
}
const bd = { style: BorderStyle.SINGLE, size: 2, color: LINE }, borders = { top: bd, bottom: bd, left: bd, right: bd };
function cell(text, w, fill, o) { o = o || {}; return new TableCell({ width: { size: w, type: WidthType.DXA }, borders, shading: { type: ShadingType.CLEAR, fill }, margins: { top: 50, bottom: 50, left: 120, right: 120 }, verticalAlign: VerticalAlign.CENTER, children: [new Paragraph({ alignment: o.align || AlignmentType.LEFT, children: [new TextRun({ text, bold: !!o.bold, color: o.color || DARK, size: o.size || 20 })] })] }); }

// ---- Cover ----
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 1400, after: 0 }, shading: { type: ShadingType.CLEAR, fill: INK },
  children: [new TextRun({ text: "  " + TITLE + "  ", bold: true, size: 50, font: "Calibri", color: "FFFFFF" })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 160, after: 40 }, children: [new TextRun({ text: "Real, currently-open Upwork postings that require Adobe Creative Cloud work", size: 26, color: DARK })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 30 }, children: [new TextRun({ text: "Each entry is the client's actual brief, with the Adobe app(s) the work needs", size: 22, color: ACCENT, italics: true })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 320 }, children: [new TextRun({ text: "Compiled 8 June 2026 · read-only DOM harvest, no OCR, no fabrication", size: 20, color: GREY })] }));
[[TASKS.length.toLocaleString() + " task briefs", "every one a real, current Upwork posting with its full description"],
 [verticals.length + " industries", "branding, real estate, health, food, tech, video, fashion, publishing & more"],
 ["Adobe tools", topTools.split("   ·   ").slice(0, 6).join("   ·   ")],
 ["Method", "polite, rate-limited browser harvest of public search results — links open the live Upwork search each task was found in"]
].forEach(g => children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 70 }, children: [new TextRun({ text: g[0] + "   —   ", bold: true, size: 23, color: ACCENT }), new TextRun({ text: g[1], size: 20, color: DARK })] })));
children.push(new Paragraph({ children: [new PageBreak()] }));

// ---- About ----
children.push(banner("About this document", "about"));
["What this is: a large, deduplicated library of currently-open Upwork job postings that genuinely require Adobe Creative Cloud work (Photoshop, Illustrator, InDesign, After Effects, Premiere Pro, Lightroom, XD). Each entry is the actual client brief plus the specific Adobe app(s) the task calls for.",
 "How it was captured: read-only, from the browser's rendered search results (DOM) — not screenshots or OCR, so the text is exact. Collected gently and rate-limited, well within Upwork's anti-bot limits, across many search terms and result pages.",
 "Deduplication: genuine re-sightings of the same posting are removed (by title + description). Two different clients posting the same title (e.g. 'Logo Design') with different briefs are both kept — they are distinct tasks.",
 "Links: per-job permalinks require login, so each task links to the live Upwork search it was found in. To pull the entire Upwork inventory continuously and compliantly, the project also includes an automated pipeline and supports the official Upwork API.",
 "Filtering: off-topic results (pure data-entry/VA gigs, SEO/lead-gen sales roles) were excluded — only genuine Adobe design, video and photo tasks are kept."
].forEach(t => children.push(new Paragraph({ numbering: { reference: "b", level: 0 }, spacing: { after: 100 }, children: [new TextRun({ text: t, size: 21 })] })));

// ---- Snapshot ----
children.push(banner("Snapshot — tasks by industry"));
const rows = [new TableRow({ tableHeader: true, children: [cell("Industry", 7400, INK, { bold: true, color: "FFFFFF" }), cell("Tasks", 1960, INK, { bold: true, color: "FFFFFF", align: AlignmentType.CENTER })] })];
verticals.forEach((v, i) => rows.push(new TableRow({ children: [
  new TableCell({ width: { size: 7400, type: WidthType.DXA }, borders, shading: { type: ShadingType.CLEAR, fill: i % 2 ? CARD : "FFFFFF" }, margins: { top: 50, bottom: 50, left: 120, right: 120 }, verticalAlign: VerticalAlign.CENTER, children: [new Paragraph({ children: [new InternalHyperlink({ anchor: slug(v), children: [new TextRun({ text: v, color: INK, size: 20 })] })] })] }),
  cell(String(byVert[v].length), 1960, i % 2 ? CARD : "FFFFFF", { bold: true, color: ACCENT2, align: AlignmentType.CENTER })] })));
rows.push(new TableRow({ children: [cell("TOTAL", 7400, BAND, { bold: true, color: INK }), cell(String(TASKS.length), 1960, BAND, { bold: true, color: ACCENT2, align: AlignmentType.CENTER })] }));
children.push(new Table({ width: { size: 9360, type: WidthType.DXA }, columnWidths: [7400, 1960], rows }));
children.push(new Paragraph({ spacing: { before: 160, after: 40 }, children: [new TextRun({ text: "Adobe tool coverage:  ", bold: true, size: 20, color: ACCENT2 }), new TextRun({ text: topTools, size: 19, color: DARK })] }));

// ---- Task renderer ----
function renderTask(t, n) {
  children.push(new Paragraph({ spacing: { before: 200, after: 40 }, keepNext: true, shading: { type: ShadingType.CLEAR, fill: CARD }, border: { left: { style: BorderStyle.SINGLE, size: 20, color: ACCENT, space: 8 } },
    children: [new TextRun({ text: n + ".  " + t.title, bold: true, size: 24, font: "Calibri", color: INK })] }));
  const meta = [t.platform, t.budget, t.posted, t.location].filter(Boolean).join("    ·    ");
  if (meta) children.push(new Paragraph({ spacing: { after: 50 }, keepNext: true, children: [new TextRun({ text: meta, italics: true, size: 19, color: GREY })] }));
  if (t.tools && t.tools.length) children.push(new Paragraph({ spacing: { after: 70 }, keepNext: true, children: [new TextRun({ text: "Adobe tools:  ", bold: true, size: 20, color: ACCENT2 }), new TextRun({ text: t.tools.join("  ·  "), bold: true, size: 20, color: ACCENT2 })] }));
  if (t.fulldesc) children.push(new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: t.fulldesc, size: 21, color: DARK })] }));
  if (t.url) children.push(new Paragraph({ spacing: { after: 220 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 8 } }, children: [new ExternalHyperlink({ link: t.url, children: [new TextRun({ text: "Open the Upwork search this task was found in", style: "Hyperlink", size: 19 })] })] }));
  else children.push(new Paragraph({ spacing: { after: 220 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 8 } }, children: [new TextRun({ text: "", size: 2 })] }));
}
verticals.forEach((v) => {
  children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(banner(v, slug(v)));
  children.push(new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: byVert[v].length + (byVert[v].length === 1 ? " task" : " tasks"), italics: true, size: 19, color: GREY })] }));
  byVert[v].forEach((t, k) => renderTask(t, k + 1));
});

const footerPara = new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Adobe Upwork Task Library   ·   compiled 8 Jun 2026   ·   page ", size: 16, color: "AAAAAA" }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "AAAAAA" })] });
const doc = new Document({
  styles: { default: { document: { run: { font: "Calibri", size: 22 }, paragraph: { spacing: { line: 288 } } } },
    paragraphStyles: [{ id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 30, bold: true, font: "Calibri", color: INK }, paragraph: { spacing: { before: 220, after: 130 }, outlineLevel: 0 } }] },
  numbering: { config: [{ reference: "b", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 560, hanging: 280 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } }, footers: { default: new Footer({ children: [footerPara] }) }, children }]
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log("WROTE", OUT, "—", TASKS.length, "tasks across", verticals.length, "industries"); });
