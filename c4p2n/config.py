from pydantic import BaseSettings


class Config(BaseSettings):
    NOTION_TOKEN: str
    NOTION_LINK: str


config = Config()
