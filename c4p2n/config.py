from ppm_telegram_bot_client import ApiClient
from pydantic import (
    BaseSettings,
    SecretBytes,
    SecretStr,
)

client = ApiClient(
    host="https://fb2e38d3-14e7-40f3-95d8-a3f4f44e69cc.api.beta.kintohub.com/ppm-telegram-bot-sl"
)


class Config(BaseSettings):
    NOTION_TOKEN: SecretStr
    NOTION_SPEAKERS_VIEW_URL: str
    NOTION_TALKS_VIEW_URL: str
    WEBHOOK_SECRET: SecretBytes


config = Config()
