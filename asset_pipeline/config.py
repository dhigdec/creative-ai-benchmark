"""Config: env/keys, model candidate registry, prices, caps.
The ONLY file to touch when model ids drift."""
from __future__ import annotations
import os
from pathlib import Path

PIPE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = PIPE_DIR.parent
DATASET = PROJECT_DIR / "adobe_doable_full.json"
OUT_ROOT = PROJECT_DIR / "input_assets"

try:
    from dotenv import load_dotenv
    load_dotenv(PIPE_DIR / ".env")
except ImportError:
    pass  # --check will still report keys missing

KEYS = {
    "gemini": os.environ.get("GEMINI_API_KEY", "").strip(),
    "openai": os.environ.get("OPENAI_API_KEY", "").strip(),
    "anthropic": os.environ.get("ANTHROPIC_API_KEY", "").strip(),
}
PROVIDERS = {k: bool(v) for k, v in KEYS.items()}

# Candidate lists per logical role — first entry whose provider has a key wins.
# Format: (provider, model, quality_or_None)
MODELS = {
    "image_photoreal": [
        ("openai", "gpt-image-1", "high"),
        ("gemini", "imagen-4.0-generate-001", None),
        ("gemini", "gemini-2.5-flash-image", None),
    ],
    "image_logo": [
        ("openai", "gpt-image-1", "high"),
        ("gemini", "gemini-2.5-flash-image", None),
    ],
    "image_cheap": [
        ("gemini", "gemini-2.5-flash-image", None),
        ("openai", "gpt-image-1", "medium"),
    ],
    "writer": [
        ("gemini", "gemini-2.5-flash", None),
        ("openai", "gpt-4.1-mini", None),
        ("anthropic", "claude-sonnet-4-6", None),
    ],
    "judge": [  # vision QC — orchestrator prefers a DIFFERENT provider than the generator
        ("gemini", "gemini-2.5-flash", None),
        ("openai", "gpt-4.1-mini", None),
    ],
    # ---- round-2 roles: top-tier models (probed available on both keys 2026-06-10) ----
    "image_hero_text": [   # text-bearing logos/heroes — Nano Banana Pro leads (SOTA text rendering)
        ("gemini", "gemini-3-pro-image", None),
        ("openai", "gpt-image-2", "high"),
        ("openai", "gpt-image-1", "high"),
    ],
    "image_photoreal2": [  # people/property/product photography — newest OpenAI flagship leads
        ("openai", "gpt-image-2", "high"),
        ("gemini", "gemini-3-pro-image", None),
        ("openai", "gpt-image-1", "high"),
    ],
    "image_cheap2": [
        ("gemini", "gemini-3.1-flash-image", None),
        ("gemini", "gemini-2.5-flash-image", None),
    ],
    # ---- video / audio roles (HQ-first, 2026-06-16: quality Veo @1080p, Sora-2-pro, clean TTS) ----
    "video": [("gemini", "veo-3.1-generate-preview", None), ("gemini", "veo-3.0-generate-001", None),
              ("openai", "sora-2-pro", None), ("openai", "sora-2", None)],
    "video_sora": [("openai", "sora-2-pro", None), ("openai", "sora-2", None)],
    "audio_vo": [("openai", "gpt-4o-mini-tts", None)],
    # ---- package judge: VISION-capable reasoners; one per provider (dedup at panel) ----
    # anthropic entry is inert until ANTHROPIC_API_KEY is set; then it auto-joins as 3rd judge.
    # Model ids verified at runtime; sonnet-4-6 is the default, bump to claude-opus-4-8 for max rigor.
    "package_judge": [
        ("anthropic", "claude-sonnet-4-6", None),
        ("gemini", "gemini-2.5-flash", None),
        ("openai", "gpt-4.1", None),
    ],
}

# USD estimates per image / per call — treated as ESTIMATES for the cost meter & gate.
PRICES = {
    "openai:gpt-image-1:high:1024x1024": 0.167,
    "openai:gpt-image-1:high:1024x1536": 0.25,
    "openai:gpt-image-1:high:1536x1024": 0.25,
    "openai:gpt-image-1:medium:1024x1024": 0.063,
    "openai:gpt-image-1:medium:1024x1536": 0.094,
    "gemini:gemini-2.5-flash-image": 0.039,
    "gemini:imagen-4.0-generate-001": 0.04,
    "gemini:gemini-3-pro-image": 0.134,        # Nano Banana Pro (1K/2K)
    "gemini:gemini-3.1-flash-image": 0.045,
    "openai:gpt-image-2:high:1024x1024": 0.19,
    "openai:gpt-image-2:high:1024x1536": 0.28,
    "openai:gpt-image-2:high:1536x1024": 0.28,
    "video:veo": 3.20,            # Veo 3.1/3.0 quality ~8s 1080p clip (est; ~2.7x the fast tier)
    "video:sora": 1.50,           # Sora-2-pro short clip (est)
    "audio:tts": 0.03,            # OpenAI gpt-4o-mini-tts clean 48k narration (est)
    "text_call": 0.002,           # flat rough estimate per writer/judge call
    "judge_call": 0.006,          # one package-judge vision call (multi-image, text out)
    "judge_image_surcharge": 0.0015,  # per image included in a judge call
}

MAX_IMAGES_PER_RUN = 60
COST_GATE_USD = 10.0   # confirm above this unless --yes
QC_MIN_SCORE = 7
QC_MAX_REGENS = 2


def image_price(provider: str, model: str, quality, size: str) -> float:
    if provider == "openai":
        q = quality or "high"
        return PRICES.get("openai:%s:%s:%s" % (model, q, size), 0.167)
    return PRICES.get("%s:%s" % (provider, model), 0.04)


def resolve(role: str, only_provider: str = None):
    """First (provider, model, quality) in the role's list whose key exists."""
    for prov, model, quality in MODELS.get(role, []):
        if only_provider and prov != only_provider:
            continue
        if PROVIDERS.get(prov):
            return prov, model, quality
    return None


def key_matrix() -> str:
    lines = ["Provider keys: " + ", ".join(
        "%s=%s" % (k, "set" if v else "MISSING") for k, v in PROVIDERS.items())]
    for role in MODELS:
        r = resolve(role)
        lines.append("  %-16s -> %s" % (role, ("%s/%s%s" % (r[0], r[1], " (" + r[2] + ")" if r[2] else "")) if r else "UNSERVABLE"))
    return "\n".join(lines)
