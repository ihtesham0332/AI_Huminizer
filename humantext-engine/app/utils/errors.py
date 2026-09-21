"""
HumanText Engine — Error Handling & Exception Hierarchy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Design principles:
  1. NO silent failures — every error is captured, logged, and traceable.
  2. Every exception carries a UNIQUE error code for fast debugging.
  3. Every exception carries context (which skill, agent, or step failed).
  4. Structured error responses for API consumers.
  5. Root-cause chain: exceptions wrap the original cause so you never lose it.

Error Code Format:
  HTE-XXXX where:
    HTE-1xxx = Input/Validation errors
    HTE-2xxx = Analysis/Skill errors
    HTE-3xxx = Transformation errors
    HTE-4xxx = Validation/Guardian errors
    HTE-5xxx = LLM/Model errors
    HTE-6xxx = Graph/Orchestration errors
    HTE-7xxx = API/Service errors
    HTE-8xxx = Configuration errors
    HTE-9xxx = System/Infrastructure errors

Usage:
    from app.utils.errors import (
        InputValidationError,
        SemanticDriftError,
        FactualInconsistencyError,
        LLMError,
    )

    raise InputValidationError(
        message="Input text is empty",
        context={"field": "text", "received": ""},
    )
"""

from __future__ import annotations

import traceback
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ERROR CODES — Fast lookup for debugging
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ErrorCode(str, Enum):
    """
    Unique error codes for every failure type.
    Search the codebase for any code to instantly find where it's raised.
    """

    # ── HTE-1xxx: Input/Validation ──
    INPUT_EMPTY = "HTE-1001"
    INPUT_TOO_LONG = "HTE-1002"
    INPUT_MALFORMED = "HTE-1003"
    INPUT_UNSUPPORTED_LANGUAGE = "HTE-1004"
    INPUT_INVALID_MODE = "HTE-1005"
    INPUT_INVALID_DOCUMENT_TYPE = "HTE-1006"
    INPUT_INVALID_WRITING_DNA = "HTE-1007"

    # ── HTE-2xxx: Analysis/Skill ──
    SKILL_EXECUTION_FAILED = "HTE-2001"
    SKILL_TIMEOUT = "HTE-2002"
    SKILL_INVALID_OUTPUT = "HTE-2003"
    DOCUMENT_ANALYSIS_FAILED = "HTE-2010"
    SEMANTIC_ANALYSIS_FAILED = "HTE-2011"
    STYLE_ANALYSIS_FAILED = "HTE-2012"
    CONTEXT_ANALYSIS_FAILED = "HTE-2013"
    READABILITY_ANALYSIS_FAILED = "HTE-2014"
    CLAIM_EXTRACTION_FAILED = "HTE-2015"
    FACT_EXTRACTION_FAILED = "HTE-2016"

    # ── HTE-3xxx: Transformation ──
    PLANNING_FAILED = "HTE-3001"
    REWRITE_FAILED = "HTE-3002"
    SENTENCE_TRANSFORM_FAILED = "HTE-3003"
    PARAGRAPH_TRANSFORM_FAILED = "HTE-3004"
    DISCOURSE_OPTIMIZATION_FAILED = "HTE-3005"
    TERMINOLOGY_LOCK_FAILED = "HTE-3006"
    CITATION_LOCK_FAILED = "HTE-3007"

    # ── HTE-4xxx: Validation/Guardian ──
    SEMANTIC_DRIFT_DETECTED = "HTE-4001"
    FACTUAL_INCONSISTENCY = "HTE-4002"
    STYLE_MISMATCH = "HTE-4003"
    NATURALNESS_BELOW_THRESHOLD = "HTE-4004"
    QUALITY_BELOW_THRESHOLD = "HTE-4005"
    SEMANTIC_VALIDATION_FAILED = "HTE-4010"
    FACT_VALIDATION_FAILED = "HTE-4011"
    STYLE_VALIDATION_FAILED = "HTE-4012"
    GUARDIAN_CHECK_FAILED = "HTE-4020"
    MAX_REVISIONS_EXCEEDED = "HTE-4030"

    # ── HTE-5xxx: LLM/Model ──
    LLM_API_ERROR = "HTE-5001"
    LLM_TIMEOUT = "HTE-5002"
    LLM_RATE_LIMITED = "HTE-5003"
    LLM_INVALID_RESPONSE = "HTE-5004"
    LLM_JSON_PARSE_ERROR = "HTE-5005"
    LLM_CONTEXT_OVERFLOW = "HTE-5006"
    LLM_PROVIDER_UNAVAILABLE = "HTE-5007"
    EMBEDDING_ERROR = "HTE-5010"
    MODEL_NOT_FOUND = "HTE-5011"

    # ── HTE-6xxx: Graph/Orchestration ──
    GRAPH_EXECUTION_FAILED = "HTE-6001"
    GRAPH_NODE_FAILED = "HTE-6002"
    GRAPH_EDGE_FAILED = "HTE-6003"
    GRAPH_STATE_INVALID = "HTE-6004"
    GRAPH_TIMEOUT = "HTE-6005"
    PARALLEL_EXECUTION_FAILED = "HTE-6010"
    AGENT_EXECUTION_FAILED = "HTE-6020"
    AGENT_CONFLICT = "HTE-6021"

    # ── HTE-7xxx: API/Service ──
    SERVICE_ERROR = "HTE-7001"
    REQUEST_VALIDATION_ERROR = "HTE-7002"
    WRITING_DNA_NOT_FOUND = "HTE-7003"
    WRITING_DNA_CREATION_FAILED = "HTE-7004"

    # ── HTE-8xxx: Configuration ──
    CONFIG_MISSING = "HTE-8001"
    CONFIG_INVALID = "HTE-8002"
    NO_LLM_PROVIDER = "HTE-8003"
    PROMPT_NOT_FOUND = "HTE-8004"

    # ── HTE-9xxx: System/Infrastructure ──
    DATABASE_ERROR = "HTE-9001"
    CACHE_ERROR = "HTE-9002"
    FILE_SYSTEM_ERROR = "HTE-9003"
    UNEXPECTED_ERROR = "HTE-9999"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ERROR DETAIL MODEL — Structured, serializable error info
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ErrorDetail(BaseModel):
    """
    Structured error detail for API responses and logging.
    Every error in the system can be serialized to this format.
    """

    error_code: str = Field(description="Unique error code (e.g., HTE-1001)")
    message: str = Field(description="Human-readable error message")
    category: str = Field(description="Error category (input, analysis, transform, etc.)")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="When the error occurred (UTC ISO-8601)",
    )
    context: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context for debugging (skill, agent, step, inputs)",
    )
    cause: Optional[str] = Field(
        default=None,
        description="Root cause exception message (from the original error)",
    )
    traceback_summary: Optional[str] = Field(
        default=None,
        description="Shortened traceback for debugging (last 5 frames)",
    )
    request_id: Optional[str] = Field(
        default=None,
        description="Request ID for tracing across the entire pipeline",
    )
    recovery_hint: Optional[str] = Field(
        default=None,
        description="Suggested action to fix or recover from this error",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# BASE EXCEPTION — All project exceptions inherit from this
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class HumanTextError(Exception):
    """
    Base exception for the HumanText Engine.
    
    Every exception carries:
      - error_code: unique code for fast lookup
      - message: human-readable description
      - context: dict of debugging info (what skill, what input, what step)
      - cause: the original exception that triggered this error
      - recovery_hint: what the developer/user can do about it
      
    This makes it trivial to find the EXACT root cause of any failure:
      1. Search the error code (e.g., HTE-4001) in the codebase
      2. Read the context dict for what was happening
      3. Read the cause for the underlying error
      4. Read the traceback_summary for the call chain
    """

    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.UNEXPECTED_ERROR,
        context: dict[str, Any] | None = None,
        cause: Exception | None = None,
        recovery_hint: str | None = None,
        request_id: str | None = None,
    ) -> None:
        self.error_code = error_code
        self.message = message
        self.context = context or {}
        self.cause = cause
        self.recovery_hint = recovery_hint
        self.request_id = request_id

        # Build the full message with error code prefix
        full_message = f"[{error_code.value}] {message}"
        if cause:
            full_message += f" | Caused by: {type(cause).__name__}: {cause}"

        super().__init__(full_message)

        # Preserve the exception chain
        if cause:
            self.__cause__ = cause

    @property
    def category(self) -> str:
        """Derive category from error code prefix."""
        code = self.error_code.value
        prefix = int(code.split("-")[1][0])
        categories = {
            1: "input_validation",
            2: "analysis",
            3: "transformation",
            4: "validation",
            5: "llm",
            6: "orchestration",
            7: "api",
            8: "configuration",
            9: "system",
        }
        return categories.get(prefix, "unknown")

    def to_detail(self) -> ErrorDetail:
        """Convert to a structured ErrorDetail for API responses and logging."""
        # Get shortened traceback (last 5 frames)
        tb_summary = None
        if self.cause and self.cause.__traceback__:
            tb_lines = traceback.format_tb(self.cause.__traceback__)
            tb_summary = "".join(tb_lines[-5:]) if len(tb_lines) > 5 else "".join(tb_lines)
        elif self.__traceback__:
            tb_lines = traceback.format_tb(self.__traceback__)
            tb_summary = "".join(tb_lines[-5:]) if len(tb_lines) > 5 else "".join(tb_lines)

        return ErrorDetail(
            error_code=self.error_code.value,
            message=self.message,
            category=self.category,
            context=self.context,
            cause=f"{type(self.cause).__name__}: {self.cause}" if self.cause else None,
            traceback_summary=tb_summary,
            request_id=self.request_id,
            recovery_hint=self.recovery_hint,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary for logging."""
        return self.to_detail().model_dump(exclude_none=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SPECIFIC EXCEPTION CLASSES — Organized by category
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ── Input/Validation (HTE-1xxx) ────────────────────────────────────

class InputValidationError(HumanTextError):
    """Raised when input text fails validation (empty, too long, malformed)."""

    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.INPUT_EMPTY,
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, error_code=error_code, **kwargs)


# ── Analysis/Skill (HTE-2xxx) ─────────────────────────────────────

class SkillExecutionError(HumanTextError):
    """Raised when a skill fails to execute."""

    def __init__(
        self,
        message: str,
        skill_name: str,
        error_code: ErrorCode = ErrorCode.SKILL_EXECUTION_FAILED,
        **kwargs: Any,
    ) -> None:
        context = kwargs.pop("context", {})
        context["skill_name"] = skill_name
        super().__init__(
            message=f"Skill '{skill_name}' failed: {message}",
            error_code=error_code,
            context=context,
            **kwargs,
        )


class SkillTimeoutError(SkillExecutionError):
    """Raised when a skill exceeds its timeout."""

    def __init__(self, skill_name: str, timeout_seconds: int, **kwargs: Any) -> None:
        super().__init__(
            message=f"Timed out after {timeout_seconds}s",
            skill_name=skill_name,
            error_code=ErrorCode.SKILL_TIMEOUT,
            recovery_hint=f"Increase timeout or simplify input for skill '{skill_name}'",
            **kwargs,
        )


class SkillOutputError(SkillExecutionError):
    """Raised when a skill produces invalid/unexpected output."""

    def __init__(self, skill_name: str, message: str, **kwargs: Any) -> None:
        super().__init__(
            message=message,
            skill_name=skill_name,
            error_code=ErrorCode.SKILL_INVALID_OUTPUT,
            **kwargs,
        )


# ── Transformation (HTE-3xxx) ─────────────────────────────────────

class TransformationError(HumanTextError):
    """Raised when a transformation operation fails."""

    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.REWRITE_FAILED,
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, error_code=error_code, **kwargs)


class PlanningError(TransformationError):
    """Raised when the humanization planner fails to create a plan."""

    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(
            message=message,
            error_code=ErrorCode.PLANNING_FAILED,
            recovery_hint="Check if the analysis results are complete and valid",
            **kwargs,
        )


# ── Validation/Guardian (HTE-4xxx) ────────────────────────────────

class ValidationError(HumanTextError):
    """Base for all validation failures."""

    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.GUARDIAN_CHECK_FAILED,
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, error_code=error_code, **kwargs)


class SemanticDriftError(ValidationError):
    """
    Raised when a rewrite violates semantic preservation (Dimension 12 HARD GATE).
    
    This is the MOST CRITICAL error in the system.
    It means the rewrite changed the meaning of the original text.
    """

    def __init__(
        self,
        message: str,
        semantic_score: float,
        threshold: float,
        drift_details: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> None:
        context = kwargs.pop("context", {})
        context.update({
            "semantic_score": semantic_score,
            "threshold": threshold,
            "drift_details": drift_details or [],
        })
        super().__init__(
            message=f"SEMANTIC DRIFT DETECTED: score={semantic_score:.3f} < threshold={threshold:.3f}. {message}",
            error_code=ErrorCode.SEMANTIC_DRIFT_DETECTED,
            context=context,
            recovery_hint="Revision agent should fix specific drift points without re-introducing new ones",
            **kwargs,
        )


class FactualInconsistencyError(ValidationError):
    """
    Raised when a rewrite contains factual errors (numbers, dates, names changed).
    
    Second most critical error — the Fact Guardian caught a discrepancy.
    """

    def __init__(
        self,
        message: str,
        fact_score: float,
        threshold: float,
        discrepancies: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> None:
        context = kwargs.pop("context", {})
        context.update({
            "fact_score": fact_score,
            "threshold": threshold,
            "discrepancies": discrepancies or [],
        })
        super().__init__(
            message=f"FACTUAL INCONSISTENCY: score={fact_score:.3f} < threshold={threshold:.3f}. {message}",
            error_code=ErrorCode.FACTUAL_INCONSISTENCY,
            context=context,
            recovery_hint="Revision agent must restore original facts exactly",
            **kwargs,
        )


class MaxRevisionsExceededError(ValidationError):
    """Raised when the revision loop hits the maximum attempts."""

    def __init__(
        self,
        max_revisions: int,
        best_score: float,
        **kwargs: Any,
    ) -> None:
        context = kwargs.pop("context", {})
        context.update({"max_revisions": max_revisions, "best_score": best_score})
        super().__init__(
            message=f"Max revisions ({max_revisions}) exceeded. Best quality score: {best_score:.3f}",
            error_code=ErrorCode.MAX_REVISIONS_EXCEEDED,
            context=context,
            recovery_hint="Returning best-effort output. Consider simplifying the input or relaxing thresholds.",
            **kwargs,
        )


# ── LLM/Model (HTE-5xxx) ─────────────────────────────────────────

class LLMError(HumanTextError):
    """Base for all LLM-related errors."""

    def __init__(
        self,
        message: str,
        model: str = "unknown",
        provider: str = "unknown",
        error_code: ErrorCode = ErrorCode.LLM_API_ERROR,
        **kwargs: Any,
    ) -> None:
        context = kwargs.pop("context", {})
        context.update({"model": model, "provider": provider})
        super().__init__(message=message, error_code=error_code, context=context, **kwargs)


class LLMTimeoutError(LLMError):
    """Raised when an LLM call times out."""

    def __init__(self, model: str, timeout_seconds: int, **kwargs: Any) -> None:
        super().__init__(
            message=f"LLM call timed out after {timeout_seconds}s",
            model=model,
            error_code=ErrorCode.LLM_TIMEOUT,
            recovery_hint="Retry with a shorter input or increase timeout",
            **kwargs,
        )


class LLMRateLimitError(LLMError):
    """Raised when hitting LLM provider rate limits."""

    def __init__(self, model: str, provider: str, retry_after: int | None = None, **kwargs: Any) -> None:
        context = kwargs.pop("context", {})
        if retry_after:
            context["retry_after_seconds"] = retry_after
        super().__init__(
            message=f"Rate limited by {provider}. Retry after {retry_after}s" if retry_after else f"Rate limited by {provider}",
            model=model,
            provider=provider,
            error_code=ErrorCode.LLM_RATE_LIMITED,
            context=context,
            recovery_hint="Wait and retry, or switch to a different model/provider",
            **kwargs,
        )


class LLMJsonParseError(LLMError):
    """Raised when LLM output cannot be parsed as valid JSON."""

    def __init__(self, model: str, raw_output: str, **kwargs: Any) -> None:
        context = kwargs.pop("context", {})
        # Truncate raw output for logging (keep first 500 chars)
        context["raw_output_preview"] = raw_output[:500] + ("..." if len(raw_output) > 500 else "")
        super().__init__(
            message="LLM returned invalid JSON",
            model=model,
            error_code=ErrorCode.LLM_JSON_PARSE_ERROR,
            context=context,
            recovery_hint="Retry the call — JSON parse failures are usually transient",
            **kwargs,
        )


class LLMProviderUnavailableError(LLMError):
    """Raised when no LLM provider is available."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(
            message="No LLM provider is configured or available",
            error_code=ErrorCode.LLM_PROVIDER_UNAVAILABLE,
            recovery_hint="Set at least one API key in .env (OPENAI_API_KEY, ANTHROPIC_API_KEY, or GOOGLE_API_KEY)",
            **kwargs,
        )


