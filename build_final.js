// Final builder v2: merge verified tasks + large Freelancer.com API pull,
// filter to complex + recent(<=31d) + Adobe-required + business-use, dedupe, cap ~300,
// render a beautified, sectioned docx (colored banners, snapshot table, card headers).
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat, ExternalHyperlink,
  InternalHyperlink, Bookmark, HeadingLevel, BorderStyle, PageBreak, PageNumber, Footer,
  Table, TableRow, TableCell, WidthType, ShadingType, VerticalAlign
} = require("docx");

// ---------- palette ----------
const INK = "16243F", ACCENT = "C8472B", ACCENT2 = "9E480E", BAND = "E8EDF5", CARD = "F5F7FB",
      GREY = "6B7280", DARK = "23303F", LINE = "D9DEE8";

// ---------- 1. verified tasks ----------
let EXISTING = [];
for (const f of ["tasks_b1.js","tasks_b2.js","tasks_b3.js","tasks_b4.js","tasks_b5.js","tasks_b6.js","tasks_upwork.js"]) {
  try { EXISTING = EXISTING.concat(require("./" + f)); } catch (e) { console.log("skip " + f + ": " + e.message); }
}
for (const f of ["tasks_upwork2.js"]) { try { EXISTING = EXISTING.concat(require("./" + f)); } catch (e) {} } // optional extra Upwork

