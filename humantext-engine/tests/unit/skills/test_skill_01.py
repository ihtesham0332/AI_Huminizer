import pytest
from app.skills.skill_01 import validate_input
from app.utils.errors import InputValidationError
from app.config.settings import get_settings

def test_validate_input_valid():
    raw_text = "  This is a   valid input text.  "
    result, cleaned = validate_input(raw_text)
    
    assert result["is_valid"] is True
    assert cleaned == "This is a valid input text."
    assert result["original_length"] == len(raw_text)
    assert result["cleaned_length"] == len(cleaned)

def test_validate_input_empty():
    with pytest.raises(InputValidationError) as exc_info:
        validate_input("   \n \t  ")
    assert "empty or contains only whitespace" in str(exc_info.value)

def test_validate_input_too_long(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "MAX_INPUT_LENGTH", 10)
    
    with pytest.raises(InputValidationError) as exc_info:
        validate_input("This is way too long")
    assert "exceeds maximum length" in str(exc_info.value)

def test_validate_input_not_string():
    with pytest.raises(InputValidationError) as exc_info:
        validate_input(123)
    assert "must be a string" in str(exc_info.value)
