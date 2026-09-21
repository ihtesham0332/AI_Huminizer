import pytest
from app.skills.skill_16 import validate_fact_preservation

def test_validate_fact_preservation_empty():
    result = validate_fact_preservation({}, "")
    assert result["is_valid"] is True

def test_validate_fact_preservation_empty_text_with_facts():
    facts = {"entities": [{"value": "Apple"}]}
    result = validate_fact_preservation(facts, "")
    assert result["is_valid"] is False
    assert len(result["missing_facts"]) == 1

def test_validate_fact_preservation_all_present():
    facts = {
        "entities": [{"value": "Google"}],
        "numbers": [{"value": "100"}]
    }
    text = "Google employs over 100 people."
    result = validate_fact_preservation(facts, text)
    assert result["is_valid"] is True
    assert result["missing_facts"] == []

def test_validate_fact_preservation_missing():
    facts = {
        "entities": [{"value": "Microsoft"}],
        "numbers": [{"value": "500"}]
    }
    text = "Microsoft is a large company."
    result = validate_fact_preservation(facts, text)
    assert result["is_valid"] is False
    assert result["missing_facts"] == ["500"]
