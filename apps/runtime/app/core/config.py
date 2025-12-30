from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Environment
    env: str = "local"
    runtime_port: int = 8000

    # Database
    database_url: str = "postgresql://agentops:agentops@localhost:5432/agentops"

    # Redis
    redis_url: str = "redis://localhost:6379"

    # LLM Provider (to be configured)
    # openai_api_key: str | None = None
    # anthropic_api_key: str | None = None


settings = Settings()


