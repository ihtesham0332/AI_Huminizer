import os
from io import BytesIO
from PyPDF2 import PdfReader
import docx

def parse_txt(content: bytes) -> str:
    """Parses plain text bytes."""
    return content.decode('utf-8')

def parse_pdf(content: bytes) -> str:
    """Parses text from a PDF file."""
    reader = PdfReader(BytesIO(content))
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text.strip()

def parse_docx(content: bytes) -> str:
    """Parses text from a DOCX file."""
    doc = docx.Document(BytesIO(content))
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

def parse_document(content: bytes, filename: str) -> str:
    """
    Routes the byte content to the appropriate parser based on the file extension.
    """
    ext = os.path.splitext(filename)[1].lower()
    
    if ext == '.txt' or ext == '.md':
        return parse_txt(content)
    elif ext == '.pdf':
        return parse_pdf(content)
    elif ext == '.docx':
        return parse_docx(content)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
