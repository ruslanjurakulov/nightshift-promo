"""Nox, the night-owl mascot, drawn in code (original character, no stock art).

Drawn at 2x and downsampled for clean edges. Colours come from the day's palette, so Nox is a different colour every day
while staying recognisably the same owl: round body, ear tufts, big eyes, a lit headlamp, and a scarf.
"""
import math
import numpy as np
from PIL import Image, ImageDraw

CX0, CX1, CY0, CY1 = -430, 430, -690, 60      # local canvas (units); (0,0) = centre of the feet


def _ell(cx, cy, rx, ry, n=48):
    th = np.linspace(0, 2 * math.pi, n, endpoint=False)
    return np.stack([cx + rx * np.cos(th), cy + ry * np.sin(th)], 1)


def _wing(side, theta):
    sx, sy = 178 * side, -385
    cxw, cyw = sx + side * 95 * math.sin(theta), sy + 95 * math.cos(theta)
    p = _ell(0, 0, 40, 112); rot = -side * theta; c, s = math.cos(rot), math.sin(rot)
    return np.stack([cxw + p[:, 0] * c - p[:, 1] * s, cyw + p[:, 0] * s + p[:, 1] * c], 1)


def owl_layer(pal, K, wR, wL, look, mouth, blink, squint, sway, SS=2):
    sc = K * SS
    w, h = int((CX1 - CX0) * sc), int((CY1 - CY0) * sc)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    body, belly, wing, line, acc, acc2, beak = (tuple(pal[k]) for k in ("owl_body", "owl_belly", "owl_wing", "owl_line", "accent", "accent2", "beak"))
    A = lambda c, a=255: (*c, a)
    P = lambda pts: [((x - CX0) * sc, (y - CY0) * sc) for x, y in pts]
    lw = lambda v: max(1, int(v * sc))

    def poly(pts, fill, ol=None, wd=0): d.polygon(P(pts), fill=A(fill), outline=A(ol) if ol else None, width=lw(wd) if wd else 1)

    def ell(cx, cy, rx, ry, fill, ol=None, wd=0, a=255):
        d.ellipse([(cx - rx - CX0) * sc, (cy - ry - CY0) * sc, (cx + rx - CX0) * sc, (cy + ry - CY0) * sc],
                  fill=A(fill, a), outline=A(ol) if ol else None, width=lw(wd) if wd else 1)

    ell(0, -6, 195, 16, (0, 0, 0), a=70)                                            # contact shadow
    ell(-70, -12, 46, 20, beak, line, 4); ell(70, -12, 46, 20, beak, line, 4)       # feet
    poly([(-175, -455), (-205, -615), (-85, -520)], body, line, 5); poly([(175, -455), (205, -615), (85, -520)], body, line, 5)   # ear tufts
    poly([(-165, -470), (-190, -585), (-105, -515)], wing); poly([(165, -470), (190, -585), (105, -515)], wing)
    ell(0, -275, 205, 265, body, line, 5)                                           # body
    ell(0, -165, 130, 150, belly, wing, 4)                                          # belly
    for r, y0 in enumerate([-215, -160, -105, -50]):
        n = 4 - (r % 2)
        for k in range(n):
            xx = (k - (n - 1) / 2) * 52
            d.arc([(xx - 26 - CX0) * sc, (y0 - 22 - CY0) * sc, (xx + 26 - CX0) * sc, (y0 + 22 - CY0) * sc], 20, 160, fill=A(wing), width=lw(4))
    # scarf: band across the chest + a tail that sways
    top = lambda x: -300 - 18 * (x / 200) ** 2
    xs = list(range(-190, 191, 10))
    band = [(x, top(x)) for x in xs] + [(x, top(x) + 38) for x in reversed(xs)]
    poly(band, acc2, line, 4)
    for x in range(-170, 171, 68): d.line(P([(x, top(x) + 4), (x + 22, top(x) + 34)]), fill=A((255, 255, 255), 150), width=lw(7))
    poly([(95, top(95) + 22), (150, top(150) + 18), (168 + sway, -150), (112 + sway, -142)], acc2, line, 4)
    d.line(P([(118, -225), (140 + sway * 0.9, -215)]), fill=A((255, 255, 255), 150), width=lw(7))
    # headband + lamp
    d.arc([(-196 - CX0) * sc, (-540 - CY0) * sc, (196 - CX0) * sc, (-260 - CY0) * sc], 215, 325, fill=A((50, 40, 60)), width=lw(15))
    ell(0, -522, 31, 31, acc, (50, 40, 60), 8); ell(-8, -530, 9, 9, (255, 255, 255))
    # eyes
    for ex in (-86, 86):
        ey = -405
        ell(ex, ey, 84, 84, (255, 255, 255), line, 6)
        if squint > 0.5:
            d.arc([(ex - 46 - CX0) * sc, (ey - 22 - CY0) * sc, (ex + 46 - CX0) * sc, (ey + 40 - CY0) * sc], 200, 340, fill=A((30, 20, 40)), width=lw(10))
        else:
            ry = max(4, 40 * (1 - blink)); px, py = ex + look[0] * 24, ey + look[1] * 16
            ell(px, py, 40, ry, acc); ell(px, py, 28, max(3, ry * 0.7), (24, 18, 40))
            if blink < 0.5: ell(px - 11, py - 13 * (1 - blink), 10, 10 * (1 - blink) + 1, (255, 255, 255))
            if blink > 0.05:
                # lid = chord of the eye circle, so it never spills over the headband like a rectangle did
                dy = max(-83.0, min(83.0, -84 + 168 * blink)); phi = math.degrees(math.asin(dy / 84))
                d.chord([(ex - 84 - CX0) * sc, (ey - 84 - CY0) * sc, (ex + 84 - CX0) * sc, (ey + 84 - CY0) * sc], 180 - phi, 360 + phi, fill=A(body))
    # beak (opens with the voice)
    poly([(-20, -330), (20, -330), (0, -322 + 14 + 22 * mouth)], tuple(int(c * 0.65) for c in beak), line, 2)
    poly([(-30, -362), (30, -362), (0, -320)], beak, line, 3)
    # wings in front
    poly(_wing(1, wR), wing, line, 5); poly(_wing(-1, wL), wing, line, 5)
    # premultiplied resize: no dark fringes at the soft edges
    return im.convert("RGBa").resize((int((CX1 - CX0) * K), int((CY1 - CY0) * K)), Image.LANCZOS).convert("RGBA")
