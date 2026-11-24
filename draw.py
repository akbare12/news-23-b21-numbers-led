#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news front page (1024x1024).

Layout (top to bottom):
  masthead -> giant number grid (2x5) -> region bar -> UTC strip
  -> 3 hero scenes -> 10 small cards (2 rows x 5) -> world map + ALSO list
  -> DATE CHECK box -> footer with sources + chip legend.
All scenes are drawn illustrations, not photographs.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 246, 236)          # warm newsprint
INK = (24, 24, 24)
RED = (178, 34, 34)
DARK = (28, 34, 48)
BLUE = (31, 78, 160)
GREY = (110, 110, 108)
LINE = (180, 172, 156)
CARD_BG = (255, 253, 247)
AMBER = (176, 118, 8)
GREEN = (28, 120, 70)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(d, text, path, size, max_w, start=None):
    """Largest font size <= size that fits max_w, else the smallest."""
    s = start or size
    while s > 6:
        f = font(path, s)
        if d.textlength(text, font=f) <= max_w:
            return f
        s -= 1
    return font(path, 6)


def wrap(d, text, f, max_w):
    """Greedy word wrap returning lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            if d.textlength(cur + " " + w, font=f) <= max_w:
                cur += " " + w
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def text_block(d, x, y, text, f, color, max_w, leading, max_lines=None):
    """Draw wrapped text; return y after the last line."""
    lines = wrap(d, text, f, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=f, fill=color)
        y += leading
    return y


def chip(d, x, y, label, fill):
    """Certainty chip; returns width used."""
    f = font(SANS_B, 9)
    w = int(d.textlength(label, font=f)) + 12
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=fill)
    d.text((x + 6, y + 2), label, font=f, fill=(255, 255, 255))
    return w


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 4], fill=RED)
d.text((16, 10), "THE WORLD TODAY", font=font(SERIF_B, 46), fill=INK)
d.text((16, 62), "MONDAY 23 NOVEMBER 2026", font=font(SANS_B, 17), fill=RED)
d.text((W - 16, 14), "31 STORIES", font=font(SANS_B, 15), fill=INK, anchor="ra")
d.text((W - 16, 36), "6 REGIONS", font=font(SANS_B, 15), fill=INK, anchor="ra")
d.text((W - 16, 62), "AI ROUT  ·  AI RULES  ·  POWER SHIFT",
       font=font(SANS_B, 11), fill=GREY, anchor="ra")
d.line([16, 86, W - 16, 86], fill=INK, width=2)

# ------------------------------------------------------- giant number grid
NUMBERS = [
    ("-3.3%", "KOSPI"),
    ("5.3", "US-CHINA GAP"),
    ("11,762", "EBOLA CASES"),
    ("10T WON", "SEOUL FUND"),
    ("2%", "BILLIONAIRE TAX"),
    ("$450M", "SKUBAL DEAL"),
    ("165", "MISSILES / WEEK"),
    ("12,000", "CLEARED"),
    ("264 KG", "EXPLOSIVES"),
    ("$107.3B", "ANTHROPIC IPO"),
]
gx0, gy0, gw, gh, gap = 16, 94, 190, 44, 8
for i, (num, lab) in enumerate(NUMBERS):
    r, c = divmod(i, 5)
    x = gx0 + c * (gw + gap)
    y = gy0 + r * (gh + 4)
    d.rectangle([x, y, x + gw, y + gh], outline=LINE, width=1, fill=CARD_BG)
    nf = fit(d, num, SANS_B, 26, gw - 12)
    d.text((x + gw // 2, y + 3), num, font=nf, fill=RED, anchor="ma")
    d.text((x + gw // 2, y + 29), lab, font=font(SANS_B, 9), fill=INK, anchor="ma")

# ------------------------------------------------------------- region bar
REGIONS = [
    ("NORTH AMERICA 8", (31, 78, 160)),
    ("EUROPE 6", (198, 110, 20)),
    ("MIDDLE EAST 6", (122, 60, 150)),
    ("ASIA-PACIFIC 7", (22, 130, 110)),
    ("AFRICA 3", (150, 90, 20)),
    ("WORLD 1", (90, 90, 90)),
]
rx, ry, rh = 16, 194, 22
nseg = len(REGIONS)
wseg = (W - 32) // nseg
for label, color in REGIONS:
    d.rectangle([rx, ry, rx + wseg - 2, ry + rh], fill=color)
    f = font(SANS_B, 10)
    d.text((rx + wseg // 2, ry + 5), label, font=f, fill=(255, 255, 255),
           anchor="ma")
    rx += wseg

# -------------------------------------------------------------- UTC strip
d.rectangle([16, 224, W - 16, 246], fill=DARK)
d.text((24, 229), "THE DAY IN UTC", font=font(SANS_B, 11), fill=(255, 255, 255))
utc = "~00:00 ASIA OPENS   ·   06:30 KOSPI CLOSES -3.3%   ·   ~09:00 SEOUL FUND   ·   14:30 WALL ST +3%   ·   ~16:00 GUTERRES   ·   ~21:00 FBI HACK   (~ = APPROX.)"
d.text((150, 229), utc, font=font(SANS, 10), fill=(230, 230, 225))

# ------------------------------------------------------------- hero scenes
HY = 254          # hero block top
HW = 322          # hero column width
HGAP = 8
SCENE_H = 168

def hero_col(i, kicker, title, body, source, chip_label, chip_fill):
    x = 16 + i * (HW + HGAP)
    return x


# --- hero 1: Kospi rout — falling chart over a Seoul skyline (dark scene)
x0 = hero_col(0, "", "", "", "", "", None)
d.rectangle([x0, HY, x0 + HW, HY + SCENE_H], fill=(18, 24, 44))
# skyline
import random
random.seed(23)
bx = x0 + 6
while bx < x0 + HW - 10:
    bw = random.randint(16, 30)
    bh = random.randint(34, 88)
    d.rectangle([bx, HY + SCENE_H - bh, bx + bw, HY + SCENE_H], fill=(38, 48, 74))
    for wy in range(HY + SCENE_H - bh + 6, HY + SCENE_H - 6, 10):
        for wx in range(bx + 4, bx + bw - 3, 8):
            if random.random() < 0.55:
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(250, 210, 110))
    bx += bw + 4
# falling chart line
pts = []
for j in range(9):
    px = x0 + 14 + j * (HW - 28) / 8
    py = HY + 18 + j * 13 + random.randint(-4, 4)
    pts.append((px, py))
d.line(pts, fill=(235, 70, 60), width=3)
for (px, py) in pts:
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255),
              outline=(235, 70, 60))
d.text((x0 + 12, HY + 8), "intraday -5.8%", font=font(SANS_B, 11),
       fill=(255, 255, 255))
d.text((x0 + HW - 12, HY + 6), "-3.3%", font=font(SANS_B, 30),
       fill=(235, 70, 60), anchor="ra")

# --- hero 2: Guterres — globe + AI network + podium (dark blue scene)
x1 = hero_col(1, "", "", "", "", "", None)
d.rectangle([x1, HY, x1 + HW, HY + SCENE_H], fill=(16, 42, 78))
d.text((x1 + 8, HY + 6), "150 DELEGATES", font=font(SANS_B, 11),
       fill=(250, 210, 110))
# globe
cx, cy, cr = x1 + 78, HY + 92, 52
d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(90, 160, 220),
          outline=(200, 225, 245), width=2)
d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], outline=(255, 255, 255))
d.arc([cx - cr, cy - 26, cx + cr, cy + 26], 0, 360, fill=(200, 225, 245), width=1)
d.arc([cx - 26, cy - cr, cx + 26, cy + cr], 0, 360, fill=(200, 225, 245), width=1)
d.line([cx - cr, cy, cx + cr, cy], fill=(200, 225, 245), width=1)
# network nodes
random.seed(7)
nodes = []
for _ in range(9):
    nodes.append((x1 + 165 + random.randint(0, 135), HY + 30 + random.randint(0, 110)))
for a in range(len(nodes)):
    for b in range(a + 1, len(nodes)):
        if abs(nodes[a][0] - nodes[b][0]) + abs(nodes[a][1] - nodes[b][1]) < 90:
            d.line([nodes[a], nodes[b]], fill=(140, 190, 240), width=1)
for (nx, ny) in nodes:
    d.ellipse([nx - 4, ny - 4, nx + 4, ny + 4], fill=(250, 210, 110),
              outline=(255, 255, 255))
# podium silhouette
d.rectangle([x1 + HW - 62, HY + SCENE_H - 34, x1 + HW - 22, HY + SCENE_H],
            fill=(10, 26, 52))
d.ellipse([x1 + HW - 52, HY + SCENE_H - 58, x1 + HW - 32, HY + SCENE_H - 38],
          fill=(10, 26, 52))

# --- hero 3: power index bars (light scene)
x2 = hero_col(2, "", "", "", "", "", None)
d.rectangle([x2, HY, x2 + HW, HY + SCENE_H], fill=CARD_BG, outline=LINE)
d.text((x2 + 10, HY + 8), "ASIA POWER INDEX 2026", font=font(SANS_B, 12), fill=INK)
bars = [("US", 78.9, BLUE), ("CHINA", 73.6, RED), ("INDIA 3rd", 40.5, (140, 140, 140))]
by = HY + 38
for name, val, col in bars:
    d.text((x2 + 10, by), name, font=font(SANS_B, 12), fill=INK)
    d.rectangle([x2 + 92, by + 2, x2 + 92 + int(val * 2.1), by + 16], fill=col)
    d.text((x2 + 92 + int(val * 2.1) + 6, by), f"{val}",
           font=font(SANS_B, 12), fill=INK)
    by += 30
d.text((x2 + 10, by + 2), "GAP 5.3", font=font(SANS_B, 20), fill=RED)
d.text((x2 + 108, by + 8), "narrowest since 2018", font=font(SANS, 11), fill=GREY)

# hero text under scenes
HEROES = [
    ("#1 ASIA · MARKETS", "AI ROUT HITS ASIA",
     "Kospi closes 4,708.54, sheds 161 pts. Samsung -3.1%, SK Hynix -2.5%. AI sell-off spreads from Wall Street.",
     "Yonhap · Korea JoongAng", "REPORTED", GREEN),
    ("#2 WORLD · UNITED NATIONS", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
     "UN News · Reuters", "REPORTED", GREEN),
    ("#3 ASIA-PACIFIC · POWER", "US LEAD OVER CHINA AT RECORD LOW",
     "Gap 5.3 narrowest since 2018. US diplomatic influence -6 to 76.7. India third at 40.5.",
     "Lowy Institute", "REPORTED", GREEN),
]
ty = HY + SCENE_H + 6
for i, (kick, title, body, src, clab, cfill) in enumerate(HEROES):
    x = 16 + i * (HW + HGAP)
    d.text((x, ty), kick, font=font(SANS_B, 10), fill=RED)
    tf = fit(d, title, SANS_B, 17, HW)
    text_block(d, x, ty + 14, title, tf, INK, HW, 19, max_lines=2)
    text_block(d, x, ty + 52, body, font(SANS, 11), INK, HW, 14, max_lines=3)
    d.text((x, ty + 96), "Source: " + src, font=font(SANS, 9), fill=GREY)
    chip(d, x + HW - 62, ty + 94, clab, cfill)

# ------------------------------------------------------------- 10 small cards
CARDS = [
    ("#4", "SPORT · US", "Skubal signs $450M Mets deal",
     "Two-time Cy Young winner, nine years — the largest ever for a pitcher.",
     "ESPN", "REPORTED", GREEN, (31, 78, 160), "ball"),
    ("#5", "TECH · US", "Anthropic IPO: $107.3B, largest ever",
     "Claude maker raised at $83 a share on 19 Nov; debut close $97.17.",
     "Bloomberg", "REPORTED", GREEN, (22, 130, 110), "chip"),
    ("#6", "EUROPE · WAR", "Poland: 3 Russian missiles crossed airspace",
     "Kyiv says three Kh-101 entered Poland on Friday; Tusk: provocation.",
     "AP", "CLAIM", AMBER, (150, 60, 40), "missile"),
    ("#7", "EUROPE · SECURITY", "Intel warns of Russian nuclear satellite",
     "Moscow built a satellite to carry a nuclear warhead; launch possible next month.",
     "Bloomberg", "CLAIM", AMBER, (90, 70, 130), "sat"),
    ("#8", "EUROPE · ECONOMY", "Paris: 100+ back 2% billionaire tax",
     "Economists, politicians and unions rally behind France's 2% minimum wealth tax.",
     "AFP", "REPORTED", GREEN, (198, 110, 20), "coin"),
    ("#9", "EUROPE · UK", "Manchester: 12,000 cleared after scare",
     "Substance scare empties arena district; no casualties reported.",
     "AP", "REPORTED", GREEN, (122, 60, 150), "building"),
    ("#10", "EUROPE · WAR", "Zelenskyy: 165 Russian missiles in a week",
     "Kyiv says Moscow fired 165 missiles in seven days as US delays Patriots.",
     "Kyiv", "CLAIM", AMBER, (150, 60, 40), "missile"),
    ("#11", "EUROPE · CLIMATE", "COP31: the day after",
     "Sunday's collapse — 194 nations reject the Antalya Pact — draws fury.",
     "CNN", "REPORTED", GREEN, (22, 130, 110), "globe"),
    ("#12", "AFRICA · LIBYA", "Benghazi: UN demands probe of port attacks",
     "Drones hit two Russian ships; UN calls for an investigation.",
     "UN News", "CLAIM", AMBER, (150, 90, 20), "ship"),
    ("#13", "MIDDLE EAST · ISRAEL", "Israel unity talks resume",
     "Likud and Gantz's Yashar return to the table after Sunday's stall.",
     "Reuters", "ONGOING", BLUE, (31, 78, 160), "flag"),
]

def glyph(cx, cy, kind):
    s = 7
    if kind == "ball":
        d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=(255, 255, 255), width=2)
        d.arc([cx - s, cy - s, cx + s, cy + s], 300, 60, fill=(255, 255, 255), width=1)
    elif kind == "chip":
        d.rectangle([cx - s, cy - s, cx + s, cy + s], outline=(255, 255, 255), width=2)
        for dx in (-4, 0, 4):
            d.line([cx + dx, cy - s - 3, cx + dx, cy - s], fill=(255, 255, 255), width=1)
            d.line([cx + dx, cy + s, cx + dx, cy + s + 3], fill=(255, 255, 255), width=1)
    elif kind == "missile":
        d.polygon([(cx - s, cy + 4), (cx + s, cy), (cx - s, cy - 4)], fill=(255, 255, 255))
        d.line([cx - s - 6, cy, cx - s, cy], fill=(255, 255, 255), width=2)
    elif kind == "sat":
        d.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], outline=(255, 255, 255), width=2)
        d.rectangle([cx - 11, cy - 2, cx - 4, cy + 2], fill=(255, 255, 255))
        d.rectangle([cx + 4, cy - 2, cx + 11, cy + 2], fill=(255, 255, 255))
    elif kind == "coin":
        d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=(255, 255, 255), width=2)
        d.text((cx, cy - 5), "$", font=font(SANS_B, 9), fill=(255, 255, 255), anchor="ma")
    elif kind == "building":
        d.rectangle([cx - 5, cy - s, cx + 5, cy + s], outline=(255, 255, 255), width=2)
        d.line([cx, cy - s, cx, cy + s], fill=(255, 255, 255), width=1)
    elif kind == "globe":
        d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=(255, 255, 255), width=2)
        d.line([cx - s, cy, cx + s, cy], fill=(255, 255, 255), width=1)
    elif kind == "ship":
        d.polygon([(cx - s, cy + 2), (cx + s, cy + 2), (cx + s - 2, cy + s), (cx - s + 2, cy + s)],
                  fill=(255, 255, 255))
        d.line([cx, cy + 2, cx, cy - s], fill=(255, 255, 255), width=2)
    elif kind == "flag":
        d.line([cx - 4, cy - s, cx - 4, cy + s], fill=(255, 255, 255), width=2)
        d.polygon([(cx - 4, cy - s), (cx + s, cy - s + 3), (cx - 4, cy - s + 6)],
                  fill=(255, 255, 255))

CW, CH, CGAP = 192, 84, 8
CY0 = 542
for i, (num, kick, title, body, src, clab, cfill, scol, gk) in enumerate(CARDS):
    r, c = divmod(i, 5)
    x = 16 + c * (CW + CGAP)
    y = CY0 + r * (CH + 6)
    d.rectangle([x, y, x + CW, y + CH], outline=LINE, width=1, fill=CARD_BG)
    # strip: number + kicker + glyph + chip
    d.rectangle([x, y, x + CW, y + 16], fill=scol)
    d.text((x + 5, y + 3), f"{num} · {kick}", font=font(SANS_B, 8),
           fill=(255, 255, 255))
    glyph(x + CW - 72, y + 8, gk)
    # chip overlaid at strip right (small)
    cf = font(SANS_B, 8)
    cw = int(d.textlength(clab, font=cf)) + 10
    d.rounded_rectangle([x + CW - cw - 3, y + 2, x + CW - 3, y + 14], radius=2,
                        fill=cfill)
    d.text((x + CW - cw - 3 + 5, y + 3), clab, font=cf, fill=(255, 255, 255))
    # title (max 2 lines)
    tf = font(SANS_B, 11)
    text_block(d, x + 5, y + 19, title, tf, INK, CW - 10, 12, max_lines=2)
    # body (max 2 lines)
    text_block(d, x + 5, y + 45, body, font(SANS, 10), INK, CW - 10, 11,
               max_lines=2)
    d.text((x + 5, y + 70), src, font=font(SANS, 8), fill=GREY)

# ------------------------------------------------------- map + ALSO list
MY0 = 720
d.text((16, MY0), "THE WORLD — WHERE IT HAPPENED", font=font(SANS_B, 12),
       fill=RED)
d.text((16, MY0 + 14), "PIN = STORY NUMBER", font=font(SANS, 8), fill=GREY)

MAP = (16, 740, 540, 878)   # x0, y0, x1, y1
d.rectangle([MAP[0], MAP[1], MAP[2], MAP[3]], fill=(208, 224, 234),
            outline=LINE)

def ll(lon, lat):
    x = MAP[0] + (lon + 180) / 360 * (MAP[2] - MAP[0])
    y = MAP[1] + (90 - lat) / 180 * (MAP[3] - MAP[1])
    return x, y

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 80), (-80, 73),
     (-75, 62), (-65, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 26),
     (-90, 21), (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 48),
     (-140, 60), (-165, 60)],
    [(-58, 64), (-45, 60), (-30, 68), (-40, 76), (-58, 76)],
    [(-78, 7), (-72, 11), (-60, 8), (-50, 0), (-35, -8), (-40, -20),
     (-48, -28), (-58, -35), (-65, -41), (-70, -52), (-73, -40), (-70, -20),
     (-80, -5), (-81, 0)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (30, 70), (25, 71),
     (18, 69), (12, 65), (5, 60), (-2, 58), (-5, 50), (-9, 43)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (32, -29),
     (25, -34), (18, -35), (15, -27), (12, -18), (9, -1), (9, 4), (-8, 5),
     (-13, 8)],
    [(30, 70), (40, 68), (55, 69), (70, 72), (90, 75), (110, 76), (130, 72),
     (150, 70), (170, 66), (178, 65), (170, 60), (160, 55), (158, 50),
     (142, 45), (140, 40), (130, 35), (127, 35), (122, 30), (120, 25),
     (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (80, 20),
     (75, 10), (70, 25), (60, 25), (55, 27), (50, 30), (48, 30), (43, 28),
     (40, 32), (35, 36), (30, 36), (30, 42), (30, 45), (25, 45), (20, 45),
     (15, 44), (12, 45), (10, 44), (5, 42), (0, 40)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (130, -32), (137, -35),
     (140, -38), (145, -38), (150, -37), (153, -27), (150, -22), (146, -19),
     (142, -11), (136, -12), (130, -13), (122, -14), (115, -20)],
]
for poly in CONTINENTS:
    d.polygon([ll(lon, lat) for lon, lat in poly], fill=(232, 222, 190),
              outline=(190, 178, 150))

# pins: (story no, lon, lat, dx, dy, kind) kind: R=reported, C=claim, O=ongoing
PINS = [
    (1, 127, 37.5, 0, 0, "R"), (22, 127, 37.5, 9, -8, "R"),
    (23, 127, 37.5, 11, 6, "R"), (25, 127, 37.5, -10, 7, "R"),
    (2, -59.6, 13.1, 0, 0, "R"), (3, 116.4, 39.9, 0, 0, "R"),
    (4, -74, 40.7, 0, 0, "R"), (29, -74, 40.7, 10, -7, "R"),
    (5, -122.4, 37.8, 0, 0, "R"), (6, 19, 52, 0, 0, "C"),
    (7, 37.6, 55.8, 0, 0, "C"), (8, 2.35, 48.85, 0, 0, "R"),
    (9, -2.24, 53.48, 0, 0, "R"), (10, 30.5, 50.45, 0, 0, "C"),
    (11, 30.7, 36.9, 0, 0, "R"), (12, 20.1, 32.1, 0, 0, "C"),
    (13, 35.2, 31.8, 0, 0, "O"), (14, 34.5, 31.5, -9, 5, "R"),
    (15, 35.2, 31.9, 9, 7, "R"), (16, 51.4, 35.7, 0, 0, "R"),
    (17, 35.5, 33.9, -7, -7, "R"), (18, 50.6, 26.2, 0, 0, "R"),
    (19, 32.5, 15.6, 0, 0, "R"), (20, 29.7, 1.6, 0, 0, "R"),
    (21, 90.4, 23.8, 0, 0, "R"), (24, 121.5, 31.2, 0, 0, "R"),
    (26, -77, 38.9, 0, 0, "R"), (27, -77, 38.9, 9, -8, "R"),
    (28, -77, 38.9, -9, 7, "R"), (30, -105, 39.7, 0, 0, "R"),
    (31, -97.7, 30.3, 0, 0, "R"),
]
PCOL = {"R": RED, "C": AMBER, "O": BLUE}
for n, lon, lat, dx, dy, kind in PINS:
    px, py = ll(lon, lat)
    px += dx
    py += dy
    r = 7 if n >= 10 else 6
    d.ellipse([px - r, py - r, px + r, py + r], fill=PCOL[kind],
              outline=(255, 255, 255), width=1)
    d.text((px, py - 5), str(n), font=font(SANS_B, 7), fill=(255, 255, 255),
           anchor="ma")
d.text((MAP[0] + 4, MAP[3] - 12), "N ↑", font=font(SANS_B, 9), fill=INK)

# ALSO list (two columns)
AX0 = 552
d.text((AX0, MY0), "ALSO ON MONDAY — 18 MORE STORIES", font=font(SANS_B, 12),
       fill=RED)
ALSO = [
    ("MIDDLE EAST", RED, [
        "14 Gaza: two killed in Israeli strike",
        "15 West Bank: settler attacks hit villages",
        "16 Iran war: no deal in sight",
        "17 Lebanon seizes 264 kg of explosives",
        "18 Bahrain: Iranian strike hits plant, 2 hurt"]),
    ("AFRICA", (150, 90, 20), [
        "19 Sudan: air defences down drones",
        "20 DRC: fighting traps Ebola teams"]),
    ("WORLD", (90, 90, 90), [
        "31 States sue SpaceX over AI safety claims"]),
    ("ASIA-PACIFIC", (22, 130, 110), [
        "21 Bangladesh: Hasina jailed if she returns",
        "22 Seoul minister quits over AI exam chaos",
        "23 SK Telecom -7.3% as Anthropic hype cools",
        "24 China eases margin rules to calm rout",
        "25 Seoul readies 10T-won stabilisation fund"]),
    ("NORTH AMERICA", BLUE, [
        "26 Bessent demands Nvidia answers",
        "27 FBI probes hack of police database",
        "28 Trump: Iran strikes may resume in New Year",
        "29 US futures jump 3% holiday week",
        "30 Tom Jackson dies at 75"]),
]
col_w = 224
ay = MY0 + 18
col = 0
for gname, gcol, items in ALSO:
    cx = AX0 + col * (col_w + 8)
    d.text((cx, ay), gname, font=font(SANS_B, 10), fill=gcol)
    ay += 13
    for it in items:
        f = font(SANS, 9)
        while d.textlength(it, font=f) > col_w and len(it) > 4:
            it = it[:-1]
        d.text((cx, ay), it, font=f, fill=INK)
        ay += 11
    ay += 3
    if gname == "WORLD":
        col = 1
        ay = MY0 + 18

# -------------------------------------------------------------- DATE CHECK
DY = 884
d.rectangle([16, DY, W - 16, DY + 62], outline=RED, width=2, fill=(255, 244, 242))
d.text((24, DY + 5), "DATE CHECK", font=font(SANS_B, 12), fill=RED)
d.text((W - 24, DY + 5), "WIRES READ UP TO 23:00 UTC", font=font(SANS_B, 9),
       fill=RED, anchor="ra")
d.text((24, DY + 21),
       "Every story above happened or was first reported on Monday 23 November 2026.",
       font=font(SANS_B, 10), fill=INK)
d.text((24, DY + 35),
       "LEFT OUT (not 23 Nov): Democrats reach 258 (22 Nov) · Sparta II fire (22 Nov) · El Chapo Isidro captured (22 Nov) ·",
       font=font(SANS, 9), fill=INK)
d.text((24, DY + 47),
       "EU–Indonesia pact (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov).  NOT YET: Dymer search continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO evacuating trapped Ebola staff.",
       font=font(SANS, 9), fill=INK)

# ------------------------------------------------------------------ footer
FY = 954
d.text((16, FY),
       "SOURCES: AP · Reuters · Bloomberg · AFP · CNN · ESPN · UN News · WHO · Kyiv · Lowy Institute · Korea JoongAng · Morningstar",
       font=font(SANS, 9), fill=GREY)
d.text((16, FY + 13),
       "CONFIRMED = 2+ outlets · REPORTED = carried by a named source · CLAIM = one side alleges · ONGOING = developing.  Red pin = reported · Amber pin = claim (unverified) · Blue pin = ongoing.",
       font=font(SANS, 9), fill=GREY)
d.text((16, FY + 26), "THE WORLD TODAY · 23 NOV 2026",
       font=font(SANS_B, 9), fill=INK)
d.text((W - 16, FY + 26), "Scenes are drawn illustrations, not photographs.",
       font=font(SANS, 9), fill=GREY, anchor="ra")
d.line([16, FY + 42, W - 16, FY + 42], fill=LINE, width=1)

img.save("entry.png")
print("saved entry.png", img.size)
