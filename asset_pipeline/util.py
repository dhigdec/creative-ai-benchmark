"""Shared helpers: slugify, retry, files, cost meter, run logger."""
from __future__ import annotations
import base64
import hashlib
import json
import re
import time
from pathlib import Path


def slugify(s: str, maxlen: int = 40) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return s[:maxlen].rstrip("-") or "item"


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def b64_to_file(b64: str, path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(b64))
    return path


def write_json(path, obj) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False))


def read_json(path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text())


def extract_json(text: str):
    """Parse JSON out of an LLM reply that may carry fences/prose."""
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if m:
        text = m.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = min((i for i in (text.find("{"), text.find("[")) if i >= 0), default=-1)
        if start >= 0:
            for end in range(len(text), start, -1):
                try:
                    return json.loads(text[start:end])
                except json.JSONDecodeError:
                    continue
    raise ValueError("no parseable JSON in reply (first 200 chars): %r" % text[:200])


def retry(fn, attempts: int = 3, base_delay: float = 2.0, retriable=(Exception,), logger=None):
    """Call fn() with exponential backoff. Honors exc.retry_after if present."""
    last = None
    for i in range(attempts):
        try:
            return fn()
        except retriable as e:  # noqa: PERF203
            last = e
            if i == attempts - 1:
                break
            delay = getattr(e, "retry_after", None) or base_delay * (2 ** i)
            delay = min(float(delay) + 0.5 * i, 30.0)
            if logger:
                logger.log("retry %d/%d after error: %s (sleep %.1fs)" % (i + 1, attempts, str(e)[:160], delay))
            time.sleep(delay)
    raise last


class CostMeter:
    def __init__(self):
        self.usd = 0.0
        self.images = 0
        self.text_calls = 0

    def add_image(self, usd: float):
        self.usd += usd
        self.images += 1

    def add_text(self, usd: float):
        self.usd += usd
        self.text_calls += 1

    def add_media(self, usd: float):
        self.usd += usd
        self.media = getattr(self, "media", 0) + 1


class RunLogger:
    """Tee to stdout + per-task run.log. Never log key material."""

    def __init__(self, logfile=None, quiet: bool = False):
        self.logfile = Path(logfile) if logfile else None
        self.quiet = quiet
        if self.logfile:
            self.logfile.parent.mkdir(parents=True, exist_ok=True)

    def log(self, msg: str):
        line = "[%s] %s" % (time.strftime("%H:%M:%S"), msg)
        if not self.quiet:
            print(line, flush=True)
        if self.logfile:
            with open(self.logfile, "a") as f:
                f.write(line + "\n")
