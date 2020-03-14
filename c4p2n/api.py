from typing import (
    Dict,
    Any,
)

from fastapi import Depends, FastAPI, HTTPException
from fastapi_security_typeform import SignatureHeader
from ppm_telegram_bot_client.models import TalkInfo
from pydantic import ValidationError
from fastapi import BackgroundTasks, FastAPI
from starlette.responses import JSONResponse

from c4p2n.config import config
from c4p2n.models import CallForPaperRequest
from c4p2n.notion import Notion
from c4p2n.telegram import telegram_api

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
async def call_for_paper_webhook(
    request: CallForPaperRequest, background_tasks: BackgroundTasks
) -> JSONResponse:
    try:
        prepared_request = request.prepare()
    except ValidationError:
        background_tasks.add_task(telegram_api.triggers_api.typeform_invalid)
        return JSONResponse(status_code=422, content={"error": "invalid_form"})

    try:
        talk_url = notion.add_talk_info(prepared_request)
    except Exception:
        background_tasks.add_task(telegram_api.triggers_api.notion_error)
        return JSONResponse(status_code=500, content={"error": "notion_error"},)

    background_tasks.add_task(
        telegram_api.triggers_api.talk_new,
        TalkInfo(
            speaker_name=prepared_request.name,
            talk_name=prepared_request.talk_title,
            talk_dates=prepared_request.talk_dates,
            notion_url=talk_url,
        ),
    )
    return JSONResponse(content={"success": True})
