import pytest
from app.agents.input_analyzer import analyze_input_text

def test_analyze_input_text_academic():
    academic_text = "Recent studies in convolutional neural networks (Smith et al., 2023) suggest that gradient descent optimization can lead to local minima."
    
    result = analyze_input_text(academic_text)
    
    assert result.word_count > 10
    assert result.language.lower() == "english"
    # Qwen should easily detect this as Academic/Technical and flag citations
    assert "academic" in result.content_type.lower() or "technical" in result.content_type.lower()
    assert result.has_citations is True
    assert result.has_technical_terms is True

def test_analyze_input_text_casual():
    casual_text = "Hey man! I just got back from the store and forgot to buy milk lol. Be there in 5 mins."
    
    result = analyze_input_text(casual_text)
    
    assert result.word_count > 10
    assert result.language.lower() == "english"
    assert "casual" in result.content_type.lower() or "email" in result.content_type.lower() or "general" in result.content_type.lower()
    assert result.has_citations is False
    assert result.has_technical_terms is False
