from fastapi import FastAPI

from c4p2n.config import config
from c4p2n.models import CallForPaperRequest
from c4p2n.notion import Notion

app = FastAPI()
notion = Notion(token=config.NOTION_TOKEN, db_link=config.NOTION_LINK)


@app.post("/call_for_paper")
def call_for_paper_webhook(request: CallForPaperRequest):
    answers = request.extract_answers()
    notion.add_talk_info(answers)
    return {"success": True}
