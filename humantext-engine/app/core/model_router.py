import os
from typing import Optional, Any
from langchain_ollama import ChatOllama

class ModelRouter:
    """
    Abstracts LLM APIs. Configured for local open-source models via Ollama.
    """
    
    def __init__(self):
        # We default to popular open-source models. 
        # Ensure you have pulled these in Ollama (e.g., `ollama run llama3`)
        
        self.primary_model = ChatOllama(
            model=os.getenv("OLLAMA_PRIMARY_MODEL", "qwen2.5:3b"),
            temperature=0.85,
            top_p=0.92,
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )
        
        self.fallback_model = ChatOllama(
            model=os.getenv("OLLAMA_FALLBACK_MODEL", "qwen2.5:7b"),
            temperature=0.85,
            top_p=0.92,
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )
        
    def get_model(self, tier: str) -> Any:
        """
        Returns the appropriate LangChain model. Since we are local, 
        we can just use the primary model for all tiers or split by weight if desired.
        """
        return self.primary_model
            
    def invoke_with_fallback(self, tier: str, prompt: str) -> str:
        """
        Helper method to execute a prompt with automatic fallback.
        """
        model = self.get_model(tier)
        try:
            # Execute actual LLM call to local Ollama
            response = model.invoke(prompt)
            return response.content
            
        except Exception as e:
            print(f"Primary local model failed: {e}. Triggering fallback...")
            try:
                fallback_response = self.fallback_model.invoke(prompt)
                return fallback_response.content
            except Exception as fallback_error:
                return f"Error: Local Ollama models failed. Is Ollama running on localhost:11434? Details: {fallback_error}"
