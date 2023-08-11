import re

from lib.schemes.vim import Highlight

def custom_out(content: str, group2hl: dict[str, Highlight]):
    def get_hl(m: re.Match[str]) -> str:
        groups = m.groups()
        hl = group2hl.get(groups[0])
        if not hl:
            raise Exception(f'group {groups[0]} is not defined.')

        value = {
            'fg': hl.fg, 'bg': hl.bg, 'deco': hl.deco, 'ul': hl.ul
        }.get(groups[1])
        if not value:
            raise Exception(f'highlight for group {groups[0]} doesn\'t have any setting for value {groups[1]}.')

        return str(value)

    return re.sub(r'\{\{ ([a-zA-Z]+)\.(fg|bg|deco|ul) \}\}', get_hl, content)
