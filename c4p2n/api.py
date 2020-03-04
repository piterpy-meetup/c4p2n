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
notion = Notion(
    token=config.NOTION_TOKEN.get_secret_value(),
    speakers_view_link=config.NOTION_SPEAKERS_VIEW_URL,
    talks_view_link=config.NOTION_TALKS_VIEW_URL,
)
signature_header_security = SignatureHeader(
    secret=config.WEBHOOK_SECRET.get_secret_value()
)


@app.get("/")
def health_check() -> Dict[str, str]:
    return {"notion_user": notion.client.current_user.full_name}


@app.post("/call_for_paper", dependencies=[Depends(signature_header_security)])
def call_for_paper_webhook(request: CallForPaperRequest,) -> Dict[str, Any]:
    try:
        prepared_request = request.prepare()
    except ValidationError:
        raise HTTPException(status_code=422, detail={"error": "invalid_form"})
    try:
        notion.add_talk_info(prepared_request)
    except Exception:
        raise HTTPException(
            status_code=500, detail={"error": "notion_error"},
        )
    return {"success": True}
