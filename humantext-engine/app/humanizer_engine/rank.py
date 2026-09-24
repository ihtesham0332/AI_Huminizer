from __future__ import annotations
import re

from .config import LevelSpec, ScoreWeights
from .models import Candidate
from .segment import split_sentences, words


def fluency_score(text: str) -> float:
    """Cheap fluency proxy: penalise stutters, run-ons, missing terminal punctuation."""
    pen = 0.0
    ws = [w.lower() for w in words(text)]
    pen += 0.15 * sum(1 for a, b in zip(ws, ws[1:]) if a == b and a not in {"that", "had"})
    for s in split_sentences(text):
        n = len(words(s))
        if n > 45: pen += 0.15
        if n < 2: pen += 0.05
    if text and text.rstrip()[-1] not in ".!?\"'”)⟧]":
        pen += 0.1
    if re.search(r"\s[,.;]", text): pen += 0.05
    return max(0.0, 1.0 - pen)


def score(c: Candidate, spec: LevelSpec, w: ScoreWeights) -> float:
    m = c.verdict.metrics
    style = 1.0 - m["template_after"]
    burstiness = min(1.0, m.get("burstiness_after", 0.0) / 5.0)
    nov = min(1.0, m["novelty"] / max(spec.target_novelty, 0.2))
    flu = fluency_score(c.text)
    
    # Penalize remaining stock phrases, semicolons, and hashtags
    penalty = 0.20 * m["stock_left"]
    if ";" in c.text:
        penalty += 0.2
    if "#" in c.text:
        penalty += 0.3
    if re.search(r"\bwhether\s+(?:it\'s\s+for|for)\s+", c.text, re.IGNORECASE):
        penalty += 0.25
        
    return round(0.35 * style + 0.25 * burstiness + 0.25 * nov + 0.15 * flu - penalty, 4)


def rank(cands: list[Candidate], spec: LevelSpec, w: ScoreWeights) -> list[Candidate]:
    ok = [c for c in cands if c.verdict.passed]
    for c in ok:
        c.score = score(c, spec, w)
    return sorted(ok, key=lambda c: c.score, reverse=True)
