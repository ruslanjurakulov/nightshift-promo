#!/usr/bin/env python3
"""usage: check_facts.py <episode-id> [...]  -> exit 0 only if every quote in queue/plan.json is still on the live site.

A queued video was scripted days earlier. The site is the source of truth on the publish day, so an episode whose
quote has disappeared (price changed, feature renamed) must not go out. Matching ignores markup, case, whitespace
and curly-vs-straight quotes, nothing else: a changed number is a mismatch, on purpose.
"""
import html, json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace(" ", " ").replace("‑", "-")
    return re.sub(r"\s+", " ", s).strip().lower()


_cache = {}
def page_text(url):
    if url not in _cache:
        raw = subprocess.run(["curl", "-sSL", "--fail", "-m", "60", url], capture_output=True, text=True, check=True).stdout
        raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
        txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
        _cache[url] = norm(txt)
    return _cache[url]


def check(ep):
    bad = []
    for f in ep["facts"]:
        q = norm(f["quote"]); t = page_text(f["page"])
        if q not in t and q.replace(" | ", " ") not in t:
            bad.append(f)
    return bad


if __name__ == "__main__":
    plan = {e["id"]: e for e in json.load(open(os.path.join(ROOT, "queue", "plan.json")))["episodes"]}
    ids = sys.argv[1:] or list(plan)
    failed = 0
    for i in ids:
        bad = check(plan[i])
        print(i, "OK" if not bad else "MISSING: " + " || ".join(f'{b["page"]}: {b["quote"]}' for b in bad))
        failed += bool(bad)
    sys.exit(1 if failed else 0)
