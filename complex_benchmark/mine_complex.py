#!/usr/bin/env python3
"""Mine the DB for tasks whose CORRECT execution demands a wide mix of advanced
Adobe connector tools we have never used. Scores by advanced-tool-family diversity
+ brief specificity. Scans both adobe_doable_full.json and the broader clean DB."""
import json, re, sqlite3, sys
from collections import Counter, defaultdict

ROOT = "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads"

# ---- the full connector universe (from adobe_mandatory_init doc) ----
USED = {"image_remove_background", "image_apply_auto_tone", "image_vectorize",
        "image_crop_and_resize", "image_adjust_color_temperature",
        "image_adjust_vibrance_and_saturation", "image_generative_expand",
        "document_convert_pdf"}  # convert was local-assembled but count it touched

# advanced tool FAMILIES we have never meaningfully used -> the tools they map to.
# each family: (weight, [signal regexes], [connector tools it would invoke])
FAMILIES = {
 "masking_selective": (5, [
    r"\bbackground blur", r"\bblur(?:red)? (?:the )?background", r"\bbokeh", r"depth of field",
    r"make (?:the |my )?\w+ pop", r"\bmake .{0,20}stand out", r"\bisolate the (?:subject|product)",
    r"\bselective", r"\bbrighten (?:the |just the )?(?:subject|face|product)",
    r"\bdarken (?:the )?background", r"keep .{0,20}in focus", r"\bcut ?out and",
    r"\bmask", r"only the (?:sky|background|subject|product|car|dress)",
   ], ["image_select_subject", "image_select_by_prompt", "image_invert_selection",
       "image_apply_lens_blur", "image_apply_gaussian_blur"]),
 "selective_color": (5, [
    r"selective colou?r", r"splash of colou?r", r"pop of colou?r", r"black and white except",
    r"colou?r splash", r"keep (?:only )?the \w+ (?:red|blue|green|yellow|in colou?r)",
    r"desaturat", r"single colou?r",
   ], ["image_select_by_prompt", "image_adjust_single_color_saturation",
       "image_adjust_hsl", "image_invert_selection"]),
 "duotone_tint": (4, [
    r"duotone", r"two-tone", r"monochromatic", r"colou?r overlay", r"brand[- ]?colou?r wash",
    r"tinted", r"spotify[- ]?style", r"\bmonochrome\b",
   ], ["image_apply_monochromatic_tint", "image_apply_color_overlay"]),
 "halftone_print_fx": (4, [
    r"halftone", r"pop[- ]?art", r"comic", r"newspaper print", r"dot pattern", r"risograph",
    r"screen[- ]?print", r"ben[- ]?day",
   ], ["image_apply_halftone", "image_vectorize"]),
 "glitch_fx": (4, [
    r"glitch", r"vaporwave", r"cyberpunk", r"vhs", r"datamosh", r"distort(?:ed|ion)? effect",
   ], ["image_apply_glitch_effect"]),
 "grain_texture": (3, [
    r"film grain", r"\bgrain\b", r"analog(?:ue)? (?:look|film)", r"vintage film", r"35mm look",
    r"add (?:texture|noise)", r"\bnoise\b", r"matte film",
   ], ["image_add_grain", "image_add_noise"]),
 "preset_batch": (4, [
    r"lightroom preset", r"\bpreset", r"consistent (?:edit|look|style|grade)",
    r"same (?:look|edit|style|filter)", r"matching (?:style|look|edit)", r"cohesive (?:edit|look)",
    r"\bfilter\b", r"batch (?:edit|process|retouch)", r"edit(?:ed)? the same",
   ], ["image_list_presets", "image_apply_preset"]),
 "fine_grading": (4, [
    r"colou?r grad", r"cinematic", r"\bmoody\b", r"teal and orange", r"\bexposure\b",
    r"\bhighlights?\b", r"\bshadows?\b", r"white balance", r"\btonal\b", r"\bHDR\b",
    r"recover(?:y)? (?:detail|highlights|shadows)", r"\bcurves?\b", r"dynamic range",
    r"\bvibran", r"\bcontrast\b",
   ], ["image_adjust_exposure", "image_adjust_highlights", "image_adjust_dark_portions",
       "image_adjust_light_portions", "image_adjust_brightness_and_contrast",
       "image_adjust_hsl", "image_apply_auto_tone"]),
 "data_merge": (6, [
    r"data ?merge", r"mail ?merge", r"variable data", r"from (?:a |an )?(?:spreadsheet|csv|excel|list)",
    r"name ?badges?", r"name ?tags?", r"certificates?", r"place ?cards?", r"escort cards?",
    r"\bnumbered\b", r"raffle ticket", r"per (?:attendee|guest|student|employee|recipient|name)",
    r"price tags?", r"\d{2,4} (?:badges|cards|certificates|labels|tickets|tags|invitations)",
    r"list of names", r"each (?:badge|card|certificate|label).{0,20}(?:name|different)",
    r"personali[sz]ed (?:for each|cards|certificates|badges|labels)",
   ], ["document_merge_data_layout", "document_merge_data_vector", "document_render_layout",
       "document_render_vector"]),
 "stock_sourcing": (3, [
    r"stock (?:photo|image)", r"royalty[- ]?free", r"adobe stock", r"source (?:the )?images?",
    r"find (?:suitable |relevant )?(?:photos|images|stock)", r"licen[sc]e(?:d)? (?:photos|images)",
   ], ["asset_search", "asset_license_and_download_stock"]),
 "straighten_geo": (2, [
    r"\bcrooked\b", r"straighten", r"\bhorizon\b", r"\btilt(?:ed)?\b", r"\blevel the",
    r"perspective", r"\bwonky\b",
   ], ["image_auto_straighten", "image_crop_to_bounds"]),
 "bg_color": (2, [
    r"white background", r"solid (?:colou?r )?background", r"studio background",
    r"plain background", r"background colou?r", r"change .{0,15}background to",
   ], ["image_select_subject", "change_background_color", "image_remove_background"]),
 "video_edit": (5, [
    r"\bvideo\b", r"\breel\b", r"highlight (?:reel|clip)", r"\bfootage\b", r"premiere",
    r"sizzle", r"\bclips?\b", r"youtube (?:edit|video)", r"\btrim\b", r"\bb-roll\b",
   ], ["video_create_quick_cut", "video_resize", "media_summarize"]),
 "audio_speech": (4, [
    r"\baudio\b", r"podcast", r"voice[- ]?over", r"enhance speech", r"clean (?:up )?(?:the )?audio",
    r"transcri", r"\bnarration\b",
   ], ["media_enhance_speech", "media_summarize"]),
 "font_pairing": (1, [r"font pairing", r"font (?:recommendation|suggestion|pair)", r"typeface pairing"],
                  ["font_recommend"]),
}

