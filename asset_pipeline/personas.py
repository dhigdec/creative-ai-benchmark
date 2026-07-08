"""Stage 1 — synthesize the simulated client (brand persona) per task.
Cached as persona.json in the task folder so every asset/retry stays on-brand."""
from __future__ import annotations
import json
from pathlib import Path

from util import write_json, read_json

SAFE_FONTS = ["Archivo", "Inter", "Fraunces", "Source Serif Pro", "Work Sans",
              "Libre Franklin", "Manrope", "Lora", "DM Sans", "Bitter"]

SCHEMA_HINT = """{
  "brand_name": "<short, pronounceable, NO real-world trademark>",
  "tagline": "<6 words max>",
  "industry": "<specific niche>",
  "palette": [{"name": "...", "hex": "#RRGGBB", "role": "primary|secondary|accent"}],
  "fonts": {"heading": "<one of: %s>", "body": "<one of the same list>"},
  "voice": "<2 sentences on tone>",
  "logo_style_brief": "<1-2 sentences: what the logo should look like>",
  "photo_style_tokens": "<comma phrase injected into every photo prompt for visual consistency, e.g. 'warm terracotta surfaces, soft window light, muted earth tones, 35mm look'>",
  "facts_from_brief": {"<fact>": "<value taken verbatim from the client brief>"},
  "invented": ["<list every detail you invented>"],
  "photo_plan": [<OPTIONAL — only if asked: list of photo subject descriptions>]
}""" % ", ".join(SAFE_FONTS)


def ensure_persona(task_dir: Path, spec: dict, record: dict, llm, logger, force: bool = False) -> dict:
    pfile = Path(task_dir) / "persona.json"
    if pfile.exists() and not force:
        logger.log("persona: using cached persona.json")
        return read_json(pfile)

    p = spec["persona"]
    mode = p.get("mode", "invent")
    sys_prompt = (
        "You are a meticulous brand strategist creating a SIMULATED client for a design-pipeline test. "
        "The persona must be coherent, specific and tasteful — never generic. "
        "Brand name must not collide with any real company or trademark. "
        "Fonts MUST come from the allowed list. Output JSON matching exactly this shape:\n" + SCHEMA_HINT)
    user = "TASK CONTEXT (the freelance brief this client posted):\n%s\n\nDIRECTIVES:\n%s" % (
        (record.get("desc") or "")[:1500], p["directives"])
    if mode == "from_brief":
        user += ("\n\nMODE: from_brief — extract real facts from the brief into facts_from_brief "
                 "(business name, site, product domain) and invent ONLY what is missing.")
    else:
        user += "\n\nMODE: invent — the brief names no brand; invent everything coherently."

    persona = llm.complete_json(sys_prompt, user, temperature=0.9)
    # minimal validation + safe-font enforcement
    for k in ("brand_name", "palette", "fonts", "voice", "photo_style_tokens"):
        if k not in persona:
            raise RuntimeError("persona missing key %r" % k)
    for slot in ("heading", "body"):
        if persona["fonts"].get(slot) not in SAFE_FONTS:
            persona["fonts"][slot] = SAFE_FONTS[0]
    persona.setdefault("facts_from_brief", {})
    persona.setdefault("invented", [])
    write_json(pfile, persona)
    logger.log("persona: %s (%s) — %s" % (
        persona["brand_name"], persona.get("industry", "?"),
        ", ".join(c.get("hex", "?") for c in persona["palette"][:3])))
    return persona


def flat_fields(persona: dict) -> dict:
    """Flatten persona for str.format use inside prompt templates."""
    palette = persona.get("palette", [])
    return {
        "brand_name": persona.get("brand_name", ""),
        "tagline": persona.get("tagline", ""),
        "industry": persona.get("industry", ""),
        "voice": persona.get("voice", ""),
        "palette_hexes": ", ".join("%s (%s)" % (c.get("hex"), c.get("name")) for c in palette),
        "palette_hex_list": ", ".join(c.get("hex", "") for c in palette),
        "fonts_heading": persona.get("fonts", {}).get("heading", ""),
        "fonts_body": persona.get("fonts", {}).get("body", ""),
        "logo_style_brief": persona.get("logo_style_brief", ""),
        "photo_style_tokens": persona.get("photo_style_tokens", ""),
    }