# ── Graph/Orchestration (HTE-6xxx) ────────────────────────────────

class GraphExecutionError(HumanTextError):
    """Raised when the LangGraph workflow fails."""

    def __init__(
        self,
        message: str,
        node: str = "unknown",
        error_code: ErrorCode = ErrorCode.GRAPH_EXECUTION_FAILED,
        **kwargs: Any,
    ) -> None:
        context = kwargs.pop("context", {})
        context["graph_node"] = node
        super().__init__(message=message, error_code=error_code, context=context, **kwargs)


class GraphNodeError(GraphExecutionError):
    """Raised when a specific graph node fails."""

    def __init__(self, node: str, message: str, **kwargs: Any) -> None:
        super().__init__(
            message=f"Node '{node}' failed: {message}",
            node=node,
            error_code=ErrorCode.GRAPH_NODE_FAILED,
            **kwargs,
        )


class ParallelExecutionError(GraphExecutionError):
    """Raised when parallel agent execution partially fails."""

    def __init__(
        self,
        failed_agents: list[str],
        succeeded_agents: list[str],
        errors: list[dict[str, Any]],
        **kwargs: Any,
    ) -> None:
        context = kwargs.pop("context", {})
        context.update({
            "failed_agents": failed_agents,
            "succeeded_agents": succeeded_agents,
            "agent_errors": errors,
        })
        super().__init__(
            message=f"Parallel execution partial failure: {len(failed_agents)} failed, {len(succeeded_agents)} succeeded",
            error_code=ErrorCode.PARALLEL_EXECUTION_FAILED,
            context=context,
            recovery_hint=f"Failed agents: {', '.join(failed_agents)}. Check individual agent errors.",
            **kwargs,
        )


