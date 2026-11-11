"""Music + sound effects + voice mix. Everything is synthesised in numpy, so there is no licensed music to worry about.

The music is a light four-chord loop with a soft beat; the voice ducks it (sidechain) so the narration always stays clear.
"""
import json, os, subprocess, wave, zlib
import numpy as np

SR = 48000
NOTE = lambda midi: 440.0 * 2 ** ((midi - 69) / 12)


def _wr(path, x):
    x = np.int16(np.clip(x, -1, 1) * 32767)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(x.tobytes())


def build_audio(tl, work):
    total = tl["total"]; n = int(SR * total); t = np.arange(n) / SR; pal = tl["palette"]
    rng = np.random.default_rng(zlib.crc32(tl["id"].encode())); key = pal["key"]; bpm = pal["bpm"]; beat = 60.0 / bpm; bar = beat * 4

    def env_at(a, b, c, d): return np.clip((t - a) / (b - a), 0, 1) * (1 - np.clip((t - c) / (d - c), 0, 1))

    def tone(t0, midi, dur, g, harm=(1.0, 0.3, 0.1), decay=3.0):
        m = (t >= t0) & (t < t0 + dur); x = np.zeros(n); q = t[m] - t0
        s = sum(h * np.sin(2 * np.pi * NOTE(midi) * (k + 1) * q) for k, h in enumerate(harm))
        x[m] = s * np.exp(-q * decay) * np.minimum(q / 0.01, 1) * g; return x

    # chord loop Am - F - C - G (shifted by `key`)
    prog = [(57, (57, 60, 64)), (53, (53, 57, 60)), (48, (48, 52, 55)), (55, (55, 59, 62))]
    music = np.zeros(n); nb = int(total / bar) + 2
    for b in range(nb):
        t0 = b * bar; root, chord = prog[b % 4]
        for note in chord: music += tone(t0, note + key + 12, bar * 1.05, 0.020, (1.0, 0.2), 0.9)       # soft pad
        music += tone(t0, root + key - 12, beat * 1.8, 0.16, (1.0, 0.25), 2.2) + tone(t0 + 2 * beat, root + key - 12, beat * 1.8, 0.12, (1.0, 0.25), 2.2)
        for k in range(8):                                                                              # plucky arpeggio
            music += tone(t0 + k * beat / 2, chord[(k * 2 + (b % 2)) % 3] + key + 24, beat * 0.9, 0.028, (1.0, 0.4, 0.15), 6.0)
        for kb in (0, 2):                                                                               # kick on 1 and 3
            m = (t >= t0 + kb * beat) & (t < t0 + kb * beat + 0.25); q = t[m] - (t0 + kb * beat)
            music[m] += np.sin(2 * np.pi * (45 * q + 70 * (1 - np.exp(-q * 30)) / 30)) * np.exp(-q * 14) * 0.30
        for k in range(8):                                                                              # hi-hat on the off-beats
            if k % 2:
                m = (t >= t0 + k * beat / 2) & (t < t0 + k * beat / 2 + 0.05); music[m] += rng.standard_normal(m.sum()) * np.exp(-(t[m] - t0 - k * beat / 2) * 90) * 0.025
    music *= env_at(0, 1.2, total - 1.8, total)

    def burst(t0, d, g, kind):
        m = (t >= t0) & (t < t0 + d); x = np.zeros(n); q = (t[m] - t0)
        if kind == "pop": x[m] = np.sin(2 * np.pi * (500 + 900 * (1 - np.exp(-q * 40))) * q) * np.exp(-q * 22) * g
        elif kind == "blip": x[m] = np.sin(2 * np.pi * 1700 * q) * np.exp(-q * 45) * g
        elif kind == "tick": x[m] = (np.sin(2 * np.pi * 1300 * q) + 0.4 * np.sin(2 * np.pi * 2600 * q)) * np.exp(-q * 55) * g
        elif kind == "thump": x[m] = np.sin(2 * np.pi * (38 * q + 72 * (1 - np.exp(-q * 9)) / 9)) * np.exp(-q * 5.5) * g * 3
        elif kind == "thud": x[m] = np.sin(2 * np.pi * (60 * q + 40 * (1 - np.exp(-q * 20)) / 20)) * np.exp(-q * 9) * g * 4
        elif kind == "ding": x[m] = (np.sin(2 * np.pi * 1760 * q) + 0.5 * np.sin(2 * np.pi * 2640 * q)) * np.exp(-q * 6) * g * 1.4
        elif kind == "click":
            x[m] = np.sin(2 * np.pi * 900 * q) * np.exp(-q * 70) * g * 2
            for k, f in enumerate((1320, 1760, 2093, 2637)):
                m2 = (t >= t0 + 0.12 + 0.07 * k) & (t < t0 + 0.5 + 0.07 * k); q2 = t[m2] - (t0 + 0.12 + 0.07 * k)
                x[m2] += np.sin(2 * np.pi * f * q2) * np.exp(-q2 * 12) * g * 0.6
        return x

    sfx = np.zeros(n); gains = dict(pop=0.18, blip=0.12, tick=0.12, thump=0.16, thud=0.22, ding=0.14, click=0.14)
    for sc in tl["scenes"]:
        for ct, kind in sc["cues"]:
            sfx += burst(ct, 0.6, gains[kind], kind)
        m = (t >= sc["start"] - 0.15) & (t < sc["start"] + 0.35); q = (t[m] - (sc["start"] - 0.15)) / 0.5     # whoosh into each scene
        sfx[m] += np.convolve(rng.standard_normal(m.sum()), np.ones(8) / 8, "same") * np.sin(np.pi * q) ** 2 * 0.05
    mus = np.tanh((music + sfx * 0.9) * 1.05)
    mus_path = os.path.join(work, "music.wav"); _wr(mus_path, mus)

    paths = [s["path"] for sc in tl["scenes"] for s in sc["sents"]]; starts = [s["start"] for sc in tl["scenes"] for s in sc["sents"]]
    ins, fc, labels = [], "", ""
    for j, (p, st) in enumerate(zip(paths, starts)):
        ins += ["-i", p]; fc += f"[{j}]adelay={int(st * 1000)}:all=1,aresample=48000[v{j}];"; labels += f"[v{j}]"
    j = len(paths)
    fc += f"{labels}amix=inputs={j}:normalize=0,apad=whole_dur={total},atrim=0:{total},volume=1.6,asplit=3[vo][sc][vf];"
    fc += f"[{j}]volume=1.0[m];[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350[md];"
    fc += f"[vo][md]amix=inputs=2:normalize=0,alimiter=limit=0.92,atrim=0:{total},aformat=channel_layouts=stereo[out]"
    mix, vo = os.path.join(work, "mix.wav"), os.path.join(work, "voice_only.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-i", mus_path, "-filter_complex", fc, "-map", "[out]", mix,
                   "-map", "[vf]", "-ac", "1", "-ar", "48000", vo], check=True)
    with wave.open(vo) as w: a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    fr = SR // 30; nf = int(total * 30) + 2
    e = np.array([np.sqrt(np.mean(a[i * fr:(i + 1) * fr] ** 2)) if (i + 1) * fr <= len(a) else 0 for i in range(nf)])
    e = np.convolve(e / (np.percentile(e[e > 0.005], 90) if (e > 0.005).any() else 1), [.25, .5, .25], "same")
    env_path = os.path.join(work, "env.npy"); np.save(env_path, np.clip(e, 0, 1))
    return mix, env_path
