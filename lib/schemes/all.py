import os
import re
from typing import Literal

from lib.data import Scheme

disclaimer = 'GENERATED WITH https://github.com/jannis-baum/dynamic-term-colors'

def format_colordefs(text: str, scheme: Scheme, true_color: Literal['dark'] | Literal['light'] | None = None) -> str:
    def get_hl(m: re.Match[str]) -> str:
        id = m.groups()[0]
        return scheme.from_str(id, true_color)
    return re.sub(r'\{\{ ([^} ]+) \}\}', get_hl, text)

def save_to(dest: str, content: str):
    path = os.path.expanduser(dest)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as fp:
        fp.write(content)
