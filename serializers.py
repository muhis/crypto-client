from enum import Enum
from typing import List

def enum_to_choices(obj: Enum) -> List[tuple[str, str]]:
    choices: List[tuple[str, str]] = []
    for content in obj._member_map_.values():
        resulting_tuple: tuple[str, str] = (content.value, content.value.title())
        choices.append(resulting_tuple)
    return choices