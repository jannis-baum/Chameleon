from lib.data import Highlight
from lib.schemes.all import disclaimer

def vim_hl(hl: Highlight, group: str) -> str:
    return ' '.join([
        f'highlight {group}',
        f'ctermfg={hl.fg or "none"}',
        f'ctermbg={hl.bg or "none"}',
        f'cterm={hl.deco or "none"}',
        f'ctermul={hl.ul or "none"}',
    ])

def vim_out(header: str | None, group2hl: dict[str, Highlight]) -> str:
    header = f'" {disclaimer}\n\n{header or ""}'
    return '\n'.join([header] + [
        vim_hl(hl, group) for group, hl in group2hl.items()
    ])
