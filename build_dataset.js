// Extensive dataset builder: PART A = client tasks (Freelancer API, no date limit, floor 400),
// PART B = job listings (RemoteOK / Remotive / Arbeitnow / We Work Remotely). Beautiful Word output.
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat, ExternalHyperlink,
  InternalHyperlink, Bookmark, HeadingLevel, BorderStyle, PageBreak, PageNumber, Footer,
  Table, TableRow, TableCell, WidthType, ShadingType, VerticalAlign
} = require("docx");

const INK="16243F", ACCENT="C8472B", ACCENT2="9E480E", TEAL="1F6F6B", BAND="E8EDF5", CARD="F5F7FB",
      GREY="6B7280", DARK="23303F", LINE="D9DEE8";
const read = f => { try { return fs.readFileSync(f, "utf8"); } catch (e) { return ""; } };
const clean = s => (s || "").replace(/\s+/g, " ").trim();
const stripHtml = h => clean((h||"").replace(/<[^>]+>/g," ").replace(/&amp;/g,"&").replace(/&nbsp;/g," ").replace(/&#?[a-z0-9]+;/gi," "));
const normUrl = u => (u || "").toLowerCase().replace(/[#?].*$/, "").replace(/\/+$/, "");
const normTitle = t => (t || "").toLowerCase().replace(/[^a-z0-9]+/g, "");
const slug = s => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
const NOW = Date.now() / 1000;

// ---------- shared taggers ----------
function detectVertical(title, desc) {
  const t = (title + " " + desc).toLowerCase(); const any = (...k) => k.some(x => t.includes(x));
  if (any("wedding","bride","groom","save the date","bridal")) return "Wedding & Stationery";
  if (any("cannabis","dispensary"," cbd","thc","vape","smoke shop","marijuana")) return "Cannabis & Dispensary";
  if (any("skincare","skin care","cosmetic","makeup","perfume","fragrance"," salon"," spa ","serum","beauty brand","haircare","shampoo")) return "Beauty, Cosmetics & Personal Care";
  if (any(" pet ","pets ","dog ","cat ","puppy","veterinar","animal ")) return "Pets & Animals";
  if (any("restaurant","menu","food ","beverage","coffee","cafe","bakery","snack","spice","burger","pizza","brewery","wine","chocolate"," tea ","juice","catering","chef","sauce","grocery")) return "Food, Restaurant & Beverage";
  if (any("medical","health","clinic","hospital","dental","pharma","wellness","patient","doctor","supplement","nutrition","therapy","fitness","gym","healthcare")) return "Health, Wellness & Medical";
  if (any("real estate","realtor","property","construction","architect","interior design","landscap","contractor","renovation","mortgage")) return "Real Estate, Construction & Property";
  if (any("automotive","vehicle","truck","motorcycle","agricultur","farm","tractor","industrial","manufactur","machinery","solar","mining","logistics","equipment")) return "Automotive, Industrial & Agriculture";
  if (any("church","ministry","nonprofit","non-profit","charity"," ngo","foundation","mosque","temple","islamic","christian","faith","fundrais","gospel")) return "Nonprofit, Religious & Community";
  if (any("school","education","course","student","kids","children","toddler","toy ","learning","university","teacher","flashcard","e-learning","academy")) return "Education & Children";
  if (any("finance","financial","bank","investment","consult","law firm","legal","attorney","accounting","insurance","advisory"," tax ","trading","crypto","fintech","pitch deck","wealth")) return "Finance, Crypto & Professional Services";
  if (any("fashion","apparel","clothing","t-shirt","tshirt","streetwear","jersey","garment","tech pack","lookbook","textile","jewelry","jewellery","footwear","swimwear","hoodie","merch ","boutique")) return "Fashion & Apparel";
  if (any("music","album","band ","record label","book cover","novel","author","publish","magazine"," film","movie","podcast","comic","webtoon","entertainment","gaming","trailer")) return "Music, Film, Publishing & Media";
  if (any("ecommerce","e-commerce","amazon","shopify","etsy","online store","dropship","product listing","product photo")) return "E-commerce, Retail & Product";
  if (any("saas","software","startup"," app ","mobile app","platform","cyber","fintech"," ai ","tech company","b2b","dashboard","ui/ux","web app")) return "Technology, SaaS & Startups";
  if (any("motion graphic","explainer","after effects","kinetic","video edit","reel","footage","animation video","video editor")) return "Video Editing & Motion Graphics";
  if (any("retouch","photo editing","photo edit","background remov","photo restoration","color correct","image editing","prepress")) return "Photo Editing, Retouching & Restoration";
  if (any("event","party","concert","festival","gala","conference","expo","exhibition","tradeshow","trade show")) return "Party, Events & Promotion";
  return "General / Cross-Industry Branding & Graphics";
}
function deriveTools(skills, text) {
  const s = skills.map(x => x.toLowerCase()); const has = k => s.some(x => x.includes(k)) || text.toLowerCase().includes(k);
  const tools = []; const add = x => { if (!tools.includes(x)) tools.push(x); };
  if (has("photoshop")) add("Photoshop"); if (has("illustrator")) add("Illustrator"); if (has("indesign")) add("InDesign");
  if (has("after effects")) add("After Effects"); if (has("premiere")) add("Premiere Pro"); if (has("lightroom")) add("Lightroom");
  if (has("adobe xd")) add("XD"); if (has("animate")) add("Animate"); if (has("acrobat")) add("Acrobat");
  if (tools.length === 0) { const t = text.toLowerCase();
    if (/(motion graphic|after effects|explainer|kinetic|animated video)/.test(t)) add("After Effects");
    if (/(video|reel|premiere|footage)/.test(t)) add("Premiere Pro");
    if (/(retouch|photo edit|composit|background remov|restoration|color grad)/.test(t)) add("Photoshop");
    if (/(brochure|catalog|magazine|booklet|multi-?page|annual report|ebook|layout|book )/.test(t)) add("InDesign");
    if (/(logo|vector|\.ai|\.eps|svg|brand|illustration)/.test(t)) add("Illustrator");
    if (tools.length === 0) { add("Photoshop"); add("Illustrator"); } }
  return tools.slice(0, 3);
}
function whyFor(tools, text) {
  const t = text.toLowerCase(), c = [];
  if (/(print-ready|cmyk|300\s?dpi|bleed|press-ready|offset)/.test(t)) c.push("print-ready CMYK output");
  if (/(vector|\.ai\b|\.eps|svg|scalable|logo)/.test(t)) c.push("scalable vector artwork");
  if (/(\.psd|layered|retouch|composit|mockup|photo)/.test(t)) c.push("layered/retouched assets");
  if (/(multi-?page|brochure|catalog|magazine|booklet|annual report|layout)/.test(t)) c.push("multi-page layout");
  if (/(video|reel|motion|footage|animation|explainer)/.test(t)) c.push("video/motion editing");
  return tools.join("  ·  ") + (c.length ? "  —  for " + c.slice(0, 2).join(" and ") : "");
}
function budgetStr(p) {
  const cu = p.currency || {}, code = cu.code || "", sg = cu.sign || ""; const b = p.budget || {};
  const f = n => (n == null ? "" : (n % 1 === 0 ? String(n) : String(Math.round(n))));
  let s = "See posting";
  if (b.minimum != null && b.maximum != null) s = `${sg}${f(b.minimum)}–${sg}${f(b.maximum)} ${code}`;
  else if (b.minimum != null) s = `${sg}${f(b.minimum)}+ ${code}`;
  if ((p.type || "") === "hourly") s += " /hr";
  return s.trim();
}

// ---------- PART A: tasks ----------
const ADOBE_SKILL_RX = /(photoshop|illustrator|indesign|after effects|premiere|lightroom|adobe)/i;
const ADOBE_RX = /(photoshop|illustrator|indesign|after effects|premiere|lightroom|adobe |\.psd|\.ai\b|\.indd|\.eps|graphic design|logo|vector|brand|brochure|packaging|flyer|poster|retouch|illustration|motion graphic)/i;
const TRIVIAL_RX = /(data entry|copy[- ]?paste|typing|pdf to word|captcha|survey|virtual assistant|lead generation|web scrap|wordpress install|website development|app development|mobile app develop|bookkeep|data mining)/i;
const PERSONAL_RX = /(fan ?art|\bd&d\b|\bdnd\b|dungeons|tattoo|cosplay|my girlfriend|my boyfriend|gift for my|portrait of my|anime oc\b)/i;
const BIZ_RX = /(brand|company|business|product|packaging|logo|market|client|commercial|store|startup|firm|corporate|launch|campaign|brochure|catalog|label|menu|signage|ecommerce|e-commerce|b2b|professional|agency|retail|wholesale|customer|saas)/i;

let TASKS = []; const tIds = new Set();
for (const dir of ["/tmp/flp", "/tmp/flp2", "/tmp/flp3"]) {
  let files = []; try { files = fs.readdirSync(dir).filter(f => f.endsWith(".json")).map(f => dir + "/" + f); } catch (e) {}
  for (const fp of files) {
    let d; try { d = JSON.parse(read(fp)); } catch (e) { continue; }
    for (const p of ((d.result || {}).projects || [])) {
      if (tIds.has(p.id)) continue; tIds.add(p.id);
      const desc = clean(p.description); if (desc.length < 400) continue;
      const skills = (p.jobs || []).map(j => j.name).filter(Boolean); const blob = p.title + " " + desc;
      if (TRIVIAL_RX.test(blob)) continue;
      if (PERSONAL_RX.test(blob) && !BIZ_RX.test(blob)) continue;
      if (!skills.some(x => ADOBE_SKILL_RX.test(x)) && !ADOBE_RX.test(desc)) continue;
      const days = p.submitdate ? Math.max(0, Math.round((NOW - p.submitdate) / 86400)) : null;
      const tools = deriveTools(skills, desc);
      const cues = (desc.match(/(deliverable|print-ready|vector|mockup|cmyk|bleed|\.ai|\.psd|\.eps|source file|editable|dimensions|pantone|revision|format|guidelines|3d)/gi) || []).length;
      TASKS.push({ title: clean(p.title), vertical: detectVertical(p.title, desc), platform: "Freelancer.com",
        budget: budgetStr(p), posted: days == null ? "Active" : (days === 0 ? "Posted today" : "Posted " + days + (days === 1 ? " day ago" : " days ago")),
        url: "https://www.freelancer.com/projects/" + (p.seo_url || ""), tools, toolsWhy: whyFor(tools, desc), fulldesc: desc,
        _score: desc.length + 150 * tools.length + 220 * cues + (BIZ_RX.test(blob) ? 500 : 0) });
    }
  }
}
// verified hand-checked tasks
let EX = [];
for (const f of ["tasks_b1.js","tasks_b2.js","tasks_b3.js","tasks_b4.js","tasks_b5.js","tasks_b6.js","tasks_upwork.js","tasks_upwork2.js"]) { try { EX = EX.concat(require("./" + f)); } catch (e) {} }
const seenU = new Set(), seenT = new Set();
const allTasks = [];
const pushT = t => { const u = normUrl(t.url), n = normTitle(t.title); if (seenU.has(u) || seenT.has(n)) return; seenU.add(u); seenT.add(n); allTasks.push(t); };
EX.filter(t => clean(t.fulldesc).length >= 400).forEach(pushT);
TASKS.sort((a, b) => b._score - a._score).forEach(pushT);

// ---------- PART B: job listings ----------
const ADX = /(photoshop|illustrator|indesign|after effects|premiere|lightroom|adobe|graphic design|motion design|motion graphic|art director|brand design|branding|creative design|visual design|ui\/?ux|ui design|product design|video edit|3d design|web design)/i;
function listingTools(text) {
  const t = text.toLowerCase(), out = [];
  [["photoshop","Photoshop"],["illustrator","Illustrator"],["indesign","InDesign"],["after effects","After Effects"],["premiere","Premiere Pro"],["lightroom","Lightroom"],["adobe xd","XD"]].forEach(([k,v]) => { if (t.includes(k) && !out.includes(v)) out.push(v); });
  if (out.length === 0) { if (/motion|after effects|video|animation/.test(t)) { out.push("After Effects","Premiere Pro"); } else { out.push("Photoshop","Illustrator"); } if (/layout|brochure|magazine|editorial|publication/.test(t)) out.push("InDesign"); }
  return out.slice(0, 3);
}
let LISTINGS = []; const lSeen = new Set();
const pushL = l => { const u = normUrl(l.url); if (!l.url || lSeen.has(u)) return; lSeen.add(u); LISTINGS.push(l); };
try { (JSON.parse(read("/tmp/jobs/remoteok.json") || "[]")).forEach(j => { if (!j || !j.position) return; const blob = j.position + " " + (j.tags||[]).join(" ") + " " + (j.description||""); if (!ADX.test(blob)) return;
  pushL({ source:"RemoteOK", title:j.position, company:j.company||"", location:j.location||"Remote", salary:j.salary_min?("$"+j.salary_min+(j.salary_max?"–$"+j.salary_max:"")):"", type:"", url:j.url||("https://remoteok.com/l/"+j.id), tools:listingTools(blob), desc:stripHtml(j.description).slice(0,950) }); }); } catch (e) {}
try { ((JSON.parse(read("/tmp/jobs/remotive.json")||"{}")).jobs||[]).forEach(j => { const blob=j.title+" "+(j.tags||[]).join(" ")+" "+(j.description||"");
  pushL({ source:"Remotive", title:j.title, company:j.company_name||"", location:j.candidate_required_location||"Remote", salary:j.salary||"", type:j.job_type||"", url:j.url, tools:listingTools(blob), desc:stripHtml(j.description).slice(0,950) }); }); } catch (e) {}
try { fs.readdirSync("/tmp/jobs").filter(f => f.startsWith("arbeitnow")).forEach(f => { ((JSON.parse(read("/tmp/jobs/"+f)||"{}")).data||[]).forEach(j => { const blob=j.title+" "+(j.tags||[]).join(" ")+" "+(j.description||""); if (!ADX.test(blob)) return;
  pushL({ source:"Arbeitnow", title:j.title, company:j.company_name||"", location:j.location||"", salary:"", type:(j.job_types||[]).join(", "), url:j.url, tools:listingTools(blob), desc:stripHtml(j.description).slice(0,950) }); }); }); } catch (e) {}
try { const rss = read("/tmp/jobs/wwr.rss"); (rss.match(/<item>[\s\S]*?<\/item>/g)||[]).forEach(it => { const g=(re)=>{ const m=it.match(re); return m?clean(m[1]):""; };
  const title=g(/<title>(?:<!\[CDATA\[)?([\s\S]*?)(?:\]\]>)?<\/title>/), link=g(/<link>([\s\S]*?)<\/link>/), desc=stripHtml(g(/<description>(?:<!\[CDATA\[)?([\s\S]*?)(?:\]\]>)?<\/description>/)), region=g(/<region>([\s\S]*?)<\/region>/);
  if (!title || !link) return; let company="", role=title; const ci=title.indexOf(":"); if (ci>0){ company=title.slice(0,ci).trim(); role=title.slice(ci+1).trim(); }
  pushL({ source:"We Work Remotely", title:role, company, location:region||"Remote", salary:"", type:"", url:link, tools:listingTools(title+" "+desc), desc:desc.slice(0,950) }); }); } catch (e) {}

// ---------- group ----------
const VERT_ORDER = ["Fashion & Apparel","Beauty, Cosmetics & Personal Care","Food, Restaurant & Beverage","Wedding & Stationery","Party, Events & Promotion","Health, Wellness & Medical","Real Estate, Construction & Property","Automotive, Industrial & Agriculture","Technology, SaaS & Startups","E-commerce, Retail & Product","Cannabis & Dispensary","Music, Film, Publishing & Media","Video Editing & Motion Graphics","Photo Editing, Retouching & Restoration","Pets & Animals","Education & Children","Nonprofit, Religious & Community","Finance, Crypto & Professional Services","General / Cross-Industry Branding & Graphics"];
const byVert = {}; allTasks.forEach(t => (byVert[t.vertical] = byVert[t.vertical] || []).push(t));
Object.values(byVert).forEach(a => a.sort((x, y) => (y._score||0) - (x._score||0)));
const verticals = [...VERT_ORDER.filter(v => byVert[v]), ...Object.keys(byVert).filter(v => !VERT_ORDER.includes(v))];
const bySrc = {}; LISTINGS.forEach(l => (bySrc[l.source] = bySrc[l.source] || []).push(l));
const sources = Object.keys(bySrc).sort((a, b) => bySrc[b].length - bySrc[a].length);
const toolCount = {}; allTasks.forEach(t => (t.tools||[]).forEach(x => toolCount[x] = (toolCount[x]||0)+1));
const topTools = Object.entries(toolCount).sort((a,b)=>b[1]-a[1]).map(([k,v])=>k+" ("+v+")").join("   ·   ");
console.log("TASKS:", allTasks.length, "| industries:", verticals.length, "| LISTINGS:", LISTINGS.length, "from", sources.length, "sources");

// ---------- render ----------
const children = [];
function banner(text, id, fill, bar) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 200, after: 140 },
    shading: { type: ShadingType.CLEAR, fill: fill || BAND },
    border: { left: { style: BorderStyle.SINGLE, size: 26, color: bar || ACCENT, space: 8 }, bottom: { style: BorderStyle.SINGLE, size: 6, color: INK, space: 4 } },
    children: [id ? new Bookmark({ id, children: [new TextRun(text)] }) : new TextRun(text)] });
}
function partDivider(label, sub) {
  children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 2400, after: 60 }, shading: { type: ShadingType.CLEAR, fill: INK },
    children: [new TextRun({ text: "  " + label + "  ", bold: true, size: 44, color: "FFFFFF", font: "Calibri" })] }));
  children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [new TextRun({ text: sub, size: 24, color: ACCENT, italics: true })] }));
}
// Cover
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 1400, after: 0 }, shading: { type: ShadingType.CLEAR, fill: INK },
  children: [new TextRun({ text: "  Adobe Freelance Tasks & Jobs — Master Dataset  ", bold: true, size: 46, font: "Calibri", color: "FFFFFF" })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 160, after: 40 }, children: [new TextRun({ text: "An extensive catalogue of Adobe-related freelance tasks and job listings from across the web", size: 25, color: DARK })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 30 }, children: [new TextRun({ text: "Part A — client tasks  ·  Part B — employer job listings", size: 22, color: ACCENT, italics: true })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 320 }, children: [new TextRun({ text: "Compiled 4 June 2026", size: 20, color: GREY })] }));
