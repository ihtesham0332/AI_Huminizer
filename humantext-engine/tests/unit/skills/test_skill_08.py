import pytest
from app.skills.skill_08 import analyze_readability

def test_analyze_readability_empty():
    result = analyze_readability("")
    assert result["flesch_kincaid_grade"] == 0.0
    assert result["sentence_complexity"] == 0.0

def test_analyze_readability_basic():
    text = "This is a simple sentence. And here is another one!"
    result = analyze_readability(text)
    
    # 10 words, 2 sentences -> avg 5.0
    assert result["sentence_complexity"] == 5.0
    assert result["flesch_kincaid_grade"] == 2.5
    assert result["vocabulary_level"] > 0.0