// ---------- helpers ----------
const clean = s => (s || "").replace(/\s+/g, " ").trim();
const normUrl = u => (u || "").toLowerCase().replace(/#.*$/, "").replace(/\/+$/, "");
const normTitle = t => (t || "").toLowerCase().replace(/[^a-z0-9]+/g, "");
const slug = s => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
const NOW = Date.now() / 1000;

function detectVertical(title, desc) {
  const t = (title + " " + desc).toLowerCase();
  const any = (...k) => k.some(x => t.includes(x));
  if (any("wedding","bride","groom","save the date","save-the-date","bridal")) return "Wedding & Stationery";
  if (any("cannabis","dispensary"," cbd","thc","vape","smoke shop","marijuana","weed ")) return "Cannabis & Dispensary";
  if (any("skincare","skin care","cosmetic","makeup","perfume","fragrance"," salon"," spa ","serum","lotion","beauty brand","beauty ","haircare","shampoo")) return "Beauty, Cosmetics & Personal Care";
  if (any(" pet ","pets ","dog ","cat ","puppy","kitten","veterinar","animal ","pet brand")) return "Pets & Animals";
  if (any("restaurant","menu","food ","beverage","coffee","cafe","bakery","snack","spice","burger","pizza","kitchen","brewery","wine","chocolate"," tea ","juice","catering","culinary","chef","sauce","drink ","grocery","confection")) return "Food, Restaurant & Beverage";
  if (any("medical","health","clinic","hospital","dental","dentist","pharma","wellness","patient","doctor","nurse","supplement","nutrition","therapy","mental health","fitness","gym","healthcare")) return "Health, Wellness & Medical";
  if (any("real estate","realtor","property","construction","architect","interior design","landscap","contractor","renovation","mortgage","home builder","building company","facade")) return "Real Estate, Construction & Property";
  if (any("automotive","vehicle","truck","motorcycle","agricultur","farm","tractor","mower","industrial","manufactur","machinery","solar","mining","logistics","engineering firm","oil and gas","equipment")) return "Automotive, Industrial & Agriculture";
  if (any("church","ministry","nonprofit","non-profit","charity"," ngo","foundation","mosque","temple","islamic","christian","faith","fundrais","volunteer","community event","gospel")) return "Nonprofit, Religious & Community";
  if (any("school","education","course","student","kids","children","toddler","toy ","learning","university","teacher","flashcard","e-learning","academy","nursery","curriculum","tutoring")) return "Education & Children";
  if (any("finance","financial","bank","investment","consult","law firm","legal","attorney","accounting","insurance","advisory"," tax ","trading","crypto","fintech","pitch deck","wealth","capital")) return "Finance, Crypto & Professional Services";
  if (any("fashion","apparel","clothing","t-shirt","tshirt","streetwear","jersey","garment","tech pack","lookbook","textile","jewelry","jewellery","footwear","swimwear","scarf","hoodie","merch ","boutique","sneaker")) return "Fashion & Apparel";
  if (any("music","album","band ","record label","book cover","novel","author","publish","magazine"," film","movie","podcast","comic","webtoon","vtuber","entertainment","gaming","game studio","trailer","song")) return "Music, Film, Publishing & Media";
  if (any("ecommerce","e-commerce","amazon","shopify","etsy","online store","dropship","product listing","product photo","marketplace listing")) return "E-commerce, Retail & Product";
  if (any("saas","software","startup"," app ","mobile app","platform","cyber","fintech"," ai ","technology company","tech company","b2b","dashboard","ui/ux","web app")) return "Technology, SaaS & Startups";
  if (any("motion graphic","explainer","after effects","kinetic","video edit","reel","footage","animation video","2d animation","3d animation","video editor","whiteboard animation")) return "Video Editing & Motion Graphics";
  if (any("retouch","photo editing","photo edit","background remov","photo restoration","color correct","colour correct","image editing","prepress","photo manipulation")) return "Photo Editing, Retouching & Restoration";
  if (any("event","party","concert","festival","gala","conference","expo","exhibition","tradeshow","trade show")) return "Party, Events & Promotion";
  return "General / Cross-Industry Branding & Graphics";
}
function deriveTools(skills, text) {
  const s = skills.map(x => x.toLowerCase());
  const has = k => s.some(x => x.includes(k));
  const tools = []; const add = x => { if (!tools.includes(x)) tools.push(x); };
  if (has("photoshop")) add("Photoshop");
  if (has("illustrator")) add("Illustrator");
  if (has("indesign")) add("InDesign");
  if (has("after effects")) add("After Effects");
  if (has("premiere")) add("Premiere Pro");
  if (has("lightroom")) add("Lightroom");
  if (has("adobe xd")) add("XD");
  if (has("animate")) add("Animate");
  if (has("acrobat")) add("Acrobat");
  if (tools.length === 0) {
    const t = text.toLowerCase();
    if (/(motion graphic|after effects|explainer|kinetic|animated video)/.test(t)) add("After Effects");
    if (/(video|reel|premiere|footage)/.test(t)) add("Premiere Pro");
    if (/(retouch|photo edit|photo editing|composit|background remov|restoration|color grad|colour grad)/.test(t)) add("Photoshop");
    if (/(brochure|catalog|catalogue|magazine|booklet|multi-?page|annual report|ebook|layout|book )/.test(t)) add("InDesign");
    if (/(logo|vector|\.ai|\.eps|svg|brand|illustration)/.test(t)) add("Illustrator");
    if (tools.length === 0) { add("Photoshop"); add("Illustrator"); }
  }
  return tools.slice(0, 3);
}
function whyFor(tools, text) {
  const t = text.toLowerCase(), cues = [];
  if (/(print-ready|cmyk|300\s?dpi|bleed|press-ready|offset)/.test(t)) cues.push("print-ready CMYK output");
  if (/(vector|\.ai\b|\.eps|svg|scalable|logo)/.test(t)) cues.push("scalable vector artwork");
  if (/(\.psd|layered|retouch|composit|mockup|photo)/.test(t)) cues.push("layered/retouched assets");
  if (/(multi-?page|brochure|catalog|magazine|booklet|annual report|layout)/.test(t)) cues.push("multi-page layout");
  if (/(video|reel|motion|footage|animation|explainer)/.test(t)) cues.push("video/motion editing");
  return tools.join("  ·  ") + (cues.length ? "  —  for " + cues.slice(0, 2).join(" and ") : "");
}
function budgetStr(p) {
  const c = p.currency || {}, code = c.code || "", sign = c.sign || "";
  const b = p.budget || {}, lo = b.minimum, hi = b.maximum;
  const f = n => (n == null ? "" : (n % 1 === 0 ? String(n) : String(Math.round(n))));
  let s = "See posting";
  if (lo != null && hi != null) s = `${sign}${f(lo)}–${sign}${f(hi)} ${code}`;
  else if (lo != null) s = `${sign}${f(lo)}+ ${code}`;
  if ((p.type || "") === "hourly") s += " /hr";
  return s.trim();
}

// ---------- 2. ingest API ----------
const ADOBE_RX = /(photoshop|illustrator|indesign|after effects|premiere|lightroom|adobe xd|adobe creative|adobe |\.psd|\.ai\b|\.indd|\.eps)/i;
const ADOBE_SKILL_RX = /(photoshop|illustrator|indesign|after effects|premiere|lightroom|adobe)/i;
const TRIVIAL_RX = /(data entry|copy[- ]?paste|typing|resize \d|convert .* to word|pdf to word|sign ?up|captcha|survey|virtual assistant|lead generation|web scrap|wordpress install|fix my website|website development|app development|mobile app develop|\bseo\b|bookkeep|data mining|enter .* into excel)/i;
const PERSONAL_RX = /(fan ?art|\bd&d\b|\bdnd\b|dungeons|tattoo|cosplay|my girlfriend|my boyfriend|gift for my|portrait of my|my own personal|anime oc\b|for my bedroom)/i;
const BIZ_RX = /(brand|company|business|product|packaging|logo|market|client|commercial|store|startup|firm|corporate|launch|campaign|brochure|catalog|label|menu|signage|ecommerce|e-commerce|b2b|professional|agency|retail|investor|wholesale|customer|saas)/i;

let API = []; const apiSeen = new Set();
try {
  const files = [];
  for (const dir of ["/tmp/flp", "/tmp/flp2"]) { try { fs.readdirSync(dir).forEach(f => { if (f.endsWith(".json")) files.push(dir + "/" + f); }); } catch (e) {} }
  for (const fp of files) {
    let d; try { d = JSON.parse(fs.readFileSync(fp, "utf8")); } catch (e) { continue; }
    for (const p of ((d.result || {}).projects || [])) {
      if (apiSeen.has(p.id)) continue; apiSeen.add(p.id);
      const desc = clean(p.description);
      const skills = (p.jobs || []).map(j => j.name).filter(Boolean);
      if (desc.length < 750) continue;
      const blob = p.title + " " + desc;
      if (TRIVIAL_RX.test(blob)) continue;
      if (PERSONAL_RX.test(blob) && !BIZ_RX.test(blob)) continue;       // drop clear hobby/personal
      const adobeSkill = skills.some(x => ADOBE_SKILL_RX.test(x));
      if (!adobeSkill && !ADOBE_RX.test(desc)) continue;
      if (p.submitdate && p.submitdate < NOW - 31 * 86400) continue;
      const days = p.submitdate ? Math.max(0, Math.round((NOW - p.submitdate) / 86400)) : null;
      const tools = deriveTools(skills, desc);
      const cues = (desc.match(/(deliverable|print-ready|vector|mockup|cmyk|bleed|\.ai|\.psd|\.eps|source file|editable|dimensions|pantone|revision|format|guidelines|3d)/gi) || []).length;
      API.push({
        title: clean(p.title), vertical: detectVertical(p.title, desc), platform: "Freelancer.com",
        budget: budgetStr(p),
        posted: days == null ? "Active" : (days === 0 ? "Posted today" : "Posted " + days + (days === 1 ? " day ago" : " days ago")),
        url: "https://www.freelancer.com/projects/" + (p.seo_url || ""), tools, toolsWhy: whyFor(tools, desc), fulldesc: desc,
        _score: desc.length + 150 * tools.length + 220 * cues + (BIZ_RX.test(blob) ? 500 : 0)
      });
    }
  }
} catch (e) { console.log("API ingest note: " + e.message); }

// ---------- 3. merge + dedupe + select ----------
const TARGET = 100000, CAP = 100000; // include ALL qualifying briefs
const seenU = new Set(), seenT = new Set(), vc = {};
const result = [];
const push = t => { result.push(t); seenU.add(normUrl(t.url)); seenT.add(normTitle(t.title)); vc[t.vertical] = (vc[t.vertical] || 0) + 1; };
EXISTING.filter(t => clean(t.fulldesc).length >= 500).forEach(t => { if (!seenU.has(normUrl(t.url)) && !seenT.has(normTitle(t.title))) push(t); });
const apiSorted = API.sort((a, b) => b._score - a._score);
for (const t of apiSorted) { if (result.length >= TARGET) break; if (seenU.has(normUrl(t.url)) || seenT.has(normTitle(t.title))) continue; if ((vc[t.vertical] || 0) >= CAP) continue; push(t); }
for (const t of apiSorted) { if (result.length >= TARGET) break; if (seenU.has(normUrl(t.url)) || seenT.has(normTitle(t.title))) continue; push(t); }

// ---------- 4. group & order ----------
const VERT_ORDER = ["Fashion & Apparel","Beauty, Cosmetics & Personal Care","Food, Restaurant & Beverage","Wedding & Stationery","Party, Events & Promotion","Health, Wellness & Medical","Real Estate, Construction & Property","Automotive, Industrial & Agriculture","Technology, SaaS & Startups","E-commerce, Retail & Product","Cannabis & Dispensary","Music, Film, Publishing & Media","Video Editing & Motion Graphics","Photo Editing, Retouching & Restoration","Pets & Animals","Education & Children","Nonprofit, Religious & Community","Finance, Crypto & Professional Services","General / Cross-Industry Branding & Graphics"];
const byVert = {};
result.forEach(t => { (byVert[t.vertical] = byVert[t.vertical] || []).push(t); });
Object.values(byVert).forEach(arr => arr.sort((a, b) => (b._score || 0) - (a._score || 0)));
const verticals = [...VERT_ORDER.filter(v => byVert[v]), ...Object.keys(byVert).filter(v => !VERT_ORDER.includes(v))];
const total = result.length;
const toolCount = {};
result.forEach(t => (t.tools || []).forEach(x => { toolCount[x] = (toolCount[x] || 0) + 1; }));
const topTools = Object.entries(toolCount).sort((a, b) => b[1] - a[1]).map(([k, v]) => k + " (" + v + ")").join("   ·   ");
console.log("FINAL:", total, "tasks |", verticals.length, "industries | API candidates kept:", API.length);

// ---------- 5. render ----------
const children = [];
const rule = (color, size) => new Paragraph({ spacing: { after: 120 }, border: { bottom: { style: BorderStyle.SINGLE, size: size || 18, color } } });
// Cover
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 1500, after: 0 }, shading: { type: ShadingType.CLEAR, fill: INK },
  children: [new TextRun({ text: "  Adobe Creative Freelance Tasks  ", bold: true, size: 52, font: "Calibri", color: "FFFFFF" })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 160, after: 40 },
  children: [new TextRun({ text: "Complex, currently-open freelance briefs that require Adobe tools", size: 26, color: DARK })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 30 },
  children: [new TextRun({ text: "A business-use-case catalogue, organised by industry", size: 22, color: ACCENT, italics: true })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 360 },
  children: [new TextRun({ text: "Compiled 4 June 2026", size: 20, color: GREY })] }));
