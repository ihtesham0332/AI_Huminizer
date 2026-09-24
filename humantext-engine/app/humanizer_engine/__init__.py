"""Humanizer Engine: a controllable, verifiable rewriting pipeline for AI-drafted text.

Design goal: make machine-drafted prose read like careful human writing while
guaranteeing meaning, facts, numbers, quotes and citations are preserved.
"""
from .config import EngineConfig, LEVELS, TONES
from .pipeline import HumanizerEngine, HumanizeResult
from .providers import AnthropicProvider, MockProvider, Provider

__all__ = [
    "EngineConfig", "LEVELS", "TONES", "HumanizerEngine", "HumanizeResult",
    "AnthropicProvider", "MockProvider", "Provider",
]
__version__ = "0.1.0"
