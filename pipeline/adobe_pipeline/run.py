"""CLI orchestrator.

  python -m adobe_pipeline.run collect [--source NAME]
  python -m adobe_pipeline.run export-csv  --out FILE [--kind task|listing]
  python -m adobe_pipeline.run export-json --out FILE [--kind task|listing]
  python -m adobe_pipeline.run export-docx --out FILE [--kind task|listing] [--limit N]
  python -m adobe_pipeline.run stats
  python -m adobe_pipeline.run upwork-auth-url
  python -m adobe_pipeline.run upwork-exchange --code CODE
"""
import os
import sys
import json
import time
import logging
import inspect
import argparse

from . import db, export
from .http import TokenBucket, PoliteSession, BlockedError
from .collectors import REGISTRY
from . import upwork as up

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("pipeline.run")


def load_config():
    with open(os.path.join(ROOT, "config.json"), encoding="utf-8") as f:
        return json.load(f)


def load_env():
    env = {}
    p = os.path.join(ROOT, ".env")
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    env.update({k: v for k, v in os.environ.items() if k.startswith("UPWORK_")})
    return env


def _session(name, scfg, ua):
    bucket = TokenBucket(scfg.get("rate_per_sec", 0.5), scfg.get("burst", 1))
    return PoliteSession(bucket, ua, daily_cap=scfg.get("daily_cap"))


def collect(cfg, only=None):
    conn = db.connect(os.path.join(ROOT, cfg["db_path"]))
    ua = cfg["user_agent"]
    env = load_env()
    sources = cfg["sources"]
    targets = [only] if only else list(sources.keys())
    for name in targets:
        scfg = sources.get(name)
        if not scfg or not scfg.get("enabled"):
            if only:
                log.warning("source '%s' not enabled in config", name)
            continue
        run_id = db.start_run(conn, name)
        fetched = new = updated = errors = 0
        status = "ok"
        try:
            session = _session(name, scfg, ua)
            if name == "upwork":
                token = env.get("UPWORK_ACCESS_TOKEN")
                if not token:
                    raise RuntimeError("no UPWORK_ACCESS_TOKEN — run upwork-exchange first")
                gen = up.collect_upwork(session, scfg, cfg["filters"], token)
            else:
                fn = REGISTRY[name]
                kw = {"conn": conn} if "conn" in inspect.signature(fn).parameters else {}
                gen = fn(session, scfg, cfg["filters"], **kw)
            for item in gen:
                fetched += 1
                res = db.upsert_item(conn, item)
                if res == "new":
                    new += 1
                elif res == "updated":
                    updated += 1
                if fetched % 200 == 0:
                    conn.commit()
                    log.info("[%s] fetched=%d new=%d updated=%d", name, fetched, new, updated)
            conn.commit()
        except BlockedError as e:
            status, errors = "blocked", errors + 1
            log.error("[%s] BLOCKED: %s — pausing this source", name, e)
        except Exception as e:
            status, errors = "error", errors + 1
            log.exception("[%s] failed: %s", name, e)
        db.set_state(conn, name, cursor=str(int(time.time())))
        db.finish_run(conn, run_id, fetched, new, updated, errors, status)
        log.info("[%s] DONE status=%s fetched=%d new=%d updated=%d", name, status, fetched, new, updated)
    conn.close()


def stats(cfg):
    conn = db.connect(os.path.join(ROOT, cfg["db_path"]))
    c = db.counts(conn)
    print("Total items: %d  (tasks=%d, listings=%d)" % (c["total"], c["tasks"], c["listings"]))
    print("By source:", ", ".join("%s=%d" % (k, v) for k, v in c["by_source"].items()))
    print("Top industries:")
    for r in conn.execute("SELECT vertical, COUNT(*) c FROM items WHERE kind='task' GROUP BY vertical ORDER BY c DESC LIMIT 20"):
        print("  %4d  %s" % (r["c"], r["vertical"]))
    print("Recent runs:")
    for r in conn.execute("SELECT source,fetched,new,updated,status FROM runs ORDER BY id DESC LIMIT 8"):
        print("  %-16s fetched=%-5d new=%-5d updated=%-4d %s" % (r["source"], r["fetched"], r["new"], r["updated"], r["status"]))
    conn.close()


