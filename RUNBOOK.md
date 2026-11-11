# Daily run (08:00 Asia/Samarkand). Each run is a FRESH session: everything needed is in this repo.
1. Add the repo with push access (`add_repo ruslanjurakulov/nightshift-promo`, access push) and clone it.
2. `pip install --break-system-packages -r requirements.txt`; check `ffmpeg -version`.
3. Read `topics.md`; pick a topic not used yet and a palette different from yesterday's (palettes in engine/palettes.py).
4. Read https://nightshift-ai.studio (pricing, features, approval wording). Use ONLY facts found there. Never imply the bot publishes publicly on its own; uploads are private until a person decides.
5. Write `episodes/epNNN-<slug>.json` (scene types: hook, bubble, steps, price, fail, chips, approve, cta; see ep002-price.json). 6-8 scenes, 40-60 s, English, one message per video.
6. `python3 engine/build.py episodes/<file>.json 2` (4K, ~15 min). Then QA per QA_RUBRIC.md; write `qa/<id>.json`.
7. Pass -> commit the video to `videos/` and push to main; import into vidIQ from `https://raw.githubusercontent.com/ruslanjurakulov/nightshift-promo/main/videos/<id>.mp4` (vidiq_video_upload), create a draft for Instagram @nightshift_ai.studio (account 29426377243641986; NEVER the personal ruslan_jurakulov) and the YouTube channel @nightshift_ai_studio, publish, poll status, retry only the failed destination.
8. Update `topics.md` with the result. If anything fails (reconnectRequired, quota), stop and tell the owner what to fix.
