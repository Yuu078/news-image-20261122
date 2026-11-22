#!/usr/bin/env python3
"""THE MORNING ATLAS - Sunday 22 November 2026.
One-page newspaper poster: 35 stories, 7 regions.
Drawn from scratch with Pillow. Deterministic: no timestamps, no randomness,
no network. Run: python3 render_atlas.py  ->  entry.png (1024x1024).
"""

import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 242, 232)
PAPER = (250, 246, 236)
INK = (22, 22, 22)
SOFT = (74, 70, 62)
RED = (193, 39, 45)
NAVY = (31, 58, 95)
STEEL = (58, 88, 132)
PALE = (214, 224, 236)
LINE = (180, 172, 156)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"

_cache = {}


def fnt(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(d, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_size(d, text, path, start, max_w, minimum=8):
    """Largest font size (<= start) at which text fits max_w."""
    size = start
    while size > minimum and d.textlength(text, font=fnt(path, size)) > max_w:
        size -= 1
    return size


def centre(d, y, text, font, fill=INK, x0=16, x1=1008):
    tw = d.textlength(text, font=font)
    d.text(((x0 + x1 - tw) / 2, y), text, font=font, fill=fill)


def rule(d, y, x0=16, x1=1008, width=1, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_masthead(d):
    centre(d, 8, "THE MORNING ATLAS", fnt(SERIF_B, 45))
    rule(d, 62, width=2)
    centre(d, 68, "SUNDAY 22 NOVEMBER 2026", fnt(SERIF_B, 29))
    centre(d, 100, "35 stories  ·  7 regions  ·  one page", fnt(SANS, 13), fill=SOFT)
    rule(d, 119, width=1, fill=LINE)


STRIP = [
    ("200", "nations at COP31"),
    ("35%", "electrification by 2035"),
    ("7,641", "Taiwan stocks plunge (points)"),
    ("100,000", "young Europeans a year"),
    ("50", "Wembanyama points"),
    ("36", "missing in factory fire"),
]


def draw_strip(d):
    x = 16
    cell_w, gap = 160, 6
    for num, label in STRIP:
        d.rectangle([x, 126, x + cell_w, 170], outline=LINE, width=1)
        size = fit_size(d, num, SANS_B, 23, cell_w - 10)
        nf = fnt(SANS_B, size)
        nw = d.textlength(num, font=nf)
        d.text((x + (cell_w - nw) / 2, 127), num, font=nf, fill=NAVY)
        for i, ln in enumerate(wrap(d, label, fnt(SANS, 10), cell_w - 10)[:2]):
            centre(d, 150 + i * 11, ln, fnt(SANS, 10), fill=SOFT,
                   x0=x, x1=x + cell_w)
        x += cell_w + gap

# ---- illustration helpers -------------------------------------------------

def banner(d, x, y, label):
    f = fnt(SANS_B, 10)
    tw = d.textlength(label, font=f)
    d.rectangle([x, y, x + tw + 10, y + 14], fill=RED)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))


def big_num(d, x, y, w, h, num, fill=NAVY):
    n = len(num)
    size = 22 if n <= 2 else (18 if n <= 4 else 14)
    f = fnt(SANS_B, size)
    tw = d.textlength(num, font=f)
    px, py = x + w - tw - 5, y + h - size - 4
    for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        d.text((px + ox, py + oy), num, font=f, fill=(255, 255, 255))
    d.text((px, py), num, font=f, fill=fill)


def num_badge(d, x, y, n):
    d.rectangle([x, y, x + 16, y + 14], fill=RED)
    f = fnt(SANS_B, 10)
    t = str(n)
    d.text((x + (16 - d.textlength(t, font=f)) / 2, y + 2), t,
           font=f, fill=(255, 255, 255))


def scene_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(205, 220, 236))
    d.rectangle([x, y, x + w, y + 18], fill=(178, 198, 222))
    cols = [RED, NAVY, (46, 125, 60), (212, 160, 30), (255, 255, 255), (120, 60, 140)]
    for i, c in enumerate(cols):
        fx = x + 20 + i * 92
        d.line([(fx, y + 4), (fx, y + 30)], fill=INK, width=2)
        d.rectangle([fx, y + 4, fx + 34, y + 18], fill=c, outline=INK)
    cx, cy = x + w // 2, y + h - 26
    d.ellipse([cx - 200, cy - 22, cx + 200, cy + 22], fill=(146, 108, 66),
              outline=INK, width=2)
    d.ellipse([cx - 200, cy - 22, cx + 200, cy + 2], fill=(172, 130, 84),
              outline=INK, width=2)
    for sx in (-230, -150, 150, 230):
        d.rectangle([cx + sx - 16, cy - 8, cx + sx + 16, cy + 16],
                    fill=(90, 60, 40), outline=INK)
    d.rectangle([cx - 95, y + 34, cx + 95, y + 82], fill=(255, 255, 255),
                outline=INK, width=2)
    d.text((cx - 38, y + 38), "DRAFT", font=fnt(SANS_B, 20), fill=RED)
    for i in range(4):
        d.line([(cx - 80, y + 62 + i * 5), (cx + 80, y + 62 + i * 5)],
               fill=(150, 150, 150), width=1)
    d.ellipse([cx + 62, y + 34, cx + 88, y + 58], outline=RED, width=3)