NEG = [r"\blooking for (a|an|someone|skilled|experienced|talented)\b", r"\bwe(?:'re| are) (?:seeking|hiring)",
       r"\bideal (?:candidate|skills)\b", r"\byears? of experience\b", r"\bportfolio\b", r"\bproposal\b",
       r"\blong[- ]term\b", r"\bongoing (?:work|basis)\b", r"\bhourly\b", r"\bper hour\b",
       r"\bjoin (?:our|the) team\b", r"\bapply\b", r"\bbid\b"]

def analyze(desc, title, category=""):
    text = (title + "\n" + desc)
    low = text.lower()
    hit_families, tools = {}, set()
    for fam, (w, sigs, ftools) in FAMILIES.items():
        n = sum(1 for s in sigs if re.search(s, low))
        if n:
            hit_families[fam] = (w, n)
            tools.update(ftools)
    adv_tools = tools - USED
    # diversity score: sum of family weights (capped per family) + bonus for breadth
    fam_score = sum(w * min(n, 2) for w, n in hit_families.values())
    breadth = len(hit_families)
    new_tool_count = len(adv_tools)
    neg = sum(1 for p in NEG if re.search(p, low))
    L = len(desc)
    spec = min(L / 300.0, 6)
    score = fam_score + breadth * 3 + new_tool_count * 1.5 + spec - neg * 2.5
    return {"score": round(score, 1), "families": list(hit_families.keys()),
            "breadth": breadth, "new_tools": sorted(adv_tools),
            "new_tool_count": new_tool_count, "neg": neg, "len": L}

