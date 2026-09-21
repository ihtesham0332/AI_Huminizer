import pytest
from app.skills.skill_07 import analyze_context, ContextProfile

def test_analyze_context_empty():
    result = analyze_context("")
    assert result["document_type"] == "unknown"
    assert result["audience"] == "general"

def test_analyze_context_no_llm():
    result = analyze_context("Dear John,\n\nHow are you?")
    assert result["document_type"] == "email"

def test_analyze_context_with_mock_llm():
    class MockLLM:
        def invoke(self, inputs):
            return ContextProfile(
                document_type="report",
                audience="experts",
                purpose="persuade",
                register="technical"
            )
            
    result = analyze_context("The latency metrics show...", llm_client=MockLLM())
    assert result["document_type"] == "report"
    assert result["audience"] == "experts"
    assert result["purpose"] == "persuade"
    assert result["register"] == "technical"
