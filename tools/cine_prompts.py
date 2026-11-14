"""Director-level prompts for the cinematic queue (owner, 2026-11-13: "a place that can shoot film was given prompts
too plain for a cartoon"). Each ad has a BIBLE (cast, wardrobe, set, light plan, film look) that is repeated in every
shot, and each shot is a full camera brief: framing and lens, camera move, what happens second by second within the
5 s, and the light. One continuous 5-second take per prompt; the edit happens in our engine.
"""

FILM = ("Shot on ARRI Alexa 35 with Cooke anamorphic lenses, 2.39 feel inside a 16:9 frame, natural film grain, soft halation on "
        "highlights, real practical light sources, photoreal, high-end commercial cinematography, one continuous 5-second take, "
        "no cuts inside the shot, no on-screen text, no logos.")

BIBLE = {
 "nightshift": "CAST: Mira, 27, Central Asian features, short black bob with a few loose strands, small silver hoop earrings, oversized heather-grey hoodie with sleeves pushed up. SET: her small 9th-floor studio apartment, a wooden desk against a floor-to-ceiling window, a silver laptop and a matte black mug, a brass desk lamp, a low bed with white linen, a city skyline of glass towers outside. LIGHT PLAN: night = cool 5600K moonlight and city spill from the window, laptop glow as key, warm 2700K lamp as practical; dawn = low golden sun raking through the same window. PALETTE: deep teal shadows, magenta city bokeh, amber practicals.",
 "price": "CAST: Daniyar, 30, curly dark hair, short beard, navy cable-knit sweater, reading glasses pushed up. SET: a calm home office at night, walnut desk, one brass banker's lamp, a small clear glass jar, a stack of old gold coins, a window with rain. LIGHT PLAN: single warm 2700K lamp as key from screen left, cool rain light from the window as rim, deep falloff into black. PALETTE: amber, walnut brown, steel blue, gold highlights.",
 "silkroad": "WORLD: the Silk Road at its height, a caravan of Bactrian camels with woven saddle blankets, a traveller in a sand-coloured hooded cloak with an indigo sash, the city of Samarkand with the turquoise-tiled domes and mosaic portals of the Registan. LIGHT PLAN: golden hour turning to dusk, sun low and behind, long shadows, warm dust hanging in the air, first lanterns igniting. PALETTE: saffron gold, turquoise, terracotta, deep indigo sky.",
 "airs": "WORLD: an empty 19th-century theatre at night, red velvet curtain with gold fringe, dust drifting in a single follow spot, rows of worn red seats. CAST: Lola, 25, long dark braid, black turtleneck, sitting alone in row five; a white snowy owl perched on the edge of the balcony. LIGHT PLAN: one hard tungsten follow spot, everything else falling to black, gentle haze. PALETTE: crimson, gold, black, warm white.",
 "studio": "SET: a creator's studio at night on the shore of a still lake, long oak work table, floor-to-ceiling window over the water, tools and paper prints on the table. HANDS: the same pair of hands throughout, slim, a thin silver ring on the right index finger, cream knit sleeve cuffs. LIGHT PLAN: blue hour outside, warm 3000K practical lamps inside, reflections on the glass. PALETTE: dusk blue, peach, cream, soft violet.",
 "languages": "CAST: Timur, 28, short dark hair, light stubble, olive wool coat, worn brown leather backpack; he is a traveller walking through three cities in one night. LIGHT PLAN: each city lit by its own practicals (lanterns, street lamps, neon) but one shared grade. PALETTE: warm amber practicals against deep blue night, wet reflections.",
 "channels": "SET: one tall modernist apartment block at night with a grid of identical windows, seen from across a quiet street; inside one corner apartment, the operator. CAST: Aziza, 32, red wool scarf, hair in a low bun, calm and focused; a white owl on the roof parapet. LIGHT PLAN: windows glow warm 3200K, street in cool sodium and moonlight, light haze. PALETTE: warm window amber in a blue-black grid.",
 "noswap": "WORLD: a small black-box theatre, one singer: tall silhouette in a long charcoal coat, short hair, always seen from behind or in profile, never a clear face; one hard spotlight; a narrow backstage corridor with a steel door. LIGHT PLAN: single hard spot, haze, deep shadows, one red exit light. PALETTE: black, cold white, one accent of red.",
 "free": "CAST: Nodira, 24, curly shoulder-length hair, mustard-yellow cardigan over a white tee, warm and curious. SET: a cozy attic room with a round window, warm string lights, a wooden desk, a small wrapped gift box with a cream ribbon. LIGHT PLAN: warm 2700K string lights and desk lamp, blue night through the round window; dawn = pink-gold light through the same window. PALETTE: honey, cream, rose, night blue.",
 "storyboard": "SET: a film director's office at night, a cork wall of hand-drawn storyboard panels, a wooden table, a vintage clapperboard, a 16mm projector. CAST: Sardor, 34, director, flat cap, round glasses, rolled-up denim shirt sleeves. LIGHT PLAN: warm tungsten desk lamp key, cool window fill, projector beam in haze. PALETTE: tungsten amber, ink black, paper cream, cyan beam.",
 "editor": "SET: a night editing room, wooden desk, analogue film reels and a splicer, a turntable with a vinyl record, a few neon tubes on the wall. HANDS: the same pair of hands throughout, black leather watch strap, dark sweater cuffs. LIGHT PLAN: neon magenta and cyan rims, warm desk lamp key, deep shadows. PALETTE: magenta, cyan, warm amber, black.",
 "styles": "SET: a small art studio at night, white shelves with three identical white ceramic vases, a paint-stained work table, a clay figure on a pottery wheel, a desk lamp. HANDS: the same pair of hands throughout, paint on the fingertips, rolled linen sleeves. LIGHT PLAN: soft window-like key from the left, coloured accent lights on the vases, gentle falloff. PALETTE: off-white, terracotta, cobalt, saffron.",
 "data": "SET: a quiet private office at night, a dark walnut desk, a heavy steel safe with a brass dial, a tall window on a sleeping city. HANDS: the same pair of hands throughout, crisp white shirt cuffs, a simple steel watch. LIGHT PLAN: cool moonlight from the window as key, one warm green-shaded banker's lamp as practical. PALETTE: steel blue, deep green, brass, black.",
}

