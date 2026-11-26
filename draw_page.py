#!/usr/bin/env python3
"""Paint the Wednesday 25 November 2026 front page of THE WORLD.

Twelve stories from one day, three columns, and a real news
photograph beside every story: the pictures are file photos from
Wikimedia Commons, shown whole (contain-fit, never cropped) with a
credit under each one. Headlines and body use Playfair Display and
PT Serif; kickers and labels use Oswald — all OFL fonts from
Google Fonts.

This is a build-time script only. It reads nothing but files in
this repository (fonts/*.ttf, photos/*) and paints one deterministic
1024x1024 PNG: no clock, no randomness, no network, so running it
twice gives the same bytes. Pillow is needed only here; main.py,
the entrypoint, is standard library only and copies the PNG.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024

PAPER = (247, 243, 232)   # warm newsprint background
MAT = (233, 228, 213)     # photo mat behind contain-fit photos
INK = (17, 17, 17)        # body ink
RED = (176, 30, 30)       # kicker and date red
GREY = (96, 96, 92)       # captions and standfirst
HAIR = (150, 144, 128)    # hairline rules

MX = 29                   # side margin
COLW = 310                # column width
GAP = 18                  # gap between columns
COLX = [MX, MX + COLW + GAP, MX + 2 * (COLW + GAP)]

PLAYFAIR = HERE / "fonts" / "PlayfairDisplay.ttf"
PTSERIF = HERE / "fonts" / "PTSerif-Regular.ttf"
PTSERIF_IT = HERE / "fonts" / "PTSerif-Italic.ttf"
PTSERIF_B = HERE / "fonts" / "PTSerif-Bold.ttf"
OSWALD = HERE / "fonts" / "Oswald.ttf"


def load_font(path, size, weight=None):
    """Load a TTF (possibly variable) at a size and weight."""
    f = ImageFont.truetype(str(path), size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f


MAST = lambda s: load_font(PLAYFAIR, s, 900)
HEAD = lambda s: load_font(PLAYFAIR, s, 700)
BODY = lambda s: load_font(PTSERIF, s)
CAP = lambda s: load_font(PTSERIF_IT, s)
KICK = lambda s: load_font(OSWALD, s, 600)


def font_height(f):
    asc, desc = f.getmetrics()
    return asc + desc


def wrap(draw, text, f, width, max_lines=None):
    """Greedy word wrap; returns a list of lines (at most max_lines)."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
            if max_lines and len(lines) >= max_lines:
                cur = ""
                break
    if cur:
        lines.append(cur)
    if max_lines:
        lines = lines[:max_lines]
    return lines


def draw_tracked(draw, x, y, s, f, fill, tracking=1):
    """Draw text with extra tracking between characters; returns width."""
    cx = x
    for ch in s:
        draw.text((cx, y), ch, font=f, fill=fill)
        cx += draw.textlength(ch, font=f) + tracking
    return cx - x - tracking


def draw_centered(draw, cx, y, s, f, fill, tracking=1):
    """Draw tracked text centred on cx."""
    w = sum(draw.textlength(ch, font=f) + tracking for ch in s) - tracking
    draw_tracked(draw, cx - w / 2, y, s, f, fill, tracking)


