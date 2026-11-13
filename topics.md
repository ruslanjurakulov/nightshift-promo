# Topic history (newest last). A new day must pick a topic NOT already here.
| id | date | topic | palette | status |
|---|---|---|---|---|
| ep001 | 2026-11 | Meet Nox: what Nightshift is (first 55 s ad, 8K, sent by hand) | sunrise | posted manually |
| ep002-price | test | Know the price before you press start | candy | test, awaiting owner OK |
| ep003-editor | 2026-11-11 | Editing costs zero credits (free editor: trim, split, text, music, speed, captions, frame shapes) | forest | posted: YouTube public, Instagram, X, Telegram |
| ep004-failfree | 2026-11-12 | A failed run costs nothing (quote, hold, charge, return) | sunrise | posted: YouTube public, Instagram, X, Telegram |
| ep005-storyboard | 2026-11-13 | Read the plan before you pay (storyboard review: edit, approve and render, or discard for free) | candy (aurora failed hue check) | posted: YouTube public, Instagram, X, Telegram |

## Topic bank (all must be backed by facts read from the live site that day)
- Why failed runs cost 0 credits  · Private until you say so (approve step)  · 100 free credits: what you can make
- Script, voice, visuals, captions in one run  · Editor: trim, split, text, music  · Plans compared (Plus/Pro/Business)
- ~~Storyboard review~~ (ep005)  · Thumbnail brief & working titles  · Image / clip / voice / upscale / cut-out tools

## Run log (not published; does not consume a topic)
- 2026-11-14 (Asia/Samarkand): ep006-topic blocked before rendering. Seedance 2.5 unlimited request returned `429 rate_limit_reached`; stopped per RUNBOOK, with no paid fallback or platform posts. Queue remains 2/60 clips and 0/30 stashed videos. Selected ocean instead of yesterday's candy. See `qa/ep006-topic.json`.
- 2026-11-14 owner-requested retry: MCP balance confirmed unlimited access after a transient connection failure, but Seedance 2.5 (720p, 5 s, use_unlim=true) again returned `429 rate_limit_reached`. No job ID, render, or publication. This does not establish the status of concurrent Claude requests.
- 2026-11-14: Owner reported Seedance 2.0 working in Claude. Tested ep035-planmonth-0 through this ChatGPT MCP connection with 720p, mode=std, audio enabled, 5 s, use_unlim=true after verifying allowance. Backend returned `429 rate_limit_reached`; no job submitted, no render or publication. Queue status left todo. See `qa/ep035-planmonth.json`.
