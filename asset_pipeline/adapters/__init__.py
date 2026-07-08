"""Adapter factories. Resolution order lives in config.MODELS."""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config  # noqa: E402


def get_image_adapter(role: str, only_provider: str = None, logger=None):
    """Return (adapter, provider, model, quality) for the first servable candidate."""
    from . import openai_img, gemini_img
    r = config.resolve(role, only_provider)
    if not r:
        raise RuntimeError(
            "No provider available for image role %r (keys: %s)" % (role, config.PROVIDERS))
    prov, model, quality = r
    if prov == "openai":
        return openai_img.OpenAIImageAdapter(config.KEYS["openai"], model, quality, logger), prov, model, quality
    return gemini_img.GeminiImageAdapter(config.KEYS["gemini"], model, logger), prov, model, quality


def get_image_chain(role: str, only_provider: str = None, logger=None):
    """All servable candidates for a role, in order — for fallback on hard errors."""
    from . import openai_img, gemini_img
    out = []
    for prov, model, quality in config.MODELS.get(role, []):
        if only_provider and prov != only_provider:
            continue
        if not config.PROVIDERS.get(prov):
            continue
        if prov == "openai":
            out.append((openai_img.OpenAIImageAdapter(config.KEYS["openai"], model, quality, logger), prov, model, quality))
        else:
            out.append((gemini_img.GeminiImageAdapter(config.KEYS["gemini"], model, logger), prov, model, quality))
    return out