# ---------------------------------------------------------------- stories
# Every story is a real event of Wednesday 25 November 2026, as reported
# that day. Photos are file pictures from Wikimedia Commons, credited
# beneath each image; none is presented as taken at the event itself.
STORIES = [
    dict(photo="hormuz.jpg", kicker="THE GULF — LEAD",
         headline="Two tankers hit by mines in the Strait of Hormuz",
         summary="Iran's Guard said two oil tankers struck naval mines and caught fire crossing the strait.",
         credit="Photo: DVIDSHUB"),
    dict(photo="riyadh.jpg", kicker="SAUDI ARABIA",
         headline="Houthis strike Riyadh tower and a Saudi refinery",
         summary="Yemen's Houthis said they hit the Ras Tanura refinery and a Riyadh tower, injuring 11.",
         credit="Photo: Wajahat Mahmood"),
    dict(photo="gaza.jpg", kicker="GAZA",
         headline="Israel kills Hamas security chief and his family",
         summary="Israel killed Hamas colonel Mohammad Abuelouf, his wife and two children, Gaza medics said.",
         credit="Photo: WAFA / APAimages"),
    dict(photo="kyiv.jpg", kicker="UKRAINE",
         headline="Russian strikes kill two in Odesa and hit Kyiv",
         summary="A Russian strike on Odesa killed two and injured three; Kyiv was hit again, its mayor said.",
         credit="Photo: Kyiv City Administration"),
    dict(photo="sudan.jpg", kicker="SUDAN",
         headline="RSF drones kill nineteen in Sudan's Blue Nile",
         summary="The RSF killed 19 civilians and wounded 20 in drone strikes on two cities, monitors said.",
         credit="Photo: INPE"),
    dict(photo="pope.jpg", kicker="CLIMATE — COP31",
         headline="Climate talks fail as Pope warns of extremes",
         summary="COP31 ended without a deal, and Pope Leo XIV warned extreme weather was growing more frequent.",
         credit="Photo: Edgar Beltrán / The Pillar"),
    dict(photo="solomon.jpg", kicker="THE PACIFIC",
         headline="Solomon Islands signs treaty barring foreign bases",
         summary="The Solomon Islands and Australia signed a treaty barring any foreign military base there.",
         credit="Photo: Jenny Scott"),
    dict(photo="huawei.jpg", kicker="TECHNOLOGY",
         headline="Huawei convicted in US court over trade secrets",
         summary="A US court found Huawei guilty of stealing trade secrets and bank fraud, but not racketeering.",
         credit="Photo: RG72"),
    dict(photo="shenzhou.jpg", kicker="SPACE",
         headline="China carries Pakistan's first astronaut to orbit",
         summary="Shenzhou-24 docked at Tiangong with a Pakistani aboard, the first foreign astronaut China flew.",
         credit="Photo: China News Service"),
    dict(photo="trump.jpg", kicker="UNITED STATES",
         headline="Trump to unveil new tariffs on fourteen economies",
         summary="The Trump administration was set to unveil new tariffs on 14 major economies, sources said.",
         credit="Photo: The White House"),
    dict(photo="netanyahu.jpg", kicker="ISRAEL",
         headline="Judges urge dropping key Netanyahu bribery case",
         summary="Jerusalem judges urged prosecutors to drop the gravest bribery case against Netanyahu.",
         credit="Photo: Dan Scavino"),
    dict(photo="dhaka.jpg", kicker="BANGLADESH",
         headline="Dhaka raises garment wage after protests",
         summary="Bangladesh raised garment workers' minimum wage by 36% to $139 after violent protests.",
         credit="Photo: Fahad Faisal"),
]


def story_height(draw, st, photo_h, head_size, max_sum_lines=2):
    """Height of one story block (photo + text) at the given settings."""
    h = photo_h + 5
    h += font_height(KICK(10)) + 2
    head = wrap(draw, st["headline"], HEAD(head_size), COLW, max_lines=2)
    h += len(head) * (head_size + 3) + 3
    summ = wrap(draw, st["summary"], BODY(10), COLW, max_lines=max_sum_lines)
    h += len(summ) * 13 + 2
    h += font_height(CAP(8))
    return h


def measure(draw, photo_h, head_size):
    """Aligned row heights: row r is as tall as the tallest of its three
    stories, so every row starts at the same y in all three columns."""
    heights = [story_height(draw, st, photo_h, head_size) for st in STORIES]
    rows = [max(heights[r], heights[4 + r], heights[8 + r]) for r in range(4)]
    total = sum(rows) + 3 * 10
    return total, heights, rows


