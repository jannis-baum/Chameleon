import re

from lib.colors import color2str
from lib.schemes.all import disclaimer

def kitty_out(header: str | None, term2true: dict[int, tuple[int, int]]) -> tuple[str, str]:
    header = f'# {disclaimer}\n\n{header or ""}'
    headers = (
        re.sub(r'(\S+)\|\|\|\S+', r'\1', header),
        re.sub(r'\S+\|\|\|(\S+)', r'\1', header)
    )

    def mode(i: int) -> str:
        return '\n'.join([headers[i]] + [
            f'color{term} {color2str(true[i])}' for term, true in term2true.items()
        ])

    return (mode(0), mode(1))
