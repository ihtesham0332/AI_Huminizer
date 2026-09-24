from typing import List, Dict, Any

class QualityCriticAgent:
    """
    The ultimate gatekeeper. Evaluates the LLM output against the 
    Facts and Citations extracted by the Protection Engine.
    """
    
    def __init__(self, fact_guardian, citation_guardian):
        self.fact_guardian = fact_guardian
        self.citation_guardian = citation_guardian
        
    def evaluate(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates the generated text and decides if it passes the Quality Gate.
        """
        original_facts = state.get("facts", [])
        original_citations = state.get("citations", [])
        generated_text = state.get("candidates", [""])[0] # Just evaluating the top candidate for now
        
        # 1. Verify Facts
        fact_result = self.fact_guardian.verify(original_facts, generated_text)
        if fact_result["status"] == "FAIL":
            return {
                "passed": False,
                "reason": fact_result["message"],
                "trigger_revision": True
            }
            
        # 2. Verify Citations
        cite_result = self.citation_guardian.verify(original_citations, generated_text)
        if cite_result["status"] == "FAIL":
            return {
                "passed": False,
                "reason": cite_result["message"],
                "trigger_revision": True
            }
            
        # 3. Semantic Verification (Placeholder for actual LLM cross-check)
        # In a full implementation, we ask a Tier 1 model: "Does Candidate A mean exactly the same as Original Text?"
        
        return {
            "passed": True,
            "reason": "All integrity checks passed.",
            "trigger_revision": False,
            "metrics": {
                "fact_preservation": 100,
                "citation_preservation": 100
            }
        }
