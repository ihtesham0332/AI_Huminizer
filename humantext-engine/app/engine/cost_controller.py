from typing import Dict, Any

class CostControllerAgent:
    """
    Dynamically optimizes and calculates internal credit costs for a job.
    Adheres to Master Prompt Section 30 and 45.
    """
    
    # Internal credit rates per 1,000 words
    RATES = {
        "basic_rewrite": 1.0,
        "deep_rewrite": 2.0,
        "multi_candidate": 3.0,
        "grammar_only": 0.1,
        "advanced_verification": 1.0
    }
    
    def __init__(self, user_plan: str):
        self.user_plan = user_plan
        
    def calculate_estimated_credits(self, words_to_process: int, mode: str, candidates: int, deep_verification: bool) -> float:
        """
        Calculates the internal credits required to process the given text.
        """
        base_rate = self.RATES["deep_rewrite"] if mode in ["aggressive", "ghost"] else self.RATES["basic_rewrite"]
        
        multiplier = 1.0
        if candidates > 1:
            multiplier += (candidates - 1) * 0.5 # 50% extra cost per additional candidate
            
        if deep_verification:
            base_rate += self.RATES["advanced_verification"]
            
        # Cost is calculated per 1000 words
        total_credits = (words_to_process / 1000) * base_rate * multiplier
        
        return round(max(0.1, total_credits), 2)
        
    def generate_cost_plan(self, document_words: int, words_to_process: int, mode: str) -> Dict[str, Any]:
        """
        Generates the cost parameters for the ModelRouter and the User UI.
        """
        # Determine features based on plan
        if self.user_plan in ["PRO", "PRO_PLUS", "ENTERPRISE"]:
            candidates = 3
            max_revision_loops = 3
            deep_verification = True
        else:
            candidates = 2
            max_revision_loops = 1
            deep_verification = False
            
        estimated_credits = self.calculate_estimated_credits(words_to_process, mode, candidates, deep_verification)
        
        return {
            "estimated_credits": estimated_credits,
            "candidate_count": candidates,
            "max_revision_loops": max_revision_loops,
            "deep_verification": deep_verification,
            "original_word_count": document_words,
            "optimized_word_count": words_to_process
        }
