from typing import Dict, Any, List
import time

# Import all skills
from app.skills.skill_01 import validate_input
from app.skills.skill_02 import analyze_document
from app.skills.skill_03 import analyze_semantics
from app.skills.skill_04 import extract_claims
from app.skills.skill_05 import extract_facts
from app.skills.skill_06 import analyze_style
from app.skills.skill_07 import analyze_context
from app.skills.skill_08 import analyze_readability
from app.skills.skill_09 import generate_plan
from app.skills.skill_10 import transform_sentences
from app.skills.skill_11 import transform_paragraphs
from app.skills.skill_12 import optimize_discourse
from app.skills.skill_13 import preserve_terminology
from app.skills.skill_14 import preserve_citations
from app.skills.skill_15 import validate_source_integrity
from app.skills.skill_16 import validate_fact_preservation
from app.skills.skill_17 import validate_tone_consistency
from app.skills.skill_18 import score_quality
from app.skills.skill_19 import calculate_humanization
from app.skills.skill_20 import generate_revision_instructions

from langchain_ollama import ChatOllama

# Initialize the local open-source LLM (4-bit Quantized Qwen2.5 3B)
llm_client = ChatOllama(
    model="qwen2.5:3b",
    temperature=0.7,
    format="json"
)

def _track_latency(state: Dict[str, Any], agent_name: str, start_time: float):
    if "agent_metadata" not in state:
        state["agent_metadata"] = {}
    state["agent_metadata"][agent_name] = {
        "agent_name": agent_name,
        "status": "completed",
        "latency_ms": (time.time() - start_time) * 1000
    }

def input_validator_node(state: Dict[str, Any]) -> Dict[str, Any]:
    start = time.time()
    result, cleaned = validate_input(state.get("original_text", ""))
    _track_latency(state, "Input Validator", start)
    if not result["is_valid"]:
        state["status"] = "failed"
        state["validation_errors"].append("Input validation failed")
    else:
        state["original_text"] = cleaned # use cleaned text for remainder of pipeline
    return {"original_text": state["original_text"], "status": state["status"]}

def document_analyst_node(state: Dict[str, Any]) -> Dict[str, Any]:
    start = time.time()
    text = state.get("original_text", "")
    doc_stats = analyze_document(text)
    readability = analyze_readability(text)
    _track_latency(state, "Document Analyst", start)
    return {"document_analysis": doc_stats, "readability_analysis": readability}

def semantic_analyst_node(state: Dict[str, Any]) -> Dict[str, Any]:
    start = time.time()
    text = state.get("original_text", "")
    semantics = analyze_semantics(text, llm_client)
    claims = extract_claims(text, llm_client)
    facts = extract_facts(text, llm_client)
    _track_latency(state, "Semantic Analyst", start)
    return {"semantic_analysis": semantics, "claims": claims, "facts": facts}

def style_analyst_node(state: Dict[str, Any]) -> Dict[str, Any]:
    start = time.time()
    text = state.get("original_text", "")
    style = analyze_style(text, llm_client)
    _track_latency(state, "Style Analyst", start)
    return {"style_analysis": style}

def context_analyst_node(state: Dict[str, Any]) -> Dict[str, Any]:
    start = time.time()
    text = state.get("original_text", "")
    context = analyze_context(text, llm_client)
    _track_latency(state, "Context Analyst", start)
    return {"context_analysis": context}

def planner_node(state: Dict[str, Any]) -> Dict[str, Any]:
    start = time.time()
    analysis = {
        "document": state.get("document_analysis"),
        "semantics": state.get("semantic_analysis"),
        "style": state.get("style_analysis"),
        "context": state.get("context_analysis")
    }
    plan = generate_plan(analysis, llm_client)
    _track_latency(state, "Planner", start)
    return {"transformation_plan": plan}

