"""Common-schema normalization: industry detection, Adobe-tool derivation, relevance filters."""
import re

ADOBE_SKILL_RX = re.compile(r"(photoshop|illustrator|indesign|after effects|premiere|lightroom|adobe)", re.I)
ADOBE_RX = re.compile(r"(photoshop|illustrator|indesign|after effects|premiere|lightroom|adobe |\.psd|\.ai\b|\.indd|\.eps|graphic design|logo|vector|brand|brochure|packaging|flyer|poster|retouch|illustration|motion graphic)", re.I)
ADX = re.compile(r"(photoshop|illustrator|indesign|after effects|premiere|lightroom|adobe|graphic design|motion design|motion graphic|art director|brand design|branding|creative design|visual design|ui/?ux|ui design|product design|video edit|3d design|web design)", re.I)
TRIVIAL_RX = re.compile(r"(data entry|copy[- ]?paste|typing|pdf to word|captcha|survey|virtual assistant|lead generation|web scrap|wordpress install|website development|app development|mobile app develop|bookkeep|data mining)", re.I)
PERSONAL_RX = re.compile(r"(fan ?art|\bd&d\b|\bdnd\b|dungeons|tattoo|cosplay|my girlfriend|my boyfriend|gift for my|portrait of my|anime oc\b)", re.I)
BIZ_RX = re.compile(r"(brand|company|business|product|packaging|logo|market|client|commercial|store|startup|firm|corporate|launch|campaign|brochure|catalog|label|menu|signage|ecommerce|e-commerce|b2b|professional|agency|retail|wholesale|customer|saas)", re.I)

_VERTICALS = [
    ("Wedding & Stationery", ["wedding", "bride", "groom", "save the date", "bridal"]),
    ("Cannabis & Dispensary", ["cannabis", "dispensary", " cbd", "thc", "vape", "smoke shop", "marijuana"]),
    ("Beauty, Cosmetics & Personal Care", ["skincare", "skin care", "cosmetic", "makeup", "perfume", "fragrance", " salon", " spa ", "serum", "beauty brand", "haircare", "shampoo"]),
    ("Pets & Animals", [" pet ", "pets ", "dog ", "cat ", "puppy", "veterinar", "animal "]),
    ("Food, Restaurant & Beverage", ["restaurant", "menu", "food ", "beverage", "coffee", "cafe", "bakery", "snack", "spice", "burger", "pizza", "brewery", "wine", "chocolate", " tea ", "juice", "catering", "chef", "sauce", "grocery"]),
    ("Health, Wellness & Medical", ["medical", "health", "clinic", "hospital", "dental", "pharma", "wellness", "patient", "doctor", "supplement", "nutrition", "therapy", "fitness", "gym", "healthcare"]),
    ("Real Estate, Construction & Property", ["real estate", "realtor", "property", "construction", "architect", "interior design", "landscap", "contractor", "renovation", "mortgage"]),
    ("Automotive, Industrial & Agriculture", ["automotive", "vehicle", "truck", "motorcycle", "agricultur", "farm", "tractor", "industrial", "manufactur", "machinery", "solar", "mining", "logistics", "equipment"]),
    ("Nonprofit, Religious & Community", ["church", "ministry", "nonprofit", "non-profit", "charity", " ngo", "foundation", "mosque", "temple", "islamic", "christian", "faith", "fundrais", "gospel"]),
    ("Education & Children", ["school", "education", "course", "student", "kids", "children", "toddler", "toy ", "learning", "university", "teacher", "flashcard", "e-learning", "academy"]),
    ("Finance, Crypto & Professional Services", ["finance", "financial", "bank", "investment", "consult", "law firm", "legal", "attorney", "accounting", "insurance", "advisory", " tax ", "trading", "crypto", "fintech", "pitch deck", "wealth"]),
    ("Fashion & Apparel", ["fashion", "apparel", "clothing", "t-shirt", "tshirt", "streetwear", "jersey", "garment", "tech pack", "lookbook", "textile", "jewelry", "jewellery", "footwear", "swimwear", "hoodie", "merch ", "boutique"]),
    ("Music, Film, Publishing & Media", ["music", "album", "band ", "record label", "book cover", "novel", "author", "publish", "magazine", " film", "movie", "podcast", "comic", "webtoon", "entertainment", "gaming", "trailer"]),
    ("E-commerce, Retail & Product", ["ecommerce", "e-commerce", "amazon", "shopify", "etsy", "online store", "dropship", "product listing", "product photo"]),
    ("Technology, SaaS & Startups", ["saas", "software", "startup", " app ", "mobile app", "platform", "cyber", "fintech", " ai ", "tech company", "b2b", "dashboard", "ui/ux", "web app"]),
    ("Video Editing & Motion Graphics", ["motion graphic", "explainer", "after effects", "kinetic", "video edit", "reel", "footage", "animation video", "video editor"]),
    ("Photo Editing, Retouching & Restoration", ["retouch", "photo editing", "photo edit", "background remov", "photo restoration", "color correct", "image editing", "prepress"]),
    ("Party, Events & Promotion", ["event", "party", "concert", "festival", "gala", "conference", "expo", "exhibition", "tradeshow", "trade show"]),
]


