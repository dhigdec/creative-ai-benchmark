"""OpenAI gpt-image-1 adapter (b64 responses)."""
from __future__ import annotations
import base64

from .base import GenResult

VALID_SIZES = {"1024x1024", "1536x1024", "1024x1536", "auto"}


class OpenAIImageAdapter:
    provider = "openai"

    def __init__(self, api_key: str, model: str = "gpt-image-1", quality: str = "high", logger=None):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.quality = quality or "high"
        self.logger = logger

    def generate(self, prompt: str, size: str = "1024x1024", n: int = 1, background: str = None):
        req_size = size if size in VALID_SIZES else "1024x1024"
        kwargs = dict(model=self.model, prompt=prompt, size=req_size, n=n, quality=self.quality)
        if background == "transparent":
            kwargs["background"] = "transparent"
            kwargs["output_format"] = "png"
        try:
            resp = self.client.images.generate(**kwargs)
        except Exception as e:
            msg = str(e)
            if "verified" in msg.lower() and "organization" in msg.lower():
                raise RuntimeError(
                    "gpt-image-1 requires a VERIFIED OpenAI organization "
                    "(platform.openai.com -> Settings -> Organization -> Verify). "
                    "Falling back to Gemini if available. Original: %s" % msg[:200])
            raise
        out = []
        for d in resp.data:
            out.append(GenResult(
                data=base64.b64decode(d.b64_json), provider=self.provider, model=self.model,
                final_prompt=prompt, size=req_size, quality=self.quality,
                raw_meta={"revised_prompt": getattr(d, "revised_prompt", None)}))
        return out
