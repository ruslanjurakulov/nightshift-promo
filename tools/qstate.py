#!/usr/bin/env python3
"""Tiny state helper for queue/plan.json, so each session (or scheduled run) can pick up where the last one stopped.
  qstate.py next              -> key and prompt of the next clip to generate (todo, in episode order)
  qstate.py pending           -> clips submitted but not collected (key job_id)
  qstate.py set KEY STATUS [JOB_ID] [URL]
  qstate.py ready             -> episodes whose clips are all done and that are not rendered yet
  qstate.py render ID STATUS [ASSET]
  qstate.py expire            -> after the Higgsfield unlimited window: every clip not done becomes skipped
  qstate.py nextpublish       -> first stashed, unpublished episode in day order
  qstate.py published ID WHAT -> record where it went (or "stale: <why>")
"""
import json, os, sys
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "queue", "plan.json")
d = json.load(open(P)); eps = d["episodes"]; cmd = sys.argv[1]
clips = [c for e in eps for c in e["clips"]]
if cmd == "next":
    c = next((c for c in clips if c["status"] == "todo"), None); print(json.dumps(c and {"key": c["key"], "duration": c.get("duration", 5), "prompt": c["prompt"]}))
elif cmd == "pending":
    for c in clips:
        if c["status"] == "submitted": print(c["key"], c["job_id"])
elif cmd == "set":
    c = next(c for c in clips if c["key"] == sys.argv[2]); c["status"] = sys.argv[3]
    if len(sys.argv) > 4: c["job_id"] = sys.argv[4]
    if len(sys.argv) > 5: c["url"] = sys.argv[5]
elif cmd == "ready":
    for e in eps:
        if e["render"] == "todo" and all(c["status"] in ("done", "skipped") for c in e["clips"]): print(e["id"])
elif cmd == "render":
    e = next(e for e in eps if e["id"] == sys.argv[2]); e["render"] = sys.argv[3]
    if len(sys.argv) > 4: e["asset"] = sys.argv[4]
elif cmd == "expire":
    for c in clips:
        if c["status"] != "done": c["status"] = "skipped"
elif cmd == "nextpublish":
    e = next((e for e in eps if e["render"] == "stashed" and not e.get("published")), None); print(e["id"] if e else "")
elif cmd == "published":
    e = next(e for e in eps if e["id"] == sys.argv[2]); e["published"] = sys.argv[3]
elif cmd == "summary":
    print("clips done", sum(c["status"] == "done" for c in clips), "/", len(clips), "| rendered", sum(e["render"] == "stashed" for e in eps), "/", len(eps))
json.dump(d, open(P, "w"), indent=1)
