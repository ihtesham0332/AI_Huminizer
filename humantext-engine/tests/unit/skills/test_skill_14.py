import pytest
from app.skills.skill_14 import preserve_citations

def test_preserve_citations_empty():
    result = preserve_citations({}, "")
    assert result == []

def test_preserve_citations_basic():
    facts = {
        "citations": [{"value": "(Smith, 2023)"}],
        "urls": [{"value": "https://example.com"}]
    }
    text = "According to (Smith, 2023), the data is at https://example.com."
    
    result = preserve_citations(facts, text)
    assert len(result) == 2
    assert "(Smith, 2023)" in result
    assert "https://example.com" in result

def test_preserve_citations_not_in_text():
    facts = {
        "urls": [{"value": "https://other.com"}]
    }
    text = "The site is offline."
    
    result = preserve_citations(facts, text)
    assert result == []
