import pytest
from app.skills.skill_06 import analyze_style, StyleProfile

def test_analyze_style_empty():
    result = analyze_style("")
    assert result["formality_score"] == 0.5
    assert result["tone"] == []

def test_analyze_style_no_llm():
    text_formal = "Therefore, we conclude the test."
    result_formal = analyze_style(text_formal)
    assert result_formal["formality_score"] == 0.8
    assert "academic" in result_formal["tone"]
    
    text_casual = "Hey, let's wrap this up."
    result_casual = analyze_style(text_casual)
    assert result_casual["formality_score"] == 0.4
    assert "conversational" in result_casual["tone"]

def test_analyze_style_with_mock_llm():
    class MockLLM:
        def invoke(self, inputs):
            return StyleProfile(
                formality_score=0.9,
                tone=["formal", "objective"],
                voice="passive",
                lexical_patterns=["nominalization"]
            )
            
    result = analyze_style("It was determined that...", llm_client=MockLLM())
    assert result["formality_score"] == 0.9
    assert result["voice"] == "passive"
    assert "objective" in result["tone"]
