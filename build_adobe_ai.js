// Builds an Adobe AI-Doable Tasks document from a JSON array of classified tasks.
// Each entry: task_type, title, source, date, url, vertical, mcp_workflow, inputs[], desc
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, ExternalHyperlink, InternalHyperlink,
  Bookmark, HeadingLevel, BorderStyle, PageBreak, PageNumber, Footer, Table, TableRow, TableCell,
  WidthType, ShadingType, VerticalAlign, LevelFormat,
} = require("docx");

const INK = "1A1333", ACCENT = "7A1FA2", ACCENT2 = "5B158C", BAND = "F1E9F7", CARD = "FAF6FD",
      GREY = "6B7280", DARK = "23303F", LINE = "E0D6EA",
      JDBG = "F7FAF4", JDBAR = "5B8C3E", WFBG = "EAF2FB", WFBAR = "1F6FB2", INBG = "FFF6E9", INBAR = "D08A1E";
const SRC = process.argv[2] || "./adobe_ai_sample.json";
const OUT = process.argv[3] || "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/Adobe_AI_Tasks_SAMPLE.docx";
const TITLE = process.argv[4] || "Adobe AI-Doable Tasks — SAMPLE";
const E = JSON.parse(fs.readFileSync(SRC, "utf8"));
const slug = s => (s || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
const PLAT = { upwork: "Upwork", freelancer: "Freelancer.com", peopleperhour: "PeoplePerHour" };

const byType = {};
E.forEach(e => (byType[e.task_type] = byType[e.task_type] || []).push(e));
const types = Object.keys(byType).sort((a, b) => byType[b].length - byType[a].length);

const children = [];
function banner(text, id) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 220, after: 140 },
    shading: { type: ShadingType.CLEAR, fill: BAND },
    border: { left: { style: BorderStyle.SINGLE, size: 26, color: ACCENT, space: 8 }, bottom: { style: BorderStyle.SINGLE, size: 6, color: INK, space: 4 } },
    children: [id ? new Bookmark({ id, children: [new TextRun(text)] }) : new TextRun(text)] });
}

// Cover
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 1400, after: 0 }, shading: { type: ShadingType.CLEAR, fill: INK },
  children: [new TextRun({ text: "  " + TITLE + "  ", bold: true, size: 46, font: "Calibri", color: "FFFFFF" })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 160, after: 40 }, children: [new TextRun({ text: "Real freelance design tasks that AI agents can execute through the Adobe Creative Cloud connectors", size: 24, color: DARK })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 30 }, children: [new TextRun({ text: "Each task is mapped to its Adobe MCP / Firefly / Express workflow and the input assets the agent must gather", size: 21, color: ACCENT, italics: true })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 320 }, children: [new TextRun({ text: "Compiled 9 June 2026", size: 20, color: GREY })] }));
[[E.length + " tasks", "each a real, currently-posted freelance brief"],
 [types.length + " task types", "logo, social, photo edit, presentation, flyer, t-shirt, cover art & more"],
 ["For every task", "the source listing (link + date), the Adobe tool workflow, and the input assets needed"],
 ["The input-assets column", "the exact files & details the agent collects from the client before starting"]
].forEach(g => children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 70 }, children: [new TextRun({ text: g[0] + "   —   ", bold: true, size: 22, color: ACCENT }), new TextRun({ text: g[1], size: 20, color: DARK })] })));
children.push(new Paragraph({ children: [new PageBreak()] }));

// How to read
children.push(banner("How to read each task"));
[ "Task type & title — what kind of design work it is, and the original posting title.",
  "Source / date / link — which freelance site it came from, when it was posted, and a link to the live posting.",
  "Adobe workflow — the actual chain of Adobe Creative Cloud tools (MCP / Firefly / Express / Document Services) an agent would run to produce the deliverable.",
  "Input assets the agent needs — the specific files and details the agent must collect from the client (brand name, logo file, photos, copy, colors, dimensions, etc.) before it can start. This is the practical 'what do I need from you' checklist.",
  "Original brief — the client's full task description, unedited."
].forEach(t => children.push(new Paragraph({ numbering: { reference: "b", level: 0 }, spacing: { after: 100 }, children: [new TextRun({ text: t, size: 21 })] })));

function box(label, labelColor, bg, bar, runs) {
  children.push(new Paragraph({ spacing: { before: 20, after: 8 }, keepNext: true, shading: { type: ShadingType.CLEAR, fill: bg }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: bar, space: 8 }, top: { style: BorderStyle.SINGLE, size: 2, color: bar, space: 3 } },
    children: [new TextRun({ text: label + "  ", bold: true, size: 17, color: labelColor }), ...runs] }));
}

