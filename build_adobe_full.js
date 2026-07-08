// Builds the full Adobe Connector-Doable Tasks document (3 feasibility tiers, family→category).
// Entry: family, category, task_type, title, source, date, url, vertical, mcp_workflow, inputs[], feasibility, note, desc
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, ExternalHyperlink,
  Bookmark, HeadingLevel, BorderStyle, PageBreak, PageNumber, Footer, Table, TableRow, TableCell,
  WidthType, ShadingType, VerticalAlign, LevelFormat,
} = require("docx");

const INK = "1A1333", ACCENT = "7A1FA2", ACCENT2 = "5B158C", BAND = "F1E9F7", CARD = "FAF6FD",
      GREY = "6B7280", DARK = "23303F", LINE = "E0D6EA", SUBBAND = "EFE4F6",
      JDBG = "F7FAF4", JDBAR = "5B8C3E", WFBG = "EAF2FB", WFBAR = "1F6FB2", INBG = "FFF6E9", INBAR = "D08A1E",
      LIMBG = "FBECEC", LIMBAR = "B3492E",
      FULLBAR = "2E8B57", TPLBAR = "7A4FB5", PARTBAR = "C9821E";
const TIER = {
  full:     { badge: "✓ FULLY DOABLE", bar: FULLBAR, label: "full" },
  template: { badge: "◆ TEMPLATE-BASED", bar: TPLBAR, label: "template" },
  partial:  { badge: "◑ PARTIAL", bar: PARTBAR, label: "partial" },
};
const SRC = process.argv[2] || "adobe_doable_full.json";
const OUT = process.argv[3] || "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/Adobe_Connector_Doable_Tasks.docx";
const TITLE = process.argv[4] || "Adobe Connector-Doable Tasks";
const E = JSON.parse(fs.readFileSync(SRC, "utf8"));
const slug = s => (s || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
const PLAT = { upwork: "Upwork", freelancer: "Freelancer.com", peopleperhour: "PeoplePerHour" };
const cnt = (arr, f) => arr.filter(f).length;

// family -> [categories], category -> [entries]
const FAM_ORDER = ["Express Template Design", "Photo & Image Editing", "Vector & Illustrator", "InDesign & Documents", "Video & Audio", "Stock"];
const byFam = {};
E.forEach(e => ((byFam[e.family] = byFam[e.family] || {})[e.category] = (byFam[e.family][e.category] || [])).push(e));
const fams = Object.keys(byFam).sort((a, b) => (FAM_ORDER.indexOf(a) + 99) % 100 - (FAM_ORDER.indexOf(b) + 99) % 100 || 0);
const famList = E.reduce((m, e) => (m[e.family] = (m[e.family] || 0) + 1, m), {});
const famSorted = Object.keys(byFam).sort((a, b) => famList[b] - famList[a]);
const nFull = cnt(E, e => e.feasibility === "full"), nTpl = cnt(E, e => e.feasibility === "template"), nPart = cnt(E, e => e.feasibility === "partial");

const children = [];
function banner(text, id, fill, bar, size) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 240, after: 140 },
    shading: { type: ShadingType.CLEAR, fill: fill || BAND },
    border: { left: { style: BorderStyle.SINGLE, size: 30, color: bar || ACCENT, space: 10 }, bottom: { style: BorderStyle.SINGLE, size: 6, color: INK, space: 4 } },
    children: [id ? new Bookmark({ id, children: [new TextRun({ text, size })] }) : new TextRun({ text, size })] });
}
function subbanner(text, id) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 200, after: 110 },
    shading: { type: ShadingType.CLEAR, fill: SUBBAND },
    border: { left: { style: BorderStyle.SINGLE, size: 22, color: ACCENT2, space: 8 } },
    children: [id ? new Bookmark({ id, children: [new TextRun(text)] }) : new TextRun(text)] });
}

