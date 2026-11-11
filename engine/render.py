#!/usr/bin/env python3
"""Frame renderer. Design space is 1920x1080 units; K scales to pixels (K=2 -> 4K 3840x2160).

usage: render.py timeline.json K preview t1,t2,...   -> PNG previews into ./prev
       render.py timeline.json K seg out.mp4 f0 f1   -> encode frames [f0,f1) (silent; build.py joins segments + audio)
"""
import json, math, os, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import nox

TL = json.load(open(sys.argv[1])); K = float(sys.argv[2]); MODE = sys.argv[3]
W, H = int(1920 * K), int(1080 * K); FPS = 30; DUR = TL["total"]
PAL = {k: (tuple(v) if isinstance(v, list) and v and isinstance(v[0], int) else v) for k, v in TL["palette"].items()}
ACC, ACC2, GOOD = PAL["accent"], PAL["accent2"], PAL["good"]
WHITE, MUTED = (255, 255, 255), (200, 200, 225)
ENV = np.load(TL["env"])
GF, IF = "/usr/share/fonts/truetype/google-fonts/", "/usr/share/fonts/opentype/inter/"
HEAD, MEDF, BODY, BODYB = GF + "Poppins-Bold.ttf", GF + "Poppins-Medium.ttf", IF + "Inter-Regular.otf", IF + "Inter-SemiBold.otf"
OX, OY = 500, 960                      # Nox's feet
CXC = 1290                             # centre of the content column (right of Nox)


def U(x): return int(round(x * K))
def ease(t): t = min(max(t, 0), 1); return 1 - (1 - t) ** 3
def eio(t): t = min(max(t, 0), 1); return t * t * (3 - 2 * t)
def back(t): t = min(max(t, 0), 1); c = 1.70158; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def win(t, a, b): return min(max((t - a) / (b - a), 0), 1)
def fade(t, a0, a1, b0, b1): return eio(win(t, a0, a1)) * (1 - eio(win(t, b0, b1)))
def A(t, t0, d=0.4): return ease(win(t, t0, t0 + d))
def rgba(c, a=1.0): return (*c, int(max(0, min(1, a)) * 255))
def mix(c1, c2, f): return tuple(int(c1[i] + (c2[i] - c1[i]) * f) for i in range(3))


# ---------- text ----------
_fc, _tc = {}, {}
def F(path, size):
    k = (path, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, U(size))
    return _fc[k]
