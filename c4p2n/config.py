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
    PPM_TELEGRAM_BOT_API_URL: str


config = Config()
