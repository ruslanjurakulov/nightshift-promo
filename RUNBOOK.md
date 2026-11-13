# Daily run (08:00 Asia/Samarkand). Each run is a FRESH session: everything needed is in this repo.
1. Add the repo with push access (`add_repo ruslanjurakulov/nightshift-promo`, access push) and clone it.
2. `pip install --break-system-packages -r requirements.txt`; check `ffmpeg -version`.
2b. **Queue first** (owner decision 2026-11-13): if `python3 tools/qstate.py nextpublish` prints an id, publish that pre-made video instead of rendering a new one: follow "Publishing from the queue" below and skip steps 3-6. After publishing, run one "Producer pass" (below) before finishing.
3. Read `topics.md`; pick a topic not used yet and a palette different from yesterday's (palettes in engine/palettes.py).
4. Read https://nightshift-ai.studio (pricing, features, approval wording). Use ONLY facts found there. Never imply the bot publishes publicly on its own; uploads are private until a person decides.
5. Write `episodes/epNNN-<slug>.json` (scene types: hook, bubble, steps, price, fail, chips, approve, cta; see ep002-price.json). 6-8 scenes, 40-60 s, English, one message per video.
6. `python3 engine/build.py episodes/<file>.json 2` (4K, ~15 min). Then QA per QA_RUBRIC.md; write `qa/<id>.json`.
7. Pass -> commit the video to `videos/` and push to main; import into vidIQ from `https://raw.githubusercontent.com/ruslanjurakulov/nightshift-promo/main/videos/<id>.mp4` (vidiq_video_upload), create a draft for Instagram @nightshift_ai.studio (account 29426377243641986; NEVER the personal ruslan_jurakulov) and the YouTube channel @nightshift_ai_studio, publish to three destinations: Instagram, YouTube and X @nightshift_ai (platformAccountId 1300249842439131136, text under 280 chars, include the site) (YouTube visibility: PUBLIC, owner decision 2026-11-11), poll status, retry only the failed destination.
8. Update `topics.md` with the result. If anything fails (reconnectRequired, quota), stop and tell the owner what to fix.

## Telegram (channel https://t.me/nightshiftaistudio)
Telegram is sent by GitHub Actions (`.github/workflows/telegram.yml`), not by this session: the bot token is a repo secret `TELEGRAM_BOT_TOKEN` that only Actions can read.
After the video is pushed to `videos/`, commit `captions/<id>.txt` (same text as the X post, <= 1000 chars) in a LATER commit and push: that push triggers the workflow, which re-encodes to 1080p (Telegram's 50 MB limit) and sends it. Check the run under the repo's Actions tab; if it failed, tell the owner (usual cause: secret missing).

## Queue (30 pre-made days, owner decision 2026-11-13)
The owner asked for 30 days of videos made ahead with Higgsfield b-roll, stored on GitHub and released one a day.
Format is hybrid: Higgsfield makes silent footage (no text), our engine adds the voice, cards, Nox and CTA, so every
claim still comes from the site. Footage is labelled "AI-GENERATED FOOTAGE" on screen while it shows.
- `tools/make_queue.py` wrote `episodes/ep006..ep035` and `queue/plan.json` (per episode: facts with page+quote, X text, 2 clip prompts).
- `tools/qstate.py` reads/updates the queue state (`summary`, `next`, `pending`, `ready`, `nextpublish`, ...).
- Clips: Higgsfield `seedance_2_5`, 5 s, 720p, 16:9, `use_unlim: true` (the unlimited window covers 720p only and ends
  2026-11-16 19:08 UTC; never spend credits on them). The account is rate-limited (429): submit one at a time; on 429 stop and try next run.
  After the window, `qstate.py expire`: a scene without a clip keeps the plain palette background. No paid or stock substitute.
- Render: `python3 tools/prep_broll.py <id>` then `python3 engine/build.py work/<id>.json 2`, then `engine/qa_check.py`.
  If only the colour check fails, change `palette` in `episodes/<id>.json` to the next one in ocean/sunrise/candy/forest/ember (not aurora) and rebuild, max 2 remakes.
- Store: `tools/stash.sh <id>` pushes the video on an orphan branch `stash/<id>`; `.github/workflows/stash.yml` uploads it to the
  `queue` release and deletes the branch. Asset URL: https://github.com/ruslanjurakulov/nightshift-promo/releases/download/queue/<id>.mp4
  Then `qstate.py render <id> stashed <asset-url>` and push `queue/plan.json` + `qa/<id>.json` to main.

### Publishing from the queue (daily job)
1. `id=$(python3 tools/qstate.py nextpublish)`. If empty, do the normal render flow (steps 3-8 above).
2. `python3 tools/check_facts.py $id` re-reads the live pages. Exit 1 = a quote is gone: `qstate.py published $id "stale: <quote>"`, try the next one.
3. Download the asset to `videos/$id.mp4`, run `engine/qa_check.py` and the contact-sheet rubric (QA_RUBRIC.md) as usual.
4. Same publishing steps as a fresh video: commit the video to main, vidIQ (title = plan `title`, X text = plan `x_text`), caption commit for Telegram.
5. `qstate.py published $id "<links>"`, add the row to topics.md, push.

### Producer pass (run by the daily job after it publishes, and by any session asked to fill the queue)
1. Collect: each clip from `qstate.py pending` -> Higgsfield jobs_wait; completed -> `qstate.py set <key> done <job_id> <result_url>`, failed -> `set <key> todo`.
2. Generate (only before 2026-11-16T19:00Z): `qstate.py next` -> Higgsfield generate_video {model seedance_2_5, duration 5, resolution 720p, aspect_ratio 16:9, use_unlim true, prompt as given}. Never spend credits. On 429 stop for today (normal). After the window: `qstate.py expire` once.
3. Render up to 2 episodes from `qstate.py ready` (see Render/Store above). Commit ONLY queue/plan.json, qa/*.json, episodes/*.json; never `git add -A` (queued videos must not reach main).