def text_layer(txt, path, size, sp=0):
    k = (txt, path, size, sp)
    if k in _tc: return _tc[k]
    f = F(path, size); s = U(sp)
    ws = [f.getlength(c) for c in txt] if sp else None
    w = (int(sum(ws) + s * (len(txt) - 1)) if sp else int(f.getlength(txt))) + U(12); h = int(size * K * 1.7)
    im = Image.new("L", (w, h), 0); d = ImageDraw.Draw(im)
    if not sp: d.text((U(6), h // 2), txt, font=f, fill=255, anchor="lm")
    else:
        x = U(6)
        for c, wc in zip(txt, ws): d.text((x, h // 2), c, font=f, fill=255, anchor="lm"); x += wc + s
    _tc[k] = im; return im
def put(cv, layer, cx, cy, a=1.0, color=WHITE, left=False):
    if a <= 0.004: return
    m = layer if a >= 0.995 else layer.point(lambda v, a=a: int(v * a))
    cv.paste(color, (int(U(cx)) if left else int(U(cx) - layer.width / 2), int(U(cy) - layer.height / 2)), m)
def tw(layer): return layer.width / K
def rr(D, box, r, fill=None, outline=None, w=2):
    D.rounded_rectangle([U(box[0]), U(box[1]), U(box[2]), U(box[3])], radius=U(r), fill=fill, outline=outline, width=U(w) if outline else 0)
def glass(D, box, r, a, edge=None, w=2, tint=None):
    rr(D, box, r, fill=rgba(tint or WHITE, 0.10 * a if not tint else 0.16 * a), outline=rgba(edge or WHITE, 0.30 * a), w=w)
def pill(cv, D, cx, cy, text, a, size=30, filled=False, h=76, color=None, fnt=MEDF, minw=0, dx=0):
    if a <= 0.004: return
    l = text_layer(text, fnt, size); w = max(minw, tw(l) + 70); dx = dx + (1 - ease(a)) * 20
    if filled:
        rr(D, (cx - w / 2 + dx, cy - h / 2, cx + w / 2 + dx, cy + h / 2), h / 2, fill=rgba(color or ACC, a))
        put(cv, l, cx + dx, cy, a, color=(24, 16, 40))
    else:
        glass(D, (cx - w / 2 + dx, cy - h / 2, cx + w / 2 + dx, cy + h / 2), h / 2, a, edge=color)
        put(cv, l, cx + dx, cy, a)
def label(cv, txt, cx, cy, a, size=22, color=MUTED): put(cv, text_layer(txt, BODYB, size, 5), cx, cy, 0.85 * a, color=color)


# ---------- logos ----------
def _prep(path):
    im = Image.open(path).convert("L"); a = np.asarray(im); ys, xs = np.where(a > 40)
    return im.crop((xs.min() - 4, ys.min() - 4, xs.max() + 5, ys.max() + 5))
LOCK = _prep(os.path.join(ROOT, "assets", "lockup.png")); _lk = {}
def put_lock(cv, cx, cy, wu, a):
    if a <= 0.004: return
    if wu not in _lk:
        w = U(wu); h = int(LOCK.height * w / LOCK.width); g = np.asarray(LOCK.resize((w, h), Image.LANCZOS)).astype(np.float32) / 255
        _lk[wu] = Image.fromarray((np.clip((g - 0.28) / 0.22, 0, 1) * 255).astype(np.uint8))
    m = _lk[wu]; m = m if a >= 0.995 else m.point(lambda v: int(v * a))
    cv.paste(WHITE, (int(U(cx) - m.width / 2), int(U(cy) - m.height / 2)), m)


# ---------- living background ----------
_rng = np.random.default_rng(7)
NOISE = _rng.integers(-1, 2, (H, W, 1)).astype(np.int16)
GX, GY = np.meshgrid(np.linspace(0, 1, 320, dtype=np.float32), np.linspace(0, 1, 180, dtype=np.float32))
BASE = (np.array(PAL["bg0"], np.float32)[None, None] * (1 - GY[..., None]) + np.array(PAL["bg1"], np.float32)[None, None] * GY[..., None])
def background(t):
    g = BASE.copy()
    for i, col in enumerate(PAL["blobs"]):
        cx = 0.5 + 0.40 * math.sin(t * 0.21 + i * 2.1); cy = 0.5 + 0.36 * math.cos(t * 0.17 + i * 1.7)
        f = np.exp(-(((GX - cx) * 16 / 9) ** 2 + (GY - cy) ** 2) / (2 * 0.17 ** 2)) * (0.50 + 0.12 * math.sin(t * 0.9 + i))
        g += f[..., None] * np.array(col, np.float32)[None, None] * 0.55
    im = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
    return Image.fromarray(np.clip(np.asarray(im).astype(np.int16) + NOISE, 0, 255).astype(np.uint8))
random.seed(11)
BOKEH = [dict(x=random.uniform(0, 1920), y=random.uniform(0, 1080), v=random.uniform(5, 22), r=random.uniform(2, 9), a=random.uniform(.10, .38),
              ph=random.uniform(0, 6.28), c=random.choice([ACC, ACC2, WHITE, WHITE])) for _ in range(46)]


# ---------- Nox ----------
def pulse(t, wins, fi=0.2, fo=0.3):
    return max([eio(win(t, a, a + fi)) * (1 - eio(win(t, b - fo, b))) for a, b in wins] or [0])
_glow = None
def draw_owl(cv, D, t):
    global _glow
    O = TL["owl"]; bob = 5 * math.sin(t * 2.4); jump = 0
    for c in O["cheer"]:
        if 0 <= t - c < 0.6: jump = -64 * math.sin(math.pi * (t - c) / 0.6) ** 1.5
    wave = pulse(t, O["wave"]); point = pulse(t, O["point"]); cheer = max([eio(win(t, c - .05, c + .1)) * (1 - eio(win(t, c + .8, c + 1.2))) for c in O["cheer"]] or [0])
    wR = 0.2 + (0.9 + 0.35 * math.sin(t * 14)) * wave + 1.45 * point + 1.2 * cheer
    wL = 0.2 + 1.1 * cheer + 0.06 * math.sin(t * 2.4)
    look = (0.9, -0.1 + 0.15 * math.sin(t * 0.8))
    if point > 0.2: look = (0.85, 0.5 * point - 0.5)
    blink = 0
    for per, off in ((3.7, 0.0), (4.9, 1.9)):
        ph = (t + off) % per
        if ph < 0.2: blink = max(blink, 1 - abs(ph - 0.1) / 0.1)
    squint = 1 if any(a <= t < b for a, b in O["squint"]) else 0
    mouth = float(min(1, ENV[min(int(t * FPS), len(ENV) - 1)] * 1.5)); sway = 14 * math.sin(t * 3.1)
    ent = ease(win(t, 0.0, 0.7)); y = OY + bob + jump + (1 - ent) * 60
    # beat rings on the floor + lamp glow
    per = 60.0 / PAL["bpm"]; ph = (t % per) / per
    if t > 0.6:
        for k in (0, 1):
            p = (ph + k * 0.5) % 1.0; rx = 150 + 380 * p
            D.ellipse([U(OX - rx), U(OY - 4 - rx * 0.16), U(OX + rx), U(OY - 4 + rx * 0.16)], outline=rgba(ACC, 0.30 * (1 - p) ** 2 * ent), width=U(3))
    if _glow is None:
        n = U(520); yy, xx = np.mgrid[0:n, 0:n].astype(np.float32); r = np.sqrt((xx - n / 2) ** 2 + (yy - n / 2) ** 2) / (n / 2)
        _glow = Image.fromarray((np.clip(1 - r, 0, 1) ** 2.2 * 255).astype(np.uint8))
    gm = _glow.point(lambda v: int(v * (0.55 + 0.12 * math.sin(t * 2.0)) * ent))
    cv.paste(ACC, (U(OX) - gm.width // 2, U(y - 522) - gm.height // 2), gm)
    lay = nox.owl_layer(PAL, K, wR, wL, look, mouth, blink, squint, sway)
    a = lay.getchannel("A")
    if ent < 0.995: a = a.point(lambda v: int(v * ent))
    cv.paste(lay.convert("RGB"), (U(OX + nox.CX0), int(U(y) + U(nox.CY0))), a)


def eq_bars(cv, D, t):
    if t < 0.8: return
    e = ENV[min(int(t * FPS), len(ENV) - 1)]
    for i in range(30):
        h = 6 + 56 * min(1, e) * (0.45 + 0.55 * abs(math.sin(i * 0.8 + t * 9.0))) + 3 * math.sin(i + t * 3)
        x = 900 + i * 31; c = mix(ACC, ACC2, i / 29)
        D.rounded_rectangle([U(x), U(1032 - h), U(x + 16), U(1032)], radius=U(8), fill=rgba(c, 0.55))


# ---------- scenes ----------
def parse_line(s):
    segs, hi, out = s.split("*"), False, []
    for seg in segs:
        if seg: out.append((seg, hi))
        hi = not hi
    return out

def sc_hook(cv, D, t, a, sc):
    tt = sc["t"]["lines"]; n = len(sc["lines"]); mark = sc.get("mark")
    if mark:
        m = text_layer(mark, HEAD, 760); put(cv, m, CXC + 120, 540, 0.12 * a * (0.9 + 0.1 * math.sin(t * 1.5)), color=ACC)
    ys = [540 + (i - (n - 1) / 2) * 165 for i in range(n)]; hi_i = 0
    for i, line in enumerate(sc["lines"]):
        p = A(t, tt[i], 0.55); b = back(win(t, tt[i], tt[i] + 0.55))
        if p <= 0: continue
        size = 124; segs = parse_line(line)
        width = sum(tw(text_layer(s, HEAD, size)) for s, _ in segs) + 24 * (len(segs) - 1)
        if width > 860: size = size * 860 / width
        layers = [(text_layer(s, HEAD, size), h) for s, h in segs]; width = sum(tw(l) for l, _ in layers)
        x = CXC - width / 2; dy = (1 - b) * 70
        for l, h in layers:
            put(cv, l, x, ys[i] + dy, p * a, color=(ACC if hi_i % 2 == 0 else ACC2) if h else WHITE, left=True); x += tw(l)
            if h: hi_i += 0
        if any(h for _, h in layers): hi_i += 1

def sc_bubble(cv, D, t, a, sc):
    tt = sc["t"]; p = A(t, tt["in"], 0.5) * a; sub = A(t, tt["sub"], 0.5) * a
    if p <= 0: return
    dx = (1 - ease(p)) * 30; bx0, by0, bx1, by1 = 880 + dx, 270, 1740 + dx, 560
    D.polygon([(U(bx0 + 3), U(380)), (U(bx0 - 56), U(430)), (U(bx0 + 3), U(470))], fill=rgba(mix(PAL["bg1"], WHITE, 0.14), p), outline=rgba(ACC, 0.9 * p))
    rr(D, (bx0, by0, bx1, by1), 44, fill=rgba(mix(PAL["bg1"], WHITE, 0.14), p), outline=rgba(ACC, 0.9 * p), w=3)
    D.rectangle([U(bx0 - 1), U(384), U(bx0 + 8), U(466)], fill=rgba(mix(PAL["bg1"], WHITE, 0.14), p))
    put(cv, text_layer(sc["big"], HEAD, 100), bx0 + 56, 365, p, left=True)
    put(cv, text_layer(sc["small"], BODY, 54), bx0 + 56, 475, 0.9 * sub, color=MUTED, left=True)
    if sc.get("lock"): put_lock(cv, CXC, 760, 520, A(t, tt["sub"], 0.7) * a)

def sc_steps(cv, D, t, a, sc):
    items, tt = sc["items"], sc["t"]; n = len(items); h = 102; gap = 22; y0 = 540 - (n * h + (n - 1) * gap) / 2
    if sc.get("topic"):
        glass(D, (880, y0 - 150, 1740, y0 - 62), 44, a, edge=ACC); label(cv, "TOPIC", 940, y0 - 106, a, 20)
        put(cv, text_layer(sc["topic"], MEDF, 38), 1040, y0 - 106, a, left=True)
    cols = [ACC, ACC2, GOOD, ACC]
    for i, it in enumerate(items):
        ta = tt["items"][i]; ai = ease(win(t, ta - 0.15, ta + 0.35)) * a
        if ai <= 0: continue
        y = y0 + i * (h + gap); xo = (1 - ease(win(t, ta - 0.15, ta + 0.4))) * 50; prog = win(t, ta, ta + tt["len"]); done = prog >= 1
        glass(D, (880 + xo, y, 1740 + xo, y + h), 30, ai, edge=cols[i % 4] if done else None, tint=cols[i % 4] if done else None)
        rr(D, (880 + xo, y + 14, 890 + xo, y + h - 14), 5, fill=rgba(cols[i % 4], ai))
        put(cv, text_layer(it["label"], HEAD, 38, 2), 925 + xo, y + 36, ai, left=True)
        put(cv, text_layer(it["sub"], BODY, 25), 925 + xo, y + 74, 0.7 * ai, color=MUTED, left=True)
        bx0, bx1, by = 1330 + xo, 1620 + xo, y + h / 2 + 4
        rr(D, (bx0, by - 5, bx1, by + 5), 5, fill=rgba(WHITE, 0.18 * ai))
        if prog > 0: rr(D, (bx0, by - 5, bx0 + (bx1 - bx0) * ease(prog), by + 5), 5, fill=rgba(mix(ACC, ACC2, prog), ai))
        if done:
            ck = ease(win(t, ta + tt["len"], ta + tt["len"] + 0.25)); cx, cy = 1685 + xo, y + h / 2
            pts = [(cx - 14, cy), (cx - 4, cy + 11), (cx + 16, cy - 13)]; cut = ck * 2; seg = [pts[0]]
            if cut <= 1: seg.append((pts[0][0] + (pts[1][0] - pts[0][0]) * cut, pts[0][1] + (pts[1][1] - pts[0][1]) * cut))
            else: seg += [pts[1], (pts[1][0] + (pts[2][0] - pts[1][0]) * (cut - 1), pts[1][1] + (pts[2][1] - pts[1][1]) * (cut - 1))]
            D.line([(U(x), U(yy)) for x, yy in seg], fill=rgba(GOOD, ai), width=U(6), joint="curve")

def sc_price(cv, D, t, a, sc):
    tt = sc["t"]; M = sc.get("minutes", 5); rate = sc.get("rate", 60); mn = sc.get("min_credits", 30)
    label(cv, sc.get("header", "PRICE SHOWN BEFORE YOU START"), CXC, 215, A(t, sc["start"] + 0.3, 0.5) * a, 22)
    pc = A(t, sc["start"] + 0.2, 0.6) * a
    glass(D, (850, 255, 1730, 650), 40, pc)
    p = ease(win(t, tt["slide0"], tt["slide1"])); m = M * p; credits = max(mn, int(round(rate * m))) if p > 0 else 0
    x0, x1, y = 940, 1640, 360
    rr(D, (x0, y - 6, x1, y + 6), 6, fill=rgba(WHITE, 0.20 * pc))
    rr(D, (x0, y - 6, x0 + (x1 - x0) * m / M, y + 6), 6, fill=rgba(mix(ACC, ACC2, p), pc))
    for i in range(M + 1):
        xx = x0 + (x1 - x0) * i / M; D.line([(U(xx), U(y + 18)), (U(xx), U(y + 30))], fill=rgba(WHITE, 0.4 * pc), width=U(2))
        if i: put(cv, text_layer(f"{i} min", BODY, 22), xx, y + 52, 0.7 * pc, color=MUTED)
    kx = x0 + (x1 - x0) * m / M; D.ellipse([U(kx - 24), U(y - 24), U(kx + 24), U(y + 24)], fill=rgba(WHITE, pc), outline=rgba(ACC, pc), width=U(6))
    num = text_layer(str(credits), HEAD, 170); put(cv, num, CXC, 505, pc, color=mix(WHITE, ACC, 0.65 + 0.35 * p))
    put(cv, text_layer("credits", MEDF, 38), CXC, 600, 0.8 * pc, color=MUTED)
    pill(cv, D, CXC, 725, f"min. {mn} credits per run", A(t, tt["min"], 0.45) * a, 28)
    if "quote" in sc:
        q = A(t, tt["quote"], 0.5) * a
        put(cv, text_layer(sc["quote"], MEDF, 40), CXC, 815, q)
    if "button" in sc:
        b = A(t, tt["button"], 0.5) * a; sc_ = 1 + 0.03 * math.sin((t - tt["button"]) * 6) * (1 if t > tt["button"] else 0)
        pill(cv, D, CXC, 920, sc["button"], b, 40, filled=True, h=96, fnt=HEAD, minw=560 * sc_)

def sc_fail(cv, D, t, a, sc):
    tt = sc["t"]; pc = A(t, sc["start"] + 0.2, 0.6) * a
    label(cv, "WHAT IF A RUN FAILS?", CXC, 235, pc, 22)
    glass(D, (850, 290, 1730, 700), 40, pc)
    bad = t >= tt["fail"]
    D.ellipse([U(910), U(345), U(938), U(373)], fill=rgba(ACC2 if bad else GOOD, pc))
    put(cv, text_layer("Run #1", HEAD, 40), 960, 360, pc, left=True)
    put(cv, text_layer("FAILED" if bad else "RENDERING", BODYB, 26, 4), 1700, 360, pc, color=ACC2 if bad else MUTED, left=False if False else True) if False else None
    st = text_layer("FAILED" if bad else "RENDERING", BODYB, 26, 4); put(cv, st, 1700 - tw(st), 360, pc, color=ACC2 if bad else MUTED, left=True)
    prog = win(t, sc["start"] + 0.4, tt["fail"]) * 0.72 if not bad else 0.72
    rr(D, (910, 420, 1670, 442), 11, fill=rgba(WHITE, 0.16 * pc))
    rr(D, (910, 420, 910 + 760 * prog, 442), 11, fill=rgba(ACC2 if bad else ACC, pc))
    if bad:
        sh = 6 * math.sin((t - tt["fail"]) * 60) * max(0, 1 - (t - tt["fail"]) * 3)
        D.line([(U(1560 + sh), U(405)), (U(1600 + sh), U(457))], fill=rgba(ACC2, pc), width=U(7)); D.line([(U(1600 + sh), U(405)), (U(1560 + sh), U(457))], fill=rgba(ACC2, pc), width=U(7))
    z = A(t, tt["zero"], 0.5) * a
    if z > 0:
        s = back(win(t, tt["zero"], tt["zero"] + 0.5))
        put(cv, text_layer("0", HEAD, 230 * (0.6 + 0.4 * s)), CXC - 230, 570, z, color=GOOD)
        put(cv, text_layer("credits charged", MEDF, 44), CXC - 130, 600, z, left=True)
        rp = win(t, tt["zero"], tt["zero"] + 0.8)
        if 0 < rp < 1:
            r = 90 + 260 * ease(rp); D.ellipse([U(CXC - 90 - r), U(570 - r * 0.6), U(CXC - 90 + r), U(570 + r * 0.6)], outline=rgba(GOOD, 0.6 * (1 - rp) * a), width=U(4))
    if sc.get("note"): put(cv, text_layer(sc["note"], BODY, 32), CXC, 790, A(t, tt["zero"] + 0.5, 0.5) * a, color=MUTED)

def sc_chips(cv, D, t, a, sc):
    items, tt = sc["items"], sc["t"]; n = len(items); cols = [ACC, ACC2, GOOD, ACC2, ACC, GOOD]
    if sc.get("header"): label(cv, sc["header"], CXC, 205, A(t, sc["start"] + 0.3, 0.5) * a, 22)
    rows = (n + 1) // 2; y0 = 540 - (rows * 150 - 30) / 2 + 20
    for i, it in enumerate(items):
        ai = A(t, tt["items"][i], 0.45) * a
        if ai <= 0: continue
        col, row = i % 2, i // 2; cx = 1075 + col * 440; cy = y0 + row * 150 + 60 + (1 - ease(ai)) * 24
        wide = (n % 2 == 1 and i == n - 1)
        if wide: cx = CXC
        w = 420 if not wide else 860
        glass(D, (cx - w / 2, cy - 62, cx + w / 2, cy + 62), 32, ai, edge=cols[i % 6], tint=cols[i % 6])
        D.ellipse([U(cx - w / 2 + 28), U(cy - 12), U(cx - w / 2 + 52), U(cy + 12)], fill=rgba(cols[i % 6], ai))
        put(cv, text_layer(it["title"], HEAD if len(it["title"]) < 18 else MEDF, 34), cx - w / 2 + 72, cy - 14, ai, left=True)
        put(cv, text_layer(it["sub"], BODY, 24), cx - w / 2 + 72, cy + 26, 0.75 * ai, color=MUTED, left=True)

def sc_approve(cv, D, t, a, sc):
    tt = sc["t"]; CLICK = tt["click"]; sc_s = 0.8 + 0.2 * ease(win(t, sc["start"], sc["start"] + 0.8))
    cx, cy, hw, hh = CXC, 480, 310 * sc_s, 172 * sc_s
    put(cv, text_layer(sc.get("headline", "Nothing goes live until you say so."), HEAD, 52), CXC, 150, A(t, sc["sents"][min(1, len(sc["sents"]) - 1)]["start"] - 0.2, 0.6) * a)
    approved = t >= CLICK + 0.05; ba = A(t, tt["badge"], 0.5) * a
    bl = text_layer("APPROVED BY YOU" if approved else "PRIVATE  ·  READY FOR REVIEW", BODYB, 22, 3); bw = tw(bl) + 84
    rr(D, (CXC - bw / 2, 214, CXC + bw / 2, 262), 24, fill=rgba(GOOD if approved else PAL["bg1"], ba), outline=rgba(GOOD if approved else ACC, ba), w=2)
    put(cv, bl, CXC + 12, 238, ba, color=(20, 40, 30) if approved else WHITE)
    D.ellipse([U(CXC - bw / 2 + 24), U(232), U(CXC - bw / 2 + 36), U(244)], fill=rgba((20, 40, 30) if approved else ACC, ba * (1 if approved else 0.6 + 0.4 * math.sin(t * 6))))
    rr(D, (cx - hw, cy - hh + 20, cx + hw, cy + hh + 20), 30, fill=rgba(mix(ACC2, ACC, 0.5), 0.20 * a), outline=rgba(WHITE, 0.55 * a), w=3)
    tri = [(cx - 24, cy - 24), (cx - 24, cy + 64), (cx + 38, cy + 20)]; D.polygon([(U(x), U(y)) for x, y in tri], fill=rgba(WHITE, 0.75 * a))
    rr(D, (cx - hw + 30, cy + hh - 6, cx + hw - 30, cy + hh + 1), 3, fill=rgba(WHITE, 0.25 * a))
    pill(cv, D, CXC, 735, sc.get("sign", "2nd person sign-off  ·  optional"), A(t, tt["sign"], 0.45) * a, 24, h=60, color=ACC)
    ab = A(t, sc["sents"][min(1, len(sc["sents"]) - 1)]["start"] - 0.3, 0.6) * a
    press = 1 - 0.05 * math.sin(math.pi * min(max((t - (CLICK - 0.02)) / 0.22, 0), 1)); by = 865
    fl = 1.0 if t < CLICK else (0.6 + 0.4 * win(t, CLICK, CLICK + 0.5)); bwid, bhei = 290 * press, 84 * press
    rr(D, (CXC - bwid / 2, by - bhei / 2, CXC + bwid / 2, by + bhei / 2), 42, fill=rgba(ACC, ab * fl))
    put(cv, text_layer(sc.get("button", "Approve"), HEAD, 34), CXC, by, ab, color=(24, 16, 40))
    rp = win(t, CLICK, CLICK + 0.6)
    if 0 < rp < 1:
        gx, gy = 150 + 90 * ease(rp), 44 + 60 * ease(rp); rr(D, (CXC - gx, by - gy, CXC + gx, by + gy), gy, outline=rgba(ACC, 0.8 * (1 - rp) * a), w=3)
    cp = ease(win(t, CLICK - 1.0, CLICK - 0.05))
    if cp > 0:
        cxp, cyp = 1760 + (CXC + 60 - 1760) * cp, 1030 + (by + 14 - 1030) * cp; cur = [(0, 0), (0, 34), (8, 26), (14, 40), (21, 37), (15, 24), (25, 24)]
        D.polygon([(U(cxp + x), U(cyp + y)) for x, y in cur], fill=rgba(WHITE, min(1, win(t, CLICK - 1.0, CLICK - 0.75)) * a), outline=(0, 0, 0, 255), width=U(2))
    st = t - CLICK
    if 0 <= st < 1.2:
        rnd = random.Random(5)
        for _ in range(46):
            ang = rnd.uniform(0, 6.283); sp = rnd.uniform(160, 620); life = rnd.uniform(0.6, 1.2); c = rnd.choice([ACC, ACC2, GOOD, WHITE])
            if st < life:
                k = st / life; r = max(1.5, 9 * (1 - k)); px = CXC + math.cos(ang) * sp * st; py = by + math.sin(ang) * sp * st * 0.8 + 140 * st * st
                D.ellipse([U(px - r), U(py - r), U(px + r), U(py + r)], fill=rgba(c, 1 - k))

def sc_cta(cv, D, t, a, sc):
    tt = sc["t"]; put_lock(cv, CXC, 300 + (1 - ease(win(t, tt["lock"], tt["lock"] + 0.8))) * 24, 720, ease(win(t, tt["lock"], tt["lock"] + 0.8)) * a)
    for i, ptxt in enumerate(sc.get("pills", [])): pill(cv, D, CXC, 450 + i * 92, ptxt, A(t, tt["pills"][i], 0.45) * a, 30)
    u = A(t, tt["url"], 0.55) * a; yb = 450 + len(sc.get("pills", [])) * 92 + 70
    sp = 1 + 0.025 * math.sin(t * 5) * (1 if u > 0.9 else 0)
    pill(cv, D, CXC, yb, sc.get("url", "nightshift-ai.studio"), u, 46, filled=True, h=112, fnt=HEAD, minw=620 * sp)
    put(cv, text_layer(sc.get("tagline", "We make the video. You press publish."), MEDF, 40), CXC, yb + 120, A(t, tt["url"] + 0.5, 0.6) * a, color=WHITE)

SCENES = dict(hook=sc_hook, bubble=sc_bubble, steps=sc_steps, price=sc_price, fail=sc_fail, chips=sc_chips, approve=sc_approve, cta=sc_cta)


def frame(t):
    cv = background(t); D = ImageDraw.Draw(cv, "RGBA")
    for p in BOKEH:
        yy = (p["y"] - p["v"] * t) % 1080; tw_ = 0.55 + 0.45 * math.sin(t * 1.3 + p["ph"]); r = U(p["r"])
        cx, cy = U(p["x"] + 8 * math.sin(t * 0.4 + p["ph"])), U(yy)
        D.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rgba(p["c"], p["a"] * tw_ * eio(win(t, 0, 0.8))))
    draw_owl(cv, D, t); eq_bars(cv, D, t)
    for i, sc in enumerate(TL["scenes"]):
        a = eio(win(t, sc["start"], sc["start"] + 0.45)) * (1 - eio(win(t, sc["end"] - 0.3, sc["end"])))
        if i == 0: a = eio(win(t, 0.5, 1.0)) * (1 - eio(win(t, sc["end"] - 0.3, sc["end"])))
        if a > 0.004: SCENES[sc["type"]](cv, D, t, a, sc)
    g = min(eio(win(t, 0.0, 0.3)), 1 - eio(win(t, DUR - 0.5, DUR)))
    if g < 0.999: cv = Image.eval(cv, lambda v: int(v * g))
    return cv


if MODE == "preview":
    od = os.path.join(os.getcwd(), "prev"); os.makedirs(od, exist_ok=True)
    for ts in sys.argv[4].split(","):
        frame(float(ts)).save(os.path.join(od, f"t{float(ts):06.2f}.png"))
    print("ok")
else:
    out, f0, f1 = sys.argv[4], int(sys.argv[5]), int(sys.argv[6]); tmp = out + ".part.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-an", tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(f0, f1):
        p.stdin.write(frame(i / FPS).tobytes())
        if i % 30 == 0: print(f"frame {i}/{f1}", flush=True)
    p.stdin.close(); rc = p.wait()
    if rc == 0: os.rename(tmp, out)
    print("done", rc)
