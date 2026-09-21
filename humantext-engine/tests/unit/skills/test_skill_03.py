import pytest
from app.skills.skill_03 import analyze_semantics, SemanticGraph, Proposition

def test_analyze_semantics_empty():
    result = analyze_semantics("")
    assert result["propositions"] == []
    assert result["meaning_graph"]["propositions"] == []
    assert result["meaning_graph"]["entailments"] == []

def test_analyze_semantics_no_llm():
    text = "This is a valid sentence."
    result = analyze_semantics(text)
    assert len(result["propositions"]) == 1
    assert result["propositions"][0]["id"] == "p1"
    assert "Mock proposition" in result["propositions"][0]["text"]

def test_analyze_semantics_with_mock_llm():
    class MockLLM:
        def invoke(self, inputs):
            return SemanticGraph(
                propositions=[Proposition(id="p1", text="The sky is blue")],
                entailments=[{"source": "p1", "target": "p2"}]
            )
            
    result = analyze_semantics("The sky is blue.", llm_client=MockLLM())
    
    assert len(result["propositions"]) == 1
    assert result["propositions"][0]["text"] == "The sky is blue"
    assert len(result["meaning_graph"]["entailments"]) == 1
