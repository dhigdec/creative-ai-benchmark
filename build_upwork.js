// Builds Upwork_Tasks.docx from tasks_upwork_live.js — a measured, browser-harvested sample.
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, ExternalHyperlink, InternalHyperlink,
  Bookmark, HeadingLevel, BorderStyle, PageBreak, PageNumber, Footer, Table, TableRow, TableCell,
  WidthType, ShadingType, VerticalAlign, LevelFormat
} = require("docx");

const INK = "16243F", ACCENT = "1A7A5E", ACCENT2 = "0F5C46", BAND = "E7F1EC", CARD = "F2F8F5",
      GREY = "6B7280", DARK = "23303F", LINE = "D9DEE8";
const TASKS = require("./tasks_upwork_live.js");
const slug = s => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");

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

// Cover
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 1500, after: 0 }, shading: { type: ShadingType.CLEAR, fill: INK },
  children: [new TextRun({ text: "  Upwork — Adobe Task Sample  ", bold: true, size: 50, font: "Calibri", color: "FFFFFF" })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 160, after: 40 }, children: [new TextRun({ text: "Currently-open Upwork postings that require Adobe tools", size: 26, color: DARK })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 30 }, children: [new TextRun({ text: "Harvested live, read-only — no OCR", size: 22, color: ACCENT, italics: true })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 320 }, children: [new TextRun({ text: "Captured 5 June 2026", size: 20, color: GREY })] }));
[[TASKS.length + " full task briefs", "each a real, current Upwork posting with its complete brief"],
 [verticals.length + " industries", "video, branding, real estate, finance, publishing, fashion & more"],
 ["Method", "read-only browser page-text extraction (DOM), not OCR"],
 ["Note", "a measured sample — Upwork caps search depth & rate-limits bots; the official API is the way to pull everything"]
].forEach(g => children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 70 }, children: [new TextRun({ text: g[0] + "   —   ", bold: true, size: 23, color: ACCENT }), new TextRun({ text: g[1], size: 20, color: DARK })] })));
children.push(new Paragraph({ children: [new PageBreak()] }));

// About
children.push(banner("About this document", "about"));
["What this is: a measured sample of currently-open Upwork job postings that genuinely require Adobe Creative Cloud work. Each entry is the actual brief plus the specific Adobe app(s) the task needs.",
 "How it was captured: read-only, via the browser's rendered page text (DOM) — NOT screenshots or OCR, so the text is exact. Captured 5 June 2026, gently, stopping well short of Upwork's anti-bot limits.",
 "Why it's a sample, not everything: Upwork caps how deep a search can be read and rate-limits automation, and per-job permalinks require login. So each link below opens the Upwork search the task was found in. To pull the full Upwork inventory compliantly, use the official Upwork API (approval pending).",
 "Filtering: off-topic results (SEO sales roles, pure data-entry VA gigs that only mention 'basic photo editing') were excluded — only genuine Adobe design/video/photo tasks are kept."
].forEach(t => children.push(new Paragraph({ numbering: { reference: "b", level: 0 }, spacing: { after: 100 }, children: [new TextRun({ text: t, size: 21 })] })));

// Snapshot
children.push(banner("Snapshot"));
const rows = [new TableRow({ tableHeader: true, children: [cell("Industry", 7400, INK, { bold: true, color: "FFFFFF" }), cell("Tasks", 1960, INK, { bold: true, color: "FFFFFF", align: AlignmentType.CENTER })] })];
verticals.forEach((v, i) => rows.push(new TableRow({ children: [cell(v, 7400, i % 2 ? CARD : "FFFFFF", { color: INK }), cell(String(byVert[v].length), 1960, i % 2 ? CARD : "FFFFFF", { bold: true, color: ACCENT2, align: AlignmentType.CENTER })] })));
children.push(new Table({ width: { size: 9360, type: WidthType.DXA }, columnWidths: [7400, 1960], rows }));
children.push(new Paragraph({ spacing: { before: 160, after: 40 }, children: [new TextRun({ text: "Adobe tool coverage:  ", bold: true, size: 20, color: ACCENT2 }), new TextRun({ text: topTools, size: 19, color: DARK })] }));

// Tasks by vertical
function renderTask(t, n) {
  children.push(new Paragraph({ spacing: { before: 200, after: 40 }, keepNext: true, shading: { type: ShadingType.CLEAR, fill: CARD }, border: { left: { style: BorderStyle.SINGLE, size: 20, color: ACCENT, space: 8 } },
    children: [new TextRun({ text: n + ".  " + t.title, bold: true, size: 24, font: "Calibri", color: INK })] }));
  children.push(new Paragraph({ spacing: { after: 50 }, keepNext: true, children: [new TextRun({ text: [t.platform, t.budget, t.posted, t.location].filter(Boolean).join("    ·    "), italics: true, size: 19, color: GREY })] }));
  children.push(new Paragraph({ spacing: { after: 70 }, keepNext: true, children: [new TextRun({ text: "Adobe tools:  ", bold: true, size: 20, color: ACCENT2 }), new TextRun({ text: (t.tools || []).join("  ·  "), bold: true, size: 20, color: ACCENT2 }), new TextRun({ text: t.toolsWhy ? "   —   " + t.toolsWhy : "", size: 19, color: DARK })] }));
  children.push(new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: t.fulldesc, size: 21, color: DARK })] }));
  children.push(new Paragraph({ spacing: { after: 220 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 8 } }, children: [new ExternalHyperlink({ link: t.url, children: [new TextRun({ text: "Open the Upwork search this task was found in", style: "Hyperlink", size: 19 })] })] }));
}
verticals.forEach((v, i) => {
  children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(banner(v, slug(v)));
  children.push(new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: byVert[v].length + (byVert[v].length === 1 ? " task" : " tasks"), italics: true, size: 19, color: GREY })] }));
  byVert[v].forEach((t, k) => renderTask(t, k + 1));
});

const footerPara = new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Upwork Adobe Task Sample   ·   captured 5 Jun 2026   ·   page ", size: 16, color: "AAAAAA" }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "AAAAAA" })] });
const doc = new Document({
  styles: { default: { document: { run: { font: "Calibri", size: 22 }, paragraph: { spacing: { line: 288 } } } },
    paragraphStyles: [{ id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 30, bold: true, font: "Calibri", color: INK }, paragraph: { spacing: { before: 220, after: 130 }, outlineLevel: 0 } }] },
  numbering: { config: [{ reference: "b", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 560, hanging: 280 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } }, footers: { default: new Footer({ children: [footerPara] }) }, children }]
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/Upwork_Tasks.docx", b); console.log("WROTE Upwork_Tasks.docx —", TASKS.length, "tasks across", verticals.length, "industries"); });
