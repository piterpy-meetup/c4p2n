from datetime import datetime
from typing import Dict, Any, List, Union

from pydantic import BaseModel, Field

from c4p2n.constants import C4P_FIELDS
from c4p2n.extractors import field_ref, extract_answer


class BaseWebhookRequest(BaseModel):
    event_id: str
    event_type: str
    form_response: Dict[str, Any]


class BaseFormResponse(BaseModel):
    form_id: str
    token: str
    landed_at: datetime
    submitted_at: datetime
    definition: Dict[str, Any]
    answers: List[Dict[str, Any]]


class BaseField(BaseModel):
    id: str
    type: str
    ref: str


class DefinitionField(BaseField):
    title: str
    properties: Dict[str, Any]


class BaseDefinition(BaseModel):
    id: str
    title: str
    _fields: List[Any] = Field(None, alias="fields")


class TextDefinitionField(DefinitionField):
    pass


class Choice(BaseModel):
    id: str
    label: str


class MultipleChoiceDefinitionField(DefinitionField):
    allow_multiple_selections: bool
    allow_other_choice: bool
    choices: List[Choice]


CallForPaperDefinitionFields = Union[
    TextDefinitionField,
]


class CallForPaperDefinition(BaseDefinition):
    _fields: List[CallForPaperDefinitionFields] = Field(None, alias="fields")


class BaseAnswer(BaseModel):
    type: str
    field: BaseField


class TextAnswer(BaseAnswer):
    text: str


class Choices(BaseModel):
    labels: List[str]


class MultipleChoiceAnswer(BaseAnswer):
    choices: Choices


CallForPaperAnswer = Union[TextAnswer, MultipleChoiceAnswer]


class CallForPaperFormResponse(BaseFormResponse):
    definition: CallForPaperDefinition
    answers: List[CallForPaperAnswer]


class CallForPaperRequest(BaseWebhookRequest):
    form_response: CallForPaperFormResponse

    def extract_answers(self):
        answers = {
            field_ref(answer.dict()): extract_answer(answer.dict())
            for answer in self.form_response.answers
        }
        return {key: value for key, value in answers.items() if key in C4P_FIELDS}
