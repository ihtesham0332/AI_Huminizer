import pytest
from app.skills.skill_09 import generate_plan, TransformationPlan, Operation

def test_generate_plan_empty():
    result = generate_plan({})
    assert result["operations"] == []
    assert result["global_constraints"] == []

def test_generate_plan_no_llm():
    analysis = {"style": {"formality_score": 0.9}}
    result = generate_plan(analysis)
    
    assert len(result["operations"]) == 1
    assert result["operations"][0]["action"] == "rewrite_paragraph"
    assert "Preserve facts" in result["global_constraints"]

def test_generate_plan_with_mock_llm():
    class MockLLM:
        def invoke(self, inputs):
            return TransformationPlan(
                operations=[Operation(action="split_sentence", target="global", instruction="Split long sentences")],
                global_constraints=["No slang"]
            )
            
    result = generate_plan({"test": "data"}, llm_client=MockLLM())
    assert len(result["operations"]) == 1
    assert result["operations"][0]["action"] == "split_sentence"
    assert "No slang" in result["global_constraints"]
