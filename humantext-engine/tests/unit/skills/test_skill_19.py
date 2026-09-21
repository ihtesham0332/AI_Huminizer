import pytest
from app.skills.skill_19 import calculate_humanization, HumanizationScore

def test_calculate_humanization_empty():
    result = calculate_humanization("")
    assert result["naturalness_score"] == 0.0

def test_calculate_humanization_no_llm():
    result = calculate_humanization("Some text.")
    assert result["naturalness_score"] == 0.85
    assert result["evasion_estimate"] == 0.9

def test_calculate_humanization_with_mock_llm():
    class MockLLM:
        def invoke(self, inputs):
            return HumanizationScore(naturalness_score=0.95, evasion_estimate=0.98)
            
    result = calculate_humanization("Perfect text.", llm_client=MockLLM())
    assert result["naturalness_score"] == 0.95
    assert result["evasion_estimate"] == 0.98