def rewriter_node(state: Dict[str, Any]) -> Dict[str, Any]:
    start = time.time()
    text = state.get("original_text", "")
    mode = state.get("target_mode", "natural")
    tone = state.get("target_tone", "clear")
    
    # Build a proper LangChain Prompt
    from langchain_core.prompts import PromptTemplate
    prompt = PromptTemplate.from_template(
        "You are an expert human writer. Rewrite the following text so that it sounds 100% human and completely bypasses AI detectors. "
        "You must fix any repetitive phrasing, uneven rhythm, and low readability.\n\n"
        "Follow these rules:\n"
        "1. PRESERVE STRUCTURE: You MUST keep the exact same paragraph structure, line breaks, bullet points, and formatting as the original text. Only change the words and phrasing, do NOT change the layout.\n"
        "2. ZERO PLAGIARISM: Do not copy the original sentence structures. Rewrite the concepts using your own entirely original phrasing.\n"
        "3. HIGH READABILITY: Use natural, everyday vocabulary. Do not use overly complex or archaic words. Keep the flow smooth and easy to read.\n"
        "4. NATURAL RHYTHM: Vary your sentence lengths naturally. Use a mix of short and medium sentences. Avoid repetitive starting words (e.g., don't start every sentence with 'The' or 'This').\n"
        "5. NO AI JARGON: Strictly avoid words like 'delve', 'testament', 'crucial', 'multifaceted', 'moreover', 'furthermore', 'tapestry', 'realm', 'foster', 'underscore', and 'leverage'.\n"
        "6. VOICE: Write in a highly human, {tone} tone. Use active voice.\n\n"
        "Original Text:\n{text}\n\n"
        "Return ONLY the absolute final, perfectly humanized text. Do not include any notes."
    )
    
    # Execute the LLM
    try:
        # Turn off structured format temporarily just for the rewriter node so it outputs raw string
        from langchain_ollama import ChatOllama
        local_llm = ChatOllama(model="qwen2.5:3b", temperature=0.95)
        chain = prompt | local_llm
        response = chain.invoke({"tone": tone, "text": text})
        optimized = response.content if hasattr(response, "content") else str(response)
    except Exception as e:
        print(f"Error in rewriter_node: {e}")
        optimized = text # Fallback
        
    # Deterministic term preservation
    locked_terms = preserve_terminology(state.get("facts", {}), text)
    locked_citations = preserve_citations(state.get("facts", {}), text)
    state["constraints"] = [{"terms": locked_terms, "citations": locked_citations}]
    
    _track_latency(state, "Rewriter", start)
    return {"rewritten_text": optimized.strip(), "constraints": state["constraints"]}

def semantic_validator_node(state: Dict[str, Any]) -> Dict[str, Any]:
    start = time.time()
    original_claims = {"claims": state.get("claims", [])}
    text = state.get("rewritten_text", "")
    result = validate_source_integrity(original_claims, text, llm_client)
    _track_latency(state, "Semantic Validator", start)
    return {"semantic_score": 1.0 if result["is_valid"] else 0.0}

def fact_validator_node(state: Dict[str, Any]) -> Dict[str, Any]:
    start = time.time()
    facts = state.get("facts", {})
    text = state.get("rewritten_text", "")
    result = validate_fact_preservation(facts, text)
    _track_latency(state, "Fact Validator", start)
    return {"factual_score": 1.0 if result["is_valid"] else 0.0}

def style_critic_node(state: Dict[str, Any]) -> Dict[str, Any]:
    start = time.time()
    tone = [state.get("target_tone")] if state.get("target_tone") else []
    text = state.get("rewritten_text", "")
    result = validate_tone_consistency(tone, text, llm_client)
    _track_latency(state, "Style Critic", start)
    return {"style_score": 1.0 if result["is_valid"] else 0.0}

def quality_judge_node(state: Dict[str, Any]) -> Dict[str, Any]:
    start = time.time()
    text = state.get("rewritten_text", "")
    
    qa = score_quality(text)
    hum = calculate_humanization(text, llm_client)
    
    state["readability_score"] = qa.get("overall_quality", 0.0)
    state["naturalness_score"] = hum.get("naturalness_score", 0.0)
    
    total_score = (
        state.get("semantic_score", 0.0) * 0.4 +
        state.get("factual_score", 0.0) * 0.3 +
        state.get("style_score", 0.0) * 0.2 +
        state.get("readability_score", 0.0) * 0.1
    )
    
    _track_latency(state, "Quality Judge", start)
    
    if total_score >= 0.8:
        state["status"] = "completed"
    else:
        state["status"] = "needs_revision"
        
    return {
        "readability_score": state["readability_score"],
        "naturalness_score": state["naturalness_score"],
        "quality_score": total_score,
        "status": state["status"]
    }

def revision_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    start = time.time()
    failures = [{"reasoning": "Quality score below threshold"}]
    instructions = generate_revision_instructions(failures, state.get("original_text", ""), state.get("rewritten_text", ""), llm_client)
    
    state["revision_count"] += 1
    state["revision_history"].append(instructions)
    _track_latency(state, "Revision Agent", start)
    return {"revision_count": state["revision_count"], "revision_history": state["revision_history"]}