def scene_bahrain(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 190))
    d.rectangle([x + 8, y + 18, x + 120, y + h], fill=(70, 70, 74), outline=INK)
    d.rectangle([x + 20, y + 6, x + 28, y + 18], fill=(70, 70, 74))
    d.rectangle([x + 44, y + 10, x + 52, y + 18], fill=(70, 70, 74))
    d.polygon([(x + 130, y + h), (x + 148, y + 6), (x + 166, y + h)], fill=(240, 120, 20))
    d.polygon([(x + 138, y + h), (x + 148, y + 18), (x + 158, y + h)], fill=RED)
    for i in range(3):
        sx = x + 185 + i * 16
        d.line([(sx, y + 26 - i * 6), (sx + 12, y + 14 - i * 6)], fill=INK, width=2)
        d.ellipse([sx + 10, y + 10 - i * 6, sx + 15, y + 15 - i * 6], fill=RED)


def scene_indonesia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 228, 208))
    d.rectangle([x + 10, y + 20, x + 130, y + h], fill=(120, 72, 44), outline=INK)
    for i in range(3):
        d.polygon([(x + 10 + i * 40, y + 20), (x + 30 + i * 40, y + 8),
                   (x + 50 + i * 40, y + 20)], fill=(90, 50, 30))
    d.polygon([(x + 145, y + h), (x + 162, y + 4), (x + 180, y + h)], fill=(240, 120, 20))
    d.polygon([(x + 152, y + h), (x + 162, y + 16), (x + 172, y + h)], fill=RED)
    for i, (sx, sy, r) in enumerate([(200, 8, 6), (212, 2, 5), (222, 8, 4)]):
        d.ellipse([x + sx - r, y + sy, x + sx + r, y + sy + 2 * r],
                  fill=(150, 150, 150))


def scene_lasvegas(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 28, 52))
    d.arc([x - 30, y - 6, x + 150, y + h + 26], 300, 60, fill=(120, 120, 130),
          width=7)
    d.rounded_rectangle([x + 88, y + 12, x + 178, y + 26], radius=5, fill=RED,
                        outline=(255, 255, 255))
    d.polygon([(x + 178, y + 14), (x + 196, y + 8), (x + 196, y + 24),
               (x + 178, y + 24)], fill=RED)
    for wx in (100, 158):
        d.ellipse([x + wx, y + 24, x + wx + 14, y + h - 2], fill=INK,
                  outline=(255, 255, 255))
    for i in range(2):
        for j in range(2):
            c = (255, 255, 255) if (i + j) % 2 == 0 else INK
            d.rectangle([x + 205 + i * 8, y + 4 + j * 8, x + 213 + i * 8,
                         y + 12 + j * 8], fill=c)


def scene_wemby(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 196, 150))
    d.line([(x, y + h - 8), (x + w, y + h - 8)], fill=(255, 255, 255), width=2)
    d.line([(x + 196, y + 2), (x + 196, y + h - 8)], fill=INK, width=3)
    d.rectangle([x + 176, y + 2, x + 196, y + 16], fill=(255, 255, 255),
                outline=INK)
    d.ellipse([x + 168, y + 14, x + 190, y + 20], outline=(230, 90, 20), width=3)
    d.ellipse([x + 30, y + 6, x + 58, y + 34], fill=(230, 110, 30), outline=INK)
    d.arc([x + 30, y + 6, x + 58, y + 34], 200, 340, fill=INK, width=1)
    d.line([(x + 30, y + 20), (x + 58, y + 20)], fill=INK, width=1)
    d.line([(x + 44, y + 6), (x + 44, y + 34)], fill=INK, width=1)


