import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

def plan_humanization_node(state: dict) -> dict:
    """
    LangGraph node: Reads the original text, metadata, and protected tokens,
    then generates a structured blueprint for the Humanizer to follow.
    """
    text = state.get("original_text", "")
    metadata = state.get("metadata", {})
    protected_tokens = state.get("protected_tokens", [])
    strength = state.get("strength", "medium")
    
    # We use a fast local model for planning
    llm = ChatOllama(model="qwen2.5:3b", temperature=0.1, format="json")
    
    prompt = PromptTemplate.from_template(
        "You are an expert AI Humanization Planner.\n"
        "Your job is to determine the best strategy to make the text sound natural and human, "
        "while protecting the provided facts and citations.\n\n"
        "Input Metadata: {metadata}\n"
        "Protected Tokens (DO NOT ALTER THESE): {protected}\n"
        "Requested Rewrite Strength: {strength} (If light, minimize structural changes. If aggressive, restructure paragraphs entirely).\n\n"
        "Return a JSON object with exactly these keys:\n"
        "- 'sentence_variation': 'high', 'medium', or 'low'\n"
        "- 'vocabulary_change': 'high', 'medium', or 'low'\n"
        "- 'tone_adjustment': A short string describing the required tone (e.g. 'Maintain academic formality but increase sentence length variance').\n\n"
        "Text to plan for:\n{text}"
    )
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({
            "text": text[:2000], 
            "metadata": json.dumps(metadata), 
            "protected": json.dumps(protected_tokens),
            "strength": strength
        })
        content = response.content if hasattr(response, "content") else str(response)
        rewrite_plan = json.loads(content)
        return {"rewrite_plan": rewrite_plan}
    except Exception as e:
        print(f"Planner error: {e}")
        # Safe fallback
        return {"rewrite_plan": {
            "sentence_variation": "medium", 
            "vocabulary_change": "medium", 
            "tone_adjustment": "Maintain original meaning."
        }}
