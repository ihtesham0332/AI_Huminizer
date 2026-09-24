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
        "You are an elite Anti-AI Detection Strategist.\n"
        "Your job is to determine the best strategy to make the text sound natural, human, and completely undetectable by AI detectors (like GPTZero and Quillbot), "
        "while absolutely protecting the provided facts and citations.\n\n"
        "Input Metadata: {metadata}\n"
        "Protected Tokens (DO NOT ALTER THESE): {protected}\n"
        "Requested Rewrite Strength: {strength} (If aggressive, restructure paragraphs entirely to break AI patterns).\n\n"
        "Return a JSON object with exactly these keys:\n"
        "- 'sentence_variation': MUST BE 'high'. Mandate drastic variations between short, punchy sentences and longer, complex ones (Burstiness).\n"
        "- 'vocabulary_change': MUST BE 'high'. Mandate replacing predictable AI words with conversational, slightly imperfect phrasing (Perplexity).\n"
        "- 'tone_adjustment': A short string describing the required tone (e.g. 'Use extreme burstiness, highly colloquial phrasing, and active voice. Strictly avoid all formal or corporate AI tropes.').\n\n"
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
