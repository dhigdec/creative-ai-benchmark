// Builds the Adobe Connector-Doable Tasks document.
// Each entry: category, task_type, title, source, date, url, vertical, mcp_workflow, inputs[], feasibility, note, desc
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, ExternalHyperlink,
  Bookmark, HeadingLevel, BorderStyle, PageBreak, PageNumber, Footer, Table, TableRow, TableCell,
  WidthType, ShadingType, VerticalAlign, LevelFormat,
} = require("docx");

const INK = "1A1333", ACCENT = "7A1FA2", ACCENT2 = "5B158C", BAND = "F1E9F7", CARD = "FAF6FD",
      GREY = "6B7280", DARK = "23303F", LINE = "E0D6EA",
      JDBG = "F7FAF4", JDBAR = "5B8C3E", WFBG = "EAF2FB", WFBAR = "1F6FB2", INBG = "FFF6E9", INBAR = "D08A1E",
      FULLBG = "E7F5EC", FULLBAR = "2E8B57", PARTBG = "FDF3E3", PARTBAR = "C9821E", LIMBG = "FBECEC", LIMBAR = "B3492E";
const SRC = process.argv[2] || "/tmp/adobe_doable_final.json";
const OUT = process.argv[3] || "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/Adobe_Connector_Doable_Tasks.docx";
const TITLE = process.argv[4] || "Adobe Connector-Doable Tasks";
const E = JSON.parse(fs.readFileSync(SRC, "utf8"));
const slug = s => (s || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
const PLAT = { upwork: "Upwork", freelancer: "Freelancer.com", peopleperhour: "PeoplePerHour" };

const byCat = {};
E.forEach(e => (byCat[e.category] = byCat[e.category] || []).push(e));
const cats = Object.keys(byCat).sort((a, b) => byCat[b].length - byCat[a].length);
const nFull = E.filter(e => e.feasibility === "full").length;
const nPart = E.length - nFull;

const children = [];
function banner(text, id) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 220, after: 140 },
    shading: { type: ShadingType.CLEAR, fill: BAND },
    border: { left: { style: BorderStyle.SINGLE, size: 26, color: ACCENT, space: 8 }, bottom: { style: BorderStyle.SINGLE, size: 6, color: INK, space: 4 } },
    children: [id ? new Bookmark({ id, children: [new TextRun(text)] }) : new TextRun(text)] });
}

// ---------- Cover ----------
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 1300, after: 0 }, shading: { type: ShadingType.CLEAR, fill: INK },
  children: [new TextRun({ text: "  " + TITLE + "  ", bold: true, size: 46, font: "Calibri", color: "FFFFFF" })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 160, after: 40 }, children: [new TextRun({ text: "Real, currently-posted freelance briefs an AI agent can execute through the Adobe Creative Cloud connector", size: 24, color: DARK })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 30 }, children: [new TextRun({ text: "Every task is verified against the connector's actual tool surface — no text-to-image generation is assumed", size: 21, color: ACCENT, italics: true })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 }, children: [new TextRun({ text: "Compiled 9 June 2026", size: 20, color: GREY })] }));
[[E.length + " connector-doable tasks", "filtered from 3,888 cleaned briefs; every one re-checked tool-by-tool"],
 [nFull + " fully doable  ·  " + nPart + " partial", "“partial” = the connector does a substantial chunk; a human finishes a pixel-level step"],
 [cats.length + " work categories", "background removal, photo retouch, vectorize, colour, resize, PDF, video"],
 ["For every task", "the source listing (link + date), the exact Adobe tool chain, and the input assets to collect"]
].forEach(g => children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 70 }, children: [new TextRun({ text: g[0] + "   —   ", bold: true, size: 22, color: ACCENT }), new TextRun({ text: g[1], size: 20, color: DARK })] })));
children.push(new Paragraph({ children: [new PageBreak()] }));

// ---------- What this list is / isn't ----------
children.push(banner("What this list is — and what it deliberately leaves out"));
[ ["Scope.", "These are the freelance tasks the Adobe Creative Cloud connector can actually perform: editing and transforming an asset the client already has, sourcing stock, vectorising, resizing, PDF work, and video cutting."],
  ["No generation.", "The connector has no text-to-image tool. Tasks whose real deliverable is original artwork created from nothing — logo design, illustration, a poster or t-shirt designed from scratch — were removed (277 of them), even when keyword-similar. They need the Firefly Services API, which is a separate path."],
  ["Fully doable (✓).", "The connector can produce the entire deliverable end-to-end: e.g. remove a background, vectorise a raster logo, resize a design for social, license a stock photo, convert a PDF."],
  ["Partial (◑).", "The connector does the heavy, repeatable part (tone, colour, crop, cut-out, batch grade) but a human finishes a step it can't do — clone/heal skin retouching, precise compositing, print pre-press. The task line says exactly what's left."],
].forEach(t => children.push(new Paragraph({ numbering: { reference: "b", level: 0 }, spacing: { after: 110 }, children: [new TextRun({ text: t[0] + "  ", bold: true, size: 21, color: INK }), new TextRun({ text: t[1], size: 21 })] })));

