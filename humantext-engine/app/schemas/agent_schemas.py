from pydantic import BaseModel, Field
from typing import Optional

class InputAnalysisResult(BaseModel):
    word_count: int = Field(description="The total number of words in the document.")
    language: str = Field(description="The detected language of the text, e.g., 'English', 'Urdu'.")
    content_type: str = Field(description="The classification of the text, e.g., 'Academic', 'Blog', 'Email', 'Casual', 'Technical'.")
    has_citations: bool = Field(description="True if the text contains academic or inline citations.")
    has_technical_terms: bool = Field(description="True if the text contains highly technical jargon or coding terms.")
