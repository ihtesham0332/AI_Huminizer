"""
HumanText Engine — Structured Logging & Observability
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Design principles:
  1. STRUCTURED (JSON) logs — machine-parseable, searchable.
  2. Every log entry carries request_id for end-to-end tracing.
  3. Every log entry carries component (skill/agent/graph node).
  4. Rich console output for development, JSON for production.
  5. Performance timing built-in (how long each step took).
  6. Error context automatically captured and attached.

Usage:
    from app.utils.logging import get_logger, log_execution_time

    logger = get_logger("skill_02_document_analysis")
    
    logger.info("Starting analysis", text_length=1500, document_type="academic")
    logger.error("Analysis failed", error_code="HTE-2010", cause="spacy model not found")

    # Timing decorator
    @log_execution_time("semantic_analysis")
    async def analyze(text: str) -> dict:
        ...
"""

from __future__ import annotations

import functools
import sys
import time
from contextvars import ContextVar
from typing import Any, Callable

import structlog

from app.config.settings import LogFormat, LogLevel, get_settings

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONTEXT VARIABLES — Thread/async-safe request tracking
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)
_component_var: ContextVar[str | None] = ContextVar("component", default=None)


def set_request_id(request_id: str) -> None:
    """Set the request ID for the current async context."""
    _request_id_var.set(request_id)


def get_request_id() -> str | None:
    """Get the request ID for the current async context."""
    return _request_id_var.get()


def set_component(component: str) -> None:
    """Set the current component name (skill/agent/node)."""
    _component_var.set(component)