def scene_youth(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 236, 228))
    d.rectangle([x + 14, y + 6, x + 74, y + h - 6], fill=NAVY, outline=INK)
    d.line([(x + 14, y + h // 2), (x + 74, y + h // 2)], fill=(255, 255, 255),
           width=4)
    d.line([(x + 44, y + 6), (x + 44, y + h - 6)], fill=(255, 255, 255), width=4)
    d.line([(x + 14, y + 6), (x + 74, y + h - 6)], fill=RED, width=2)
    d.line([(x + 74, y + 6), (x + 14, y + h - 6)], fill=RED, width=2)
    d.polygon([(x + 100, y + 12), (x + 128, y + h // 2), (x + 100, y + h - 12)],
              fill=(46, 125, 60))
    d.line([(x + 100, y + h // 2), (x + 128, y + h // 2)], fill=(46, 125, 60),
           width=3)
    d.rectangle([x + 128, y + 6, x + 176, y + h - 6], fill=(0, 51, 153),
                outline=INK)
    for i in range(8):
        import math
        a = math.pi * 2 * i / 8
        sx = x + 152 + int(7 * math.cos(a))
        sy = y + h // 2 + int(7 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 210, 0))


def scene_taiwan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.line([(x + 8, y + 4), (x + 8, y + h - 6)], fill=INK, width=1)
    d.line([(x + 8, y + h - 6), (x + w - 6, y + h - 6)], fill=INK, width=1)
    pts = [(x + 14, y + 8), (x + 60, y + 12), (x + 100, y + 10),
           (x + 140, y + 20), (x + 180, y + 28), (x + 220, y + h - 10)]
    d.line(pts, fill=RED, width=3)
    for bx, bh, c in [(30, 10, (46, 125, 60)), (80, 16, (46, 125, 60)),
                      (130, 8, RED), (180, 6, RED)]:
        d.rectangle([x + bx, y + h - 6 - bh, x + bx + 18, y + h - 6], fill=c)


def scene_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(190, 214, 232))
    d.rectangle([x, y + 16, x + w, y + h], fill=(52, 110, 160))
    for wy in (22, 30):
        for wx in range(0, w, 24):
            d.arc([x + wx, y + wy - 4, x + wx + 24, y + wy + 8], 180, 360,
                  fill=(255, 255, 255), width=2)
    d.rectangle([x + 120, y + 6, x + 225, y + 18], fill=(40, 40, 44), outline=INK)
    for i, c in enumerate([(200, 60, 40), (40, 120, 70), (220, 180, 40)]):
        d.rectangle([x + 128 + i * 32, y - 2, x + 154 + i * 32, y + 6], fill=c,
                    outline=INK)
    d.ellipse([x + 34, y + 22, x + 44, y + 32], fill=(232, 180, 140), outline=INK)
    d.arc([x + 20, y + 26, x + 52, y + 40], 180, 360, fill=(232, 180, 140),
          width=4)


def scene_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 198))
    d.line([(x, y + h - 6), (x + w, y + h - 6)], fill=(150, 120, 80), width=2)
    for i, bx in enumerate((16, 78, 140)):
        fill = (255, 255, 255) if i == 1 else (150, 105, 55)
        d.rectangle([x + bx, y + 14, x + bx + 52, y + h - 6], fill=fill,
                    outline=INK)
        d.line([(x + bx + 26, y + 14), (x + bx + 26, y + h - 6)], fill=INK,
               width=1)
        d.line([(x + bx, y + 14), (x + bx + 52, y + h - 6)], fill=INK, width=1)
    d.rectangle([x + 101, y + 16, x + 107, y + 30], fill=RED)
    d.rectangle([x + 92, y + 21, x + 116, y + 27], fill=RED)


def scene_yemen(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 222, 190))
    for jx, jy in [(30, 8), (110, 4), (190, 12)]:
        d.polygon([(x + jx, y + jy + 10), (x + jx + 22, y + jy + 4),
                   (x + jx + 22, y + jy + 12), (x + jx, y + jy + 16)],
                  fill=(50, 50, 55))
        d.polygon([(x + jx + 22, y + jy + 4), (x + jx + 34, y + jy + 8),
                   (x + jx + 22, y + jy + 12)], fill=(50, 50, 55))
    for sx, sy in [(60, 26), (150, 30), (215, 24)]:
        for k in range(6):
            import math
            a = math.pi * k / 3
            ex = x + sx + int(9 * math.cos(a))
            ey = y + sy + int(9 * math.sin(a))
            d.line([(x + sx, y + sy), (ex, ey)], fill=(230, 120, 20), width=2)
        d.ellipse([x + sx - 3, y + sy - 3, x + sx + 3, y + sy + 3],
                  fill=(240, 90, 20))


def scene_gamer(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(36, 36, 48))
    d.rounded_rectangle([x + 70, y + 8, x + 175, y + h - 6], radius=9,
                        fill=(70, 70, 86), outline=(255, 255, 255))
    d.ellipse([x + 82, y + 14, x + 96, y + 28], fill=(60, 60, 74), outline=INK)
    d.line([(x + 89, y + 14), (x + 89, y + 28)], fill=(255, 255, 255), width=2)
    d.line([(x + 82, y + 21), (x + 96, y + 21)], fill=(255, 255, 255), width=2)
    for bx, by, c in [(150, 14, (240, 200, 40)), (162, 20, RED),
                      (150, 26, (46, 125, 60)), (138, 20, NAVY)]:
        d.ellipse([x + bx, y + by, x + bx + 8, y + by + 8], fill=c,
                  outline=(255, 255, 255))
    d.rounded_rectangle([x + 12, y + 6, x + 58, y + 26], radius=6,
                        fill=(255, 255, 255), outline=INK)
    for i in range(3):
        d.ellipse([x + 20 + i * 10, y + 14, x + 25 + i * 10, y + 19], fill=INK)


def scene_mexico(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 214))
    d.ellipse([x + 10, y + 2, x + w - 10, y + 26], fill=(120, 120, 128),
              outline=INK)
    d.ellipse([x + 30, y + 8, x + w - 30, y + 22], fill=(46, 125, 60))
    d.rectangle([x, y + 26, x + w, y + h], fill=(46, 125, 60))
    d.line([(x, y + 32), (x + w, y + 32)], fill=(255, 255, 255), width=1)
    for px in (30, 210):
        d.line([(x + px, y + 2), (x + px, y + 18)], fill=INK, width=2)
        d.ellipse([x + px - 6, y - 2, x + px + 6, y + 6], fill=(255, 240, 150),
                  outline=INK)
    d.ellipse([x + 108, y + 24, x + 138, y + h - 4], fill=(120, 70, 30),
              outline=(255, 255, 255))
    d.line([(x + 112, y + 28), (x + 134, y + 28)], fill=(255, 255, 255), width=1)
    d.line([(x + 123, y + 24), (x + 123, y + h - 4)], fill=(255, 255, 255),
           width=1)


# ---- hero + cards ---------------------------------------------------------

HERO_BODY = ("Talks ran past Friday's deadline into overtime; a final draft "
             "landed in the early hours of Sunday. It drops fossil-fuel "
             "phase-out language and targets 35% electrification by 2035.")


def draw_hero(d):
    d.rectangle([16, 176, 1008, 306], outline=INK, width=2)
    scene_cop31(d, 17, 177, 594, 128)
    hf = fnt(SANS_B, 46)
    hw = d.textlength("200", font=hf)
    hx, hy = 611 - 8 - hw, 226
    for ox, oy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2)):
        d.text((hx + ox, hy + oy), "200", font=hf, fill=(255, 255, 255))
    d.text((hx, hy), "200", font=hf, fill=RED)
    banner(d, 17, 177, "COP31")
    num_badge(d, 590, 177, 1)
    d.text((623, 180), "1  ·  THE BIG STORY", font=fnt(SANS_B, 10), fill=RED)
    d.text((623, 196), "COP31 FINAL DEAL IN SIGHT", font=fnt(SANS_B, 20),
           fill=INK)
    for i, ln in enumerate(wrap(d, HERO_BODY, fnt(SANS, 12), 372)):
        d.text((623, 224 + i * 15), ln, font=fnt(SANS, 12), fill=INK)
    d.text((623, 288), "Antalya, Turkey  ·  (Reuters; AP; BBC)",
           font=fnt(SANS_I, 10), fill=SOFT)


