from app.schemas.request import SentenceRewriteRequest
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
import json

def rewrite_sentence(request: SentenceRewriteRequest) -> dict:
    llm = ChatOllama(model="qwen2.5:3b", temperature=0.9, format="json")
    
    prompt = PromptTemplate.from_template(
        "You are an expert human writer. Rewrite the following sentence into 3 completely different variations.\n"
        "The variations should sound 100% human and completely bypass AI detectors by varying the rhythm and vocabulary.\n"
        "Context (if any): {context}\n"
        "Original Sentence: {sentence}\n"
        "Target Tone: {tone}\n\n"
        "Return a JSON object with exactly one key 'variations' which is a list of 3 string variations.\n"
        "Example: {{\"variations\": [\"var1\", \"var2\", \"var3\"]}}"
    )
    
    chain = prompt | llm
    try:
        response = chain.invoke({"sentence": request.sentence, "context": request.context, "tone": request.tone})
        content = response.content if hasattr(response, "content") else str(response)
        data = json.loads(content)
        variations = data.get("variations", [request.sentence])
        return {"variations": variations[:3]}
    except Exception as e:
        print(f"Error in sentence rewriting: {e}")
        return {"variations": [request.sentence]}
