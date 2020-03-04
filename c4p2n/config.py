from pydantic import (
    BaseSettings,
    SecretBytes,
)


class Config(BaseSettings):
    NOTION_TOKEN: str
    NOTION_SPEAKERS_VIEW_URL: str
    NOTION_TALKS_VIEW_URL: str
    WEBHOOK_SECRET: SecretBytes


config = Config()