CARDS = [
    (2, "BAHRAIN", "IRAN HITS BAHRAIN",
     "Iranian strike hits a civilian plant; Saudi downs 3 missiles and 1 drone.",
     "(News Media House; wires)", scene_bahrain, "3"),
    (3, "INDONESIA", "INDONESIA FACTORY FIRE",
     "Search for 36 missing after fire at Milkita candy factory in Cikande, Serang.",
     "(Reuters; BBC)", scene_indonesia, "36"),
    (4, "LAS VEGAS", "VERSTAPPEN WINS LAS VEGAS GP",
     "Verstappen wins a Las Vegas GP with 34 lead changes; two Ferraris collide.",
     "(BBC)", scene_lasvegas, "34"),
    (5, "WEMBANYAMA", "WEMBANYAMA 50",
     "Wembanyama scores 50 as San Antonio Spurs beat New Orleans 114-91.",
     "(BBC)", scene_wemby, "50"),
    (6, "YOUTH DEAL", "UK\u2013EU YOUTH DEAL GOES AHEAD",
     "Deal opens Britain to 100,000 young Europeans a year, fees row aside.",
     "(wires; BBC)", scene_youth, "100,000"),
    (7, "TAIWAN", "TAIWAN STOCKS PLUNGE",
     "Stocks fell 7,641 points last week; fund steps in, short-selling curbed.",
     "(wires)", scene_taiwan, "7,641"),
    (8, "HORMUZ", "PUGH SWIMS THE STRAIT",
     "Lewis Pugh, 56, finishes a 3-day, 15-km swim through the strait.",
     "(Daily Perspective; wires)", scene_hormuz, "15"),
    (9, "GAZA", "GAZA AID WORKERS KILLED",
     "Israeli troops kill 3 Palestinians handing out supplies, witnesses say.",
     "(wires)", scene_gaza, "3"),
    (10, "YEMEN", "70+ SAUDI RAIDS ON YEMEN",
     "Houthis say over 70 Saudi air raids hit 8 Yemeni areas.",
     "(wires)", scene_yemen, "70+"),
    (11, "TEEN GAMER", "TEEN GAMER RESCUES GIRL",
     "Landon Tresp, 16, meets a girl in a game and helps the FBI rescue her.",
     "(BBC)", scene_gamer, "16"),
    (12, "MEXICO CITY", "NFL IN MEXICO CITY TONIGHT",
     "49ers (8-1) host Vikings (7-2) at Estadio Banorte \u2014 first SNF in Mexico.",
     "(NFL/DAZN/CNN)", scene_mexico, "7,352"),
]