# 7 shots per ad, in story order. Each: framing + lens, camera move, beats inside the 5 s, light/detail.
SHOTS = {
 "nightshift": [
  "Extreme close-up on Mira's eyes at 3 a.m., 100mm macro, locked off with a barely perceptible push-in. 0-2s: she stares, the laptop's cold light flickering on her irises; 2-4s: one slow, heavy blink; 4-5s: steam from the black mug drifts through the foreground out of focus. Cold screen key, magenta city bokeh behind.",
  "Medium close-up of Mira at the desk, 50mm, slow dolly-in from the side. 0-2s: she exhales and pushes her hair back; 2-4s: she gently closes the laptop lid and the cold glow drains from her face; 4-5s: she reaches up and clicks off the brass lamp, the room falls to moonlit blue.",
  "Wide shot from behind Mira's silhouette at the dark window, 32mm, slow push-in past her shoulder toward the glass. 0-5s: across the skyline, windows in the towers switch on one after another in a steady rhythm, like a sequence being assembled, their reflections sliding across the glass. Moonlit room, warm windows outside.",
  "Aerial tracking shot beside a white snowy owl gliding over the same glass towers at night, 35mm, drone matching its speed. 0-2s: the owl's wings spread, feathers catching window light; 2-5s: it banks gracefully past lit windows, the city sliding underneath. Cool moonlight on white feathers, warm windows below.",
  "Medium shot of Mira asleep on the low bed, 40mm, slow overhead slide. 0-2s: room in deep blue night, she breathes slowly; 2-3s: the phone on the nightstand glows softly once, warm white; 3-5s: she stirs, half-smiles in her sleep and turns over. Calm, safe mood.",
  "Wide shot of the same apartment at sunrise, 28mm, slow push-in from the doorway. 0-2s: low golden sun floods through the floor-to-ceiling window; 2-4s: Mira, in the hoodie, stretches by the window holding the black mug, steam glowing gold; 4-5s: she turns toward the desk with a relaxed smile. Warm halation on everything.",
  "Macro close-up of Mira's finger pressing one key on the laptop keyboard in morning light, 100mm macro, slow push. 0-2s: the finger hovers, dust motes in a sunbeam; 2-3s: the key goes down; 3-5s: a soft warm flare blooms from the edge of frame. Warm gold light, shallow focus.",
 ],
 "price": [
  "Close-up of a sealed cream envelope on the walnut desk under the brass lamp, 75mm, very slow push-in. 0-3s: rain shadows crawl across the envelope; 3-5s: Daniyar's hand enters, hesitates and does not open it. Tension, deep shadows.",
  "Medium close-up of Daniyar at the walnut desk, 50mm, slow arc around him. 0-2s: he looks at a small polished brass desk bell glowing in the lamp light; 2-4s: he rests his hand calmly on the desk beside it; 4-5s: a small relaxed nod. Warm lamp key, rain rim light.",   # reworded: the first version was rejected twice as nsfw
  "Close-up of an antique brass hourglass on the desk, 85mm, locked off. 0-5s: fine golden sand pours through the neck in slow motion, each grain catching the lamp light; rain-soaked window bokeh behind.",
  "Top-down close-up of the small clear glass jar on the walnut desk, 65mm, slow lowering crane. 0-5s: Daniyar's fingers place gold coins one by one into the jar, each landing with a gentle bounce, slow motion, warm reflections in the glass.",
  "Low-angle close-up of a line of wooden dominoes on the desk, 40mm, slow dolly along the line. 0-3s: the dominoes topple toward camera; 3-5s: the run stops dead, one domino stays standing. Hard warm side light, long shadows.",
  "Macro shot of the glass jar, 100mm, locked off, reverse slow motion. 0-5s: gold coins float back up and settle into the jar, light dancing through the glass, a magical calm. Warm key, cool rim.",
  "Medium shot of Daniyar leaning back in his chair by the rainy window, 40mm, slow pull-back. 0-3s: he takes off his glasses and smiles; 3-5s: the room feels warm and settled, rain glittering outside. Amber and steel blue.",
 ],
 "silkroad": [
  "Extreme wide aerial over golden dunes, 24mm, slow forward drone glide. 0-5s: a caravan of Bactrian camels walks in a long line along a dune ridge toward a distant city of turquoise domes, long shadows stretching across the sand, dust glowing in backlight.",
  "Aerial of the Registan in Samarkand at golden hour, 35mm, slow orbit around the three madrasa portals. 0-5s: turquoise domes and mosaic portals catch the low sun, tiny figures cross the square, swallows circle. Saffron light, deep indigo sky above.",
  "Gimbal walk through a night bazaar beside the traveller, 32mm, moving forward at walking pace. 0-5s: silk fabrics ripple in the breeze, brass lanterns sway overhead, merchants' hands lift bolts of cloth. Warm lantern key, indigo shadows.",
  "Top-down close-up of the traveller's hands unrolling an old hand-drawn map on a wooden table, 50mm, slow lowering. 0-5s: the map unrolls across the frame, a brass compass slides into place, lantern light flickers. No legible writing.",
  "Medium shot in a dusty courtyard at dusk, 40mm, slow lateral slider. 0-5s: an antique wooden cine camera on a tripod turns toward a mosaic portal as the traveller steps into frame and looks up. Warm dust, long shadows.",
  "Close-up of turquoise mosaic tiles on a dome, 85mm, slow tilt up. 0-5s: the last sun slides off the tiles, the colour shifts from gold to deep blue, one warm highlight remains. High contrast, rich texture.",
  "Wide shot from behind the traveller reaching the great gate of the city at nightfall, 28mm, slow push past his shoulder. 0-5s: the gate opens onto a glowing street of lanterns, warm light spills over his cloak. Awe, arrival.",
 ],
 "airs": [
  "Wide frontal shot of the closed red velvet curtain, 35mm, very slow push-in. 0-5s: dust drifts through one hard follow spot on the curtain, the gold fringe trembles slightly. Everything else falls to black.",
  "Extreme close-up of the white owl's face on the balcony edge, 100mm, locked off. 0-2s: its eyes are closed; 2-4s: they open, amber and calm, catching the spot; 4-5s: a slow head turn toward camera.",
  "Medium shot of a single glass display case in the dark theatre aisle, 50mm, slow arc. 0-5s: inside, a small film reel rests on velvet, the case's glass reflecting the spot, a soft hum of light. Precious, protected.",
  "Medium shot of a handheld torch beam sweeping slowly along the rows of red seats, 40mm, handheld but steady. 0-5s: the beam checks seat by seat, then settles on the stage. Careful, deliberate, haze in the beam.",
  "Close-up of Lola in row five watching the stage, 85mm, slow push-in. 0-5s: her face lit softly by the reflected spotlight, she watches attentively, one small thoughtful nod at the end.",
  "Extreme close-up of an old brass toggle switch on the theatre's lighting board, 100mm macro. 0-3s: the switch rests firmly in the down position, dust on the brass; 3-5s: the follow spot's beam passes over it. Still and certain.",
  "Wide frontal shot as the red curtain parts, 28mm, slow push-in. 0-5s: warm stage light floods out over the empty seats and over Lola, who stands up, the owl lifting off the balcony. Release, decision.",
 ],
 "studio": [
  "Wide shot over the still lake at blue hour seen through the studio window, 35mm, slow push toward the glass. 0-5s: a single hot air balloon drifts low over the mirror-like water, its burner flaring warm, reflection doubling it.",
  "Wide shot on the lake at sunset, 50mm, slow lateral pan. 0-5s: a small sailboat glides across the frame, sail lit peach, wake shimmering, the studio's warm windows visible on the shore.",
  "Close-up of a vintage studio microphone on the oak table, 85mm, slow arc. 0-5s: dust floats in a violet rim light, the hands adjust the mic arm gently into place.",
  "Medium shot of a framed painting of a sky on the studio wall, 50mm, slow push-in. 0-5s: a white dove flies out of the painting into the room, feathers catching lamp light, the painted clouds stirring.",
  "Macro of a monarch butterfly on a flower on the oak table, 100mm macro, locked off. 0-5s: the image begins soft and blurred and resolves into razor-sharp detail of wing scales, as if focus is being pulled into perfect clarity.",
  "Close-up on the table, 65mm, slow push. 0-5s: the hands lift a small potted plant up and out of a paper print, leaving a clean cut-out outline in the paper behind it. Soft lamp light.",
  "Top-down of the oak table, 40mm, slow rotation. 0-5s: the hands arrange film strips and printed frames into a neat sequence on a glowing light pad. Satisfying, organised.",
 ],
 "languages": [
  "Wide shot of Timur walking across the illuminated Registan square in Samarkand at night, 28mm, gimbal follow from behind. 0-5s: the madrasa portals glow gold and turquoise, he slows and looks up.",
  "Medium shot of Timur on a snowy boulevard at night, 40mm, slow tracking alongside him. 0-5s: snow falls through warm lamp light, old trees and a tram passing in soft focus.",
  "Medium shot of Timur crossing a rainy city street at night, 35mm, low angle. 0-5s: neon signs (no readable letters) reflect in the wet asphalt, a red bus blurs past, he turns his collar up.",
  "Wide shot from a rooftop, 35mm, slow tilt up. 0-5s: Timur releases three paper lanterns, amber, rose and teal, that rise together into the night sky.",
  "Close-up of Timur speaking into a vintage radio microphone in a small booth, 85mm, slow push-in. 0-5s: warm tungsten light, he smiles mid-sentence, sound panels behind.",
  "Wide shot from the back of a small cinema, 32mm, slow push. 0-5s: silhouetted audience heads, the projector beam glowing through haze, Timur sitting in the middle row.",
  "Wide shot of sunrise over turquoise domes and rooftops, 35mm, slow drone rise. 0-5s: Timur stands on a terrace with his backpack, golden light reaching him.",
 ],
 "channels": [
  "Wide shot of the apartment block at night from across the street, 50mm, very slow push-in. 0-5s: one corner window glows warm, Aziza's silhouette moving inside.",
  "Wide shot of the same block, 35mm, slow pull-back. 0-5s: more and more windows across the grid light up one by one until the whole facade glows.",
  "Close-up of Aziza's hand moving a chess piece on a softly glowing board, 85mm, slow arc. 0-5s: she places the piece with quiet confidence, her red scarf in soft focus.",
  "Aerial of two rivers of light (streams of car lights on two parallel avenues) flowing through the night city without crossing, 24mm, drone moving forward.",
  "Medium shot of Aziza in silhouette at her window, 50mm, slow push past her shoulder. 0-5s: she raises her hand like a conductor and the lights in the building opposite respond in rhythm.",
  "Medium shot of the white owl on the roof parapet of the block, 85mm, slow orbit. 0-5s: it surveys the glowing windows below, calm and watchful.",
  "Wide shot of sunrise over the same rooftops, 28mm, slow drone rise. 0-5s: Aziza steps onto her balcony with a cup of tea, the facade turning gold.",
 ],
 "noswap": [
  "Wide shot from the back of the black-box theatre, 40mm, slow push-in. 0-5s: the singer in the long charcoal coat stands in one hard spotlight, back to camera, haze swirling.",
  "Medium shot, 50mm, locked off. 0-2s: the spotlight flickers twice; 2-5s: it dies, leaving the singer's silhouette lit only by the red exit light, dust still drifting.",
  "Medium shot of the narrow backstage corridor, 32mm, slow push. 0-5s: the steel door at the end closes gently and firmly; nobody else walks through.",
  "Close-up of a red stop light glowing through rain on the street outside the theatre, 85mm, rack focus from raindrops to the light.",
  "Close-up at the foot of the singer's dressing room door, 65mm, low angle. 0-5s: a folded paper note slides under the door into warm lamplight. No legible writing.",
  "Macro shot of gold coins floating back up into a small glass jar in reverse slow motion, 100mm, warm key, red rim from the exit light.",
  "Wide shot from the back of the theatre, 35mm, slow push. 0-5s: the spotlight returns, warm this time; the singer turns slightly into the light, profile only, and lifts their head.",
 ],
 "free": [
  "Medium shot of the attic door, 32mm, slow push-in. 0-5s: the door swings open and warm string-light glow spills into the dark stairwell, Nodira stepping in.",
  "Close-up of the small gift box on the wooden desk, 85mm, slow push. 0-5s: Nodira's hands pull the cream ribbon, the lid lifts and soft golden light pours out over her face.",
  "Close-up of a closed leather wallet on the desk, 65mm, locked off. 0-5s: it stays shut; Nodira's hand slides it aside and out of frame.",
  "Close-up of a small brass hourglass on the desk, 100mm, locked off. 0-5s: the last grains of glowing sand fall through in slow motion.",
  "Medium shot of Nodira typing on a laptop at the desk, 50mm, slow arc behind her shoulder (screen not readable). 0-5s: string lights twinkle, she smiles, round window glowing blue.",
  "Close-up of Nodira's hand hovering between two small glowing glass orbs on the desk, 85mm. 0-5s: she considers, then simply rests her chin on her hand, unhurried.",
  "Wide shot of the attic at dawn, 28mm, slow push toward the round window. 0-5s: pink-gold sunlight pours in, Nodira opens the window and looks out over the rooftops.",
 ],
 "storyboard": [
  "Slow lateral dolly along the cork wall of hand-drawn storyboard panels, 40mm. 0-5s: warm desk light rakes across the sketches (images only, no writing), Sardor's shadow passes over them.",
  "Wide shot of the empty director's chair in the middle of the dark office, 35mm, slow push-in. 0-5s: a single tungsten spot falls on the chair, dust in the beam.",
  "Top-down shot of the wooden table, 50mm. 0-5s: Sardor's hands slide storyboard cards into a new order, remove one, and place a fresh blank card in the sequence.",
  "Close-up of a pencil sketching on a storyboard card, 100mm macro. 0-5s: a quick confident line drawing of a skyline appears under warm light. No writing.",
  "Close-up of the vintage clapperboard, 85mm, slow motion. 0-5s: Sardor's hand snaps it shut, chalk dust bursting into the light. No legible writing.",
  "Medium shot, 50mm. 0-5s: Sardor calmly drops a crumpled card into a wicker bin and leans back, relaxed.",
  "Wide shot as the 16mm projector bursts to life, 28mm, slow push along the beam. 0-5s: the beam cuts through haze and lights up the wall with moving light, Sardor watching.",
 ],
 "editor": [
  "Close-up of two analogue film reels spinning on the editing desk, 65mm, slow arc. 0-5s: neon magenta and cyan rims glint on the metal reels.",
  "Macro of a film splicer cutting a strip of film, 100mm. 0-5s: the blade comes down cleanly, the two ends separate in slow motion.",
  "Wide shot of the dark editing room, 35mm, locked off. 0-5s: neon light trails sweep through the air in smooth arcs, like long-exposure light painting, revealing the desk.",
  "Close-up of a vinyl record on the turntable, 85mm, slow push. 0-5s: the hands lower the needle, the record starts to spin, warm lamp glow on the grooves.",
  "Close-up of a drop of water hitting a glass of water, 100mm macro. 0-3s: extreme slow motion splash crown; 3-5s: it speeds up to real time.",
  "Wide shot, 40mm, locked off. 0-5s: a magenta neon glow and a cyan neon glow slowly blend into one another through haze on the wall.",
  "Medium shot of the wall, 35mm, slow lateral dolly. 0-5s: three empty picture frames, one tall, one wide, one square, light up one after another.",
 ],
 "styles": [
  "Medium shot of three identical white vases on the shelf, 50mm, slow lateral dolly. 0-5s: each vase is lit by a different coloured light, cobalt, saffron, terracotta, as the camera passes.",
  "Close-up of a palette on the work table, 85mm, slow push. 0-5s: the paint-stained fingers mix saffron into cobalt with a palette knife, colours swirling.",
  "Top-down shot of the work table, 40mm, slow rotation. 0-5s: the hands lay out a neat grid of twelve printed photographs of the same vase in different styles.",
  "Close-up of a small clay figure turning on the pottery wheel, 65mm, slow orbit. 0-5s: the hands smooth its shoulders, the character's simple face gaining form.",
  "Close-up of a clear glass perfume bottle without any label on a turntable, 85mm, locked off. 0-5s: it rotates slowly, studio light flowing over the glass.",
  "Close-up of a short stack of old gold coins on the table, 100mm, locked off. 0-5s: they stay perfectly still while the lamp light shifts around them.",
  "Wide shot of the studio wall, 35mm, slow lateral dolly. 0-5s: a series of artworks in one consistent style, cobalt and saffron, the same character repeated in each.",
 ],
 "data": [
  "Close-up of a brass padlock resting on the walnut desk, 85mm, slow orbit. 0-5s: moonlight glints on the brass, the green lamp glowing behind.",
  "Macro of a key sliding smoothly into a brass lock, 100mm. 0-5s: it turns once with a satisfying click, light catching the teeth.",
  "Wide shot from the window over the sleeping city, 35mm, slow push. 0-5s: thin streams of light rise from the streets like a gently growing line chart.",
  "Medium shot of the heavy steel safe, 50mm, locked off. 0-5s: its door swings closed and the brass dial spins and stops.",
  "Close-up, 65mm. 0-5s: the hands place a sealed envelope inside the safe and close the inner drawer.",
  "Wide shot of rooftop billboards over the night city, 28mm, slow pan. 0-5s: the billboards (blank, no letters) switch off one by one, leaving only moonlight.",
  "Macro of the hands turning the key back and pulling it out of the lock, 100mm. 0-5s: calm, deliberate, the brass catching the green lamp.",
 ],
}