[[allTasks.length + " client tasks", "real freelance briefs that require Adobe tools, grouped by industry"],
 [LISTINGS.length + " job listings", "employer design roles from RemoteOK, Remotive, Arbeitnow & We Work Remotely"],
 [verticals.length + " industries", "fashion, food, healthcare, real estate, film, finance, cannabis & more"],
 ["Source + link on every entry", "Freelancer.com API · PeoplePerHour · Upwork · remote job boards"]].forEach(g =>
  children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 70 }, children: [new TextRun({ text: g[0] + "   —   ", bold: true, size: 23, color: ACCENT }), new TextRun({ text: g[1], size: 20, color: DARK })] })));
children.push(new Paragraph({ children: [new PageBreak()] }));

// About
children.push(banner("About this dataset", "about"));
["What this is: an extensive, structured catalogue of Adobe-related freelance work from across the web. Part A lists client tasks (real freelance briefs that need Adobe Creative Cloud work); Part B lists job listings (employer roles hiring for Adobe/design skills). Every entry shows its source, a working link, the Adobe skills needed, and the full description.",
 "How it was built: the task bulk came via the official Freelancer.com API (across ~49 Adobe/design skills, no date cap), with hand-verified briefs from PeoplePerHour and Upwork. Job listings came from public job-board APIs — RemoteOK, Remotive, Arbeitnow — plus the We Work Remotely feed. Compiled 4 June 2026.",
 "Filters: substantial entries only (thin/trivial gigs and pure data-entry excluded), tasks that genuinely involve Adobe/design work, and obvious personal-hobby art removed. Tasks are ordered most-detailed-first within each industry.",
 "Reading each entry: a title bar, a meta line (source · budget/salary · location · posted), the Adobe tools needed, the full description, and a source link. Budgets/salaries appear in each posting's own currency where available."].forEach(t =>
  children.push(new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 100 }, children: [new TextRun({ text: t, size: 21 })] })));

