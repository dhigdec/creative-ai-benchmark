const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, LevelFormat, HeadingLevel, BorderStyle, WidthType, ShadingType } = require("docx");

const N = JSON.parse(fs.readFileSync("/tmp/doc_numbers.json", "utf8"));
const CW = 9360;
const PURPLE = "3C2F73", LILAC = "EFE9FB", GREY = "F1EFF6", LINE = "CCCCCC";
const border = { style: BorderStyle.SINGLE, size: 1, color: LINE };
const borders = { top: border, bottom: border, left: border, right: border,
                  insideHorizontal: border, insideVertical: border };
const cellMargin = { top: 60, bottom: 60, left: 120, right: 120 };

function P(text, opts = {}) {
  return new Paragraph({ spacing: { after: opts.after ?? 120 }, children: [new TextRun({ text, size: opts.size ?? 22, bold: !!opts.bold, color: opts.color })] });
}
function bullet(text, bold) {
  const parts = []; // support "label — rest" bolding of the label
  if (bold && text.includes(" — ")) {
    const i = text.indexOf(" — ");
    parts.push(new TextRun({ text: text.slice(0, i), bold: true, size: 22 }));
    parts.push(new TextRun({ text: text.slice(i), size: 22 }));
  } else parts.push(new TextRun({ text, size: 22 }));
  return new Paragraph({ numbering: { reference: "b", level: 0 }, spacing: { after: 60 }, children: parts });
}
function cell(text, { w, head = false, bold = false, align } = {}) {
  return new TableCell({ borders, width: { size: w, type: WidthType.DXA }, margins: cellMargin,
    shading: head ? { fill: PURPLE, type: ShadingType.CLEAR } : undefined,
    children: [new Paragraph({ alignment: align, children: [new TextRun({ text: String(text), size: 20, bold: head || bold, color: head ? "FFFFFF" : undefined })] })] });
}
function table(rows2d, widths, { headerRow = true, numCols = [] } = {}) {
  return new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: widths,
    rows: rows2d.map((r, ri) => new TableRow({ tableHeader: ri === 0 && headerRow,
      children: r.map((c, ci) => cell(c, { w: widths[ci], head: ri === 0 && headerRow, align: numCols.includes(ci) ? AlignmentType.CENTER : undefined })) })) });
}
function countTable(title, obj, order) {
  const rows = [[title, "Tasks"]];
  let tot = 0;
  (order || Object.keys(obj)).forEach(k => { rows.push([k, obj[k]]); tot += obj[k]; });
  rows.push(["Total", tot]);
  return table(rows, [6960, 2400], { numCols: [1] });
}

const OPN = { O1: "O1 tonal grade & restore", O2: "O2 masked recolor & isolation", O3: "O3 video & audio",
  O4: "O4 preset retouch & look-dev", O5: "O5 data-merge & layout", O6: "O6 stylized & duotone",
  O7: "O7 vector & screen-print", O8: "O8 stock-sourced hero" };

const children = [];
const push = (...x) => children.push(...x);

// ---- Title ----
push(new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: "Creative AI Benchmark", bold: true, size: 44, color: PURPLE })] }));
push(new Paragraph({ spacing: { after: 240 }, children: [new TextRun({ text: "What we built · the metadata tags · the task distribution", size: 24, color: "5A5274" })] }));
push(P("A plain-English overview of the 100-task creative benchmark: what it is, the labels (metadata tags) we put on every task, and the distribution table used to plan the budget.", { after: 240 }));

// ---- 1. What we did ----
push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("1.  What we did")] }));
push(P("We built a benchmark of 100 real creative tasks — the kind of jobs a freelance designer gets — and organized it so it can be measured, priced, and sold. Specifically:"));
push(bullet("Organized the set by the nature of the task (create / edit / analyze), not by brand.", true));
push(bullet("Designed a standard set of metadata tags (labels) and put them on every task.", true));
push(bullet("Grew the set from 66 to 100 tasks, balanced across industries.", true));
push(bullet("Built a distribution table so the human-annotation budget can be planned.", true));
push(bullet("Kept it editing / analysis only (no image generation), Adobe-connector tools only, and QA'd every task.", true));

// ---- 2. The 100 tasks ----
push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("2.  The 100 tasks")] }));
push(P("Each task is a genuine freelance brief (grounded in a real posting, with fictional IP-clean brand names) that an AI agent completes using Adobe Creative Cloud tools. The set spans:"));
push(bullet(`${N.domains_used} industries (food, retail, jewelry, fashion, real estate, media, and more).`));
push(bullet("4 families of work: Photo & Image · Vector & Print · Layout & Data · Motion & Audio."));
push(bullet("All three activity types: create, edit, and analyze."));

// ---- 3. Metadata tags ----
push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("3.  The metadata tags")] }));
push(P("What they are (simple):", { bold: true, after: 60 }));
push(P("A metadata tag is just a label with a fixed set of allowed answers — like a form with dropdowns. We put the same set of labels on every task, which turns 100 loose task descriptions into a clean, sortable spreadsheet."));
push(P("How we designed them:", { bold: true, after: 60 }));
push(bullet("Brainstormed from every angle (inputs, output, operation, difficulty, industry, sales value) → 100+ candidate tags."));
push(bullet("Distilled to a clean 71 tags, each with a fixed list of allowed answers."));
push(bullet("Grouped them into 9 categories so they read in sections, not one long wall."));
push(bullet("Split into two layers: 6 taxonomy tags (that organize the whole set) + 65 descriptive tags (extra detail)."));
push(bullet("Most tags are filled automatically or computed by code, so they are exact and consistent."));

