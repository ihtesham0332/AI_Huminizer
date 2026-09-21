"""
Tests for app.utils.errors — Error handling system.
"""

from __future__ import annotations

import pytest

from app.utils.errors import (
    ErrorCode,
    ErrorDetail,
    FactualInconsistencyError,
    HumanTextError,
    InputValidationError,
    LLMError,
    LLMJsonParseError,
    LLMRateLimitError,
    LLMTimeoutError,
    MaxRevisionsExceededError,
    SemanticDriftError,
    SkillExecutionError,
    SkillTimeoutError,
    format_error_chain,
    wrap_error,
)


class TestErrorCodes:
    """Test that error codes are structured correctly."""

    def test_error_code_format(self):
        """All error codes follow HTE-XXXX format."""
        for code in ErrorCode:
            assert code.value.startswith("HTE-"), f"Code {code} doesn't follow format"
            assert len(code.value) == 8, f"Code {code} should be 8 chars"

    def test_error_code_categories(self):
        """Each category has codes in the right range."""
        assert ErrorCode.INPUT_EMPTY.value == "HTE-1001"
        assert ErrorCode.SKILL_EXECUTION_FAILED.value == "HTE-2001"
        assert ErrorCode.REWRITE_FAILED.value == "HTE-3002"
        assert ErrorCode.SEMANTIC_DRIFT_DETECTED.value == "HTE-4001"
        assert ErrorCode.LLM_API_ERROR.value == "HTE-5001"
        assert ErrorCode.GRAPH_EXECUTION_FAILED.value == "HTE-6001"
        assert ErrorCode.SERVICE_ERROR.value == "HTE-7001"
        assert ErrorCode.CONFIG_MISSING.value == "HTE-8001"
        assert ErrorCode.UNEXPECTED_ERROR.value == "HTE-9999"


class TestHumanTextError:
    """Test base exception behavior."""

    def test_basic_error(self):
        err = HumanTextError(
            message="Something went wrong",
            error_code=ErrorCode.UNEXPECTED_ERROR,
        )
        assert "HTE-9999" in str(err)
        assert "Something went wrong" in str(err)
        assert err.category == "system"

    def test_error_with_cause(self):
        original = ValueError("bad value")
        err = HumanTextError(
            message="Wrapper error",
            error_code=ErrorCode.SKILL_EXECUTION_FAILED,
            cause=original,
        )
        assert err.cause is original
        assert err.__cause__ is original
        assert "ValueError" in str(err)

    def test_error_with_context(self):
        err = HumanTextError(
            message="Test",
            context={"skill": "skill_02", "input_length": 1500},
        )
        assert err.context["skill"] == "skill_02"
        assert err.context["input_length"] == 1500

    def test_error_to_detail(self):
        err = HumanTextError(
            message="Test error",
            error_code=ErrorCode.LLM_API_ERROR,
            context={"model": "gpt-4o"},
            recovery_hint="Check API key",
            request_id="req-123",
        )
        detail = err.to_detail()
        assert isinstance(detail, ErrorDetail)
        assert detail.error_code == "HTE-5001"
        assert detail.message == "Test error"
        assert detail.category == "llm"
        assert detail.context["model"] == "gpt-4o"
        assert detail.recovery_hint == "Check API key"
        assert detail.request_id == "req-123"

    def test_error_to_dict(self):
        err = HumanTextError(message="Test", error_code=ErrorCode.INPUT_EMPTY)
        d = err.to_dict()
        assert isinstance(d, dict)
        assert d["error_code"] == "HTE-1001"
        assert "timestamp" in d


class TestSpecificErrors:
    """Test domain-specific exception classes."""

    def test_input_validation_error(self):
        err = InputValidationError(
            message="Text is empty",
            error_code=ErrorCode.INPUT_EMPTY,
        )
        assert err.category == "input_validation"

    def test_skill_execution_error(self):
        err = SkillExecutionError(
            message="spaCy model not loaded",
            skill_name="skill_02_document_analysis",
        )
        assert "skill_02_document_analysis" in str(err)
        assert err.context["skill_name"] == "skill_02_document_analysis"

    def test_skill_timeout_error(self):
        err = SkillTimeoutError(
            skill_name="skill_03_semantic_analysis",
            timeout_seconds=30,
        )
        assert "30s" in str(err)
        assert err.recovery_hint is not None

    def test_semantic_drift_error(self):
        err = SemanticDriftError(
            message="Hedging changed from 'may' to 'will'",
            semantic_score=0.72,
            threshold=0.85,
            drift_details=[{"type": "modality_change", "original": "may", "rewritten": "will"}],
        )
        assert err.error_code == ErrorCode.SEMANTIC_DRIFT_DETECTED
        assert err.context["semantic_score"] == 0.72
        assert err.context["threshold"] == 0.85
        assert len(err.context["drift_details"]) == 1

    def test_factual_inconsistency_error(self):
        err = FactualInconsistencyError(
            message="Date changed from 2023 to 2024",
            fact_score=0.80,
            threshold=0.95,
            discrepancies=[{"type": "date_altered", "original": "2023", "rewritten": "2024"}],
        )
        assert err.error_code == ErrorCode.FACTUAL_INCONSISTENCY
        assert len(err.context["discrepancies"]) == 1

    def test_max_revisions_exceeded(self):
        err = MaxRevisionsExceededError(max_revisions=3, best_score=0.68)
        assert "3" in str(err)
        assert err.context["best_score"] == 0.68

    def test_llm_timeout_error(self):
        err = LLMTimeoutError(model="gpt-4o", timeout_seconds=60)
        assert err.context["model"] == "gpt-4o"

    def test_llm_rate_limit_error(self):
        err = LLMRateLimitError(model="gpt-4o", provider="openai", retry_after=30)
        assert err.context["retry_after_seconds"] == 30

    def test_llm_json_parse_error(self):
        err = LLMJsonParseError(model="gpt-4o", raw_output="this is not json {{{")
        assert "raw_output_preview" in err.context


class TestErrorUtilities:
    """Test error wrapping and formatting utilities."""

    def test_wrap_error(self):
        original = ConnectionError("Connection refused")
        wrapped = wrap_error(
            original,
            message="Failed to reach API",
            error_code=ErrorCode.LLM_API_ERROR,
            context={"endpoint": "https://api.openai.com"},
        )
        assert isinstance(wrapped, HumanTextError)
        assert wrapped.cause is original
        assert wrapped.context["endpoint"] == "https://api.openai.com"

    def test_format_error_chain_simple(self):
        err = HumanTextError(message="Top level error")
        chain = format_error_chain(err)
        assert "Top level error" in chain

    def test_format_error_chain_nested(self):
        root = ConnectionError("Connection refused")
        mid = wrap_error(root, "API unreachable", ErrorCode.LLM_API_ERROR)
        top = wrap_error(mid, "Skill failed", ErrorCode.SKILL_EXECUTION_FAILED)

        chain = format_error_chain(top)
        assert "Skill failed" in chain
        assert "API unreachable" in chain
        assert "Connection refused" in chain
        assert "↳ Caused by:" in chain
