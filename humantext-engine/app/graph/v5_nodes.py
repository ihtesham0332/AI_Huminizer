from typing import Dict, Any
from app.graph.v5_state import HumanizerState
from app.agents.style_agent import StyleAgent
from app.agents.guardians.fact_guardian import FactGuardianAgent
from app.agents.guardians.citation_guardian import CitationGuardianAgent
from app.agents.cost_controller import CostControllerAgent
from app.agents.quality_critic import QualityCriticAgent
from app.core.model_router import ModelRouter

# Initialize Agents
style_agent = StyleAgent()
fact_guardian = FactGuardianAgent()
citation_guardian = CitationGuardianAgent()
cost_controller = CostControllerAgent()
model_router = ModelRouter()
quality_critic = QualityCriticAgent(fact_guardian, citation_guardian)

# 1. Understanding Node
def analyze_node(state: HumanizerState) -> Dict[str, Any]:
    text = state["original_text"]
    
    # Run analysis in parallel (simulated here synchronously for simplicity)
    style = style_agent.analyze_style(text)
    facts = fact_guardian.extract_facts(text)
    citations = citation_guardian.extract_citations(text)
    
    return {
        "style_profile": style,
        "facts": facts,
        "citations": citations
    }

# 2. Planning Node
def planning_node(state: HumanizerState) -> Dict[str, Any]:
    # Hardcoded user_tier for skeleton. In production, comes from JWT/Context.
    budget = cost_controller.determine_budget(
        state["original_text"], 
        user_tier="pro", 
        mode=state.get("mode", "balanced")
    )
    return {"budget": budget}

# 3. Generation Node
def generate_node(state: HumanizerState) -> Dict[str, Any]:
    budget = state["budget"]
    
    if budget.get("skip_llm", False):
        return {"candidates": [state["original_text"]]}
        
    tier = budget.get("model_tier", "tier1")
    
    facts_str = ", ".join([f["value"] for f in state.get("facts", [])])
    citations_str = ", ".join([c["value"] for c in state.get("citations", [])])
    
    # 1. Base Prompt
    prompt = f"You are an expert human ghostwriter. Your task is to COMPLETELY REWRITE the following text so that it sounds 100% human, natural, and engaging. Do NOT just swap synonyms. Change the sentence structures, vary the paragraph lengths, and inject natural transitions. \n\nYOU MUST RETAIN THESE FACTS EXACTLY: {facts_str}. \nYOU MUST PRESERVE THESE CITATIONS IN THEIR EXACT FORMAT: {citations_str}\n\n"
    
    # 2. Inject Length Constraint
    length = state.get("length", "maintain")
    if length == "condense":
        prompt += "CONSTRAINT: You must significantly CONDENSE the text. Make it punchy and short.\n"
    elif length == "expand":
        prompt += "CONSTRAINT: You must EXPAND the text, adding detail, flow, and rich descriptions.\n"
        
    # 3. Inject Mode Constraint
    mode = state.get("mode", "balanced")
    if mode == "ghost":
        prompt += "MODE: GHOST MODE. You must completely restructure sentences and use highly creative phrasing to aggressively bypass AI detectors.\n"
    elif mode == "deep":
        prompt += "MODE: DEEP STRUCTURE. Maintain a highly formal, academic, and structured tone.\n"
    elif mode == "creative":
        prompt += "MODE: CREATIVE. Use vivid storytelling elements and engaging metaphors.\n"
        
    # 4. Inject DNA Profile
    if state.get("profile_instructions"):
        prompt += f"WRITING DNA PROFILE INSTRUCTIONS: {state['profile_instructions']}\n"
        
    # 5. Append Original Text
    prompt += f"\nOriginal:\n{state['original_text']}"
    
    # If this is a revision loop, append the critique
    if state.get("revision_count", 0) > 0:
        prompt += f"\n\nCRITIQUE FROM LAST ATTEMPT: {state['quality_report'].get('reason')}. Fix this."
    
    # Generate candidate(s)
    output = model_router.invoke_with_fallback(tier, prompt)
    
    return {"candidates": [output]}

# 4. Critique Node
def critique_node(state: HumanizerState) -> Dict[str, Any]:
    budget = state["budget"]
    if budget.get("skip_llm", False):
        return {"quality_report": {"passed": True}, "final_output": state["original_text"]}
        
    report = quality_critic.evaluate(state)
    
    new_revision_count = state.get("revision_count", 0)
    if not report["passed"]:
        new_revision_count += 1
        
    return {
        "quality_report": report,
        "revision_count": new_revision_count
    }

# 5. Router Edge Logic
def route_after_critique(state: HumanizerState) -> str:
    report = state.get("quality_report", {})
    budget = state.get("budget", {})
    
    if report.get("passed", False):
        return "finalize"
        
    if state.get("revision_count", 0) >= budget.get("max_revisions", 1):
        return "finalize" # Force finalize if we hit budget limits to avoid infinite loops
        
    return "generate" # Send back to generation node for revision

# 6. Finalize Node
def finalize_node(state: HumanizerState) -> Dict[str, Any]:
    # If it failed all revisions, we might want to fallback to the original text
    # to protect the facts, rather than outputting a hallucination.
    report = state.get("quality_report", {})
    if not report.get("passed", False):
         # Safety fallback: Return original if LLM couldn't fix itself within budget
         return {"final_output": state["original_text"]}
         
    return {"final_output": state["candidates"][0]}
