// Builds "StudioBench_Spec.docx" from the paper-style markdown spec.
// Small purpose-built md->docx renderer (headings, tables, bullet/ordered lists,
// inline bold/italic/code, horizontal rules) using docx 9.7.1.
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, TableOfContents,
  Footer, PageNumber, TableLayoutType, PageBreak,
} = require("docx");

const SRC = process.argv[2] || (process.env.HOME + "/.claude/plans/snoopy-imagining-kite.md");
const OUT = process.argv[3] || path.join(process.cwd(), "StudioBench_Spec.docx");

const md = fs.readFileSync(SRC, "utf8");
const lines = md.replace(/\r\n/g, "\n").split("\n");

const BODY_FONT = "Arial";      // universally available in Word
const MONO = "Courier New";     // universally available monospace
const CONTENT_W = 9360;         // ~6.5in printable width in twips
const cellBorder = { style: BorderStyle.SINGLE, size: 4, color: "BBBBBB" };
const TBL_BORDERS = {
  top: cellBorder, bottom: cellBorder, left: cellBorder, right: cellBorder,
  insideHorizontal: cellBorder, insideVertical: cellBorder,
};

// ---- inline parser: **bold**, `code`, *italic*
function parseInline(text, base = {}) {
  const runs = [];
  let i = 0;
  const pats = [
    { re: /\*\*([\s\S]+?)\*\*/, style: { bold: true } },
    { re: /`([^`]+?)`/, style: { font: MONO } },
    { re: /\*([^*]+?)\*/, style: { italics: true } },
  ];
  while (i < text.length) {
    let best = null;
    for (const p of pats) {
      const m = p.re.exec(text.slice(i));
      if (m) {
        const idx = i + m.index;
        if (!best || idx < best.idx) best = { idx, len: m[0].length, content: m[1], style: p.style };
      }
    }
    if (!best) { runs.push(new TextRun({ text: text.slice(i), ...base })); break; }
    if (best.idx > i) runs.push(new TextRun({ text: text.slice(i, best.idx), ...base }));
    runs.push(new TextRun({ text: best.content, ...base, ...best.style }));
    i = best.idx + best.len;
  }
  if (runs.length === 0) runs.push(new TextRun({ text: "", ...base }));
  return runs;
}

const isTableLine = (l) => /^\s*\|.*\|\s*$/.test(l);
const isSepRow = (cells) => cells.length > 0 && cells.every((c) => /^:?-{1,}:?$/.test(c.trim()));
const alignOf = (c) => {
  const t = c.trim();
  if (t.startsWith(":") && t.endsWith(":")) return AlignmentType.CENTER;
  if (t.endsWith(":")) return AlignmentType.RIGHT;
  return AlignmentType.LEFT;
};
const splitRow = (l) => l.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());

function buildTable(block) {
  const rows = block.map(splitRow);
  let sepIdx = rows.findIndex(isSepRow);
  const aligns = sepIdx >= 0 ? rows[sepIdx].map(alignOf) : rows[0].map(() => AlignmentType.LEFT);
  const dataRows = rows.filter((_, idx) => idx !== sepIdx);
  const header = dataRows[0];
  const body = dataRows.slice(1);
  const ncol = header.length;

  // ---- explicit column widths (fixed layout) so Word doesn't collapse columns.
  // Width ∝ longest cell per column (capped so one long cell can't eat the table),
  // with a per-column minimum, then normalized to the printable width.
  const CAP = 26, MINW = 460;
  const maxlen = new Array(ncol).fill(1);
  for (const r of dataRows) {
    for (let c = 0; c < ncol; c++) {
      const t = (r[c] || "").replace(/[*`]/g, "");
      maxlen[c] = Math.max(maxlen[c], Math.min(CAP, t.length));
    }
  }
  const sum = maxlen.reduce((a, b) => a + b, 0);
  let widths = maxlen.map((l) => Math.max(MINW, Math.round((CONTENT_W * l) / sum)));
  const s2 = widths.reduce((a, b) => a + b, 0);
  widths = widths.map((w) => Math.round((w * CONTENT_W) / s2));

  const mkCell = (txt, ci, isHeader) =>
    new TableCell({
      width: { size: widths[ci], type: WidthType.DXA },
      margins: { top: 40, bottom: 40, left: 90, right: 90 },
      shading: isHeader ? { fill: "1A1333" } : undefined,
      children: [
        new Paragraph({
          alignment: aligns[ci] || AlignmentType.LEFT,
          spacing: { after: 0 },
          children: parseInline(txt || "", isHeader ? { bold: true, color: "FFFFFF" } : {}),
        }),
      ],
    });

  const trows = [
    new TableRow({ tableHeader: true, children: header.map((c, ci) => mkCell(c, ci, true)) }),
    ...body.map((r) => new TableRow({ children: header.map((_, ci) => mkCell(r[ci], ci, false)) })),
  ];
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: widths,
    layout: TableLayoutType.FIXED,
    borders: TBL_BORDERS,
    rows: trows,
  });
}

