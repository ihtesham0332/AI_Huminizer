"""Rule-based critic: turns measurable weaknesses into concrete revision instructions."""
from __future__ import annotations
from .analyze import analyze
from .models import Profile


def critique(text: str, before: Profile) -> list[str]:
    p = analyze(text)
    issues: list[str] = []
    if p.stock_hits:
        issues.append("Still contains stock phrasing: " + ", ".join(sorted(set(p.stock_hits))) +
                      ". Replace with plain, specific wording.")
    if p.n_sentences >= 3 and p.burstiness < 0.35:
        issues.append("Sentence lengths are too uniform. Mix a few short sentences (under 8 words) "
                      "with longer ones.")
    if p.transition_density > 0.25:
        issues.append("Too many sentences start with connective transitions. Let ideas connect through "
                      "content instead.")
    if p.opener_repeat > 0.3:
        issues.append("Several sentences start with the same word. Vary the openings.")
    if ";" in text:
        issues.append("Remove all semicolons (;). Split into separate punchy sentences using periods.")
    if "#" in text:
        issues.append("Remove all hashtags (#). Do not include any tags.")
    if ":" in text and any(w in text.lower() for w in ("topic:", "lesson:", "note:", "important topic:")):
        issues.append("Remove formulaic topic colons (:). Write in natural narrative flow.")
    import re
    if re.search(r"\bwhether\s+(?:it\'s\s+for|for)\s+", text, re.IGNORECASE):
        issues.append("Eliminate formulaic brochure list ('whether it's for A, B, C, or D'). State the point simply and naturally without parallel list enumeration.")
    if re.search(r"\b(?:isn\'t|is not)\s+just\s+about\b", text, re.IGNORECASE):
        issues.append("Eliminate formulaic antithesis ('isn't just about X; it's about Y'). Express the thought in authentic human conversational words.")
    if re.search(r"\bThanks,\s*.*?for sharing\b", text, re.IGNORECASE):
        issues.append("Remove corporate thank-you boilerplate. Conclude with a natural human sign-off.")
    return issues
