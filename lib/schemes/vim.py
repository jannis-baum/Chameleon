from lib.data import Highlight
from lib.schemes.all import disclaimer

def vim_out(header: str | None, group2hl: dict[str, Highlight]) -> str:
    header = f'" {disclaimer}\n\n{header or ""}'
    return '\n'.join([header] + [
        hl.vim(group) for group, hl in group2hl.items()
    ])
