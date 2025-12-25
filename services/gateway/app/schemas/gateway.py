"""
Gateway request/response schemas.

Defines explicit typed schemas for the gateway API with model selection,
guardrails configuration, and detailed response metrics including token usage.
"""

from pydantic import BaseModel, Field
from typing import Optional


class SecuritySettings(BaseModel):
    """Unified security and validation settings."""

    # Privacy
    pii_masking: bool = Field(False, description="Enable PII detection/masking")

    # Input Security
    sanitize_input: bool = Field(False, description="Enable input sanitization")
    detect_threats: bool = Field(
        False, description="Enable threat detection (SQLi, XSS, etc)"
    )

    # Output Validation
    content_filter: bool = Field(False, description="Enable content toxicity filtering")
    hallucination_check: bool = Field(
        False, description="Enable hallucination detection"
    )
    citation_check: bool = Field(False, description="Enable citation verification")
    tone_check: bool = Field(False, description="Enable tone consistency check")

    # Advanced / Misc
    toon_mode: bool = Field(False, description="Enable TOON format conversion")
    enable_llm_forward: bool = Field(False, description="Enable LLM forwarding")


class GatewayRequest(BaseModel):
    """
    Enhanced gateway request with nested settings.
    """

    query: str = Field(..., description="User query/prompt to process")
    system_prompt: Optional[str] = Field(
        default="You are a helpful AI assistant.",
        description="System prompt to guide LLM behavior",
    )
    model: str = Field(
        default="gemini-3-flash-preview",
        description="LLM model to use",
    )
    moderation: str = Field(
        default="moderate",
        description="Content moderation level: strict, moderate, relaxed, or raw",
    )
    output_format: str = Field(
        default="json", description="Output format: json or toon"
    )
    max_output_tokens: Optional[int] = Field(
        default=None, description="Max tokens for LLM response"
    )

    settings: SecuritySettings = Field(
        default_factory=SecuritySettings, description="Security and validation settings"
    )


class TokenUsage(BaseModel):
    """LLM token usage metrics."""

    input_tokens: int = Field(..., description="Number of input tokens consumed")
    output_tokens: int = Field(..., description="Number of output tokens generated")
    total_tokens: int = Field(..., description="Total tokens (input + output)")


class ResponseMetrics(BaseModel):
    """Detailed response metrics."""

    security_score: float = Field(
        default=0.0, description="Security risk score (0.0 = safe, 1.0 = high risk)"
    )
    tokens_saved: int = Field(
        default=0, description="Tokens saved via TOON compression"
    )
    token_usage: Optional[TokenUsage] = Field(
        default=None, description="LLM token usage breakdown"
    )
    model_used: Optional[str] = Field(
        default=None, description="Actual LLM model used for response"
    )
    threats_detected: int = Field(
        default=0, description="Number of threats/injections detected"
    )
    pii_redacted: int = Field(
        default=0, description="Number of PII items detected and redacted"
    )
    processing_time_ms: Optional[float] = Field(
        default=None, description="Total processing time in milliseconds"
    )

    # NEW: Guardian validation results
    hallucination_detected: Optional[bool] = Field(
        default=None, description="Whether hallucination was detected in LLM response"
    )
    citations_verified: Optional[bool] = Field(
        default=None, description="Whether citations were verified as authentic"
    )
    tone_compliant: Optional[bool] = Field(
        default=None, description="Whether response matches the specified brand tone"
    )
    disclaimer_injected: Optional[bool] = Field(
        default=None, description="Whether a legal disclaimer was automatically added"
    )
    false_refusal_detected: Optional[bool] = Field(
        default=None, description="Whether LLM incorrectly refused a valid request"
    )
    toxicity_score: Optional[float] = Field(
        default=None, description="Toxicity score from 0.0 (safe) to 1.0 (toxic)"
    )


class GatewayResponse(BaseModel):
    """
    Enhanced gateway response with detailed metrics.

    Example:
        {
            "response": "Machine learning is...",
            "app": "my-app",
            "metrics": {
                "security_score": 0.1,
                "tokens_saved": 0,
                "token_usage": {
                    "input_tokens": 15,
                    "output_tokens": 150,
                    "total_tokens": 165
                },
                "model_used": "gemini-2.0-flash",
                "threats_detected": 0,
                "pii_redacted": 0
            }
        }
    """

    response: Optional[str] = Field(
        default=None, description="LLM response content (null if blocked)"
    )
    app: str = Field(..., description="Application name that made the request")
    metrics: ResponseMetrics = Field(..., description="Detailed processing metrics")