// ---------- Cover ----------
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 1200, after: 0 }, shading: { type: ShadingType.CLEAR, fill: INK },
  children: [new TextRun({ text: "  " + TITLE + "  ", bold: true, size: 46, font: "Calibri", color: "FFFFFF" })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 160, after: 40 }, children: [new TextRun({ text: "Real, currently-posted freelance briefs an AI agent can execute through the Adobe Creative Cloud connector", size: 24, color: DARK })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 30 }, children: [new TextRun({ text: "Every task verified against the connector's real tool surface — Photoshop edits, Express templates, Illustrator vector, InDesign, PDF, Stock & Premiere", size: 21, color: ACCENT, italics: true })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 }, children: [new TextRun({ text: "Compiled 9 June 2026", size: 20, color: GREY })] }));
[[E.length + " connector-doable tasks", "filtered & verified from 3,888 cleaned freelance briefs"],
 [nFull + " full  ·  " + nTpl + " template  ·  " + nPart + " partial", "full = whole deliverable; template = via a pro Express/InDesign template + your content; partial = connector does the heavy part, a human finishes one step"],
 [fams.length + " families  ·  " + Object.keys(E.reduce((m,e)=>(m[e.category]=1,m),{})).length + " categories", "design, photo editing, vector, InDesign/PDF, video/audio, stock"],
 ["For every task", "the source listing (link + date), the exact Adobe tool chain, and the specific input assets to collect"]
].forEach(g => children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 70 }, children: [new TextRun({ text: g[0] + "   —   ", bold: true, size: 22, color: ACCENT }), new TextRun({ text: g[1], size: 19, color: DARK })] })));
children.push(new Paragraph({ children: [new PageBreak()] }));

// ---------- What this is ----------
children.push(banner("What this list is — and how to read the feasibility tier"));
[ ["Scope.", "These are the freelance tasks the Adobe Creative Cloud connector can actually perform — using its real tools: Photoshop-class image edits, Adobe Express templates (its built-in design-creation path), Illustrator vectorising, InDesign layout & data-merge, PDF services, Adobe Stock, and Premiere-class video/audio."],
  ["No from-scratch generation.", "The connector has no text-to-image tool. Tasks whose core deliverable is original artwork invented from nothing — a unique custom logo MARK/icon, a bespoke illustration, character or mascot art — were removed (≈1,000 of them), even when keyword-similar. They need a separate Firefly-API path."],
  ["✓ Full.", "The connector produces the entire deliverable end-to-end: background removal, photo colour/tone, vectorize a raster logo, resize/repurpose, source stock, convert/merge a PDF, export a supplied InDesign file."],
  ["◆ Template.", "Delivered via a professional Adobe Express (or InDesign data-merge) template with your content filled in — flyers, posters, social posts, business cards, invitations, banners, menus, certificates, ads, resumes, simple wordmark logos. Honest caveat: it's a professional template, not a bespoke-from-scratch custom design, and the connector's text-fill changes copy only (a human tweaks exact brand font/colour in Express)."],
  ["◑ Partial.", "The connector does the heavy, repeatable chunk (cut-out, tone, colour, batch grade, vectorize, sizzle-cut) but a human finishes one step — clone/heal retouch, complex multi-page layout, a hero illustration, print pre-press. Each task says exactly what's left."],
].forEach(t => children.push(new Paragraph({ numbering: { reference: "b", level: 0 }, spacing: { after: 100 }, children: [new TextRun({ text: t[0] + "  ", bold: true, size: 21, color: INK }), new TextRun({ text: t[1], size: 20 })] })));

