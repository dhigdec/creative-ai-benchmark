"""Asset-generation orchestrator.

Usage (from project root or anywhere):
  .venv/bin/python generate.py --check [--deep]
  .venv/bin/python generate.py --task 440 --dry-run
  .venv/bin/python generate.py --task 440
  .venv/bin/python generate.py --all-pilot [--yes]
Options: --force (regen everything), --asset KEY (regen one asset), --images-provider
openai|gemini, --skip-vision-qc, --quiet.
"""
from __future__ import annotations
import argparse
import io
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config  # noqa: E402
import qc  # noqa: E402
import degrade as degrade_mod  # noqa: E402
import manifest as manifest_mod  # noqa: E402
import contact_sheet  # noqa: E402
import specs as specs_mod  # noqa: E402
import personas  # noqa: E402
from adapters import get_image_chain  # noqa: E402
from adapters.text_llm import TextLLM  # noqa: E402
from util import (CostMeter, RunLogger, read_json, write_json, retry, extract_json)  # noqa: E402


class Ctx:
    def __init__(self, record, spec, persona):
        self.record = record
        self.spec = spec
        self.persona = persona
        self.flat = dict(personas.flat_fields(persona))
        self.flat["no_text"] = specs_mod.NO_TEXT
        self.flat["no_tm"] = specs_mod.NO_TM
        self.assets = {}
        self.scratch = {}


# --------------------------------------------------------------------------
def render_prompts(asset, ctx):
    n = asset.get("count", 1)
    if asset.get("prompt_fn"):
        ps = asset["prompt_fn"](ctx)
        if len(ps) != n:
            raise RuntimeError("%s: prompt_fn returned %d prompts for count=%d" % (asset["key"], len(ps), n))
        return ps
    tpl = asset["prompt"]
    return [tpl.format(**dict(ctx.flat, i=i + 1)) for i in range(n)]


def render_filenames(asset, ctx):
    n = asset.get("count", 1)
    if asset.get("filename_fn"):
        names = asset["filename_fn"](ctx)
        if len(names) != n:
            raise RuntimeError("%s: filename_fn returned %d names for count=%d" % (asset["key"], len(names), n))
        return names
    f = asset["filename"]
    if n == 1:
        return [f]
    return [f.format(i=i + 1) for i in range(n)]


def data_checks(obj, checks):
    """Raises RuntimeError on the first failed check. Supports:
      'field==N' / 'field>=N'  — list length
      'field[].sub'            — every item in obj[field] must have a non-empty 'sub'
    """
    EMPTY = (None, "", [], {})
    for c in checks or []:
        c = c.strip()
        if c == "json_valid":
            continue
        if "[]." in c:
            field, sub = c.split("[].", 1)
            items = obj.get(field.strip(), [])
            bad = [i for i, it in enumerate(items)
                   if not (isinstance(it, dict) and it.get(sub) not in EMPTY)]
            if bad:
                raise RuntimeError("data check failed: %s — records %s missing/empty '%s'" % (c, bad, sub))
            continue
        for op in ("==", ">="):
            if op in c:
                field, val = c.split(op)
                got = len(obj.get(field.strip(), []))
                want = int(val)
                ok = got == want if op == "==" else got >= want
                if not ok:
                    raise RuntimeError("data check failed: %s (got %d)" % (c, got))
                break


def render_md(obj, path: Path):
    lines = []
    if "items" in obj:  # menu
        lines.append("# %s — Menu" % obj.get("restaurant", ""))
        if obj.get("tagline"):
            lines.append("*%s*\n" % obj["tagline"])
        cats = {}
        for it in obj["items"]:
            cats.setdefault(it.get("category", "Menu"), []).append(it)
        for cat, items in cats.items():
            lines.append("\n## %s\n" % cat)
            for it in items:
                flags = " ".join("`%s`" % f for f in it.get("dietary", []))
                pop = " ⭐" if it.get("popular") else ""
                lines.append("**%s** — $%.2f%s %s  \n%s\n" % (
                    it["name"], float(it["price_usd"]), pop, flags, it["description"]))
    elif "posts" in obj:
        lines.append("# Social post copy")
        for p in obj["posts"]:
            lines.append("\n## Post %s — %s (%s)" % (p.get("id"), p.get("purpose"), p.get("platform")))
            lines.append("**%s**  \n%s  \n%s  \n→ pairs with `%s`" % (
                p.get("headline"), p.get("caption"),
                " ".join("#" + h.lstrip("#") for h in p.get("hashtags", [])), p.get("pairs_with")))
    elif "products" in obj:
        lines.append("# Product handles")
        for p in obj["products"]:
            lines.append("- `%s` — %s (%s)" % (p.get("handle"), p.get("display_name"), p.get("type")))
    else:
        import json as _j
        lines.append("```json\n%s\n```" % _j.dumps(obj, indent=2))
    path.write_text("\n".join(lines))


