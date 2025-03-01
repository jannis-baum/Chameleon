from lib.data import Highlight, Scheme
from lib.schemes.all import disclaimer, save_to

def _hl(hl: Highlight, group: str) -> str:
    return ' '.join([
        f'highlight {group}',
        f'ctermfg={hl.fg or "none"}',
        f'ctermbg={hl.bg or "none"}',
        f'cterm={hl.deco or "none"}',
        # nvim doesn't support ctermul, only guisp, but guisp only supports
        # true colors, not terminal colors, so we can't use it
        # https://github.com/neovim/neovim/issues/23025#issuecomment-2450467152
        # https://github.com/neovim/neovim/issues/8583#issuecomment-2450472808
        # f'ctermul={hl.ul or "none"}',
    ])

def gen_nvim(config: dict, scheme: Scheme):
    destination = config.get('destination_nvim')
    if not destination:
        return
    header = f'" {disclaimer}\n\n{config.get("header_nvim") or ""}'

    content: list[str] = [header]
    for hl_def in config['highlight']:
        hl = scheme.get_hl(hl_def)
        group = hl_def['set']
        if type(group) is list:
            for g in group:
                content.append(_hl(hl, g))
        else: content.append(_hl(hl, group))

    save_to(destination, '\n'.join(content))