def draw_cards(d):
    for i, (n, label, head, body, src, scene, key) in enumerate(CARDS):
        row, col = divmod(i, 4)
        x = 16 + col * 250
        y = 312 + row * 106
        d.rectangle([x, y, x + 242, y + 100], outline=INK, width=1)
        scene(d, x + 1, y + 1, 240, 38)
        big_num(d, x + 1, y + 1, 240, 38, key)
        banner(d, x + 1, y + 1, label)
        num_badge(d, x + 225, y + 1, n)
        hs = fit_size(d, head, SANS_B, 12, 230)
        d.text((x + 6, y + 42), head, font=fnt(SANS_B, hs), fill=INK)
        for j, ln in enumerate(wrap(d, body, fnt(SANS, 11), 230)[:2]):
            d.text((x + 6, y + 58 + j * 12), ln, font=fnt(SANS, 11), fill=INK)
        d.text((x + 6, y + 85), src, font=fnt(SANS_I, 10), fill=SOFT)
    # 12th cell: pointer to the wire below
    x = 16 + 3 * 250
    y = 312 + 2 * 106
    d.rectangle([x, y, x + 242, y + 100], outline=LINE, width=1)
    d.text((x + 12, y + 12), "12 STORIES ABOVE", font=fnt(SANS_B, 12), fill=NAVY)
    for j, ln in enumerate(wrap(d, "23 more stories in THE WIRE below, "
                                 "each with the time it broke.",
                                 fnt(SANS, 10), 218)):
        d.text((x + 12, y + 34 + j * 13), ln, font=fnt(SANS, 10), fill=SOFT)
    d.text((x + 12, y + 78), "All 35 verified for 22 Nov 2026.",
           font=fnt(SANS_I, 9), fill=SOFT)

# ---- heat map -------------------------------------------------------------

