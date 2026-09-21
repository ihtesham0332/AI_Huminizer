"""
HumanText Engine — Text Utilities
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Deterministic text processing utilities used by multiple skills.
These are pure Python functions — no LLM calls, no network, no side effects.

Functions here are reused by:
  - Skill 01 (Input Validation)
  - Skill 02 (Document Analysis)
  - Skill 08 (Readability Analysis)
  - Skill 13 (Terminology Preservation)
  - Skill 14 (Citation Preservation)
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from typing import Any


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEXT CLEANING & NORMALIZATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def clean_text(text: str) -> str:
    """
    Normalize text for processing without altering content.
    
    - Normalize Unicode (NFC)
    - Replace non-breaking spaces with regular spaces
    - Collapse multiple whitespace into single spaces
    - Strip leading/trailing whitespace
    - Preserve paragraph breaks (double newlines)
    """
    # Unicode normalization
    text = unicodedata.normalize("NFC", text)
    # Replace non-breaking spaces
    text = text.replace("\u00a0", " ").replace("\u200b", "")
    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Collapse multiple spaces (but NOT newlines)
    text = re.sub(r"[^\S\n]+", " ", text)
    # Collapse more than 2 consecutive newlines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip
    text = text.strip()
    return text


def normalize_whitespace(text: str) -> str:
    """Collapse all whitespace into single spaces."""
    return re.sub(r"\s+", " ", text).strip()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SENTENCE & PARAGRAPH SPLITTING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Abbreviations that should NOT trigger sentence splits
_ABBREVIATIONS = {
    "mr", "mrs", "ms", "dr", "prof", "sr", "jr", "st", "rd", "ave",
    "vs", "etc", "inc", "ltd", "corp", "dept", "univ",
    "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "oct", "nov", "dec",
    "fig", "eq", "no", "vol", "pp", "ed", "rev", "approx",
    "e.g", "i.e", "cf", "al",
}


def split_sentences(text: str) -> list[str]:
    """
    Split text into sentences using regex-based rules.
    
    Handles:
      - Standard period/question/exclamation endings
      - Abbreviations (Dr., Mr., etc.)
      - Decimal numbers (3.14)
      - Ellipsis (...)
      - Quoted sentences
    
    For more accurate splitting in production, use spaCy's sentencizer.
    This function is a fast, dependency-free fallback.
    """
    if not text.strip():
        return []

    # Split on sentence-ending punctuation followed by space and uppercase
    # But not after abbreviations or numbers
    pattern = r'(?<=[.!?])\s+(?=[A-Z"])'
    raw_splits = re.split(pattern, text)

    sentences: list[str] = []
    buffer = ""

    for chunk in raw_splits:
        chunk = chunk.strip()
        if not chunk:
            continue

        buffer = f"{buffer} {chunk}".strip() if buffer else chunk

        # Check if buffer ends with an abbreviation
        last_word = buffer.rstrip(".!?").rsplit(None, 1)[-1].lower() if buffer else ""
        if last_word in _ABBREVIATIONS:
            continue  # Don't split here

        # Check if it ends with a number followed by a period (decimal)
        if re.search(r"\d\.$", buffer):
            continue

        sentences.append(buffer)
        buffer = ""

    if buffer:
        sentences.append(buffer)

    return [s.strip() for s in sentences if s.strip()]


def split_paragraphs(text: str) -> list[str]:
    """Split text into paragraphs on double newlines."""
    paragraphs = re.split(r"\n\s*\n", text)
    return [p.strip() for p in paragraphs if p.strip()]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# WORD & TOKEN COUNTING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def count_words(text: str) -> int:
    """Count words in text (whitespace-delimited)."""
    return len(text.split())


def count_characters(text: str, include_spaces: bool = True) -> int:
    """Count characters in text."""
    if include_spaces:
        return len(text)
    return len(text.replace(" ", ""))


def get_words(text: str) -> list[str]:
    """Extract lowercased words from text (alphanumeric only)."""
    return re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SENTENCE STATISTICS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def sentence_lengths(text: str) -> list[int]:
    """Get word count for each sentence."""
    return [count_words(s) for s in split_sentences(text)]


def sentence_length_stats(text: str) -> dict[str, float]:
    """
    Compute sentence length statistics.
    
    Returns:
        avg: average sentence length (words)
        min: shortest sentence
        max: longest sentence
        std_dev: standard deviation (uniformity measure)
        variance_coefficient: std_dev / avg (normalized variability)
    """
    lengths = sentence_lengths(text)
    if not lengths:
        return {"avg": 0, "min": 0, "max": 0, "std_dev": 0, "variance_coefficient": 0, "count": 0}

    n = len(lengths)
    avg = sum(lengths) / n
    variance = sum((l - avg) ** 2 for l in lengths) / n if n > 1 else 0
    std_dev = variance ** 0.5

    return {
        "avg": round(avg, 2),
        "min": min(lengths),
        "max": max(lengths),
        "std_dev": round(std_dev, 2),
        "variance_coefficient": round(std_dev / avg, 3) if avg > 0 else 0,
        "count": n,
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LEXICAL ANALYSIS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def type_token_ratio(text: str) -> float:
    """
    Compute type-token ratio (TTR) — a lexical diversity measure.
    
    TTR = unique_words / total_words
    Higher = more diverse vocabulary.
    Range: 0.0 to 1.0
    
    Note: TTR is sensitive to text length (longer texts have lower TTR).
    For cross-document comparison, use MATTR (moving-average TTR) instead.
    """
    words = get_words(text)
    if not words:
        return 0.0
    return round(len(set(words)) / len(words), 4)


def moving_average_ttr(text: str, window_size: int = 50) -> float:
    """
    Compute Moving-Average Type-Token Ratio (MATTR).
    
    More stable than TTR for comparing texts of different lengths.
    Slides a window across the text and averages the TTR of each window.
    """
    words = get_words(text)
    if len(words) <= window_size:
        return type_token_ratio(text)

    ttrs: list[float] = []
    for i in range(len(words) - window_size + 1):
        window = words[i : i + window_size]
        ttrs.append(len(set(window)) / window_size)

    return round(sum(ttrs) / len(ttrs), 4) if ttrs else 0.0


def get_repeated_ngrams(text: str, n: int = 3, min_count: int = 2) -> list[dict[str, Any]]:
    """
    Find repeated n-grams (phrases) in text.
    
    Returns list of {ngram, count} for phrases appearing min_count+ times.
    Useful for detecting repetitive patterns.
    """
    words = get_words(text)
    if len(words) < n:
        return []

    ngrams = [" ".join(words[i : i + n]) for i in range(len(words) - n + 1)]
    counter = Counter(ngrams)

    return [
        {"ngram": ngram, "count": count}
        for ngram, count in counter.most_common()
        if count >= min_count
    ]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SENTENCE OPENER ANALYSIS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_sentence_openers(text: str, n_words: int = 1) -> list[str]:
    """Extract the first n_words of each sentence."""
    sentences = split_sentences(text)
    openers: list[str] = []
    for s in sentences:
        words = s.split()[:n_words]
        if words:
            openers.append(" ".join(words))
    return openers


def opener_repetition_rate(text: str) -> float:
    """
    Compute how repetitive sentence openings are.
    
    Rate = 1 - (unique_openers / total_sentences)
    0.0 = all unique openers (best)
    1.0 = all same opener (worst)
    """
    openers = get_sentence_openers(text)
    if len(openers) <= 1:
        return 0.0
    unique = len(set(o.lower() for o in openers))
    return round(1 - (unique / len(openers)), 4)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DISCOURSE MARKERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Common discourse markers that AI tends to overuse
DISCOURSE_MARKERS = {
    "additive": ["moreover", "furthermore", "additionally", "also", "in addition", "besides"],
    "contrastive": ["however", "nevertheless", "nonetheless", "on the other hand", "conversely", "although", "despite"],
    "causal": ["therefore", "consequently", "thus", "hence", "as a result", "accordingly"],
    "sequential": ["firstly", "secondly", "thirdly", "finally", "subsequently", "next"],
    "exemplifying": ["for example", "for instance", "specifically", "in particular", "such as"],
    "concluding": ["in conclusion", "to summarize", "in summary", "overall", "ultimately"],
    "emphasizing": ["importantly", "significantly", "notably", "it is important to note", "it is worth noting"],
}

# Flat list for quick lookup
ALL_DISCOURSE_MARKERS = [
    marker for markers in DISCOURSE_MARKERS.values() for marker in markers
]


def count_discourse_markers(text: str) -> dict[str, Any]:
    """
    Count discourse markers by category and compute density.
    
    Returns:
        total: total marker count
        per_sentence: markers per sentence (density)
        by_category: count per category
        overused: markers appearing 3+ times
    """
    text_lower = text.lower()
    sentences = split_sentences(text)
    n_sentences = max(len(sentences), 1)

    by_category: dict[str, int] = {}
    marker_counts: Counter[str] = Counter()

    for category, markers in DISCOURSE_MARKERS.items():
        cat_count = 0
        for marker in markers:
            count = len(re.findall(r"\b" + re.escape(marker) + r"\b", text_lower))
            if count > 0:
                marker_counts[marker] += count
                cat_count += count
        by_category[category] = cat_count

    total = sum(marker_counts.values())
    overused = [
        {"marker": m, "count": c} for m, c in marker_counts.most_common() if c >= 3
    ]

    return {
        "total": total,
        "per_sentence": round(total / n_sentences, 3),
        "by_category": by_category,
        "overused": overused,
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# VOICE ANALYSIS (ACTIVE/PASSIVE)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Simple heuristic patterns for passive voice detection
_PASSIVE_PATTERNS = [
    r"\b(?:is|are|was|were|been|being|be)\s+\w+ed\b",
    r"\b(?:is|are|was|were|been|being|be)\s+\w+en\b",
    r"\b(?:has|have|had)\s+been\s+\w+ed\b",
    r"\b(?:has|have|had)\s+been\s+\w+en\b",
]


def estimate_passive_voice_ratio(text: str) -> float:
    """
    Estimate the ratio of passive voice constructions.
    
    This is a heuristic (regex-based), not a full parse.
    For accurate results, use spaCy's dependency parser in Skill 06.
    
    Returns: float between 0.0 and 1.0
    """
    sentences = split_sentences(text)
    if not sentences:
        return 0.0

    passive_count = 0
    for sentence in sentences:
        for pattern in _PASSIVE_PATTERNS:
            if re.search(pattern, sentence, re.IGNORECASE):
                passive_count += 1
                break  # Count each sentence only once

    return round(passive_count / len(sentences), 4)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FORMALITY INDICATORS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FORMAL_INDICATORS = [
    "utilize", "utilization", "facilitate", "implementation",
    "in order to", "it is important to note", "it should be noted",
    "it is worth noting", "it can be observed", "it is evident",
    "subsequently", "henceforth", "aforementioned", "hereby",
    "notwithstanding", "with respect to", "in regard to",
    "pertaining to", "in the context of", "on the basis of",
]

INFORMAL_INDICATORS = [
    "gonna", "wanna", "gotta", "kinda", "sorta",
    "yeah", "yep", "nope", "ok", "okay",
    "stuff", "thing", "lots of", "a bunch of",
    "pretty much", "kind of", "sort of",
]


def count_contractions(text: str) -> int:
    """Count contractions in text (e.g., don't, won't, it's)."""
    return len(re.findall(r"\b\w+'\w+\b", text))


def contraction_rate(text: str) -> float:
    """Contractions per sentence."""
    sentences = split_sentences(text)
    if not sentences:
        return 0.0
    return round(count_contractions(text) / len(sentences), 4)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CITATION & ENTITY DETECTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def extract_urls(text: str) -> list[str]:
    """Extract URLs from text."""
    return re.findall(r"https?://[^\s<>\"']+", text)


def extract_emails(text: str) -> list[str]:
    """Extract email addresses from text."""
    return re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)