// Snapshot
children.push(banner("Snapshot"));
const bd = { style: BorderStyle.SINGLE, size: 2, color: LINE }, borders = { top: bd, bottom: bd, left: bd, right: bd };
function cell(text, w, fill, o) { o = o || {}; return new TableCell({ width: { size: w, type: WidthType.DXA }, borders, shading: { type: ShadingType.CLEAR, fill }, margins: { top: 50, bottom: 50, left: 120, right: 120 }, verticalAlign: VerticalAlign.CENTER, children: [new Paragraph({ alignment: o.align || AlignmentType.LEFT, children: [new TextRun({ text, bold: !!o.bold, color: o.color || DARK, size: o.size || 20 })] })] }); }
const snap = [new TableRow({ tableHeader: true, children: [cell("Industry (Part A — tasks)", 7400, INK, { bold: true, color: "FFFFFF" }), cell("Count", 1960, INK, { bold: true, color: "FFFFFF", align: AlignmentType.CENTER })] })];
verticals.forEach((v, i) => snap.push(new TableRow({ children: [cell(v, 7400, i % 2 ? CARD : "FFFFFF", { color: INK }), cell(String(byVert[v].length), 1960, i % 2 ? CARD : "FFFFFF", { bold: true, color: ACCENT, align: AlignmentType.CENTER })] })));
snap.push(new TableRow({ children: [cell("Job listings (Part B — by source: " + sources.map(s => s + " " + bySrc[s].length).join(", ") + ")", 7400, "EEF3EE", { color: TEAL }), cell(String(LISTINGS.length), 1960, "EEF3EE", { bold: true, color: TEAL, align: AlignmentType.CENTER })] }));
children.push(new Table({ width: { size: 9360, type: WidthType.DXA }, columnWidths: [7400, 1960], rows: snap }));
children.push(new Paragraph({ spacing: { before: 160, after: 40 }, children: [new TextRun({ text: "Adobe tool coverage (tasks):  ", bold: true, size: 20, color: ACCENT2 }), new TextRun({ text: topTools, size: 19, color: DARK })] }));

