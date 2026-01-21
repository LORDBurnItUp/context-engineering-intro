"""Application settings and configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )

    # API Keys
    anthropic_api_key: str
    openai_api_key: str

    # LiveKit Configuration
    livekit_url: str = "ws://localhost:7880"
    livekit_api_key: str
    livekit_api_secret: str

    # TTS Providers
    elevenlabs_api_key: Optional[str] = None

    # STT Providers
    deepgram_api_key: Optional[str] = None

    # Database Configuration
    database_url: str = "postgresql://user:password@localhost:5432/callcenter"
    redis_url: str = "redis://localhost:6379/0"

    # Vector Database
    chroma_host: str = "localhost"
    chroma_port: int = 8000
    qdrant_url: Optional[str] = None
    qdrant_api_key: Optional[str] = None

    # Email Configuration
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str
    smtp_password: str
    smtp_from_email: str
    smtp_from_name: str = "AI Call Center"

    # Application Settings
    app_name: str = "AI Call Center Army"
    app_version: str = "0.1.0"
    debug: bool = False
    log_level: str = "INFO"
    environment: str = "development"

    # Security
    secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    # Performance Tuning
    max_concurrent_calls: int = 10
    token_cache_size: int = 1000
    rag_top_k: int = 5
    rag_similarity_threshold: float = 0.7

    # Self-Improvement
    enable_learning: bool = True
    min_calls_for_learning: int = 10
    prompt_version: str = "1.0.0"

    # Monitoring
    enable_analytics: bool = True
    call_recording_enabled: bool = True
    call_recording_path: str = "/data/recordings"

    # Industry-Specific
    default_industry: str = "hvac"  # hvac, roofing, solar
    default_role: str = "support"  # support, troubleshoot, sales, cold_call

    # CRM Integration
    crm_webhook_url: Optional[str] = None
    crm_api_key: Optional[str] = None

    # Deployment
    hostinger_ssh_host: Optional[str] = None
    hostinger_ssh_user: Optional[str] = None
    hostinger_domain: Optional[str] = None


# Global settings instance
settings = Settings()
