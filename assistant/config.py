from pathlib import Path

from pydantic import FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    COPY_BUTTON: FilePath
    EXPERT_BUTTON: FilePath
    INSTANT_BUTTON: FilePath
    MESSAGE_FIELD: FilePath
    SUBMIT_MESSAGE_BUTTON: FilePath

    HOST: str = "0.0.0.0"
    PORT: int = 12345

    model_config = SettingsConfigDict(
            env_file=Path(__file__).parent.parent.joinpath(".env"),
            env_file_encoding="utf-8",
            case_sensitive=True,
            extra="ignore",
    )

settings = Settings()
