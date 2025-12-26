from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "Clestiq Shield - Sentinel (Input Security)"
    VERSION: str = "1.0.0"

    # Datadog APM
    TELEMETRY_ENABLED: bool = True
    DD_SERVICE: str = "clestiq-shield-sentinel"
    DD_ENV: str = "production"
    DD_VERSION: str = "1.0.0"

    # Gemini AI Studio
    GEMINI_API_KEY: str

    # Security Settings (defaults to False - opt-in via request body)
    SECURITY_SANITIZATION_ENABLED: bool = False
    SECURITY_PII_REDACTION_ENABLED: bool = False
    SECURITY_XSS_PROTECTION_ENABLED: bool = False
    SECURITY_SQL_INJECTION_DETECTION_ENABLED: bool = False
    SECURITY_COMMAND_INJECTION_DETECTION_ENABLED: bool = False

    # TOON Conversion Settings (default False - opt-in via request body)
    TOON_CONVERSION_ENABLED: bool = False

    # LLM Settings (default False - opt-in via request body)
    LLM_FORWARD_ENABLED: bool = False
    LLM_MODEL_NAME: str = "gemini-3-flash-preview"
    LLM_MAX_TOKENS: int = 8192

    # Guardian Service (Output Validation)
    GUARDIAN_SERVICE_URL: str = "http://guardian:8002"

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
