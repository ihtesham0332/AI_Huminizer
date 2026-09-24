# 11. DOCUMENT INTELLIGENCE ENGINE

The Document Intelligence Engine is responsible for understanding the structure and semantic hierarchy of an uploaded document *before* any text rewriting occurs.

## 1. Supported Formats
*   `TXT`: Standard plain text.
*   `Markdown`: Extracted with preserving `#`, `*`, and link structures.
*   `DOCX`: Parsed using `python-docx` to extract text while maintaining paragraph breaks and bold/italic indicators.
*   `PDF`: Parsed using `PyMuPDF` (fitz) or `PyPDF2` to extract text blocks. Note: Complex multi-column PDFs may require OCR fallback (P4).

## 2. Document Object Model (DOM)
The engine creates an internal, normalized JSON structure representing the document:
```json
{
  "document_id": "doc_123",
  "metadata": {
    "total_words": 1500,
    "language": "en"
  },
  "hierarchy": [
    {
      "type": "heading",
      "level": 1,
      "text": "Introduction"
    },
    {
      "type": "paragraph",
      "index": 0,
      "sentences": [
        {"index": 0, "text": "This is a sentence."},
        {"index": 1, "text": "This is another."}
      ]
    }
  ]
}
```

## 3. Structural Analysis
The engine determines the context of a paragraph. A paragraph under a "Methodology" heading in a research paper is treated differently than a paragraph under "Executive Summary".

## 4. Chunking Strategy
For long documents, the text is chunked into logical units (typically paragraphs, max 1000 tokens) to ensure the LLM generator does not lose context or hallucinate. Paragraph boundaries are strictly respected during generation.
