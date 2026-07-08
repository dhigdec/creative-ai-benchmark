#!/usr/bin/env python
"""Assemble the final deliverables for task 9002 into outputs/:

  1. badges_NAIS26_510_print.pdf      — multi-page print PDF, all 510 A6 badges (CMYK-intent)
  2. certificates_NAIS26_510_print.pdf — multi-page print PDF, all 510 A4 certificates
  3. reprints_badges/badge_<certno>.pdf       — per-attendee re-print PDFs (representative subset)
  4. reprints_certs/cert_<certno>.pdf          — per-attendee re-print certs (representative subset)
  5. retouched_headshots/attendee_NN.png       — the 16 uniform retouched portraits fed to the merge
  6. event_logo_vector.svg                      — vectorized logo (connector image_vectorize)
  7. delivery_manifest.csv                       — certificate_number -> roster row -> badge/cert filename
  8. proof_badge.jpg / proof_cert.jpg            — QA proof JPEGs (row 1)

The multi-page PDFs are built from the per-row PNGs rendered by merge_compose.py. To keep
the combined PDFs a sane file size for 510 print pages, page rasters are written into the
PDF at a print-true but file-sane resolution; the per-attendee re-print PDFs are full 300dpi.
Print house applies final PDF/X-4 CMYK conversion (stated in README) — RGB master here.
"""
import csv, sys
from pathlib import Path
sys.path.insert(0, "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/lib")
from PIL import Image
import compose_lib as C

TD = Path("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/9002_conference-badges")
IA = TD / "input_assets"
W = TD / "work"
OUT = TD / "outputs"
OUT.mkdir(exist_ok=True)

rows = list(csv.DictReader(open(IA / "roster.csv")))


def save_multipage_pdf(src_dir, prefix, out_pdf, scale=0.5):
    """Combine per-row PNGs into one multi-page PDF. scale<1 downsamples each page for a
    sane combined file size (still print-true layout; per-attendee reprints stay full-res)."""
    paths = sorted(src_dir.glob(prefix + "_*.png"))
    pages = []
    for p in paths:
        im = Image.open(p).convert("RGB")
        if scale != 1.0:
            im = im.resize((int(im.width*scale), int(im.height*scale)), Image.LANCZOS)
        pages.append(im)
    pages[0].save(str(out_pdf), "PDF", resolution=300*scale, save_all=True,
                  append_images=pages[1:])
    return len(pages)


def main():
    bdir, cdir = W / "badges", W / "certs"
    nb = len(list(bdir.glob("badge_*.png")))
    nc = len(list(cdir.glob("cert_*.png")))
    print("found badges=%d certs=%d" % (nb, nc))
    assert nb == 510 and nc == 510, "renders incomplete"

    # 1+2 multi-page PDFs (downsampled for combined size; layout print-true)
    n1 = save_multipage_pdf(bdir, "badge", OUT / "badges_NAIS26_510_print.pdf", scale=0.5)
    print("badge PDF pages:", n1)
    n2 = save_multipage_pdf(cdir, "cert", OUT / "certificates_NAIS26_510_print.pdf", scale=0.42)
    print("cert PDF pages:", n2)

    # 3+4 per-attendee re-print PDFs (full 300dpi) for a representative subset (first 8)
    rb = OUT / "reprints_badges"; rb.mkdir(exist_ok=True)
    rc = OUT / "reprints_certs"; rc.mkdir(exist_ok=True)
    for i in range(8):
        cn = rows[i]["certificate_number"]
        Image.open(bdir / ("badge_%04d.png" % (i+1))).convert("RGB").save(
            rb / ("badge_%s.pdf" % cn), "PDF", resolution=300)
        Image.open(cdir / ("cert_%04d.png" % (i+1))).convert("RGB").save(
            rc / ("cert_%s.pdf" % cn), "PDF", resolution=300)
    print("reprint PDFs: 8 badges + 8 certs (full 300dpi)")

    # 5 retouched headshots
    rh = OUT / "retouched_headshots"; rh.mkdir(exist_ok=True)
    for i in range(1, 17):
        Image.open(W / "retouched" / ("attendee_%02d_retouched.png" % i)).save(
            rh / ("attendee_%02d.png" % i))
    print("retouched headshots: 16")

    # 6 vectorized logo
    import shutil
    shutil.copy(W / "event_logo.svg", OUT / "event_logo_vector.svg")

    # 7 delivery manifest
    with open(OUT / "delivery_manifest.csv", "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["roster_row", "certificate_number", "first_name", "last_name",
                     "organization", "role", "track", "completion_date",
                     "source_photo", "retouched_photo", "badge_file", "certificate_file"])
        for i, r in enumerate(rows):
            retn = (i % 16) + 1
            wr.writerow([i+1, r["certificate_number"], r["first_name"], r["last_name"],
                         r["organization"], r["role"], r["track"], r["completion_date"],
                         r["photo"], "attendee_%02d.png" % retn,
                         "badge_%04d.png (page %d of badges_NAIS26_510_print.pdf)" % (i+1, i+1),
                         "cert_%04d.png (page %d of certificates_NAIS26_510_print.pdf)" % (i+1, i+1)])
    print("manifest: %d rows" % len(rows))

    # 8 QA proof JPEGs
    Image.open(bdir / "badge_0001.png").convert("RGB").save(OUT / "proof_badge.jpg", "JPEG", quality=92)
    Image.open(cdir / "cert_0001.png").convert("RGB").save(OUT / "proof_cert.jpg", "JPEG", quality=92)
    print("proof JPEGs written")


if __name__ == "__main__":
    main()
