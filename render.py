# render.py — draws the 24 November 2026 front page as vector art + system-font text.
# Every letter is rendered from a system font; every picture is original vector art
# built from PIL shapes. No photographs, no copied artwork, no image-generator output.
# Run: python3 render.py  -> writes entry.png (1024x1024, < 1 MiB), deterministic.
import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 36                      # page margin
CW = W - 2 * M              # content width = 952
PAPER = (248, 244, 232)
INK = (20, 20, 20)
RED = (178, 33, 30)
BLUE = (31, 78, 121)
GREEN = (46, 125, 50)
GREY = (90, 88, 82)
LIGHT = (233, 228, 213)
CHIPGREEN = (118, 185, 0)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, font, max_w, fill=INK, leading=None):
    """Draw wrapped paragraph; returns y after the last line."""
    leading = leading or int(font.size * 1.32)
    for line in wrap(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def rule(draw, x, y, w, weight=2, fill=INK):
    draw.rectangle([x, y, x + w, y + weight - 1], fill=fill)
    return y + weight


def double_rule(draw, x, y, w):
    rule(draw, x, y, w, 3)
    rule(draw, x, y + 6, w, 1)
    return y + 10


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
y = 18
rule(d, M, y, CW, 3)
y += 10
mast = F(SERIF_B, 80)
title = "THE WORLD TODAY"
tw = d.textlength(title, font=mast)
d.text(((W - tw) / 2, y), title, font=mast, fill=INK)
y += 98
rule(d, M, y, CW, 1)
y += 6
# dateline bar
small = F(SANS_B, 19)
date_f = F(SANS_B, 24)
d.text((M, y), "WORLD NEWS", font=small, fill=RED)
date = "TUESDAY, 24 NOVEMBER 2026"
dw = d.textlength(date, font=date_f)
d.text(((W - dw) / 2, y - 3), date, font=date_f, fill=INK)
right = "ONE PAGE  \u2022  EVERY STORY"
rw = d.textlength(right, font=small)
d.text((W - M - rw, y), right, font=small, fill=GREY)
y += 30
y = double_rule(d, M, y, CW)
y += 4

# ---------------------------------------------------------------- lead story
kicker = F(SANS_B, 20)
d.text((M, y), "TECH  \u2022  NVIDIA COMEBACK", font=kicker, fill=RED)
y += 28
head = F(SERIF_B, 54)
for line in ["NVIDIA BRINGS BACK HUANG", "AFTER TRUMP INTERVENTION"]:
    d.text((M, y), line, font=head, fill=INK)
    y += 62
y += 2
# lead illustration (right) + deck/body (left)
ILL_X, ILL_Y, ILL_W, ILL_H = W - M - 300, y, 300, 180
TEXT_W = ILL_X - M - 24
deck = F(SANS_B, 21)
y2 = para(d, M, y, "The board unanimously reinstates Jensen Huang as chief "
        "executive, 11 days after he quit over revelations of affairs \u2014 "
        "including one with a woman US officials suspect of spying for China.",
        deck, TEXT_W, leading=27)
y2 += 6
body = F(SANS, 16)
y2 = para(d, M, y2, "President Donald Trump says he pressed the board "
        "personally and sent Vice-President JD Vance as his emissary. The "
        "board says it consulted senior US officials and is confident the "
        "return poses no national security risk.",
        body, TEXT_W, leading=21)
# --- vector art: a green chip under a rising market arrow ---
ix, iy, iw, ih = ILL_X, ILL_Y, ILL_W, ILL_H
d.rectangle([ix, iy, ix + iw, iy + ih], fill=(226, 240, 210), outline=INK, width=2)
# rising chart line with arrowhead, across the top of the panel
pts = [(ix + 16, iy + 52), (ix + 70, iy + 40), (ix + 110, iy + 46),
       (ix + 160, iy + 28), (ix + 210, iy + 34), (ix + 262, iy + 16)]
d.line(pts, fill=GREEN, width=5, joint="curve")
d.polygon([(ix + 262, iy + 16), (ix + 242, iy + 12), (ix + 258, iy + 34)],
          fill=GREEN)
# chip
cx0, cy0, cs = ix + 114, iy + 66, 72
for px in range(cx0 + 12, cx0 + cs - 8, 18):
    d.line([px, cy0 - 10, px, cy0], fill=INK, width=4)
    d.line([px, cy0 + cs, px, cy0 + cs + 10], fill=INK, width=4)
for py in range(cy0 + 12, cy0 + cs - 8, 18):
    d.line([cx0 - 10, py, cx0, py], fill=INK, width=4)
    d.line([cx0 + cs, py, cx0 + cs + 10, py], fill=INK, width=4)
d.rectangle([cx0, cy0, cx0 + cs, cy0 + cs], fill=(30, 30, 30),
            outline=CHIPGREEN, width=3)
d.rectangle([cx0 + 14, cy0 + 14, cx0 + cs - 14, cy0 + cs - 14],
            outline=CHIPGREEN, width=2)
d.text((cx0 + 22, cy0 + 24), "AI", font=F(SANS_B, 26), fill=CHIPGREEN)
d.text((ix + 8, iy + ih - 22), "SHARES SOAR BY A THIRD", font=F(SANS_B, 13), fill=INK)

y = max(y2, ILL_Y + ILL_H) + 10
y = double_rule(d, M, y, CW)
y += 8

# ------------------------------------------------------- secondary stories
def jet_icon(draw, x, y, s):
    """Fighter jet silhouette over a radar sweep."""
    draw.arc([x + 8, y + 4, x + 88, y + 84], 200, 340, fill=BLUE, width=3)
    draw.polygon([(x + 48, y + 6), (x + 56, y + 30), (x + 52, y + 58),
                  (x + 44, y + 58), (x + 40, y + 30)], fill=(52, 68, 88))
    draw.polygon([(x + 40, y + 34), (x + 8, y + 52), (x + 40, y + 46)],
                 fill=(52, 68, 88))
    draw.polygon([(x + 56, y + 34), (x + 88, y + 52), (x + 56, y + 46)],
                 fill=(52, 68, 88))
    draw.polygon([(x + 44, y + 58), (x + 40, y + 74), (x + 48, y + 70),
                  (x + 52, y + 74), (x + 56, y + 70)], fill=(52, 68, 88))


def tanker_icon(draw, x, y, s):
    """Oil tanker with a flame above it."""
    draw.rectangle([x, y + 30, x + 96, y + 50], fill=(120, 40, 30))
    draw.rectangle([x + 70, y + 12, x + 88, y + 30], fill=(120, 40, 30))
    draw.rectangle([x + 8, y + 20, x + 24, y + 30], fill=(120, 40, 30))
    draw.polygon([(x + 44, y + 26), (x + 52, y + 4), (x + 60, y + 26)],
                 fill=(232, 120, 20))
    draw.polygon([(x + 48, y + 26), (x + 52, y + 14), (x + 56, y + 26)],
                 fill=(250, 200, 40))
    for wy in (58, 66):
        draw.arc([x, y + wy - 8, x + 96, y + wy + 8], 0, 180, fill=BLUE, width=3)


def ship_icon(draw, x, y, s):
    """Warship silhouette on waves, listing to one side."""
    draw.polygon([(x, y + 34), (x + 14, y + 34), (x + 22, y + 22), (x + 74, y + 22),
                  (x + 86, y + 34), (x + 96, y + 34), (x + 88, y + 50), (x + 8, y + 50)],
                 fill=(52, 68, 88))
    draw.rectangle([x + 34, y + 8, x + 40, y + 22], fill=(52, 68, 88))
    draw.rectangle([x + 52, y + 14, x + 58, y + 22], fill=(52, 68, 88))
    for wy in (58, 66):
        draw.arc([x, y + wy - 8, x + 96, y + wy + 8], 0, 180, fill=BLUE, width=3)
    draw.line([x + 6, y + 30, x + 90, y + 30], fill=(232, 84, 24), width=3)
    d2 = draw
    d2.polygon([(x + 60, y + 22), (x + 66, y + 2), (x + 72, y + 22)],
               fill=(232, 120, 20))


def ballot_icon(draw, x, y, s):
    """Ballot box with a ballot slip and a circle of stars."""
    for k in range(12):
        a = math.radians(k * 30 - 90)
        sx = x + 48 + int(34 * math.cos(a))
        sy = y + 40 + int(34 * math.sin(a))
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(250, 200, 40))
    draw.rectangle([x + 18, y + 44, x + 78, y + 76], fill=BLUE)
    draw.rectangle([x + 38, y + 40, x + 58, y + 44], fill=INK)
    draw.rectangle([x + 40, y + 20, x + 56, y + 40], fill=(248, 244, 232),
                   outline=INK, width=2)
    draw.line([x + 44, y + 30, x + 48, y + 34], fill=RED, width=3)
    draw.line([x + 48, y + 34, x + 54, y + 26], fill=RED, width=3)


