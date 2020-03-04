from abc import abstractmethod
from datetime import datetime
from functools import wraps
from typing import Dict, Any, List, Union

from pydantic import BaseModel, Field, validator


@wraps(Field)
def EmptyStringField(**kwargs: Any) -> Any:
    """
    Replacement for an ugly Field("") call.
    """
    return Field("", **kwargs)


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
    _fields: List[DefinitionField] = Field(..., alias="fields")


class BaseAnswer(BaseModel):
    """
    Each answer contains answer itself and information about question field.
    """

    type: str
    field: BaseField

    @abstractmethod
    def extract(self) -> Any:
        raise NotImplementedError

    @property
    def ref(self) -> str:
        return self.field.ref


class TextAnswer(BaseAnswer):
    text: str

    def extract(self) -> str:
        return self.text


class Choices(BaseModel):
    labels: List[str]


class MultipleChoiceAnswer(BaseAnswer):
    choices: Choices

    def extract(self) -> List[str]:
        return self.choices.labels


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


class CallForPaperPreparedRequest(BaseModel):
    name: str
    job: str
    photo_link: str
    talk_date: List[str]
    telegram: str = EmptyStringField()
    contact: str = EmptyStringField()
    phone: str
    talk_title: str = EmptyStringField()
    talk_description: str
    questions: str = EmptyStringField()

    @property
    def talk_dates(self) -> str:
        return ", ".join(self.talk_date)

    @validator("telegram", always=True)
    def prepare_telegram(cls, v: str) -> str:
        return v.strip("@").lower()


class CallForPaperRequest(BaseModel):
    """
    Typeform request format which we expects in our webhook.
    """

    event_id: str
    event_type: str
    form_response: CallForPaperFormResponse

    def prepare(self) -> CallForPaperPreparedRequest:
        answers_dict = {
            answer.ref: answer.extract() for answer in self.form_response.answers
        }
        return CallForPaperPreparedRequest(**answers_dict)
