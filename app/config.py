from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    secret_token: str
    access_token_ttl: int
    refresh_token_ttl: int
    algorithm: str


settings = Settings()  # pyright: ignore[reportCallIssue]