// ---------- Category summary table ----------
children.push(banner("Categories at a glance"));
function cell(txt, { w, bold, color, fill, align, size } = {}) {
  return new TableCell({ width: { size: w, type: WidthType.DXA }, shading: fill ? { type: ShadingType.CLEAR, fill } : undefined, verticalAlign: VerticalAlign.CENTER,
    margins: { top: 40, bottom: 40, left: 120, right: 120 },
    children: [new Paragraph({ alignment: align || AlignmentType.LEFT, children: [new TextRun({ text: txt, bold: !!bold, size: size || 19, color: color || DARK })] })] });
}
const rows = [new TableRow({ tableHeader: true, children: [
  cell("Category", { w: 5200, bold: true, color: "FFFFFF", fill: ACCENT }),
  cell("Tasks", { w: 1400, bold: true, color: "FFFFFF", fill: ACCENT, align: AlignmentType.CENTER }),
  cell("Fully doable", { w: 1700, bold: true, color: "FFFFFF", fill: ACCENT, align: AlignmentType.CENTER }),
  cell("Partial", { w: 1700, bold: true, color: "FFFFFF", fill: ACCENT, align: AlignmentType.CENTER }),
] })];
cats.forEach((c, i) => {
  const list = byCat[c], f = list.filter(x => x.feasibility === "full").length;
  rows.push(new TableRow({ children: [
    cell(c.replace(/\s+/g, " "), { w: 5200, bold: true, fill: i % 2 ? "FFFFFF" : CARD }),
    cell(String(list.length), { w: 1400, fill: i % 2 ? "FFFFFF" : CARD, align: AlignmentType.CENTER, bold: true, color: ACCENT2 }),
    cell(f ? "✓ " + f : "—", { w: 1700, fill: i % 2 ? "FFFFFF" : CARD, align: AlignmentType.CENTER, color: FULLBAR }),
    cell((list.length - f) ? "◑ " + (list.length - f) : "—", { w: 1700, fill: i % 2 ? "FFFFFF" : CARD, align: AlignmentType.CENTER, color: PARTBAR }),
  ] }));
});
rows.push(new TableRow({ children: [
  cell("TOTAL", { w: 5200, bold: true, fill: BAND }),
  cell(String(E.length), { w: 1400, bold: true, fill: BAND, align: AlignmentType.CENTER }),
  cell("✓ " + nFull, { w: 1700, bold: true, fill: BAND, align: AlignmentType.CENTER, color: FULLBAR }),
  cell("◑ " + nPart, { w: 1700, bold: true, fill: BAND, align: AlignmentType.CENTER, color: PARTBAR }),
] }));
children.push(new Table({ width: { size: 10000, type: WidthType.DXA }, rows,
  borders: { top: { style: BorderStyle.SINGLE, size: 2, color: LINE }, bottom: { style: BorderStyle.SINGLE, size: 2, color: LINE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE }, insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: LINE }, insideVertical: { style: BorderStyle.SINGLE, size: 2, color: "EEE6F4" } } }));

children.push(new Paragraph({ spacing: { before: 220, after: 0 }, children: [new TextRun({ text: "How to read each task", bold: true, size: 22, color: INK })] }));
[ "Header — the specific task, the original posting title, and a ✓ fully-doable or ◑ partial badge.",
  "Source / date / link — the freelance site, the post date, and a link to the live posting.",
  "Adobe workflow — the exact ordered chain of connector tools an agent runs to produce the deliverable.",
  "Input assets the agent needs — the specific files & details to collect from the client before starting.",
  "Connector limit (partial tasks only) — the one step the connector can't finish, stated plainly.",
  "Original brief — the client's full task description, unedited."
].forEach(t => children.push(new Paragraph({ numbering: { reference: "b", level: 0 }, spacing: { after: 90 }, children: [new TextRun({ text: t, size: 20 })] })));

