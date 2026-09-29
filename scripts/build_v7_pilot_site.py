"""Publish only real V7 pilot artifacts into a separate Gatsby Pages view."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image


REPO = Path(__file__).resolve().parents[1]
WORKSPACE = REPO.parents[1]
RUNS = WORKSPACE / "benchmark_runs/pilot_v7_hybrid_2026-09-28"
TASKS = REPO / "docs/gatsby-v7/tasks"
SITE = REPO / "docs/gatsby-v7/pilot-2026-09-28"
PDFTOPPM = Path("/Users/dhiren/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm")
ORDER = ["PHOTO-04", "PHOTO-06", "PHOTO-08", "PHOTO-10", "PHOTO-19", "PHOTO-20", "PHOTO-24", "PHOTO-26", "PHOTO-28", "LAYOUT-15"]
DRIVE = {
    "PHOTO-04": "https://drive.google.com/drive/folders/16aIRVzOq0oKnX5nsJv6at185qosISaD9",
    "PHOTO-06": "https://drive.google.com/drive/folders/1QO0rSu6uQiD4W6evMronQ2iFzq4bKm10",
    "PHOTO-08": "https://drive.google.com/drive/folders/1C6aE6Nn3-xiRDRCqpuDoNcmv9dbPOigO",
    "PHOTO-10": "https://drive.google.com/drive/folders/19G-elQ-umq1Ddt_hzCDj5JCIP1xW7zea",
    "PHOTO-19": "https://drive.google.com/drive/folders/1Ac85m3qJQ5PhFRG8bki36KD32MPxcwHl",
    "PHOTO-20": "https://drive.google.com/drive/folders/15I5Wt5__sINg8HvGA4mK9jnK-41sKq0L",
    "PHOTO-24": "https://drive.google.com/drive/folders/1EPe-n-zi1VJouffI2x2Zr4zOlNkM7BW1",
    "PHOTO-26": "https://drive.google.com/drive/folders/1gpjquEk9H6mHj2R7vHi56J1p1klyohER",
    "PHOTO-28": "https://drive.google.com/drive/folders/1DfSmb1AiIHRpMG5g3kn7OEwpFrhAS_lc",
    "LAYOUT-15": "https://drive.google.com/drive/folders/1ifrchpccBfDdnVVlNPbokc0IbqKrZDTH",
}


def thumb(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix.lower() == ".pdf":
        subprocess.run(
            [str(PDFTOPPM), "-f", "1", "-l", "1", "-singlefile", "-scale-to", "680", "-jpeg", str(source), str(destination.with_suffix(""))],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return
    with Image.open(source) as original:
        image = original.convert("RGBA")
        image.thumbnail((680, 680), Image.Resampling.LANCZOS)
        frame = Image.new("RGBA", image.size, "white")
        frame.alpha_composite(image)
        frame.convert("RGB").save(destination, quality=86, optimize=True)


def build() -> None:
    SITE.mkdir(parents=True, exist_ok=True)
    data = []
    for code in ORDER:
        task = json.loads((TASKS / code / "TASK_SPEC.json").read_text())
        manifest_path = RUNS / code / "artifacts/DELIVERY_MANIFEST.json"
        expected = len(task["deliverables"])
        entry = {
            "code": code,
            "title": task["task_name"],
            "family": task["family"],
            "expected": expected,
            "brief_url": f"../#{code}",
            "drive_url": DRIVE.get(code),
            "execution": "Hybrid: Adobe connector edits + local Python layout",
            "outputs": [],
            "trajectory_url": None,
            "notes": [],
        }
        if manifest_path.is_file():
            manifest = json.loads(manifest_path.read_text())
            task_site = SITE / "runs" / code
            (task_site / "deliverables").mkdir(parents=True, exist_ok=True)
            (task_site / "thumbnails").mkdir(parents=True, exist_ok=True)
            for item in manifest.get("deliverables", []):
                for record in item.get("files", []):
                    name = record["filename"]
                    source = RUNS / code / "deliverables" / name
                    if not source.is_file():
                        continue
                    target = task_site / "deliverables" / name
                    shutil.copy2(source, target)
                    preview = task_site / "thumbnails" / f"{name}.jpg"
                    thumb(source, preview)
                    entry["outputs"].append({
                        "id": item["deliverable_id"],
                        "name": item["name"],
                        "file": name,
                        "url": f"runs/{code}/deliverables/{name}",
                        "preview": f"runs/{code}/thumbnails/{name}.jpg",
                        "format": source.suffix.lower().lstrip("."),
                        "size_mb": round(source.stat().st_size / 1_000_000, 1),
                        "note": item.get("notes", ""),
                    })
            for name in ["trajectory.html", "trajectory.json", "trajectory.jsonl", "verifier-results.json"]:
                path = RUNS / code / name
                if path.is_file():
                    shutil.copy2(path, task_site / name)
            if (RUNS / code / "previews").is_dir():
                shutil.copytree(RUNS / code / "previews", task_site / "previews", dirs_exist_ok=True)
            shutil.copy2(manifest_path, task_site / "DELIVERY_MANIFEST.json")
            if (task_site / "trajectory.html").is_file():
                entry["trajectory_url"] = f"runs/{code}/trajectory.html"
            entry["notes"] = [str(note.get("detail", "")) if isinstance(note, dict) else str(note) for note in manifest.get("declared_exceptions", [])]
        entry["status"] = "Delivered" if len(entry["outputs"]) == expected else "In progress"
        data.append(entry)
    (SITE / "data.js").write_text("window.PILOT_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")
    print(json.dumps({"tasks": len(data), "delivered_tasks": sum(item["status"] == "Delivered" for item in data), "files": sum(len(item["outputs"]) for item in data)}, indent=2))


if __name__ == "__main__":
    build()
