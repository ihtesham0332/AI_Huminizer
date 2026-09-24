from app.agents.evaluators.semantic_checker import evaluate_semantics

def evaluate_candidate_quality(original: str, candidate: str, protected_tokens: list) -> dict:
    """
    The ultimate judge. Evaluates a single candidate across semantic and factual constraints.
    Returns a dict with pass/fail and reasons.
    """
    # 1. Fact & Citation Check (Deterministic)
    missing_tokens = []
    for token in protected_tokens:
        if token not in candidate:
            missing_tokens.append(token)
            
    fact_pass = len(missing_tokens) == 0
    fact_reason = f"Missing protected tokens: {missing_tokens}" if not fact_pass else "All protected tokens preserved."
    
    # 2. Semantic Check (LLM-based)
    semantic_result = evaluate_semantics(original, candidate)
    
    # 3. Final Aggregation
    is_pass = fact_pass and semantic_result.get("pass", False)
    
    return {
        "pass": is_pass,
        "fact_check": {"pass": fact_pass, "reason": fact_reason},
        "semantic_check": semantic_result
    }

def quality_critic_node(state: dict) -> dict:
    """
    LangGraph node: Evaluates all candidates.
    If at least one passes, selects the best one.
    Otherwise, provides feedback for a rewrite.
    """
    original = state.get("original_text", "")
    candidates = state.get("candidates", [])
    protected = state.get("protected_tokens", [])
    
    evaluations = []
    passing_candidates = []
    
    for idx, candidate in enumerate(candidates):
        eval_result = evaluate_candidate_quality(original, candidate, protected)
        eval_result["candidate_index"] = idx
        evaluations.append(eval_result)
        
        if eval_result["pass"]:
            passing_candidates.append((idx, candidate))
            
    best_candidate = None
    if passing_candidates:
        # Just pick the first passing candidate for now (could be optimized for style later)
        best_candidate = passing_candidates[0][1]
        
    return {
        "evaluations": evaluations,
        "best_candidate": best_candidate
    }
