import pytest
from app.skills.skill_05 import extract_facts, Fact

def test_extract_facts_empty():
    result = extract_facts("")
    assert result["numbers"] == []
    assert result["dates"] == []
    assert result["entities"] == []

def test_extract_facts_no_llm():
    text = "In 2026, AI reached 42 percent adoption."
    result = extract_facts(text)
    
    assert len(result["dates"]) == 1
    assert result["dates"][0]["value"] == "2026"
    
    assert len(result["entities"]) == 1
    assert result["entities"][0]["value"] == "AI"
    
    assert len(result["numbers"]) == 1
    assert result["numbers"][0]["value"] == "42"

def test_extract_facts_with_mock_llm():
    class MockLLM:
        def invoke(self, inputs):
            return {
                "numbers": [{"id": "f1", "type": "number", "value": "100", "context": None}],
                "dates": [],
                "names": [{"id": "f2", "type": "name", "value": "Alice", "context": None}],
                "entities": [],
                "citations": [],
                "urls": []
            }
            
    result = extract_facts("Alice has 100 apples.", llm_client=MockLLM())
    
    assert len(result["numbers"]) == 1
    assert result["numbers"][0]["value"] == "100"
    
    assert len(result["names"]) == 1
    assert result["names"][0]["value"] == "Alice"