HEAT7 = (31, 58, 95)
HEAT6 = (58, 88, 132)
HEAT4 = (110, 134, 170)
HEAT3 = (168, 184, 204)

NA = [(-168, 66), (-145, 70), (-130, 71), (-115, 68), (-100, 69), (-90, 69),
      (-82, 66), (-78, 62), (-70, 58), (-60, 55), (-55, 52), (-60, 47),
      (-65, 44), (-70, 42), (-74, 39), (-76, 35), (-80, 32), (-81, 27),
      (-84, 30), (-90, 21), (-95, 19), (-97, 16), (-92, 15), (-86, 12),
      (-83, 9), (-79, 9), (-83, 13), (-90, 14), (-95, 17), (-105, 20),
      (-110, 23), (-114, 28), (-117, 33), (-122, 37), (-124, 42), (-124, 48),
      (-130, 55), (-140, 60), (-150, 61), (-160, 58), (-165, 60)]
SA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
      (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -52), (-68, -55),
      (-66, -50), (-65, -45), (-62, -41), (-57, -38), (-50, -33), (-42, -23),
      (-38, -15), (-35, -9), (-35, -6), (-40, -3), (-44, -2), (-50, 0),
      (-53, 4), (-58, 7), (-62, 9), (-68, 11), (-72, 12), (-76, 10)]
EU = [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (1, 51), (4, 53), (8, 55),
      (8, 57), (11, 58), (6, 60), (12, 61), (18, 64), (18, 69), (25, 71),
      (30, 70), (35, 68), (40, 68), (42, 66), (40, 62), (38, 58), (35, 55),
      (32, 52), (30, 48), (28, 45), (26, 42), (23, 40), (22, 37), (20, 40),
      (16, 42), (13, 44), (8, 44), (3, 43), (0, 39), (-2, 37), (-6, 36),
      (-9, 38)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (0, 53), (1, 51), (-2, 50)]
AF = [(-6, 35), (-1, 35), (5, 37), (10, 37), (11, 34), (15, 32), (20, 32),
      (25, 32), (30, 31), (32, 31), (34, 28), (35, 24), (37, 20), (39, 16),
      (41, 12), (44, 11), (48, 11), (51, 11), (50, 7), (46, 4), (42, 0),
      (40, -5), (39, -10), (37, -15), (35, -20), (33, -26), (30, -30),
      (27, -33), (22, -35), (18, -33), (16, -29), (14, -24), (13, -19),
      (12, -14), (12, -9), (11, -4), (9, 0), (9, 4), (5, 5), (0, 6), (-5, 5),
      (-8, 4), (-12, 8), (-15, 11), (-17, 15), (-17, 20), (-16, 25),
      (-14, 28), (-11, 30), (-9, 32)]
AS = [(30, 70), (38, 68), (45, 68), (52, 69), (60, 69), (68, 70), (75, 72),
      (82, 73), (90, 75), (98, 76), (105, 77), (112, 76), (120, 73),
      (128, 72), (135, 72), (142, 72), (150, 70), (158, 69), (162, 66),
      (170, 66), (178, 65), (172, 62), (165, 60), (162, 56), (158, 52),
      (156, 55), (150, 59), (144, 58), (142, 52), (140, 46), (138, 43),
      (134, 42), (130, 42), (128, 38), (126, 38), (122, 38), (120, 34),
      (122, 30), (120, 27), (116, 23), (112, 21), (109, 18), (108, 13),
      (105, 9), (103, 6), (101, 8), (99, 11), (97, 15), (94, 17), (92, 21),
      (90, 22), (88, 22), (86, 20), (83, 18), (80, 15), (78, 10), (76, 9),
      (74, 14), (72, 20), (70, 22), (68, 24), (66, 25), (63, 25), (60, 25),
      (58, 26), (56, 27), (54, 27), (52, 28), (50, 29), (48, 30), (46, 30),
      (44, 29), (42, 15), (41, 13), (43, 12), (45, 13), (48, 14), (52, 15),
      (55, 17), (58, 20), (59, 23), (58, 25), (56, 26), (53, 27), (50, 28)]
ARABIA = [(42, 15), (41, 13), (43, 12), (45, 13), (48, 14), (52, 15),
          (55, 17), (58, 20), (59, 23), (58, 25), (56, 26), (53, 27),
          (50, 28), (48, 30), (46, 30), (44, 29), (42, 20), (42, 15)]
