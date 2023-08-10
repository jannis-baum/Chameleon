import plistlib as pl
import uuid

from lib.data import Highlight

def tm_colorstring(color256: int | None = None) -> str:
    if not color256: return '#00000000'
    return f'{color256:#04x}000000'.replace('0x', '#')

def tm_settings(hl: Highlight) -> dict:
    d = dict()
    if hl.fg: d['foreground'] = tm_colorstring(hl.fg)
    if hl.bg: d['background'] = tm_colorstring(hl.bg)
    if hl.deco: d['fontStyle'] = hl.deco
    return d

def tm_out(tm_config: dict, group2hl: dict[str, Highlight]) -> str:

    def get_hl(group: str) -> Highlight:
        try: return group2hl[group]
        except: raise Exception(f'The group "{group}" is not defined.')

    def global_settings() -> dict:
        # map 'no color' for everything initially
        settings = { key: tm_colorstring() for key in
            ['foreground', 'background', 'caret', 'invisibles', 'lineHighlight', 'selection']
        }
        if 'global' not in tm_config: return {'settings': settings }
        defs = tm_config['global']
        if 'fg' in defs: settings['foreground'] = tm_colorstring(get_hl(defs['fg']).fg)
        if 'bg' in defs: settings['background'] = tm_colorstring(get_hl(defs['bg']).bg)
        if 'caret' in defs: settings['caret'] = tm_colorstring(get_hl(defs['caret']).bg)
        if 'invisibles' in defs: settings['invisibles'] = tm_colorstring(get_hl(defs['invisibles']).fg)
        if 'line-hl' in defs: settings['lineHighlight'] = tm_colorstring(get_hl(defs['line-hl']).bg)
        if 'selection' in defs: settings['selection'] = tm_colorstring(get_hl(defs['selection']).bg)
        return { 'settings': settings }

    out = {
        'author': tm_config['author'],
        'name': tm_config['name'],
        'colorSpaceName': 'sRGB',
        'uuid': str(uuid.uuid4()),
        'settings': [global_settings()]
    }

    if 'groups' in tm_config:
        out['settings'] += [
                { 'scope': ', '.join(gdef['scopes']), 'settings': tm_settings(get_hl(gdef['vim'])) }
        for gdef in tm_config['groups']]

    return pl.dumps(out).decode()
