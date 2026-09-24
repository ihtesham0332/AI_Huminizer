"""Stylometric analysis: how templated does a paragraph read?

Signals are classic, interpretable stylometry (rhythm, repetition, stock phrasing).
This is a *planning* tool that tells the engine what to fix. It is deliberately
not a re-implementation of any commercial detector.
"""
from __future__ import annotations
from statistics import mean, pstdev

from .lexicon import find_stock, starts_with_transition
from .models import Profile
from .segment import split_sentences, words


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def analyze(text: str) -> Profile:
    sents = split_sentences(text)
    lens = [len(words(s)) for s in sents] or [0]
    n = len(sents)
    wc = sum(lens)
    m = mean(lens) if lens else 0.0
    burst = (pstdev(lens) / m) if (n >= 2 and m > 0) else 0.0

    openers = [(words(s) or [""])[0].lower() for s in sents]
    opener_rep = (1 - len(set(openers)) / n) if n > 1 else 0.0
    trans = (sum(starts_with_transition(s) for s in sents) / n) if n else 0.0
    hits = find_stock(text)
    stock_100 = (len(hits) / wc * 100) if wc else 0.0

    # Weighted blend; short paragraphs get a neutral rhythm component.
    rhythm = (1 - _clamp(burst / 0.6)) if n >= 3 else 0.3
    score = (
        0.35 * rhythm
        + 0.25 * _clamp(stock_100 / 2.0)
        + 0.20 * _clamp(trans / 0.4)
        + 0.10 * _clamp(opener_rep / 0.5)
        + 0.10 * _clamp((m - 20) / 10)
    ) if m else 0.0
    return Profile(n, wc, round(m, 2), round(burst, 3), round(opener_rep, 3),
                   round(trans, 3), hits, round(stock_100, 3), round(_clamp(score), 3))