# ---------- 1) re-mine the doable set ----------
doable = json.load(open(ROOT + "/adobe_doable_full.json"))
rows = []
for d in doable:
    a = analyze(d.get("desc", ""), d.get("title", ""), d.get("category", ""))
    rows.append((a, d, "doable"))

# ---------- 2) scan the broader clean DB (not necessarily in doable) ----------
doable_ids = {d["id"] for d in doable}
con = sqlite3.connect(ROOT + "/pipeline/data/adobe.db")
con.row_factory = sqlite3.Row
extra = []
for r in con.execute("SELECT * FROM items WHERE cleantask=1"):
    a = analyze(r["description"] or "", r["title"] or "", r["vertical"] or "")
    extra.append((a, dict(r), "cleandb"))

mode = sys.argv[1] if len(sys.argv) > 1 else "summary"

if mode == "summary":
    print("=== UNUSED TOOL UNIVERSE (never used in any execution) ===")
    allfam = set()
    for w, sigs, ft in FAMILIES.values(): allfam.update(ft)
    print(sorted(allfam - USED))
    print("\n=== DOABLE set (1,260): advanced-workflow potential ===")
    fam_counter = Counter()
    rich = [x for x in rows if x[0]["breadth"] >= 2 and x[0]["neg"] <= 2]
    for a, d, _ in rows:
        for f in a["families"]: fam_counter[f] += 1
    print("tasks touching >=2 advanced families (low job-ad noise):", len(rich))
    print("family frequency across doable:", dict(fam_counter.most_common()))
    print("\n=== top 30 doable by complexity ===")
    for a, d, _ in sorted(rows, key=lambda x:-x[0]["score"])[:30]:
        print("%5.1f | id=%-5s b=%d nt=%2d | %-22s | %-26s | %s" % (
            a["score"], d["id"], a["breadth"], a["new_tool_count"],
            ",".join(a["families"])[:22], d["category"][:26], d["title"][:42]))
    print("\n=== top 25 from CLEAN DB not already in doable ===")
    seen = set()
    cnt = 0
    for a, r, _ in sorted(extra, key=lambda x:-x[0]["score"]):
        if r["id"] in doable_ids: continue
        if a["breadth"] < 2 or a["neg"] > 2: continue
        print("%5.1f | id=%-5s b=%d nt=%2d | %-26s | %s" % (
            a["score"], r["id"], a["breadth"], a["new_tool_count"],
            ",".join(a["families"])[:26], (r["title"] or "")[:46]))
        cnt += 1
        if cnt >= 25: break

elif mode == "archetypes":
    # group best candidates by dominant family (one strong example set per archetype)
    by_fam = defaultdict(list)
    allrows = rows + [(a, r, src) for a, r, src in extra if r["id"] not in doable_ids]
    for a, d, src in allrows:
        if a["neg"] > 2 or a["len"] < 300: continue
        for f in a["families"]:
            by_fam[f].append((a, d, src))
    for fam in FAMILIES:
        lst = sorted(by_fam.get(fam, []), key=lambda x:-x[0]["score"])[:6]
        if not lst: continue
        print("\n### %s — %d candidates" % (fam.upper(), len(by_fam[fam])))
        for a, d, src in lst:
            tid = d["id"]; title = d.get("title","")
            print("  %5.1f [%s] id=%-5s b=%d | %s" % (a["score"], src, tid, a["breadth"], title[:55]))

elif mode == "show":
    ids = {int(x) for x in sys.argv[2:]}
    pool = {d["id"]: (a, d, s) for a, d, s in rows + extra}
    for tid in ids:
        if tid not in pool: print("id", tid, "not found"); continue
        a, d, src = pool[tid]
        print("="*100)
        desc = d.get("desc") or d.get("description") or ""
        print("id=%s [%s] score=%.1f | families=%s | new_tools=%s" % (
            tid, src, a["score"], a["families"], a["new_tools"]))
        print("TITLE:", d.get("title"))
        print("CATEGORY:", d.get("category", d.get("vertical","")))
        print("URL:", d.get("url"))
        print("-"*100)
        print(desc[:2600])
        print()
