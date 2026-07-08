// Build Upwork_Tasks.docx from the 448 browser-harvested FULL briefs (upwork_full_448.json).
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, ExternalHyperlink, InternalHyperlink,
  Bookmark, HeadingLevel, BorderStyle, PageBreak, PageNumber, Footer, Table, TableRow, TableCell,
  WidthType, ShadingType, VerticalAlign, LevelFormat
} = require("docx");

const INK="16243F", ACCENT="1A7A5E", ACCENT2="0F5C46", BAND="E7F1EC", CARD="F2F8F5", GREY="6B7280", DARK="23303F", LINE="D9DEE8";
const raw = JSON.parse(fs.readFileSync(__dirname + "/upwork_full_448.json", "utf8"));
const clean = s => (s || "").replace(/\s+/g, " ").trim();
const slug = s => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");

function detectVertical(title, desc) {
  const t = (title + " " + desc).toLowerCase(); const any = (...k) => k.some(x => t.includes(x));
  if (any("wedding","bride","groom","save the date","bridal","invitation suite")) return "Wedding & Stationery";
  if (any("cannabis","dispensary"," cbd","vape","smoke shop")) return "Cannabis & Dispensary";
  if (any("skincare","skin care","cosmetic","makeup","perfume","fragrance"," salon"," spa ","serum","beauty brand","haircare")) return "Beauty, Cosmetics & Personal Care";
  if (any(" pet ","pets ","dog ","cat ","puppy","veterinar")) return "Pets & Animals";
  if (any("restaurant","menu","food ","beverage","coffee","cafe","bakery","snack","brewery","wine","chocolate","juice","catering","chef")) return "Food, Restaurant & Beverage";
  if (any("medical","health","clinic","hospital","dental","pharma","wellness","therapy","fitness","gym","healthcare","supplement","nutrition")) return "Health, Wellness & Medical";
  if (any("real estate","realtor","property","construction","architect","interior design","landscap","contractor","renovation","mortgage")) return "Real Estate, Construction & Property";
  if (any("automotive","vehicle","truck","motorcycle","agricultur","industrial","manufactur","machinery","equipment")) return "Automotive, Industrial & Agriculture";
  if (any("church","ministry","nonprofit","non-profit","charity"," ngo","foundation","mosque","temple","islamic","christian","fundrais")) return "Nonprofit, Religious & Community";
  if (any("school","education","course","student","kids","children","learning","university","teacher","academy","e-learning","textbook")) return "Education & Children";
  if (any("finance","financial","bank","investment","consult","law firm","legal","attorney","accounting","insurance","advisory","crypto","fintech","pitch deck","wealth","coaching")) return "Finance, Crypto & Professional Services";
  if (any("fashion","apparel","clothing","t-shirt","tshirt","streetwear","jersey","garment","tech pack","lookbook","textile","jewelry","footwear","swimwear","merch ","boutique")) return "Fashion & Apparel";
  if (any("music","album","band ","record label","book cover","novel","author","publish","magazine"," film","movie","podcast","comic","entertainment","gaming")) return "Music, Film, Publishing & Media";
  if (any("ecommerce","e-commerce","amazon","shopify","etsy","online store","dropship","product listing","product photo","packshot")) return "E-commerce, Retail & Product";
  if (any("saas","software","startup"," app ","mobile app","platform","cyber"," ai ","tech company","b2b","dashboard","ui/ux","ui ux","web app","website","landing page")) return "Technology, SaaS & Web";
  if (any("motion graphic","explainer","after effects","kinetic","video edit","reel","footage","video editor","youtube")) return "Video Editing & Motion Graphics";
  if (any("retouch","photo editing","photo edit","background remov","photo restoration","color correct","image editing","prepress")) return "Photo Editing, Retouching & Restoration";
  if (any("event","party","concert","festival","gala","conference","expo","exhibition","trade show")) return "Party, Events & Promotion";
  return "General / Cross-Industry Branding & Graphics";
}
function deriveTools(skills, text) {
  const s = (skills.join(" ") + " " + text).toLowerCase(); const out = []; const add = x => { if (!out.includes(x)) out.push(x); };
  if (s.includes("photoshop")) add("Photoshop"); if (s.includes("illustrator")) add("Illustrator"); if (s.includes("indesign")) add("InDesign");
  if (s.includes("after effects")) add("After Effects"); if (s.includes("premiere")) add("Premiere Pro"); if (s.includes("lightroom")) add("Lightroom");
  if (s.includes("adobe xd")) add("XD"); if (s.includes("animate")) add("Animate"); if (s.includes("acrobat")) add("Acrobat");
  if (!out.length) {
    if (/(motion graphic|after effects|explainer|kinetic)/.test(text)) add("After Effects");
    if (/(video|reel|premiere|footage|youtube)/.test(text)) add("Premiere Pro");
    if (/(retouch|photo edit|composit|background remov|restoration|color grad)/.test(text)) add("Photoshop");
    if (/(brochure|catalog|magazine|booklet|multi-?page|annual report|ebook|layout|book )/.test(text)) add("InDesign");
    if (/(logo|vector|\.ai|\.eps|svg|brand|illustration)/.test(text)) add("Illustrator");
    if (!out.length) { add("Photoshop"); add("Illustrator"); }
  }
  return out.slice(0, 4);
}
function toolsWhy(text) {
  const t = text.toLowerCase(), c = [];
  if (/(print-ready|cmyk|300\s?dpi|bleed|press-ready|pantone)/.test(t)) c.push("print-ready CMYK output");
  if (/(vector|\.ai\b|\.eps|svg|scalable|logo)/.test(t)) c.push("scalable vector artwork");
  if (/(\.psd|layered|retouch|composit|mockup|photo)/.test(t)) c.push("layered/retouched assets");
  if (/(multi-?page|brochure|catalog|magazine|booklet|layout|indesign)/.test(t)) c.push("multi-page layout");
  if (/(video|reel|motion|footage|animation|explainer)/.test(t)) c.push("video/motion editing");
  return c.length ? "for " + c.slice(0, 2).join(" and ") : "";
}
function parseBudget(info) {
  if (!info) return "See posting";
  const h = info.match(/Hourly:?\s*(\$[\d.,]+(?:\s*-\s*\$[\d.,]+)?)/i);
  if (h) return "Hourly " + h[1].replace(/\.00/g, "").replace(/\s/g, "");
  if (/Hourly/i.test(info)) return "Hourly";
  const fb = info.match(/budget:?\s*(\$[\d.,]+)/i);
  if (fb) return "Fixed " + fb[1].replace(/\.00/g, "");
  if (/Fixed/i.test(info)) return "Fixed price";
  const a = info.match(/\$[\d.,]+/); return a ? a[0] : "See posting";
}
const expOf = i => ((i || "").match(/Entry Level|Intermediate|Expert/) || [""])[0];
const NONDESIGN = /(link building|guest post|cold calling|appointment setter|telemarket|bookkeep|lead generation|seo outreach)/i;

