from lib.data import Highlight, Scheme
from lib.schemes.all import disclaimer, save_to

def _hl(hl: Highlight, group: str) -> str:
    return ' '.join([
        f'highlight {group}',
        f'ctermfg={hl.fg or "none"}',
        f'ctermbg={hl.bg or "none"}',
        f'cterm={hl.deco or "none"}',
        f'ctermul={hl.ul or "none"}',
    ])

def gen_vim(config: dict, scheme: Scheme):
    header = f'" {disclaimer}\n\n{config.get("header") or ""}'

    content: list[str] = [header]
    for hl_def in config['highlight']:
        hl = scheme.get_hl(hl_def)
        group = hl_def['set']
        if type(group) is list:
            for g in group:
                content.append(_hl(hl, g))
        else: content.append(_hl(hl, group))

    save_to(config['destination'], '\n'.join(content))
