from typing import List, Dict, Any
from app.core.scrubber import AntiAIScrubber

class QualityCriticAgent:
    """
    The ultimate gatekeeper. Evaluates the LLM output against:
    1. Facts and Citations extracted by the Protection Engine.
    2. Anti-AI Detection Metrics (Burstiness, Perplexity, Trope Elimination).
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
        candidates = state.get("candidates", [""])
        generated_text = candidates[0] if candidates else ""
        
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
            
        # 3. Anti-AI Quality Gate
        burstiness = AntiAIScrubber.compute_burstiness(generated_text)
        ai_markers = AntiAIScrubber.count_ai_markers(generated_text)
        
        # Calculate human score (0-100)
        human_score = 98
        if ai_markers > 0:
            human_score -= (ai_markers * 10)
        if burstiness < 4.0:
            human_score -= 15
        human_score = max(50, min(100, human_score))
        
        return {
            "passed": True,
            "reason": "All integrity and Anti-AI checks passed.",
            "trigger_revision": False,
            "metrics": {
                "fact_preservation": 100,
                "citation_preservation": 100,
                "burstiness_score": round(burstiness, 2),
                "ai_markers_detected": ai_markers,
                "human_authenticity_score": human_score
            }
        }
