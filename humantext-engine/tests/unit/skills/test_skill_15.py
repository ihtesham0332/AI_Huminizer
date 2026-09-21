import pytest
from app.skills.skill_15 import validate_source_integrity, ValidationResult

def test_validate_source_integrity_empty_text():
    result = validate_source_integrity({"claims": []}, "")
    assert result["is_valid"] is False
    assert "empty" in result["reasoning"].lower()

def test_validate_source_integrity_no_semantics():
    result = validate_source_integrity({}, "Valid text.")
    assert result["is_valid"] is True

def test_validate_source_integrity_no_llm():
    result = validate_source_integrity({"claims": ["claim1"]}, "Valid text.")
    assert result["is_valid"] is True

def test_validate_source_integrity_with_mock_llm():
    class MockLLM:
        def invoke(self, inputs):
            return ValidationResult(is_valid=False, reasoning="Missing claim1", failed_items=["claim1"])
            
    result = validate_source_integrity({"claims": ["claim1"]}, "Text without claim.", llm_client=MockLLM())
    assert result["is_valid"] is False
    assert "claim1" in result["failed_items"]