# The last shot of each ad (owner, 2026-11-14: "it starts cinematic and ends as the old plain card"). The call to action
# is laid over this footage in clean type, so every end shot keeps calm negative space in the upper-middle of the frame.
END = {
 "nightshift": "Wide shot of Mira's apartment in full morning light, 28mm, slow pull-back from the window. 0-5s: she sits at the desk with the black mug, laptop open (screen not visible), the glass towers glowing gold outside; soft open sky fills the upper half of the frame. Hopeful, warm.",
 "price": "Wide shot of Daniyar's home office as the rain stops, 32mm, slow pull-back. 0-5s: he stands at the window with a cup of tea, the glass jar of gold coins glowing on the desk, clouds parting over the city; open dark sky in the upper half. Calm, settled.",
 "silkroad": "Extreme wide aerial at blue hour, 24mm, slow rise. 0-5s: the caravan rests outside the walls of Samarkand, lanterns glowing along the walls, the turquoise domes lit, a vast deep-indigo sky with the first stars filling the upper half. Epic and serene.",
 "airs": "Wide shot from the stage looking out at the theatre, 24mm, slow push-in. 0-5s: warm stage light washes over the empty red seats, Lola stands in row five smiling, the white owl glides across the balcony; dark ornate ceiling fills the upper half. Triumphant, quiet.",
 "studio": "Wide shot of the lake studio at night from the water, 35mm, slow drift. 0-5s: the studio's tall windows glow warm, the hot air balloon drifts high above, reflections doubling everything on the still lake; open night sky in the upper half. Dreamy.",
 "languages": "Extreme wide aerial at sunrise over Samarkand's domes, 24mm, slow forward glide. 0-5s: Timur stands small on a terrace, golden light spilling across turquoise tiles, three paper lanterns still drifting high in a soft pink sky that fills the upper half. Warm, open.",
 "channels": "Wide shot of the apartment block at dawn from across the street, 35mm, slow rise. 0-5s: every window glows gold in the first sunlight, Aziza on her balcony, the white owl lifting off the roof into a pale sky that fills the upper half. Confident.",
 "noswap": "Wide shot from the back of the theatre, 28mm, slow push-in. 0-5s: the singer stands in a warm full spotlight, silhouette from behind, arms slightly open, haze glowing; deep black above them in the upper half. Strong, resolved.",
 "free": "Wide shot of the attic at sunrise, 28mm, slow pull-back. 0-5s: Nodira sits by the open round window with the laptop on her knees (screen not visible), pink-gold light, string lights still glowing; soft open sky through the window fills the upper half. Fresh start.",
 "storyboard": "Wide shot of the director's office, 28mm, slow push-in. 0-5s: the 16mm projector throws a big warm moving light onto the wall above Sardor, who leans back in his chair watching; the bright projected wall fills the upper half. Satisfied.",
 "editor": "Wide shot of the editing room, 28mm, slow pull-back. 0-5s: neon magenta and cyan glow, reels spinning, the vinyl turning, the hands lean back from the desk; dark wall with soft neon haze in the upper half. Cool, finished.",
 "styles": "Wide shot of the art studio, 28mm, slow pull-back. 0-5s: the finished artworks in one consistent cobalt-and-saffron style line the walls, the three vases glow in their colours; calm empty wall space fills the upper half. Proud.",
 "data": "Wide shot of the private office from behind the desk, 28mm, slow push toward the window. 0-5s: the safe closed, the green lamp glowing, the sleeping city calm under moonlight; wide night sky in the upper half. Safe, quiet.",
}
