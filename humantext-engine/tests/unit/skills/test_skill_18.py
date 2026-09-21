import pytest
from app.skills.skill_18 import score_quality

def test_score_quality_empty():
    result = score_quality("")
    assert result["fluency"] == 0.0

def test_score_quality_short():
    result = score_quality("Hello world.")
    assert result["fluency"] == 1.0

def test_score_quality_long():
    result = score_quality("This is a sufficiently long sentence to test the logic.")
    assert result["fluency"] == 0.9
    assert result["cohesion"] == 0.85
