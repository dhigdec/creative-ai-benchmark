"""Source collectors. Each yields normalized item dicts (the common schema).

Add a new source by writing one collect_<name>(session, cfg, filters) generator that yields:
  {kind, source, external_id, title, company, vertical, adobe_tools, budget, salary,
   location, posted_at, url, description, raw}
Everything else (rate limiting, dedup, storage, export) is automatic.
"""
import re
import json
import time
import hashlib
import datetime as dt

from . import normalize as N


def _iso(epoch):
    try:
        return dt.datetime.utcfromtimestamp(float(epoch)).strftime("%Y-%m-%d")
    except Exception:
        return None


# ---------------- Freelancer.com (client tasks) ----------------
def collect_freelancer(session, cfg, filters):
    base = "https://www.freelancer.com/api/projects/0.1/projects/active/"
    page_size = cfg.get("page_size", 50)
    max_pages = cfg.get("max_pages_per_run", 100)
    common = [("limit", page_size), ("full_description", "true"), ("job_details", "true")]
    for sid in cfg.get("skill_ids", []):
        common.append(("jobs[]", sid))
    for page in range(max_pages):
        params = common + [("offset", page * page_size)]
        data = session.get_json(base, params=params)
        projects = (data.get("result") or {}).get("projects") or []
        if not projects:
            break
        for p in projects:
            desc = (p.get("description") or "").strip()
            skills = [j.get("name", "") for j in (p.get("jobs") or [])]
            if not N.is_task_relevant(skills, p.get("title"), desc, filters):
                continue
            tools = N.derive_tools(skills, desc)
            yield {
                "kind": "task", "source": "freelancer", "external_id": p.get("id"),
                "title": (p.get("title") or "").strip(),
                "company": "", "vertical": N.detect_vertical(p.get("title"), desc),
                "adobe_tools": tools, "budget": N.budget_str_freelancer(p), "salary": "",
                "location": "Remote", "posted_at": _iso(p.get("submitdate")),
                "url": "https://www.freelancer.com/projects/" + (p.get("seo_url") or ""),
                "description": desc,
                "raw": {"skills": skills, "tools_why": N.tools_why(tools, desc)},
            }


# ---------------- remote job boards (listings) ----------------
def _listing(source, ext_id, title, company, location, salary, jtype, url, desc, tags):
    text = (title or "") + " " + " ".join(tags or []) + " " + (desc or "")
    tools = N.derive_tools([], text)
    return {
        "kind": "listing", "source": source, "external_id": ext_id, "title": title,
        "company": company or "", "vertical": N.detect_vertical(title, desc),
        "adobe_tools": tools, "budget": "", "salary": salary or "", "location": location or "Remote",
        "posted_at": None, "url": url, "description": (N.strip_html(desc) or "")[:1500],
        "raw": {"type": jtype, "tags": tags or []},
    }


def collect_remoteok(session, cfg, filters):
    data = session.get_json("https://remoteok.com/api")
    for j in data:
        if not isinstance(j, dict) or not j.get("position"):
            continue
        if not N.is_listing_relevant(j.get("position"), j.get("tags"), j.get("description"), filters):
            continue
        sal = ""
        if j.get("salary_min"):
            sal = "$%s%s" % (j["salary_min"], ("–$%s" % j["salary_max"]) if j.get("salary_max") else "")
        yield _listing("remoteok", j.get("id") or j.get("slug"), j.get("position"), j.get("company"),
                       j.get("location") or "Remote", sal, "", j.get("url") or ("https://remoteok.com/l/%s" % j.get("id")),
                       j.get("description"), j.get("tags"))


def collect_remotive(session, cfg, filters):
    data = session.get_json("https://remotive.com/api/remote-jobs?category=design")
    for j in (data.get("jobs") or []):
        if not N.is_listing_relevant(j.get("title"), j.get("tags"), j.get("description"), filters):
            continue
        yield _listing("remotive", j.get("id"), j.get("title"), j.get("company_name"),
                       j.get("candidate_required_location") or "Remote", j.get("salary") or "",
                       j.get("job_type") or "", j.get("url"), j.get("description"), j.get("tags"))


def collect_jobicy(session, cfg, filters):
    data = session.get_json("https://jobicy.com/api/v2/remote-jobs?count=100&tag=design")
    for j in (data.get("jobs") or []):
        desc = j.get("jobExcerpt") or j.get("jobDescription") or ""
        tags = j.get("jobIndustry") or []
        if not N.is_listing_relevant(j.get("jobTitle"), tags, desc, filters):
            continue
        yield _listing("jobicy", j.get("id"), j.get("jobTitle"), j.get("companyName"),
                       j.get("jobGeo") or "Remote", (j.get("annualSalaryMin") and "$%s–$%s" % (j.get("annualSalaryMin"), j.get("annualSalaryMax"))) or "",
                       ", ".join(j.get("jobType") or []), j.get("url"), desc, tags)


