from typing import (
    Dict,
    Any,
)

from fastapi import Depends, FastAPI, HTTPException
from fastapi_security_typeform import SignatureHeader
from pydantic import ValidationError

from c4p2n.config import config
from c4p2n.models import CallForPaperRequest
from c4p2n.notion import Notion

app = FastAPI()
notion = Notion(token=config.NOTION_TOKEN, db_link=config.NOTION_LINK)
signature_header_security = SignatureHeader(
    secret=config.WEBHOOK_SECRET.get_secret_value()
)


@app.get("/")
def health_check() -> Dict[str, str]:
    return {"notion_user": notion.client.current_user.full_name}


@app.post("/call_for_paper", dependencies=[Depends(signature_header_security)])
def call_for_paper_webhook(request: CallForPaperRequest,) -> Dict[str, Any]:
    try:
        answers = request.extract_answers()
    except ValidationError:
        raise HTTPException(status_code=422, detail={"error": "invalid_form"})
    try:
        notion.add_talk_info(answers)
    except Exception:
        raise HTTPException(
            status_code=500, detail={"error": "notion_error"},
        )
    return {"success": True}
