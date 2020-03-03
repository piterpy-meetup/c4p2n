from datetime import datetime
from typing import Dict, Any, List, Union

from pydantic import BaseModel, Field

from c4p2n.constants import C4P_FIELDS
from c4p2n.extractors import field_ref, extract_answer


class BaseField(BaseModel):
    id: str
    type: str
    ref: str


class DefinitionField(BaseField):
    title: str
    properties: Dict[str, Any]


class CallForPaperDefinition(BaseModel):
    """
    Definition of Typeform form: id, name, fields.
    """

    id: str
    title: str
    _fields: List[DefinitionField] = Field(None, alias="fields")


class BaseAnswer(BaseModel):
    """
    Each answer contains answer itself and information about question field.
    """

    type: str
    field: BaseField


class TextAnswer(BaseAnswer):
    text: str


class Choices(BaseModel):
    labels: List[str]


class MultipleChoiceAnswer(BaseAnswer):
    choices: Choices


class CallForPaperFormResponse(BaseModel):
    """
    Data with specific Typeform form answer.
    """

    form_id: str
    token: str
    landed_at: datetime
    submitted_at: datetime
    definition: CallForPaperDefinition
    answers: List[Union[TextAnswer, MultipleChoiceAnswer]]


class CallForPaperRequest(BaseModel):
    """
    Typeform request format which we expects in our webhook.
    """

    event_id: str
    event_type: str
    form_response: CallForPaperFormResponse

    def extract_answers(self) -> Dict[str, Any]:
        answers = {
            field_ref(answer.dict()): extract_answer(answer.dict())
            for answer in self.form_response.answers
        }
        return {key: value for key, value in answers.items() if key in C4P_FIELDS}
