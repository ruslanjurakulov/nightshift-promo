#!/usr/bin/env python3
"""usage: prep_broll.py <episode-id> -> downloads the episode's done clips to broll/<key>.mp4 and writes
work/<id>.json, the episode with b-roll only where a clip exists. A skipped clip means that scene keeps the plain
palette background: no paid substitute, no stock footage, nothing silently swapped in."""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
eid = sys.argv[1]
plan = next(e for e in json.load(open(os.path.join(ROOT, "queue", "plan.json")))["episodes"] if e["id"] == eid)
ep = json.load(open(os.path.join(ROOT, "episodes", eid + ".json")))
os.makedirs(os.path.join(ROOT, "broll"), exist_ok=True); os.makedirs(os.path.join(ROOT, "work"), exist_ok=True)
for c in plan["clips"]:
    sc = ep["scenes"][c["scene"]]; dst = os.path.join(ROOT, "broll", c["key"] + ".mp4")
    if c["status"] == "done" and c.get("url"):
        if not os.path.exists(dst): subprocess.run(["curl", "-sSL", "--fail", "-o", dst, c["url"]], check=True)
        sc["broll"] = f"broll/{c['key']}.mp4"
    else:
        sc.pop("broll", None); print("no clip for", c["key"], "-> plain background")
out = os.path.join(ROOT, "work", eid + ".json"); json.dump(ep, open(out, "w"), indent=1); print(out)