def collect_arbeitnow(session, cfg, filters):
    max_pages = cfg.get("max_pages_per_run", 10)
    for page in range(1, max_pages + 1):
        data = session.get_json("https://www.arbeitnow.com/api/job-board-api?page=%d" % page)
        rows = data.get("data") or []
        if not rows:
            break
        for j in rows:
            if not N.is_listing_relevant(j.get("title"), j.get("tags"), j.get("description"), filters):
                continue
            yield _listing("arbeitnow", j.get("slug"), j.get("title"), j.get("company_name"),
                           j.get("location") or "Remote", "", ", ".join(j.get("job_types") or []),
                           j.get("url"), j.get("description"), j.get("tags"))


def collect_weworkremotely(session, cfg, filters):
    import re
    rss = session.get_text("https://weworkremotely.com/categories/remote-design-jobs.rss")
    for block in re.findall(r"<item>([\s\S]*?)</item>", rss):
        def g(pat):
            m = re.search(pat, block)
            return (m.group(1).strip() if m else "")
        title = g(r"<title>(?:<!\[CDATA\[)?([\s\S]*?)(?:\]\]>)?</title>")
        link = g(r"<link>([\s\S]*?)</link>")
        desc = g(r"<description>(?:<!\[CDATA\[)?([\s\S]*?)(?:\]\]>)?</description>")
        region = g(r"<region>([\s\S]*?)</region>")
        if not title or not link:
            continue
        company, role = "", title
        if ":" in title:
            company, role = title.split(":", 1)
            company, role = company.strip(), role.strip()
        if not N.is_listing_relevant(title, [], desc, filters):
            continue
        yield _listing("weworkremotely", link, role, company, region or "Remote", "", "", link, desc, [])


def collect_themuse(session, cfg, filters):
    max_pages = cfg.get("max_pages_per_run", 25)
    for page in range(1, max_pages + 1):
        data = session.get_json("https://www.themuse.com/api/public/jobs",
                                params=[("category", "Design and UX"), ("page", page)])
        results = data.get("results") or []
        if not results:
            break
        for j in results:
            desc = N.strip_html(j.get("contents"))
            company = (j.get("company") or {}).get("name", "")
            locs = ", ".join(l.get("name", "") for l in (j.get("locations") or [])) or "Remote"
            cats = [c.get("name", "") for c in (j.get("categories") or [])]
            if not N.is_listing_relevant(j.get("name"), cats, desc, filters):
                continue
            url = (j.get("refs") or {}).get("landing_page") or ""
            yield _listing("themuse", j.get("id"), j.get("name"), company, locs, "",
                           j.get("type") or "", url, desc, cats)
        if data.get("page_count") and page >= data["page_count"]:
            break


def collect_himalayas(session, cfg, filters):
    max_pages = cfg.get("max_pages_per_run", 10)
    last_first = None
    for page in range(max_pages):
        data = session.get_json("https://himalayas.app/jobs/api",
                                params=[("limit", 50), ("offset", page * 50)])
        jobs = data.get("jobs") or []
        if not jobs or (jobs and jobs[0].get("title") == last_first):
            break
        last_first = jobs[0].get("title")
        for j in jobs:
            desc = N.strip_html(j.get("excerpt") or j.get("description") or "")
            company = j.get("companyName", "")
            cats = [c for c in (j.get("categories") or []) if isinstance(c, str)]
            if not N.is_listing_relevant(j.get("title"), cats, desc, filters):
                continue
            url = j.get("applicationLink") or j.get("url") or ("https://himalayas.app/companies/" + (j.get("companySlug") or ""))
            sal = ("%s%s-%s" % (j.get("currency") or "$", j.get("minSalary"), j.get("maxSalary"))) if j.get("minSalary") else ""
            ext = j.get("guid") or j.get("id") or hashlib.md5(((j.get("title") or "") + company).encode("utf-8")).hexdigest()
            loc = ", ".join(j.get("locationRestrictions") or []) or "Remote"
            yield _listing("himalayas", ext, j.get("title"), company, loc, sal,
                           j.get("employmentType") or "", url, desc, cats)


def collect_workingnomads(session, cfg, filters):
    data = session.get_json("https://www.workingnomads.com/api/exposed_jobs/")
    rows = data if isinstance(data, list) else (data.get("jobs") or [])
    for j in rows:
        desc = N.strip_html(j.get("description") or "")
        tags = j.get("tags")
        tags = tags.split(",") if isinstance(tags, str) else (tags or [])
        cats = [j.get("category_name", "")] + [t for t in tags if isinstance(t, str)]
        if not N.is_listing_relevant(j.get("title"), cats, desc, filters):
            continue
        url = j.get("url") or ""
        ext = url or hashlib.md5(((j.get("title") or "") + (j.get("company_name") or "")).encode("utf-8")).hexdigest()
        yield _listing("workingnomads", ext, j.get("title"), j.get("company_name"),
                       j.get("location") or "Remote", "", "", url, desc, cats)


