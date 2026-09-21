from typing import Dict, Any

def optimize_discourse(plan: Dict[str, Any], text: str, llm_client: Any = None) -> str:
    """
    Skill 12: Discourse Optimization
    Optimizes discourse markers, coherence, and argument flow using an LLM.
    
    Args:
        plan: The generated TransformationPlan dictionary.
        text: The full text.
        llm_client: Optional LLM client to perform the transformations.
        
    Returns:
        The optimized text.
    """
    if not text:
        return ""
        
    if not plan:
        return text
        
    if llm_client is None:
        # Mock logic
        return text + "\n\n(Discourse optimized)"
        
    try:
        response = llm_client.invoke({"plan": plan, "text": text})
        if isinstance(response, str):
            return response
        elif hasattr(response, "text"):
            return response.text
        elif isinstance(response, dict) and "text" in response:
            return response["text"]
    except Exception:
        pass
        
    return text
