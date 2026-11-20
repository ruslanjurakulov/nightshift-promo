#!/usr/bin/env python3
"""usage: eleven_tts.py list                     -> prints the account's voices (name, id, category)
       eleven_tts.py make <out_dir> <ep-id>...  -> one mp3 per narration sentence, named by voice_name()

Runs only inside the `voice` workflow, which is the only place ELEVENLABS_API_KEY exists. The key is read from the
environment and never printed, logged or written anywhere, not even in part.
"""
import json, os, sys, urllib.error, urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engine"))
from voice import ROOT, load_cfg, voice_name  # noqa: E402

API = "https://api.elevenlabs.io/v1"


def _key():
    k = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not k:
        sys.exit("ELEVENLABS_API_KEY is not set: add it under Settings > Secrets and variables > Actions of this repo")
    return k


def _call(path, body=None):
    req = urllib.request.Request(API + path, data=None if body is None else json.dumps(body).encode(),
                                 headers={"xi-api-key": _key(), "Content-Type": "application/json",
                                          "Accept": "audio/mpeg" if body else "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        # invalid_api_key and quota_exceeded share HTTP 401 and need opposite fixes, so the remedy is named per status
        try:
            detail = json.loads(e.read().decode()).get("detail", {})
        except Exception:
            detail = {}
        status = detail.get("status", "") if isinstance(detail, dict) else ""
        fix = {"invalid_api_key": "the key is wrong or revoked: replace the ELEVENLABS_API_KEY secret",
               "quota_exceeded": "the ElevenLabs character quota is used up: wait for the monthly reset or upgrade the plan",
               "voice_not_found": "the voice id is not on this account: run the workflow with mode=list and pick one",
               "missing_permissions": "the key lacks the text_to_speech / voices_read permission: create a key with them",
               }.get(status, "see the status above")
        sys.exit(f"ElevenLabs {e.code} {status or ''}: {fix}")


def cmd_list():
    for v in json.loads(_call("/voices"))["voices"]:
        print(f"{v['name']:<28} {v['voice_id']}  {v.get('category', '')}  {json.dumps(v.get('labels', {}))}")


def cmd_make(out, ids):
    cfg = load_cfg(require_elevenlabs=True); os.makedirs(out, exist_ok=True); n = chars = 0
    for eid in ids:
        ep = json.load(open(os.path.join(ROOT, "episodes", eid + ".json")))
        for sc in ep["scenes"]:
            for text in sc["sentences"]:
                p = os.path.join(out, voice_name(text, cfg))
                if os.path.exists(p):
                    continue
                audio = _call(f"/text-to-speech/{cfg['elevenlabs_voice_id']}?output_format=mp3_44100_128",
                              {"text": text, "model_id": cfg["elevenlabs_model"]})
                if len(audio) < 1000:
                    sys.exit(f"ElevenLabs returned {len(audio)} bytes for {eid}: {text!r}")
                open(p, "wb").write(audio); n += 1; chars += len(text)
        print(eid, "ok")
    print(f"{n} new lines, {chars} characters")


if __name__ == "__main__":
    if sys.argv[1:2] == ["list"]:
        cmd_list()
    elif sys.argv[1:2] == ["make"] and len(sys.argv) > 3:
        cmd_make(sys.argv[2], sys.argv[3:])
    else:
        sys.exit(__doc__)
