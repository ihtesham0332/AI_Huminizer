"""Versioned pattern catalog of stock phrasing that makes prose read as templated.

These are *style* patterns (over-used by both LLMs and content mills), not
detector signatures. Extend via your own data flywheel.
"""
from __future__ import annotations
import re

LEXICON_VERSION = "2026.1"

STOCK_REPLACEMENTS: dict[str, str] = {
    "delve into": "look at", "delves into": "looks at", "delving into": "looking at",
    "in today's fast-paced world": "today", "in today's digital age": "today",
    "in today's world": "today", "in the ever-evolving landscape of": "in",
    "it is important to note that": "", "it's important to note that": "",
    "it is worth noting that": "", "it should be noted that": "",
    "plays a crucial role in": "matters for", "plays a vital role in": "matters for",
    "plays a pivotal role in": "shapes",
    "a testament to": "proof of", "rich tapestry": "mix", "tapestry": "mix",
    "in the realm of": "in", "navigate the complexities of": "deal with",
    "unlock the potential of": "make use of", "harness the power of": "use",
    "embark on a journey": "start", "game-changer": "big shift",
    "cutting-edge": "modern", "state-of-the-art": "modern",
    "leveraging": "using", "leverage": "use", "utilizing": "using", "utilize": "use",
    "comprehensive": "thorough", "robust": "solid", "seamlessly": "smoothly",
    "seamless": "smooth", "pivotal": "key", "multifaceted": "complex",
    "underscores": "shows", "fosters": "encourages", "foster": "encourage",
    "in conclusion,": "", "in summary,": "", "to summarize,": "",
}

TRANSITIONS = (
    "moreover", "furthermore", "additionally", "in addition", "consequently",
    "therefore", "thus", "hence", "in conclusion", "to summarize", "in summary",
    "overall", "ultimately", "nevertheless", "nonetheless", "likewise", "in essence",
)

_STOCK_RE = re.compile(
    "|".join(sorted((re.escape(k.rstrip(",")) for k in STOCK_REPLACEMENTS), key=len, reverse=True)),
    re.IGNORECASE,
)
_TRANS_RE = re.compile(r"^\W*(?:%s)\b" % "|".join(re.escape(t) for t in TRANSITIONS), re.IGNORECASE)


def find_stock(text: str) -> list[str]:
    return [m.group(0).lower() for m in _STOCK_RE.finditer(text)]


def starts_with_transition(sentence: str) -> bool:
    return bool(_TRANS_RE.match(sentence))
