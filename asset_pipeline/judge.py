"""Package judge — scores how good a generated input-asset SET is FOR ITS TASK
(package-level, task-relative), with a cross-provider panel, an adversarial
red-team pass, a per-asset-QC cross-check, and a closed regeneration loop.

Usage:
  .venv/bin/python judge.py --check
  .venv/bin/python judge.py --task 440
  .venv/bin/python judge.py --all
  .venv/bin/python judge.py --task 5649 --improve --yes
"""
from __future__ import annotations
import argparse
import base64
import io
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config  # noqa: E402
import scorecard  # noqa: E402
import specs as specs_mod  # noqa: E402
from adapters.text_llm import TextLLM  # noqa: E402
from util import read_json, write_json, RunLogger, CostMeter, extract_json  # noqa: E402

DIMS = ["task_fit", "completeness", "executability", "realism", "coherence", "decision_quality"]
DIM_LABEL = {
    "task_fit": "Task Fit", "completeness": "Completeness", "executability": "Executability",
    "realism": "Realism", "coherence": "Coherence", "decision_quality": "Decision Quality",
}
WEIGHTS = {
    "editing":  {"task_fit": .22, "completeness": .13, "executability": .30,
                 "realism": .17, "coherence": .06, "decision_quality": .12},
    "template": {"task_fit": .17, "completeness": .22, "executability": .10,
                 "realism": .17, "coherence": .22, "decision_quality": .12},
}
VERDICTS = [(8.5, "client-ready"), (7.0, "minor-gaps"), (5.0, "needs-rework"), (0.0, "reject")]
THUMB_PX = 768
MAX_IMAGES = 16


def archetype_for(man: dict) -> str:
    return "template" if "express template" in (man.get("family") or "").lower() else "editing"


def verdict_for(score: float) -> str:
    for thr, name in VERDICTS:
        if score >= thr:
            return name
    return "reject"


def task_dir_for(task_id: int) -> Path:
    slug = specs_mod.SPECS[task_id]["slug"]
    return config.OUT_ROOT / ("%s_%s" % (task_id, slug))


# --------------------------------------------------------------------------
# Package loading
# --------------------------------------------------------------------------
def _downscale_jpeg(path: Path, px: int) -> bytes:
    from PIL import Image
    im = Image.open(path)
    if im.mode in ("RGBA", "LA", "PA"):  # flatten onto WHITE for the judge view
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        bg.alpha_composite(im.convert("RGBA"))
        im = bg.convert("RGB")
    else:
        im = im.convert("RGB")
    im.thumbnail((px, px), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=80)
    return buf.getvalue()


def load_package(task_dir: Path, skip_images: bool = False, thumb_px: int = THUMB_PX,
                 max_images: int = MAX_IMAGES) -> dict:
    """Returns {man, images:[{key,requirement,mime,bytes,vision_score}], texts:[...], image_overflow}."""
    man = read_json(task_dir / "manifest.json")
    images, texts, overflow = [], [], 0
    TEXT_CAP = 12000
    for a in man.get("assets", []):
        f = a.get("file")
        is_imgfile = str(f or "").lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
        if (a.get("kind") == "image" or (a.get("kind") == "program" and is_imgfile)) \
                and f and (task_dir / f).exists():
            if skip_images:
                continue
            if len(images) >= max_images:
                overflow += 1
                continue
            images.append({
                "key": a["key"], "requirement": a.get("input_requirement", ""),
                "mime": "image/jpeg", "bytes": _downscale_jpeg(task_dir / f, thumb_px),
                "vision_score": (a.get("qc") or {}).get("vision_score"), "file": f,
                "dims": a.get("dims"),
                "deterministic": a.get("kind") == "program",
            })
        elif a.get("kind") in ("data", "text") and f and (task_dir / f).exists():
            if str(a.get("key", "")).endswith(".render") and not str(f).endswith(".csv"):
                continue  # skip the .md re-render duplicate, but KEEP the .csv (it is the
                          # data-merge consumable the executability dimension needs to see)
            raw = (task_dir / f).read_text()
            full_len = len(raw)
            note = ""
            if str(f).endswith(".json"):
                # compact JSON so more real content fits the cap; if still over, tell the
                # judges the truth: the file on disk is complete and parser-valid.
                try:
                    obj = json.loads(raw)
                    raw = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
                    full_len = len(raw)
                    if full_len > TEXT_CAP and isinstance(obj, dict):
                        shape = ", ".join(
                            "%s[%d]" % (k, len(v)) if isinstance(v, (list, dict)) else k
                            for k, v in obj.items())
                        note = ("\n...[EXCERPT ONLY — the full file on disk is %d chars of COMPLETE, "
                                "syntactically VALID JSON (parser-verified just now). Full top-level "
                                "shape: {%s}. Judge content quality from this excerpt; do NOT treat the "
                                "file as malformed or sections beyond the excerpt as missing.]"
                                % (full_len, shape)) if shape else ""
                except Exception:
                    pass
            if full_len > TEXT_CAP and not note:
                note = "\n...[EXCERPT — full file is %d chars on disk]" % full_len
            texts.append({"key": a["key"], "requirement": a.get("input_requirement", ""),
                          "file": f, "content": raw[:TEXT_CAP] + (note if full_len > TEXT_CAP else "")})
    return {"man": man, "images": images, "texts": texts, "image_overflow": overflow}


