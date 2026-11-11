#!/usr/bin/env python3
"""usage: build.py episodes/epNNN.json [K=2] -> videos/<id>.mp4 (plan -> audio -> two parallel segments -> concat -> mux)."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
import plan, audio

ep = json.load(open(sys.argv[1])); K = sys.argv[2] if len(sys.argv) > 2 else "2"
work = os.path.abspath(os.path.join(ROOT, "work", ep["id"])); os.makedirs(work, exist_ok=True)
tl = plan.make_plan(ep, work)
mix, env = audio.build_audio(tl, work); tl["env"] = env
tlp = os.path.join(work, "timeline.json"); json.dump(tl, open(tlp, "w"))
nf = int(tl["total"] * 30); mid = nf // 2; R = os.path.join(HERE, "render.py")
segs = [(os.path.join(work, "segA.mp4"), 0, mid), (os.path.join(work, "segB.mp4"), mid, nf)]
procs = [subprocess.Popen([sys.executable, R, tlp, K, "seg", o, str(a), str(b)], stdout=subprocess.DEVNULL) for o, a, b in segs]
if any(p.wait() for p in procs): sys.exit("segment render failed")
lst = os.path.join(work, "list.txt"); open(lst, "w").write("".join(f"file '{o}'\n" for o, _, _ in segs))
vid = os.path.join(work, "silent.mp4")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid], check=True)
os.makedirs(os.path.join(ROOT, "videos"), exist_ok=True); out = os.path.join(ROOT, "videos", ep["id"] + ".mp4")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", mix, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
print(out, tl["total"])
