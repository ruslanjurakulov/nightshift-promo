#!/usr/bin/env python3
"""Second wave of the cinematic queue (owner, 2026-11-14: "nobody else will use Higgsfield; make as many as the
unlimited window allows, don't stop").

Each ad is one CREATOR WORLD (a person with a niche YouTube channel, their place, their night) told in 8 shots that
always follow the same arc: late-night struggle -> hands the work over -> the night does its work -> craft detail
-> rest -> morning check -> payoff -> wide end shot with calm space for the call to action. Over that arc runs one
ANGLE: seven titles and lines, each quoted from the live site. The footage is about a real kind of creator; the
words are about the product; the arc keeps them in step, so no shot is a random clip under an unrelated line.
Appends ep049+ to queue/plan.json; already made or published episodes are never touched.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cine_prompts import FILM
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME, STUDIO, PRICING = "https://nightshift-ai.studio", "https://nightshift-ai.studio/studio", "https://nightshift-ai.studio/pricing"
YT, CS = "https://nightshift-ai.studio/solutions/youtube-channels", "https://nightshift-ai.studio/solutions/creative-studio"
PALS = ["candy", "sunrise", "forest", "ember"]
END_FACTS = [(HOME, "Type a topic. See what the plan looks like."), (HOME, "100 free credits, once, when you sign up. No card.")]

# name, bible, 8 shots in arc order (R1..R8). Screens are never readable; faces are fictional.
WORLDS = [
 ("lighthouse", "CAST: Elena, 40, weathered windbreaker in deep red, grey-streaked hair tied back, runs a channel about the sea. SET: a working lighthouse on a rocky cape, the lamp room with its great glass lens, a small keeper's room with a wooden desk, a laptop and a kettle. LIGHT PLAN: night = sweeping lighthouse beam, storm-blue moonlight, warm oil-lamp practical; dawn = pale gold over a calm sea. PALETTE: storm blue, brass, warm amber, sea green.",
  ["Medium close-up of Elena at the desk in the keeper's room at 2 a.m., 50mm, slow push-in. 0-3s: she rubs her eyes as the lighthouse beam sweeps across the window behind her; 3-5s: rain streaks the glass, the laptop glow on her tired face.",
   "Close-up of Elena's hands, 65mm, slow arc. 0-3s: she types one short line on the laptop (screen not visible); 3-5s: she closes the lid gently and leans back, relieved.",
   "Extreme wide aerial of the lighthouse on the cape at night, 24mm, slow orbit. 0-5s: the great beam sweeps over a storm-tossed sea, waves exploding on the rocks, rain glittering in the light.",
   "Macro of the lighthouse's Fresnel lens turning in the lamp room, 100mm, locked off. 0-5s: prisms of light split and slide across the brass, slow and hypnotic.",
   "Medium shot of Elena asleep in an armchair under a wool blanket, 40mm, slow overhead slide. 0-5s: the beam passes softly over her, the kettle steams on the stove, calm.",
   "Medium shot of Elena at the window at dawn, 50mm, slow push-in. 0-3s: she opens the laptop with a mug of tea (screen not visible); 3-5s: a small surprised smile.",
   "Close-up of Elena's finger pressing a key, 100mm macro, slow push. 0-3s: pale gold dawn light, salt on the window; 3-5s: the key goes down and she laughs quietly.",
   "Extreme wide shot of the lighthouse at sunrise, 24mm, slow drone rise. 0-5s: calm sea, gulls, the lamp still glowing faintly; a vast soft pink sky fills the upper half. Peaceful."]),
 ("bakery", "CAST: Bekzod, 35, flour-dusted dark apron over a white tee, short beard, runs a channel about bread. SET: a small night bakery with a stone oven, a wooden kneading table, linen-covered proofing baskets, a laptop on a shelf. LIGHT PLAN: night = warm oven glow and one hanging bulb, blue street light through the window; dawn = soft gold through the front glass. PALETTE: wheat gold, fire orange, flour white, night blue.",
  ["Medium close-up of Bekzod at the kneading table at 3 a.m., 50mm, slow push-in. 0-3s: he wipes flour from his brow, exhausted; 3-5s: he glances at the laptop on the shelf, its cold glow against the warm oven.",
   "Close-up of Bekzod's floury hands on the laptop, 65mm, slow arc. 0-3s: he types one short line (screen not visible); 3-5s: he closes it and dusts his hands, decided.",
   "Wide shot of the dark bakery, 28mm, slow dolly along the shelves. 0-5s: in the proofing baskets the dough slowly rises, the stone oven breathing orange light, flour hanging in the air.",
   "Macro of a loaf's crust splitting open in the oven, 100mm, time-lapse feel. 0-5s: the score blooms, steam curls, the crust turns deep gold.",
   "Medium shot of Bekzod napping on a flour sack in the corner, 40mm, slow slide. 0-5s: the oven glow pulses softly on him, a cat curls up at his feet.",
   "Medium shot of Bekzod at dawn by the front window, 50mm, slow push-in. 0-3s: he opens the laptop beside a tray of fresh loaves (screen not visible); 3-5s: he grins.",
   "Close-up of Bekzod's finger pressing a key, 100mm macro. 0-3s: gold morning light and steam from the bread; 3-5s: the key goes down, flour puffs up from the keyboard.",
   "Wide shot of the bakery front at sunrise from the street, 28mm, slow pull-back. 0-5s: warm windows, loaves stacked, the first customers arriving; clear morning sky over the rooftops in the upper half."]),
 ("observatory", "CAST: Malika, 29, round glasses, burgundy knit beanie, oversized denim jacket, runs a channel about the night sky. SET: a small rooftop observatory with a brass telescope, star charts pinned to wood panels, a laptop on a folding table, a thermos. LIGHT PLAN: deep blue moonlight, red astronomer's headlamp as practical, faint city glow on the horizon; dawn = lavender to gold. PALETTE: indigo, moon silver, brass, red accent.",
  ["Medium close-up of Malika at the folding table at 2 a.m., 50mm, slow push-in. 0-3s: she yawns, her red headlamp lighting her breath in the cold; 3-5s: the laptop glow on her tired face, the telescope behind her.",
   "Close-up of Malika's gloved hands on the laptop, 65mm. 0-3s: she types one short line (screen not visible); 3-5s: she closes it and pulls her beanie down, smiling.",
   "Extreme wide shot of the night sky over the observatory dome, 24mm, slow tilt up. 0-5s: the Milky Way wheels slowly, a shooting star crosses, the dome glows faintly.",
   "Macro of the brass telescope focuser, 100mm, slow rack focus. 0-5s: the full moon sharpens from a blur into crisp craters reflected in the eyepiece.",
   "Medium shot of Malika asleep in a camping chair wrapped in a blanket, 40mm, slow overhead slide. 0-5s: moonlight silvers her face, the thermos steams.",
   "Medium shot of Malika at dawn, 50mm, slow push-in. 0-3s: lavender light, she opens the laptop (screen not visible); 3-5s: she covers her mouth in happy surprise.",
   "Close-up of Malika's finger pressing a key, 100mm macro. 0-3s: first gold light on the brass telescope; 3-5s: the key goes down.",
   "Extreme wide shot of the rooftop observatory at sunrise, 24mm, slow drone rise. 0-5s: the dome opens to a soft lavender-gold sky filling the upper half, the city waking below."]),
 ("teacher", "CAST: Ustoz Rustam, 55, neat grey beard, dark green chapan over a white shirt, runs a history channel. SET: an old study in Samarkand with carved wooden doors, shelves of old books, a brass lamp, a laptop on a carpet-covered table, a window on the turquoise domes. LIGHT PLAN: night = warm brass lamp, moonlit domes outside; dawn = saffron light on the domes. PALETTE: turquoise, saffron, walnut, deep red carpet.",
  ["Medium close-up of Rustam at the table at midnight, 50mm, slow push-in. 0-3s: he takes off his glasses and rubs his eyes among piles of books; 3-5s: the laptop glow on his face, moonlit domes in the window.",
   "Close-up of Rustam's hands on the laptop, 65mm, slow arc. 0-3s: he types one short line (screen not visible); 3-5s: he closes it and rests his hand on an old book.",
   "Wide aerial of Samarkand's domes at night, 28mm, slow orbit. 0-5s: the Registan lit gold and turquoise, swallows crossing the moon.",
   "Macro of an old manuscript page with miniature paintings turning in lamp light, 100mm. 0-5s: gold leaf glints, no legible writing.",
   "Medium shot of Rustam dozing in an armchair, 40mm, slow slide. 0-5s: the brass lamp glows, a cup of green tea steams on the carpet.",
   "Medium shot of Rustam at the window at dawn, 50mm, slow push-in. 0-3s: saffron light, he opens the laptop (screen not visible); 3-5s: a warm proud smile.",
   "Close-up of Rustam's finger pressing a key, 100mm macro. 0-3s: saffron light, dust in the air; 3-5s: the key goes down.",
   "Extreme wide aerial of the domes of Samarkand at sunrise, 24mm, slow forward glide. 0-5s: turquoise tiles catching gold light, a clean pale sky fills the upper half."]),
 ("chef", "CAST: Dilnoza, 33, white chef's jacket with rolled sleeves, hair under a black bandana, runs a cooking channel. SET: a small restaurant kitchen after closing, steel counters, copper pans on hooks, a gas range, a laptop beside a cutting board. LIGHT PLAN: night = single warm pendant over the pass, blue flame glow, dark dining room; dawn = clean white light through a back window. PALETTE: copper, steel, flame blue, herb green.",
  ["Medium close-up of Dilnoza at the steel counter after midnight, 50mm, slow push-in. 0-3s: she leans on the counter, exhausted, the pendant light above; 3-5s: the laptop glow beside the cutting board.",
   "Close-up of Dilnoza's hands on the laptop, 65mm. 0-3s: she types one short line (screen not visible); 3-5s: she closes it and unties her bandana.",
   "Wide shot of the empty kitchen at night, 28mm, slow dolly. 0-5s: copper pans sway gently, a pot simmers on a low blue flame, steam drifting through the pendant light.",
   "Macro of herbs being chopped on a wooden board in slow motion, 100mm. 0-5s: green leaves flutter, droplets fly, the knife flashes.",
   "Medium shot of Dilnoza asleep at a dining table, head on her arms, 40mm, slow slide. 0-5s: chairs stacked, city lights through the window.",
   "Medium shot of Dilnoza at dawn, 50mm, slow push-in. 0-3s: white morning light, she opens the laptop with an espresso (screen not visible); 3-5s: she smiles.",
   "Close-up of Dilnoza's finger pressing a key, 100mm macro. 0-3s: steam from the espresso; 3-5s: the key goes down.",
   "Wide shot of the restaurant front at sunrise from across the street, 28mm, slow pull-back. 0-5s: the chef's light still on, a clean morning sky in the upper half."]),
 ("cabin", "CAST: Javlon, 31, red flannel shirt, knit cap, short beard, runs a hiking and travel channel. SET: a wooden mountain cabin with a stone fireplace, maps and a coil of rope on the wall, a laptop on a log table, snowy peaks outside. LIGHT PLAN: night = fire glow and cold moonlight on snow; dawn = alpenglow pink on the peaks. PALETTE: fire orange, snow blue, pine green, alpenglow pink.",
  ["Medium close-up of Javlon at the log table at 1 a.m., 50mm, slow push-in. 0-3s: he warms his hands, tired, fire crackling; 3-5s: the laptop glow on his face, snow falling outside.",
   "Close-up of Javlon's hands on the laptop, 65mm. 0-3s: he types one short line (screen not visible); 3-5s: he closes it and stretches toward the fire.",
   "Extreme wide shot of the snowy valley at night, 24mm, slow drone glide. 0-5s: the cabin's single window glows, aurora-like moonlit clouds roll over the peaks.",
   "Macro of embers in the fireplace, 100mm, locked off. 0-5s: sparks lift and swirl in slow motion.",
   "Medium shot of Javlon asleep in a sleeping bag by the fire, 40mm, slow overhead slide. 0-5s: firelight flickers, snow ticks against the glass.",
   "Medium shot of Javlon at the window at dawn, 50mm, slow push-in. 0-3s: pink alpenglow on the peaks, he opens the laptop (screen not visible); 3-5s: he grins.",
   "Close-up of Javlon's finger pressing a key, 100mm macro. 0-3s: pink light, frost on the window; 3-5s: the key goes down.",
   "Extreme wide shot of the cabin and peaks at sunrise, 24mm, slow drone rise. 0-5s: alpenglow on the snow, wide clear sky in the upper half."]),
 ("watchmaker", "CAST: Anvar, 60, loupe on his forehead, brown leather apron, rolled shirt sleeves, runs a channel about fixing old watches. SET: a tiny workshop with a green-shaded lamp, a wall of ticking clocks, a bench of tiny tools, a laptop on the shelf. LIGHT PLAN: one green banker's lamp, brass reflections, deep shadows; dawn = soft window light. PALETTE: brass, green, walnut, black.",
  ["Medium close-up of Anvar at the bench at 2 a.m., 50mm, slow push-in. 0-3s: he lowers the loupe and rubs his eyes; 3-5s: a wall of clocks ticks behind him, the laptop glows on the shelf.",
   "Close-up of Anvar's hands on the laptop, 65mm. 0-3s: he types one short line (screen not visible); 3-5s: he closes it with a satisfied tap.",
   "Wide shot of the wall of clocks, 28mm, slow dolly. 0-5s: dozens of pendulums swing in rhythm, the hands creep toward morning.",
   "Macro of a watch movement, 100mm, locked off. 0-5s: gears and a balance wheel turn, a jewel catches the light.",
   "Medium shot of Anvar asleep in his chair, 40mm, slow slide. 0-5s: the green lamp glows, clocks tick softly around him.",
   "Medium shot of Anvar at dawn, 50mm, slow push-in. 0-3s: soft window light, he opens the laptop (screen not visible); 3-5s: he chuckles.",
   "Close-up of Anvar's finger pressing a key, 100mm macro. 0-3s: brass reflections; 3-5s: the key goes down as all the clocks chime.",
   "Wide shot of the workshop from the doorway at sunrise, 28mm, slow pull-back. 0-5s: morning light floods in, clocks gleaming; plain warm wall above fills the upper half."]),
 ("greenhouse", "CAST: Sevara, 27, green overalls over a striped shirt, hair in a messy bun, runs a plants channel. SET: a glass greenhouse full of tropical plants, misting pipes, a potting bench with a laptop. LIGHT PLAN: night = purple grow lights and moonlight through glass; dawn = soft mist and gold. PALETTE: leaf green, grow-light magenta, glass silver, gold.",
  ["Medium close-up of Sevara at the potting bench at midnight, 50mm, slow push-in. 0-3s: soil on her cheek, tired; 3-5s: the laptop glows among the plants under purple grow lights.",
   "Close-up of Sevara's hands on the laptop, 65mm. 0-3s: she types one short line (screen not visible); 3-5s: she closes it and smiles at a seedling.",
   "Wide shot of the greenhouse at night, 28mm, slow dolly. 0-5s: misting pipes release fog, leaves glisten under grow lights, the moon through the glass roof.",
   "Macro of a fern frond slowly unfurling, 100mm, time-lapse feel. 0-5s: dew drops roll along it.",
   "Medium shot of Sevara asleep in a hammock between plants, 40mm, slow slide. 0-5s: fog drifts, grow lights hum softly.",
   "Medium shot of Sevara at dawn, 50mm, slow push-in. 0-3s: gold mist, she opens the laptop (screen not visible); 3-5s: she beams.",
   "Close-up of Sevara's finger pressing a key, 100mm macro. 0-3s: a dew drop falls nearby; 3-5s: the key goes down.",
   "Wide shot of the greenhouse at sunrise from outside, 28mm, slow pull-back. 0-5s: gold light through misty glass, a clean pale sky fills the upper half."]),
 ("musician", "CAST: Kamron, 26, curly hair, headphones around his neck, black bomber jacket, runs a music channel. SET: a small home studio with a keyboard, a guitar on a stand, foam panels, a laptop on the desk, a window on a rainy city. LIGHT PLAN: night = warm desk lamp, blue rain light, a red tally light; dawn = grey-gold after rain. PALETTE: deep blue, warm amber, red accent.",
  ["Medium close-up of Kamron at the keyboard at 3 a.m., 50mm, slow push-in. 0-3s: he drops his head on his arms, exhausted; 3-5s: rain on the window, the laptop glowing.",
   "Close-up of Kamron's hands on the laptop, 65mm. 0-3s: he types one short line (screen not visible); 3-5s: he closes it and hangs his headphones up.",
   "Wide shot of the rainy city from the studio window, 28mm, slow push. 0-5s: neon reflections ripple in puddles, a night bus passes, rain glitters.",
   "Macro of a guitar string vibrating, 100mm. 0-5s: the string blurs in slow motion, light catching its edge.",
   "Medium shot of Kamron asleep on a sofa with headphones on, 40mm, slow slide. 0-5s: the red tally light blinks softly.",
   "Medium shot of Kamron at dawn, 50mm, slow push-in. 0-3s: grey-gold light after rain, he opens the laptop (screen not visible); 3-5s: he grins and nods to a beat.",
   "Close-up of Kamron's finger pressing a key, 100mm macro. 0-3s: drops on the window behind; 3-5s: the key goes down.",
   "Wide shot of the rain-washed city at sunrise from a rooftop, 24mm, slow drone rise. 0-5s: wet rooftops shine, a soft clearing sky fills the upper half."]),
 ("garage", "CAST: Farhod, 38, grease-stained grey coveralls, short hair, runs a car restoration channel. SET: a garage with a half-restored 1970s coupe, tool walls, an engine hoist, a laptop on a workbench. LIGHT PLAN: night = hanging work lamps and a welding glow; dawn = light through a half-open roller door. PALETTE: steel, sodium orange, primer grey, chrome.",
  ["Medium close-up of Farhod at the workbench at 1 a.m., 50mm, slow push-in. 0-3s: he wipes grease from his hands, tired; 3-5s: the laptop glows among tools, the old coupe behind him.",
   "Close-up of Farhod's hands on the laptop, 65mm. 0-3s: he types one short line (screen not visible); 3-5s: he closes it and pats the car's fender.",
   "Wide shot of the garage at night, 28mm, slow dolly around the coupe. 0-5s: work lamps sway, chrome glints, sparks from a forgotten grinder fade.",
   "Macro of a chrome hubcap being polished, 100mm. 0-5s: the reflection sharpens as the cloth passes.",
   "Medium shot of Farhod asleep in the car's driver's seat, 40mm, slow slide. 0-5s: a work lamp glows on the windshield.",
   "Medium shot of Farhod at dawn by the roller door, 50mm, slow push-in. 0-3s: light floods under the door, he opens the laptop (screen not visible); 3-5s: he laughs.",
   "Close-up of Farhod's finger pressing a key, 100mm macro. 0-3s: dawn light on the chrome; 3-5s: the key goes down.",
   "Wide shot of the coupe rolling out of the garage into sunrise, 28mm, slow pull-back. 0-5s: the street glows gold, an open morning sky in the upper half."]),
 ("pottery", "CAST: Zarina, 34, clay-spattered linen apron, silver bangles pushed up, hair in a scarf, runs a ceramics channel. SET: a ceramics studio with a potter's wheel, shelves of glazed bowls, a kiln, a laptop on a stool. LIGHT PLAN: night = kiln glow and one warm bulb; dawn = soft north window light. PALETTE: terracotta, kiln orange, glaze blue, cream.",
  ["Medium close-up of Zarina at the wheel at midnight, 50mm, slow push-in. 0-3s: clay on her arms, she slumps, tired; 3-5s: the laptop glows on a stool beside her.",
   "Close-up of Zarina's clay-dusted hands on the laptop, 65mm. 0-3s: she types one short line (screen not visible); 3-5s: she closes it and smiles.",
   "Wide shot of the studio at night, 28mm, slow dolly. 0-5s: the kiln glows orange, rows of bowls cast long shadows, dust in the bulb light.",
   "Macro of a bowl rising on the spinning wheel, 100mm. 0-5s: wet clay climbs between two hands, perfectly smooth.",
   "Medium shot of Zarina asleep on a bench, 40mm, slow slide. 0-5s: the kiln's glow breathes on her.",
   "Medium shot of Zarina at dawn, 50mm, slow push-in. 0-3s: soft window light, she opens the laptop (screen not visible); 3-5s: she laughs.",
   "Close-up of Zarina's finger pressing a key, 100mm macro. 0-3s: glazed bowls glinting behind; 3-5s: the key goes down.",
   "Wide shot of the studio at sunrise, 28mm, slow pull-back. 0-5s: shelves of finished bowls glowing in morning light; calm plaster wall above fills the upper half."]),
 ("boat", "CAST: Aziz, 36, yellow rain jacket, wet hair, runs a channel about the ocean. SET: a small research boat at night, a cabin with charts, a laptop in a waterproof case, a lantern. LIGHT PLAN: night = lantern and deck lights, black sea; dawn = pearl grey to gold over the water. PALETTE: sea black, lantern amber, jacket yellow, pearl.",
  ["Medium close-up of Aziz in the boat's cabin at 2 a.m., 50mm, slow push-in. 0-3s: the cabin rocks gently, he rubs his eyes; 3-5s: the laptop glows, lantern swinging.",
   "Close-up of Aziz's hands on the laptop, 65mm. 0-3s: he types one short line (screen not visible); 3-5s: he closes it and steps out on deck.",
   "Wide shot from the deck at night, 28mm, slow drift. 0-5s: bioluminescent plankton glow blue in the wake, stars above the black sea.",
   "Macro underwater of a jellyfish pulsing in the deck lights, 100mm. 0-5s: it drifts gracefully, glowing.",
   "Medium shot of Aziz asleep in a bunk, 40mm, slow slide. 0-5s: the lantern sways, waves lap the hull.",
   "Medium shot of Aziz on deck at dawn, 50mm, slow push-in. 0-3s: pearl light, he opens the laptop (screen not visible); 3-5s: he smiles widely.",
   "Close-up of Aziz's finger pressing a key, 100mm macro. 0-3s: salt spray glints; 3-5s: the key goes down.",
   "Extreme wide aerial of the small boat on a calm sea at sunrise, 24mm, slow rise. 0-5s: dolphins arc nearby, a vast gold sky in the upper half."]),
 ("atelier", "CAST: Madina, 30, black turtleneck, tape measure around her neck, sleek ponytail, runs a fashion channel. SET: a tailoring atelier with a dress form, bolts of silk, a vintage sewing machine, a laptop on the cutting table. LIGHT PLAN: night = one spotlight on the dress form and warm desk lamps; dawn = pale light through tall windows. PALETTE: ivory silk, emerald, black, gold thread.",
  ["Medium close-up of Madina at the cutting table at 1 a.m., 50mm, slow push-in. 0-3s: pins in her mouth, she sighs, exhausted; 3-5s: the laptop glows beside the fabric.",
   "Close-up of Madina's hands on the laptop, 65mm. 0-3s: she types one short line (screen not visible); 3-5s: she closes it and drapes the tape measure.",
   "Wide shot of the atelier at night, 28mm, slow dolly. 0-5s: silk drapes ripple in a breeze from the window, the dress form stands in a spotlight.",
   "Macro of a needle stitching emerald silk, 100mm. 0-5s: gold thread pulls through in slow motion.",
   "Medium shot of Madina asleep on a velvet chaise, 40mm, slow slide. 0-5s: silk scraps around her, the lamp glows.",
   "Medium shot of Madina at dawn, 50mm, slow push-in. 0-3s: pale window light, she opens the laptop (screen not visible); 3-5s: a delighted smile.",
   "Close-up of Madina's finger pressing a key, 100mm macro. 0-3s: silk shimmering behind; 3-5s: the key goes down.",
   "Wide shot of the atelier at sunrise, 28mm, slow pull-back. 0-5s: the finished emerald dress on the form glows in the light; tall bright windows fill the upper half."]),
 ("gamer", "CAST: Doniyor, 22, oversized black hoodie, gaming headset, bleached fringe, runs a tech review channel. SET: a small neon-lit room with an RGB keyboard, a microphone arm, gadgets on shelves, a laptop. LIGHT PLAN: night = cyan and magenta LED strips, monitor glow; dawn = grey-blue daylight overpowering the neon. PALETTE: cyan, magenta, black, white.",
  ["Medium close-up of Doniyor at 4 a.m., 50mm, slow push-in. 0-3s: he slumps in his gaming chair, headset askew; 3-5s: neon glow on his tired face.",
   "Close-up of Doniyor's hands on the laptop, 65mm. 0-3s: he types one short line (screen not visible); 3-5s: he closes it and drops the headset on the desk.",
   "Wide shot of the neon city outside his window, 28mm, slow push. 0-5s: signs (no readable letters) pulse, a drone of lights crosses the sky.",
   "Macro of an RGB keyboard as the colours ripple across the keys, 100mm. 0-5s: a wave of light rolls from left to right.",
   "Medium shot of Doniyor asleep in the gaming chair, 40mm, slow slide. 0-5s: LEDs fade to a soft breathing glow.",
   "Medium shot of Doniyor at dawn, 50mm, slow push-in. 0-3s: daylight washes out the neon, he opens the laptop (screen not visible); 3-5s: he pumps his fist.",
   "Close-up of Doniyor's finger pressing a key, 100mm macro. 0-3s: last neon glints; 3-5s: the key goes down.",
   "Wide shot of the neon city at sunrise, 24mm, slow drone rise. 0-5s: the signs switch off, a clean blue-gold sky fills the upper half."]),
 ("storyteller", "CAST: Buvi Oydin, 70, white headscarf with a blue pattern, kind wrinkled face, embroidered vest, runs a folk tales channel. SET: a village house with a carpeted sitting room, a tandir oven in the yard, a samovar, a laptop on a low table. LIGHT PLAN: night = lantern and samovar glow, starry sky over the yard; dawn = rose light on adobe walls. PALETTE: indigo, rose, clay, brass.",
  ["Medium close-up of Buvi Oydin on the floor cushions at midnight, 50mm, slow push-in. 0-3s: she adjusts her glasses, tired; 3-5s: the laptop glows on the low table beside the samovar.",
   "Close-up of her hands on the laptop, 65mm. 0-3s: she types one short line slowly (screen not visible); 3-5s: she closes it and pats it fondly.",
   "Wide shot of the village at night, 28mm, slow crane up. 0-5s: flat rooftops under a sky full of stars, a dog trots across a lantern-lit lane.",
   "Macro of the samovar's spout pouring tea into a blue bowl, 100mm. 0-5s: steam curls, the tea glows amber.",
   "Medium shot of Buvi Oydin asleep under a quilt, 40mm, slow slide. 0-5s: lantern light, a cat purring at her side.",
   "Medium shot of her at dawn in the yard, 50mm, slow push-in. 0-3s: rose light on adobe walls, she opens the laptop (screen not visible); 3-5s: she claps her hands in joy.",
   "Close-up of her finger pressing a key, 100mm macro. 0-3s: tandir smoke drifting; 3-5s: the key goes down.",
   "Wide shot of the village yard at sunrise, 28mm, slow pull-back. 0-5s: bread baking in the tandir, children waving; a soft rose sky fills the upper half."]),
]

# 7 beats per angle in arc order: (title with *accent*, spoken line). The 8th shot is the end card.
ANGLES = [
 ("topic", "One topic. A finished video. You press publish.",
  [("Up all *night*?", "Up all night again?"), ("Give it *one* topic.", "Give Nightshift one topic."), ("Script. Voice. *Visuals.*", "It writes the script, the voice and the visuals,"),
   ("And the *captions*.", "and the captions."), ("It waits for *your* OK.", "Then it waits for your OK."), ("Private until *you* say so.", "Finished videos upload as private, until you say so."),
   ("*You* press publish.", "You press publish.")],
  [(HOME, "Nightshift writes the script, the voice, the visuals and the captions"), (HOME, "and wait for your OK"), (HOME, "Finished videos upload to YouTube as private"),
   (HOME, "Nothing goes public until you say so"), (HOME, "You press publish.")]),
 ("price", "See the price first. A failed run costs nothing.",
  [("What will it *cost?*", "What will it cost?"), ("The price comes *first*.", "The price is on the button before anything starts."), ("60 credits a *minute*.", "Sixty credits a minute of finished video."),
   ("Held when it *starts*.", "The credits are held when the run starts."), ("Never more than the *quote*.", "You never pay more than the quote."),
   ("Failed? *Nothing* to pay.", "A failed run costs nothing."), ("Pay for what you *make*.", "Pay for what you make. Never for a failure.")],
  [(HOME, "The price is on the button before anything starts"), (HOME, "60 credits a minute of finished video"), (PRICING, "Held when it starts"),
   (HOME, "never more than the quote"), (HOME, "A failed run costs nothing"), (HOME, "Pay for what you make. Never for a failure.")]),
 ("private", "Uploads stay private. You decide.",
  [("Who *publishes?*", "Who presses publish?"), ("Uploads as *private*.", "Every finished video uploads to YouTube as private."), ("Publish check *first*.", "It passes a publish check first."),
   ("Passed, or *blocked and why*.", "The verdict is on the video's page: passed, or blocked and why."), ("Auto-publish: *off*.", "Auto-publish stays off unless you turn it on."),
   ("You *watch* it.", "You watch it first."), ("*You* decide.", "Going public is your decision.")],
  [(HOME, "Finished videos upload to YouTube as private and pass a publish check first"), (STUDIO, "the verdict is shown on the video’s page: passed, or blocked and why"),
   (HOME, "Auto-publish is off unless you turn it on for a channel"), (STUDIO, "You watch the video"), (STUDIO, "Going public is your decision")]),
 ("storyboard", "Read the plan before anything is made.",
  [("Read the *plan*.", "Read the plan,"), ("Before it's *made*.", "before anything is made."), ("Storyboard *ready*.", "On a channel that asks for it, the run stops at storyboard ready."),
   ("Change any *scene*.", "Edit a scene's narration or visual. Move it, add one, or delete one."), ("The price *updates*.", "Save, and the price updates."),
   ("No? It costs *nothing*.", "Discard it, and nothing is rendered or charged."), ("Yes? *Render*.", "Approve, and it renders.")],
  [(STUDIO, "Read the plan before anything is made."), (STUDIO, "On a channel that asks for it, the run stops after the script and the scene plan and waits for you"),
   (STUDIO, "Edit a scene’s narration or visual description, move scenes, delete one or add one"), (STUDIO, "Save, and the price updates"),
   (STUDIO, "Discard a storyboard and nothing is rendered or charged"), (STUDIO, "Nothing is rendered, and no render is charged, until you approve")]),
 ("free", "100 free credits. No card.",
  [("*Curious?*", "Curious?"), ("*100* free credits.", "One hundred free credits, once, when you sign up."), ("*No* card.", "No card."), ("Just your *email*.", "You sign up with your email."),
   ("About *1 minute* of video.", "That covers about one minute of finished video."), ("Pay only when *you* choose.", "You pay only when you pick a plan or a pack."), ("Start *tonight*.", "Start tonight.")],
  [(HOME, "100 free credits, once, when you sign up. No card."), (PRICING, "Your 100 free credits cover about 1 min of finished video at this rate"),
   (PRICING, "Email sign-up, no card. You pay only when you pick a plan or a pack.")]),
 ("channel", "Every channel keeps its own voice.",
  [("*Your* channel.", "Your channel."), ("Its own *language*.", "Its own language,"), ("Its own *voice*.", "its own voice,"), ("Its own *style*.", "its own visual style,"),
   ("Its own *schedule*.", "and its own schedule."), ("Never *mixed*.", "Set per channel, and never leaking into another."), ("Uzbek. Russian. *English.*", "In Uzbek, Russian or English.")],
  [(YT, "Language, voice, visual style and schedule are set per channel and never leak into another"),
   (STUDIO, "The app is in Uzbek, Russian and English. Each channel is set to one of the three for its videos")]),
 ("studio", "One picture, one clip, one voice-over. Priced on the button.",
  [("Just *one* piece?", "Need just one piece?"), ("A *picture*.", "A picture,"), ("A *clip*.", "a clip,"), ("A *voice-over*.", "or a voice-over."),
   ("Price on the *button*.", "Each one shows its price on its button."), ("Failed? Credits *return*.", "If a generation fails, its credits return on their own."),
   ("Edit it *free*.", "Then edit it in the editor, for no credits.")],
  [(HOME, "Need just one piece? The Studio makes it."), (CS, "Pictures, clips and voice‑overs, priced on the button."),
   (CS, "It will not keep the credits of a generation that failed; they return on their own"), (STUDIO, "Editing and exporting use no credits")]),
 ("editor", "Edit for zero credits.",
  [("Your *cut*.", "Your cut."), ("Trim. *Split.*", "Trim and split."), ("Text on *screen*.", "Put text on screen."), ("Music and *sound*.", "Add music and sound."),
   ("0.5x to *2x*.", "Change the speed, from half to double."), ("9:16. 16:9. *1:1.*", "Vertical, wide or square."), ("*Zero* credits.", "Editing and exporting use no credits.")],
  [(STUDIO, "Split a clip at the playhead"), (STUDIO, "Add text"), (STUDIO, "Add music or effects from your library"), (STUDIO, "Play a clip at 0.5×, 0.75×, 1.25×, 1.5× or 2×"),
   (STUDIO, "Vertical 9:16, wide 16:9 or square 1:1"), (STUDIO, "Editing and exporting use no credits")]),
 ("noswap", "Your voice, or no video.",
  [("*Your* voice.", "You chose the voice."), ("*Unavailable?*", "What if it is unavailable?"), ("No *swap*.", "Nightshift will not swap in a different voice or model."),
   ("The run *stops*.", "The run stops,"), ("...and says *why*.", "and says why."), ("Credits *come back*.", "If a run fails, the credits come back on their own."), ("Your voice, or *no video*.", "Your voice, or no video.")],
  [(YT, "It will not swap in a different voice or model when the chosen one is unavailable — the run stops and says why"), (HOME, "If a run fails, the credits come back on their own")]),
 ("data", "Your Google data, only for your channel.",
  [("Your *data*.", "Your Google data."), ("Only for *your* channel.", "Used only to upload to the channel you connect,"), ("Your *numbers*, for you.", "and to show you its analytics."),
   ("*Encrypted.*", "Access tokens are encrypted,"), ("Never in the *browser*.", "and never reach the browser."), ("*Never* for ads.", "Never used for advertising."), ("Revoke *any time*.", "Revoke access any time.")],
  [(HOME, "Nightshift uses your Google account only to upload videos to the YouTube channel you connect and to read that channel's data and analytics for your dashboard"),
   (HOME, "Access tokens are encrypted and never reach the browser"), (HOME, "the data is never used for advertising"), (HOME, "you can revoke access at any time")]),
]
# Second spoken line per beat, same order as ANGLES. With 8 s clips this takes each ad to about a minute.
EXTRA = {
 "topic": ["Type a line, or let your channel pick its next topic.", "One run, from topic to finished video.", "Made for the length you choose.",
           "In your channel's voice, in its language.", "Nothing goes out without you.", "And it passes a publish check first.", "We make the video. You press publish."],
 "price": ["No guessing, no surprises.", "You see it before you press start.", "A five minute video is quoted at three hundred credits.",
           "Set aside, so it is not spent on anything else.", "You are charged for what it actually used.", "Every held credit comes back on its own.",
           "Every hold, charge and return is in your credit history."],
 "private": ["You do.", "Only you, and the people you share it with, can watch it.", "Every video, every time.", "So you know where it stands.",
             "And so does Publish when approved. Both are switches per channel.", "Then you record your decision in the app.", "Nothing goes public until you say so."],
 "storyboard": ["The script and the scene plan come first.", "Nothing is rendered yet.", "It stops, and waits for you.", "Your words. Your shots.",
                "You see the new price before you go on.", "Saying no costs nothing.", "No render is charged until you approve."],
 "free": ["Try Nightshift free.", "Welcome credits, once.", "Nothing to enter but your email.", "That is all it takes.", "At sixty credits a minute.",
          "Plans and credit packs are your choice.", "Your first video starts with one topic."],
 "channel": ["Faceless or not.", "Uzbek, Russian or English.", "The narrator speaks as your channel.", "Your channel's look, in every video.",
             "When it posts is set per channel.", "Nothing leaks from one channel into another.", "The app speaks all three, too."],
 "studio": ["Not a whole video.", "From a description, in the shape you need.", "From text, or from a picture you made.", "Text to speech, in your workspace's voices.",
            "The press shows the price.", "Nothing to ask for.", "Trim, split, add text and music."],
 "editor": ["In the editor, it is yours.", "At the playhead, one frame at a time.", "At the top, the middle or the bottom.", "Music lowered under speech.",
            "Point five to two times.", "Vertical suits Shorts and Reels.", "Exports land in your library."],
 "noswap": ["For a reason.", "It happens.", "No quiet substitute.", "Nothing goes out in a voice you did not choose.", "So you know what to fix.",
            "You do not need to ask.", "That is the promise."],
 "data": ["Here is what Nightshift does with it.", "And nowhere else.", "Shown only to you.", "Locked away.", "They stay out of your browser.",
          "Not for advertising.", "In your Google account."],
}
EXTRA_FACTS = {
 "topic": [(HOME, "Type a line, or let your channel pick its next topic from its niche"), (YT, "Script, narration, visuals, captions and the edit, made for the length you choose"),
           (HOME, "Narrator Your channel’s voice, in its language."), (HOME, "We make the video.")],
 "price": [(PRICING, "so it is not spent on anything else meanwhile"), (PRICING, "you are charged for the resources it actually used"),
           (PRICING, "every hold, charge and return in your organization's credit history"), (PRICING, "5 min"), (PRICING, "300 credits")],
 "private": [(STUDIO, "which only you and the people you share it with can watch"), (STUDIO, "record your decision in the app"),
             (STUDIO, "Auto-publish and “Publish when approved” are switches per channel, and both stay off until you turn them on")],
 "storyboard": [(STUDIO, "Saying no costs nothing"), (STUDIO, "until you approve")],
 "free": [(HOME, "Your first video starts with one topic."), (HOME, "60 credits a minute of finished video")],
 "channel": [(YT, "often faceless ones"), (HOME, "Narrator Your channel’s voice"), (HOME, "Visuals In your channel’s look.")],
 "studio": [(HOME, "Image From a description, in the shape you need"), (CS, "Short clips from text, or animate a picture you made or uploaded"),
            (CS, "Text to speech in the voices your workspace has"), (CS, "the press shows the price"), (HOME, "Editor Trim, split, add text and music")],
 "editor": [(STUDIO, "one frame at a time"), (STUDIO, "whether it sits at the top, middle or bottom"), (STUDIO, "have music lowered"),
            (STUDIO, "Vertical suits Shorts, Reels and TikTok"), (CS, "Exports land in your library and cost no credits")],
 "noswap": [], "data": [(STUDIO, "revoke access in your Google account, at any time")],
}
CLIP_SECONDS = 8   # unlimited covers 8 s at 720p; one 8 s take per beat gives two lines room to breathe


X_TAIL = {"topic": "What topic would you give it?", "price": "What would you make first?", "private": "Would you let a bot publish for you?",
          "storyboard": "Would you read the plan first?", "free": "What would you make with 100 credits?", "channel": "What is your channel about?",
          "studio": "Picture, clip or voice: which first?", "editor": "Vertical or wide?", "noswap": "Which voice is your channel?", "data": "Questions? Ask below."}


def x_text(world, angle_slug, title):
    t = f"{title} A {world} channel's night shift, made with Nightshift. {X_TAIL[angle_slug]} nightshift-ai.studio"
    return t


def combos(n):
    """Every (world, angle) pair once, worlds and angles both rotating so neighbouring days never repeat either."""
    out, seen = [], set()
    i = 0
    while len(out) < n:
        w, a = i % len(WORLDS), (i + i // len(WORLDS)) % len(ANGLES)
        if (w, a) not in seen: seen.add((w, a)); out.append((w, a))
        i += 1
    return out


def main(n_ads=60):
    pp = os.path.join(ROOT, "queue", "plan.json"); d = json.load(open(pp)); old = {e["id"]: e for e in d["episodes"]}
    first = 49; added = 0
    for k, (wi, ai) in enumerate(combos(n_ads)):
        wname, bible, shots = WORLDS[wi]; aslug, title, beats, facts = ANGLES[ai]
        eid = f"ep{first + k:03d}-{wname}-{aslug}"
        if eid in old and (old[eid]["render"] != "todo" or old[eid].get("published")): continue
        scenes = [{"type": "shot", "hold": 3.2, "big": big, "sentences": [line, EXTRA[aslug][j]], "broll": f"broll/{eid}-{j}.mp4"} for j, (big, line) in enumerate(beats)]
        scenes.append({"type": "end", "hold": 2.5, "broll": f"broll/{eid}-7.mp4", "big": "Type your topic. See the plan.",
                       "sentences": ["Type your own topic at nightshift-ai dot studio, and see the plan.", "One hundred free credits. No card."]})
        pal = PALS[(first + k) % len(PALS)]
        json.dump({"id": eid, "palette": pal, "title": title, "format": "cine", "scenes": scenes}, open(os.path.join(ROOT, "episodes", eid + ".json"), "w"), indent=1)
        prev = {c["key"]: c for c in old.get(eid, {}).get("clips", [])}
        clips = [dict(key=f"{eid}-{j}", scene=j, duration=CLIP_SECONDS, prompt=bible + " SHOT: " + shots[j].replace("0-5s", "0-8s").replace("3-5s", "5-8s").replace("4-5s", "6-8s").replace("2-4s", "3-6s").replace("0-3s", "0-5s").replace("0-2s", "0-3s") + " " + FILM.replace("5-second", "8-second"),
                      status=prev.get(f"{eid}-{j}", {}).get("status", "todo"), job_id=prev.get(f"{eid}-{j}", {}).get("job_id"),
                      url=prev.get(f"{eid}-{j}", {}).get("url")) for j in range(8)]
        xt = x_text(wname.replace("storyteller", "folk tales").replace("gamer", "tech"), aslug, title)
        assert len(xt) < 280, (eid, len(xt))
        e = dict(id=eid, day=None, title=title, palette=pal, format="cine", x_text=xt, facts=[{"page": p, "quote": q} for p, q in facts + EXTRA_FACTS[aslug] + END_FACTS],
                 clips=clips, render="todo", asset=None, published=None)
        if eid in old: d["episodes"][[x["id"] for x in d["episodes"]].index(eid)] = e
        else: d["episodes"].append(e); added += 1
    json.dump(d, open(pp, "w"), indent=1)
    print("added", added, "ads; total clips now", sum(len(e["clips"]) for e in d["episodes"]))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 60)