function heading(line) {
  const m = /^(#{1,3})\s+(.*)$/.exec(line);
  const level = m[1].length;
  const txt = m[2];
  if (level === 1) return new Paragraph({ heading: HeadingLevel.TITLE, spacing: { after: 80 }, children: parseInline(txt) });
  if (level === 2) return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 240, after: 100 }, children: parseInline(txt) });
  return new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 160, after: 60 }, children: parseInline(txt) });
}

const hr = () =>
  new Paragraph({ spacing: { before: 80, after: 80 }, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "CCCCCC", space: 1 } }, children: [new TextRun("")] });

// ---- main walk
const children = [];
let firstHeadingDone = false;
for (let i = 0; i < lines.length; i++) {
  let line = lines[i];
  if (line.trim() === "") continue;

  if (line.trim() === "[[PAGEBREAK]]") { children.push(new Paragraph({ children: [new PageBreak()] })); continue; }

  if (isTableLine(line)) {
    const block = [];
    while (i < lines.length && isTableLine(lines[i])) { block.push(lines[i]); i++; }
    i--;
    children.push(buildTable(block));
    children.push(new Paragraph({ spacing: { after: 80 }, children: [new TextRun("")] }));
    continue;
  }

  if (/^#{1,3}\s+/.test(line)) {
    children.push(heading(line));
    // insert TOC right after the very first (title) heading
    if (!firstHeadingDone) {
      firstHeadingDone = true;
      // subtitle (next non-blank line if italic) handled by normal flow
      children.push(new Paragraph({ spacing: { before: 120, after: 40 }, children: [new TextRun({ text: "Contents", bold: true, size: 24 })] }));
      children.push(new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-2" }));
      children.push(hr());
    }
    continue;
  }

  if (line.trim() === "---") { children.push(hr()); continue; }

  const bullet = /^\s*-\s+(.*)$/.exec(line);
  if (bullet) {
    children.push(new Paragraph({ bullet: { level: 0 }, spacing: { after: 40 }, children: parseInline(bullet[1]) }));
    continue;
  }

  const ol = /^\s*(\d+)\.\s+(.*)$/.exec(line);
  if (ol) {
    children.push(new Paragraph({
      indent: { left: 360, hanging: 260 }, spacing: { after: 40 },
      children: [new TextRun({ text: ol[1] + ". ", bold: true }), ...parseInline(ol[2])],
    }));
    continue;
  }

  // plain paragraph
  children.push(new Paragraph({ spacing: { after: 100 }, children: parseInline(line) }));
}

const doc = new Document({
  creator: "StudioBench",
  title: "StudioBench — A Benchmark for Long-Horizon Creative-Agent Workflows",
  styles: {
    default: { document: { run: { font: BODY_FONT, size: 21 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", next: "Normal", run: { size: 40, bold: true, color: "1A1333" }, paragraph: { spacing: { after: 120 } } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 30, bold: true, color: "2E2152" } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 25, bold: true, color: "4A3A7A" } },
    ],
  },
  sections: [
    {
      properties: { page: { margin: { top: 1000, bottom: 1000, left: 1100, right: 1100 } } },
      footers: {
        default: new Footer({
          children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "StudioBench · page ", size: 16, color: "888888" }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "888888" })] })],
        }),
      },
      children,
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log("wrote", OUT, "(" + (buf.length / 1024).toFixed(1) + " KB)");
});