def render_csv(obj, path: Path):
    """Write the first list-of-dicts found in obj as a CSV."""
    import csv as _csv
    rows = None
    for v in obj.values():
        if isinstance(v, list) and v and isinstance(v[0], dict):
            rows = v
            break
    if not rows:
        raise RuntimeError("no list-of-dicts in data asset for CSV render")
    cols = []
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    with open(path, "w", newline="") as f:
        w = _csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: (", ".join(map(str, v)) if isinstance(v, list) else v) for k, v in r.items()})


def save_image_bytes(data: bytes, path: Path, fmt: str, keep_alpha: bool = False):
    """jpg: alpha flattened onto WHITE. png: alpha kept only when wanted
    (keep_alpha), else flattened onto white — prevents black-background
    surprises when a model returns an unexpected RGBA."""
    from PIL import Image
    path.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(io.BytesIO(data))
    if fmt == "jpg":
        degrade_mod.flatten_white(im).save(path, "JPEG", quality=92)
    elif im.mode in ("RGBA", "LA", "PA") and not keep_alpha:
        degrade_mod.flatten_white(im).save(path, "PNG")
    else:
        path.write_bytes(data)


def img_dims(path):
    from PIL import Image
    with Image.open(path) as im:
        return [im.width, im.height]


# --------------------------------------------------------------------------
class TaskRunner:
    def __init__(self, task_id, args):
        self.rec, self.spec = specs_mod.load_task(task_id)
        self.args = args
        self.dir = config.OUT_ROOT / ("%s_%s" % (task_id, self.spec["slug"]))
        self.dir.mkdir(parents=True, exist_ok=True)
        (self.dir / "assets").mkdir(exist_ok=True)
        (self.dir / "prompts").mkdir(exist_ok=True)
        self.log = RunLogger(self.dir / "run.log", quiet=args.quiet)
        self.llm = TextLLM(self.log)
        self.meter = CostMeter()
        self.state = read_json(self.dir / "state.json", {"assets": {}})
        self.feedback = read_json(self.dir / "feedback.json", {})  # {asset_key: prompt_delta} from package judge
        self.regens = 0

    # ---- estimation (no API calls) ----
    def estimate(self):
        images = 0.0
        n_img = 0
        text_calls = 1  # persona
        for a in self.spec["assets"]:
            if a["kind"] == "image":
                r = config.resolve(a["generator_role"], self.args.images_provider)
                if not r:
                    return None, "image role %r unservable with current keys" % a["generator_role"]
                prov, model, quality = r
                images += a.get("count", 1) * config.image_price(prov, model, quality, a.get("size", "1024x1024"))
                n_img += a.get("count", 1)
                if a.get("qc", {}).get("vision"):
                    text_calls += a.get("count", 1)
            elif a["kind"] == "program":
                continue  # deterministic local render, no model cost
            elif a["kind"] == "video":
                images += a.get("count", 1) * config.PRICES.get("video:%s" % a.get("generator", "veo"), 1.0)
            elif a["kind"] == "audio":
                images += a.get("count", 1) * config.PRICES.get("audio:tts", 0.02)
            else:
                if not config.resolve("writer"):
                    return None, "no writer model available"
                text_calls += 1
        usd = images + text_calls * config.PRICES["text_call"]
        return {"usd": usd, "images": n_img, "text_calls": text_calls}, None

    # ---- generation ----
    def run(self):
        t0 = time.time()
        self.log.log("=== task %s (%s) — %s ===" % (self.rec["id"], self.spec["slug"], self.rec["title"]))
        persona = personas.ensure_persona(self.dir, self.spec, self.rec, self.llm, self.log,
                                          force=self.args.force)
        self.meter.add_text(config.PRICES["text_call"])
        ctx = Ctx(self.rec, self.spec, persona)

        kind_of = {a["key"]: a["kind"] for a in self.spec["assets"]}
        for asset in self.spec["assets"]:
            # preload data deps generated in earlier runs
            self._load_cached_data(ctx)
            for dep in asset.get("depends_on", []):
                # only DATA/TEXT deps go into ctx.assets and must be loaded first; an
                # image/video/audio/program dep is just an ordering hint (nothing to load).
                if kind_of.get(dep, "data") in ("data", "text") and dep not in ctx.assets:
                    raise RuntimeError("%s depends on %s which is not generated yet" % (asset["key"], dep))
            if asset["kind"] in ("data", "text"):
                self._gen_text_asset(asset, ctx)
            elif asset["kind"] == "program":
                self._gen_program_asset(asset, ctx)
            elif asset["kind"] == "video":
                self._gen_video_asset(asset, ctx)
            elif asset["kind"] == "audio":
                self._gen_audio_asset(asset, ctx)
            else:
                self._gen_image_asset(asset, ctx)
            write_json(self.dir / "state.json", self.state)

        stats = {"images_generated": self.meter.images, "regenerations": self.regens,
                 "est_cost_usd": round(self.meter.usd, 2), "text_calls": self.meter.text_calls,
                 "wall_time_s": int(time.time() - t0)}
        man = manifest_mod.build(self.dir, self.rec, self.spec, persona, self.state, stats)
        manifest_mod.render_intake(self.dir, man)
        contact_sheet.write_task_sheet(self.dir, man)
        self.log.log("task %s done: ready_for_agent=%s, est $%.2f, %ds" % (
            self.rec["id"], man["ready_for_agent"], self.meter.usd, stats["wall_time_s"]))
        self._sync_to_gcs()
        return man

    def _sync_to_gcs(self):
        """Auto-mirror this task's assets to GCS after a real regeneration.
        Best-effort: never fails the run. Disable with env GCS_SYNC=0."""
        import os, shutil, subprocess
        if getattr(self.args, "dry_run", False):
            return
        if os.environ.get("GCS_SYNC", "").lower() in ("0", "off", "false", "no"):
            self.log.log("gcs sync: disabled via GCS_SYNC")
            return
        here = os.path.dirname(os.path.abspath(__file__))
        script = os.path.join(here, "sync_to_gcs.sh")
        if not os.path.exists(script) or not shutil.which("gsutil"):
            return
        try:
            r = subprocess.run(["bash", script, "--task", self.rec["id"]],
                               capture_output=True, text=True, timeout=900)
            if r.returncode == 0:
                self.log.log("gcs sync: %s mirrored to bucket" % self.rec["id"])
            else:
                tail = (r.stderr or r.stdout or "").strip().splitlines()
                self.log.log("gcs sync skipped (%s): %s" % (
                    self.rec["id"], tail[-1][:160] if tail else "unknown"))
        except Exception as e:
            self.log.log("gcs sync error (%s): %s" % (self.rec["id"], e))

    def _load_cached_data(self, ctx):
        for a in self.spec["assets"]:
            if a["kind"] in ("data", "text") and a["key"] not in ctx.assets:
                f = self.dir / "assets" / a["filename"]
                if f.exists():
                    try:
                        ctx.assets[a["key"]] = read_json(f) if a["kind"] == "data" else f.read_text()
                    except Exception:
                        pass

    def _skip(self, key):
        """Asset-level skip when resuming (files exist + state entry present)."""
        if self.args.force:
            return False
        if self.args.asset and self.args.asset == key:
            return False
        st = self.state["assets"].get(key)
        if not st:
            return False
        for e in st["entries"]:
            if e.get("file") and not (self.dir / e["file"]).exists():
                return False
        return True

    def _gen_text_asset(self, asset, ctx):
        key = asset["key"]
        out = self.dir / "assets" / asset["filename"]
        if self._skip(key):
            self.log.log("%s: cached, skip" % key)
            if asset["kind"] == "data":
                ctx.assets[key] = read_json(out)
            return
        self.log.log("%s: writing %s" % (key, asset["filename"]))
        prompt = asset["prompt"].format(**dict(ctx.flat, i=1))
        # Closed-loop repair: if the judge flagged this data/text asset AND it already exists,
        # apply a SURGICAL patch to the existing file (reliable for "add a field / fix a value")
        # rather than re-rolling the whole thing from scratch.
        fb = self.feedback.get(asset["key"])
        patch = bool(fb) and out.exists()
        if fb:
            self.log.log("%s: judge feedback (%d chars) — %s" % (key, len(fb), "SURGICAL PATCH" if patch else "regenerate"))
        check_status = "pass"
        if asset["kind"] == "data":
            checks = asset.get("qc", {}).get("checks")

            def _gen_data(extra=""):
                if patch:
                    return self.llm.complete_json(
                        "You apply a SURGICAL edit to an existing JSON document for a design project. Apply ONLY "
                        "the requested fix; keep every other field identical and the same overall shape. Return "
                        "the full corrected JSON.",
                        "FIX TO APPLY:\n%s%s\n\nCURRENT %s:\n%s" % (fb, extra, asset["filename"], out.read_text()),
                        temperature=0.2)
                return self.llm.complete_json(
                    "You produce precise, high-quality structured content for a design project.", prompt + extra)

            obj = _gen_data()
            try:
                data_checks(obj, checks)
            except RuntimeError as e:
                # one sharper retry naming the exact required fields, then mark honestly (no false pass)
                self.log.log("%s: data check failed (%s) — retrying with explicit field list" % (key, str(e)[:120]))
                req = [c for c in (checks or []) if "[]." in c]
                obj2 = _gen_data("\n\nMANDATORY: every record MUST include non-empty values for: %s. "
                                 "Do not leave any of these null or empty." % ", ".join(req))
                self.meter.add_text(config.PRICES["text_call"])
                try:
                    data_checks(obj2, checks)
                    obj = obj2
                except RuntimeError as e2:
                    obj = obj2
                    check_status = "failed"
                    self.log.log("%s: data check STILL failing after retry (%s) — marking FAILED" % (key, str(e2)[:120]))
            write_json(out, obj)
            ctx.assets[key] = obj
            if asset.get("also_render"):
                rpath = self.dir / "assets" / asset["also_render"]
                if asset["also_render"].endswith(".csv"):
                    render_csv(obj, rpath)
                else:
                    render_md(obj, rpath)
        else:
            if patch:
                txt = self.llm.complete(
                    "You apply a surgical edit to an existing markdown brand document. Apply ONLY the "
                    "requested fix; keep everything else identical. Return the full corrected markdown.",
                    "FIX TO APPLY:\n%s\n\nCURRENT %s:\n%s" % (fb, asset["filename"], out.read_text()))
            else:
                txt = self.llm.complete(
                    "You write impeccable, concise brand documents. Markdown only.", prompt)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(txt)
            ctx.assets[key] = txt
        self.meter.add_text(config.PRICES["text_call"])
        (self.dir / "prompts" / ("%s.txt" % key)).write_text(prompt + (("\n\n[PATCH FEEDBACK]\n" + fb) if patch else ""))
        used = (self.llm.last_used or "writer-chain").split("/", 1)
        entry = {"key": key, "input_requirement": asset["input_requirement"], "kind": asset["kind"],
                 "file": "assets/%s" % asset["filename"], "format": asset["filename"].split(".")[-1],
                 "generator": {"provider": used[0], "model": used[-1],
                               "prompt": prompt, "prompt_file": "prompts/%s.txt" % key},
                 "qc": {"status": check_status, "technical": check_status, "attempts": 1}}
        entries = [entry]
        if asset.get("also_render"):
            entries.append(dict(entry, key=key + ".render", file="assets/%s" % asset["also_render"],
                                format="md"))
        self.state["assets"][key] = {"entries": entries}

    def _gen_program_asset(self, asset, ctx):
        """Deterministic asset rendered by spec-provided python (no model call) —
        e.g. real scannable QR codes. asset['program_fn'](ctx, paths) writes the
        files and returns a params dict recorded in the manifest."""
        import json as _j
        key = asset["key"]
        if self._skip(key):
            self.log.log("%s: cached, skip" % key)
            return
        names = render_filenames(asset, ctx)
        paths = [self.dir / "assets" / n for n in names]
        for p in paths:
            p.parent.mkdir(parents=True, exist_ok=True)
        self.log.log("%s: program-rendering %d file(s) (%s)" % (
            key, len(paths), asset.get("program_desc", "program_fn")))
        params = asset["program_fn"](ctx, paths) or {}
        entries = []
        for i, (n, p) in enumerate(zip(names, paths)):
            ok = p.exists() and p.stat().st_size > 100
            e = {"key": "%s[%d]" % (key, i) if len(names) > 1 else key,
                 "input_requirement": asset["input_requirement"], "kind": "program",
                 "file": "assets/%s" % n, "format": n.split(".")[-1],
                 "generator": {"provider": "deterministic",
                               "model": asset.get("program_desc", "program_fn"),
                               "prompt": _j.dumps(params)[:500]},
                 "qc": {"status": "pass" if ok else "failed",
                        "technical": "pass" if ok else "fail", "attempts": 1}}
            if ok and n.lower().endswith((".png", ".jpg", ".jpeg")):
                e["dims"] = img_dims(p)
            entries.append(e)
        self.state["assets"][key] = {"entries": entries}

    def _gen_video_asset(self, asset, ctx):
        """Generate video clips (Veo/Sora). asset: generator veo|sora, seconds, aspect,
        prompt/prompt_fn, filename/filename_fn, optional depends_on."""
        from adapters import media_gen
        key = asset["key"]
        if self._skip(key):
            self.log.log("%s: cached, skip" % key)
            return
        prompts = render_prompts(asset, ctx)
        names = render_filenames(asset, ctx)
        provider = asset.get("generator", "veo")
        seconds = asset.get("seconds", 8)
        aspect = asset.get("aspect", "16:9")
        entries = []
        prev = self.state["assets"].get(key, {}).get("entries", [])
        for i, (prompt, fname) in enumerate(zip(prompts, names)):
            target = self.dir / "assets" / fname
            done = next((e for e in prev if e.get("file") == "assets/%s" % fname), None)
            if done and target.exists() and not self.args.force and self.args.asset != key:
                entries.append(done)
                continue
            self.log.log("%s[%d]: video via %s (%ss, %s)" % (key, i, provider, seconds, aspect))
            meta, ok = {}, False
            if not self.args.dry_run:
                try:
                    meta = media_gen.generate_video(prompt, target, provider=provider,
                                                    seconds=seconds, aspect=aspect, logger=self.log)
                    ok = target.exists() and target.stat().st_size > 10000
                except Exception as e:
                    self.log.log("%s[%d] video FAILED: %s" % (key, i, str(e)[:180]))
            self.meter.add_media(config.PRICES.get("video:%s" % provider, 1.0))
            entries.append({
                "key": "%s[%d]" % (key, i) if len(names) > 1 else key,
                "input_requirement": asset["input_requirement"], "kind": "video",
                "file": "assets/%s" % fname, "format": fname.split(".")[-1],
                "generator": {"provider": meta.get("provider", provider),
                              "model": meta.get("model", provider), "prompt": prompt[:600]},
                "dims": [meta.get("width"), meta.get("height")] if meta.get("width") else None,
                "duration_s": meta.get("duration"), "has_audio": meta.get("has_audio"),
                "qc": {"status": "pass" if ok else "failed",
                       "technical": "pass" if ok else "fail", "attempts": 1}})
            self.state["assets"][key] = {"entries": entries}
            write_json(self.dir / "state.json", self.state)
        self.state["assets"][key] = {"entries": entries}

    def _gen_audio_asset(self, asset, ctx):
        """Generate a voiceover (OpenAI TTS); optional roughen for media_enhance_speech.
        asset: voice, text (template) or text_fn(ctx), filename, optional roughen:true."""
        from adapters import media_gen
        key = asset["key"]
        if self._skip(key):
            self.log.log("%s: cached, skip" % key)
            return
        if asset.get("text_fn"):
            texts = asset["text_fn"](ctx)
        else:
            texts = [asset["text"].format(**dict(ctx.flat, i=1))]
        names = render_filenames(asset, ctx)
        voice = asset.get("voice", "alloy")
        entries = []
        prev = self.state["assets"].get(key, {}).get("entries", [])
        for i, (text, fname) in enumerate(zip(texts, names)):
            target = self.dir / "assets" / fname
            done = next((e for e in prev if e.get("file") == "assets/%s" % fname), None)
            if done and target.exists() and not self.args.force and self.args.asset != key:
                entries.append(done)
                continue
            self.log.log("%s[%d]: tts voice=%s%s" % (key, i, voice, " +roughen" if asset.get("roughen") else ""))
            meta, ok = {}, False
            if not self.args.dry_run:
                try:
                    if asset.get("roughen"):
                        clean = self.dir / "originals" / ("clean_" + fname)
                        clean.parent.mkdir(parents=True, exist_ok=True)
                        media_gen.generate_tts(text, clean, voice=voice, logger=self.log)
                        media_gen.roughen_audio(clean, target, logger=self.log)
                        meta = media_gen.probe_media(target)
                        meta.update(provider="openai", model="gpt-4o-mini-tts+roughen")
                    else:
                        meta = media_gen.generate_tts(text, target, voice=voice, logger=self.log)
                    ok = target.exists() and target.stat().st_size > 2000
                except Exception as e:
                    self.log.log("%s[%d] tts FAILED: %s" % (key, i, str(e)[:180]))
            self.meter.add_media(config.PRICES.get("audio:tts", 0.02))
            (self.dir / "assets" / (fname.rsplit(".", 1)[0] + ".txt")).write_text(text)
            entries.append({
                "key": "%s[%d]" % (key, i) if len(names) > 1 else key,
                "input_requirement": asset["input_requirement"], "kind": "audio",
                "file": "assets/%s" % fname, "format": fname.split(".")[-1],
                "generator": {"provider": meta.get("provider", "openai"),
                              "model": meta.get("model", "gpt-4o-mini-tts"), "prompt": text[:600]},
                "duration_s": meta.get("duration"),
                "qc": {"status": "pass" if ok else "failed",
                       "technical": "pass" if ok else "fail", "attempts": 1}})
            self.state["assets"][key] = {"entries": entries}
            write_json(self.dir / "state.json", self.state)
        self.state["assets"][key] = {"entries": entries}

    def _gen_image_asset(self, asset, ctx):
        key = asset["key"]
        if self._skip(key):
            self.log.log("%s: cached, skip" % key)
            return
        prompts = render_prompts(asset, ctx)
        names = render_filenames(asset, ctx)
        chain = get_image_chain(asset["generator_role"], self.args.images_provider, self.log)
        if not chain:
            raise RuntimeError("no image provider for role %s" % asset["generator_role"])
        entries = []
        prev = self.state["assets"].get(key, {}).get("entries", [])
        for i, (prompt, fname) in enumerate(zip(prompts, names)):
            target = self.dir / "assets" / fname
            done = next((e for e in prev if e.get("file") == "assets/%s" % fname), None)
            if done and target.exists() and not self.args.force and self.args.asset != key:
                entries.append(done)
                continue
            entry = self._gen_one_image(asset, ctx, prompt, fname, i, chain)
            entries.append(entry)
            self.state["assets"][key] = {"entries": entries}
            write_json(self.dir / "state.json", self.state)
        self.state["assets"][key] = {"entries": entries}

    def _gen_one_image(self, asset, ctx, prompt, fname, idx, chain):
        key, fmt = asset["key"], asset.get("format", "png")
        size = asset.get("size", "1024x1024")
        background = asset.get("background")
        target = self.dir / "assets" / fname
        qc_cfg = asset.get("qc", {})
        min_score = qc_cfg.get("min_score", config.QC_MIN_SCORE)
        criteria = (qc_cfg.get("criteria") or "").format(**dict(ctx.flat, i=idx + 1))
        tech_cfg = qc_cfg.get("technical", {})
        best = None  # (score, meta)
        cur_prompt = prompt
        fb = self.feedback.get(asset["key"])  # package-judge closed-loop feedback for this asset
        if fb:
            cur_prompt = prompt + ("\n\nJUDGE FEEDBACK — a package reviewer flagged this asset. "
                                   "Fix specifically:\n%s" % fb)
            self.log.log("%s[%d]: applying judge feedback (%d chars)" % (key, idx, len(fb)))
        attempts = 0
        max_attempts = 1 + (config.QC_MAX_REGENS if qc_cfg.get("vision") else 0)

        while attempts < max_attempts:
            attempts += 1
            if self.meter.images >= config.MAX_IMAGES_PER_RUN:
                raise RuntimeError("MAX_IMAGES_PER_RUN (%d) hit — aborting for safety" % config.MAX_IMAGES_PER_RUN)
            gen_meta = None
            for adapter, prov, model, quality in chain:
                try:
                    res = retry(lambda a=adapter, p=cur_prompt: a.generate(p, size=size, n=1, background=background),
                                attempts=3, logger=self.log)[0]
                    gen_meta = (res, prov, model, quality)
                    break
                except Exception as e:
                    msg = str(e)
                    self.log.log("%s[%d]: %s/%s failed: %s" % (key, idx, prov, model, msg[:160]))
                    if any(w in msg.lower() for w in ("safety", "blocked", "content_policy", "moderation")):
                        try:
                            cur_prompt = self.llm.complete(
                                "Rewrite this image prompt to avoid content-policy triggers while keeping the "
                                "exact same subject, style and constraints. Return only the rewritten prompt.",
                                cur_prompt, temperature=0.4)
                            self.meter.add_text(config.PRICES["text_call"])
                            res = retry(lambda a=adapter, p=cur_prompt: a.generate(p, size=size, n=1, background=background),
                                        attempts=2, logger=self.log)[0]
                            gen_meta = (res, prov, model, quality)
                            break
                        except Exception as e2:
                            self.log.log("%s[%d]: sanitize retry failed: %s" % (key, idx, str(e2)[:140]))
                    continue
            if not gen_meta:
                if best:
                    break  # fall back to best earlier attempt
                self.log.log("%s[%d]: ALL providers failed — marking asset failed" % (key, idx))
                return {"key": "%s[%d]" % (key, idx), "input_requirement": asset["input_requirement"],
                        "kind": "image", "file": None, "format": fmt,
                        "generator": {"prompt": cur_prompt},
                        "qc": {"status": "failed", "attempts": attempts, "issues": ["all providers failed"]}}

            res, prov, model, quality = gen_meta
            self.meter.add_image(config.image_price(prov, model, quality, size))
            save_image_bytes(res.data, target, fmt, keep_alpha=(background == "transparent"))
            ok_t, t_issues = qc.technical(
                target, expect_size=size,
                expect_alpha=(background == "transparent" and prov == "openai"),
                messy_background=bool(tech_cfg.get("messy_background")))
            review = {"score": None, "issues": []}
            if ok_t and qc_cfg.get("vision") and not self.args.skip_vision_qc:
                try:
                    review = qc.vision(self.llm, target, criteria, generator_provider=prov)
                    self.meter.add_text(config.PRICES["text_call"])
                except Exception as e:
                    self.log.log("%s[%d]: vision QC unavailable (%s) — accepting on technical" % (key, idx, str(e)[:120]))
                    review = {"score": min_score, "issues": ["vision QC unavailable"], "judge": "none"}
            score = review.get("score")
            issues = t_issues + (review.get("issues") or [])
            self.log.log("%s[%d] attempt %d via %s/%s — tech:%s vision:%s" % (
                key, idx, attempts, prov, model, "ok" if ok_t else "FAIL", score))
            cand = {"bytes_done": True, "prov": prov, "model": model, "quality": quality,
                    "prompt": cur_prompt, "score": score if score is not None else (min_score if ok_t else 0),
                    "tech_ok": ok_t, "issues": issues, "judge": review.get("judge"),
                    "data": res.data}
            if best is None or cand["score"] > best["score"]:
                best = cand
            if ok_t and (score is None or score >= min_score):
                break
            if attempts < max_attempts:
                self.regens += 1
                cur_prompt = prompt + "\n\nA previous attempt FAILED review. Avoid these exact issues:\n- " + \
                    "\n- ".join(str(x) for x in issues[:6])

        # persist best attempt
        save_image_bytes(best["data"], target, fmt, keep_alpha=(background == "transparent"))
        post_entries = []
        for pp in asset.get("post_process", []):
            if pp["op"] == "soften":
                orig = self.dir / "originals" / ("clean_" + fname)
                orig.parent.mkdir(exist_ok=True)
                save_image_bytes(best["data"], orig, "png")
                params = degrade_mod.soften(target, target, seed=self.rec["id"])
                post_entries.append({"op": "soften", "params": params,
                                     "original": "originals/clean_%s" % fname})
            elif pp["op"] == "degrade":
                orig = self.dir / "originals" / fname
                orig.parent.mkdir(exist_ok=True)
                save_image_bytes(best["data"], orig, fmt)
                profile = degrade_mod.PROFILES[idx % len(degrade_mod.PROFILES)]
                params = degrade_mod.degrade(orig, target, profile, seed=self.rec["id"] * 1000 + idx)
                post_entries.append({"op": "degrade", "profile": profile, "params": params,
                                     "original": "originals/%s" % fname})
        pfile = self.dir / "prompts" / ("%s_%d.txt" % (key, idx))
        pfile.write_text(best["prompt"])
        status = "pass" if (best["tech_ok"] and (best["score"] is None or best["score"] >= min_score)) \
            else ("accepted_with_warnings" if best["tech_ok"] or best["score"] >= 5 else "failed")
        return {"key": "%s[%d]" % (key, idx) if asset.get("count", 1) > 1 else key,
                "input_requirement": asset["input_requirement"], "kind": "image",
                "file": "assets/%s" % fname, "format": fmt, "dims": img_dims(target),
                "generator": {"provider": best["prov"], "model": best["model"],
                              "quality": best["quality"], "size": size, "prompt": best["prompt"],
                              "prompt_file": "prompts/%s_%d.txt" % (key, idx)},
                "post_process": post_entries,
                "qc": {"status": status, "technical": "pass" if best["tech_ok"] else "fail",
                       "vision_score": best["score"], "judge": best.get("judge"),
                       "attempts": attempts, "issues": best["issues"][:6]}}


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="AI input-asset generation pipeline (5-task pilot)")
    ap.add_argument("--task", action="append", type=int, help="task id (repeatable)")
    ap.add_argument("--all-pilot", action="store_true")
    ap.add_argument("--check", action="store_true", help="print key/model matrix + spec lint")
    ap.add_argument("--deep", action="store_true", help="with --check: ping text providers")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--asset", help="regenerate just this asset key")
    ap.add_argument("--images-provider", choices=["openai", "gemini"])
    ap.add_argument("--skip-vision-qc", action="store_true")
    ap.add_argument("--yes", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if args.check:
        print(config.key_matrix())
        ds = specs_mod.load_dataset()
        print("\nSpec lint (coverage):")
        for tid, spec in specs_mod.SPECS.items():
            rec = ds[tid]
            claimed = {a["input_requirement"] for a in spec["assets"]} | \
                      {d["requirement"] for d in spec.get("decisions", [])}
            unc = [i for i in rec["inputs"] if i not in claimed]
            print("  %s (%s): %s" % (tid, spec["slug"],
                                     "OK — all %d inputs covered" % len(rec["inputs"]) if not unc
                                     else "UNCOVERED: %s" % unc))
        if args.deep:
            log = RunLogger(None, quiet=False)
            llm = TextLLM(log)
            try:
                pong = llm.complete("Reply with exactly: pong", "ping", temperature=0)
                print("\nwriter ping: %s" % pong.strip()[:40])
            except Exception as e:
                print("\nwriter ping FAILED: %s" % e)
        return

    task_ids = specs_mod.PILOT_ORDER if args.all_pilot else (args.task or [])
    if not task_ids:
        ap.error("pass --task ID (repeatable), --all-pilot, or --check")

    # preflight + estimate (no spend)
    total, plans = 0.0, []
    for tid in task_ids:
        r = TaskRunner(tid, args)
        est, err = r.estimate()
        if err:
            print("PREFLIGHT FAIL task %s: %s" % (tid, err))
            sys.exit(2)
        plans.append((tid, r, est))
        total += est["usd"]
    print("Plan: %d task(s), ~%d images, est $%.2f total" % (
        len(plans), sum(e["images"] for _, _, e in plans), total))
    for tid, r, est in plans:
        print("  task %-5s %-24s ~%2d imgs  est $%.2f" % (tid, r.spec["slug"], est["images"], est["usd"]))
    if args.dry_run:
        return
    if total > config.COST_GATE_USD and not args.yes:
        if not sys.stdin.isatty():
            print("Estimated cost $%.2f exceeds gate ($%.2f) — re-run with --yes" % (total, config.COST_GATE_USD))
            sys.exit(3)
        if input("Proceed? [y/N] ").strip().lower() != "y":
            sys.exit(3)

    results = []
    for tid, runner, _ in plans:
        try:
            man = runner.run()
            results.append((tid, man["ready_for_agent"], runner.meter.usd, None))
        except Exception as e:
            results.append((tid, False, runner.meter.usd, str(e)[:200]))
            runner.log.log("TASK FAILED: %s" % e)
    contact_sheet.write_index()

    print("\n=== SUMMARY ===")
    for tid, ready, usd, err in results:
        print("  task %-5s ready_for_agent=%-5s  $%.2f  %s" % (tid, ready, usd, err or ""))
    print("Total spend (est): $%.2f" % sum(u for _, _, u, _ in results))
    print("Browse: %s" % (config.OUT_ROOT / "index.html"))


if __name__ == "__main__":
    main()
