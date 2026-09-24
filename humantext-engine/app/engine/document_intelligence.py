import io
from typing import Dict, Any

try:
    import docx
except ImportError:
    docx = None

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None


class DocumentIntelligenceEngine:
    """
    Handles structured parsing of various document formats.
    Adheres to Master Prompt Section 4 (Document Intelligence Engine).
    """
    
    def parse_plain_text(self, text: str) -> Dict[str, Any]:
        """Creates the internal document representation from raw text."""
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        return {
            "metadata": {"format": "txt", "char_count": len(text)},
            "sections": [{"paragraphs": paragraphs}],
            "raw_text": text
        }
        
    def parse_docx(self, file_bytes: bytes) -> Dict[str, Any]:
        """Parses a DOCX file while attempting to preserve structure."""
        if not docx:
            raise ImportError("python-docx is not installed. Run 'pip install python-docx'")
            
        doc = docx.Document(io.BytesIO(file_bytes))
        paragraphs = []
        headings = []
        
        for p in doc.paragraphs:
            if not p.text.strip():
                continue
            if p.style.name.startswith('Heading'):
                headings.append(p.text)
            else:
                paragraphs.append(p.text)
                
        raw_text = "\n\n".join(paragraphs)
        
        return {
            "metadata": {"format": "docx", "char_count": len(raw_text)},
            "headings": headings,
            "sections": [{"paragraphs": paragraphs}],
            "raw_text": raw_text
        }
        
    def parse_pdf(self, file_bytes: bytes) -> Dict[str, Any]:
        """Parses a PDF file."""
        if not PyPDF2:
            raise ImportError("PyPDF2 is not installed. Run 'pip install pypdf2'")
            
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text_chunks = []
        
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_chunks.append(text)
                
        raw_text = "\n\n".join(text_chunks)
        
        return {
            "metadata": {"format": "pdf", "pages": len(reader.pages)},
            "raw_text": raw_text
        }