def detect_vertical(title, desc):
    t = ((title or "") + " " + (desc or "")).lower()
    for name, kws in _VERTICALS:
        if any(k in t for k in kws):
            return name
    return "General / Cross-Industry Branding & Graphics"


def strip_html(h):
    if not h:
        return ""
    h = re.sub(r"<[^>]+>", " ", h)
    h = h.replace("&amp;", "&").replace("&nbsp;", " ")
    h = re.sub(r"&#?[a-z0-9]+;", " ", h, flags=re.I)
    return re.sub(r"\s+", " ", h).strip()


def derive_tools(skills, text):
    s = " ".join(skills).lower() + " " + (text or "").lower()
    out = []
    for key, name in [("photoshop", "Photoshop"), ("illustrator", "Illustrator"), ("indesign", "InDesign"),
                      ("after effects", "After Effects"), ("premiere", "Premiere Pro"),
                      ("lightroom", "Lightroom"), ("adobe xd", "XD"), ("animate", "Animate"), ("acrobat", "Acrobat")]:
        if key in s and name not in out:
            out.append(name)
    if not out:
        t = (text or "").lower()
        if re.search(r"(motion graphic|after effects|explainer|kinetic|animated video)", t):
            out.append("After Effects")
        if re.search(r"(video|reel|premiere|footage)", t):
            out.append("Premiere Pro")
        if re.search(r"(retouch|photo edit|composit|background remov|restoration|color grad)", t):
            out.append("Photoshop")
        if re.search(r"(brochure|catalog|magazine|booklet|multi-?page|annual report|ebook|layout|book )", t):
            out.append("InDesign")
        if re.search(r"(logo|vector|\.ai|\.eps|svg|brand|illustration)", t):
            out.append("Illustrator")
        if not out:
            out = ["Photoshop", "Illustrator"]
    return out[:3]


def tools_why(tools, text):
    t = (text or "").lower()
    cues = []
    if re.search(r"(print-ready|cmyk|300\s?dpi|bleed|press-ready|offset)", t):
        cues.append("print-ready CMYK output")
    if re.search(r"(vector|\.ai\b|\.eps|svg|scalable|logo)", t):
        cues.append("scalable vector artwork")
    if re.search(r"(\.psd|layered|retouch|composit|mockup|photo)", t):
        cues.append("layered/retouched assets")
    if re.search(r"(multi-?page|brochure|catalog|magazine|booklet|annual report|layout)", t):
        cues.append("multi-page layout")
    if re.search(r"(video|reel|motion|footage|animation|explainer)", t):
        cues.append("video/motion editing")
    base = "  ·  ".join(tools)
    return base + ("  —  for " + " and ".join(cues[:2]) if cues else "")


def is_task_relevant(skills, title, desc, filters):
    blob = (title or "") + " " + (desc or "")
    if filters.get("exclude_trivial") and TRIVIAL_RX.search(blob):
        return False
    if filters.get("exclude_personal") and PERSONAL_RX.search(blob) and not BIZ_RX.search(blob):
        return False
    if filters.get("require_adobe") and not (any(ADOBE_SKILL_RX.search(s) for s in skills) or ADOBE_RX.search(desc or "")):
        return False
    if len(desc or "") < filters.get("min_description_chars", 0):
        return False
    return True


def is_listing_relevant(title, tags, desc, filters):
    blob = (title or "") + " " + " ".join(tags or []) + " " + (desc or "")
    if not ADX.search(blob):
        return False
    if len(strip_html(desc) or "") < filters.get("min_listing_chars", 0):
        return False
    return True


def budget_str_freelancer(p):
    cu = p.get("currency") or {}
    code, sign = cu.get("code", ""), cu.get("sign", "")
    b = p.get("budget") or {}
    lo, hi = b.get("minimum"), b.get("maximum")

    def f(n):
        if n is None:
            return ""
        return str(int(n)) if float(n).is_integer() else str(round(n))

    if lo is not None and hi is not None:
        s = "%s%s–%s%s %s" % (sign, f(lo), sign, f(hi), code)
    elif lo is not None:
        s = "%s%s+ %s" % (sign, f(lo), code)
    else:
        s = "See posting"
    if (p.get("type") or "") == "hourly":
        s += " /hr"
    return s.strip()
