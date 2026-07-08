"""Offline validation of generated task folders (no API keys needed).
Checks: manifest schema, files exist + sha256 match, dims match, 1097
assets<->originals pairing, the COVERAGE invariant, ready_for_agent."""
from __future__ import annotations
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402
from util import sha256_file  # noqa: E402

REQUIRED_KEYS = ["schema_version", "task_id", "title", "mcp_workflow", "client_persona",
                 "assets", "decisions", "coverage", "ready_for_agent"]


def validate_task(task_dir: Path):
    errs, warns = [], []
    mf = task_dir / "manifest.json"
    if not mf.exists():
        return ["manifest.json missing"], warns
    man = json.loads(mf.read_text())
    for k in REQUIRED_KEYS:
        if k not in man:
            errs.append("manifest missing key %r" % k)

    for e in man.get("assets", []):
        f = e.get("file")
        if not f:
            if (e.get("qc") or {}).get("status") == "failed":
                errs.append("asset %s FAILED generation" % e.get("key"))
            continue
        p = task_dir / f
        if not p.exists():
            errs.append("file missing: %s" % f)
            continue
        if e.get("sha256") and sha256_file(p) != e["sha256"]:
            errs.append("sha256 mismatch: %s" % f)
        if e.get("kind") == "image" and e.get("dims"):
            try:
                from PIL import Image
                with Image.open(p) as im:
                    if [im.width, im.height] != e["dims"]:
                        errs.append("dims mismatch %s: %sx%s != %s" % (f, im.width, im.height, e["dims"]))
            except Exception as ex:
                errs.append("unreadable image %s: %s" % (f, ex))
        for pp in e.get("post_process", []):
            if pp.get("original") and not (task_dir / pp["original"]).exists():
                errs.append("post_process original missing: %s" % pp["original"])

    cov = man.get("coverage", {})
    if cov.get("uncovered"):
        errs.append("COVERAGE FAIL — uncovered inputs: %s" % cov["uncovered"])
    if not man.get("ready_for_agent"):
        warns.append("ready_for_agent is false")
    for e in man.get("assets", []):
        st = (e.get("qc") or {}).get("status")
        if st == "accepted_with_warnings":
            warns.append("%s accepted_with_warnings (score %s)" % (e.get("key"), (e.get("qc") or {}).get("vision_score")))
    return errs, warns


def main():
    root = config.OUT_ROOT
    dirs = sorted(d for d in root.glob("*_*") if d.is_dir())
    if not dirs:
        print("no task folders under %s" % root)
        sys.exit(1)
    bad = 0
    for d in dirs:
        errs, warns = validate_task(d)
        status = "OK" if not errs else "FAIL"
        if errs:
            bad += 1
        print("[%s] %s" % (status, d.name))
        for e in errs:
            print("    ERR  %s" % e)
        for w in warns:
            print("    warn %s" % w)
    print("\n%d/%d task folders valid" % (len(dirs) - bad, len(dirs)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
