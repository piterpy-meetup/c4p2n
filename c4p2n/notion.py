from notion.client import NotionClient

from c4p2n.models import CallForPaperAnswers


class Notion:
    def __init__(self, token: str, db_link: str):
        self._token = token
        self.client = NotionClient(token_v2=token)
        self.db_link = db_link
        self._talks_collection_view = self.client.get_collection_view(db_link)
        self.talks_collection = self._talks_collection_view.collection

    def add_talk_info(self, answers: CallForPaperAnswers) -> None:
        row = self.talks_collection.add_row()
        row.name = answers.name
        row.job = answers.job
        row.photo = [answers.photo_link]
        row.talk_title = answers.talk_title
        row.talk_description = answers.talk_description
        row.talk_date = answers.talk_dates()
        row.telegram = answers.telegram
        row.contact = answers.contact
        row.phone = answers.phone
        row.questions = answers.questions