STORIES = [
    ("THE GULF  \u2022  ESCALATION", "Iran steps up Gulf strikes, sues for $290bn",
     "Tehran hits US bases and civilian sites in the Gulf after a lull, "
     "as a US naval blockade and sanctions squeeze the country. Iran calls "
     "the blockade \u201cmilitary aggression\u201d.", tanker_icon),
    ("KOREA  \u2022  AIRSPACE ALERT", "Russian jets enter Seoul\u2019s defence zone",
     "Multiple Russian warplanes enter South Korea\u2019s air defence zone "
     "without notice, and Seoul issues an emergency alert for Ulleung "
     "Island. Moscow also warns Finland and Estonia.", jet_icon),
    ("LIBYA  \u2022  WAR AT SEA", "Ukraine says it sank a Russian warship",
     "Kyiv claims seven sea drones sank the corvette Merkury off Benghazi "
     "and hit a cargo ship. Russia vows a response and warns of a "
     "\u201cdangerous trend\u201d in attacks on its shipping.", ship_icon),
    ("EUROPE  \u2022  SANCTIONS & VOTES", "EU targets Russian sport in 22nd package",
     "The European Commission proposes banning Russian teams from EU events "
     "and curbing crypto channels. In Spain, final polls put the right on "
     "course to oust S\u00e1nchez on 29 November.", ballot_icon),
]

