from typing import Literal
from lib.colors import color2str, ranked_matches, str2color

class Highlight:
    def __init__(self, fg: int | None, bg: int | None, deco: str | None, ul: int | None):
        self.fg = fg
        self.bg = bg
        self.deco = deco
        self.ul = ul

class Scheme:
    def __init__(self):
        # 256-color -> (dark-24bit, light-24bit)
        self.term2true: dict[int, tuple[int, int]] = dict()
        # and the other way around
        self._true2term: dict[tuple[int, int], int] = dict()
        # group/name/scope to hl reference
        self._group2hl: dict[str, Highlight] = dict()

    # load best remaining match OR already existing mapping for
    # dark/light 24-bit color to 256 color
    def _load_256(self, color_def: dict[str, str]) -> int:
        dl = (str2color(color_def['dark']), str2color(color_def['light']))
        if dl in self._true2term:
            i = self._true2term[dl]
        else:
            matches = ranked_matches(*dl)
            try:
                i = next(m for m in matches if not m in self.term2true)
            except:
                raise Exception('you can only use 256 colors in total')
            self.term2true[i] = dl
            self._true2term[dl] = i
        return i

    def _get(self, group: str) -> Highlight:
        try: return self._group2hl[group]
        except: raise Exception(f'The color "{group}" is not defined.')

    # get hl from existing or new group and save for future use
    def get_hl(self, source) -> Highlight:
        if type(source) is str:
            return self._get(source)

        hl = Highlight(
            self._load_256(source['fg']) if 'fg' in source else None,
            self._load_256(source['bg']) if 'bg' in source else None,
            source.get('deco'),
            self._load_256(source['ul']) if 'ul' in source else None,
        )

        group = source['set']
        if type(group) is list:
            for g in group:
                self._group2hl[g] = hl
        else: self._group2hl[group] = hl

        return hl
    
    # get Group.fg|bg|... as 256 or dark/light true color
    def from_str(self, id: str, true_color: Literal['dark'] | Literal['light'] | None = None) -> str:
        group = '.'.join(id.split('.')[:-1])
        hl = self._get(group)

        field = id.split('.')[-1] 
        value = {
            'fg': hl.fg, 'bg': hl.bg, 'deco': hl.deco, 'ul': hl.ul
        }.get(field)
        if not value:
            raise Exception(f'highlight for color {group} doesn\'t have any setting for value {field}.')

        # deco
        if type(value) is str: return value
        # translate to true dark/light
        if true_color == 'dark':
            return color2str(self.term2true[value][0])
        if true_color == 'light':
            return color2str(self.term2true[value][1])
        # 256 color
        return str(value)
