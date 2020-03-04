from notion.client import NotionClient
from notion.collection import CollectionRowBlock

from c4p2n.models import CallForPaperPreparedRequest


class Notion:
    def __init__(self, token: str, speakers_view_link: str, talks_view_link: str):
        self._token = token
        self.client = NotionClient(token_v2=token)
        self.talks = self.client.get_collection_view(talks_view_link)
        self.speakers = self.client.get_collection_view(speakers_view_link)

    def create_speaker_block(
        self, call_for_paper_request: CallForPaperPreparedRequest
    ) -> CollectionRowBlock:
        speaker = self.speakers.collection.add_row()
        speaker.name = call_for_paper_request.name
        speaker.job = call_for_paper_request.job
        speaker.telegram = call_for_paper_request.telegram
        speaker.contact = call_for_paper_request.contact
        speaker.phone = call_for_paper_request.phone
        speaker.photo = [call_for_paper_request.photo_link]
        return speaker

    def create_talk_block(
        self,
        call_for_paper_request: CallForPaperPreparedRequest,
        speaker: CollectionRowBlock,
    ) -> CollectionRowBlock:
        talk = self.talks.collection.add_row()
        talk.name = call_for_paper_request.talk_title
        talk.description = call_for_paper_request.talk_description
        talk.date = call_for_paper_request.talk_dates
        talk.questions = call_for_paper_request.questions
        talk.speaker = speaker
        return talk

    def add_talk_info(
        self, call_for_paper_request: CallForPaperPreparedRequest
    ) -> None:
        # TODO: in ideal world we need to filter speaker by name first
        # blocking issue: https://github.com/jamalex/notion-py/issues/110
        speaker = self.create_speaker_block(call_for_paper_request)
        talk = self.create_talk_block(call_for_paper_request, speaker)