[
  [total + " substantial tasks", "every entry is a real, detailed brief — no listings, no trivial gigs"],
  [verticals.length + " industries", "fashion, food, healthcare, real estate, cannabis, film, finance & more"],
  ["Posted within ~30 days", "all briefs are recent and currently open"],
  ["Sources", "Freelancer.com API · PeoplePerHour · Upwork"]
].forEach(g => children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 70 }, children: [
  new TextRun({ text: g[0] + "   —   ", bold: true, size: 23, color: ACCENT }), new TextRun({ text: g[1], size: 20, color: DARK })] })));
children.push(new Paragraph({ children: [new PageBreak()] }));

// section heading helper (colored banner)
function banner(text, id) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 200, after: 140 },
    shading: { type: ShadingType.CLEAR, fill: BAND },
    border: { left: { style: BorderStyle.SINGLE, size: 26, color: ACCENT, space: 8 }, bottom: { style: BorderStyle.SINGLE, size: 6, color: INK, space: 4 } },
    children: [id ? new Bookmark({ id, children: [new TextRun(text)] }) : new TextRun(text)] });
}

// About
children.push(banner("About this document", "about"));
[
  "What this is: a curated catalogue of complex, currently-open freelance tasks that genuinely require Adobe Creative Cloud work and serve a clear business use case. Each entry is the actual brief — requirements, deliverables, sizes, file formats — plus the specific Adobe app(s) the work needs. These are tasks, not 'we're hiring a designer' listings.",
  "How it was built: the bulk was pulled via the official Freelancer.com API (filtered across ~46 Adobe/design skills), with additional hand-verified briefs from PeoplePerHour and Upwork. Compiled 4 June 2026.",
  "Filters applied: substantial briefs only (no thin or trivial gigs); postings from roughly the last 30 days only; tasks that clearly need Adobe tools (non-Adobe Canva/Figma/PowerPoint-only and non-design work excluded); and a business-use lean (obvious personal/hobby art excluded).",
  "How to read each task: a title bar, a meta line (platform · budget · when posted), the recommended Adobe tools and why, the full brief, and a link to the source. Budgets are shown in each client's own currency. Upwork links open the relevant Upwork search."
].forEach(t => children.push(new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 100 }, children: [new TextRun({ text: t, size: 21 })] })));

