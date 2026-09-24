from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
import json

router = APIRouter()

class SentenceRewriteRequest(BaseModel):
    sentence: str
    context: str = ""
    tone: str = "natural"

@router.post("/sentence")
async def rewrite_sentence(request: SentenceRewriteRequest):
    """
    Takes a single sentence and returns 3 alternative variations.
    Used for the interactive "Deep Scan" rewriting UI.
    """
    llm = ChatOllama(model="qwen2.5:3b", temperature=0.8, format="json")
    
    prompt = PromptTemplate.from_template(
        "You are an expert editor. Rewrite the following sentence in 3 different ways.\n"
        "Tone requested: {tone}\n"
        "Context (optional, for flow): {context}\n\n"
        "Sentence to rewrite: {sentence}\n\n"
        "Return a JSON object with exactly one key 'alternatives' containing a list of 3 string variations."
    )
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({
            "sentence": request.sentence,
            "context": request.context,
            "tone": request.tone
        })
        
        content = response.content if hasattr(response, "content") else str(response)
        data = json.loads(content)
        
        return {"alternatives": data.get("alternatives", [request.sentence])}
        
    except Exception as e:
        print(f"Sentence rewrite error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate sentence alternatives.")