// Contents
children.push(banner("Contents"));
children.push(new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "PART A — CLIENT TASKS", bold: true, size: 22, color: INK })] }));
verticals.forEach(v => children.push(new Paragraph({ spacing: { after: 36 }, children: [new InternalHyperlink({ anchor: slug("t-" + v), children: [new TextRun({ text: "   " + v, style: "Hyperlink", size: 21 })] }), new TextRun({ text: "   (" + byVert[v].length + ")", size: 19, color: GREY })] })));
children.push(new Paragraph({ spacing: { before: 120, after: 60 }, children: [new TextRun({ text: "PART B — JOB LISTINGS", bold: true, size: 22, color: TEAL })] }));
sources.forEach(s => children.push(new Paragraph({ spacing: { after: 36 }, children: [new InternalHyperlink({ anchor: slug("l-" + s), children: [new TextRun({ text: "   " + s, style: "Hyperlink", size: 21 })] }), new TextRun({ text: "   (" + bySrc[s].length + ")", size: 19, color: GREY })] })));

// PART A
partDivider("PART A", allTasks.length + " client tasks across " + verticals.length + " industries");
function renderTask(t, n) {
  children.push(new Paragraph({ spacing: { before: 200, after: 40 }, keepNext: true, shading: { type: ShadingType.CLEAR, fill: CARD }, border: { left: { style: BorderStyle.SINGLE, size: 20, color: ACCENT, space: 8 } },
    children: [new TextRun({ text: (n ? n + ".  " : "") + t.title, bold: true, size: 24, font: "Calibri", color: INK })] }));
  children.push(new Paragraph({ spacing: { after: 50 }, keepNext: true, children: [new TextRun({ text: [t.platform, t.budget, t.posted].filter(Boolean).join("    ·    "), italics: true, size: 19, color: GREY })] }));
  children.push(new Paragraph({ spacing: { after: 70 }, keepNext: true, children: [new TextRun({ text: "Adobe tools:  ", bold: true, size: 20, color: ACCENT2 }), new TextRun({ text: (t.tools && t.tools.length ? t.tools.join("  ·  ") : "Adobe Creative Cloud"), bold: true, size: 20, color: ACCENT2 }), new TextRun({ text: t.toolsWhy ? "   —   " + t.toolsWhy.replace(/^[A-Za-z0-9 ·]+—\s*/, "") : "", size: 19, color: DARK })] }));
  children.push(new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: t.fulldesc, size: 21, color: DARK })] }));
  children.push(new Paragraph({ spacing: { after: 220 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 8 } }, children: [new ExternalHyperlink({ link: t.url, children: [new TextRun({ text: "View the live posting", style: "Hyperlink", size: 19 })] })] }));
}
verticals.forEach((v, i) => { if (i > 0) children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(banner(v, slug("t-" + v)));
  children.push(new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: byVert[v].length + (byVert[v].length === 1 ? " task" : " tasks") + " in this industry", italics: true, size: 19, color: GREY })] }));
  byVert[v].forEach((t, k) => renderTask(t, k + 1)); });

