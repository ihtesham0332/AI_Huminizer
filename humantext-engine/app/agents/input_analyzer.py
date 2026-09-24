import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from app.schemas.agent_schemas import InputAnalysisResult

def analyze_input_text(text: str) -> InputAnalysisResult:
    """
    Analyzes the raw input text to determine language, word count, 
    content type, and the presence of citations or technical terms.
    """
    word_count = len(text.split())
    
    # We use a fast, local model for this classification task
    llm = ChatOllama(model="qwen2.5:3b", temperature=0.1, format="json")
    
    prompt = PromptTemplate.from_template(
        "You are an expert Document Input Analyzer.\n"
        "Analyze the following text and return a JSON object with exactly these keys:\n"
        "- 'language': (string) The detected language, e.g. 'English', 'Urdu'.\n"
        "- 'content_type': (string) The classification, e.g. 'Academic', 'Blog', 'Technical', 'Email', 'Casual'.\n"
        "- 'has_citations': (boolean) True if the text contains academic citations, False otherwise.\n"
        "- 'has_technical_terms': (boolean) True if the text contains highly technical jargon or coding terms.\n\n"
        "Text to analyze:\n{text}"
    )
    
    chain = prompt | llm
    
    try:
        # We only need to analyze the first 1500 chars to determine context
        response = chain.invoke({"text": text[:1500]})
        content = response.content if hasattr(response, "content") else str(response)
        data = json.loads(content)
        
        return InputAnalysisResult(
            word_count=word_count,
            language=data.get("language", "Unknown"),
            content_type=data.get("content_type", "General"),
            has_citations=data.get("has_citations", False),
            has_technical_terms=data.get("has_technical_terms", False)
        )
    except Exception as e:
        print(f"Input Analyzer error: {e}")
        # Fallback response
        return InputAnalysisResult(
            word_count=word_count,
            language="English",
            content_type="General",
            has_citations=False,
            has_technical_terms=False
        )