# ---------------------------------------------------------------------------
# PeoplePerHour: no API, but it publishes sitemaps (crawler-sanctioned) and its
# detail pages embed schema.org JobPosting ld+json. We read the jobs sitemap,
# keep only design/Adobe URLs (by slug keyword), then fetch newest-first detail
# pages politely and parse the ld+json. Honors robots: sitemaps + detail paths
# are allowed; we never touch the disallowed "?query" listing URLs.
# ---------------------------------------------------------------------------
PPH_SITEMAP_INDEX = "https://www.peopleperhour.com/pphsitemaps/sitemap.live.jobs.index.xml"
PPH_DESIGN_KW = re.compile(
    r"(logo|design|photoshop|illustrat|indesign|after-?effects|premiere|lightroom|brochure|"
    r"flyer|banner|packaging|poster|graphic|brand|retouch|animation|infographic|vector|"
    r"book-?cover|label|cartoon|caricature|typograph|mockup|photo-?edit|image-?edit|"
    r"video-?edit|motion|artwork|illustration)", re.I)


def _pph_parse_detail(html, url, ext):
    title = desc = posted = None
    for m in re.finditer(r"application/ld\+json[^>]*>(.*?)</script>", html, re.S):
        try:
            data = json.loads(m.group(1))
        except Exception:
            continue
        for d in (data if isinstance(data, list) else [data]):
            if isinstance(d, dict) and d.get("@type") == "JobPosting":
                title = d.get("title")
                desc = N.strip_html(d.get("description") or "")
                posted = d.get("datePosted")
                break
        if title:
            break
    if not desc:
        return None
    bm = re.search(r"(£|\$|€|₹)\s?[\d,]{2,}", html)
    return {"title": title or "", "description": desc, "posted_at": posted or "",
            "budget": (bm.group(0) if bm else "See posting"), "url": url, "ext": ext}


def collect_peopleperhour(session, cfg, filters, conn=None):
    max_shards = cfg.get("max_shards_per_run", 1)
    max_details = cfg.get("max_details_per_run", 250)
    seen = set()
    if conn is not None:
        try:
            for r in conn.execute("SELECT external_id FROM items WHERE source='peopleperhour'"):
                seen.add(r["external_id"])
        except Exception:
            pass
    shards = re.findall(r"<loc>\s*(.*?)\s*</loc>", session.get_text(PPH_SITEMAP_INDEX))

    def snum(u):
        m = re.search(r"jobs\.(\d+)\.xml", u)
        return int(m.group(1)) if m else -1

    shards.sort(key=snum, reverse=True)  # newest shard first
    done = 0
    for shard in shards[:max_shards]:
        urls = re.findall(r"<loc>\s*(.*?)\s*</loc>", session.get_text(shard))
        design = [u for u in urls if PPH_DESIGN_KW.search(u)]
        design.reverse()  # highest id (newest) first
        for u in design:
            if done >= max_details:
                return
            mid = re.search(r"-(\d+)/?$", u)
            ext = mid.group(1) if mid else u
            if ext in seen:
                continue
            try:
                html = session.get_text(u)
            except Exception:
                continue
            p = _pph_parse_detail(html, u, ext)
            if not p or len(p["description"]) < filters.get("min_description_chars", 200):
                continue
            if not N.is_task_relevant([], p["title"], p["description"], filters):
                continue
            tools = N.derive_tools([], (p["title"] or "") + " " + p["description"])
            done += 1
            yield {
                "kind": "task", "source": "peopleperhour", "external_id": ext,
                "title": p["title"], "company": "",
                "vertical": N.detect_vertical(p["title"], p["description"]),
                "adobe_tools": tools, "budget": p["budget"], "salary": "", "location": "Remote",
                "posted_at": p["posted_at"], "url": u, "description": p["description"], "raw": {},
            }


def _ldjson_jobposting(html):
    """Return the first schema.org JobPosting object embedded in a page, or None."""
    for m in re.finditer(r"application/ld\+json[^>]*>(.*?)</script>", html, re.S):
        try:
            data = json.loads(m.group(1))
        except Exception:
            continue
        for d in (data if isinstance(data, list) else [data]):
            if isinstance(d, dict) and d.get("@type") == "JobPosting":
                return d
    return None


