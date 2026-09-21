import pytest
from app.skills.skill_13 import preserve_terminology

def test_preserve_terminology_empty():
    result = preserve_terminology({}, "")
    assert result == []

def test_preserve_terminology_basic():
    facts = {
        "entities": [{"value": "REST API"}],
        "names": [{"value": "JSON"}]
    }
    text = "The REST API returns data in JSON format."
    
    result = preserve_terminology(facts, text)
    assert len(result) == 2
    assert "REST API" in result
    assert "JSON" in result

def test_preserve_terminology_not_in_text():
    facts = {
        "entities": [{"value": "GraphQL"}]
    }
    text = "The REST API returns data in JSON format."
    
    result = preserve_terminology(facts, text)
    assert result == []
