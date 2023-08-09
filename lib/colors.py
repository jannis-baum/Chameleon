import os

def rgb_from(color: int) -> tuple[int, int, int]:
    return (
        color >> 16,
        (color >> 8) & 0x00ff,
        color & 0x0000ff
    )

# adjusted from kitty/colors.c
def color_at(i: int) -> int:
    if i < 16: raise Exception('first 16 colors are usually customized') 
    valuerange = [0x00, 0x5f, 0x87, 0xaf, 0xd7, 0xff];
    if (i < 232):
        color = i - 16;
        r = valuerange[int(color / 36) % 6]
        g = valuerange[int(color / 6) % 6]
        b = valuerange[color % 6];
        return (r << 16) | (g << 8) | b;
    else:
        gray = i - 232;
        v = 8 + gray * 10;
        return (v << 16) | (v << 8) | v;

def ranked_matches(*colors: int) -> list[int]:
    rgbs = [rgb_from(c) for c in colors]
    def diff_to(color: int):
        rgb = rgb_from(color)
        return sum(((rgb[0] - r)**2 + (rgb[1] - g)**2 + (rgb[2] - b)**2)**2 for r, g, b in rgbs)

    diffs = [(i, diff_to(color_at(i))) for i in range(16, 256)]
    diffs.sort(key=lambda d: d[1], reverse=True)
    return [i for i, _ in diffs]

def color2str(color: int) -> str: return hex(color).replace('0x', '#')

def str2color(s: str) -> int:
    s = s.replace('#', '')
    full = None
    if len(s) == 1: full = s * 6
    if len(s) == 2: full = s * 3
    if len(s) == 3: full = s[0] * 2 + s[1] * 2 + s[2] * 2
    if len(s) == 6: full = s
    if not full: raise Exception('hex colors can only be 1, 2, 3 or 6 digits')
    return int(full, 16)

def ansi_color(color: int, text: str | None = None) -> str:
    content = text or color2str(color)

    term = os.getenv('COLORTERM')
    truecolor = bool(term and (term == 'truecolor' or term == '24bit'))
    if not truecolor: return content

    r, g, b = rgb_from(color)
    foreground = 30 if (r+g+b > 382) else 37
    return f'\033[{foreground};48;2;{r};{g};{b}m   {content}   \033[0m'