// ---------- Family summary table ----------
children.push(banner("The doable set at a glance"));
function cell(txt, { w, bold, color, fill, align, size } = {}) {
  return new TableCell({ width: { size: w, type: WidthType.DXA }, shading: fill ? { type: ShadingType.CLEAR, fill } : undefined, verticalAlign: VerticalAlign.CENTER,
    margins: { top: 40, bottom: 40, left: 110, right: 110 },
    children: [new Paragraph({ alignment: align || AlignmentType.LEFT, children: [new TextRun({ text: txt, bold: !!bold, size: size || 19, color: color || DARK })] })] });
}
function tierTable(rowsData, firstHdr, firstW) {
  const W = [firstW, 1250, 1300, 1450, 1250];
  const head = new TableRow({ tableHeader: true, children: [
    cell(firstHdr, { w: W[0], bold: true, color: "FFFFFF", fill: ACCENT }),
    cell("Tasks", { w: W[1], bold: true, color: "FFFFFF", fill: ACCENT, align: AlignmentType.CENTER }),
    cell("✓ Full", { w: W[2], bold: true, color: "FFFFFF", fill: FULLBAR, align: AlignmentType.CENTER }),
    cell("◆ Template", { w: W[3], bold: true, color: "FFFFFF", fill: TPLBAR, align: AlignmentType.CENTER }),
    cell("◑ Partial", { w: W[4], bold: true, color: "FFFFFF", fill: PARTBAR, align: AlignmentType.CENTER }),
  ] });
  const body = rowsData.map((r, i) => new TableRow({ children: [
    cell(r.name, { w: W[0], bold: r.bold, fill: r.fill || (i % 2 ? "FFFFFF" : CARD), color: r.tot===undefined?DARK:INK }),
    cell(String(r.n), { w: W[1], bold: true, fill: r.fill || (i % 2 ? "FFFFFF" : CARD), align: AlignmentType.CENTER, color: ACCENT2 }),
    cell(r.f ? String(r.f) : "—", { w: W[2], fill: r.fill || (i % 2 ? "FFFFFF" : CARD), align: AlignmentType.CENTER, color: FULLBAR }),
    cell(r.t ? String(r.t) : "—", { w: W[3], fill: r.fill || (i % 2 ? "FFFFFF" : CARD), align: AlignmentType.CENTER, color: TPLBAR }),
    cell(r.p ? String(r.p) : "—", { w: W[4], fill: r.fill || (i % 2 ? "FFFFFF" : CARD), align: AlignmentType.CENTER, color: PARTBAR }),
  ] }));
  return new Table({ width: { size: 10000, type: WidthType.DXA }, rows: [head, ...body],
    borders: { top: { style: BorderStyle.SINGLE, size: 2, color: LINE }, bottom: { style: BorderStyle.SINGLE, size: 2, color: LINE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE }, insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: LINE }, insideVertical: { style: BorderStyle.SINGLE, size: 2, color: "EEE6F4" } } });
}
const famRows = famSorted.map(f => {
  const list = Object.values(byFam[f]).flat();
  return { name: f, n: list.length, f: cnt(list, x => x.feasibility==="full"), t: cnt(list, x => x.feasibility==="template"), p: cnt(list, x => x.feasibility==="partial") };
});
famRows.push({ name: "TOTAL", n: E.length, f: nFull, t: nTpl, p: nPart, bold: true, fill: BAND, tot: 1 });
children.push(tierTable(famRows, "Family", 4750));

// ---------- Category summary table ----------
children.push(new Paragraph({ spacing: { before: 220, after: 0 }, children: [new TextRun({ text: "By category", bold: true, size: 22, color: INK })] }));
const catRows = [];
famSorted.forEach(f => Object.keys(byFam[f]).sort((a, b) => byFam[f][b].length - byFam[f][a].length).forEach(c => {
  const list = byFam[f][c];
  catRows.push({ name: "   " + c, n: list.length, f: cnt(list, x => x.feasibility==="full"), t: cnt(list, x => x.feasibility==="template"), p: cnt(list, x => x.feasibility==="partial") });
}));
children.push(tierTable(catRows, "Category", 4750));
children.push(new Paragraph({ spacing: { before: 200, after: 60 }, children: [new TextRun({ text: "How to read each task:  ", bold: true, size: 20, color: INK }),
  new TextRun({ text: "header (task + posting title + tier badge) · source/date/link · ", size: 19, color: DARK }),
  new TextRun({ text: "🔵 Adobe workflow", size: 19, color: WFBAR, bold: true }), new TextRun({ text: " (the exact tool chain) · ", size: 19, color: DARK }),
  new TextRun({ text: "🟡 Input assets", size: 19, color: "9A6410", bold: true }), new TextRun({ text: " (what to collect from the client) · ", size: 19, color: DARK }),
  new TextRun({ text: "🔴 Connector limit", size: 19, color: LIMBAR, bold: true }), new TextRun({ text: " (template/partial only) · ", size: 19, color: DARK }),
  new TextRun({ text: "🟢 Original brief", size: 19, color: "3A6624", bold: true }), new TextRun({ text: ".", size: 19, color: DARK })] }));

