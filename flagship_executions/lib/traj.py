#!/usr/bin/env python
"""Trajectory logger for flagship executions.

Every action an agent takes on a task — Adobe connector call, local compose
stage, export, verification — is appended as one step, each with a snapshot
image in steps/. This is the audit trail the presentation HTML will replay.

Usage:
  traj.py init <task_dir> <task_id> <slug> "<title>"
  traj.py add  <task_dir> --json '<entry-json>' [--snap <image-path>] [--snap-name <label>]
  traj.py finish <task_dir>

Entry JSON fields (caller supplies; n/ts/step_image are filled in here):
  phase:  upload | element_processing | composition | export | verify
  actor:  adobe_connector | local_compositor | local_verify
  action: tool or function name (e.g. image_remove_background, compose_front_panel)
  note:   one human sentence — WHY this step exists for this task
  input / output: file paths relative to the task dir (or URLs)
  adobe_request_id: requestId from the connector result (connector steps ONLY)
  params: small dict of the parameters that mattered
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _load(td: Path) -> dict:
    f = td / "trajectory.json"
    return json.loads(f.read_text()) if f.exists() else None


def _write(td: Path, doc: dict):
    (td / "trajectory.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False))


def main():
    cmd, td = sys.argv[1], Path(sys.argv[2])
    if cmd == "init":
        doc = {"task_id": int(sys.argv[3]), "slug": sys.argv[4], "title": sys.argv[5],
               "started": time.strftime("%Y-%m-%dT%H:%M:%S"), "finished": None, "steps": []}
        _write(td, doc)
        print("trajectory initialized")
        return
    doc = _load(td)
    if doc is None:
        sys.exit("trajectory.json missing — run init first")
    if cmd == "finish":
        doc["finished"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        _write(td, doc)
        print("trajectory finished: %d steps" % len(doc["steps"]))
        return
    if cmd == "add":
        args = sys.argv[3:]
        entry, snap, snap_name = {}, None, None
        i = 0
        while i < len(args):
            if args[i] == "--json":
                entry = json.loads(args[i + 1]); i += 2
            elif args[i] == "--snap":
                snap = args[i + 1]; i += 2
            elif args[i] == "--snap-name":
                snap_name = args[i + 1]; i += 2
            else:
                i += 1
        n = len(doc["steps"]) + 1
        entry["n"] = n
        entry["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        if snap:
            from compose_lib import step_preview
            entry["step_image"] = step_preview(
                snap, td / "steps", n, snap_name or entry.get("action", "step"))
        doc["steps"].append(entry)
        _write(td, doc)
        print("step %d logged: %s" % (n, entry.get("action")))
        return
    sys.exit("unknown command %r" % cmd)


if __name__ == "__main__":
    main()
