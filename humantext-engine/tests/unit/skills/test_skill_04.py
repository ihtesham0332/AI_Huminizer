import pytest
from app.skills.skill_04 import extract_claims, Claim

def test_extract_claims_empty():
    result = extract_claims("")
    assert result == []

def test_extract_claims_no_llm():
    text = "The study suggests that AI may improve productivity in some workplaces."
    result = extract_claims(text)
    
    assert len(result) == 1
    claim = result[0]
    assert claim["id"] == "c1"
    assert claim["modality"] == "may"
    assert claim["scope"] == "some"
    assert claim["evidence_level"] == "suggests"

def test_extract_claims_with_mock_llm():
    class MockResponse:
        def __init__(self, claims):
            self.claims = claims
            
    class MockLLM:
        def invoke(self, inputs):
            return MockResponse([
                Claim(
                    id="c1",
                    text="AI improves productivity",
                    evidence_level="proves",
                    modality="will",
                    scope="all",
                    hedging=None
                )
            ])
            
    result = extract_claims("AI will prove to improve productivity in all workplaces.", llm_client=MockLLM())
    
    assert len(result) == 1
    claim = result[0]
    assert claim["text"] == "AI improves productivity"
    assert claim["modality"] == "will"
    assert claim["evidence_level"] == "proves"
    assert claim["scope"] == "all"
    assert claim["hedging"] is None