CELL_W = (CW - 24) // 2
CELL_H = 150
kick_f = F(SANS_B, 15)
head_f = F(SERIF_B, 25)
body_f = F(SANS, 15)
start_y = y
for i, (kick, head, body, icon) in enumerate(STORIES):
    cx = M + (i % 2) * (CELL_W + 24)
    cy = start_y + (i // 2) * (CELL_H + 8)
    icon(d, cx, cy + 6, 96)
    tx = cx + 108
    d.text((tx, cy), kick, font=kick_f, fill=RED)
    hy = para(d, tx, cy + 22, head, head_f, CELL_W - 108, leading=28)
    para(d, tx, hy + 2, body, body_f, CELL_W - 108, leading=18)
    if i % 2 == 0:
        d.line([cx + CELL_W + 12, cy, cx + CELL_W + 12, cy + CELL_H - 12],
               fill=GREY, width=1)
y = start_y + 2 * CELL_H + 14
y = double_rule(d, M, y, CW)
y += 8

# ---------------------------------------------------------------- bottom strip
d.text((M, y), "ALSO TODAY", font=F(SANS_B, 17), fill=RED)
y += 24
COL_W = (CW - 48) // 3
bottom = [
    ("BUSINESS", "CrowdStrike agrees to buy Zscaler in a $44bn deal as "
     "AI attacks drive mergers."),
    ("LAW  \u2022  AI", "Virginia and Oregon sue SpaceX over Grok AI sexual "
     "imagery, seeking an injunction."),
    ("HEALTH", "England launches the largest AI breast-screening trial, "
     "for 700,000 women."),
]
bx = M
for label, text in bottom:
    d.text((bx, y), label, font=F(SANS_B, 15), fill=BLUE)
    para(d, bx, y + 22, text, F(SANS, 14), COL_W, leading=18)
    bx += COL_W + 24
y += 22 + 2 * 18 + 8
y = rule(d, M, y, CW, 1)
y += 8
d.text((M, y), "Sources: Reuters  \u2022  BBC  \u2022  CNN  \u2022  Al Jazeera  \u2022  "
       "France 24  \u2022  Yonhap  \u2022  The Straits Times  \u2022  Drawn from the "
       "day\u2019s reporting; every picture is original vector art.",
       font=F(SANS, 12), fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
