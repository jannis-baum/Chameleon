import re

from lib.data import Scheme

disclaimer = 'GENERATED WITH https://github.com/jannis-baum/dynamic-term-colors'

def format_colordefs(text: str, scheme: Scheme) -> str:
    def get_hl(m: re.Match[str]) -> str:
        id = m.groups()[0]
        return scheme.from_str(id)
    return re.sub(r'\{\{ ([^} ]+) \}\}', get_hl, text)