# ── Configuration (HTE-8xxx) ──────────────────────────────────────

class ConfigurationError(HumanTextError):
    """Raised when configuration is missing or invalid."""

    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.CONFIG_MISSING,
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, error_code=error_code, **kwargs)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# UTILITY FUNCTIONS — For wrapping and re-raising errors
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def wrap_error(
    original: Exception,
    message: str,
    error_code: ErrorCode = ErrorCode.UNEXPECTED_ERROR,
    context: dict[str, Any] | None = None,
    request_id: str | None = None,
) -> HumanTextError:
    """
    Wrap any exception into a HumanTextError while preserving the cause chain.
    
    Use this in try/except blocks to convert external library errors
    into structured HumanText errors without losing the original traceback.
    
    Example:
        try:
            result = openai_client.chat(...)
        except openai.APIError as e:
            raise wrap_error(
                e,
                message="Failed to call OpenAI API",
                error_code=ErrorCode.LLM_API_ERROR,
                context={"model": "gpt-4o", "prompt_length": 1500},
            )
    """
    return HumanTextError(
        message=message,
        error_code=error_code,
        context=context or {},
        cause=original,
        request_id=request_id,
    )


def format_error_chain(error: Exception, max_depth: int = 10) -> str:
    """
    Format an error and its full cause chain into a readable string.
    
    Useful for debugging nested exceptions — shows the full path
    from the surface error down to the root cause.
    
    Example output:
        [HTE-5001] Failed to call OpenAI API
          ↳ Caused by: openai.APIConnectionError: Connection refused
            ↳ Caused by: ConnectionRefusedError: [Errno 111] Connection refused
    """
    lines: list[str] = []
    current: Exception | None = error
    depth = 0

    while current is not None and depth < max_depth:
        indent = "  " * depth
        prefix = "↳ Caused by: " if depth > 0 else ""

        if isinstance(current, HumanTextError):
            lines.append(f"{indent}{prefix}[{current.error_code.value}] {current.message}")
        else:
            lines.append(f"{indent}{prefix}{type(current).__name__}: {current}")

        current = current.__cause__
        depth += 1

    return "\n".join(lines)