// ---------- Entry rendering ----------
function renderEntry(e, n) {
  const tier = TIER[e.feasibility] || TIER.partial;
  children.push(new Paragraph({ spacing: { before: 230, after: 28 }, keepNext: true, shading: { type: ShadingType.CLEAR, fill: CARD }, border: { left: { style: BorderStyle.SINGLE, size: 22, color: ACCENT, space: 8 } },
    children: [
      new TextRun({ text: n + ".  ", bold: true, size: 23, color: ACCENT2 }),
      new TextRun({ text: e.task_type, bold: true, size: 22, font: "Calibri", color: INK }),
      new TextRun({ text: "    " + "  " + tier.badge + "  ", bold: true, size: 15, color: "FFFFFF", shading: { type: ShadingType.CLEAR, fill: tier.bar } }),
    ] }));
  children.push(new Paragraph({ spacing: { after: 6 }, keepNext: true, children: [new TextRun({ text: e.title, size: 21, color: DARK, italics: true })] }));
  children.push(new Paragraph({ spacing: { after: 38 }, keepNext: true,
    children: [new TextRun({ text: [(PLAT[e.source] || e.source), e.date ? ("posted " + e.date) : "date n/a", e.vertical].filter(Boolean).join("    ·    ") + "    ", size: 17, color: GREY, italics: true }), e.url ? new ExternalHyperlink({ link: e.url, children: [new TextRun({ text: "[open posting]", style: "Hyperlink", size: 17 })] }) : new TextRun({ text: "" })] }));
  children.push(new Paragraph({ spacing: { before: 18, after: 8 }, keepNext: true, shading: { type: ShadingType.CLEAR, fill: WFBG }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: WFBAR, space: 8 }, top: { style: BorderStyle.SINGLE, size: 2, color: WFBAR, space: 3 } },
    children: [new TextRun({ text: "ADOBE WORKFLOW  ", bold: true, size: 16, color: WFBAR }), new TextRun({ text: e.mcp_workflow, size: 18, color: "1F4E79" })] }));
  children.push(new Paragraph({ spacing: { before: 28, after: 6 }, keepNext: true, shading: { type: ShadingType.CLEAR, fill: INBG }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: INBAR, space: 8 }, top: { style: BorderStyle.SINGLE, size: 2, color: INBAR, space: 3 } },
    children: [new TextRun({ text: "INPUT ASSETS THE AGENT NEEDS", bold: true, size: 16, color: "9A6410" })] }));
  (e.inputs || []).forEach(inp => children.push(new Paragraph({ spacing: { after: 4 }, shading: { type: ShadingType.CLEAR, fill: INBG }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: INBAR, space: 8 } }, indent: { left: 200 },
    children: [new TextRun({ text: "•  ", bold: true, size: 18, color: INBAR }), new TextRun({ text: inp, size: 18, color: "5C4413" })] })));
  const hasNote = (e.feasibility !== "full") && e.note;
  children.push(new Paragraph({ spacing: { after: hasNote ? 4 : 28 }, shading: { type: ShadingType.CLEAR, fill: INBG }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: INBAR, space: 8 }, bottom: hasNote ? undefined : { style: BorderStyle.SINGLE, size: 2, color: INBAR, space: 3 } }, children: [new TextRun({ text: "", size: 2 })] }));
  if (hasNote) {
    children.push(new Paragraph({ spacing: { before: 22, after: 28 }, keepNext: true, shading: { type: ShadingType.CLEAR, fill: LIMBG }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: LIMBAR, space: 8 }, top: { style: BorderStyle.SINGLE, size: 2, color: LIMBAR, space: 3 }, bottom: { style: BorderStyle.SINGLE, size: 2, color: LIMBAR, space: 3 } },
      children: [new TextRun({ text: (e.feasibility === "template" ? "TEMPLATE NOTE  " : "CONNECTOR LIMIT  "), bold: true, size: 16, color: LIMBAR }), new TextRun({ text: e.note, size: 18, color: "7A3422" })] }));
  }
  const jd = (e.desc || "").replace(/\s+/g, " ").trim();
  children.push(new Paragraph({ spacing: { before: 28, after: 8 }, keepNext: true, shading: { type: ShadingType.CLEAR, fill: JDBG }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: JDBAR, space: 8 }, top: { style: BorderStyle.SINGLE, size: 2, color: JDBAR, space: 3 } },
    children: [new TextRun({ text: "ORIGINAL CLIENT BRIEF", bold: true, size: 16, color: "3A6624" })] }));
  children.push(new Paragraph({ spacing: { after: 110 }, shading: { type: ShadingType.CLEAR, fill: JDBG }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: JDBAR, space: 8 }, bottom: { style: BorderStyle.SINGLE, size: 2, color: JDBAR, space: 3 } },
    children: [new TextRun({ text: jd.length > 1400 ? jd.slice(0, 1400) + " …" : jd, size: 18, color: "44503A" })] }));
  children.push(new Paragraph({ spacing: { after: 70 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 8 } }, children: [new TextRun({ text: "", size: 2 })] }));
}

