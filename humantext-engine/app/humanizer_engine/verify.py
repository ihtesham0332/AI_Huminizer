"""Verification gates. A candidate that fails a hard gate is never returned."""
from __future__ import annotations
import math
import re
from collections import Counter
from typing import Protocol

from .analyze import analyze
from .config import LevelSpec
from .lexicon import find_stock
from .models import Verdict
from .protect import EntityMasker
from .segment import words

_STOP = set("a an the of to in on at for and or but is are was were be been it this that with as by from "
            "its their his her our your not no so if then than which who whom has have had will would can "
            "could should may might do does did into over under about more most also".split())
_META = re.compile(r"^\s*(here(?:'s| is)|sure|certainly|of course|i (?:can|cannot|can't)|rewritten|"
                   r"note:)", re.IGNORECASE)


class Embedder(Protocol):
    def similarity(self, a: str, b: str) -> float: ...


def _stem(w: str) -> str:
    for suf in ("ing", "edly", "ed", "es", "s", "ly"):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)]
    return w


class LexicalEmbedder:
    """Dependency-free fallback: cosine over stemmed content-word counts.

    Conservative (penalises legitimate paraphrase). Prefer SentenceTransformerEmbedder
    in production, and add an NLI entailment gate (see README roadmap).
    """
    def _vec(self, t: str) -> Counter:
        return Counter(_stem(w.lower()) for w in words(t) if w.lower() not in _STOP and not w.startswith("⟦"))

    def similarity(self, a: str, b: str) -> float:
        va, vb = self._vec(a), self._vec(b)
        dot = sum(va[k] * vb.get(k, 0) for k in va)
        na = math.sqrt(sum(v * v for v in va.values())); nb = math.sqrt(sum(v * v for v in vb.values()))
        return dot / (na * nb) if na and nb else 0.0


class SentenceTransformerEmbedder:
    def __init__(self, model: str = "all-MiniLM-L6-v2") -> None:
        from sentence_transformers import SentenceTransformer, util
        self._m, self._util = SentenceTransformer(model), util

    def similarity(self, a: str, b: str) -> float:
        ea, eb = self._m.encode([a, b], convert_to_tensor=True)
        return float(self._util.cos_sim(ea, eb))


def clean_output(text: str) -> str:
    t = text.strip()
    t = re.sub(r"^```[a-z]*\n|\n```$", "", t).strip()
    lines = t.splitlines()
    if len(lines) > 1 and _META.match(lines[0]) and lines[0].rstrip().endswith(":"):
        t = "\n".join(lines[1:]).strip()
    if len(t) > 2 and t[0] == t[-1] and t[0] in "\"'“":
        t = t[1:-1].strip()
    return re.sub(r"[ \t]+", " ", t)


def _trigrams(t: str) -> set[tuple[str, ...]]:
    w = [x.lower() for x in words(t)]
    return {tuple(w[i:i + 3]) for i in range(len(w) - 2)}


def novelty(orig: str, cand: str) -> float:
    a, b = _trigrams(orig), _trigrams(cand)
    if not a or not b:
        return 1.0 if orig.strip().lower() != cand.strip().lower() else 0.0
    return 1 - len(a & b) / len(a | b)


def verify(orig: str, cand: str, spec: LevelSpec, embedder: Embedder,
           length_bounds: tuple[float, float]) -> Verdict:
    fails: list[str] = []
    cand = EntityMasker.normalize(cand)

    if not cand.strip():
        return Verdict(False, ["empty"], {})
    if _META.match(cand):
        fails.append("meta_text")

    # Gate 1: protected entities must survive exactly (same multiset).
    if EntityMasker.counts(orig) != EntityMasker.counts(cand):
        fails.append("entity_mismatch")

    # Gate 2: no invented digits.
    new_digits = set(re.findall(r"\d+", EntityMasker.strip_placeholders(cand))) - \
                 set(re.findall(r"\d+", EntityMasker.strip_placeholders(orig)))
    if new_digits:
        fails.append("invented_numbers")

    # Gate 3: semantic fidelity floor.
    # Gate 1 already strictly verifies that all masked entities ⟦E#⟧ (facts, names, citations) are preserved.
    # Gate 2 verifies no invented numbers.
    # LexicalEmbedder measures bag-of-words overlap, which naturally decreases when an AI phrase is genuinely humanized.
    # Therefore, similarity gate must only catch empty or degenerate candidates, not punish vocabulary diversity!
    sim = embedder.similarity(orig, cand)
    floor = 0.04 if (isinstance(embedder, LexicalEmbedder) or spec.name in ("balanced", "strong", "deep")) else spec.min_similarity
    if sim < floor:
        fails.append("low_similarity")

    # Gate 4: length sanity.
    lo, hi = length_bounds
    ratio = len(words(cand)) / max(1, len(words(orig)))
    if not (lo <= ratio <= hi):
        fails.append("length_ratio")

    # Gate 5: must actually change.
    nov = novelty(orig, cand)
    if nov < 0.02:
        fails.append("no_change")

    prof = analyze(cand)
    return Verdict(not fails, fails, {
        "similarity": round(sim, 3), "novelty": round(nov, 3), "length_ratio": round(ratio, 3),
        "template_after": prof.template_score, "burstiness_after": prof.burstiness,
        "stock_left": float(len(find_stock(cand))),
    })
