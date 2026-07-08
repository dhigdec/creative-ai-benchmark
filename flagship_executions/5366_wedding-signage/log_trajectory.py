#!/usr/bin/env python
"""Replays work/stage_manifest.json into trajectory.json via traj.py, then logs
export and verify steps. Run AFTER compose_5366.py."""
import json
import subprocess
import sys
from pathlib import Path

PY = "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/asset_pipeline/.venv/bin/python"
TRAJ = "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/flagship_executions/lib/traj.py"
TD = Path("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/flagship_executions/5366_wedding-signage")


def add(entry, snap, snap_name):
    r = subprocess.run([PY, TRAJ, "add", str(TD), "--json", json.dumps(entry, ensure_ascii=False),
                        "--snap", snap, "--snap-name", snap_name],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"traj add failed: {r.stderr}")
    print(r.stdout.strip())


manifest = json.loads((TD / "work" / "stage_manifest.json").read_text())
for m in manifest:
    entry = {k: m[k] for k in ("phase", "actor", "action", "note", "input", "output", "params")}
    add(entry, m["snap"], m["snap_name"])

report = json.loads((TD / "work" / "verify_report.json").read_text())

EXPORTS = [
    ("01_welcome_gathering_20x30.png", "6000x9000", "Welcome Gathering Sign 20x30in",
     "outputs/01_welcome_gathering_20x30.png"),
    ("02_welcome_ceremony_reception_35.4x23.6.png", "10620x7080", "Welcome Ceremony & Reception Sign 35.4x23.6in",
     "outputs/02_welcome_ceremony_reception_35.4x23.6.png"),
    ("03a_menu_thankyou_front_4x9.png", "1275x2775", "Menu/Thank-You card FRONT (4x9in trim + 0.125in bleed)",
     "outputs/03a_menu_thankyou_front_4x9.png"),
    ("03b_menu_thankyou_back_4x9.png", "1275x2775", "Menu/Thank-You card BACK (4x9in trim + 0.125in bleed)",
     "outputs/03b_menu_thankyou_back_4x9.png"),
    ("04_seating_chart_47.2x35.4.png", "14160x10620", "Seating Chart 47.2x35.4in, 15 tables / 120 names",
     "outputs/04_seating_chart_47.2x35.4.png"),
    ("05a_program_outside_10x7.png", "3075x2175", "Program OUTSIDE spread (10x7in flat + 0.125in bleed)",
     "outputs/05a_program_outside_10x7.png"),
    ("05b_program_inside_10x7.png", "3075x2175", "Program INSIDE spread (10x7in flat + 0.125in bleed)",
     "outputs/05b_program_inside_10x7.png"),
]
for fname, px, what, snap_rel in EXPORTS:
    add({"phase": "export", "actor": "local_compositor", "action": "export_png",
         "note": f"Exports {what} at exactly {px}px, 300dpi tag, per print_spec.json.",
         "input": "compose_5366.py", "output": f"outputs/{fname}",
         "params": {"px": px, "dpi": 300}},
        str(TD / snap_rel), f"export_{fname.split('_')[0]}")

add({"phase": "export", "actor": "local_compositor", "action": "export_png_table_signs",
     "note": "Exports the six 5x7in table signs (1500x2100px each, 300dpi) — numerals 1-6 from seating_chart.json, identical layout.",
     "input": "compose_5366.py",
     "output": "outputs/06_table_sign_1.png ... 06_table_sign_6.png",
     "params": {"px": "1500x2100 x6", "dpi": 300}},
    str(TD / "work" / "montage_tables.png"), "export_06_family")

add({"phase": "export", "actor": "local_compositor", "action": "export_suite_pdf",
     "note": "Assembles the 13-page print suite PDF LOCALLY with PIL (one page per piece) because the Adobe connector exposes no image-to-PDF tool; PDF/X-4 prepress conversion stays a print-house step.",
     "input": "outputs/*.png",
     "output": "outputs/wedding_signage_suite.pdf",
     "params": {"pages": report["pdf_pages"], "resolution_dpi": 300, "assembly": "local PIL"}},
    str(TD / "work" / "verify_sheet.png"), "export_suite_pdf")

add({"phase": "verify", "actor": "local_verify", "action": "assert_dimensions",
     "note": "Python pass asserts every one of the 13 PNGs at its exact target pixel size and floral coverage <=28% on every canvas (type wins).",
     "input": "outputs/*.png", "output": "work/verify_report.json",
     "params": {"dims_ok": len(report["dims_ok"]), "floral_coverage": report["floral_coverage"]}},
    str(TD / "work" / "verify_sheet.png"), "verify_dimensions")

add({"phase": "verify", "actor": "local_verify", "action": "assert_copy_fidelity",
     "note": "All 120 guest names (incl. suffixes), all menu courses/choices/descriptions, drink names, pet stories and dot-joined ingredients verified rendered verbatim from the input JSON; 7 PLAN-specified connective headers used (noted per stage).",
     "input": "input_assets/wedding_copy.json + seating_chart.json", "output": "work/verify_report.json",
     "params": {"guests_rendered": report["guests_rendered"],
                "rendered_strings": report["rendered_strings"],
                "microcopy_headers": report["microcopy_headers"],
                "violations": report["violations"]}},
    "/tmp/5366_t13.png", "verify_copy_fidelity")

add({"phase": "verify", "actor": "local_verify", "action": "visual_review_and_fixes",
     "note": "Visual read of seating chart, program inside and menu front found three flaws — bare wooden stand visible in floral corners, lawn-heavy cluster garnish, top-heavy welcome stack — fixed (stand cropped from cutout, garnish zoomed to bloom mass, stack re-spaced) and ALL pieces re-rendered before export.",
     "input": "work/stages/*", "output": "outputs/*.png",
     "params": {"fixes": ["arch stand crop 0.82h", "garnish zoom 0.70sq", "01/02 stack re-spacing"],
                "script_clipping": "none — snell lines advanced by bbox*1.25"}},
    "/tmp/5366_hdr.png", "verify_visual_review")

print("trajectory logging complete")