// Snapshot table
children.push(banner("Snapshot — tasks by industry"));
const bd = { style: BorderStyle.SINGLE, size: 2, color: LINE };
const borders = { top: bd, bottom: bd, left: bd, right: bd };
function cell(text, w, fill, opts) {
  opts = opts || {};
  return new TableCell({ width: { size: w, type: WidthType.DXA }, borders, shading: { type: ShadingType.CLEAR, fill },
    margins: { top: 60, bottom: 60, left: 120, right: 120 }, verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({ alignment: opts.align || AlignmentType.LEFT, children: [new TextRun({ text, bold: !!opts.bold, color: opts.color || DARK, size: opts.size || 20 })] })] });
}
const snapRows = [ new TableRow({ tableHeader: true, children: [
  cell("Industry", 7400, INK, { bold: true, color: "FFFFFF" }), cell("Tasks", 1960, INK, { bold: true, color: "FFFFFF", align: AlignmentType.CENTER }) ] }) ];
verticals.forEach((v, i) => snapRows.push(new TableRow({ children: [
  cell(v, 7400, i % 2 ? CARD : "FFFFFF", { color: INK }), cell(String(byVert[v].length), 1960, i % 2 ? CARD : "FFFFFF", { bold: true, color: ACCENT, align: AlignmentType.CENTER }) ] })));
