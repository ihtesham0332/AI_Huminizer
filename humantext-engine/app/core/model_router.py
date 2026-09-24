import os
import httpx
from typing import Optional, Any, List
from langchain_ollama import ChatOllama

class ModelRouter:
    """
    Abstracts LLM APIs. Configured for local open-source models via Ollama.
    Dynamically prioritizes available models: llama3.1:8b -> qwen2.5:7b -> qwen2.5:3b.
    """
    
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.preferred_models: List[str] = [
            os.getenv("OLLAMA_PRIMARY_MODEL", "llama3.1:8b"),
            os.getenv("OLLAMA_FALLBACK_MODEL", "qwen2.5:7b"),
            "qwen2.5:3b"
        ]
        
    def _get_model_instance(self, model_name: str) -> ChatOllama:
        return ChatOllama(
            model=model_name,
            temperature=0.85,
            top_p=0.92,
            base_url=self.base_url
        )
        
    def get_model(self, tier: str = "tier1") -> Any:
        return self._get_model_instance(self.preferred_models[0])
            
    def invoke_with_fallback(self, tier: str, prompt: str) -> str:
        """
        Executes a prompt with automatic multi-model fallback.
        """
        last_error = None
        for model_name in self.preferred_models:
            try:
                model = self._get_model_instance(model_name)
                response = model.invoke(prompt)
                content = response.content if hasattr(response, "content") else str(response)
                if content and not content.startswith("Error:"):
                    return content
            except Exception as e:
                last_error = e
                print(f"Model '{model_name}' invocation failed: {e}. Trying next local model...")
                continue
                
        return f"Error: All local Ollama models failed. Details: {last_error}"