let tasks = [];
for (const j of Object.values(raw)) {
  const title = clean(j.t), desc = clean(j.d);
  if (!title || desc.length < 90) continue;
  if (NONDESIGN.test(title + " " + desc) && !/(design|photoshop|illustrat|photo edit|retouch|brand|logo)/i.test(title + " " + desc)) continue;
  const skills = (j.s || []).filter(Boolean);
  const tools = deriveTools(skills, (title + " " + desc).toLowerCase());
  tasks.push({ title, desc, skills, tools, toolsWhy: toolsWhy(title + " " + desc), vertical: detectVertical(title, desc), budget: parseBudget(j.i), exp: expOf(j.i) });
}
const seen = new Set(); tasks = tasks.filter(t => { const k = t.title.toLowerCase(); if (seen.has(k)) return false; seen.add(k); return true; });
fs.writeFileSync(__dirname + "/upwork_full_processed.json", JSON.stringify(tasks));

const byVert = {}; tasks.forEach(t => (byVert[t.vertical] = byVert[t.vertical] || []).push(t));
const verticals = Object.keys(byVert).sort((a, b) => byVert[b].length - byVert[a].length);
verticals.forEach(v => byVert[v].sort((a, b) => b.desc.length - a.desc.length));
const toolCount = {}; tasks.forEach(t => t.tools.forEach(x => toolCount[x] = (toolCount[x] || 0) + 1));
const topTools = Object.entries(toolCount).sort((a, b) => b[1] - a[1]).map(([k, v]) => k + " (" + v + ")").join("   ·   ");
console.log("UPWORK FULL:", tasks.length, "tasks across", verticals.length, "industries");

