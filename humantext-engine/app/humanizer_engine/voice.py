"""Voice profiles: extract measurable habits from a writing sample."""
from __future__ import annotations
import re
from dataclasses import dataclass
from statistics import mean, pstdev

from .segment import split_sentences, words


@dataclass
class VoiceProfile:
    mean_len: float
    len_spread: float
    contractions_per_100w: float
    first_person: bool
    em_dashes: bool
    semicolons: bool
    questions: bool

    def to_prompt(self) -> str:
        bits = [f"average sentence about {round(self.mean_len)} words, varying by about {round(self.len_spread)}"]
        bits.append("uses contractions freely" if self.contractions_per_100w >= 1.5 else
                    "rarely uses contractions")
        if self.first_person: bits.append("writes in first person")
        if self.em_dashes: bits.append("likes dashes")
        if self.semicolons: bits.append("uses semicolons")
        if self.questions: bits.append("sometimes asks rhetorical questions")
        return "; ".join(bits)


def extract_voice(sample: str) -> VoiceProfile | None:
    sents = split_sentences(sample)
    ws = words(sample)
    if len(ws) < 40 or not sents:
        return None
    lens = [len(words(s)) for s in sents]
    contr = len(re.findall(r"\b\w+['’](?:t|s|re|ve|ll|d|m)\b", sample))
    return VoiceProfile(
        mean_len=mean(lens), len_spread=pstdev(lens) if len(lens) > 1 else 0.0,
        contractions_per_100w=contr / len(ws) * 100,
        first_person=bool(re.search(r"\b(I|my|we|our)\b", sample)),
        em_dashes="—" in sample or " - " in sample,
        semicolons=";" in sample, questions="?" in sample,
    )