AU = [(113, -22), (114, -28), (115, -33), (118, -35), (122, -34), (126, -32),
      (129, -32), (132, -32), (135, -35), (137, -35), (140, -38), (143, -39),
      (146, -39), (149, -37), (151, -34), (153, -31), (153, -27), (151, -24),
      (148, -20), (145, -19), (142, -16), (142, -11), (140, -12), (137, -12),
      (135, -15), (133, -12), (131, -12), (129, -14), (126, -14), (123, -16),
      (120, -19), (117, -20), (114, -21)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (140, 39),
         (141, 41), (142, 43), (144, 44), (143, 42), (141, 39), (139, 36),
         (136, 34), (133, 34), (131, 32)]

MAP_Y0, MAP_Y1 = 646, 786
LAT_TOP, LAT_BOT = 80, -58


def proj(lon, lat):
    px = 16 + (lon + 180) / 360 * 992
    py = MAP_Y0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * (MAP_Y1 - MAP_Y0)
    return (px, py)


def poly(d, coords, fill):
    d.polygon([proj(lo, la) for lo, la in coords], fill=fill, outline=INK)


def draw_map(d):
    d.text((16, 630), "WHERE IT HAPPENED", font=fnt(SANS_B, 13), fill=INK)
    d.rectangle([16, MAP_Y0, 1008, MAP_Y1], fill=(232, 236, 240), outline=INK,
                width=1)
    poly(d, NA, HEAT6)
    poly(d, SA, HEAT3)
    poly(d, EU, HEAT7)
    poly(d, UK, HEAT7)
    poly(d, AF, HEAT4)
    poly(d, AS, HEAT7)
    poly(d, ARABIA, HEAT4)
    poly(d, AU, HEAT7)
    poly(d, JAPAN, HEAT7)
    lab = fnt(SANS_B, 9)
    for text, lo, la in [("NORTH AMERICA 6", -138, 68),
                         ("LATIN AMERICA 3", -62, -16),
                         ("EUROPE 7", 18, 60),
                         ("AFRICA 4", 18, 6),
                         ("ASIA-PACIFIC 7", 88, 52)]:
        lx, ly = proj(lo, la)
        for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            d.text((lx + ox, ly + oy), text, font=lab, fill=(255, 255, 255))
        d.text((lx, ly), text, font=lab, fill=NAVY)
    d.rectangle([16, 770, 1008, MAP_Y1], fill=PAPER)
    centre(d, 773,
           "Europe 7  ·  Asia-Pacific 7  ·  North America 6  ·  Middle East 4  ·  "
           "Africa 4  ·  Latin America 3  ·  Global 4 (no pin)",
           fnt(SANS_B, 10), fill=NAVY)
    pins = [(1, 30.7, 36.9), (2, 50.6, 26.2), (3, 106.2, -6.1),
            (4, -115.1, 36.2), (5, -98.5, 29.4), (6, -0.1, 51.5),
            (7, 121.5, 25.0), (8, 56.2, 26.5), (9, 36.0, 30.5),
            (10, 47.5, 15.5), (11, -108.0, 42.0), (12, -103.0, 19.4)]
    pf = fnt(SANS_B, 8)
    for n, lo, la in pins:
        cx, cy = proj(lo, la)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255),
                  outline=RED, width=2)
        t = str(n)
        d.text((cx - d.textlength(t, font=pf) / 2, cy - 5), t, font=pf,
               fill=NAVY)


# ---- the wire -------------------------------------------------------------