const children = [];
function banner(text, id) { return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 220, after: 140 }, shading: { type: ShadingType.CLEAR, fill: BAND }, border: { left: { style: BorderStyle.SINGLE, size: 26, color: ACCENT, space: 8 }, bottom: { style: BorderStyle.SINGLE, size: 6, color: INK, space: 4 } }, children: [id ? new Bookmark({ id, children: [new TextRun(text)] }) : new TextRun(text)] }); }
const bd = { style: BorderStyle.SINGLE, size: 2, color: LINE }, borders = { top: bd, bottom: bd, left: bd, right: bd };
const cell = (text, w, fill, o) => { o = o || {}; return new TableCell({ width: { size: w, type: WidthType.DXA }, borders, shading: { type: ShadingType.CLEAR, fill }, margins: { top: 50, bottom: 50, left: 120, right: 120 }, verticalAlign: VerticalAlign.CENTER, children: [new Paragraph({ alignment: o.align || AlignmentType.LEFT, children: [new TextRun({ text, bold: !!o.bold, color: o.color || DARK, size: o.size || 20 })] })] }); };

children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 1500, after: 0 }, shading: { type: ShadingType.CLEAR, fill: INK }, children: [new TextRun({ text: "  Upwork — Adobe Tasks (Full Briefs)  ", bold: true, size: 48, font: "Calibri", color: "FFFFFF" })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 160, after: 40 }, children: [new TextRun({ text: "Currently-open Upwork postings requiring Adobe tools — complete briefs", size: 26, color: DARK })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 30 }, children: [new TextRun({ text: "Harvested read-only from search results (DOM text, no OCR)", size: 21, color: ACCENT, italics: true })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 340 }, children: [new TextRun({ text: "Captured 5 June 2026", size: 20, color: GREY })] }));
[[tasks.length + " full task briefs", "complete client descriptions — paginated across dozens of Adobe searches"],
 [verticals.length + " industries", "video, branding, real estate, fashion, publishing, finance & more"],
 ["Each entry", "title · budget · experience · Adobe tools · the full brief"],
 ["Note", "per-job permalinks are blocked by Upwork's page sandbox; full links come via the API"]
].forEach(g => children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 70 }, children: [new TextRun({ text: g[0] + "   —   ", bold: true, size: 23, color: ACCENT }), new TextRun({ text: g[1], size: 20, color: DARK })] })));
children.push(new Paragraph({ children: [new PageBreak()] }));

children.push(banner("About this document", "about"));
["What this is: every currently-open Upwork posting I could reach that genuinely requires Adobe Creative Cloud work — with the COMPLETE brief, not a summary. " + tasks.length + " tasks across " + verticals.length + " industries.",
 "How it was captured: read-only, from Upwork's own search-result cards (the full description is in the page, just visually clamped). Pure DOM text — no OCR, no screenshots. Paginated across dozens of Adobe/design searches and several result pages each.",
 "Tools and industry are derived from each posting's skill tags and text; budgets/experience are shown as Upwork displayed them.",
 "One limit: Upwork's page sandbox blocks per-job URLs, so individual permalinks aren't included. The official Upwork API (approval pending) returns those plus the full inventory."
].forEach(t => children.push(new Paragraph({ numbering: { reference: "b", level: 0 }, spacing: { after: 100 }, children: [new TextRun({ text: t, size: 21 })] })));

