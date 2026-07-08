"""Text + vision-judge adapter with a gemini -> openai -> anthropic chain.
complete()/complete_json() for writing; review_image() for QC scoring."""
from __future__ import annotations
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config  # noqa: E402
from util import extract_json  # noqa: E402


class TextLLM:
    def __init__(self, logger=None):
        self.logger = logger
        self.last_used = None   # "provider/model" of the most recent successful call
        self._gem = None
        self._oai = None
        self._ant = None

    # ---- lazy clients ----
    def _gemini(self):
        if self._gem is None and config.PROVIDERS["gemini"]:
            from google import genai
            self._gem = genai.Client(api_key=config.KEYS["gemini"])
        return self._gem

    def _openai(self):
        if self._oai is None and config.PROVIDERS["openai"]:
            from openai import OpenAI
            self._oai = OpenAI(api_key=config.KEYS["openai"])
        return self._oai

    def _anthropic(self):
        if self._ant is None and config.PROVIDERS["anthropic"]:
            try:
                import anthropic
                self._ant = anthropic.Anthropic(api_key=config.KEYS["anthropic"])
            except ImportError:
                return None
        return self._ant

    def _chain(self, role: str, prefer: str = None, avoid: str = None):
        provs = []
        for prov, model, _ in config.MODELS.get(role, []):
            if config.PROVIDERS.get(prov) and prov not in provs:
                provs.append((prov, model))
        if prefer:
            provs.sort(key=lambda pm: 0 if pm[0] == prefer else 1)
        if avoid and len([p for p in provs if p[0] != avoid]) > 0:
            provs.sort(key=lambda pm: 1 if pm[0] == avoid else 0)
        return provs

    # ---- text ----
    def complete(self, system: str, user: str, role: str = "writer",
                 prefer: str = None, temperature: float = 0.8) -> str:
        errs = []
        for prov, model in self._chain(role, prefer=prefer):
            try:
                if prov == "gemini":
                    from google.genai import types
                    resp = self._gemini().models.generate_content(
                        model=model, contents=user,
                        config=types.GenerateContentConfig(
                            system_instruction=system or None, temperature=temperature))
                    if resp.text:
                        self.last_used = "%s/%s" % (prov, model)
                        return resp.text
                    raise RuntimeError("empty gemini reply")
                if prov == "openai":
                    msgs = ([{"role": "system", "content": system}] if system else []) + \
                           [{"role": "user", "content": user}]
                    r = self._openai().chat.completions.create(
                        model=model, messages=msgs, temperature=temperature)
                    self.last_used = "%s/%s" % (prov, model)
                    return r.choices[0].message.content
                if prov == "anthropic":
                    cli = self._anthropic()
                    if not cli:
                        continue
                    r = cli.messages.create(model=model, max_tokens=4096,
                                            system=system or "", temperature=temperature,
                                            messages=[{"role": "user", "content": user}])
                    self.last_used = "%s/%s" % (prov, model)
                    return r.content[0].text
            except Exception as e:  # noqa: PERF203
                errs.append("%s: %s" % (prov, str(e)[:160]))
                if self.logger:
                    self.logger.log("text %s failed -> next provider (%s)" % (prov, str(e)[:120]))
        raise RuntimeError("all text providers failed: %s" % "; ".join(errs))

    def complete_json(self, system: str, user: str, **kw):
        sys_j = (system or "") + "\nReturn ONLY valid JSON. No prose, no markdown fences."
        txt = self.complete(sys_j, user, **kw)
        try:
            return extract_json(txt)
        except ValueError:
            txt = self.complete(sys_j, user + "\n\nREMINDER: reply with ONLY the JSON object.",
                                **dict(kw, temperature=0.4))
            return extract_json(txt)

    # ---- vision QC ----
    def review_image(self, image_path, criteria: str, avoid_provider: str = None) -> dict:
        """Score an image 0-10 against criteria. Returns {score, issues[], text_found}."""
        img = Path(image_path).read_bytes()
        mime = "image/png" if str(image_path).lower().endswith("png") else "image/jpeg"
        ask = ("You are a strict art director QCing an AI-generated asset before client delivery.\n"
               "CRITERIA:\n%s\n\nScore 0-10 (10 = flawless for the criteria; below 7 = must regenerate). "
               "List concrete issues. Transcribe any text visible in the image EXACTLY.\n"
               'Return ONLY JSON: {"score": <int>, "issues": ["..."], "text_found": "..."}' % criteria)
        errs = []
        for prov, model in self._chain("judge", avoid=avoid_provider):
            try:
                if prov == "gemini":
                    from google.genai import types
                    resp = self._gemini().models.generate_content(
                        model=model,
                        contents=[types.Part.from_bytes(data=img, mime_type=mime), ask],
                        config=types.GenerateContentConfig(temperature=0.2))
                    out = extract_json(resp.text or "")
                elif prov == "openai":
                    r = self._openai().chat.completions.create(
                        model=model, temperature=0.2,
                        messages=[{"role": "user", "content": [
                            {"type": "text", "text": ask},
                            {"type": "image_url", "image_url": {"url": "data:%s;base64,%s" % (
                                mime, base64.b64encode(img).decode())}}]}])
                    out = extract_json(r.choices[0].message.content)
                else:
                    continue
                out["judge"] = "%s/%s" % (prov, model)
                out["score"] = int(out.get("score", 0))
                out.setdefault("issues", [])
                return out
            except Exception as e:  # noqa: PERF203
                errs.append("%s: %s" % (prov, str(e)[:140]))
        raise RuntimeError("all judges failed: %s" % "; ".join(errs))