// ---------- Entry rendering ----------
function renderEntry(e, n) {
  const full = e.feasibility === "full";
  const badge = full ? "  ✓ FULLY DOABLE  " : "  ◑ PARTIAL  ";
  children.push(new Paragraph({ spacing: { before: 240, after: 30 }, keepNext: true, shading: { type: ShadingType.CLEAR, fill: CARD }, border: { left: { style: BorderStyle.SINGLE, size: 22, color: ACCENT, space: 8 } },
    children: [
      new TextRun({ text: n + ".  ", bold: true, size: 24, color: ACCENT2 }),
      new TextRun({ text: e.task_type, bold: true, size: 23, font: "Calibri", color: INK }),
      new TextRun({ text: "    " + badge, bold: true, size: 16, color: "FFFFFF", shading: { type: ShadingType.CLEAR, fill: full ? FULLBAR : PARTBAR } }),
    ] }));
  children.push(new Paragraph({ spacing: { after: 6 }, keepNext: true, children: [new TextRun({ text: e.title, size: 21, color: DARK, italics: true })] }));
  children.push(new Paragraph({ spacing: { after: 40 }, keepNext: true,
    children: [new TextRun({ text: [(PLAT[e.source] || e.source), e.date ? ("posted " + e.date) : "date n/a", e.vertical].filter(Boolean).join("    ·    ") + "    ", size: 18, color: GREY, italics: true }), e.url ? new ExternalHyperlink({ link: e.url, children: [new TextRun({ text: "[open posting]", style: "Hyperlink", size: 18 })] }) : new TextRun({ text: "" })] }));
  // Workflow box
  children.push(new Paragraph({ spacing: { before: 20, after: 8 }, keepNext: true, shading: { type: ShadingType.CLEAR, fill: WFBG }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: WFBAR, space: 8 }, top: { style: BorderStyle.SINGLE, size: 2, color: WFBAR, space: 3 } },
    children: [new TextRun({ text: "ADOBE WORKFLOW  ", bold: true, size: 17, color: WFBAR }), new TextRun({ text: e.mcp_workflow, size: 19, color: "1F4E79" })] }));
  // Input assets box
  children.push(new Paragraph({ spacing: { before: 30, after: 6 }, keepNext: true, shading: { type: ShadingType.CLEAR, fill: INBG }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: INBAR, space: 8 }, top: { style: BorderStyle.SINGLE, size: 2, color: INBAR, space: 3 } },
    children: [new TextRun({ text: "INPUT ASSETS THE AGENT NEEDS", bold: true, size: 17, color: "9A6410" })] }));
  (e.inputs || []).forEach(inp => children.push(new Paragraph({ spacing: { after: 4 }, shading: { type: ShadingType.CLEAR, fill: INBG }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: INBAR, space: 8 } }, indent: { left: 200 },
    children: [new TextRun({ text: "•  ", bold: true, size: 19, color: INBAR }), new TextRun({ text: inp, size: 19, color: "5C4413" })] })));
  children.push(new Paragraph({ spacing: { after: e.feasibility === "partial" && e.note ? 4 : 30 }, shading: { type: ShadingType.CLEAR, fill: INBG }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: INBAR, space: 8 }, bottom: e.feasibility === "partial" && e.note ? undefined : { style: BorderStyle.SINGLE, size: 2, color: INBAR, space: 3 } }, children: [new TextRun({ text: "", size: 2 })] }));
  // Connector limit (partial only)
  if (e.feasibility === "partial" && e.note) {
    children.push(new Paragraph({ spacing: { before: 24, after: 30 }, keepNext: true, shading: { type: ShadingType.CLEAR, fill: LIMBG }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: LIMBAR, space: 8 }, top: { style: BorderStyle.SINGLE, size: 2, color: LIMBAR, space: 3 }, bottom: { style: BorderStyle.SINGLE, size: 2, color: LIMBAR, space: 3 } },
      children: [new TextRun({ text: "CONNECTOR LIMIT  ", bold: true, size: 17, color: LIMBAR }), new TextRun({ text: e.note, size: 19, color: "7A3422" })] }));
  }
  // Original brief
  const jd = (e.desc || "").replace(/\s+/g, " ").trim();
  children.push(new Paragraph({ spacing: { before: 30, after: 8 }, keepNext: true, shading: { type: ShadingType.CLEAR, fill: JDBG }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: JDBAR, space: 8 }, top: { style: BorderStyle.SINGLE, size: 2, color: JDBAR, space: 3 } },
    children: [new TextRun({ text: "ORIGINAL CLIENT BRIEF", bold: true, size: 17, color: "3A6624" })] }));
  children.push(new Paragraph({ spacing: { after: 120 }, shading: { type: ShadingType.CLEAR, fill: JDBG }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: JDBAR, space: 8 }, bottom: { style: BorderStyle.SINGLE, size: 2, color: JDBAR, space: 3 } },
    children: [new TextRun({ text: jd.length > 1500 ? jd.slice(0, 1500) + " …" : jd, size: 19, color: "44503A" })] }));
  children.push(new Paragraph({ spacing: { after: 80 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 8 } }, children: [new TextRun({ text: "", size: 2 })] }));
}

let n = 0;
cats.forEach((c) => {
  const list = byCat[c], f = list.filter(x => x.feasibility === "full").length;
  children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(banner(c + "   (" + list.length + "  —  ✓" + f + " full, ◑" + (list.length - f) + " partial)", slug(c)));
  list.forEach(e => renderEntry(e, ++n));
});

const footer = new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Adobe Connector-Doable Tasks   ·   compiled 9 Jun 2026   ·   page ", size: 16, color: "AAAAAA" }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "AAAAAA" })] });
const doc = new Document({
  styles: { default: { document: { run: { font: "Calibri", size: 22 }, paragraph: { spacing: { line: 276 } } } },
    paragraphStyles: [{ id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 28, bold: true, font: "Calibri", color: INK }, paragraph: { spacing: { before: 220, after: 130 }, outlineLevel: 0 } }] },
  numbering: { config: [{ reference: "b", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 560, hanging: 280 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } }, footers: { default: new Footer({ children: [footer] }) }, children }]
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log("WROTE", OUT, "—", E.length, "tasks across", cats.length, "categories (", nFull, "full /", nPart, "partial )"); });
