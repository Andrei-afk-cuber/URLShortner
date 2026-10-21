from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field, model_validator, Field, PostgresDsn, TypeAdapter

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"

# Settings base
class SettingsBase(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False, env_file=ENV_FILE)


# DBSettings model
class DBSettings(SettingsBase):
    host: str = Field(alias="DB_HOST")
    port: int = Field(alias="DB_PORT")
    user: str = Field(alias="DB_USER")
    password: str = Field(alias="DB_PASSWORD")
    database: str = Field(alias="DB_NAME")

    # compute db url
    @computed_field
    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


    # validate model
    @model_validator(mode="after")
    def check_url(self):
        PostgresDsn(url=self.url)
        return self

settings = DBSettings()

print(settings)