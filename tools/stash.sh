#!/bin/bash
# usage: tools/stash.sh <episode-id>  -> pushes videos/<id>.mp4 on an orphan branch stash/<id>; Actions moves it to the
# "queue" release and deletes the branch. The orphan branch carries only the workflow and the file, so main never holds it.
set -euo pipefail
id=$1; cd "$(dirname "$0")/.."; here=$(pwd); src="videos/$id.mp4"; [ -f "$src" ] || { echo "missing $src"; exit 1; }
# One-minute 4K renders come out ~130 MB and GitHub refuses any pushed file over 100 MB (ep049, 2026-11-14), so a file
# over 95 MB is re-encoded at a capped bitrate (still 4K 30 fps, audio copied) and must pass qa_check again before it is stored.
if [ "$(stat -c %s "$src")" -gt 99614720 ]; then
  enc=$(mktemp --suffix=.mp4)
  ffmpeg -loglevel error -y -i "$src" -c:v libx264 -preset fast -b:v 11M -maxrate 12M -bufsize 24M -pix_fmt yuv420p -r 30 \
    -c:a copy -movflags +faststart "$enc"
  [ "$(stat -c %s "$enc")" -le 99614720 ] || { echo "re-encode still over 95 MB"; rm -f "$enc"; exit 1; }
  cine=""; grep -q '"format": *"cine"' "episodes/$id.json" 2>/dev/null && cine="--cine"
  python3 engine/qa_check.py "$enc" $cine >/dev/null || { echo "re-encoded file failed qa_check"; rm -f "$enc"; exit 1; }
  mv "$enc" "$src"; echo "re-encoded $src to $(( $(stat -c %s "$src") / 1048576 )) MB"
fi
tmp=$(mktemp -d); git worktree add --detach "$tmp" >/dev/null 2>&1
( cd "$tmp" && git checkout -q --orphan "stash/$id" && git rm -rqf . && mkdir -p .github/workflows outbox \
  && cp "$here/.github/workflows/stash.yml" .github/workflows/ && cp "$here/$src" outbox/ \
  && git add -A && git commit -qm "stash $id for the queue release" && git push -q origin "stash/$id" )
git worktree remove --force "$tmp"; git branch -D "stash/$id" >/dev/null 2>&1 || true
rm -f "$src"   # never let a queued video reach main through a broad git add
echo "pushed stash/$id"