let n = 0;
famSorted.forEach((f) => {
  const list = Object.values(byFam[f]).flat();
  children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 200, after: 150 }, shading: { type: ShadingType.CLEAR, fill: INK },
    border: { left: { style: BorderStyle.SINGLE, size: 30, color: ACCENT, space: 10 } },
    children: [new Bookmark({ id: slug("fam-" + f), children: [new TextRun({ text: "  " + f + "   —   " + list.length + " tasks  ", color: "FFFFFF", size: 30 })] })] }));
  Object.keys(byFam[f]).sort((a, b) => byFam[f][b].length - byFam[f][a].length).forEach(c => {
    const cl = byFam[f][c];
    children.push(subbanner(c + "   (" + cl.length + "  —  ✓" + cnt(cl,x=>x.feasibility==="full") + " full, ◆" + cnt(cl,x=>x.feasibility==="template") + " template, ◑" + cnt(cl,x=>x.feasibility==="partial") + " partial)", slug(c)));
    cl.sort((a,b)=>({full:0,template:1,partial:2}[a.feasibility]-{full:0,template:1,partial:2}[b.feasibility]) || (a.title||"").localeCompare(b.title||""));
    cl.forEach(e => renderEntry(e, ++n));
  });
});

const footer = new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Adobe Connector-Doable Tasks   ·   " + E.length + " tasks   ·   compiled 9 Jun 2026   ·   page ", size: 16, color: "AAAAAA" }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "AAAAAA" })] });
const doc = new Document({
  styles: { default: { document: { run: { font: "Calibri", size: 22 }, paragraph: { spacing: { line: 270 } } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 30, bold: true, font: "Calibri", color: INK }, paragraph: { spacing: { before: 240, after: 130 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 24, bold: true, font: "Calibri", color: ACCENT2 }, paragraph: { spacing: { before: 200, after: 110 }, outlineLevel: 1 } } ] },
  numbering: { config: [{ reference: "b", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 560, hanging: 280 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } }, footers: { default: new Footer({ children: [footer] }) }, children }]
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log("WROTE", OUT, "—", E.length, "tasks ·", fams.length, "families · tiers:", nFull, "full /", nTpl, "template /", nPart, "partial"); });
