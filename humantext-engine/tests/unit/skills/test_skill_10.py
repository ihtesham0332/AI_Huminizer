import pytest
from app.skills.skill_10 import transform_sentences

def test_transform_sentences_empty():
    result = transform_sentences({}, [])
    assert result == []

def test_transform_sentences_no_plan():
    sentences = ["First sentence."]
    result = transform_sentences({}, sentences)
    assert result == sentences

def test_transform_sentences_no_llm():
    sentences = ["First sentence."]
    result = transform_sentences({"operations": []}, sentences)
    assert result[0] == "First sentence. (transformed)"

def test_transform_sentences_with_mock_llm():
    class MockLLM:
        def invoke(self, inputs):
            return ["Transformed sentence."]
            
    result = transform_sentences({"operations": []}, ["Original sentence."], llm_client=MockLLM())
    assert result == ["Transformed sentence."]
