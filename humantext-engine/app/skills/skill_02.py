from typing import Dict, Any, List
from app.utils.text import split_paragraphs, split_sentences, count_words

def analyze_document(cleaned_text: str) -> Dict[str, Any]:
    """
    Skill 02: Document Analysis
    Analyzes sentence/paragraph statistics and structural features.
    
    Args:
        cleaned_text: The cleaned input text.
        
    Returns:
        A dictionary containing document statistics and structure map.
    """
    if not cleaned_text:
        return {
            "sentence_lengths": [],
            "paragraph_lengths": [],
            "structure_map": [],
            "total_sentences": 0,
            "total_paragraphs": 0,
            "total_words": 0
        }
        
    paragraphs = split_paragraphs(cleaned_text)
    
    sentence_lengths: List[int] = []
    paragraph_lengths: List[int] = []
    structure_map: List[Dict[str, Any]] = []
    
    total_words = count_words(cleaned_text)
    
    for i, p in enumerate(paragraphs):
        p_sentences = split_sentences(p)
        p_word_count = count_words(p)
        
        paragraph_lengths.append(p_word_count)
        
        para_structure = {
            "paragraph_index": i,
            "word_count": p_word_count,
            "sentence_count": len(p_sentences),
            "sentences": []
        }
        
        for j, s in enumerate(p_sentences):
            s_word_count = count_words(s)
            sentence_lengths.append(s_word_count)
            para_structure["sentences"].append({
                "sentence_index": j,
                "word_count": s_word_count
            })
            
        structure_map.append(para_structure)
        
    return {
        "sentence_lengths": sentence_lengths,
        "paragraph_lengths": paragraph_lengths,
        "structure_map": structure_map,
        "total_sentences": len(sentence_lengths),
        "total_paragraphs": len(paragraphs),
        "total_words": total_words
    }