# --------------------------------------------------------------------------
# Prompt construction
# --------------------------------------------------------------------------
_BANDS = """Score each dimension 0-10 using these anchors:

TASK_FIT — do the assets match what THIS specific client asked for (subjects, mandated colours, named brand)?
  10 every asset is exactly the subject/brand the brief specifies · 7 mostly on-brief, minor drift · 4 generic
  stand-ins where the brief was specific · 0 wrong subject entirely.
COMPLETENESS — is everything the task needs present AND usable (semantic coverage, not just "a file exists")?
  10 nothing an executor would still have to ask the client for · 7 a minor gap covered by a sound decision · 4 a
  needed asset is missing or too sparse to work from · 0 cannot start.
  HARD RULE: if ANY element the brief calls mandatory / required / legal / regulatory / safety is missing, null,
  or empty (e.g. a data field present in the schema but blank), completeness MUST be ≤ 3 and task_fit ≤ 5.
  SCOPE RULE: the benchmark is what THIS client actually hands over per the ORIGINAL BRIEF's own
  attachments/inputs — never demand inputs the client never promised. The FINAL deliverable pieces are
  PRODUCED by the design workflow from copy/specs/style references; a missing visual draft of a deliverable
  is NOT a completeness gap unless the brief says the client supplies one.
EXECUTABILITY — can the named Adobe mcp_workflow tools actually CONSUME these (format/dims + the specific
  affordance)? e.g. background-removal needs a REMOVABLE busy background (not a clean studio sweep); vectorize
  needs an imperfect RASTER; data-merge needs a list-of-rows CSV; a step needing a transparent PNG must have one.
  10 every tool in the chain consumes its input directly · 7 minor agent effort · 4 one asset blocks a step · 0 chain can't run.
  CLIENT-SUPPLIED INPUTS RULE: items the client/user supplies AT EXECUTION — InDesign/Illustrator data-merge
  TEMPLATES (.indd/.ai with Variables/Data-Merge fields) and licensed Adobe STOCK plates — are recorded in
  DECISIONS, NOT generated in this pack by design. Do NOT mark them missing or count them against executability/
  completeness; treat them as provided. A data asset rendered as BOTH .json and .csv DOES provide the CSV the
  data-merge step needs (the .csv render is the consumable). Judge executability only on whether the assets WE
  generate are consumable by their steps — not on the user-authored templates or stock, and not on output print
  resolution (the connector/print stage handles final DPI).
REALISM — context-appropriate authenticity: would a real owner have handed these over? MESSY where the brief
  implies a real phone snapshot, POLISHED where it implies studio/luxury. 10 indistinguishable from genuine client
  files · 7 believable · 4 obviously synthetic in a way that matters · 0 uncanny/unusable.
COHERENCE — do all assets read as ONE brand/client (palette hexes, logo, fonts, voice consistent)?
  10 flawless single identity · 7 minor inconsistency · 4 assets look like different brands · 0 incoherent.
DECISION_QUALITY — are the recorded decisions[] assumptions ones a real client would accept, and is any REAL
  input wrongly demoted to an assumption? 10 every assumption sound & justified · 7 mostly · 4 a risky/wrong
  assumption · 0 assumptions would derail the job."""

_SYSTEM_FULL = (
    "You are a senior Adobe creative-operations lead doing a PACKAGE-LEVEL review of the input assets a "
    "junior produced for ONE freelance design task. You are NOT grading images for beauty — you decide "
    "whether this HANDOFF lets an automated Adobe tool agent execute the task and satisfy the client. Judge "
    "the WHOLE set, relative to THIS task and THIS Adobe workflow.\n\n" + _BANDS + "\n\n"
    "For EVERY dimension you MUST: (a) cite evidence by asset id exactly as labelled ('image 3', 'menu.json'); "
    "(b) list concrete deductions; (c) if the score is below 8, give a machine-actionable fix naming the single "
    "target_asset_key to regenerate and a prompt_delta (specific text to append to that asset's generation "
    "prompt). You MAY contradict the per-asset self-QC scores shown to you. Be TERSE: at most 2 evidence and "
    "2 deductions per dimension, each one short phrase (<=15 words). Output STRICT JSON only, no prose, "
    "no markdown fences, matching exactly:\n"
    '{"dimensions":{"task_fit":{"score":<int 0-10>,"evidence":["..."],"deductions":["..."],'
    '"fix":{"target_asset_key":"<key>","problem":"...","prompt_delta":"..."}|null},'
    '"completeness":{...},"executability":{...},"realism":{...},"coherence":{...},"decision_quality":{...}},'
    '"overall_self":<float>,"one_line":"<<=20 words>"}'
)

