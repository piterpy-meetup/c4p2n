from pydantic import (
    BaseSettings,
    SecretBytes,
)


class Config(BaseSettings):
    NOTION_TOKEN: str
    NOTION_LINK: str
    WEBHOOK_SECRET: SecretBytes


config = Config()
