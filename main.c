#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>

#include <_types/_uint32_t.h>
#include <_types/_uint8_t.h>

uint32_t color_i(uint8_t i);

uint8_t red(uint32_t color) { return color >> 16; }
uint8_t green(uint32_t color) { return (color >> 8) & 0x00ff; }
uint8_t blue(uint32_t color) { return color & 0x0000ff;; }

void print_hex(uint32_t color, char* text);

int main(void) {
    char hehe[] = "hehe";
    print_hex(color_i(23), NULL);
    print_hex(color_i(183), hehe);
}

// adjusted from kitty/colors.c
uint32_t color_i(uint8_t i) {
    assert(i > 15); // first 16 colors are usually customized

    const uint8_t valuerange[6] = {0x00, 0x5f, 0x87, 0xaf, 0xd7, 0xff};
    if (i < 232) {
        uint8_t color = i - 16;
        uint8_t r = valuerange[(color / 36) % 6], g = valuerange[(color / 6) % 6], b = valuerange[color % 6];
        return (r << 16) | (g << 8) | b;
    } else {
        int gray = i - 232;
        uint8_t v = 8 + gray * 10;
        return (v << 16) | (v << 8) | v;
    }
}

void print_hex(uint32_t color, char* text) {
    char *term = getenv("COLORTERM");
    int truecolor = term && (!strcmp(term, "truecolor") || !strcmp(term, "24bit"));

    int r = red(color); int g = green(color); int b = blue(color);
    int foreground = (r+g+b > 382) ? 30 : 37;

    if (truecolor) printf("\e[%d;48;2;%d;%d;%dm   ", foreground, r, g, b);

    if (text) printf("%s", text);
    else printf("#%06x", color);

    if (truecolor) printf("   \e[0m");
}
