import pytest
from app.skills.skill_17 import validate_tone_consistency
from app.skills.skill_15 import ValidationResult

def test_validate_tone_consistency_empty_text():
    result = validate_tone_consistency(["casual"], "")
    assert result["is_valid"] is False

def test_validate_tone_consistency_no_tone():
    result = validate_tone_consistency([], "Some text.")
    assert result["is_valid"] is True

def test_validate_tone_consistency_no_llm():
    result = validate_tone_consistency(["formal"], "Formal text.")
    assert result["is_valid"] is True

def test_validate_tone_consistency_with_mock_llm():
    class MockLLM:
        def invoke(self, inputs):
            return ValidationResult(is_valid=False, reasoning="Too casual")
            
    result = validate_tone_consistency(["formal"], "Hey there!", llm_client=MockLLM())
    assert result["is_valid"] is False
    assert result["reasoning"] == "Too casual"
