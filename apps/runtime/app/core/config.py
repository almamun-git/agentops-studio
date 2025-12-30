from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Filled in later (db url, redis url, llm keys, etc.)
    env: str = "local"


settings = Settings()