_SYSTEM_REDTEAM = (
    "You are a hostile, hard-to-please real CLIENT who just received this input-asset handoff for your "
    "freelance design job. In <=120 words decide: (1) the single biggest reason you would REJECT this handoff, "
    "(2) the ONE asset the automated agent would choke on first, and why. Output STRICT JSON only:\n"
    '{"rejection_reason":"...","choke_asset_key":"<key>","choke_reason":"...","severity":<int 0-10>}'
)


def build_user_block(bundle: dict, weights: dict) -> str:
    man = bundle["man"]
    L = []
    a = L.append
    a("TASK %s — %s" % (man["task_id"], man.get("title", "")))
    a("type=%s | category=%s | family=%s | feasibility=%s" % (
        man.get("task_type"), man.get("category"), man.get("family"), man.get("feasibility")))
    a("\n=== ORIGINAL CLIENT BRIEF (verbatim) ===\n%s" % (man.get("original_brief") or "")[:2500])
    a("\n=== THE ADOBE WORKFLOW THESE ASSETS MUST FEED (executability anchor) ===\n%s" % man.get("mcp_workflow", ""))
    a("\n=== CLIENT INPUT REQUIREMENTS (what the client expects to hand over) ===")
    for x in man.get("assets", []):
        a("  - [%s] %s" % (x.get("kind"), x.get("input_requirement", "")))
    cov = man.get("coverage", {})
    if cov.get("uncovered"):
        a("  UNCOVERED by any asset: %s" % cov["uncovered"])
    a("\n=== RECORDED DECISIONS (assumptions made where the brief was vague) ===")
    for d in man.get("decisions", []):
        a("  - REQ: %s\n    ASSUMED: %s\n    WHY: %s" % (d.get("requirement"), d.get("assumed_value"), d.get("why")))
    p = man.get("client_persona", {})
    pal = ", ".join("%s %s(%s)" % (c.get("hex"), c.get("name", ""), c.get("role", "")) for c in (p.get("palette") or []))
    a("\n=== BRAND / PERSONA (coherence anchor) ===")
    a("  brand=%s | industry=%s | fonts=%s | palette=%s" % (
        p.get("brand_name"), p.get("industry"), p.get("fonts"), pal))
    a("  voice=%s" % p.get("voice"))
    a("\n=== ASSET INVENTORY (cite these exact ids) ===")
    for i, im in enumerate(bundle["images"], 1):
        dims = "x".join(map(str, im["dims"])) if im.get("dims") else "?"
        det = " | DETERMINISTIC (program-rendered, e.g. real QR — pixel style is expected)" \
            if im.get("deterministic") else ""
        a("  [image %d] key=%s | TRUE source dims=%s px (the thumbnail you see is downscaled) | "
          "fulfils: %s | self-QC vision_score=%s%s" % (
            i, im["key"], dims, im["requirement"][:80], im["vision_score"], det))
    if bundle["image_overflow"]:
        a("  (+%d more images of the same kinds exist, assumed similar)" % bundle["image_overflow"])
    for t in bundle["texts"]:
        a("\n  [%s] key=%s | fulfils: %s\n  ----\n%s\n  ----" % (
            t["file"], t["key"], t["requirement"][:80], t["content"]))
    a("\n=== DIMENSION WEIGHTS for this archetype (for your overall_self) ===")
    a("  " + ", ".join("%s=%.2f" % (DIM_LABEL[d], weights[d]) for d in DIMS))
    a("\nThe %d images follow, in inventory order." % len(bundle["images"]))
    return "\n".join(L)


