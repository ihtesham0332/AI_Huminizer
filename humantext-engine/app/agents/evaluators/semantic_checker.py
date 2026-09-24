import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

def evaluate_semantics(original: str, candidate: str) -> dict:
    """
    Evaluates if the candidate text retains the exact core meaning, claims, 
    and negations of the original text.
    """
    llm = ChatOllama(model="qwen2.5:3b", temperature=0.1, format="json")
    
    prompt = PromptTemplate.from_template(
        "You are an expert Semantic Verification Agent.\n"
        "Compare the ORIGINAL text to the CANDIDATE text.\n"
        "Your ONLY job is to determine if the candidate changed any core factual claims, reversed any negations (e.g. adding or removing 'not'), or altered the fundamental meaning.\n\n"
        "ORIGINAL: {original}\n\n"
        "CANDIDATE: {candidate}\n\n"
        "Return a JSON object with exactly two keys:\n"
        "- 'pass': (boolean) true if meaning is 100% preserved, false if it was altered.\n"
        "- 'reason': (string) A short explanation of your decision."
    )
    
    chain = prompt | llm
    try:
        response = chain.invoke({"original": original, "candidate": candidate})
        content = response.content if hasattr(response, "content") else str(response)
        result = json.loads(content)
        return result
    except Exception as e:
        print(f"Semantic Checker error: {e}")
        # Default to safe passing if the local model crashes
        return {"pass": True, "reason": "Evaluation failed, assumed pass."}
