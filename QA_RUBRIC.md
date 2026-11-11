# QA gate (run before every post)
Owner's rule: do not ask for approval each day. Check the video yourself; post only if it passes, otherwise remake.
This is a proxy for a viewer, not audience data. Calibrate it against real insights after 1-2 days.

1. `python3 engine/qa_check.py videos/<id>.mp4` must exit 0 (duration 35-65 s, 4K, 30 fps, loudness, no clipping, no still stretch >3 s, colourful, <299 MB).
2. Look at a contact sheet (a frame every ~3 s) and listen to the pacing, then score 1-5 in `qa/<id>.json`:
   hook (first 2 s makes you stay) · pace (something new every <=3 s) · one clear message · colour/energy · offer appeal (would an ordinary viewer open the site / sign up free) · technical quality.
3. **Fact accuracy is a hard gate**: every number, price and claim in the script must match the live site read that day (cite the line). Any mismatch = fail, fix the script, remake.
4. Pass = average >= 4 and no score < 3 and facts OK. Up to 2 remakes, then skip the day and tell the owner.
5. Never claim the video "will perform"; say what was checked and what was not.
