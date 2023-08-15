import plistlib as pl
import uuid

from lib.data import Highlight, Scheme
from lib.schemes.all import save_to

def _colstr(color256: int | None = None) -> str:
    if not color256: return '#00000000'
    return f'{color256:#04x}000000'.replace('0x', '#')

def _hl(hl: Highlight, scopes: str | list[str]) -> dict:
    settings = dict()
    if hl.fg: settings['foreground'] = _colstr(hl.fg)
    if hl.bg: settings['background'] = _colstr(hl.bg)
    if hl.deco: settings['fontStyle'] = hl.deco
    return {
        'scopes': scopes if type(scopes) is list else [scopes],
        'settings': settings
    }

def gen_tm(config: dict, scheme: Scheme):
    glob_defs = config.get('global', {})
    out = {
        'author': config['author'],
        'name': config['name'],
        'colorSpaceName': 'sRGB',
        'uuid': str(uuid.uuid4()),
        'settings': [{ 'settings': {
            key: _colstr(int(scheme.from_str(glob_defs[key])) if key in glob_defs else None)
            for key in ['foreground', 'background', 'caret', 'invisibles', 'lineHighlight', 'selection']
         } }]
    }

    if 'highlight' in config:
        for hl_def in config['highlight']:
            hl = scheme.get_hl(hl_def)
            out['settings'].append(_hl(hl, hl_def['set']))

    save_to(config['destination'], pl.dumps(out).decode())
