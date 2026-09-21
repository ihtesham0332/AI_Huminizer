import pytest
from app.skills.skill_02 import analyze_document

def test_analyze_document_empty():
    result = analyze_document("")
    assert result["total_sentences"] == 0
    assert result["total_paragraphs"] == 0
    assert result["total_words"] == 0
    assert result["sentence_lengths"] == []
    assert result["paragraph_lengths"] == []

def test_analyze_document_basic():
    text = "This is a sentence. This is another.\n\nAnd a new paragraph here."
    result = analyze_document(text)
    
    assert result["total_paragraphs"] == 2
    assert result["total_sentences"] == 3
    assert result["total_words"] == 12
    
    # Check paragraph lengths
    assert result["paragraph_lengths"] == [7, 5]
    
    # Check sentence lengths
    assert result["sentence_lengths"] == [4, 3, 5]
    
    # Check structure map
    assert len(result["structure_map"]) == 2
    
    p1 = result["structure_map"][0]
    assert p1["word_count"] == 7
    assert p1["sentence_count"] == 2
    assert p1["sentences"][0]["word_count"] == 4
    assert p1["sentences"][1]["word_count"] == 3
    
    p2 = result["structure_map"][1]
    assert p2["word_count"] == 5
    assert p2["sentence_count"] == 1
    assert p2["sentences"][0]["word_count"] == 5