# ---- Dribbble: design-only job board. /jobs is server-rendered (links with titles);
#      detail pages carry JobPosting ld+json. robots allows everything except /apply_now. ----
def collect_dribbble(session, cfg, filters, conn=None):
    max_pages = cfg.get("max_pages_per_run", 20)
    max_details = cfg.get("max_details_per_run", 300)
    seen = set()
    if conn is not None:
        try:
            for r in conn.execute("SELECT external_id FROM items WHERE source='dribbble'"):
                seen.add(r["external_id"])
        except Exception:
            pass
    done = 0
    for page in range(1, max_pages + 1):
        list_url = "https://dribbble.com/jobs" if page == 1 else "https://dribbble.com/jobs?page=%d" % page
        try:
            html = session.get_text(list_url)
        except Exception:
            break
        pg_seen, uniq = set(), []
        for jid, slug in re.findall(r"/jobs/(\d+)-([A-Za-z0-9\-]+)", html):
            if jid not in pg_seen:
                pg_seen.add(jid)
                uniq.append((jid, slug))
        if not uniq:
            break
        for jid, slug in uniq:
            if done >= max_details:
                return
            if jid in seen:
                continue
            url = "https://dribbble.com/jobs/%s-%s" % (jid, slug)
            try:
                jp = _ldjson_jobposting(session.get_text(url))
            except Exception:
                continue
            if not jp:
                continue
            title = jp.get("title") or slug.replace("-", " ")
            desc = N.strip_html(jp.get("description") or "")
            if len(desc) < filters.get("min_listing_chars", 80):
                continue
            blob = (title + " " + desc).lower()
            if "design" not in blob and not N.ADX.search(blob):
                continue
            ho = jp.get("hiringOrganization")
            company = ho.get("name", "") if isinstance(ho, dict) else ""
            loc = "Remote"
            jl = jp.get("jobLocation")
            if isinstance(jl, dict):
                addr = jl.get("address") or {}
                loc = addr.get("addressLocality") or addr.get("addressCountry") or "Remote"
            sal = ""
            bs = jp.get("baseSalary")
            if isinstance(bs, dict):
                v = bs.get("value") or {}
                if isinstance(v, dict) and v.get("minValue"):
                    sal = "%s%s-%s" % (bs.get("currency", "$"), v.get("minValue"), v.get("maxValue", ""))
            done += 1
            yield {
                "kind": "listing", "source": "dribbble", "external_id": jid, "title": title,
                "company": company, "vertical": N.detect_vertical(title, desc),
                "adobe_tools": N.derive_tools([], title + " " + desc), "budget": "", "salary": sal,
                "location": loc, "posted_at": jp.get("datePosted") or "", "url": url,
                "description": desc[:2000], "raw": {},
            }


# ---- Jobspresso: WordPress Job Manager RSS feed (?feed=job_feed). ~10 recent per query. ----
def collect_jobspresso(session, cfg, filters):
    queries = cfg.get("queries", ["design", "adobe", "photoshop", "illustrator", "graphic",
                                  "branding", "motion graphics", "video editor", "art director"])
    seen_links = set()
    for kw in queries:
        try:
            xml = session.get_text("https://jobspresso.co/", params=[("feed", "job_feed"), ("search_keywords", kw)])
        except Exception:
            continue
        for item in re.findall(r"<item>(.*?)</item>", xml, re.S):
            def g(tag):
                m = re.search(r"<%s>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</%s>" % (tag, tag), item, re.S)
                return N.strip_html(m.group(1)) if m else ""
            link = g("link")
            if not link or link in seen_links:
                continue
            seen_links.add(link)
            title = g("title")
            ce = re.search(r"<content:encoded>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</content:encoded>", item, re.S)
            desc = N.strip_html(ce.group(1)) if ce else g("description")
            if not N.is_listing_relevant(title, [], desc, filters):
                continue
            company = g("job_listing:company")
            loc = g("job_listing:location") or "Remote"
            mid = re.search(r"-(\d+)/?$", link) or re.search(r"/(\d+)/?$", link)
            ext = mid.group(1) if mid else link
            yield {
                "kind": "listing", "source": "jobspresso", "external_id": ext, "title": title,
                "company": company, "vertical": N.detect_vertical(title, desc),
                "adobe_tools": N.derive_tools([], title + " " + desc), "budget": "", "salary": "",
                "location": loc, "posted_at": g("pubDate"), "url": link, "description": desc[:2000], "raw": {},
            }


REGISTRY = {
    "freelancer": collect_freelancer,
    "remoteok": collect_remoteok,
    "remotive": collect_remotive,
    "jobicy": collect_jobicy,
    "arbeitnow": collect_arbeitnow,
    "weworkremotely": collect_weworkremotely,
    "themuse": collect_themuse,
    "himalayas": collect_himalayas,
    "workingnomads": collect_workingnomads,
    "peopleperhour": collect_peopleperhour,
    "dribbble": collect_dribbble,
    "jobspresso": collect_jobspresso,
}
