"""Remove ONLY clearly non-Adobe tasks (per user's 'remove clear non-Adobe only' choice).
A task is removed iff it hits a HARD non-Adobe signal (pure software dev / 3D-CAD-game /
non-design admin role) AND contains NO design/Adobe vocabulary at all. Any hybrid that
mentions design (web design, UX/UI, pitch deck, animation, logo, photo, etc.) is KEPT as
borderline. Prints every removed row for transparency."""
import sys, re
sys.path.insert(0, "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/pipeline")
from adobe_pipeline import db

conn = db.connect("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/pipeline/data/adobe.db")

# --- HARD non-Adobe signals (the job is fundamentally not Adobe work) ---
DEV = re.compile(r"(react[\s-]?native|\bnext\.?js\b|\bios developer\b|android developer|full[\s-]?stack|back-?end developer|front-?end developer|\bweb developer\b|website develop|web development|woocommerce developer|wordpress developer|software engineer|\bapi developer\b|\bflutter\b|llc registration website|web design dev team|website build\b|site creation|website for |website redesign/update)", re.I)
THREED = re.compile(r"(blender|\bmaya\b|3ds max|cinema 4d|zbrush|character creator|\bcc5\b|arkit|blendshape|unreal engine|\bunity\b|3d/cad|cad jewel|\b3d modeling|narrative game design|car designer for luxury)", re.I)
ROLE = re.compile(r"(customer support|sales & customer|sales representative|\bproofread|reverse recruiter|mechanical engineer|\bhvac\b|financial model|capital planning|project manager-|legal agreement|book marketing|amazon book|large language model|write a book for beginners|numeracy assessment|assessment expert|ai course content|course content creation|social media management|virtual assistant|data entry|lead generation|appointment setter|telemarket|bookkeep|\baccountant\b|transcription|voice ?over|content writer\b|copywriting only)", re.I)

# --- DESIGN / Adobe vocabulary guard: if ANY of these appear, KEEP (it's design work) ---
DESIGN = re.compile(r"(logo|illustrat|photoshop|illustrator|indesign|after effects|premiere|lightroom|\bphoto\b|retouch|packaging|brochure|flyer|poster|banner|graphic design|\bbrand|visual identity|\bvector\b|typograph|infographic|book cover|magazine|catalog|catalogue|signage|menu design|sticker|business card|thumbnail|album cover|\bui/?ux\b|\bux/?ui\b|web design|web designer|website design|website designer|landing page|pitch deck|presentation design|animation|animate|motion|video edit|\bgraphic|t-?shirt|apparel|\blabel\b|vehicle wrap|greeting card|invitation|mockup|character design|cover art|creative design|art direct|caricature|cartoon|comic|portrait|wedding|social media (design|graphic|post|creative)|ad creative|ad design|advertis)", re.I)

rows = list(conn.execute("SELECT id, source, title, description FROM items WHERE kind='task'"))
remove = []
for i, s, t, d in rows:
    txt = (t or "") + " " + (d or "")
    if DESIGN.search(txt):
        continue  # has design vocabulary -> keep (borderline or clearly Adobe)
    if DEV.search(txt) or THREED.search(txt) or ROLE.search(txt):
        remove.append((i, s, t))

print("WILL REMOVE %d clearly-non-Adobe tasks:\n" % len(remove))
for i, s, t in remove:
    print(f"  #{i} [{s}] {t}")

for i, _, _ in remove:
    conn.execute("DELETE FROM items WHERE id=?", (i,))
conn.commit()

print("\n--- after pruning ---")
tot = 0
for s, c in conn.execute("SELECT source, COUNT(*) FROM items WHERE kind='task' GROUP BY source ORDER BY COUNT(*) DESC"):
    print(f"  {s:14s} {c}"); tot += c
print(f"  {'TOTAL':14s} {tot}")
