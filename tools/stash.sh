#!/bin/bash
# usage: tools/stash.sh <episode-id>  -> pushes videos/<id>.mp4 on an orphan branch stash/<id>; Actions moves it to the
# "queue" release and deletes the branch. The orphan branch carries only the workflow and the file, so main never holds it.
set -euo pipefail
id=$1; cd "$(dirname "$0")/.."; here=$(pwd); src="videos/$id.mp4"; [ -f "$src" ] || { echo "missing $src"; exit 1; }
tmp=$(mktemp -d); git worktree add --detach "$tmp" >/dev/null 2>&1
( cd "$tmp" && git checkout -q --orphan "stash/$id" && git rm -rqf . && mkdir -p .github/workflows outbox \
  && cp "$here/.github/workflows/stash.yml" .github/workflows/ && cp "$here/$src" outbox/ \
  && git add -A && git commit -qm "stash $id for the queue release" && git push -q origin "stash/$id" )
git worktree remove --force "$tmp"; git branch -D "stash/$id" >/dev/null 2>&1 || true
echo "pushed stash/$id"
