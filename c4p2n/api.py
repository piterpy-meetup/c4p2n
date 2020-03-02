from fastapi import Depends, FastAPI

from fastapi_security_typeform import SignatureHeader

from c4p2n.config import config
from c4p2n.models import CallForPaperRequest
from c4p2n.notion import Notion

app = FastAPI()
notion = Notion(token=config.NOTION_TOKEN, db_link=config.NOTION_LINK)
signature_header_security = SignatureHeader(secret=config.WEBHOOK_SECRET.get_secret_value())


@app.post("/call_for_paper")
def call_for_paper_webhook(request: CallForPaperRequest, signature=Depends(signature_header_security)):
    answers = request.extract_answers()
    notion.add_talk_info(answers)
    return {"success": True}