children.push(banner("Snapshot"));
const rows = [new TableRow({ tableHeader: true, children: [cell("Industry", 7400, INK, { bold: true, color: "FFFFFF" }), cell("Tasks", 1960, INK, { bold: true, color: "FFFFFF", align: AlignmentType.CENTER })] })];
verticals.forEach((v, i) => rows.push(new TableRow({ children: [cell(v, 7400, i % 2 ? CARD : "FFFFFF", { color: INK }), cell(String(byVert[v].length), 1960, i % 2 ? CARD : "FFFFFF", { bold: true, color: ACCENT2, align: AlignmentType.CENTER })] })));
children.push(new Table({ width: { size: 9360, type: WidthType.DXA }, columnWidths: [7400, 1960], rows }));
children.push(new Paragraph({ spacing: { before: 160, after: 40 }, children: [new TextRun({ text: "Adobe tool coverage:  ", bold: true, size: 20, color: ACCENT2 }), new TextRun({ text: topTools, size: 19, color: DARK })] }));

children.push(banner("Contents"));
verticals.forEach(v => children.push(new Paragraph({ spacing: { after: 36 }, children: [new InternalHyperlink({ anchor: slug(v), children: [new TextRun({ text: v, style: "Hyperlink", size: 21 })] }), new TextRun({ text: "   (" + byVert[v].length + ")", size: 19, color: GREY })] })));

function renderTask(t, n) {
  children.push(new Paragraph({ spacing: { before: 200, after: 40 }, keepNext: true, shading: { type: ShadingType.CLEAR, fill: CARD }, border: { left: { style: BorderStyle.SINGLE, size: 20, color: ACCENT, space: 8 } }, children: [new TextRun({ text: n + ".  " + t.title, bold: true, size: 24, font: "Calibri", color: INK })] }));
  children.push(new Paragraph({ spacing: { after: 50 }, keepNext: true, children: [new TextRun({ text: ["Upwork", t.budget, t.exp].filter(Boolean).join("    ·    "), italics: true, size: 19, color: GREY })] }));
  children.push(new Paragraph({ spacing: { after: 70 }, keepNext: true, children: [new TextRun({ text: "Adobe tools:  ", bold: true, size: 20, color: ACCENT2 }), new TextRun({ text: t.tools.join("  ·  "), bold: true, size: 20, color: ACCENT2 }), new TextRun({ text: t.toolsWhy ? "   —   " + t.toolsWhy : "", size: 19, color: DARK }), new TextRun({ text: t.skills && t.skills.length ? "      Skills: " + t.skills.slice(0, 8).join(", ") : "", size: 18, color: GREY })] }));
  children.push(new Paragraph({ spacing: { after: 200 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 8 } }, children: [new TextRun({ text: t.desc, size: 21, color: DARK })] }));
}
verticals.forEach(v => {
  children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(banner(v, slug(v)));
  children.push(new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: byVert[v].length + (byVert[v].length === 1 ? " task" : " tasks"), italics: true, size: 19, color: GREY })] }));
  byVert[v].forEach((t, k) => renderTask(t, k + 1));
});

const footerPara = new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Upwork — Adobe Tasks (Full Briefs)   ·   captured 5 Jun 2026   ·   page ", size: 16, color: "AAAAAA" }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "AAAAAA" })] });
const doc = new Document({
  styles: { default: { document: { run: { font: "Calibri", size: 22 }, paragraph: { spacing: { line: 288 } } } }, paragraphStyles: [{ id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 30, bold: true, font: "Calibri", color: INK }, paragraph: { spacing: { before: 220, after: 130 }, outlineLevel: 0 } }] },
  numbering: { config: [{ reference: "b", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 560, hanging: 280 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } }, footers: { default: new Footer({ children: [footerPara] }) }, children }]
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(__dirname + "/Upwork_Tasks.docx", b); console.log("WROTE Upwork_Tasks.docx —", tasks.length, "full briefs across", verticals.length, "industries"); });
