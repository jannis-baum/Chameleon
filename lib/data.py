class Highlight:
    def __init__(self, fg: int | None, bg: int | None, deco: str | None, ul: int | None):
        self.fg = fg
        self.bg = bg
        self.deco = deco
        self.ul = ul

    def vim(self, group: str) -> str:
        return ' '.join([
            f'highlight {group}',
            f'ctermfg={self.fg or "none"}',
            f'ctermbg={self.bg or "none"}',
            f'cterm={self.deco or "none"}',
            f'ctermul={self.ul or "none"}',
        ])
