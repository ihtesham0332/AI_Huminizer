import pytest
from app.skills.skill_12 import optimize_discourse

def test_optimize_discourse_empty():
    result = optimize_discourse({}, "")
    assert result == ""

def test_optimize_discourse_no_plan():
    text = "Full document text."
    result = optimize_discourse({}, text)
    assert result == text

def test_optimize_discourse_no_llm():
    text = "Full document text."
    result = optimize_discourse({"operations": []}, text)
    assert result == "Full document text.\n\n(Discourse optimized)"

def test_optimize_discourse_with_mock_llm():
    class MockLLM:
        def invoke(self, inputs):
            return "Fully optimized text."
            
    result = optimize_discourse({"operations": []}, "Original text.", llm_client=MockLLM())
    assert result == "Fully optimized text."
