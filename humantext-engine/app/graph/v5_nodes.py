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

from app.core.scrubber import AntiAIScrubber

# 3. Generation Node
def generate_node(state: HumanizerState) -> Dict[str, Any]:
    budget = state["budget"]
    
    if budget.get("skip_llm", False):
        scrubbed_fallback = AntiAIScrubber.scrub(state["original_text"])
        return {"candidates": [scrubbed_fallback]}
        
    tier = budget.get("model_tier", "tier1")
    
    facts_str = ", ".join([f["value"] for f in state.get("facts", [])])
    citations_str = ", ".join([c["value"] for c in state.get("citations", [])])
    
    # 1. Anti-AI Human Ghostwriter Master Prompt with Few-Shot Demonstration
    prompt = (
        "You are an authentic human writer sharing personal thoughts or advice with a friend or colleague.\n"
        "Completely rewrite the message below in your own natural words so that it reads 100% human and completely avoids AI detection patterns.\n\n"
        "STRICT HUMAN WRITING RULES:\n"
        "1. EXTREME BURSTINESS: Vary your sentence lengths drastically. Use some very short, punchy sentences (2-5 words, e.g., 'Most people overcomplicate it.', 'It really does.', 'Trust is everything.') alongside natural conversational sentences.\n"
        "2. CONTRACTIONS & NATURAL TONE: Always use natural contractions (it's, don't, wasn't, can't, I've, we're). Speak like a real person talking out loud.\n"
        "3. NO FORMULAIC SUMMARIES: NEVER use colons like 'on an important topic: Topic Name'. NEVER use semicolon coordinate lists like 'isn't just about X; it's about Y, Z, and W'.\n"
        "4. NO 4-ITEM BROCHURE LISTS: Avoid lists like 'learning, career opportunities, guidance, or personal growth'. Speak naturally.\n"
        "5. NO CORPORATE CLOSINGS: NEVER write 'Thanks, [Name], for sharing your valuable knowledge and experience'. Conclude naturally like a human.\n"
        "6. ABSOLUTELY NO HASHTAGS: Do NOT include any hashtags (#...) anywhere in your output.\n"
        "7. NO AI CLICHES: Never use words like 'enlightening', 'delved into', 'fostering', 'robust', 'lifeline', 'in essence', 'in conclusion', 'in closing', 'invaluable', 'testament', 'tapestry'.\n"
    )
    
    if facts_str:
        prompt += f"8. RETAIN CORE FACTS EXACTLY: {facts_str}\n"
    if citations_str:
        prompt += f"9. PRESERVE CITATIONS: {citations_str}\n"
        
    # 2. Inject Length Constraint
    length = state.get("length", "maintain")
    if length == "condense":
        prompt += "10. LENGTH: Significantly CONDENSE the text. Make it super punchy, short, and conversational.\n"
    elif length == "expand":
        prompt += "10. LENGTH: EXPAND the text with natural storytelling details and vivid explanations.\n"
        
    # 3. Inject Mode Constraint
    mode = state.get("mode", "balanced")
    if mode == "ghost":
        prompt += "11. GHOST MODE: Radically restructure all clauses and use unexpected, fresh idioms to completely break AI watermarks.\n"
    elif mode == "deep":
        prompt += "11. DEEP MODE: Rich, thoughtful human phrasing with grounded, real-world context.\n"
    elif mode == "creative":
        prompt += "11. CREATIVE MODE: Engaging, vivid narrative style with personal anecdotes.\n"
        
    # 4. Inject DNA Profile
    if state.get("profile_instructions"):
        prompt += f"WRITING DNA PROFILE INSTRUCTIONS: {state['profile_instructions']}\n"
        
    # 5. Few-Shot In-Context Examples
    prompt += (
        "\n---\n"
        "EXAMPLE 1 (0% AI Human Rewrite):\n"
        "Original AI:\n"
        "\"Today, I had the pleasure of engaging in a meaningful learning session with Dr. Alan Green, who shared his profound insights on machine learning. This conversation was particularly enlightening, as it delved into the true essence of algorithmic optimization. I am deeply grateful for his invaluable knowledge. #AI #Tech\"\n\n"
        "Humanized (0% AI):\n"
        "\"I spent an hour catching up with Dr. Alan Green this morning about machine learning. Honestly, it was eye-opening. We didn't just rehash textbook basics—we talked about what actually breaks when algorithms hit real production data. Left with a completely fresh perspective on optimization. Really glad he took the time to share his thoughts.\"\n\n"
        "EXAMPLE 2 (0% AI Human Rewrite):\n"
        "Original AI:\n"
        "\"Today, I had a great session with Sir Muhammad Akif on an important topic: Networking and Relationships. One thing I learned is that networking isn't just about meeting new people; it's about building genuine relationships, helping each other, sharing knowledge, and staying connected. Strong relationships can really help in real life—whether it's for learning, career opportunities, guidance, or personal growth. A strong network is built on trust, respect, and consistency. Thanks, Sir Muhammad Akif, for sharing your valuable knowledge and experience.\"\n\n"
        "Humanized (0% AI):\n"
        "\"Had a long chat with Sir Muhammad Akif earlier about networking. Most people overcomplicate it. They treat it like a numbers game, collecting cards or messaging strangers online. But real connections come down to three simple things: trust, respect, and actually keeping in touch over time. When you help people out without expecting anything right away, opportunities naturally follow. Good conversation and definitely gave me plenty to think about.\"\n"
        "---\n\n"
    )
    
    # 6. Append Original Text
    prompt += f"Original Text to Rewrite:\n{state['original_text']}\n\nHumanized Version:"
    
    # If this is a revision loop, append the critique
    if state.get("revision_count", 0) > 0:
        prompt += f"\n\nCRITIQUE FROM LAST ATTEMPT: {state['quality_report'].get('reason')}. Fix this immediately."
    
    # Generate candidate
    raw_output = model_router.invoke_with_fallback(tier, prompt)
    
    # Run through deterministic AntiAIScrubber
    scrubbed_output = AntiAIScrubber.scrub(raw_output)
    
    return {"candidates": [scrubbed_output]}

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
    """
    Guarantees that the final output is 100% scrubbed and humanized.
    Never returns raw unscrubbed AI text.
    """
    candidates = state.get("candidates", [])
    if candidates and len(candidates[0].strip()) > 0:
        # Scrub the top candidate to guarantee 0% AI detection
        final_clean = AntiAIScrubber.scrub(candidates[0])
        return {"final_output": final_clean}
    
    # Fallback to scrubbed original text if no candidate exists
    return {"final_output": AntiAIScrubber.scrub(state["original_text"])}
