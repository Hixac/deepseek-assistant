from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    COPY_BUTTON: Path
    EXPERT_BUTTON: Path
    INSTANT_BUTTON: Path
    MESSAGE_FIELD: Path
    SUBMIT_MESSAGE_BUTTON: Path

    model_config = SettingsConfigDict(
            env_file=Path(__file__).parent.parent.joinpath(".env"),
            env_file_encoding="utf-8",
            case_sensitive=True,
            extra="ignore",
    )

settings = Settings()
