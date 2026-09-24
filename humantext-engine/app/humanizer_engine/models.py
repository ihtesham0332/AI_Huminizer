from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class Profile:
    """Measurable 'template-ness' of a paragraph. Heuristic, not a detector."""
    n_sentences: int
    n_words: int
    mean_len: float
    burstiness: float        # coefficient of variation of sentence length
    opener_repeat: float     # share of repeated sentence openers
    transition_density: float
    stock_hits: list[str]
    stock_per_100w: float
    template_score: float    # 0 (natural) .. 1 (highly templated)

    def brief(self) -> dict[str, Any]:
        d = asdict(self)
        return {k: (round(v, 3) if isinstance(v, float) else v) for k, v in d.items()}


@dataclass
class Verdict:
    passed: bool
    failures: list[str]
    metrics: dict[str, float]


@dataclass
class Candidate:
    text: str                 # masked text
    verdict: Verdict
    score: float = 0.0


@dataclass
class ParagraphResult:
    index: int
    status: str               # rewritten | skipped | fallback
    original: str
    output: str
    alternatives: list[str] = field(default_factory=list)
    before: dict[str, Any] = field(default_factory=dict)
    after: dict[str, Any] = field(default_factory=dict)
    fidelity: float | None = None
    notes: list[str] = field(default_factory=list)