push(P("The 9 groups of tags:", { bold: true, after: 80 }));
push(table([
  ["Group", "What it captures"],
  ["1. Identity & Deliverable", "what the task is — industry, deliverable, create/edit/analyze"],
  ["2. Input Assets", "what the client hands over — photos, logos, data files, templates"],
  ["3. Operation & Tooling", "the kind of work — the operation, the sub-steps, the tools used"],
  ["4. Output Spec", "the deliverable — image/video/document, format, size, colour space"],
  ["5. Domain & Brand", "context — audience, brand strictness, language, region"],
  ["6. Copy & Text", "the words — how much text, where it comes from"],
  ["7. Difficulty & Curriculum", "how hard and how long — planning, precision, effort, horizon"],
  ["8. Feasibility & Execution", "can our tools do it — doability, how it runs"],
  ["9. Data-Product & Scoring", "selling / scoring signals — capability buckets, licensing"],
], [3000, 6360]));

push(P("The 6 tags that organize everything (the taxonomy axes):", { bold: true, after: 80, after: 80 }));
push(table([
  ["Axis", "Plain meaning"],
  ["workflow_nature", "create / edit / analyze — the activity"],
  ["primary_operation", "the specific job (O1–O8)"],
  ["operation_family", "the 4 big groups (Photo, Vector, Layout, Motion)"],
  ["output_modality", "what the deliverable is (image / vector / document / video / audio)"],
  ["horizon_tier + est_calls", "how big the task is — the effort, which drives the price"],
], [2900, 6460]));

push(P("Example — one task's tags:", { bold: true, after: 60 }));
push(P("For a bakery task (\"finish our product catalog: grade the photos, vectorize the logo, merge into the template, export a print PDF\"), the tags read: industry = food, deliverable = catalog, workflow = create, operation = O5 data-merge, modality = document, print / CMYK, effort = 45 steps (long). …and so on for its 30 tags."));
push(P("Note: each task carries the 30 core tags (the must-haves shown above). The other 39 are an optional deeper layer, filled in only when finer slicing is needed — so the tagging stays clean, not overwhelming.", { after: 200 }));

// ---- 4. Distribution table ----
push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("4.  The taxonomy distribution table")] }));
push(P("What it is (simple):", { bold: true, after: 60 }));
push(P("Once every task has its tags, the distribution table is simply a count of those tags across all 100 tasks — a tally sheet. Here is the actual distribution of the set."));

push(P("By family (the 4 buckets):", { bold: true, after: 80 }));
push(countTable("Family", N.family, ["Photo & Image", "Vector & Print", "Layout & Data", "Motion & Audio"]));

push(P("By activity (create / edit / analyze):", { bold: true, after: 80 }));
push(countTable("Activity", { "create": N.workflow.create, "create + edit": N.workflow["create/edit"], "edit": N.workflow.edit, "analyze": N.workflow.analyze }, ["create", "create + edit", "edit", "analyze"]));

push(P("By output type (asset modality):", { bold: true, after: 80 }));
push(countTable("Output type", N.modality, ["image", "document", "vector", "video", "audio"]));

push(P("The pivot for budgeting (output type × activity):", { bold: true, after: 60 }));
push(P("Each cell is a chunk of work at a price bracket — Suma multiplies each by the right rate. Video and audio rows carry higher annotator cost.", { after: 80 }));
const pv = [["Output type", "Create", "Create+Edit", "Edit", "Analyze", "Total"]];
["image", "document", "vector", "video", "audio"].forEach(m => {
  const row = N.pivot[m]; const tot = row.create + row["create/edit"] + row.edit + row.analyze;
  pv.push([m, row.create, row["create/edit"], row.edit, row.analyze, tot]);
});
push(table(pv, [2160, 1440, 1440, 1440, 1440, 1440], { numCols: [1, 2, 3, 4, 5] }));

push(P("How Suma uses it:", { bold: true, after: 60, after: 60 }));
push(bullet("Budget — give each bucket a rate, multiply by its count, add up = the human-annotation cost.", true));
push(bullet("Balance — proves no single task type dominates, so the benchmark's results are trustworthy.", true));
push(bullet("Slicing — she or a buyer can pull \"all video tasks\" or \"all print data-merge jobs\" in one filter.", true));

push(new Paragraph({ spacing: { before: 240 }, children: [new TextRun({ text: "In one line: we put a standard set of labels on all 100 tasks, then counted those labels to build the distribution — turning loose tasks into a clean spreadsheet Suma can price and prove is balanced.", italics: true, size: 22, color: "5A5274" })] }));

const doc = new Document({
  numbering: { config: [{ reference: "b", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 460, hanging: 260 } } } }] }] },
  styles: { default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, font: "Arial", color: PURPLE },
        paragraph: { spacing: { before: 320, after: 140 }, outlineLevel: 0 } }] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1300, right: 1440, bottom: 1300, left: 1440 } } }, children }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync("/Users/dhiren/Downloads/Creative_AI_Benchmark_Overview.docx", buf); console.log("wrote Creative_AI_Benchmark_Overview.docx", buf.length, "bytes"); });
