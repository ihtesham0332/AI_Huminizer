import pytest
from app.skills.skill_11 import transform_paragraphs

def test_transform_paragraphs_empty():
    result = transform_paragraphs({}, [])
    assert result == []

def test_transform_paragraphs_no_plan():
    paragraphs = ["First paragraph."]
    result = transform_paragraphs({}, paragraphs)
    assert result == paragraphs

def test_transform_paragraphs_no_llm():
    paragraphs = ["First paragraph."]
    result = transform_paragraphs({"operations": []}, paragraphs)
    assert result[0] == "First paragraph. (transformed paragraph)"

def test_transform_paragraphs_with_mock_llm():
    class MockLLM:
        def invoke(self, inputs):
            return ["Transformed paragraph."]
            
    result = transform_paragraphs({"operations": []}, ["Original paragraph."], llm_client=MockLLM())
    assert result == ["Transformed paragraph."]
