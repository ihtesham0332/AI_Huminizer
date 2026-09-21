"""
Tests for app.utils.text — Text utilities.
"""

from __future__ import annotations

import pytest

from app.utils.text import (
    clean_text,
    compute_text_stats,
    contraction_rate,
    count_discourse_markers,
    count_words,
    estimate_passive_voice_ratio,
    extract_citations_apa,
    extract_citations_numeric,
    extract_numbers,
    extract_urls,
    get_repeated_ngrams,
    get_sentence_openers,
    moving_average_ttr,
    opener_repetition_rate,
    sentence_length_stats,
    split_paragraphs,
    split_sentences,
    type_token_ratio,
)


class TestCleanText:
    def test_normalize_unicode(self):
        result = clean_text("café")
        assert "café" in result or "cafe" in result  # NFC normalized

    def test_collapse_whitespace(self):
        assert clean_text("hello    world") == "hello world"

    def test_preserve_paragraphs(self):
        result = clean_text("paragraph 1\n\nparagraph 2")
        assert "\n\n" in result

    def test_collapse_excessive_newlines(self):
        result = clean_text("a\n\n\n\n\nb")
        assert result == "a\n\nb"

    def test_strip_edges(self):
        assert clean_text("  hello  ") == "hello"

    def test_empty_string(self):
        assert clean_text("") == ""


class TestSplitSentences:
    def test_simple_sentences(self):
        text = "First sentence. Second sentence. Third sentence."
        result = split_sentences(text)
        assert len(result) >= 2

    def test_question_marks(self):
        text = "What is AI? It is a field of computer science."
        result = split_sentences(text)
        assert len(result) == 2

    def test_empty_text(self):
        assert split_sentences("") == []

    def test_single_sentence(self):
        result = split_sentences("Just one sentence here.")
        assert len(result) == 1


class TestSplitParagraphs:
    def test_two_paragraphs(self):
        text = "First paragraph.\n\nSecond paragraph."
        result = split_paragraphs(text)
        assert len(result) == 2

    def test_empty(self):
        assert split_paragraphs("") == []


class TestWordCounting:
    def test_count_words(self):
        assert count_words("hello world foo") == 3

    def test_count_words_empty(self):
        assert count_words("") == 0


class TestSentenceStats:
    def test_basic_stats(self):
        text = "Short. A much longer sentence with more words. Medium sized one."
        stats = sentence_length_stats(text)
        assert stats["count"] >= 2
        assert stats["avg"] > 0
        assert stats["std_dev"] >= 0

    def test_empty_text_stats(self):
        stats = sentence_length_stats("")
        assert stats["count"] == 0
        assert stats["avg"] == 0


class TestLexicalAnalysis:
    def test_ttr_diverse(self):
        text = "The quick brown fox jumps over the lazy dog"
        ttr = type_token_ratio(text)
        assert 0.0 < ttr <= 1.0

    def test_ttr_repetitive(self):
        text = "the the the the the"
        ttr = type_token_ratio(text)
        assert ttr < 0.5  # Low diversity

    def test_ttr_empty(self):
        assert type_token_ratio("") == 0.0

    def test_mattr(self):
        text = " ".join([f"word{i}" for i in range(100)])
        mattr = moving_average_ttr(text)
        assert 0.0 < mattr <= 1.0

    def test_repeated_ngrams(self):
        text = "the cat sat on the mat and the cat sat on the floor"
        ngrams = get_repeated_ngrams(text, n=3, min_count=2)
        assert len(ngrams) > 0


class TestSentenceOpeners:
    def test_openers(self):
        text = "The first. The second. Another one. The fourth."
        openers = get_sentence_openers(text)
        assert len(openers) >= 3

    def test_repetition_rate_high(self):
        text = "The cat. The dog. The bird. The fish."
        rate = opener_repetition_rate(text)
        assert rate > 0.5  # Very repetitive

    def test_repetition_rate_low(self):
        text = "Cats are nice. Dogs love walks. Birds can fly. Fish swim deep."
        rate = opener_repetition_rate(text)
        assert rate < 0.5  # Varied openers


class TestDiscourseMarkers:
    def test_detect_markers(self):
        text = "Moreover, AI is growing. Furthermore, it impacts jobs. However, concerns exist."
        result = count_discourse_markers(text)
        assert result["total"] >= 3

    def test_categories(self):
        text = "Therefore, we proceed. However, risks exist."
        result = count_discourse_markers(text)
        assert result["by_category"]["causal"] >= 1
        assert result["by_category"]["contrastive"] >= 1


class TestPassiveVoice:
    def test_passive_detected(self):
        text = "The experiment was conducted. Results were analyzed. Data was collected."
        ratio = estimate_passive_voice_ratio(text)
        assert ratio > 0.5

    def test_active_voice(self):
        text = "We conducted the experiment. We analyzed results. We collected data."
        ratio = estimate_passive_voice_ratio(text)
        assert ratio < 0.5


class TestCitations:
    def test_apa_citations(self):
        text = "According to Smith (2023) and (Johnson et al., 2024), AI is growing."
        citations = extract_citations_apa(text)
        assert len(citations) >= 1

    def test_numeric_citations(self):
        text = "Studies show promising results [1], [2,3], and [4-7]."
        citations = extract_citations_numeric(text)
        assert len(citations) >= 2


class TestNumbers:
    def test_extract_numbers(self):
        text = "The model achieved 95.7% accuracy with 128 parameters in 2024."
        numbers = extract_numbers(text)
        assert "95.7%" in numbers or "95.7" in numbers
        assert "128" in numbers
        assert "2024" in numbers


class TestUrls:
    def test_extract_urls(self):
        text = "Visit https://openai.com and http://example.com/path for more."
        urls = extract_urls(text)
        assert len(urls) == 2


class TestContractions:
    def test_contraction_rate(self):
        text = "I don't think it's possible. We can't do that."
        rate = contraction_rate(text)
        assert rate > 0

    def test_no_contractions(self):
        text = "I do not think it is possible. We cannot do that."
        rate = contraction_rate(text)
        assert rate == 0.0


class TestComputeTextStats:
    def test_comprehensive_stats(self, sample_robotic_text):
        stats = compute_text_stats(sample_robotic_text)
        assert stats["word_count"] > 0
        assert stats["sentence_count"] > 0
        assert stats["paragraph_count"] >= 1
        assert "sentence_length_stats" in stats
        assert "type_token_ratio" in stats
        assert "discourse_markers" in stats
        assert "passive_voice_ratio" in stats

    def test_empty_text_stats(self):
        stats = compute_text_stats("")
        assert stats["word_count"] == 0
        assert stats["sentence_count"] == 0
