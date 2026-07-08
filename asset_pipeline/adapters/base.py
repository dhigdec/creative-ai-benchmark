"""Shared result type for image adapters."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class GenResult:
    data: bytes                 # raw image bytes (png/jpeg as produced)
    provider: str
    model: str
    final_prompt: str
    size: str                   # requested "WxH" (adapters normalize output to this)
    quality: str = None
    raw_meta: dict = field(default_factory=dict)