def write_env(updates):
    p = os.path.join(ROOT, ".env")
    lines = []
    if os.path.exists(p):
        lines = open(p, encoding="utf-8").read().splitlines()
    keys = set(updates)
    out, seen = [], set()
    for line in lines:
        k = line.split("=", 1)[0].strip() if "=" in line else None
        if k in keys:
            out.append("%s=%s" % (k, updates[k])); seen.add(k)
        else:
            out.append(line)
    for k in keys - seen:
        out.append("%s=%s" % (k, updates[k]))
    open(p, "w", encoding="utf-8").write("\n".join(out) + "\n")


def upwork_auth_url(cfg):
    env = load_env()
    cid, redirect = env.get("UPWORK_CLIENT_ID"), env.get("UPWORK_REDIRECT_URI", "https://localhost/callback")
    if not cid:
        print("Set UPWORK_CLIENT_ID in .env first (copy .env.example -> .env)."); return
    print("1) Open this URL, log in, and approve:\n")
    print("   " + up.build_auth_url(cid, redirect))
    print("\n2) You'll be redirected to %s?code=XXXX (the page may not load — that's fine)." % redirect)
    print("3) Copy the code and run:  python -m adobe_pipeline.run upwork-exchange --code XXXX")


def upwork_exchange(cfg, code):
    env = load_env()
    cid, secret = env.get("UPWORK_CLIENT_ID"), env.get("UPWORK_CLIENT_SECRET")
    redirect = env.get("UPWORK_REDIRECT_URI", "https://localhost/callback")
    if not (cid and secret):
        print("Set UPWORK_CLIENT_ID and UPWORK_CLIENT_SECRET in .env first."); return
    session = PoliteSession(TokenBucket(0.5, 1), cfg["user_agent"])
    tok = up.exchange_code(session, cid, secret, code, redirect)
    if "access_token" not in tok:
        print("Token exchange response (verify):", json.dumps(tok)[:400]); return
    write_env({"UPWORK_ACCESS_TOKEN": tok["access_token"], "UPWORK_REFRESH_TOKEN": tok.get("refresh_token", "")})
    print("Saved tokens to .env. Now set sources.upwork.enabled=true in config.json and run:")
    print("   python -m adobe_pipeline.run collect --source upwork")


def main(argv=None):
    cfg = load_config()
    ap = argparse.ArgumentParser(prog="adobe_pipeline.run")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("collect"); c.add_argument("--source")
    for name in ("export-csv", "export-json", "export-docx"):
        e = sub.add_parser(name); e.add_argument("--out", required=True)
        e.add_argument("--kind", choices=["task", "listing"], default=None)
        if name == "export-docx":
            e.add_argument("--limit", type=int, default=None)
    sub.add_parser("stats")
    sub.add_parser("upwork-auth-url")
    ex = sub.add_parser("upwork-exchange"); ex.add_argument("--code", required=True)
    args = ap.parse_args(argv)

    if args.cmd == "collect":
        collect(cfg, args.source)
    elif args.cmd == "stats":
        stats(cfg)
    elif args.cmd == "upwork-auth-url":
        upwork_auth_url(cfg)
    elif args.cmd == "upwork-exchange":
        upwork_exchange(cfg, args.code)
    elif args.cmd.startswith("export-"):
        conn = db.connect(os.path.join(ROOT, cfg["db_path"]))
        os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
        if args.cmd == "export-csv":
            n = export.export_csv(conn, args.out, args.kind)
        elif args.cmd == "export-json":
            n = export.export_json(conn, args.out, args.kind)
        else:
            n = export.export_docx(conn, args.out, args.kind or "task", args.limit)
        print("Wrote %d rows -> %s" % (n, args.out))
        conn.close()


if __name__ == "__main__":
    main()
