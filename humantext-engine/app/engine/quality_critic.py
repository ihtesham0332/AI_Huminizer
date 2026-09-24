from typing import Dict, Any, List

class QualityCriticEngine:
    """
    Independent agent that evaluates candidates against strict quality requirements.
    Adheres to Master Prompt Sections 22 (Quality Critic) and 23 (Quality Gate).
    """
    
    def evaluate_candidate(self, original_text: str, candidate_text: str, fact_report: Dict, citation_report: Dict) -> Dict[str, Any]:
        """
        Evaluates a candidate and scores it across multiple dimensions.
        """
        # In production, this would involve LLM calls or NLP models to assess semantic meaning.
        # For now, we simulate the evaluation based on the guardian reports.
        
        semantic_pass = True
        grammar_pass = True
        style_match = 0.95
        
        issues = []
        
        if not fact_report.get("facts_preserved", True):
            semantic_pass = False
            issues.append(f"Fact missing or altered: {fact_report.get('altered_facts', [])}")
            
        if not citation_report.get("citations_preserved", True):
            semantic_pass = False
            issues.append(f"Citation missing or altered: {citation_report.get('altered_citations', [])}")
            
        return {
            "semantic": "PASS" if semantic_pass else "FAIL",
            "facts": "PASS" if fact_report.get("facts_preserved", True) else "FAIL",
            "citations": "PASS" if citation_report.get("citations_preserved", True) else "FAIL",
            "grammar": "PASS" if grammar_pass else "FAIL",
            "style_match": style_match,
            "issues": issues,
            "revision_required": len(issues) > 0
        }

class QualityGate:
    """
    Hard validation rules that block outputs from reaching the user.
    Adheres to Master Prompt Sections 23 & 24.
    """
    
    def __init__(self, critic: QualityCriticEngine):
        self.critic = critic
        
    def execute_gate(self, original_sentences: List[str], generated_sentences: List[str], fact_reports: List[Dict], citation_reports: List[Dict]) -> Dict[str, Any]:
        """
        Validates each sentence independently and triggers targeted revisions.
        """
        final_sentences = []
        targeted_revisions = []
        
        for i in range(len(original_sentences)):
            orig = original_sentences[i]
            gen = generated_sentences[i] if i < len(generated_sentences) else orig
            
            f_rep = fact_reports[i] if i < len(fact_reports) else {}
            c_rep = citation_reports[i] if i < len(citation_reports) else {}
            
            eval_result = self.critic.evaluate_candidate(orig, gen, f_rep, c_rep)
            
            if eval_result["revision_required"]:
                # If a sentence fails the gate, we record it for Targeted Revision
                targeted_revisions.append({
                    "sentence_index": i,
                    "original": orig,
                    "failed_generation": gen,
                    "reason": eval_result["issues"]
                })
                # Revert to original text for safety until the revision loop finishes
                final_sentences.append(orig) 
            else:
                final_sentences.append(gen)
                
        return {
            "status": "PASS" if len(targeted_revisions) == 0 else "REVISION_REQUIRED",
            "safe_text": " ".join(final_sentences),
            "targeted_revisions": targeted_revisions
        }