WIRE = [
    (13, "07:10", "Nigerian youth not shaping next year's election", "BBC"),
    (14, "07:43", "Catherine's \u201croad to recovery\u201d fronts Sunday papers", "BBC"),
    (15, "08:59", "Virginia confirms first measles death of year", "WJLA"),
    (16, "10:00", "Ruto battles to keep key voting blocs for Kenya 2027", "The Standard"),
    (17, "11:05", "Brazilian town clears debris after deadly storm", "wires"),
    (18, "11:39", "BBC apologises over Strictly noise disruption; phone seized", "BBC"),
    (19, "11:43", "Trump demands Nvidia bring back Jensen Huang", "wires"),
    (20, "12:00", "Real people find their work cloned by AI characters", "BBC"),
    (21, "12:17", "Edo governor ready to supervise execution of kidnappers", "Vanguard"),
    (22, "12:19", "Beijing rejects US ban on Chinese-owned telecom firms", "wires"),
    (23, "12:41", "Ebola death toll passes 5,700 in DR Congo outbreak", "wires"),
    (24, "12:51", "Melania Trump hopes for Ukraine\u2013Russia ceasefire by year-end", "wires"),
    (25, "12:56", "Indian parties protest Facebook over deleted accounts", "wires"),
    (26, "13:01", "Theresa May \u201caghast\u201d at Burnham's EU plans", "BBC"),
    (27, "13:21", "Pulis on Pochettino's first Man Utd game vs Liverpool", "BBC"),
    (28, "13:22", "Tinubu asks parliament to decriminalise attempted suicide", "TimesLIVE"),
    (29, "13:35", "11+ dead in India after drinking illicit alcohol", "wires"),
    (30, "14:09", "Australia vows to regulate AI shoppers, surveillance pricing", "wires"),
    (31, "14:17", "Why Arsenal trail in Women's Champions League race", "BBC"),
    (32, "14:41", "Zelensky: next peace talks must bring real progress", "wires"),
    (33, "15:16", "IDF renews attacks on southern Lebanese towns", "wires"),
    (34, "15:16", "EU and Indonesia sign trade deal after 10 years of talks", "wires"),
    (35, "20:30", "U-17 World Cup Day 4: Mexico face Cameroon in Doha", "FIFA"),
]


def draw_wire(d):
    d.text((16, 792), "THE WIRE \u2014 23 more stories, as they broke (WIB)",
           font=fnt(SANS_B, 13), fill=INK)
    f = fnt(SANS, 11)
    fb = fnt(SANS_B, 11)
    for i, (n, tm, text, src) in enumerate(WIRE):
        col, row = divmod(i, 12)
        x = 16 + col * 496
        y = 810 + row * 11.5
        head = "%d \u00b7 %s  " % (n, tm)
        line = head + text + "  (%s)" % src
        if d.textlength(line, font=f) > 488:
            print("WIRE OVERFLOW:", n, line, file=sys.stderr)
        d.text((x, y), head, font=fb, fill=RED)
        d.text((x + d.textlength(head, font=fb), y), text + "  (%s)" % src,
               font=f, fill=INK)


# ---- date check + footer --------------------------------------------------

STAMP = "Verified at 15:33 WIB"

DATE_LINES = [
    "\u00d7 \u201cEl Chapo Isidro\u201d arrested \u2014 captured 20 Nov, announced "
    "21 Nov (Reuters/AP). Not 22 Nov.",
    "\u00d7 Mamdani's Rikers Island closure plan \u2014 announced 20 Nov "
    "(AP/BBC 21 Nov). Not 22 Nov.",
]


def draw_datecheck(d):
    d.rectangle([16, 950, 1008, 994], outline=RED, width=2)
    d.text((26, 954), "DATE CHECK \u2014 WHAT WE LEFT OUT",
           font=fnt(SANS_B, 11), fill=RED)
    sw = d.textlength(STAMP, font=fnt(SANS_B, 11))
    d.text((998 - sw, 954), STAMP, font=fnt(SANS_B, 11), fill=RED)
    for i, ln in enumerate(DATE_LINES):
        d.text((26, 968 + i * 12), ln, font=fnt(SANS, 11), fill=INK)


def draw_footer(d):
    centre(d, 999,
           "All 35 stories happened or were first reported on Sunday 22 November 2026.",
           fnt(SERIF_I, 11), fill=INK)
    centre(d, 1012,
           "Sources: Reuters \u00b7 AP \u00b7 BBC \u00b7 wires \u00b7 NFL/DAZN/CNN \u00b7 "
           "Daily Perspective \u00b7 News Media House \u00b7 The Standard \u00b7 Vanguard \u00b7 "
           "TimesLIVE \u00b7 WJLA \u00b7 FIFA",
           fnt(SANS, 9), fill=SOFT)


# ---- main -----------------------------------------------------------------

def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_strip(d)
    draw_hero(d)
    draw_cards(d)
    draw_map(d)
    draw_wire(d)
    draw_datecheck(d)
    draw_footer(d)
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    img = build()
    img.save(out, "PNG", optimize=True)
    data = open(out, "rb").read()
    print("entry.png", len(data), "bytes",
          hashlib.sha256(data).hexdigest())
    if len(data) > 1048576:
        print("TOO BIG", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
