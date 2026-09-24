"""Orchestrator: ingest -> mask -> analyze -> plan -> generate -> verify -> rank -> critique -> assemble."""
from __future__ import annotations
import asyncio
import hashlib
from collections import OrderedDict
from dataclasses import dataclass, field, asdict
from typing import Any

from .analyze import analyze
from .config import EngineConfig, LEVELS, TONES, LevelSpec
from .critic import critique
from .models import Candidate, ParagraphResult
from .planner import build_plan
from .prompts import SYSTEM, build_user_prompt
from .protect import EntityMasker
from .providers import Provider
from .rank import rank
from .segment import is_structural, split_paragraphs, words
from .verify import Embedder, LexicalEmbedder, clean_output, verify
from .voice import extract_voice
from app.core.scrubber import AntiAIScrubber


@dataclass
class HumanizeResult:
    text: str
    paragraphs: list[ParagraphResult]
    report: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"text": self.text, "report": self.report,
                "paragraphs": [asdict(p) for p in self.paragraphs]}


class HumanizerEngine:
    def __init__(self, provider: Provider, embedder: Embedder | None = None,
                 config: EngineConfig | None = None) -> None:
        self.provider = provider
        self.embedder = embedder or LexicalEmbedder()
        self.config = config or EngineConfig()
        self._cache: OrderedDict[str, list[str]] = OrderedDict()
        self.calls = 0

    # ------------------------------------------------------------------ public
    async def humanize(self, text: str, *, level: int | None = None, tone: str | None = None,
                       voice_sample: str | None = None) -> HumanizeResult:
        cfg = self.config
        spec = LEVELS[max(1, min(5, level or cfg.level))]
        tone = tone if tone in TONES else cfg.tone
        voice = extract_voice(voice_sample) if voice_sample else None
        voice_hint = voice.to_prompt() if voice else ""
        self.calls = 0

        masker = EntityMasker()
        masked_doc = masker.mask(text)
        paras = split_paragraphs(masked_doc)
        sem = asyncio.Semaphore(cfg.max_concurrency)

        tasks = [
            self._paragraph(i, p, paras[i - 1] if i else "", paras[i + 1] if i + 1 < len(paras) else "",
                            spec, tone, voice_hint, sem, masker)
            for i, p in enumerate(paras)
        ]
        results = await asyncio.gather(*tasks)
        out_text = "\n\n".join(r.output for r in results)
        return HumanizeResult(out_text, results, self._report(text, out_text, results, masker, spec, tone))

    def humanize_sync(self, text: str, **kw) -> HumanizeResult:
        return asyncio.run(self.humanize(text, **kw))

    # ---------------------------------------------------------------- internals
    async def _call(self, user: str, spec: LevelSpec, temp: float, seed: int) -> str | None:
        for attempt in range(self.config.provider_retries + 1):
            try:
                self.calls += 1
                raw = await self.provider.complete(SYSTEM, user, temperature=temp,
                                                   max_tokens=self.config.max_tokens, seed=seed)
                return clean_output(raw)
            except Exception:
                await asyncio.sleep(0.4 * (2 ** attempt))
        return None

    def _make_candidates(self, orig: str, raws: list[str | None], spec: LevelSpec) -> list[Candidate]:
        cands = []
        for r in raws:
            if not r:
                continue
            r = EntityMasker.normalize(r)
            v = verify(orig, r, spec, self.embedder, self.config.length_ratio_bounds)
            cands.append(Candidate(r, v))
        return cands

    async def _paragraph(self, idx: int, masked: str, prev_ctx: str, next_ctx: str, spec: LevelSpec,
                         tone: str, voice_hint: str, sem: asyncio.Semaphore,
                         masker: EntityMasker) -> ParagraphResult:
        cfg = self.config
        original = masker.unmask(masked)
        before = analyze(masked)

        if is_structural(masked) or before.n_words < cfg.min_words_to_rewrite:
            return ParagraphResult(idx, "skipped", original, original, before=before.brief(),
                                   notes=["structural or too short"])
        if before.template_score < cfg.skip_below_template and spec.name in ("light", "gentle"):
            return ParagraphResult(idx, "skipped", original, original, before=before.brief(),
                                   notes=["already reads naturally"])

        key = hashlib.sha256(f"{masked}|{spec.name}|{tone}|{voice_hint}|{self.provider.name}".encode()).hexdigest()
        if key in self._cache:
            self._cache.move_to_end(key)
            alts = self._cache[key]
            return self._finish(idx, original, alts, before, masker, note="cache hit")

        plan = build_plan(before, spec)
        user = build_user_prompt(masked, level=spec, tone=tone, ops=plan.ops, voice_hint=voice_hint,
                                 prev_ctx=prev_ctx[:600], next_ctx=next_ctx[:600])
        async with sem:
            raws = await asyncio.gather(*[
                self._call(user, spec, max(0.2, spec.temperature - 0.1 * i), seed=i)
                for i in range(spec.n_candidates)
            ])
        pool = self._make_candidates(masked, list(raws), spec)
        ranked = rank(pool, spec, cfg.weights)

        # Critic-driven revision rounds (bounded).
        for rnd in range(spec.max_revision_rounds):
            if not ranked:
                break
            issues = critique(ranked[0].text, before)
            if not issues:
                break
            rev_user = build_user_prompt(masked, level=spec, tone=tone, ops=plan.ops, voice_hint=voice_hint,
                                         prev_ctx=prev_ctx[:600], next_ctx=next_ctx[:600],
                                         draft=ranked[0].text, issues=issues)
            async with sem:
                rev = await self._call(rev_user, spec, max(0.3, spec.temperature - 0.2), seed=100 + rnd)
            pool += self._make_candidates(masked, [rev], spec)
            ranked = rank(pool, spec, cfg.weights)

        alts = [c.text for c in ranked[:3]]
        metrics = ranked[0].verdict.metrics if ranked else {}
        self._store(key, alts)
        res = self._finish(idx, original, alts, before, masker)
        if ranked:
            res.fidelity = metrics.get("similarity")
        else:
            fails = sorted({f for c in pool for f in c.verdict.failures}) or ["no_candidates"]
            res.notes.append("all candidates rejected: " + ", ".join(fails))
        return res

    def _finish(self, idx, original, alts, before, masker, note: str | None = None) -> ParagraphResult:
        if not alts:
            fallback_scrubbed = AntiAIScrubber.scrub(original)
            return ParagraphResult(idx, "fallback", original, fallback_scrubbed, before=before.brief(),
                                   notes=["kept original (scrubbed fail-safe)"])
        out = AntiAIScrubber.scrub(masker.unmask(alts[0]))
        r = ParagraphResult(idx, "rewritten", original, out,
                            alternatives=[AntiAIScrubber.scrub(masker.unmask(a)) for a in alts],
                            before=before.brief(), after=analyze(alts[0]).brief())
        if note:
            r.notes.append(note)
        return r

    def _store(self, key: str, alts: list[str]) -> None:
        if not alts:
            return
        self._cache[key] = alts
        while len(self._cache) > self.config.cache_size:
            self._cache.popitem(last=False)

    def _report(self, src: str, out: str, results: list[ParagraphResult], masker: EntityMasker,
                spec: LevelSpec, tone: str) -> dict[str, Any]:
        rw = [r for r in results if r.status == "rewritten"]
        fid = [r.fidelity for r in rw if r.fidelity is not None]
        b = [r.before["template_score"] for r in rw]
        a = [r.after["template_score"] for r in rw]
        # Final end-to-end integrity check on the *unmasked* document.
        lost = [v for _, v in masker.entities.values() if v not in out and v in src]
        return {
            "level": spec.name, "tone": tone, "provider": self.provider.name,
            "paragraphs": len(results),
            "rewritten": len(rw),
            "skipped": sum(r.status == "skipped" for r in results),
            "fallback": sum(r.status == "fallback" for r in results),
            "provider_calls": self.calls,
            "template_score_before": round(sum(b) / len(b), 3) if b else None,
            "template_score_after": round(sum(a) / len(a), 3) if a else None,
            "mean_fidelity": round(sum(fid) / len(fid), 3) if fid else None,
            "entities_protected": len(masker.entities),
            "entities_lost": lost,
            "words_in": len(words(src)), "words_out": len(words(out)),
        }
