#!/usr/bin/env python3
"""Synchronize pilot brief/brand copy from TASK_SPEC, without changing task scope."""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
from copy import deepcopy
from pathlib import Path

from build_v7_annotation_pilot import ROOT, TASKS, TASK_IDS


PAGE = ROOT / "docs/gatsby-v7"
DATA_SCRIPT = re.compile(r'(<script\b[^>]*\bid=[\"\']data[\"\'][^>]*>)(.*?)(</script>)', re.S)


def reconcile(path: Path, content: str, check: bool) -> None:
    if path.read_bytes().decode("utf-8") == content:
        return
    if check:
        raise ValueError(f"Stale content: {path.relative_to(ROOT)}")
    path.write_text(content, encoding="utf-8")
    print(path.relative_to(ROOT))


def sync_csv(path: Path, specs: dict, check: bool) -> None:
    text = path.read_bytes().decode("utf-8")
    lines = text.splitlines(keepends=True)
    reader = csv.reader(io.StringIO(text, newline=""))
    headers = next(reader)
    by_code = {spec["task_code"]: spec for spec in specs.values()}
    end = reader.line_num
    result = lines[:end]
    brand_fields = {
        "Founded / place / size": "founded_place_size", "About": "about",
        "Audience": "audience", "Price positioning": "price_positioning",
        "Brand assets status": "brand_assets_status",
    }
    for values in reader:
        start, end = end, reader.line_num
        row = dict(zip(headers, values))
        original = row.copy()
        spec = by_code.get(row.get("Task code"))
        if spec:
            if "Client brief" in row:
                row["Client brief"] = spec["client_brief"]
            if "Review page" in row:
                row["Review page"] = "https://dhigdec.github.io/creative-ai-benchmark/gatsby-v7/#" + spec["new_id"]
            for column, field in brand_fields.items():
                if column in row:
                    row[column] = spec["brand_identity"][field]
        if row == original:
            result.extend(lines[start:end])
        else:
            stream = io.StringIO(newline="")
            newline = "\r\n" if lines[end - 1].endswith("\r\n") else "\n"
            writer = csv.writer(stream, lineterminator=newline)
            writer.writerow([row[column] for column in headers])
            result.append(stream.getvalue())
    reconcile(path, "".join(result), check)


def sync(check: bool = False) -> None:
    specs = {task_id: json.loads((TASKS / task_id / "TASK_SPEC.json").read_text()) for task_id in TASK_IDS}
    for task_id, spec in specs.items():
        folder = TASKS / task_id
        brief = f'# {spec["task_code"]} | {spec["task_name"]}\n\n{spec["client_brief"]}\n'
        reconcile(folder / "BRIEF.md", brief, check)
        brand_path = folder / "BRAND_IDENTITY.json"
        old_brand = json.loads(brand_path.read_text())
        brand = spec["brand_identity"]
        markdown = (folder / "BRAND_IDENTITY.md").read_text()
        for key, old_value in old_brand.items():
            if isinstance(old_value, str) and old_value != brand[key]:
                markdown = markdown.replace(old_value, brand[key])
        reconcile(folder / "BRAND_IDENTITY.md", markdown, check)
        reconcile(brand_path, json.dumps(brand, ensure_ascii=False, indent=2) + "\n", check)

    aggregate_path = PAGE / "TASKS_V5_ALL100.json"
    tasks = json.loads(aggregate_path.read_text())
    for task in tasks:
        if task["new_id"] in specs:
            spec = specs[task["new_id"]]
            task["client_brief"] = spec["client_brief"]
            task["brand_identity"] = deepcopy(spec["brand_identity"])
    reconcile(aggregate_path, json.dumps(tasks, ensure_ascii=False, indent=1), check)

    index_path = PAGE / "index.html"
    document = index_path.read_text()
    match = DATA_SCRIPT.search(document)
    if not match:
        raise ValueError("Cannot locate V7 task data")
    data = json.loads(match[2])
    for task in data["tasks"]:
        if task["id"] in specs:
            spec = specs[task["id"]]
            task["brief"] = spec["client_brief"]
            task["brand"] = deepcopy(spec["brand_identity"])
    serialized = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    reconcile(index_path, document[:match.start(2)] + serialized + document[match.end(2):], check)

    for name in ("photo-tasks.csv", "layout-tasks.csv", "task-register.csv", "brand-identity.csv"):
        sync_csv(PAGE / "data" / name, specs, check)
    print("All ten pilot brief/brand records are synchronized.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail on stale mirrors without writing files")
    sync(parser.parse_args().check)