def extract_numbers(text: str) -> list[str]:
    """Extract numbers (integers, decimals, percentages) from text."""
    return re.findall(r"\b\d+(?:\.\d+)?%?\b", text)


def extract_citations_apa(text: str) -> list[str]:
    """Extract APA-style citations (Author, Year) or (Author et al., Year)."""
    return re.findall(r"\([A-Z][a-zA-Z]+(?:\s+(?:et\s+al\.?|&\s+[A-Z][a-zA-Z]+))?,\s*\d{4}\)", text)


def extract_citations_numeric(text: str) -> list[str]:
    """Extract numeric citations like [1], [2,3], [1-5]."""
    return re.findall(r"\[\d+(?:[,\-–]\s*\d+)*\]", text)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# COMPREHENSIVE TEXT STATISTICS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def compute_text_stats(text: str) -> dict[str, Any]:
    """
    Compute comprehensive text statistics in one call.
    
    Used by multiple skills to avoid redundant computation.
    Returns all stats needed for Skill 02, 06, and 08.
    """
    sentences = split_sentences(text)
    paragraphs = split_paragraphs(text)
    words = get_words(text)

    return {
        "character_count": len(text),
        "word_count": len(words),
        "sentence_count": len(sentences),
        "paragraph_count": len(paragraphs),
        "sentence_length_stats": sentence_length_stats(text),
        "type_token_ratio": type_token_ratio(text),
        "mattr": moving_average_ttr(text),
        "opener_repetition_rate": opener_repetition_rate(text),
        "discourse_markers": count_discourse_markers(text),
        "passive_voice_ratio": estimate_passive_voice_ratio(text),
        "contraction_rate": contraction_rate(text),
        "urls": extract_urls(text),
        "numbers": extract_numbers(text),
        "citations_apa": extract_citations_apa(text),
        "citations_numeric": extract_citations_numeric(text),
    }