def get_component() -> str | None:
    """Get the current component name."""
    return _component_var.get()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STRUCTLOG PROCESSORS — Enrich every log entry
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def add_request_context(
    logger: Any, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Inject request_id and component into every log entry."""
    request_id = get_request_id()
    component = get_component()

    if request_id:
        event_dict["request_id"] = request_id
    if component:
        event_dict["component"] = component

    return event_dict


def add_error_context(
    logger: Any, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """
    If there's an exception, automatically extract and attach:
      - error_code (if it's a HumanTextError)
      - error_type (exception class name)
      - error_cause (the root cause)
      - recovery_hint
    """
    exc_info = event_dict.get("exc_info")
    if exc_info and exc_info is not True:
        # structlog passes the exception tuple or True
        if isinstance(exc_info, tuple) and len(exc_info) == 3:
            exc = exc_info[1]
        elif isinstance(exc_info, BaseException):
            exc = exc_info
        else:
            return event_dict

        event_dict["error_type"] = type(exc).__name__

        # Import here to avoid circular imports
        from app.utils.errors import HumanTextError

        if isinstance(exc, HumanTextError):
            event_dict["error_code"] = exc.error_code.value
            event_dict["error_context"] = exc.context
            if exc.recovery_hint:
                event_dict["recovery_hint"] = exc.recovery_hint
            if exc.cause:
                event_dict["root_cause"] = f"{type(exc.cause).__name__}: {exc.cause}"

    return event_dict


def add_app_info(
    logger: Any, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Add application metadata to every log entry."""
    event_dict["app"] = "humantext-engine"
    event_dict["version"] = "0.1.0"
    return event_dict


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SETUP — Configure structlog once at startup
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_configured = False


def setup_logging() -> None:
    """
    Configure structlog for the application.
    
    Call once at startup (in main.py or FastAPI lifespan).
    Supports two modes:
      - JSON: for production (machine-parseable, log aggregators)
      - CONSOLE: for development (rich, colorful, human-readable)
    """
    global _configured
    if _configured:
        return

    settings = get_settings()

    # Map our LogLevel enum to Python log levels
    level_map = {
        LogLevel.DEBUG: "DEBUG",
        LogLevel.INFO: "INFO",
        LogLevel.WARNING: "WARNING",
        LogLevel.ERROR: "ERROR",
        LogLevel.CRITICAL: "CRITICAL",
    }
    log_level = level_map.get(settings.LOG_LEVEL, "INFO")

    # Shared processors for both modes
    shared_processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        add_request_context,
        add_error_context,
        add_app_info,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    if settings.LOG_FORMAT == LogFormat.JSON:
        # Production: JSON output
        renderer = structlog.processors.JSONRenderer()
    else:
        # Development: Rich, colorful console output
        renderer = structlog.dev.ConsoleRenderer(
            colors=True,
            exception_formatter=structlog.dev.plain_traceback,
        )

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Also configure standard library logging to use structlog
    import logging

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level)

    # Quiet noisy third-party loggers
    for noisy in ["httpx", "httpcore", "openai", "anthropic", "urllib3", "asyncio"]:
        logging.getLogger(noisy).setLevel(logging.WARNING)

    _configured = True


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOGGER FACTORY — Get a named logger for any component
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Get a structured logger for a specific component.
    
    Args:
        name: Component name (e.g., "skill_02_document_analysis", "agent_rewriter",
              "graph_workflow", "api_humanize")
    
    Returns:
        A bound structlog logger that automatically includes the component name
        and request_id in every log entry.
    
    Example:
        logger = get_logger("skill_05_fact_extraction")
        logger.info("Extracted facts", fact_count=12, entities=["GPT-4", "OpenAI"])
        logger.warning("Low confidence extraction", confidence=0.65, threshold=0.80)
        logger.error("Extraction failed", error_code="HTE-2016", exc_info=True)
    """
    # Ensure logging is set up
    if not _configured:
        setup_logging()

    return structlog.get_logger(name)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PERFORMANCE TIMING — Measure and log execution time
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def log_execution_time(component_name: str) -> Callable:
    """
    Decorator that logs the execution time of a function/coroutine.
    
    Works with both sync and async functions.
    Logs start, success (with duration), and failure (with duration + error).
    
    Example:
        @log_execution_time("skill_03_semantic_analysis")
        async def analyze_semantics(text: str) -> SemanticResult:
            ...
        
        # Log output:
        # {"event": "Starting skill_03_semantic_analysis", "component": "skill_03_semantic_analysis"}
        # {"event": "Completed skill_03_semantic_analysis", "duration_ms": 1234.56, "status": "success"}
        # OR on failure:
        # {"event": "Failed skill_03_semantic_analysis", "duration_ms": 567.89, "status": "error", "error_type": "LLMTimeoutError"}
    """
    logger = get_logger(component_name)

    def decorator(func: Callable) -> Callable:
        import asyncio

        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                prev_component = get_component()
                set_component(component_name)

                logger.info(f"Starting {component_name}")
                start = time.perf_counter()

                try:
                    result = await func(*args, **kwargs)
                    duration_ms = (time.perf_counter() - start) * 1000
                    logger.info(
                        f"Completed {component_name}",
                        duration_ms=round(duration_ms, 2),
                        status="success",
                    )
                    return result
                except Exception as e:
                    duration_ms = (time.perf_counter() - start) * 1000
                    logger.error(
                        f"Failed {component_name}",
                        duration_ms=round(duration_ms, 2),
                        status="error",
                        error_type=type(e).__name__,
                        exc_info=e,
                    )
                    raise
                finally:
                    set_component(prev_component)

            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                prev_component = get_component()
                set_component(component_name)

                logger.info(f"Starting {component_name}")
                start = time.perf_counter()

                try:
                    result = func(*args, **kwargs)
                    duration_ms = (time.perf_counter() - start) * 1000
                    logger.info(
                        f"Completed {component_name}",
                        duration_ms=round(duration_ms, 2),
                        status="success",
                    )
                    return result
                except Exception as e:
                    duration_ms = (time.perf_counter() - start) * 1000
                    logger.error(
                        f"Failed {component_name}",
                        duration_ms=round(duration_ms, 2),
                        status="error",
                        error_type=type(e).__name__,
                        exc_info=e,
                    )
                    raise
                finally:
                    set_component(prev_component)

            return sync_wrapper

    return decorator


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PIPELINE TRACER — Track full request journey
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PipelineTracer:
    """
    Tracks the full journey of a request through the pipeline.
    
    Records each step with timing, status, and any errors.
    At the end, produces a complete execution trace for debugging.
    
    Usage:
        tracer = PipelineTracer(request_id="abc-123")
        
        tracer.start_step("input_validation")
        # ... do work ...
        tracer.end_step("input_validation", status="success")
        
        tracer.start_step("semantic_analysis")
        # ... error happens ...
        tracer.end_step("semantic_analysis", status="error", error="HTE-2011")
        
        # Get full trace
        trace = tracer.get_trace()
    """

    def __init__(self, request_id: str) -> None:
        self.request_id = request_id
        self.steps: list[dict[str, Any]] = []
        self.start_time = time.perf_counter()
        self._step_starts: dict[str, float] = {}
        self.logger = get_logger("pipeline_tracer")

    def start_step(self, step_name: str, **metadata: Any) -> None:
        """Record the start of a pipeline step."""
        self._step_starts[step_name] = time.perf_counter()
        self.logger.debug(
            f"Step started: {step_name}",
            step=step_name,
            request_id=self.request_id,
            **metadata,
        )

    def end_step(
        self,
        step_name: str,
        status: str = "success",
        error: str | None = None,
        **metadata: Any,
    ) -> None:
        """Record the completion of a pipeline step."""
        start = self._step_starts.pop(step_name, time.perf_counter())
        duration_ms = (time.perf_counter() - start) * 1000

        step_record = {
            "step": step_name,
            "status": status,
            "duration_ms": round(duration_ms, 2),
            **metadata,
        }
        if error:
            step_record["error"] = error

        self.steps.append(step_record)

        log_method = self.logger.info if status == "success" else self.logger.error
        log_method(
            f"Step completed: {step_name}",
            request_id=self.request_id,
            **step_record,
        )

    def get_trace(self) -> dict[str, Any]:
        """Get the complete execution trace."""
        total_duration_ms = (time.perf_counter() - self.start_time) * 1000
        return {
            "request_id": self.request_id,
            "total_duration_ms": round(total_duration_ms, 2),
            "step_count": len(self.steps),
            "failed_steps": [s for s in self.steps if s["status"] != "success"],
            "steps": self.steps,
        }

    def get_summary(self) -> str:
        """Get a one-line summary of the trace."""
        total_ms = (time.perf_counter() - self.start_time) * 1000
        failed = sum(1 for s in self.steps if s["status"] != "success")
        return (
            f"Pipeline[{self.request_id[:8]}]: "
            f"{len(self.steps)} steps, {failed} failed, "
            f"{total_ms:.0f}ms total"
        )
