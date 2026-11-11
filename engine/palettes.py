"""Colour palettes for the daily promo. Each episode picks one, so the feed never looks like the same template twice.

bg0/bg1: vertical background gradient. blobs: the three glowing colours that drift behind the scene.
accent/accent2: UI highlights. owl_*: Nox's colours. key: semitone shift of the music so days also sound different.
"""
PALETTES = {
    "sunrise": dict(bg0=(16, 10, 40), bg1=(52, 14, 70), blobs=[(255, 94, 98), (255, 170, 64), (120, 70, 255)],
                    accent=(255, 196, 64), accent2=(255, 94, 98), good=(120, 255, 190),
                    owl_body=(250, 238, 222), owl_belly=(255, 250, 242), owl_wing=(238, 214, 188), owl_line=(110, 72, 60), beak=(255, 150, 60), key=0, bpm=100),
    "aurora": dict(bg0=(4, 18, 30), bg1=(10, 34, 56), blobs=[(40, 255, 190), (60, 140, 255), (170, 90, 255)],
                   accent=(90, 255, 205), accent2=(170, 110, 255), good=(150, 255, 150),
                   owl_body=(236, 244, 252), owl_belly=(248, 252, 255), owl_wing=(205, 222, 240), owl_line=(40, 70, 110), beak=(255, 190, 70), key=3, bpm=104),
    "candy": dict(bg0=(24, 8, 48), bg1=(58, 12, 84), blobs=[(255, 70, 190), (60, 210, 255), (255, 220, 90)],
                  accent=(255, 110, 210), accent2=(80, 220, 255), good=(150, 255, 190),
                  owl_body=(255, 240, 248), owl_belly=(255, 252, 255), owl_wing=(246, 214, 236), owl_line=(120, 40, 100), beak=(255, 170, 60), key=5, bpm=108),
    "ocean": dict(bg0=(4, 14, 44), bg1=(8, 40, 92), blobs=[(40, 170, 255), (30, 240, 220), (255, 110, 150)],
                  accent=(70, 210, 255), accent2=(255, 120, 150), good=(120, 255, 200),
                  owl_body=(238, 246, 255), owl_belly=(250, 253, 255), owl_wing=(208, 226, 246), owl_line=(30, 66, 120), beak=(255, 180, 70), key=-2, bpm=96),
    "forest": dict(bg0=(6, 24, 20), bg1=(14, 48, 36), blobs=[(120, 255, 90), (255, 190, 60), (40, 200, 160)],
                   accent=(190, 255, 90), accent2=(255, 170, 60), good=(140, 255, 160),
                   owl_body=(248, 242, 224), owl_belly=(255, 252, 240), owl_wing=(228, 218, 186), owl_line=(70, 80, 40), beak=(255, 160, 50), key=7, bpm=100),
    "ember": dict(bg0=(22, 6, 8), bg1=(58, 14, 14), blobs=[(255, 90, 40), (255, 190, 50), (200, 40, 120)],
                  accent=(255, 170, 50), accent2=(255, 80, 90), good=(150, 255, 170),
                  owl_body=(252, 238, 226), owl_belly=(255, 250, 244), owl_wing=(240, 212, 190), owl_line=(120, 50, 40), beak=(255, 140, 40), key=-5, bpm=110),
}