# --------------------------------------------------------------------------
# The panel
# --------------------------------------------------------------------------
class PackageJudge:
    def __init__(self, llm: TextLLM, logger, meter: CostMeter, panel_providers=None):
        self.llm = llm
        self.log = logger
        self.meter = meter
        self.panel_providers = panel_providers  # optional [str] restriction/order

    def available_judges(self):
        """One (provider, model) per available provider, key-filtered, optionally restricted."""
        seen, out = set(), []
        for prov, model, _ in config.MODELS.get("package_judge", []):
            if prov in seen or not config.PROVIDERS.get(prov):
                continue
            if self.panel_providers and prov not in self.panel_providers:
                continue
            seen.add(prov)
            out.append((prov, model))
        if self.panel_providers:  # honor requested order
            out.sort(key=lambda pm: self.panel_providers.index(pm[0]))
        return out

    def _charge(self, n_images):
        self.meter.usd += config.PRICES["judge_call"] + n_images * config.PRICES["judge_image_surcharge"]
        self.meter.text_calls += 1

    def judge_once(self, system, user_text, image_parts, prov, model):
        self._charge(len(image_parts))
        if prov == "gemini":
            from google.genai import types
            contents = [types.Part.from_bytes(data=im["bytes"], mime_type=im["mime"]) for im in image_parts]
            contents.append(user_text)
            resp = self.llm._gemini().models.generate_content(
                model=model, contents=contents,
                config=types.GenerateContentConfig(system_instruction=system, temperature=0.0,
                                                   max_output_tokens=8192))
            return extract_json(resp.text or "")
        if prov == "openai":
            content = [{"type": "text", "text": user_text}]
            for im in image_parts:
                content.append({"type": "image_url", "image_url": {"url": "data:%s;base64,%s" % (
                    im["mime"], base64.b64encode(im["bytes"]).decode())}})
            r = self.llm._openai().chat.completions.create(
                model=model, temperature=0.0, max_tokens=8192,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": content}])
            return extract_json(r.choices[0].message.content)
        if prov == "anthropic":
            cli = self.llm._anthropic()
            if not cli:
                return None
            content = [{"type": "text", "text": user_text}]
            for im in image_parts:
                content.append({"type": "image", "source": {
                    "type": "base64", "media_type": im["mime"],
                    "data": base64.b64encode(im["bytes"]).decode()}})
            r = cli.messages.create(model=model, max_tokens=8192, temperature=0.0,
                                    system=system, messages=[{"role": "user", "content": content}])
            return extract_json(r.content[0].text)
        return None

    def run_panel(self, bundle, weights):
        judges = self.available_judges()
        if not judges:
            raise RuntimeError("no vision judge available — set GEMINI/OPENAI/ANTHROPIC key")
        user_text = build_user_block(bundle, weights)
        imgs = bundle["images"]
        per_judge, ran, failed = [], [], []
        for prov, model in judges:
            try:
                out = self.judge_once(_SYSTEM_FULL, user_text, imgs, prov, model)
                if not out:
                    failed.append("%s/%s (unavailable)" % (prov, model)); continue
                # one parse-retry on malformed
                if "dimensions" not in out:
                    out = self.judge_once(_SYSTEM_FULL, user_text + "\n\nReturn ONLY the JSON object.", imgs, prov, model)
                out["judge"] = "%s/%s" % (prov, model)
                per_judge.append(out)
                ran.append(out["judge"])
                self.log.log("  judge %s/%s -> overall_self %s" % (prov, model, out.get("overall_self")))
            except Exception as e:  # noqa: PERF203
                failed.append("%s/%s: %s" % (prov, model, str(e)[:120]))
                self.log.log("  judge %s/%s FAILED: %s" % (prov, model, str(e)[:140]))
        if not per_judge:
            raise RuntimeError("all judges failed: %s" % "; ".join(failed))
        # adversarial red-team — first judge only
        redteam = None
        rprov, rmodel = judges[0]
        try:
            redteam = self.judge_once(_SYSTEM_REDTEAM, user_text, imgs, rprov, rmodel)
            if redteam:
                redteam["judge"] = "%s/%s" % (rprov, rmodel)
        except Exception as e:
            self.log.log("  redteam FAILED: %s" % str(e)[:140])
        return {"per_judge": per_judge, "ran": ran, "failed": failed, "redteam": redteam}


# --------------------------------------------------------------------------
# Aggregation
# --------------------------------------------------------------------------
def _clip(x):
    try:
        return max(0, min(10, int(round(float(x)))))
    except Exception:
        return 0


def qc_cross_check(man: dict, dim_scores: dict) -> list:
    """Surface 'every asset scored high individually, but a package dim is low'."""
    vis = [(a["key"], (a.get("qc") or {}).get("vision_score")) for a in man.get("assets", [])
           if a.get("kind") == "image" and (a.get("qc") or {}).get("vision_score") is not None]
    if not vis:
        return []
    avg = statistics.mean(v for _, v in vis)
    gaps = []
    for d in ("task_fit", "realism", "executability", "completeness"):
        if dim_scores.get(d, 10) <= 6 and avg >= 8.5:
            gaps.append("Per-asset self-QC averages %.1f/10, but package %s scored %d — assets are individually "
                        "strong yet wrong/insufficient for the task." % (avg, DIM_LABEL[d], dim_scores[d]))
    return gaps


def aggregate(panel: dict, weights: dict, man: dict, has_det_defect: bool = False) -> dict:
    per = panel["per_judge"]
    dims_out, dim_medians = {}, {}
    for d in DIMS:
        scores, evidence, deductions, fixes = [], [], [], []
        for j in per:
            jd = (j.get("dimensions") or {}).get(d) or {}
            if "score" in jd:
                scores.append((_clip(jd["score"]), jd))
        if not scores:
            dims_out[d] = {"score": 0, "evidence": [], "deductions": ["no judge scored this dimension"],
                           "fix": None, "low_confidence": True, "per_judge": []}
            dim_medians[d] = 0
            continue
        vals = [s for s, _ in scores]
        med = int(round(statistics.median(vals)))
        spread = max(vals) - min(vals)
        # merge evidence/deductions; keep the fix from the lowest-scoring judge
        for s, jd in scores:
            evidence += (jd.get("evidence") or [])
            deductions += (jd.get("deductions") or [])
        worst = min(scores, key=lambda sj: sj[0])[1]
        fix = worst.get("fix") if worst.get("score", 10) < 8 else None
        dims_out[d] = {
            "score": med, "evidence": _dedup(evidence)[:6], "deductions": _dedup(deductions)[:6],
            "fix": fix, "low_confidence": spread >= 3, "spread": spread, "per_judge": vals,
        }
        dim_medians[d] = med
    overall = round(sum(weights[d] * dim_medians[d] for d in DIMS), 1)
    # red-team severity cap — but ONLY when the hostile-client reject is CORROBORATED by a genuinely
    # low core dimension. A red-team will always name *some* reason at high severity; on its own that's
    # noise and would cap every package. Requiring a low core dim (completeness/task_fit/executability
    # ≤ 4) makes the cap fire on real show-stoppers (missing mandatory copy) but not on decent packages.
    rt = panel.get("redteam")
    rt_cap = None
    if rt and isinstance(rt.get("severity"), (int, float)):
        sev = rt["severity"]
        # Ground the cap in DETERMINISTIC truth where available. Fire only when the hostile-client
        # reject is corroborated by EITHER (a) a real machine-detected structural defect (a data asset
        # failing its required-field checks), OR (b) a UNANIMOUS judge consensus that a core dim is low.
        # This kills the 5.0↔8.3 flicker: a structurally-complete package can't be capped by one noisy
        # completeness vote, but a genuine missing-mandatory defect still craters the score.
        def _all_low(d, thr=4):
            pj = dims_out.get(d, {}).get("per_judge", [])
            return bool(pj) and all(v <= thr for v in pj)
        unanimous_low = any(_all_low(d) for d in ("completeness", "task_fit", "executability"))
        if sev >= 8 and (has_det_defect or unanimous_low):
            rt_cap = 3.5 if sev >= 9 else 5.0
            if overall > rt_cap:
                overall = rt_cap
    # top risks
    risks = []
    if rt:
        risks.append("CLIENT-REJECT (sev %s%s): %s" % (
            rt.get("severity"), " — capped overall to %.1f" % rt_cap if rt_cap else "",
            rt.get("rejection_reason")))
        risks.append("AGENT CHOKE on '%s': %s" % (rt.get("choke_asset_key"), rt.get("choke_reason")))
    lowest = sorted(DIMS, key=lambda d: dim_medians[d])[:2]
    for d in lowest:
        if dim_medians[d] < 7:
            risks += ["%s %d/10: %s" % (DIM_LABEL[d], dim_medians[d], x) for x in dims_out[d]["deductions"][:1]]
    gaps = qc_cross_check(man, dim_medians)
    return {
        "dimensions": dims_out, "overall": overall, "verdict": verdict_for(overall),
        "top_risks": _dedup(risks)[:6], "qc_gaps": gaps,
        "redteam": rt, "weights": weights,
    }


def _dedup(seq):
    seen, out = set(), []
    for x in seq:
        k = str(x).strip().lower()
        if k and k not in seen:
            seen.add(k); out.append(x)
    return out


# --------------------------------------------------------------------------
# Per-task judging
# --------------------------------------------------------------------------
def judge_task(task_id, panel_providers, skip_images, thumb_px, log, meter) -> dict:
    td = task_dir_for(task_id)
    if not (td / "manifest.json").exists():
        raise RuntimeError("no manifest for task %s at %s" % (task_id, td))
    bundle = load_package(td, skip_images=skip_images, thumb_px=thumb_px)
    weights = WEIGHTS[archetype_for(bundle["man"])]
    log.log("task %s (%s): %d images, %d data, archetype=%s" % (
        task_id, bundle["man"]["slug"], len(bundle["images"]), len(bundle["texts"]),
        archetype_for(bundle["man"])))
    start = meter.usd
    has_det_defect = bool(deterministic_defects(task_id, td))  # ground-truth structural defect signal
    pj = PackageJudge(TextLLM(log), log, meter, panel_providers)
    panel = pj.run_panel(bundle, weights)
    agg = aggregate(panel, weights, bundle["man"], has_det_defect=has_det_defect)
    judgement = {
        "task_id": task_id, "slug": bundle["man"]["slug"], "title": bundle["man"]["title"],
        "category": bundle["man"]["category"], "family": bundle["man"]["family"],
        "archetype": archetype_for(bundle["man"]),
        "panel": {"judges_ran": panel["ran"], "judges_failed": panel["failed"],
                  "confidence": "single-judge" if len(panel["ran"]) == 1 else "panel"},
        "dimensions": agg["dimensions"], "overall": agg["overall"], "verdict": agg["verdict"],
        "top_risks": agg["top_risks"], "qc_gaps": agg["qc_gaps"],
        "weights": agg["weights"], "judge_cost_usd": round(meter.usd - start, 4),
        "rounds": read_json(td / "judgement.json", {}).get("rounds", []),
    }
    write_json(td / "judgement.json", judgement)
    log.log("task %s: overall %.1f (%s) — %s" % (
        task_id, agg["overall"], agg["verdict"], ", ".join("%s %d" % (
            d[:4], agg["dimensions"][d]["score"]) for d in DIMS)))
    return judgement


# --------------------------------------------------------------------------
# Closed regeneration loop
# --------------------------------------------------------------------------
class ImproveArgs:
    def __init__(self, asset=None, images_provider=None):
        self.quiet = False
        self.force = False
        self.asset = asset
        self.images_provider = images_provider
        self.skip_vision_qc = False
        self.yes = True


def _base_key(k):
    return k.split("[")[0]


def collect_fixes(judgement: dict, threshold: float) -> dict:
    """{base_asset_key: prompt_delta} — ONE clean fix per asset (the most critical), never a
    concatenation (concatenated multi-part instructions make the patch LLM drop fields)."""
    best = {}  # base_key -> (score, delta)
    for d in DIMS:
        dd = judgement["dimensions"][d]
        fx = dd.get("fix")
        if dd["score"] < threshold and fx and fx.get("target_asset_key"):
            bk = _base_key(fx["target_asset_key"])
            delta = fx.get("prompt_delta") or fx.get("problem") or ""
            if delta and (bk not in best or dd["score"] < best[bk][0]):
                best[bk] = (dd["score"], delta)  # keep the lowest-scoring (most critical) dim's fix
    fixes = {bk: v[1] for bk, v in best.items()}
    rt = judgement.get("redteam") or {}
    if rt.get("choke_asset_key") and rt.get("severity", 0) >= 7:
        bk = _base_key(rt["choke_asset_key"])
        fixes.setdefault(bk, rt.get("choke_reason") or "")  # only if not already targeted
    return {k: v for k, v in fixes.items() if v}


def _spec_keys(task_id):
    return {a["key"] for a in specs_mod.SPECS[task_id]["assets"]}


def deterministic_defects(task_id, td) -> dict:
    """{data_asset_key: targeted_fix} for every data asset whose own data_checks FAIL right now.
    This is the most reliable 'genuinely broken' signal — independent of judge opinion."""
    from generate import data_checks
    out = {}
    for a in specs_mod.SPECS[task_id]["assets"]:
        if a.get("kind") != "data":
            continue
        f = td / "assets" / a["filename"]
        if not f.exists():
            continue
        checks = a.get("qc", {}).get("checks")
        try:
            data_checks(read_json(f), checks)
        except Exception as e:
            req = [c.split("[].")[-1] for c in (checks or []) if "[]." in c]
            out[a["key"]] = ("Restore/populate every record's mandatory fields: %s. None may be null or empty. "
                             "(failing check: %s)" % (", ".join(req), str(e)[:90]))
    return out


def select_targets(task_id, td, judgement, threshold) -> dict:
    """Smallest set of assets that resolves the detected defects, prioritizing reliable signals and
    AVOIDING image churn (don't re-roll a logo as collateral for a data problem).
      1) deterministic data-check failures (cheap, unambiguous)
      2) the red-team choke asset (single most-critical; may be an image — that's the real flag)
      3) only if neither: the single lowest-scoring dimension's fix."""
    spec_keys = _spec_keys(task_id)
    targets = {k: v for k, v in deterministic_defects(task_id, td).items() if k in spec_keys}
    rt = judgement.get("redteam") or {}
    if rt.get("choke_asset_key") and rt.get("severity", 0) >= 7:
        bk = _base_key(rt["choke_asset_key"])
        if bk in spec_keys:
            targets.setdefault(bk, rt.get("choke_reason") or "")
    if not targets:
        best = None  # (score, key, delta)
        for d in DIMS:
            dd = judgement["dimensions"][d]
            fx = dd.get("fix")
            if dd["score"] < threshold and fx and fx.get("target_asset_key"):
                bk = _base_key(fx["target_asset_key"])
                delta = fx.get("prompt_delta") or fx.get("problem") or ""
                if bk in spec_keys and delta and (best is None or dd["score"] < best[0]):
                    best = (dd["score"], bk, delta)
        if best:
            targets[best[1]] = best[2]
    return targets


def estimate_regen(task_id, fixes, images_provider) -> float:
    rec, spec = specs_mod.load_task(task_id)
    usd = 0.0
    for a in spec["assets"]:
        if a["key"] in fixes and a["kind"] == "image":
            r = config.resolve(a["generator_role"], images_provider)
            if r:
                prov, model, q = r
                usd += a.get("count", 1) * config.image_price(prov, model, q, a.get("size", "1024x1024"))
    return usd


def improve_task(task_id, threshold, rounds, panel_providers, skip_images, thumb_px,
                 cost_gate, yes, log, meter):
    from generate import TaskRunner  # local import (heavy module)
    td = task_dir_for(task_id)
    rounds_log = []
    prev_overall = None
    spent_regen = 0.0
    last_j = None              # most recent judging
    needs_final_judge = False  # True only if the last round regenerated without a subsequent judging
    for rnd in range(1, min(rounds, 2) + 1):
        j = judge_task(task_id, panel_providers, skip_images, thumb_px, log, meter)
        last_j, needs_final_judge = j, False
        if j["overall"] >= threshold:
            log.log("round %d: overall %.1f >= threshold %.1f — stop" % (rnd, j["overall"], threshold))
            rounds_log.append({"round": rnd, "overall": j["overall"], "action": "met-threshold"})
            break
        if prev_overall is not None and j["overall"] <= prev_overall:
            log.log("round %d: overall %.1f did not improve over %.1f — STALLED, stop" % (
                rnd, j["overall"], prev_overall))
            rounds_log.append({"round": rnd, "overall": j["overall"], "action": "stalled"})
            break
        prev_overall = j["overall"]
        # scope to the genuinely-broken asset(s) — deterministic failures first, no image churn
        fixes = select_targets(task_id, td, j, threshold)
        if not fixes:
            log.log("round %d: no actionable fixes — stop" % rnd)
            rounds_log.append({"round": rnd, "overall": j["overall"], "action": "no-fixes"})
            break
        est = estimate_regen(task_id, fixes, None)
        if spent_regen + est > cost_gate and not yes:
            log.log("round %d: regen est $%.2f would exceed gate $%.2f — stop (use --yes)" % (rnd, est, cost_gate))
            rounds_log.append({"round": rnd, "overall": j["overall"], "action": "cost-gated"})
            break
        # snapshot current files of flagged assets
        man = read_json(td / "manifest.json")
        for a in man["assets"]:
            if _base_key(a["key"]) in fixes and a.get("file") and (td / a["file"]).exists():
                snap = td / "originals" / ("preimprove_r%d_%s" % (rnd, Path(a["file"]).name))
                snap.parent.mkdir(exist_ok=True)
                snap.write_bytes((td / a["file"]).read_bytes())
        write_json(td / "feedback.json", fixes)
        # regenerate in spec-declaration order so dependencies (e.g. brand_pack) precede dependents (ad_copy)
        spec_order = [a["key"] for a in specs_mod.SPECS[task_id]["assets"]]
        ordered = sorted(fixes, key=lambda k: spec_order.index(k) if k in spec_order else 99)
        log.log("round %d: overall %.1f -> regenerating %s (est $%.2f)" % (
            rnd, j["overall"], ordered, est))
        for bk in ordered:
            runner = TaskRunner(task_id, ImproveArgs(asset=bk))
            runner.run()
            spent_regen += runner.meter.usd
        (td / "feedback.json").unlink(missing_ok=True)
        needs_final_judge = True  # we changed the assets; the saved score must reflect post-regen state
        # DETERMINISTIC fix-verification: did the flagged assets pass their own checks?
        # (a patch that fails required_fields is marked qc.status=failed by the generator)
        man2 = read_json(td / "manifest.json")
        unresolved = sorted({_base_key(a["key"]) for a in man2["assets"]
                             if _base_key(a["key"]) in fixes and (a.get("qc") or {}).get("status") == "failed"})
        resolved = [k for k in fixes if k not in unresolved]
        log.log("round %d: regenerated %s — resolved %s, UNRESOLVED %s" % (rnd, ordered, resolved, unresolved))
        rounds_log.append({"round": rnd, "overall": j["overall"], "action": "regenerated",
                           "assets": list(fixes), "resolved": resolved, "unresolved": unresolved,
                           "regen_cost": round(spent_regen, 3)})
        if unresolved:  # a fix the loop could not verify — do not keep spending / claiming success
            log.log("round %d: %s could not be verified fixed — stop (no false recovery)" % (rnd, unresolved))
            break
    # Only re-judge if the LAST round regenerated assets that were never subsequently judged.
    # If the loop already judged the current state (met-threshold / stall / no-fixes), reuse that
    # judging — running another judge would just add a noisy sample that can clobber a good result.
    if needs_final_judge or last_j is None:
        final = judge_task(task_id, panel_providers, skip_images, thumb_px, log, meter)
    else:
        final = last_j
        log.log("loop already judged current state (overall %.1f) — skipping redundant final judge" % final["overall"])
    all_unresolved = sorted({u for r in rounds_log for u in r.get("unresolved", [])})
    # DETERMINISTIC ground-truth signal — independent of the noisy LLM score: are there any
    # structural defects (data assets failing their own required-field checks) left?
    remaining = sorted(deterministic_defects(task_id, td).keys())
    loop_success = (not all_unresolved) and (not remaining)
    final["rounds"] = rounds_log + [{"round": "final", "overall": final["overall"], "action": "final-judge"}]
    final["regen_cost_usd"] = round(spent_regen, 3)
    final["unresolved_fixes"] = all_unresolved
    final["deterministic_defects_remaining"] = remaining
    final["loop_success"] = loop_success          # the trustworthy verdict (not the noisy score)
    if not loop_success:
        final["verdict"] = "needs-rework (unresolved: %s)" % ", ".join(all_unresolved + remaining)
    write_json(td / "judgement.json", final)
    log.log("task %s improve done: score %.1f->%.1f | loop_success=%s%s (deterministic: %s)" % (
        task_id, rounds_log[0]["overall"] if rounds_log else final["overall"], final["overall"],
        loop_success, " UNRESOLVED:%s" % all_unresolved if all_unresolved else "",
        "all structural defects fixed" if not remaining else "remaining %s" % remaining))
    return final


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def all_task_ids():
    ids = list(specs_mod.PILOT_ORDER) + [t for t in specs_mod.PILOT2_ORDER if t not in specs_mod.PILOT_ORDER]
    return ids + [t for t in getattr(specs_mod, "FLAGSHIP_ORDER", []) if t not in ids]


def cmd_check(args):
    log = RunLogger(None)
    pj = PackageJudge(TextLLM(log), log, CostMeter(), _panel(args))
    judges = pj.available_judges()
    print("Provider keys: " + ", ".join("%s=%s" % (k, "set" if v else "MISSING")
                                         for k, v in config.PROVIDERS.items()))
    print("Resolved judge panel (%d): %s" % (len(judges), ", ".join("%s/%s" % j for j in judges) or "NONE"))
    if not config.PROVIDERS.get("anthropic"):
        print("  (add ANTHROPIC_API_KEY to .env to light up the 3rd judge)")
    print("\nPer-task token exposure:")
    total = 0.0
    for tid in (args.task or all_task_ids()):
        td = task_dir_for(tid)
        if not (td / "manifest.json").exists():
            print("  task %-5s — NO manifest" % tid); continue
        man = read_json(td / "manifest.json")
        ni = sum(1 for a in man["assets"] if a.get("kind") == "image" and a.get("file"))
        nd = sum(1 for a in man["assets"] if a.get("kind") in ("data", "text") and a.get("file"))
        est = len(judges) * (config.PRICES["judge_call"] + min(ni, MAX_IMAGES) * config.PRICES["judge_image_surcharge"])
        est += config.PRICES["judge_call"]  # redteam
        total += est
        print("  task %-5s %-22s %2d img %d data  est $%.3f" % (tid, man["slug"], ni, nd, est))
    print("Estimated judge spend for the set: ~$%.2f (excludes any --improve regeneration)" % total)


def _panel(args):
    return [p.strip() for p in args.panel.split(",")] if args.panel else None


def main():
    ap = argparse.ArgumentParser(description="Package judge + closed regeneration loop")
    ap.add_argument("--task", action="append", type=int)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--improve", action="store_true")
    ap.add_argument("--threshold", type=float, default=7.5)
    ap.add_argument("--rounds", type=int, default=2)
    ap.add_argument("--panel")
    ap.add_argument("--thumb-px", type=int, default=THUMB_PX)
    ap.add_argument("--skip-images", action="store_true")
    ap.add_argument("--cost-gate", type=float, default=config.COST_GATE_USD)
    ap.add_argument("--yes", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if args.check:
        cmd_check(args); return

    ids = all_task_ids() if args.all else (args.task or [])
    if not ids:
        ap.error("pass --task ID (repeatable), --all, or --check")
    log = RunLogger(None, quiet=args.quiet)
    meter = CostMeter()
    judgements = []
    for tid in ids:
        try:
            if args.improve:
                j = improve_task(tid, args.threshold, args.rounds, _panel(args), args.skip_images,
                                 args.thumb_px, args.cost_gate, args.yes, log, meter)
            else:
                j = judge_task(tid, _panel(args), args.skip_images, args.thumb_px, log, meter)
            judgements.append(j)
        except Exception as e:
            log.log("task %s FAILED: %s" % (tid, e))
    if judgements:
        scorecard.write_scorecard(judgements, config.OUT_ROOT)
    print("\n=== JUDGE SUMMARY ===")
    for j in sorted(judgements, key=lambda x: -x["overall"]):
        print("  task %-5s %5.1f  %-13s  %s" % (
            j["task_id"], j["overall"], j["verdict"],
            " ".join("%s%d" % (d[:2], j["dimensions"][d]["score"]) for d in DIMS)))
    print("Judge spend (est): $%.2f" % meter.usd)
    print("Scorecard: %s" % (config.OUT_ROOT / "scorecard.html"))


if __name__ == "__main__":
    main()
