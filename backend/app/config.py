import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App Settings
    APP_NAME: str = "FreshRoute AI - Voice BI Agent"
    ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Database
    DATABASE_URL: str = "sqlite:///./backend/data/freshroute.db"
    SQL_QUERY_TIMEOUT_SECONDS: int = 10
    SQL_MAX_ROW_LIMIT: int = 500

    # Gnani.ai Models & Credentials (Vachana Platform)
    GNANI_API_KEY: Optional[str] = None
    GNANI_PRISMA_ENDPOINT: str = "https://api.vachana.ai/stt/v3"  # STT: Prisma v2.5 / v3
    GNANI_TIMBRE_ENDPOINT: str = "https://api.vachana.ai/api/v1/tts/inference"  # TTS: Timbre v2.5
    GNANI_EVON_ENDPOINT: Optional[str] = None    # LLM: Evon v3.3
    GNANI_STT_MODEL: str = "gnani-prisma-v2.5"
    GNANI_TTS_MODEL: str = "timbre-v2.5"
    GNANI_LLM_MODEL: str = "evon-v3.3"
    
    # Secondary / Cloud LLM Providers (Multi-Key Rotation & Free Tier Support)
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.5-flash"
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o"
    
    # External Web & Weather Providers (100% Free - No Credit Card Needed)
    TAVILY_API_KEY: Optional[str] = None
    OPEN_METEO_BASE_URL: str = "https://archive-api.open-meteo.com/v1/archive"
    
    # Agent Guardrails
    MAX_INVESTIGATION_STEPS: int = 8
    AGENT_TIMEOUT_SECONDS: int = 45

settings = Settings()
