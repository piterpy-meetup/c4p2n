from typing import Dict, Any, List, Union


def get_answer_type(answer: Dict[str, Any]) -> str:
    return answer["type"]


def field_ref(answer: Dict[str, Any]) -> str:
    return answer["field"]["ref"]


def extract_text(text_answer: Dict[str, Any]) -> str:
    return text_answer["text"]


def extract_choices(choices_answer: Dict[str, Any]) -> List[str]:
    return choices_answer["choices"]["labels"]


answer_type_to_extractor = {"text": extract_text, "choices": extract_choices}


def extract_answer(answer: Dict[str, Any]) -> Union[str, List[str]]:
    answer_type = get_answer_type(answer)
    extractor = answer_type_to_extractor[answer_type]
    return extractor(answer)
