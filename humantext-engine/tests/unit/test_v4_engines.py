import pytest
from app.engine.document_intelligence import DocumentIntelligenceEngine
from app.engine.quality_critic import QualityCriticEngine
from app.engine.enhanced_guardians import EnhancedFactGuardian

def test_document_intelligence_plain_text():
    engine = DocumentIntelligenceEngine()
    result = engine.parse_plain_text("Hello world.\nThis is a test.")
    
    assert result["type"] == "txt"
    assert result["metrics"]["total_words"] == 6
    assert len(result["paragraphs"]) == 2

def test_fact_guardian():
    guardian = EnhancedFactGuardian()
    
    original_text = "The revenue grew by 25% in 2026 reaching $5000."
    generated_text = "Revenue increased by 25% this year, hitting $5000."
    generated_missing_fact = "Revenue increased greatly this year."
    
    # Facts should be preserved
    res_pass = guardian.verify_facts(original_text, generated_text)
    assert res_pass["facts_preserved"] is False # It lost 2026!
    assert "2026" in res_pass["altered_facts"]
    
    # Facts completely missing
    res_fail = guardian.verify_facts(original_text, generated_missing_fact)
    assert res_fail["facts_preserved"] is False
    assert "25%" in res_fail["altered_facts"]

def test_quality_critic_eval():
    critic = QualityCriticEngine()
    
    # Simulating a fact report where facts were dropped
    fact_report = {"facts_preserved": False, "altered_facts": ["2026"]}
    citation_report = {"citations_preserved": True}
    
    result = critic.evaluate_candidate(
        original_text="In 2026, the company grew.",
        candidate_text="The company grew.",
        fact_report=fact_report,
        citation_report=citation_report
    )
    
    # The critic MUST block the output and require a revision
    assert result["semantic"] == "FAIL"
    assert result["facts"] == "FAIL"
    assert result["revision_required"] is True
