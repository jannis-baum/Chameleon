from lib.data import Highlight, Scheme
from lib.schemes.all import disclaimer

def _hl(hl: Highlight, group: str) -> str:
    return ' '.join([
        f'highlight {group}',
        f'ctermfg={hl.fg or "none"}',
        f'ctermbg={hl.bg or "none"}',
        f'cterm={hl.deco or "none"}',
        f'ctermul={hl.ul or "none"}',
    ])

def vim_out(vim_config: dict, scheme: Scheme) -> str:
    header = f'" {disclaimer}\n\n{vim_config.get("header") or ""}'

    content: list[str] = [header]
    for hl_def in vim_config['highlight']:
        hl = scheme.get_hl(hl_def)
        group = hl_def['set']
        if type(group) is list:
            for g in group:
                content.append(_hl(hl, g))
        else: content.append(_hl(hl, group))

    return '\n'.join(content)
