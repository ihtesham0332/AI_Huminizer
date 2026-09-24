from typing import Dict, Any, Optional

class ModelRouter:
    """
    Dynamically selects the most cost-efficient AI model capable of achieving the required quality.
    Adheres to Master Prompt Section 31 (Model Router) and Section 30 (Cost Controller).
    """
    
    # Pre-defined model tiers (In production, load these from config)
    MODELS = {
        "cheap": "ollama/qwen2.5:3b",      # Local, free (Use for Language Detection, Basic Grammar)
        "medium": "ollama/llama3:8b",      # Local, slightly slower (Use for Simple Rewrite, Classification)
        "strong": "anthropic/claude-3-5-sonnet-20240620" # Expensive API (Use for Complex Academic Rewrite, Semantic Conflicts)
    }
    
    def __init__(self, user_plan: str = "FREE"):
        self.user_plan = user_plan
    
    def route(self, task_type: str, complexity_score: float) -> str:
        """
        Routes the task to the appropriate model based on task type, complexity, and user plan.
        """
        # Tasks that should ALWAYS use the cheap model to save costs
        if task_type in ["language_detection", "content_classification", "basic_grammar"]:
            return self.MODELS["cheap"]
            
        # Tasks requiring deep intelligence
        if task_type in ["academic_rewrite", "semantic_verification", "ghost_mode"]:
            if self.user_plan in ["PRO", "PRO_PLUS", "ENTERPRISE"]:
                return self.MODELS["strong"]
            else:
                # Free/Student users fallback to medium local model to prevent API bankrupting the company
                return self.MODELS["medium"]
                
        # Default routing logic based on complexity
        if complexity_score > 0.8 and self.user_plan != "FREE":
            return self.MODELS["strong"]
        elif complexity_score > 0.4:
            return self.MODELS["medium"]
        else:
            return self.MODELS["cheap"]
            
    def estimate_cost(self, model_id: str, estimated_tokens: int) -> float:
        """
        Estimates the internal credit cost for a job.
        """
        if "ollama" in model_id:
            return estimated_tokens * 0.0001 # Extremely cheap internal credit cost
        elif "claude" in model_id:
            return estimated_tokens * 0.005 # Expensive API cost
        return estimated_tokens * 0.001
