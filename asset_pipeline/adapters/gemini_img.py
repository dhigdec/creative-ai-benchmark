"""Gemini image adapter: gemini-2.5-flash-image (via generate_content) and
imagen-4 (via generate_images). REST fallback for environments where the
google-genai SDK can't import. Output is normalized to the requested WxH via PIL."""
from __future__ import annotations
import base64
import io
import json

from .base import GenResult

# nearest supported aspect ratio per requested size
ASPECT = {"1024x1024": "1:1", "1024x1536": "3:4", "1536x1024": "4:3"}


def _normalize(data: bytes, size: str) -> bytes:
    """Cover-crop/resize to exactly WxH; keeps PNG if source had alpha."""
    from PIL import Image
    w, h = (int(x) for x in size.split("x"))
    im = Image.open(io.BytesIO(data))
    has_alpha = im.mode in ("RGBA", "LA")
    if im.size != (w, h):
        scale = max(w / im.width, h / im.height)
        nw, nh = max(w, round(im.width * scale)), max(h, round(im.height * scale))
        im = im.resize((nw, nh), Image.LANCZOS)
        left, top = (nw - w) // 2, (nh - h) // 2
        im = im.crop((left, top, left + w, top + h))
    buf = io.BytesIO()
    if has_alpha:
        im.save(buf, "PNG")
    else:
        im.convert("RGB").save(buf, "PNG")
    return buf.getvalue()


class GeminiImageAdapter:
    provider = "gemini"

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash-image", logger=None):
        self.api_key = api_key
        self.model = model
        self.logger = logger
        self._client = None
        self._sdk = None  # True/False once probed

    def _ensure_client(self):
        if self._sdk is None:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
                self._sdk = True
            except Exception as e:
                if self.logger:
                    self.logger.log("google-genai SDK unavailable (%s) -> REST fallback" % str(e)[:120])
                self._sdk = False
        return self._sdk

    def generate(self, prompt: str, size: str = "1024x1024", n: int = 1, background: str = None):
        if background == "transparent" and self.logger:
            self.logger.log("WARN: gemini path cannot guarantee transparent background; generating opaque")
        outs = []
        for _ in range(n):
            if self._ensure_client():
                raw = (self._imagen_sdk(prompt, size) if self.model.startswith("imagen")
                       else self._flash_sdk(prompt, size))
            else:
                raw = self._flash_rest(prompt)
            outs.append(GenResult(
                data=_normalize(raw, size), provider=self.provider, model=self.model,
                final_prompt=prompt, size=size, raw_meta={}))
        return outs

    # ---- SDK paths ----
    def _flash_sdk(self, prompt: str, size: str) -> bytes:
        from google.genai import types
        cfg_kwargs = dict(response_modalities=["TEXT", "IMAGE"])
        ar = ASPECT.get(size, "1:1")
        cfg = None
        if "3-pro" in self.model or "banana-pro" in self.model:
            try:  # Nano Banana Pro: request 2K detail tier when the SDK supports it
                cfg = types.GenerateContentConfig(
                    image_config=types.ImageConfig(aspect_ratio=ar, image_size="2K"), **cfg_kwargs)
            except Exception:  # older SDKs: pydantic extra_forbidden, TypeError, etc.
                cfg = None
        if cfg is None:
            try:  # aspect ratio only
                cfg = types.GenerateContentConfig(
                    image_config=types.ImageConfig(aspect_ratio=ar), **cfg_kwargs)
            except Exception:
                cfg = types.GenerateContentConfig(**cfg_kwargs)
        resp = self._client.models.generate_content(model=self.model, contents=prompt, config=cfg)
        for cand in (resp.candidates or []):
            for part in (cand.content.parts or []):
                inline = getattr(part, "inline_data", None)
                if inline and inline.data:
                    return inline.data if isinstance(inline.data, bytes) else base64.b64decode(inline.data)
        block = getattr(getattr(resp, "prompt_feedback", None), "block_reason", None)
        raise RuntimeError("gemini flash-image returned no image%s" %
                           (" (blocked: %s)" % block if block else ""))

    def _imagen_sdk(self, prompt: str, size: str) -> bytes:
        from google.genai import types
        resp = self._client.models.generate_images(
            model=self.model, prompt=prompt,
            config=types.GenerateImagesConfig(number_of_images=1, aspect_ratio=ASPECT.get(size, "1:1")))
        imgs = getattr(resp, "generated_images", None) or []
        if not imgs:
            raise RuntimeError("imagen returned no image")
        img = imgs[0].image
        data = getattr(img, "image_bytes", None)
        if data is None:
            raise RuntimeError("imagen response had no image_bytes")
        return data if isinstance(data, bytes) else base64.b64decode(data)

    # ---- REST fallback (generate_content only) ----
    def _flash_rest(self, prompt: str) -> bytes:
        import requests
        model = self.model if not self.model.startswith("imagen") else "gemini-2.5-flash-image"
        url = ("https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % model)
        body = {"contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}}
        r = requests.post(url, headers={"x-goog-api-key": self.api_key,
                                        "Content-Type": "application/json"},
                          data=json.dumps(body), timeout=120)
        if r.status_code == 429:
            err = RuntimeError("gemini REST 429 rate-limited")
            err.retry_after = int(r.headers.get("Retry-After", "8"))
            raise err
        r.raise_for_status()
        for cand in r.json().get("candidates", []):
            for part in cand.get("content", {}).get("parts", []):
                inline = part.get("inlineData") or part.get("inline_data")
                if inline and inline.get("data"):
                    return base64.b64decode(inline["data"])
        raise RuntimeError("gemini REST returned no image")
