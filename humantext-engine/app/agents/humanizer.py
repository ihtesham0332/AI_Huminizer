from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
import concurrent.futures

def generate_single_candidate(text: str, plan: dict, protected: list, variant: str) -> str:
    """
    Calls the LLM to generate one specific variation.
    """
    llm = ChatOllama(model="qwen2.5:3b", temperature=0.7)  # Higher temp for creativity
    
    prompt = PromptTemplate.from_template(
        "You are an expert editor. Rewrite the following text to sound extremely natural and human-written.\n"
        "Follow this strategy plan: {plan}\n\n"
        "CRITICAL RULES:\n"
        "1. You MUST preserve the exact semantic meaning.\n"
        "2. You MUST NOT alter or remove any of the following protected items: {protected}\n"
        "3. This is variant '{variant}'. Introduce slight stylistic uniqueness associated with this variant.\n\n"
        "Original Text:\n{text}\n\n"
        "Rewritten Text:"
    )
    
    chain = prompt | llm
    try:
        response = chain.invoke({
            "text": text,
            "plan": str(plan),
            "protected": str(protected),
            "variant": variant
        })
        return response.content.strip() if hasattr(response, "content") else str(response).strip()
    except Exception as e:
        print(f"Humanizer error on {variant}: {e}")
        return text

def humanizer_node(state: dict) -> dict:
    """
    LangGraph node: Takes the rewrite plan and generates 3 parallel candidates.
    """
    text = state.get("original_text", "")
    plan = state.get("rewrite_plan", {})
    protected = state.get("protected_tokens", [])
    
    variants = ["Professional", "Conversational", "Academic"]
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
