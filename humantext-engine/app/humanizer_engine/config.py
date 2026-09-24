from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(frozen=True)
class LevelSpec:
    """Explicit rewrite knobs (the DIPPER-style 'diversity control')."""
    name: str
    n_candidates: int
    temperature: float
    target_novelty: float      # desired 1 - 3-gram overlap with the original
    min_similarity: float      # hard floor on semantic similarity
    allow_restructure: bool    # merge / split / reorder sentences
    max_revision_rounds: int   # critic-driven revisions


LEVELS: dict[int, LevelSpec] = {
    1: LevelSpec("light",    1, 0.70, 0.25, 0.40, False, 0),
    2: LevelSpec("gentle",   1, 0.80, 0.35, 0.30, False, 0),
    3: LevelSpec("balanced", 1, 0.85, 0.55, 0.15, True,  0),
    4: LevelSpec("strong",   1, 0.90, 0.70, 0.10, True,  1),
    5: LevelSpec("deep",     1, 0.95, 0.85, 0.05, True,  1),
}

TONES: dict[str, str] = {
    "standard": "Clear, natural, moderately formal prose.",
    "formal": "Formal and precise; no slang; contractions avoided.",
    "casual": "Conversational and relaxed; contractions welcome; shorter sentences.",
    "academic": "Scholarly register; cautious claims; discipline-appropriate vocabulary.",
    "creative": "Vivid and rhythmic; concrete images over abstractions.",
}


@dataclass
class ScoreWeights:
    fidelity: float = 0.40
    style: float = 0.30
    novelty: float = 0.15
    fluency: float = 0.15


@dataclass
class EngineConfig:
    level: int = 3
    tone: str = "standard"
    max_concurrency: int = 6
    max_tokens: int = 1200
    provider_retries: int = 2
    cache_size: int = 512
    skip_below_template: float = 0.15   # paragraphs already natural are left alone
    min_words_to_rewrite: int = 6
    length_ratio_bounds: tuple[float, float] = (0.55, 1.6)
    weights: ScoreWeights = field(default_factory=ScoreWeights)
