from typing import Dict, Any

class CostControllerAgent:
    """
    Implements Selective Rewriting logic to optimize API costs.
    Scores sentences; if they don't need rewriting, they bypass the LLM.
    """
    
    def __init__(self):
        pass
        
    def determine_budget(self, text: str, user_tier: str, mode: str) -> Dict[str, Any]:
        """
        Determines how much compute to spend on this request.
        """
        word_count = len(text.split())
        
        # Base budget config
        budget = {
            "skip_llm": False,
            "candidates": 1,
            "max_revisions": 1,
            "model_tier": "tier1" # Fast model by default
        }
        
        # 1. Selective Rewriting (Cost Optimization)
        # If the text is super short or just a factual list, don't waste Deep models on it
        if word_count < 5:
            budget["skip_llm"] = True
            return budget
            
        # 2. Adjust based on User Tier & Mode
        if user_tier == "pro" or user_tier == "enterprise":
            if mode == "balanced":
                budget["candidates"] = 2
                budget["max_revisions"] = 2
                budget["model_tier"] = "tier2"
            elif mode == "deep":
                budget["candidates"] = 3
                budget["max_revisions"] = 3
                budget["model_tier"] = "tier3" # Requires Reasoning models (e.g., Gemini 3.1 Pro)
                
        # If Free tier, they always get tier1 regardless of mode request
        if user_tier == "free":
            budget["model_tier"] = "tier1"
            budget["max_revisions"] = 1
            
        return budget
