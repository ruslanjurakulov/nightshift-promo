#!/usr/bin/env python3
"""Cinematic queue (owner, 2026-11-13: "make it cinematic, interactive, make people curious about the site").

Each ad: 7 full-screen Higgsfield shots with one spoken line and one big title each, then the site's own
"type a topic, see the plan" box typed out on screen as the call to action. Footage carries the feeling; every
claim in a title or a line is still quoted from the live site (facts[]), and re-checked on the publish day.
Replaces the 30 plain episodes in queue/plan.json (their files stay in episodes/ for reference).
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cine_prompts   # director-level prompts; the short prompt in ADS is only the shot's intent
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME, STUDIO, PRICING = "https://nightshift-ai.studio", "https://nightshift-ai.studio/studio", "https://nightshift-ai.studio/pricing"
YT, CS = "https://nightshift-ai.studio/solutions/youtube-channels", "https://nightshift-ai.studio/solutions/creative-studio"
PALS = ["candy", "sunrise", "forest", "ember"]
LOOK = (" Cinematic commercial shot, anamorphic lens, shallow depth of field, smooth motivated camera move, "
        "rich night colour grade with warm highlights, premium advertising look. No readable text, no letters, no logos, no watermarks.")
TOPICS = ["Why the Silk Road ran through Samarkand", "How a lighthouse lens works", "Why the Moon always shows the same face", "How bread rises"]
TRY_FACTS = [(HOME, "Type a topic. See what the plan looks like."), (HOME, "100 free credits, once, when you sign up. No card.")]   # the end card says only these

# (slug, title, x_text, [(prompt, title-with-*accent*, spoken line) x7], facts)
ADS = [
 ("nightshift", "3 AM. Still editing? Put it on the night shift.",
  "3 AM and still editing? Give Nightshift one topic: it writes, voices and edits the video, then waits for your OK. Private until you say so. What topic would you give it? nightshift-ai.studio",
  [("Extreme close-up of a tired young video creator's eyes lit by a laptop screen in a dark room at 3 a.m., slow blink, steam rising from a coffee mug.", "3 AM. *Still* editing?", "Three A.M. Still editing?"),
   ("A hand slowly closes a laptop lid in a dark bedroom; the screen glow fades from the creator's face.", "Close the *laptop*.", "Close the laptop."),
   ("A night city skyline through a window; windows across the buildings light up one by one in a steady rhythm.", "Give Nightshift *one* topic.", "Give Nightshift one topic."),
   ("A snowy white owl glides silently over a glowing night city, the camera tracking alongside it.", "Script. Voice. *Visuals.* Captions.", "It writes the script, the voice, the visuals and the captions."),
   ("A phone on a nightstand glows softly once in a dark bedroom while someone sleeps peacefully.", "It waits for *your* OK.", "Then it waits for your OK."),
   ("Golden sunrise light floods a cozy apartment; a young creator stretches and smiles, coffee in hand.", "Private until *you* say so.", "Finished videos upload as private, until you say so."),
   ("Macro close-up of a finger pressing a glowing keyboard key, a soft burst of warm light.", "*You* press publish.", "You press publish.")],
  [(HOME, "Nightshift writes the script, the voice, the visuals and the captions"), (HOME, "then waits for your OK"),
   (HOME, "Give it a topic"), (HOME, "Finished videos upload to YouTube as private"), (HOME, "Nothing goes public until you say so"), (HOME, "You press publish.")]),
 ("price", "Know the price before you press start.",
  "No surprise bills: on Nightshift the price is on the button before anything starts, and a failed run gives every held credit back. What would you make first? nightshift-ai.studio",
  [("A mysterious sealed envelope on a dark desk under a single lamp, slow push-in, tension.", "Surprise *bills?*", "Afraid of a surprise bill?"),
   ("A single glowing button in the dark, a hand hovering over it, hesitating.", "The price is on the *button*.", "On Nightshift, the price is on the button before anything starts."),
   ("An hourglass of glowing golden sand on a dark desk, slow motion.", "60 credits a *minute*.", "Sixty credits a minute of finished video."),
   ("Gold coins being set aside into a small glass jar, slow motion, warm light.", "Held when it *starts*.", "The credits are held when the run starts."),
   ("A long line of dominoes stops abruptly in a dark room, one domino refusing to fall.", "Run *failed?*", "And if a run fails?"),
   ("Gold coins floating back up into a glass jar in reverse slow motion, magical warm light.", "Every credit *comes back*.", "The credits come back on their own."),
   ("A relaxed creator leaning back in a chair at night, city lights behind, calm smile.", "Pay for what you *make*.", "Pay for what you make. Never for a failure.")],
  [(HOME, "The price is on the button before anything starts"), (HOME, "60 credits a minute of finished video"), (PRICING, "Held when it starts"),
   (HOME, "If a run fails, the credits come back on their own"), (HOME, "Pay for what you make. Never for a failure.")]),
 ("silkroad", "One topic. See the whole plan first.",
  "Type one topic, like why the Silk Road ran through Samarkand, and Nightshift shows the plan: working titles, script outline, shot list, thumbnail brief. Try it on the site, free: nightshift-ai.studio",
  [("A camel caravan crossing golden dunes at dusk toward a distant city of blue domes, wide aerial.", "One *topic*.", "One topic."),
   ("The Registan in Samarkand at golden hour, slow aerial drift over the domes.", "Why the Silk Road ran through *Samarkand*", "Why the Silk Road ran through Samarkand."),
   ("A night bazaar with warm lanterns and silk fabrics fluttering, slow dolly through it.", "Working *titles*.", "First, working titles."),
   ("Hands unrolling an old map on a wooden table under lamp light.", "Script *outline*.", "A script outline."),
   ("A film camera on a slider in a dusty courtyard at dusk, slow move.", "Shot *list*.", "A shot list."),
   ("Golden light raking across blue tiled domes, high contrast, one warm accent.", "Thumbnail *brief*.", "And a thumbnail brief."),
   ("A traveller's silhouette reaching the gate of a glowing city at night.", "See the plan *first*.", "See the plan, before anything is made.")],
  [(HOME, "Why the Silk Road ran through Samarkand"), (HOME, "Working titles"), (HOME, "Script outline"), (HOME, "Shot list"), (HOME, "Thumbnail brief"),
   (STUDIO, "Read the plan before anything is made.")]),
 ("airs", "Nothing airs until you say so.",
  "Every Nightshift video uploads to YouTube as private and passes a publish check first. Auto-publish is off unless you turn it on. Going public is your decision. nightshift-ai.studio",
  [("A heavy red theatre curtain, closed, a single spotlight and dust in the air.", "Nothing *airs*...", "Nothing airs"),
   ("Close-up of an owl's eyes opening in the dark, watchful and calm.", "...until *you* say so.", "until you say so."),
   ("A precious object inside a sealed glass display case in a dark museum, soft light.", "Uploads as *private*.", "Every finished video uploads to YouTube as private."),
   ("A careful flashlight beam sweeping across shelves in a dark archive.", "Publish check *first*.", "And passes a publish check first."),
   ("A person watching a screen in a dark living room, face softly lit, attentive.", "You *watch* it.", "You watch it."),
   ("Close-up of a wall light switch in the off position, a soft violet glow around it.", "Auto-publish: *off*.", "Auto-publish is off, unless you turn it on."),
   ("A theatre curtain opening onto a bright stage, warm light flooding the room.", "Your *call*.", "Going public is your decision.")],
  [(HOME, "Nothing airs until you say so."), (HOME, "Finished videos upload to YouTube as private and pass a publish check first"),
   (HOME, "Auto-publish is off unless you turn it on for a channel"), (STUDIO, "Going public is your decision"), (STUDIO, "You watch the video")]),
 ("studio", "Need one picture, one clip, one voice-over?",
  "Need one piece, not a whole video? Nightshift's Studio makes a picture, a clip or a voice-over, priced on the button. Animate it, upscale it, cut it out, then edit for free. nightshift-ai.studio",
  [("A hot air balloon drifting over a mirror-still lake at blue hour.", "Need *one* picture?", "Need one picture?"),
   ("A sailboat at sunset on a calm sea, slow pan.", "One *clip?*", "One clip?"),
   ("A studio microphone in a dark room, violet rim light, dust in the beam.", "One *voice-over?*", "One voice-over?"),
   ("A dove flying out of a framed painting of the sky in a dark gallery.", "Bring a still to *life*.", "Bring a still picture to life."),
   ("A blurry butterfly on a flower slowly coming into crisp, sharp focus, macro.", "Sharper. *Larger.*", "Upscale it. Sharper and larger."),
   ("A potted plant lifting out of a paper card, leaving its outline behind, soft studio light.", "Cut it *out*.", "Or remove the background."),
   ("Hands arranging film strips on a glowing light table at night.", "Edit it. *Free.*", "Then cut it together in the editor. Editing uses no credits.")],
  [(HOME, "Need just one piece? The Studio makes it."), (HOME, "Animate Bring a still picture to life"), (HOME, "Upscale Sharper and larger"),
   (HOME, "Cut out Remove the background"), (STUDIO, "Editing and exporting use no credits"), (CS, "Pictures, clips and voice‑overs, priced on the button.")]),
 ("languages", "Uzbek. Russian. English.",
  "Nightshift's app is in Uzbek, Russian and English, and each channel makes its videos in its own language, captions included. Which language is your channel? nightshift-ai.studio",
  [("The Registan in Samarkand illuminated at night, slow aerial drift.", "*Uzbek.*", "Uzbek."),
   ("A snowy city boulevard at night with warm street lamps, slow push.", "*Russian.*", "Russian."),
   ("A rainy city street at night with neon reflections on wet pavement.", "*English.*", "English."),
   ("Three paper lanterns of different colours rising together into the night sky.", "One app. *Three* languages.", "The app is in Uzbek, Russian and English."),
   ("A vintage radio microphone in a cozy studio, warm light.", "Each channel, *its own*.", "Each channel is set to one of the three for its videos."),
   ("Silhouettes of an audience in a small cinema watching a glowing screen.", "Captions in its *language*.", "Captions come in the channel's language."),
   ("Sunrise over blue domes and rooftops, golden light.", "Your *language*.", "Your channel, in your language.")],
  [(STUDIO, "The app is in Uzbek, Russian and English. Each channel is set to one of the three for its videos"), (HOME, "Captions On, in the channel’s language.")]),
 ("channels", "Run several channels. Keep the last word on each.",
  "Run one YouTube channel or several on Nightshift. Each keeps its own language, voice, style and schedule, and you keep the last word on every video. How many channels do you run? nightshift-ai.studio",
  [("One lit window in a tall dark apartment building at night, slow push-in.", "One *channel*.", "One channel."),
   ("Many windows across the building light up one after another, slow pull-back.", "Or *several*.", "Or several."),
   ("A chess player's hand moving a piece on a softly glowing board at night.", "Each keeps *its own* voice.", "Each keeps its own language, voice, style and schedule."),
   ("Two rivers of light flowing side by side through a night valley without mixing, aerial.", "They *never* mix.", "They never leak into another."),
   ("A conductor's hands in silhouette leading an orchestra, warm backlight.", "*You* keep the last word.", "And you keep the last word on each."),
   ("An owl perched on a high rooftop overlooking a glowing city at night.", "Auto-publish: *off*.", "Auto-publish is off unless you turn it on."),
   ("Sunrise over city rooftops, golden light spilling across them.", "Your channels. *Your* call.", "Your channels. Your call.")],
  [(YT, "Run one channel or several, and keep the last word on each."), (YT, "Language, voice, visual style and schedule are set per channel and never leak into another"),
   (HOME, "Auto-publish is off unless you turn it on for a channel")]),
 ("noswap", "Your voice, or no video.",
  "Picked a voice for your channel? If it is unavailable, Nightshift will not swap in a different one. The run stops, says why, and the credits come back. nightshift-ai.studio",
  [("A singer's silhouette on a dark stage under a single spotlight.", "*Your* voice.", "You picked the voice."),
   ("The stage spotlight flickers and goes out, leaving darkness and drifting dust.", "*Unavailable?*", "What if it is unavailable?"),
   ("A backstage door closing gently in a dim corridor.", "No *swap*.", "Nightshift will not swap in a different voice or model."),
   ("A red stop light glowing through rain at night, slow focus pull.", "The run *stops*.", "The run stops,"),
   ("A folded note slipped under a door by warm lamplight.", "...and says *why*.", "and says why."),
   ("Gold coins floating back into a glass jar in reverse slow motion.", "Credits *come back*.", "If a run fails, the credits come back on their own."),
   ("The singer's silhouette back in a warm spotlight, applause light.", "Your voice, or *no video*.", "Your voice, or no video.")],
  [(YT, "It will not swap in a different voice or model when the chosen one is unavailable — the run stops and says why"),
   (HOME, "If a run fails, the credits come back on their own")]),
 ("free", "100 free credits. No card.",
  "Start Nightshift tonight: 100 free credits, once, when you sign up with your email. No card. That is about one minute of finished video. What would you make with it? nightshift-ai.studio",
  [("A door opening onto warm light in a dark hallway, slow push.", "Try it *free*.", "Try it free."),
   ("A small gift box opening on a dark desk, warm light pouring out.", "*100* credits.", "One hundred credits, once, when you sign up."),
   ("A leather wallet lying closed on a table at night, untouched.", "*No* card.", "No card."),
   ("An hourglass with glowing sand, the last grains falling.", "About *1 minute* of video.", "That covers about one minute of finished video."),
   ("A person typing on a laptop in a cozy room at night, screen not visible.", "Just your *email*.", "You sign up with your email."),
   ("A hand hovering between two softly glowing orbs, choosing.", "Pay only when *you* choose.", "You pay only when you pick a plan or a pack."),
   ("Sunrise through a window onto a tidy desk.", "Start *tonight*.", "Start tonight.")],
  [(HOME, "100 free credits, once, when you sign up. No card."), (PRICING, "Your 100 free credits cover about 1 min of finished video at this rate"),
   (PRICING, "Email sign-up, no card. You pay only when you pick a plan or a pack.")]),
 ("storyboard", "Read the plan before it is rendered.",
  "On a channel with storyboard review, Nightshift stops before rendering. Move scenes, edit the words, then approve at the price on the button or discard it for free. nightshift-ai.studio",
  [("Storyboard sketches pinned on a wall in a dim film studio, slow pan.", "Read the *plan*.", "Read the plan,"),
   ("An empty director's chair under a single spotlight.", "Before it's *rendered*.", "before anything is rendered."),
   ("Hands rearranging storyboard cards on a wooden table.", "Move *scenes*.", "Move scenes, delete one, or add one."),
   ("Close-up of a pen sketching on paper under warm lamplight.", "Edit the *words*.", "Edit a scene's narration or visual."),
   ("A film clapperboard snapping shut in slow motion, dust in the light.", "Approve and *render*.", "Approve and render, at the price on the button."),
   ("Crumpled papers dropped calmly into a bin, soft light.", "Or discard. *Free.*", "Or discard it. Saying no costs nothing."),
   ("A cinema projector beam bursting to life in a dark room.", "Your *story*.", "Your story. Your call.")],
  [(STUDIO, "Nothing is rendered, and no render is charged, until you approve"), (STUDIO, "Edit a scene’s narration or visual description, move scenes, delete one or add one"),
   (STUDIO, "Discard a storyboard and nothing is rendered or charged"), (STUDIO, "Saying no costs nothing"), (STUDIO, "Save, and the price updates")]),
 ("editor", "Edit for zero credits.",
  "Nightshift's editor costs zero credits: trim, split, text on screen, music, speed from 0.5x to 2x, cross-fades, and vertical, wide or square. Export free. nightshift-ai.studio",
  [("Film reels spinning on an editing desk at night, warm lamp.", "Edit for *zero* credits.", "Edit for zero credits."),
   ("Macro shot of scissors cutting a film strip in warm light.", "Trim. *Split.*", "Trim and split any clip."),
   ("Neon light trails drawing smooth shapes in a dark room, long exposure feel.", "Text on *screen*.", "Put text on screen."),
   ("A vinyl record spinning on a turntable in a dim room, slow push.", "Add *music*.", "Add music and sound."),
   ("A water splash in slow motion, then speeding up.", "0.5x to *2x*.", "Change the speed, from half to double."),
   ("Violet and orange lights slowly blending into each other in fog.", "Cross-*fades*.", "Blend one clip into the next."),
   ("Three empty picture frames of different shapes on a dark wall: tall, wide and square.", "9:16. 16:9. *1:1.*", "Vertical, wide or square. Export free.")],
  [(STUDIO, "Editing and exporting use no credits"), (STUDIO, "Split a clip at the playhead"), (STUDIO, "Play a clip at 0.5×, 0.75×, 1.25×, 1.5× or 2×"),
   (STUDIO, "Blend one clip into the next"), (STUDIO, "Vertical 9:16, wide 16:9 or square 1:1"), (STUDIO, "Add text")]),
 ("styles", "28 looks. Or your own.",
  "Give your channel a look: 28 written art directions in Nightshift's Studio, or your own kit from 3-12 pictures. Keep a character or product under an @name. A style adds no credits. nightshift-ai.studio",
  [("Three identical vases on a shelf, each lit in a different colour, slow dolly.", "*28* looks.", "Twenty-eight written art directions."),
   ("A painter mixing glowing paint on a palette at night.", "Or *your* own.", "Or your own look,"),
   ("Twelve instant photos laid out on a dark table under a lamp.", "From *3-12* pictures.", "saved from three to twelve pictures."),
   ("A small handmade clay figure turning slowly on a pottery wheel.", "Keep a *character*.", "Keep a recurring character,"),
   ("A glass perfume bottle without labels rotating on a turntable in studio light.", "...or a *product*.", "or a product, under an at-name."),
   ("A neat stack of gold coins standing still, untouched, soft light.", "No extra *credits*.", "A style adds no credits."),
   ("A gallery wall of artworks sharing one consistent style, slow pan.", "Your look. *Every* time.", "Your look, every time.")],
  [(CS, "Start from 28 written art directions in the style library, or save your own look from 3–12 pictures"), (CS, "keep a recurring character or product under an @name"),
   (CS, "A style adds no credits")]),
 ("data", "Your Google data, only for your channel.",
  "Nightshift uses your Google account only to upload to the channel you connect and show you its analytics. Tokens are encrypted, never reach the browser, never used for ads. Revoke any time. nightshift-ai.studio",
  [("A glowing padlock resting on a dark wooden desk, soft violet rim light, slow orbit.", "Your *data*.", "Your Google data."),
   ("A key sliding smoothly into a lock, warm light, macro.", "Only for *your* channel.", "Used only to upload to the channel you connect,"),
   ("Rising light trails in a dark space, like a growing chart.", "Your *numbers*, for you.", "and to show you its analytics."),
   ("A heavy vault door closing slowly in a dim corridor.", "*Encrypted.*", "Access tokens are encrypted,"),
   ("A sealed envelope locked inside a small safe.", "Never in the *browser*.", "and never reach the browser."),
   ("Rooftop billboards switching off one by one over a night city.", "*Never* for ads.", "Never used for advertising."),
   ("A hand turning a key and pulling it out of a lock, calm.", "Revoke *any time*.", "Revoke access any time.")],
  [(HOME, "Nightshift uses your Google account only to upload videos to the YouTube channel you connect and to read that channel's data and analytics for your dashboard"),
   (HOME, "Access tokens are encrypted and never reach the browser"), (HOME, "the data is never used for advertising"), (HOME, "you can revoke access at any time")]),
]


# One cast and one set per ad, repeated prompt: shots are generated one by one, and without this
# each one invents a different person and a different room, so the ad reads as unrelated clips glued together.
ANCHOR = {
 "nightshift": "Same young woman (short dark hair, oversized grey hoodie), same small city apartment with a desk by a big window, same city skyline outside.",
 "price": "Same young man (curly hair, navy sweater), same dark home office with a wooden desk, one brass lamp and a glass jar, violet-and-amber light.",
 "silkroad": "Same world: an ancient Silk Road city of blue-tiled domes in golden dusk light, warm dust, one traveller in a sand-coloured cloak.",
 "airs": "Same world: a dark old theatre with red velvet curtains, one white owl, one young woman (long braid, black turtleneck) watching from the seats.",
 "studio": "Same set: one creator's night studio with a long oak table, a big window on a lake, violet-and-amber lamp light; same pair of hands (silver ring).",
 "languages": "Same traveller (young man, olive coat, leather backpack) walking through cities at night, same warm-lantern colour grade.",
 "channels": "Same tall apartment building at night, same young woman (red scarf) as the operator in close shots, same owl on the roof.",
 "noswap": "Same world: one small dark theatre, one singer (silhouette, long coat), one spotlight, one backstage corridor.",
 "free": "Same young woman (curly hair, yellow cardigan), same cozy attic room with a round window, string lights, a wooden desk.",
 "storyboard": "Same set: one film studio office with storyboards on the wall, one director (young man, cap, glasses), warm tungsten light.",
 "editor": "Same set: one night editing room with a wooden desk, film reels, a turntable and neon tubes; same pair of hands (black watch).",
 "styles": "Same set: one small art studio at night with white shelves, a work table and a lamp; same pair of hands (paint on fingers).",
 "data": "Same set: one dark office with a steel safe, a wooden desk and a window on the city; same pair of hands (white shirt cuffs).",
}


REVIVE = {("ep037-price", 1)}   # prompt reworded after two nsfw rejections; try it again


def main():
    pp = os.path.join(ROOT, "queue", "plan.json"); old = json.load(open(pp))["episodes"]
    keep = [e for e in old if e["render"] == "stashed" and e.get("format") != "cine"]
    for e in keep:
        e["published"] = e.get("published") or "superseded: owner asked for the cinematic format (2026-11-13); not published"
    plan = []
    for n, (slug, title, xtext, shots, facts) in enumerate(ADS):
        eid = f"ep{n + 36:03d}-{slug}"; pal = PALS[n % len(PALS)]; topic = TOPICS[n % len(TOPICS)]
        assert len(xtext) < 280 and "nightshift-ai.studio" in xtext and "https://" not in xtext, eid
        done_ep = next((e for e in old if e["id"] == eid and (e["render"] == "stashed" or e.get("published"))), None)
        if done_ep:          # already made or published: leave its files and state exactly as they are
            plan.append(done_ep); continue
        scenes = [{"type": "shot", "big": big, "sentences": [line], "broll": f"broll/{eid}-{k}.mp4"} for k, (_, big, line) in enumerate(shots)]
        scenes.append({"type": "end", "broll": f"broll/{eid}-7.mp4", "big": "Type your topic. See the plan.", "sentences": [
            "Type your own topic at nightshift-ai dot studio, and see the plan.",
            "One hundred free credits. No card."]})
        json.dump({"id": eid, "palette": pal, "title": title, "format": "cine", "scenes": scenes},
                  open(os.path.join(ROOT, "episodes", eid + ".json"), "w"), indent=1)
        prev = {c["key"]: c for e in old if e["id"] == eid for c in e["clips"]}
        o = next((e for e in old if e["id"] == eid), {})
        clips = [dict(key=f"{eid}-{k}", scene=k, prompt=cine_prompts.BIBLE[slug] + " SHOT: " + (cine_prompts.SHOTS[slug] + [cine_prompts.END[slug]])[k] + " " + cine_prompts.FILM, status=("todo" if prev.get(f"{eid}-{k}", {}).get("status") == "skipped" and (eid, k) in REVIVE else prev.get(f"{eid}-{k}", {}).get("status", "todo")),
                      job_id=prev.get(f"{eid}-{k}", {}).get("job_id"), url=prev.get(f"{eid}-{k}", {}).get("url"), **({"note": prev[f"{eid}-{k}"]["note"]} if prev.get(f"{eid}-{k}", {}).get("note") and not (eid, k) in REVIVE else {})) for k, (pr, _, _) in enumerate(shots + [("", "", "")])]
        plan.append(dict(id=eid, day=n + 1, title=title, palette=pal, format="cine", x_text=xtext,
                         facts=[{"page": p, "quote": q} for p, q in facts + TRY_FACTS],
                         clips=clips, render=o.get("render", "todo"), asset=o.get("asset"), published=o.get("published")))
    json.dump({"note": "Cinematic queue (2026-11-13). 13 ads x 7 Higgsfield shots + 1 cinematic end shot (from ep037). See RUNBOOK.md 'Queue'. "
                       "status: todo -> submitted -> done | skipped; render: todo -> stashed | failed", "episodes": keep + plan},
              open(pp, "w"), indent=1)
    print("wrote", len(plan), "cinematic ads;", sum(len(e["clips"]) for e in plan), "clips")


if __name__ == "__main__":
    main()
