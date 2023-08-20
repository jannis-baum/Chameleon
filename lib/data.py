from typing import Literal
from lib.colors import color2str, ranked_matches, str2color

class Highlight:
    def __init__(self, fg: int | None, bg: int | None, deco: str | None, ul: int | None):
        self.fg = fg
        self.bg = bg
        self.deco = deco
        self.ul = ul

class Scheme:
    def __init__(self, initial_colors: dict, initial_hl: list):
        # 256-color -> (dark-24bit, light-24bit)
        self.term2true: dict[int, tuple[int, int]] = dict()
        # and the other way around
        self._true2term: dict[tuple[int, int], int] = dict()
        # named color to term
        self._name2term: dict[str, int] = dict()
        # group/name/scope to hl reference
        self._group2hl: dict[str, Highlight] = dict()

        for name, color in initial_colors.items():
            self._name2term[name] = self._load_256(color)
        for hl in initial_hl:
            _ = self.get_hl(hl)

    def _get_color(self, name: str) -> int:
        try: return self._name2term[name]
        except: raise Exception(f'The color "{name}" is not defined.')

    def _get_hl(self, group: str) -> Highlight:
        try: return self._group2hl[group]
        except: raise Exception(f'The highlight "{group}" is not defined.')

    # load best remaining match OR already existing mapping for
    # dark/light 24-bit color to 256 color
    def _load_256(self, color_def: dict[str, str] | str) -> int:
        if type(color_def) is str:
            return self._get_color(color_def)

        elif type(color_def) is dict:
            dl = (str2color(color_def['dark']), str2color(color_def['light']))
            if dl in self._true2term:
                i = self._true2term[dl]
            else:
                matches = ranked_matches(*dl)
                try:
                    i = next(m for m in matches if not m in self.term2true)
                except:
                    raise Exception('You can only use 256 colors in total')
                self.term2true[i] = dl
                self._true2term[dl] = i
            return i

        raise Exception('Incorrect color definition')

    # get hl from existing or new group and save for future use
    def get_hl(self, source: dict) -> Highlight:
        if 'from' in source:
            hl = self._get_hl(source['from'])
        else:
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
        if '.' not in id:
            value = self._get_color(id)
        else:
            group = '.'.join(id.split('.')[:-1])
            hl = self._get_hl(group)

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
