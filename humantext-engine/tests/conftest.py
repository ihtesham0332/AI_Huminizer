"""
HumanText Engine — Test Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Shared fixtures and configuration for all tests.
"""

from __future__ import annotations

import os

import pytest

# Force test environment
os.environ["DEBUG"] = "true"
os.environ["LOG_FORMAT"] = "console"
os.environ["LOG_LEVEL"] = "DEBUG"
os.environ["MAX_REVISIONS"] = "2"
os.environ["REQUEST_TIMEOUT"] = "30"


@pytest.fixture
def sample_robotic_text() -> str:
    """A typical AI-generated text with robotic patterns."""
    return (
        "Furthermore, it is important to note that artificial intelligence has significantly "
        "transformed the landscape of modern technology. Additionally, the implementation of "
        "machine learning algorithms has facilitated the development of innovative solutions. "
        "Moreover, the utilization of deep learning frameworks has enabled researchers to achieve "
        "unprecedented results. In conclusion, it can be observed that AI continues to play a "
        "pivotal role in shaping the future of technology. It is worth noting that these "
        "advancements have far-reaching implications for various industries."
    )


@pytest.fixture
def sample_natural_text() -> str:
    """A naturally-written human text with good variation."""
    return (
        "AI has changed how we build software. Machine learning algorithms — once limited to "
        "research labs — now power everything from search engines to medical diagnosis. What "
        "makes deep learning particularly interesting is its ability to find patterns humans "
        "miss entirely. But the technology isn't perfect. False positives remain a challenge, "
        "and training these models requires enormous computing resources. Still, the trajectory "
        "is clear: AI will keep reshaping industries for decades to come."
    )


@pytest.fixture
def sample_academic_text() -> str:
    """Academic text with citations and hedging language."""
    return (
        "The study suggests that AI may improve productivity in some workplaces "
        "(Smith et al., 2024). However, the evidence remains inconclusive regarding "
        "long-term effects on employment rates. According to Johnson (2023), approximately "
        "35% of surveyed organizations reported measurable efficiency gains, while 12% "
        "observed no significant change. These findings should be interpreted with caution "
        "due to the limited sample size (n=247) and self-reported data."
    )


@pytest.fixture
def sample_facts_text() -> str:
    """Text with many factual elements to test Fact Guardian."""
    return (
        "OpenAI released GPT-4 on March 14, 2023. The model supports a context window "
        "of 128,000 tokens and costs $10 per million input tokens. According to their "
        "technical report, GPT-4 scored in the 90th percentile on the Uniform Bar Exam. "
        "The company, headquartered in San Francisco, California, was founded in 2015 "
        "by Sam Altman, Elon Musk, and others with an initial $1 billion pledge."
    )


@pytest.fixture
def empty_text() -> str:
    """Empty text for validation testing."""
    return ""


@pytest.fixture
def very_long_text() -> str:
    """Text exceeding the default max length for validation testing."""
    return "This is a sentence. " * 5000  # ~100k characters
