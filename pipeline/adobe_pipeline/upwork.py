"""Upwork GraphQL collector + OAuth2 helpers.

Upwork requires OAuth2 (user context). Flow:
  1) Create an app at https://www.upwork.com/developer/apps/  (redirect URI -> https://localhost/callback)
  2) `run.py upwork-auth-url`  -> open the URL, approve, copy ?code=... from the redirect
  3) `run.py upwork-exchange --code <code>`  -> stores access/refresh tokens in .env
  4) set sources.upwork.enabled = true in config.json, then `run.py collect --source upwork`

NOTE: the GraphQL query below is a best-effort template. Upwork's schema field names change and the
docs block automated reading, so confirm field names in the live GraphQL explorer once authenticated
and tweak SEARCH_QUERY if a field is rejected. The collector parses defensively.
"""
import logging

from . import normalize as N

log = logging.getLogger("pipeline.upwork")

AUTHORIZE_URL = "https://www.upwork.com/ab/account-security/oauth2/authorize"
TOKEN_URL = "https://www.upwork.com/api/v3/oauth2/token"

SEARCH_QUERY = """
query JobSearch($q: String!, $after: String) {
  marketplaceJobPostingsSearch(
    marketPlaceJobFilter: { searchExpression_eq: $q }
    searchType: USER_JOBS_SEARCH
    sortAttributes: [{ field: RECENCY }]
    pagination: { after: $after, first: 50 }
  ) {
    totalCount
    edges {
      node {
        id
        ciphertext
        title
        description
        createdDateTime
        skills { name }
        amount { rawValue currency }
        hourlyBudgetMin { rawValue }
        hourlyBudgetMax { rawValue }
      }
    }
    pageInfo { endCursor hasNextPage }
  }
}
"""


def build_auth_url(client_id, redirect_uri):
    from urllib.parse import urlencode
    return AUTHORIZE_URL + "?" + urlencode({
        "response_type": "code", "client_id": client_id, "redirect_uri": redirect_uri,
    })


def exchange_code(session, client_id, client_secret, code, redirect_uri):
    return session.post_json(TOKEN_URL, data={
        "grant_type": "authorization_code", "code": code, "redirect_uri": redirect_uri,
        "client_id": client_id, "client_secret": client_secret,
    })


def refresh_access_token(session, client_id, client_secret, refresh_token):
    return session.post_json(TOKEN_URL, data={
        "grant_type": "refresh_token", "refresh_token": refresh_token,
        "client_id": client_id, "client_secret": client_secret,
    })


def _budget(node):
    a = node.get("amount") or {}
    if a.get("rawValue"):
        return "%s %s (fixed)" % (a.get("rawValue"), a.get("currency") or "")
    lo = (node.get("hourlyBudgetMin") or {}).get("rawValue")
    hi = (node.get("hourlyBudgetMax") or {}).get("rawValue")
    if lo or hi:
        return "$%s–$%s /hr" % (lo or "?", hi or "?")
    return "See posting"


def collect_upwork(session, cfg, filters, access_token):
    url = cfg.get("graphql_url", "https://api.upwork.com/graphql")
    headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
    max_pages = cfg.get("max_pages_per_run", 50)
    for q in cfg.get("queries", []):
        after, page = None, 0
        while page < max_pages:
            page += 1
            resp = session.post_json(url, json={"query": SEARCH_QUERY, "variables": {"q": q, "after": after}}, headers=headers)
            if resp.get("errors"):
                log.warning("upwork query '%s' error: %s", q, str(resp["errors"])[:300])
                break
            block = ((resp.get("data") or {}).get("marketplaceJobPostingsSearch") or {})
            edges = block.get("edges") or []
            if not edges:
                break
            for e in edges:
                node = e.get("node") or {}
                desc = (node.get("description") or "").strip()
                skills = [s.get("name", "") for s in (node.get("skills") or [])]
                if not N.is_task_relevant(skills, node.get("title"), desc, filters):
                    continue
                tools = N.derive_tools(skills, desc)
                cipher = node.get("ciphertext") or ""
                yield {
                    "kind": "task", "source": "upwork", "external_id": node.get("id") or cipher,
                    "title": (node.get("title") or "").strip(), "company": "",
                    "vertical": N.detect_vertical(node.get("title"), desc), "adobe_tools": tools,
                    "budget": _budget(node), "salary": "", "location": "Remote",
                    "posted_at": (node.get("createdDateTime") or "")[:10] or None,
                    "url": ("https://www.upwork.com/jobs/" + cipher) if cipher else "https://www.upwork.com/nx/search/jobs/",
                    "description": desc, "raw": {"skills": skills, "query": q, "tools_why": N.tools_why(tools, desc)},
                }
            pi = block.get("pageInfo") or {}
            if pi.get("hasNextPage") and pi.get("endCursor"):
                after = pi["endCursor"]
            else:
                break