// PART B
partDivider("PART B", LISTINGS.length + " employer job listings (Adobe / design roles)");
function renderListing(l, n) {
  children.push(new Paragraph({ spacing: { before: 200, after: 40 }, keepNext: true, shading: { type: ShadingType.CLEAR, fill: "EEF3EE" }, border: { left: { style: BorderStyle.SINGLE, size: 20, color: TEAL, space: 8 } },
    children: [new TextRun({ text: (n ? n + ".  " : "") + l.title + (l.company ? "  —  " + l.company : ""), bold: true, size: 24, font: "Calibri", color: INK })] }));
  children.push(new Paragraph({ spacing: { after: 50 }, keepNext: true, children: [new TextRun({ text: [l.source, l.location, l.salary, l.type].filter(Boolean).join("    ·    "), italics: true, size: 19, color: GREY })] }));
  children.push(new Paragraph({ spacing: { after: 70 }, keepNext: true, children: [new TextRun({ text: "Adobe / design skills:  ", bold: true, size: 20, color: TEAL }), new TextRun({ text: (l.tools && l.tools.length ? l.tools.join("  ·  ") : "Adobe Creative Suite"), bold: true, size: 20, color: TEAL })] }));
  if (l.desc) children.push(new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: l.desc + (l.desc.length >= 940 ? " …" : ""), size: 21, color: DARK })] }));
  children.push(new Paragraph({ spacing: { after: 220 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 8 } }, children: [new ExternalHyperlink({ link: l.url, children: [new TextRun({ text: "View the listing", style: "Hyperlink", size: 19 })] })] }));
}
sources.forEach((s, i) => { if (i > 0) children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(banner(s, slug("l-" + s), "EEF3EE", TEAL));
  children.push(new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: bySrc[s].length + " listings from " + s, italics: true, size: 19, color: GREY })] }));
  bySrc[s].forEach((l, k) => renderListing(l, k + 1)); });

const footerPara = new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Adobe Freelance Tasks & Jobs — Master Dataset   ·   compiled 4 Jun 2026   ·   page ", size: 16, color: "AAAAAA" }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "AAAAAA" })] });
const doc = new Document({
  styles: { default: { document: { run: { font: "Calibri", size: 22 }, paragraph: { spacing: { line: 288 } } } },
    paragraphStyles: [{ id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 30, bold: true, font: "Calibri", color: INK }, paragraph: { spacing: { before: 220, after: 130 }, outlineLevel: 0 } }] },
  numbering: { config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 560, hanging: 280 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } }, footers: { default: new Footer({ children: [footerPara] }) }, children }]
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/Adobe_Tasks_and_Jobs_Master.docx", b); console.log("WROTE Adobe_Tasks_and_Jobs_Master.docx —", allTasks.length, "tasks +", LISTINGS.length, "listings"); });
