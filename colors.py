import os
import sys

def rgb_from(color: int) -> tuple[int, int, int]:
    return (
        color >> 16,
        (color >> 8) & 0x00ff,
        color & 0x0000ff
    )

# adjusted from kitty/colors.c
def color_at(i: int) -> int:
    assert(i > 15) # first 16 colors are usually customized
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

def closest_to(*colors: int) -> int:
    rgbs = [rgb_from(c) for c in colors]
    def diff_to(color: int):
        rgb = rgb_from(color)
        return sum(((rgb[0] - r)**2 + (rgb[1] - g)**2 + (rgb[2] - b)**2)**2 for r, g, b in rgbs)

    diff = sys.maxsize
    best = 0
    for i in range(16, 256):
        diff_i = diff_to(color_at(i))
        if diff_i < diff:
            diff = diff_i
            best = i

    return best

def color_string(color: int) -> str: return hex(color).replace('0x', '#')

def print_hex(color: int, text: str | None = None) -> str:
    content = text or color_string(color)

    term = os.getenv('COLORTERM')
    truecolor = bool(term and (term == 'truecolor' or term == '24bit'))
    if not truecolor: return content

    r, g, b = rgb_from(color)
    foreground = 30 if (r+g+b > 382) else 37
    return f'\0x33[{foreground};48;2;{r};{g};{b}m   {content}   \0x33[0m'
