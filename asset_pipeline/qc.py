"""QC: L1 technical checks (free, always) + L2 vision-judge scoring."""
from __future__ import annotations
from pathlib import Path

from PIL import Image, ImageStat

import config


def technical(path, expect_size: str = None, expect_alpha: bool = False,
              messy_background: bool = False):
    """Returns (ok: bool, issues: list[str])."""
    issues = []
    p = Path(path)
    if not p.exists():
        return False, ["file missing"]
    if p.stat().st_size < 10_000:
        issues.append("file suspiciously small (%d bytes)" % p.stat().st_size)
    try:
        im = Image.open(p)
        im.load()
    except Exception as e:
        return False, ["unreadable image: %s" % e]
    if expect_size:
        w, h = (int(x) for x in expect_size.split("x"))
        if im.size != (w, h):
            issues.append("dims %sx%s != expected %s" % (im.width, im.height, expect_size))
    if expect_alpha and im.mode not in ("RGBA", "LA"):
        issues.append("no alpha channel (expected transparent background)")
    # near-uniform detector (blank/failed gens) — lenient for flat logos
    stat = ImageStat.Stat(im.convert("L"))
    if stat.stddev[0] < 3.0:
        issues.append("image is near-uniform (stddev %.1f) — likely a failed generation" % stat.stddev[0])
    if messy_background:
        # 5649: inputs must NOT have a clean white/seamless background — sample a border ring
        rgb = im.convert("RGB")
        w, h = rgb.size
        ring = 12
        samples = []
        for box in ((0, 0, w, ring), (0, h - ring, w, h), (0, 0, ring, h), (w - ring, 0, w, h)):
            region = rgb.crop(box)
            s = ImageStat.Stat(region)
            samples.append((sum(s.mean) / 3.0, sum(s.stddev) / 3.0))
        mean = sum(m for m, _ in samples) / len(samples)
        std = sum(s for _, s in samples) / len(samples)
        if mean > 232 and std < 16:
            issues.append("background looks like a clean white studio sweep (mean %.0f, std %.0f) — "
                          "brief requires messy phone-photo background" % (mean, std))
    return (len(issues) == 0), issues


def vision(llm, path, criteria: str, generator_provider: str = None) -> dict:
    """L2 judge. Prefers a different provider than the generator. Returns
    {score, issues, text_found, judge}."""
    return llm.review_image(path, criteria, avoid_provider=generator_provider)


def passes(review: dict, min_score: int = None) -> bool:
    return int(review.get("score", 0)) >= (min_score or config.QC_MIN_SCORE)
