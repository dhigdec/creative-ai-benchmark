"""Polite HTTP layer: token-bucket rate limiting + exponential backoff with jitter.

This is the safety core. Every outbound request goes through a per-source TokenBucket and a
PoliteSession that backs off on 429/5xx (honoring Retry-After), enforces a daily cap, and
surfaces 403s clearly instead of hammering.
"""
import time
import random
import logging
import threading

import requests

log = logging.getLogger("pipeline.http")


class TokenBucket:
    """Classic token bucket. acquire() blocks until a token is available."""

    def __init__(self, rate_per_sec, burst=1):
        self.rate = float(rate_per_sec)
        self.capacity = float(max(burst, 1))
        self.tokens = self.capacity
        self.timestamp = time.monotonic()
        self.lock = threading.Lock()

    def acquire(self, n=1):
        while True:
            with self.lock:
                now = time.monotonic()
                self.tokens = min(self.capacity, self.tokens + (now - self.timestamp) * self.rate)
                self.timestamp = now
                if self.tokens >= n:
                    self.tokens -= n
                    return
                deficit = n - self.tokens
            time.sleep(max(deficit / self.rate, 0.01))


class BlockedError(Exception):
    """Raised on 403 — likely a block or missing auth. Stop, don't retry."""


class PoliteSession:
    def __init__(self, bucket, user_agent, max_retries=5, timeout=45, daily_cap=None):
        self.bucket = bucket
        self.max_retries = max_retries
        self.timeout = timeout
        self.daily_cap = daily_cap
        self.calls = 0
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": user_agent, "Accept": "application/json"})

    def _cap(self):
        if self.daily_cap is not None and self.calls >= self.daily_cap:
            raise RuntimeError("daily_cap reached (%d) — stopping politely" % self.daily_cap)

    def _backoff(self, attempt, retry_after):
        if retry_after:
            try:
                delay = float(retry_after)
            except (TypeError, ValueError):
                delay = 2 ** attempt
        else:
            delay = min(60.0, 2.0 ** attempt)
        delay += random.uniform(0, delay * 0.3)  # jitter avoids thundering herd
        log.warning("backoff %.1fs (attempt %d)", delay, attempt)
        time.sleep(delay)

    def request(self, method, url, **kw):
        self._cap()
        attempt = 0
        while True:
            self.bucket.acquire()
            self.calls += 1
            try:
                r = self.s.request(method, url, timeout=self.timeout, **kw)
            except requests.RequestException as e:
                attempt += 1
                if attempt > self.max_retries:
                    raise
                log.warning("network error %s — retrying", e)
                self._backoff(attempt, None)
                continue
            if r.status_code in (429, 500, 502, 503, 504):
                attempt += 1
                if attempt > self.max_retries:
                    r.raise_for_status()
                self._backoff(attempt, r.headers.get("Retry-After"))
                continue
            if r.status_code == 403:
                raise BlockedError("403 Forbidden from %s (possible block or auth required)" % url)
            r.raise_for_status()
            return r

    def get_json(self, url, params=None, headers=None):
        return self.request("GET", url, params=params, headers=headers).json()

    def get_text(self, url, params=None, headers=None):
        h = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
        if headers:
            h.update(headers)
        return self.request("GET", url, params=params, headers=h).text

    def post_json(self, url, json=None, headers=None, data=None):
        return self.request("POST", url, json=json, data=data, headers=headers).json()
