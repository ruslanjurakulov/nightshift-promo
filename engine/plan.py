"""Turns an episode JSON into a timeline: who speaks when, and when every visual beat lands.

Voice is synthesised sentence by sentence so every visual cue can be pinned to a real sentence start
instead of a guessed fraction of the scene. Visuals and sound effects read the SAME timeline, so they cannot drift.
"""
import hashlib, json, os, subprocess, sys
from palettes import PALETTES

VOICE_BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/ryan/high/en_US-ryan-high"


def ensure_voice(work):
    d = os.path.join(work, "voice_model"); os.makedirs(d, exist_ok=True)
    onnx = os.path.join(d, "v.onnx")
    for ext, name in ((".onnx", "v.onnx"), (".onnx.json", "v.onnx.json")):
        p = os.path.join(d, name)
        if not os.path.exists(p) or os.path.getsize(p) < 1000:
            subprocess.run(["curl", "-sSL", "--fail", "-o", p, VOICE_BASE + ext], check=True)
    return onnx


def _dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True, check=True).stdout)


def synth(text, model, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, hashlib.sha1(text.encode()).hexdigest()[:12] + ".wav")
    if not os.path.exists(path):
        subprocess.run([sys.executable, "-m", "piper", "-m", model, "-f", path, "--length-scale", "0.97"],
                       input=text.encode(), check=True, capture_output=True)
    return path


def _timing(sc, start, end):
    """Per scene type: named beat times `t`, plus sound cues [(time, kind)]."""
    S = sc["sents"]; ty = sc["type"]; t = {}; cues = []
    first, last_end = S[0]["start"], S[-1]["start"] + S[-1]["dur"]; span = last_end - first
    if ty == "hook":
        n = len(sc["lines"]); t["lines"] = [round(first + 0.05 + i * span * 0.75 / n, 3) for i in range(n)]
        cues += [(x, "pop") for x in t["lines"]]
    elif ty == "bubble":
        t["in"] = round(start + 0.35, 3); t["sub"] = round(S[-1]["start"] if len(S) > 1 else start + 1.2, 3)
        cues += [(t["in"], "pop"), (t["sub"], "blip")]
    elif ty == "steps":
        n = len(sc["items"]); step = (span - 0.3) / n
        t["items"] = [round(first + 0.1 + i * step, 3) for i in range(n)]; t["len"] = round(step * 0.8, 3)
        cues += [(x + t["len"], "tick") for x in t["items"]]
    elif ty == "price":
        t["slide0"] = round(first + 0.3, 3); t["slide1"] = round(first + 0.3 + min(2.6, S[0]["dur"] * 0.85), 3)
        t["min"] = round(first + S[0]["dur"] * 0.4, 3)
        t["quote"] = round(S[1]["start"] if len(S) > 1 else t["slide1"] + 0.3, 3); t["button"] = round(t["quote"] + 0.9, 3)
        n = sc.get("minutes", 5)
        cues += [(t["slide0"] + (t["slide1"] - t["slide0"]) * i / (n - 1), "tick") for i in range(n)] + [(t["min"], "blip"), (t["button"], "pop")]
    elif ty == "fail":
        t["fail"] = round(first + 0.3, 3); t["zero"] = round(first + S[0]["dur"] * 0.62, 3)
        cues += [(t["fail"], "thud"), (t["zero"], "ding")]
    elif ty == "chips":
        n = len(sc["items"]); step = (span - 0.5) / n
        t["items"] = [round(first + 0.1 + i * step, 3) for i in range(n)]
        cues += [(x, "blip") for x in t["items"]]
    elif ty == "approve":
        t["badge"] = round(first, 3); t["click"] = round(S[1]["start"] + S[1]["dur"] * 0.85 if len(S) > 1 else start + 3.0, 3)
        t["sign"] = round(S[-1]["start"] + 0.2, 3)
        cues += [(t["badge"], "blip"), (t["click"], "click"), (t["sign"], "blip")]
    elif ty == "cta":
        n = len(sc.get("pills", [])); t["lock"] = round(start + 0.2, 3)
        t["pills"] = [round(first + 0.3 + i * 0.4, 3) for i in range(n)]; t["url"] = round(S[min(1, len(S) - 1)]["start"] + 0.1, 3)   # the URL lands with the line that says it, not the last line
        cues += [(x, "blip") for x in t["pills"]] + [(t["url"], "pop")]
    else:
        raise ValueError("unknown scene type " + ty)
    cues.append((start + 0.05, "thump"))
    return t, cues


def make_plan(ep, work):
    model = ensure_voice(work)
    vdir = os.path.join(work, "voice"); scenes = []; t = 0.0
    for i, sc in enumerate(ep["scenes"]):
        start = t; cur = start + (0.7 if i == 0 else 0.45); sents = []
        for text in sc["sentences"]:
            p = synth(text, model, vdir); d = _dur(p)
            sents.append(dict(start=round(cur, 3), dur=round(d, 3), path=p)); cur += d + 0.22
        end = sents[-1]["start"] + sents[-1]["dur"] + 0.5
        s = dict(sc); s.update(start=round(start, 3), end=round(end, 3), sents=sents)
        s["t"], s["cues"] = _timing(s, start, end); scenes.append(s); t = end - 0.25
    total = round(scenes[-1]["end"] + 0.5, 2)
    pal = dict(PALETTES[ep["palette"]])
    owl = dict(wave=[[0.4, scenes[0]["sents"][0]["start"] + scenes[0]["sents"][0]["dur"] + 0.5],
                     [scenes[-1]["sents"][-1]["start"] - 0.2, total - 0.7]], point=[], cheer=[], squint=[])
    for s in scenes:
        if s["type"] == "approve":
            c = s["t"]["click"]; owl["point"].append([s["sents"][min(1, len(s["sents"]) - 1)]["start"] - 0.2, c + 0.15])
            owl["cheer"].append(c); owl["squint"].append([c + 0.1, c + 1.3])
    return dict(id=ep["id"], palette=pal, palette_name=ep["palette"], total=total, scenes=scenes, owl=owl)
