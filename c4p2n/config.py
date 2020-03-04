from pydantic import (
    BaseSettings,
    SecretBytes,
    SecretStr,
)


class Config(BaseSettings):
    NOTION_TOKEN: SecretStr
    NOTION_SPEAKERS_VIEW_URL: str
    NOTION_TALKS_VIEW_URL: str
    WEBHOOK_SECRET: SecretBytes


config = Config()
