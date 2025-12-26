from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class ValidateConfig(BaseModel):
    """Configuration for Guardian validation features."""

    enable_content_filter: bool = False
    enable_pii_scanner: bool = False
    enable_toon_decoder: bool = False
    enable_hallucination_detector: bool = False
    enable_citation_verifier: bool = False
    enable_tone_checker: bool = False
    enable_refusal_detector: bool = False
    enable_disclaimer_injector: bool = False


class ValidateMetrics(BaseModel):
    """Detailed validation metrics/results."""

    hallucination_detected: Optional[bool] = None
    hallucination_details: Optional[str] = None
    citations_verified: Optional[bool] = None
    fake_citations: Optional[List[str]] = None
    tone_compliant: Optional[bool] = None
    tone_violation_reason: Optional[str] = None
    disclaimer_injected: Optional[bool] = None
    disclaimer_text: Optional[str] = None
    false_refusal_detected: Optional[bool] = None
    toxicity_score: Optional[float] = None
    toxicity_details: Optional[Dict[str, Any]] = None
    warnings_count: int = 0
    pii_leaks_count: int = 0
    moderation_mode: str = "moderate"


class ValidateRequest(BaseModel):
    """Request schema for /validate endpoint."""

    llm_response: str
    moderation_mode: str = "moderate"  # strict, moderate, relaxed, raw
    output_format: str = "json"  # json or toon
    guardrails: Optional[Dict[str, Any]] = None
    original_query: Optional[str] = None  # For hallucination check

    # Structured Config
    config: Optional[ValidateConfig] = ValidateConfig()


class ValidateResponse(BaseModel):
    """Response schema for /validate endpoint."""

    validated_response: Optional[str] = None
    validation_passed: bool

    # Basic blocking info (always needed at top level?)
    # Let's keep these top level for easy access, or move to a 'status' object?
    # User asked for "structured".
    # Let's keep critical status fields top level.
    content_blocked: bool = False
    content_block_reason: Optional[str] = None
    content_warnings: Optional[List[str]] = None

    output_pii_leaks: Optional[List[Dict[str, Any]]] = None
    output_redacted: bool = False
    was_toon: bool = False

    metrics: Optional[ValidateMetrics] = None
