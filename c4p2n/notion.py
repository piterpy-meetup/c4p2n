from typing import Any, Dict

from notion.client import NotionClient


class Notion:
    def __init__(self, token: str, db_link: str):
        self._token = token
        self.client = NotionClient(token_v2=token)
        self.db_link = db_link
        self._talks_collection_view = self.client.get_collection_view(db_link)
        self.talks_collection = self._talks_collection_view.collection

    def add_talk_info(self, data: Dict[str, Any]) -> None:
        row = self.talks_collection.add_row()
        row.name = data.get("name", "")
        row.job = data.get("job", "")
        if photo_link := data.get("photo_link"):
            row.photo = [photo_link]
        row.talk_title = data.get("talk_title", "")
        row.talk_description = data.get("talk_description", "")
        row.talk_date = ", ".join(data.get("talk_date", []))
        row.telegram = data.get("telegram", "")
        row.contact = data.get("contact", "")
        row.questions = data.get("questions", "")
