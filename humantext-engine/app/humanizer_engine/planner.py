from __future__ import annotations
from dataclasses import dataclass

from .config import LevelSpec
from .models import Profile


@dataclass
class Plan:
    ops: list[str]


def build_plan(p: Profile, level: LevelSpec) -> Plan:
    ops = ["Preserve every fact, number, name and every ⟦E#⟧ token."]
    if p.stock_hits:
        ops.append("Replace these stock phrases with plain wording: " + ", ".join(sorted(set(p.stock_hits))))
    if p.n_sentences >= 3 and p.burstiness < 0.35:
        ops.append("Vary sentence length: include at least one very short sentence and one longer one.")
    if p.transition_density > 0.25:
        ops.append("Remove most sentence-initial connectives (Moreover, Furthermore, Additionally...).")
    if p.opener_repeat > 0.3:
        ops.append("Vary how sentences begin.")
    if level.allow_restructure and p.n_sentences >= 2:
        ops.append("You may merge, split, or reorder sentences and clauses where it reads better.")
    if p.mean_len > 24:
        ops.append("Break up overlong sentences.")
    ops.append("Eliminate semicolons (;), topic colons (:), and formulaic brochure lists. Use natural contractions throughout.")
    ops.append("Never include hashtags (#...) or corporate closing formulas.")
    return Plan(ops)