children.push(new Table({ width: { size: 9360, type: WidthType.DXA }, columnWidths: [7400, 1960], rows: snapRows }));
children.push(new Paragraph({ spacing: { before: 160, after: 40 }, children: [
  new TextRun({ text: "Adobe tool coverage:  ", bold: true, size: 20, color: ACCENT2 }), new TextRun({ text: topTools, size: 19, color: DARK }) ] }));

// Contents
children.push(banner("Contents"));
verticals.forEach(v => children.push(new Paragraph({ spacing: { after: 40 }, children: [
  new InternalHyperlink({ anchor: slug(v), children: [new TextRun({ text: v, style: "Hyperlink", size: 22 })] }),
  new TextRun({ text: "   (" + byVert[v].length + ")", size: 20, color: GREY })] })));
children.push(new Paragraph({ children: [new PageBreak()] }));

// task card
function renderTask(t, n) {
  children.push(new Paragraph({ spacing: { before: 200, after: 40 }, keepNext: true,
    shading: { type: ShadingType.CLEAR, fill: CARD }, border: { left: { style: BorderStyle.SINGLE, size: 20, color: ACCENT, space: 8 } },
    children: [new TextRun({ text: (n ? n + ".  " : "") + t.title, bold: true, size: 24, font: "Calibri", color: INK })] }));
  children.push(new Paragraph({ spacing: { after: 50 }, keepNext: true,
    children: [new TextRun({ text: [t.platform, t.budget, t.posted].filter(Boolean).join("    ·    "), italics: true, size: 19, color: GREY })] }));
  children.push(new Paragraph({ spacing: { after: 70 }, keepNext: true, children: [
    new TextRun({ text: "Adobe tools:  ", bold: true, size: 20, color: ACCENT2 }),
    new TextRun({ text: (t.tools && t.tools.length ? t.tools.join("  ·  ") : "Adobe Creative Cloud"), bold: true, size: 20, color: ACCENT2 }),
    new TextRun({ text: t.toolsWhy ? "   —   " + t.toolsWhy.replace(/^[A-Za-z0-9 ·]+—\s*/, "") : "", size: 19, color: DARK })] }));
  children.push(new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: t.fulldesc, size: 21, color: DARK })] }));
  children.push(new Paragraph({ spacing: { after: 220 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 8 } },
    children: [new ExternalHyperlink({ link: t.url, children: [new TextRun({ text: "View the live posting", style: "Hyperlink", size: 19 })] })] }));
}
verticals.forEach((v, i) => {
  if (i > 0) children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(banner(v, slug(v)));
  children.push(new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: byVert[v].length + (byVert[v].length === 1 ? " task" : " tasks") + " in this industry", italics: true, size: 19, color: GREY })] }));
  byVert[v].forEach((t, k) => renderTask(t, k + 1));
});

const footerPara = new Paragraph({ alignment: AlignmentType.CENTER, children: [
  new TextRun({ text: "Adobe Creative Freelance Tasks   ·   compiled 4 Jun 2026   ·   page ", size: 16, color: "AAAAAA" }),
  new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "AAAAAA" }) ] });
const doc = new Document({
  styles: { default: { document: { run: { font: "Calibri", size: 22 }, paragraph: { spacing: { line: 288 } } } },
    paragraphStyles: [ { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
      run: { size: 30, bold: true, font: "Calibri", color: INK }, paragraph: { spacing: { before: 220, after: 130 }, outlineLevel: 0 } } ] },
  numbering: { config: [ { reference: "bullets", levels: [ { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 560, hanging: 280 } } } } ] } ] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    footers: { default: new Footer({ children: [footerPara] }) }, children }]
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/Adobe_Freelance_Tasks.docx", b); console.log("WROTE Adobe_Freelance_Tasks.docx (" + total + " tasks)"); });
