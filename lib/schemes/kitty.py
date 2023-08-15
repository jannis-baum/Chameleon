import re

from lib.colors import color2str
from lib.data import Scheme
from lib.schemes.all import disclaimer, format_colordefs, save_to

def gen_kitty(config: dict, scheme: Scheme):
    header = f'# {disclaimer}\n\n{config.get("header") or ""}'
    headers = (
        format_colordefs(re.sub(r'(\S+)\|\|\|\S+', r'\1', header), scheme, 'dark'),
        format_colordefs(re.sub(r'\S+\|\|\|(\S+)', r'\1', header), scheme, 'light')
    )

    def mode(i: int) -> str:
        return '\n'.join([headers[i]] + [
            f'color{term} {color2str(true[i])}' for term, true in scheme.term2true.items()
        ])

    save_to(config['destinations']['dark'], mode(0))
    save_to(config['destinations']['light'], mode(1))