function renderEntry(e, n) {
  // Header
  children.push(new Paragraph({ spacing: { before: 240, after: 30 }, keepNext: true, shading: { type: ShadingType.CLEAR, fill: CARD }, border: { left: { style: BorderStyle.SINGLE, size: 22, color: ACCENT, space: 8 } },
    children: [new TextRun({ text: n + ".  ", bold: true, size: 24, color: ACCENT2 }), new TextRun({ text: e.task_type, bold: true, size: 24, font: "Calibri", color: INK }), new TextRun({ text: "   —   " + e.title, bold: false, size: 22, color: DARK })] }));
  // Source line
  children.push(new Paragraph({ spacing: { after: 40 }, keepNext: true,
    children: [new TextRun({ text: [(PLAT[e.source] || e.source), e.date ? ("posted " + e.date) : "date n/a", e.vertical].filter(Boolean).join("    ·    ") + "    ", size: 18, color: GREY, italics: true }), e.url ? new ExternalHyperlink({ link: e.url, children: [new TextRun({ text: "[open posting]", style: "Hyperlink", size: 18 })] }) : new TextRun({ text: "" })] }));
  // Adobe workflow box
  box("ADOBE WORKFLOW", WFBAR, WFBG, WFBAR, [new TextRun({ text: e.mcp_workflow, size: 19, color: "1F4E79" })]);
  // Input assets box
  children.push(new Paragraph({ spacing: { before: 30, after: 6 }, keepNext: true, shading: { type: ShadingType.CLEAR, fill: INBG }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: INBAR, space: 8 }, top: { style: BorderStyle.SINGLE, size: 2, color: INBAR, space: 3 } },
    children: [new TextRun({ text: "INPUT ASSETS THE AGENT NEEDS", bold: true, size: 17, color: "9A6410" })] }));
  (e.inputs || []).forEach(inp => children.push(new Paragraph({ spacing: { after: 4 }, shading: { type: ShadingType.CLEAR, fill: INBG }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: INBAR, space: 8 } }, indent: { left: 200 },
    children: [new TextRun({ text: "•  ", bold: true, size: 19, color: INBAR }), new TextRun({ text: inp, size: 19, color: "5C4413" })] })));
  children.push(new Paragraph({ spacing: { after: 30 }, shading: { type: ShadingType.CLEAR, fill: INBG }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: INBAR, space: 8 }, bottom: { style: BorderStyle.SINGLE, size: 2, color: INBAR, space: 3 } }, children: [new TextRun({ text: "", size: 2 })] }));
  // Original brief box
  const jd = (e.desc || "").replace(/\s+/g, " ").trim();
  children.push(new Paragraph({ spacing: { before: 30, after: 8 }, keepNext: true, shading: { type: ShadingType.CLEAR, fill: JDBG }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: JDBAR, space: 8 }, top: { style: BorderStyle.SINGLE, size: 2, color: JDBAR, space: 3 } },
    children: [new TextRun({ text: "ORIGINAL CLIENT BRIEF", bold: true, size: 17, color: "3A6624" })] }));
  children.push(new Paragraph({ spacing: { after: 120 }, shading: { type: ShadingType.CLEAR, fill: JDBG }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: JDBAR, space: 8 }, bottom: { style: BorderStyle.SINGLE, size: 2, color: JDBAR, space: 3 } },
    children: [new TextRun({ text: jd.length > 1600 ? jd.slice(0, 1600) + " …" : jd, size: 19, color: "44503A" })] }));
  children.push(new Paragraph({ spacing: { after: 80 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 8 } }, children: [new TextRun({ text: "", size: 2 })] }));
}

let n = 0;
types.forEach((tp) => {
  children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(banner(tp + "  (" + byType[tp].length + ")", slug(tp)));
  byType[tp].forEach(e => renderEntry(e, ++n));
});

const footer = new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Adobe AI-Doable Tasks   ·   compiled 9 Jun 2026   ·   page ", size: 16, color: "AAAAAA" }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "AAAAAA" })] });
const doc = new Document({
  styles: { default: { document: { run: { font: "Calibri", size: 22 }, paragraph: { spacing: { line: 276 } } } },
    paragraphStyles: [{ id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 30, bold: true, font: "Calibri", color: INK }, paragraph: { spacing: { before: 220, after: 130 }, outlineLevel: 0 } }] },
  numbering: { config: [{ reference: "b", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 560, hanging: 280 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } }, footers: { default: new Footer({ children: [footer] }) }, children }]
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log("WROTE", OUT, "—", E.length, "tasks across", types.length, "types"); });
