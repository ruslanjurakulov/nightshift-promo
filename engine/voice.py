"""Which voice narrates, and where an ElevenLabs line lives.

voice.json at the repo root is the standing choice. With engine=elevenlabs a render takes every line from the
`voice` release (made by .github/workflows/voice.yml, the only place the API key exists). A line that is not there
stops the render: a promo that suddenly speaks in the free voice is worse than no promo.
"""
import hashlib, json, os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RELEASE = "https://github.com/ruslanjurakulov/nightshift-promo/releases/download/voice/"


def load_cfg(require_elevenlabs=False):
    cfg = json.load(open(os.path.join(ROOT, "voice.json")))
    if cfg.get("engine") not in ("piper", "elevenlabs"):
        raise SystemExit(f"voice.json: unknown engine {cfg.get('engine')!r}")
    if (cfg["engine"] == "elevenlabs" or require_elevenlabs) and len(cfg.get("elevenlabs_voice_id", "")) != 20:
        raise SystemExit("voice.json: elevenlabs_voice_id must be a 20-character id from the account's list")
    return cfg


def voice_name(text, cfg):
    # the voice and model are part of the name, so changing either can never reuse an old line
    h = hashlib.sha1(f"{cfg['elevenlabs_voice_id']}|{cfg['elevenlabs_model']}|{text}".encode()).hexdigest()[:16]
    return f"el-{h}.mp3"


def fetch_line(text, cfg, out_dir):
    """Returns a wav of this line in the configured ElevenLabs voice, or stops the render."""
    os.makedirs(out_dir, exist_ok=True); name = voice_name(text, cfg)
    mp3, wav = os.path.join(out_dir, name), os.path.join(out_dir, name[:-4] + ".wav")
    if not os.path.exists(wav):
        if not os.path.exists(mp3):
            r = subprocess.run(["curl", "-sSL", "--fail", "-o", mp3, RELEASE + name], capture_output=True)
            if r.returncode:
                raise SystemExit(f"ElevenLabs line missing from the voice release ({name}): {text!r}\n"
                                 "fix: run the voice workflow (mode=make) for this episode, then render again")
        # The mixer was tuned on Piper lines (~-15 LUFS each). ElevenLabs lines arrive ~9 dB quieter (~-24 LUFS), and the
        # first trial mix (ep053, 2026-11-20) came out at -20.1 LUFS, failing qa_check's -20 floor. So each line is
        # normalised to Piper's level. Mono like Piper; the mixer resamples to 48 kHz itself, so 44.1 kHz detail is kept.
        # Each ElevenLabs line also ends in ~0.3 s of silence that Piper lines do not have, and the planner adds its own
        # 0.22 s gap after every line. Over 16 lines that pushed ep050/ep051 to 66-67 s, past qa_check's 65 s ceiling,
        # so the trailing silence is cut (keeping 50 ms so the last word's decay is not clipped).
        trim = "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3, "-af", trim + ",loudnorm=I=-15:TP=-1.5:LRA=11",
                        "-ar", "44100", "-ac", "1", wav], check=True)
    return wav