def draw_story(draw, st, x, y, photo_h, head_size, photos):
    """Draw one story block; returns its height."""
    top = y
    # photo, contain-fit (whole photo visible, never cropped)
    im = photos[st["photo"]]
    bw, bh = COLW, photo_h
    scale = min(bw / im.width, bh / im.height)
    nw, nh = max(1, int(im.width * scale)), max(1, int(im.height * scale))
    thumb = im.resize((nw, nh), Image.LANCZOS)
    draw.rectangle([x, y, x + bw, y + bh], fill=MAT, outline=HAIR, width=1)
    draw._image.paste(thumb, (x + (bw - nw) // 2, y + (bh - nh) // 2))
    y += bh + 5
    # kicker
    draw_tracked(draw, x, y, st["kicker"], KICK(10), RED, tracking=1)
    y += font_height(KICK(10)) + 2
    # headline (max 2 lines)
    for ln in wrap(draw, st["headline"], HEAD(head_size), COLW, max_lines=2):
        draw.text((x, y), ln, font=HEAD(head_size), fill=INK)
        y += head_size + 3
    y += 3
    # summary (max 2 lines)
    for ln in wrap(draw, st["summary"], BODY(10), COLW, max_lines=2):
        draw.text((x, y), ln, font=BODY(10), fill=INK)
        y += 13
    y += 2
    # credit
    draw.text((x, y), st["credit"], font=CAP(8), fill=GREY)
    y += font_height(CAP(8))
    return y - top


def main():
    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "entry.png"
    photos = {}
    for st in STORIES:
        im = Image.open(HERE / "photos" / st["photo"]).convert("RGB")
        photos[st["photo"]] = im

    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)

    # ---- masthead ------------------------------------------------------
    y = 14
    draw.line([(MX, y), (W - MX, y)], fill=INK, width=2)
    y += 8
    mast = "THE WORLD"
    mf = MAST(48)
    draw.text(((W - draw.textlength(mast, font=mf)) / 2, y), mast,
              font=mf, fill=INK)
    y += 56
    draw_centered(draw, W / 2, y, "WEDNESDAY, 25 NOVEMBER 2026",
                  KICK(14), RED, tracking=2)
    y += 20
    stand = ("Twelve stories, each with its own photograph — from the Strait "
             "of Hormuz to the Tiangong station.")
    sf = CAP(12)
    draw.text(((W - draw.textlength(stand, font=sf)) / 2, y), stand,
              font=sf, fill=GREY)
    y += 18
    draw.line([(MX, y), (W - MX, y)], fill=INK, width=3)
    y += 4
    draw.line([(MX, y), (W - MX, y)], fill=INK, width=1)
    content_top = y + 8
    footer_rule_y = H - 26

    # ---- fit: shrink photo height until the three columns fit ----------
    avail = footer_rule_y - content_top
    photo_h, head_size = 136, 15
    while True:
        total, heights, rows = measure(draw, photo_h, head_size)
        if total <= avail or (photo_h <= 104 and head_size <= 14):
            break
        if photo_h > 104:
            photo_h -= 8
        else:
            head_size -= 1
    print("photo_h=%d head=%d row_heights=%s total=%d avail=%d"
          % (photo_h, head_size, rows, total, avail))
    assert total <= avail, "rows do not fit: %d > %d" % (total, avail)

    # ---- column rules ----------------------------------------------------
    for cx in (COLX[1] - GAP // 2, COLX[2] - GAP // 2):
        draw.line([(cx, content_top), (cx, footer_rule_y)], fill=HAIR, width=1)

    # ---- stories, 4 per column, each row the same height in all columns --
    for ci in range(3):
        y = content_top
        for r in range(4):
            draw_story(draw, STORIES[ci * 4 + r], COLX[ci], y,
                       photo_h, head_size, photos)
            y += rows[r] + 10

    # ---- footer ------------------------------------------------------------
    draw.line([(MX, footer_rule_y), (W - MX, footer_rule_y)], fill=INK, width=1)
    foot = ("Photographs: Wikimedia Commons — file pictures, credited beneath "
            "each image. A one-day front page for Wednesday, 25 November 2026.")
    ff = BODY(9)
    draw.text(((W - draw.textlength(foot, font=ff)) / 2, footer_rule_y + 6),
              foot, font=ff, fill=GREY)

    page.save(out_path, "PNG", optimize=True)
    print("wrote %s (%d bytes)" % (out_path, out_path.stat().st_size))


if __name__ == "__main__":
    main()
