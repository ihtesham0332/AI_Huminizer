import pytest
from app.skills.skill_20 import generate_revision_instructions, RevisionPlan

def test_generate_revision_instructions_empty():
    result = generate_revision_instructions([], "Orig", "Trans")
    assert result["instructions"] == []

def test_generate_revision_instructions_no_llm():
    failures = [{"is_valid": False, "reasoning": "Missing claim1"}]
    result = generate_revision_instructions(failures, "Orig", "Trans")
    assert len(result["instructions"]) == 1
    assert "Missing claim1" in result["instructions"][0]

def test_generate_revision_instructions_with_mock_llm():
    class MockLLM:
        def invoke(self, inputs):
            return RevisionPlan(instructions=["Ensure claim1 is added back."])
            
    failures = [{"is_valid": False, "reasoning": "Missing claim1"}]
    result = generate_revision_instructions(failures, "Orig", "Trans", llm_client=MockLLM())
    assert result["instructions"][0] == "Ensure claim1 is added back."
