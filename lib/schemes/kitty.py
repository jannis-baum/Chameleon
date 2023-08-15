import re

from lib.colors import color2str
from lib.data import Scheme
from lib.schemes.all import disclaimer, format_colordefs

def kitty_out(kitty_config: dict, scheme: Scheme) -> tuple[str, str]:
    header = f'# {disclaimer}\n\n{kitty_config.get("header") or ""}'
    headers = (
        format_colordefs(re.sub(r'(\S+)\|\|\|\S+', r'\1', header), scheme),
        format_colordefs(re.sub(r'\S+\|\|\|(\S+)', r'\1', header), scheme)
    )

    def mode(i: int) -> str:
        return '\n'.join([headers[i]] + [
            f'color{term} {color2str(true[i])}' for term, true in scheme.term2true.items()
        ])

    return (mode(0), mode(1))
