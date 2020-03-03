from typing import Dict, Any, List, Union


def get_answer_type(answer: Dict[str, Any]) -> str:
    return answer["type"]  # type: ignore  # will be fixed with #2


def field_ref(answer: Dict[str, Any]) -> str:
    return answer["field"]["ref"]  # type: ignore  # will be fixed with #2


def extract_text(text_answer: Dict[str, Any]) -> str:
    return text_answer["text"]  # type: ignore  # will be fixed with #2


def extract_choices(choices_answer: Dict[str, Any]) -> List[str]:
    return choices_answer["choices"]["labels"]  # type: ignore  # will be fixed with #2


answer_type_to_extractor = {"text": extract_text, "choices": extract_choices}


def extract_answer(answer: Dict[str, Any]) -> Union[str, List[str]]:
    answer_type = get_answer_type(answer)
    if answer_type == "text":
        return extract_text(answer)
    elif answer_type == "choices":
        return extract_choices(answer)
    else:
        raise TypeError(f"Unexpected answer type: {answer_type}")
