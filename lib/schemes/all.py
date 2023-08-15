import re
from typing import Literal

from lib.data import Scheme

disclaimer = 'GENERATED WITH https://github.com/jannis-baum/dynamic-term-colors'

def format_colordefs(text: str, scheme: Scheme, true_color: Literal['dark'] | Literal['light'] | None = None) -> str:
    def get_hl(m: re.Match[str]) -> str:
        id = m.groups()[0]
        return scheme.from_str(id, true_color)
    return re.sub(r'\{\{ ([^} ]+) \}\}', get_hl, text)
