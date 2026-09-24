from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
import concurrent.futures

from app.core.scrubber import AntiAIScrubber

def generate_single_candidate(text: str, plan: dict, protected: list, variant: str) -> str:
    """
    Calls the LLM to generate one specific variation.
    """
    import os
    model_name = os.getenv("OLLAMA_PRIMARY_MODEL", "llama3.1:8b")
    llm = ChatOllama(model=model_name, temperature=0.85, top_p=0.92)  # Higher temp for creativity
    
    prompt = PromptTemplate.from_template(
        "You are an average, everyday person writing a casual post or message.\n"
        "Rewrite the following text so it sounds completely natural, conversational, and written by a real human. Write at an 8th-grade reading level.\n\n"
        "Strategy: {plan}\n\n"
        "STRICT RULES:\n"
        "1. USE SIMPLE WORDS. Never use formal, academic, or corporate vocabulary. Do NOT use words like 'profound', 'enlightening', 'moreover', 'crucial', 'foster', 'delve', or 'tapestry'. Use words like 'great', 'also', 'important', 'help'.\n"
        "2. BURSTINESS: Vary your sentence lengths drastically. Write some very short sentences. Then, follow them with longer ones to explain the point.\n"
        "3. ACTIVE VOICE: Speak directly. Say 'We built a plan' instead of 'A plan was built'.\n"
        "4. PRESERVE MEANING: Do not change the core message.\n"
        "5. PROTECTED ITEMS: You MUST NOT alter or remove any of the following protected items: {protected}\n"
        "6. VARIANT: Your style is '{variant}'. Ensure the tone matches this exactly.\n\n"
        "Original Text:\n{text}\n\n"
        "Humanized Text:"
    )
    
    chain = prompt | llm
    try:
        response = chain.invoke({
            "text": text,
            "plan": str(plan),
            "protected": str(protected),
            "variant": variant
        })
        raw = response.content.strip() if hasattr(response, "content") else str(response).strip()
        return AntiAIScrubber.scrub(raw)
    except Exception as e:
        print(f"Humanizer error on {variant}: {e}")
        return AntiAIScrubber.scrub(text)

def humanizer_node(state: dict) -> dict:
    """
    LangGraph node: Takes the rewrite plan and generates 3 parallel candidates.
    """
    text = state.get("original_text", "")
    plan = state.get("rewrite_plan", {})
    protected = state.get("protected_tokens", [])
    
    # Changed from Academic/Professional to strictly human/casual styles
    variants = ["Highly Conversational", "Direct and Simple", "Personal Story"]
    candidates = []
    
    # Execute generation in parallel to reduce latency
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(generate_single_candidate, text, plan, protected, v) 
            for v in variants
        ]
        for future in concurrent.futures.as_completed(futures):
            candidates.append(future.result())
            
    return {"candidates": candidates}
