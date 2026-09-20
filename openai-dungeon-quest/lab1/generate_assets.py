"""
Asset generator for Dungeon Quest.
Run once to create all sprites and backgrounds in static/assets/.

  python generate_assets.py

Requires Pillow (already installed in the python-ai container).
"""
from PIL import Image, ImageDraw, ImageFilter
import os, math, random

BACKGROUNDS_DIR = "static/assets/backgrounds"
CHARACTERS_DIR  = "static/assets/characters"
UI_DIR          = "static/assets/ui"

for d in [BACKGROUNDS_DIR, CHARACTERS_DIR, UI_DIR]:
    os.makedirs(d, exist_ok=True)

# ─── Sprite helpers (16×16 grid, each cell = 8×8 px → 128×128 image) ──────────

P = 8   # pixels per grid cell
G = 16  # grid size

# Color palette
C = {
    '.': None,
    'K': (20,  20,  20 ),   # outline
    'W': (255, 255, 255),   # white
    'S': (245, 195, 145),   # skin
    'd': (200, 148, 98 ),   # dark skin
    'c': (155, 105, 65 ),   # shadow skin
    'H': (55,  35,  18 ),   # dark hair
    'h': (90,  58,  28 ),   # brown
    'R': (185, 35,  35 ),   # red
    'r': (235, 85,  85 ),   # light red
    'B': (48,  88,  190),   # armor blue
    'b': (88,  148, 228),   # light blue
    'G': (35,  120, 52 ),   # dark green
    'g': (62,  162, 82 ),   # green
    'e': (122, 202, 122),   # light green
    'Y': (255, 205, 10 ),   # gold
    'y': (255, 245, 122),   # light gold
    'P': (122, 35,  182),   # purple
    'p': (172, 82,  222),   # light purple
    'T': (132, 98,  48 ),   # dark brown / leather
    't': (182, 152, 88 ),   # tan
    'N': (45,  45,  45 ),   # dark gray
    'n': (78,  78,  78 ),   # medium dark gray
    'M': (122, 122, 122),   # medium gray
    'L': (182, 182, 182),   # light gray
    'I': (222, 222, 222),   # near-white
    'A': (182, 142, 52 ),   # armor gold
    'a': (222, 188, 78 ),   # light armor gold
    'O': (202, 102, 22 ),   # orange
    'o': (242, 162, 62 ),   # light orange
    'X': (82,  12,  12 ),   # very dark red
    'Z': (12,  12,  82 ),   # very dark blue
    'E': (62,  202, 122),   # emerald
    'F': (255, 132, 22 ),   # flame orange
    'f': (255, 222, 62 ),   # flame yellow
    'q': (78,  48,  118),   # dark purple
    'v': (162, 162, 162),   # silver
    'u': (228, 218, 198),   # parchment
    's': (150, 115, 70 ),   # apron leather
    'w': (180, 220, 255),   # icy blue
    'm': (120, 200, 220),   # cyan glow
    'j': (80,  130, 40 ),   # sickly green
}

def sprite_from_grid(rows):
    """Render a list of 16 strings (each 16 chars) into a 128×128 RGBA PNG."""
    img  = Image.new("RGBA", (G * P, G * P), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            col = C.get(ch)
            if col:
                draw.rectangle([x*P, y*P, x*P+P-1, y*P+P-1], fill=(*col, 255))
    return img

# ─── Character sprite grids ────────────────────────────────────────────────────

HERO = [
    "................",
    "....KLLLLLK.....",
    "...KILLbbLIK....",
    "...KInnnnnnK....",
    "....KSSSSdSK....",
    ".....SSdSSS.....",
    "....KBBBBBBK....",
    "...KBbBBBBbBK...",
    "..KBBBBBBBBBbK..",
    "..KBBtttttBBBK..",
    "..SBBBBBBBBBBS..",
    "..SBBBBBBBBBBS..",
    "...KBBBKKBBBnK..",
    "...KBBBK.nBBK...",
    "....KKKnnKKK....",
    "................",
]

INNKEEPER = [
    "................",
    ".....KHHHHK.....",
    "....KHHHHHhK....",
    "....KSSSSSdK....",
    ".....KSSdSK.....",
    "....KSSSSSSk....",
    "...KuuRRRRuuK...",
    "..KuuRRRRRRuuK..",
    "..KuuRRRRRRuuK..",
    "..KuRRRRRRRRuK..",
    "..KuuRRRRRRuuK..",
    "..KuuRuuuRuuuK..",
    "...KuRRuuRRuK...",
    "...KuRRuuRRuK...",
    "....KKKuuKKK....",
    "................",
]

GOBLIN = [
    "................",
    ".....KoooK......",
    "....KooYooK.....",
    "...KgggggggK....",
    "...KgegggeGK....",
    "....KgggggK.....",
    "...KTgggggTK....",
    "..KTTgggggTTK...",
    "..KTTTgggTTTK...",
    "..KTtTtttTtTK...",
    "..KTTTgggTTTK...",
    "...KgTgggTgK....",
    "...KggKKKggK....",
    "...KggK.KggK....",
    "....KKK.KKK.....",
    "................",
]

WIZARD = [
    "....KpppppK.....",
    "...KppPpppPK....",
    "...KpPpppPpK....",
    "....KpYpYpK.....",
    ".....KSSSdK.....",
    "....KSSSSdnK....",
    "...KPPPPPPPpK...",
    "..KPpPPPPPpPPK..",
    "..KPPPPPPPPPpK..",
    "..KPPqqqqqPPPK..",
    ".KPPPqPqPqPPPPK.",
    ".KPPPPqPqPPPPPK.",
    "...KPPPPPPPpK...",
    "A..KPPPpPPK..A..",
    "AA..KKPPPKK..A..",
    ".....KKKK.......",
]

SKELETON = [
    "....KWWWWWK.....",
    "...KWIWWWIwK....",
    "...KWnnnnWnK....",
    "....KWWnWWK.....",
    ".....KWWWK......",
    "....KvvvvvK.....",
    "...KvvNvNvvK....",
    "...KvvvvvvvK....",
    "..KvvvNNNvvvK...",
    "...KvNvvvNvK....",
    "..VKvvvvvvvKV...",
    "..VKvNvvvNvKV...",
    "...KvvKKvvvK....",
    "...KvvK.vvK.....",
    "....KKK.KK......",
    "................",
]

TROLL = [
    "................",
    "...KgggggggK....",
    "..KGgGggGggGK...",
    "..KGgggggggGK...",
    "..KGgNggNggGK...",
    "...KGggggggK....",
    "..KGGGgggGGGK...",
    ".KGGGGgggGGGGK..",
    ".KGGGGGgGGGGGK..",
    ".KGGGGGgGGGGGK..",
    ".KGGGtttGGGGGK..",
    ".KGGGGGGGGGGgK..",
    "..KGGGgKKgGGK...",
    "..KGGGK.KgGGK...",
    "...KKKKnKKKK....",
    "................",
]

DRAGON = [
    "....KqqqqqqK....",
    "...KqPqqqPqPK...",
    "...KqqqrrqqqK...",
    "...KqNqrrqNqK...",
    "....KqqrrqqK....",
    "..PK.KqPPqK.KP..",
    "..pKKKqqqKKKp...",
    ".KppppqqqqqpppK.",
    "KpppppqqPqppppK.",
    "KpppppqPpqpqppK.",
    ".KpppppPpppppK..",
    "..KpppppppppK...",
    "...KppPpPppK....",
    "....KpppppK.....",
    ".....KpqpK......",
    "......KKK.......",
]

# ─── NEW NPC sprites ──────────────────────────────────────────────────────────

TOWN_CRIER = [
    "................",
    "....KBBBBBBBK...",
    "...KBbBBBBBbK...",
    "....KBBBBBBBK...",
    ".....KSSSSdK....",
    "....KSSSSSSK....",
    "...KRRRRRRRRK...",
    "..KRRYRRRRYRRK..",
    "..KRuRuuuuRuRK..",
    "..KRuRuuuuRuRK..",
    "..KRuRuuuuRuRK..",
    "..KRRRRRRRRRRK..",
    "..KRYRRRRRRYRK..",
    "...KRRRKKRRRK...",
    "...KKKK.KKKK....",
    "................",
]

BLACKSMITH = [
    "................",
    ".....KHHHHHK....",
    "....KHHHHHHhK...",
    "....KHSSSSSK....",
    "....KHSddSSK....",
    "....KHdddddK....",
    "....KSSSSSSK....",
    "...KsssTsssK....",
    "..KssTssssTssK..",
    "..KsTsssssssTK..",
    "..KTssssssssTK..",
    "..KTssssTsssTK..",
    "..KTTsssssssTK..",
    "...KsKKK.KssK...",
    "...KKK...KKK....",
    "................",
]

FORTUNE_TELLER = [
    "................",
    "....KPPPPPPK....",
    "...KPpPPPPpK....",
    "....KPYPPYPK....",
    "....KPSSSSPK....",
    "....KPSdSSdK....",
    "....KPSSSSPK....",
    "...KpPPPPPpK....",
    "..KpPPPYPPPPK...",
    "..KpPPPpPPPpK...",
    "..KpPPpPPPpPK...",
    "..KpPPPPPpPPK...",
    "..KpPPPPPPPPK...",
    "...KpKK.KKpK....",
    "...KKK...KKK....",
    "................",
]

PRIESTESS = [
    "......KYYK......",
    ".....KyIIyK.....",
    "......KYYK......",
    "....KWHHHHWK....",
    "...KWHSSSSHWK...",
    "...KWSSSSSWK....",
    "....KWSdSSK.....",
    "....KWWWWWK.....",
    "...KWWIWIWWK....",
    "..KWWWIIIWWWK...",
    "..KWWIWIIWIWWK..",
    "..KWWWIIIWWWK...",
    "..KWWIWYWIWWK...",
    "...KWKKIKKWK....",
    "...KKK...KKK....",
    "................",
]

HERMIT = [
    "................",
    "....KHHHHHK.....",
    "...KHHHHHHHK....",
    "...KHHSSSSHK....",
    "...KHSSdSSHK....",
    "....KHdddHK.....",
    "...KHdddddHK....",
    "....KSSSSSK.....",
    "...KTTThTTTK....",
    "..KTThTTTThTK...",
    "..KTTTTThTTTK...",
    "..KTThTTTTTTK...",
    "..KTTTTTThTTK...",
    "...KTTKKTTK.....",
    "...KKK.KKK......",
    "................",
]

DRUID = [
    "................",
    "....KGGGGGGK....",
    "...KGeGGGeGK....",
    "...KeGGGGGGeK...",
    "....KGSSSSGK....",
    "....KGSdSSK.....",
    "....KGSSdSK.....",
    "...KGGGGGGGK....",
    "..KGeGGeGGeGK...",
    "..KGGGeGGeGGK...",
    "..KGeGGGGGGeK...",
    "..KGGGeGGeGGK...",
    "..KGGGGGeGGGK...",
    "...KGGKKGGGK....",
    "...KKK..KKK.....",
    "................",
]

PRISONER = [
    "................",
    "....KHHHHHHK....",
    "...KHHHhHHHK....",
    "....KHSSSSK.....",
    "....KSdSddSK....",
    "....KSSSSSSK....",
    "....KSdSSdSK....",
    "...KTTTTTTTK....",
    "..KTThhhhhTTK...",
    "..KTTThThTTTK...",
    "..KTTTTTTTTTK...",
    "..KTThhTThhTK...",
    "..KTTTTTTTTTK...",
    "...KTTKKTTK.....",
    "...KKK..KKK.....",
    "................",
]

# ─── NEW enemy sprites ────────────────────────────────────────────────────────

ZOMBIE = [
    "................",
    ".....KgggK......",
    "....KgGgggK.....",
    "....KgNgNgGK....",
    "....KgjjjgK.....",
    "....KGggggGK....",
    "...KGNGggGNGK...",
    "...KGgggggGKK...",
    "..KGgGGgggGGgK..",
    "..KGggGggggGgK..",
    "..KGGgggggGGgK..",
    "...KGgGggggGK...",
    "...KGgKKGggK....",
    "...KGgK.KggK....",
    "....KK...KK.....",
    "................",
]

SKELETON_ARCHER = [
    "....KWWWWWK..T..",
    "...KWIWWWIwK.T..",
    "...KWnnnnWnK..T.",
    "....KWWnWWK...T.",
    ".....KWWWK...T..",
    "....KvvvvvKT.T..",
    "...KvvNvNvvKTT..",
    "..KvTTTTTTTTTK..",
    "..KvvvNNNvTvKT..",
    "...KvNvvvNTvK...",
    "..VKvvvvvvTvKV..",
    "..VKvNvvvNTvKV..",
    "...KvvKKvvvK....",
    "...KvvK.vvK.....",
    "....KKK.KK......",
    "................",
]

GIANT_SPIDER = [
    "................",
    ".K....K....K...K",
    "KK...K......K.KK",
    "..KK.K......K.K.",
    "....KNNNNNNK....",
    "..KNNRNNNRNNK...",
    ".KNNNNNNNNNNNK..",
    ".KNNWNNNNNWNNK..",
    ".KNNNNNNNNNNNK..",
    ".KNNNNNNNNNNNK..",
    "..KNNNNNNNNNK...",
    "...KNNNNNNNK....",
    ".K.KK.K..K.KK..K",
    "KK..K.K..K.K..KK",
    "K...K.K..K.K...K",
    "................",
]

DIRE_WOLF = [
    "................",
    "...KnnK....KnnK.",
    "..KnNNK...KNNnK.",
    "..KnNnNnnnnNnnK.",
    ".KnnNNNNNNNNnnK.",
    ".KnNnNNnNNnNNnK.",
    ".KnNNRNNNNRNNNK.",
    ".KnNnNNWWNNnNnK.",
    "..KnNWWKKWWNnK..",
    "..KnNKWWWWKNnK..",
    "...KnNWWWWNnK...",
    "..KnnnnnnnnnK...",
    "...KnnKKKKnnK...",
    "...Kn..K.K..nK..",
    "...KK...........",
    "................",
]

ANIMATED_ARMOR = [
    "....KLLLLLK.....",
    "...KLLLLLLLK....",
    "...KLKKKKKLK....",
    "...KLKRRKKLK....",
    "....KLLLLLK.....",
    "....KvvvvvK.....",
    "...KvvLLLvvK....",
    "..KvvLLLLLvvK...",
    "..KvLLLALLLvK...",
    "..KvLLLLLLLvK...",
    "..KvLLLLLLLvK...",
    "..KvLLLALLLvK...",
    "...KvKKKKKvK....",
    "...KvKK.KKvK....",
    "....KKK.KKK.....",
    "................",
]

CULTIST = [
    "................",
    ".....KNNNNK.....",
    "....KNNqqNNK....",
    "....KNqqqqNK....",
    "....KNqnnqNK....",
    "....KNqnnqNK....",
    "...KNqqqqqqNK...",
    "..KNqqqqqqqqNK..",
    "..KNqqqWqqqqNK..",
    "..KNqqqqqqqqNK..",
    "..KNqqqqqqqqNK..",
    "..KNqqqqqqqqNK..",
    "...KNqqqqqqNK...",
    "...KNqKKKqNK....",
    "...KKK...KKK....",
    "................",
]

WRAITH = [
    ".....Kqqqq......",
    "....KqqppqqK....",
    "...KqpPqqPpqK...",
    "...KqpRqqqRpK...",
    "....KqpPqPqK....",
    "...KqpPpPpPqK...",
    "..KqppPpPpPpqK..",
    "..KqpPpPpPpPpK..",
    ".KqpPpPpPpPpPqK.",
    ".KqpPpPpPpPpPqK.",
    "..KqpPpPpPpPpK..",
    "..KqppPpPpPpqK..",
    "...KqqpPpPpqK...",
    "....KqppPpqK....",
    ".....KqppqK.....",
    "......KqqK......",
]

SPIDER_QUEEN = [
    ".......YY.......",
    "......KYAYK.....",
    "......KYKYK.....",
    ".K...KNKYKN....K",
    "KK..KNNNYNNNK.KK",
    "..KKNNRNNRNNKK..",
    "..KNNNWNNWNNNK..",
    ".KNNNNNNNNNNNNK.",
    ".KNNNNNNNNNNNNK.",
    ".KNNNNPPPPNNNNK.",
    ".KNNNNNNNNNNNNK.",
    "..KNNNNNNNNNNK..",
    "...KNNNNNNNNK...",
    ".KK.KN....NK.KK.",
    "KK...K....K...KK",
    "K....K....K....K",
]

CULT_PRIEST = [
    "................",
    "....KNqYqNK.....",
    "...KNqYYYqNK....",
    "...KNqYqYqNK....",
    "....KNSSSNK.....",
    "...KNSddSNK.....",
    "...KNqYqqYNK....",
    "..KNqqYqYqqNK...",
    "..KNqYqqqqYNK...",
    "..KNqqqYqqqNK...",
    "..KNqYqqqYqNK...",
    "..KNqqYqYqqNK...",
    "..KNqqqqqqqNK...",
    "...KNqKKqNK.....",
    "...KKK..KKK.....",
    "................",
]

LESSER_DEMON = [
    "..K..........K..",
    "..KK........KK..",
    "...KK......KK...",
    "....KKRRRRRKK...",
    "...KRRRRRRRRK...",
    "..KRRYRRRRYRRK..",
    "..KRRNNRRNNRRK..",
    "..KRRRRWWRRRRK..",
    "..KRRRRRRRRRRK..",
    "..KRRTTTTTTRRK..",
    "..KRRRRRRRRRRK..",
    "..KRRRRRRRRRRK..",
    "...KRRRKKRRRK...",
    "..KKRRKXXKRRKK..",
    "..KK..K..K..KK..",
    "................",
]

def save_sprite(grid, filename):
    sprite_from_grid(grid).save(os.path.join(CHARACTERS_DIR, filename))
    print(f"  OK {filename}")

print("Generating character sprites...")
save_sprite(HERO,      "hero.png")
save_sprite(INNKEEPER, "innkeeper.png")
save_sprite(GOBLIN,    "goblin.png")
save_sprite(WIZARD,    "wizard.png")
save_sprite(SKELETON,  "skeleton.png")
save_sprite(TROLL,     "troll.png")
save_sprite(DRAGON,    "dragon.png")

# New NPC sprites
save_sprite(TOWN_CRIER,     "town_crier.png")
save_sprite(BLACKSMITH,     "blacksmith.png")
save_sprite(FORTUNE_TELLER, "fortune_teller.png")
save_sprite(PRIESTESS,      "priestess.png")
save_sprite(HERMIT,         "hermit.png")
save_sprite(DRUID,          "druid.png")
save_sprite(PRISONER,       "prisoner.png")

# New enemy sprites
save_sprite(ZOMBIE,          "zombie.png")
save_sprite(SKELETON_ARCHER, "skeleton_archer.png")
save_sprite(GIANT_SPIDER,    "giant_spider.png")
save_sprite(DIRE_WOLF,       "dire_wolf.png")
save_sprite(ANIMATED_ARMOR,  "animated_armor.png")
save_sprite(CULTIST,         "cultist.png")
save_sprite(WRAITH,          "wraith.png")
save_sprite(SPIDER_QUEEN,    "spider_queen.png")
save_sprite(CULT_PRIEST,     "cult_priest.png")
save_sprite(LESSER_DEMON,    "lesser_demon.png")

# ─── UI icons (64×64) ──────────────────────────────────────────────────────────

def draw_heart():
    img  = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, 32, 32], fill=(200, 30, 30, 255))
    draw.ellipse([28, 4, 56, 32], fill=(200, 30, 30, 255))
    pts = [(4, 20), (32, 58), (60, 20)]
    draw.polygon(pts, fill=(200, 30, 30, 255))
    draw.ellipse([10, 10, 24, 24], fill=(240, 80, 80, 255))
    return img

def draw_coin():
    img  = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, 60, 60], fill=(200, 160, 20, 255))
    draw.ellipse([10, 10, 54, 54], fill=(240, 200, 40, 255))
    draw.ellipse([18, 18, 46, 46], fill=(220, 175, 30, 255))
    draw.text((22, 20), "G", fill=(180, 130, 10, 255))
    return img

def draw_sword_icon():
    img  = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Blade
    draw.polygon([(32, 4), (28, 52), (36, 52)], fill=(190, 190, 190, 255))
    draw.polygon([(32, 4), (30, 48), (32, 52), (34, 48)], fill=(220, 220, 220, 255))
    # Guard
    draw.rectangle([16, 48, 48, 54], fill=(160, 120, 40, 255))
    draw.rectangle([18, 49, 46, 53], fill=(200, 160, 60, 255))
    # Grip
    draw.rectangle([28, 54, 36, 62], fill=(120, 80, 30, 255))
    # Pommel
    draw.ellipse([25, 60, 39, 64], fill=(160, 120, 40, 255))
    return img

print("Generating UI icons...")
draw_heart().save(os.path.join(UI_DIR, "heart.png")); print("  OK heart.png")
draw_coin().save(os.path.join(UI_DIR, "coin.png"));   print("  OK coin.png")
draw_sword_icon().save(os.path.join(UI_DIR, "sword.png")); print("  OK sword.png")

# ─── Background scenes (800×450) ───────────────────────────────────────────────

W, H = 800, 450
rng = random.Random(42)   # deterministic

def gradient(draw, y0, y1, col_top, col_bot):
    for y in range(y0, y1):
        t = (y - y0) / max(y1 - y0 - 1, 1)
        r = int(col_top[0] + (col_bot[0]-col_top[0]) * t)
        g = int(col_top[1] + (col_bot[1]-col_top[1]) * t)
        b = int(col_top[2] + (col_bot[2]-col_top[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

def stone_wall(draw, y0, y1, base=(60, 55, 50)):
    """Draw tiled stone bricks."""
    bh, bw = 40, 80
    for row in range(y0, y1, bh):
        offset = (row // bh % 2) * (bw // 2)
        for col in range(-bw, W + bw, bw):
            x = col + offset
            shade = rng.randint(-12, 12)
            c = tuple(max(0, min(255, base[i]+shade)) for i in range(3))
            draw.rectangle([x+2, row+2, x+bw-2, row+bh-2], fill=c)
            draw.rectangle([x, row, x+bw, row+bh], outline=(30, 25, 20), width=2)

def torch(draw, x, y, flicker=0):
    """Draw a wall torch with flame."""
    draw.rectangle([x-4, y, x+4, y+18], fill=(100, 70, 30))
    draw.rectangle([x-5, y-3, x+5, y+3], fill=(130, 95, 45))
    for i, flame_color in enumerate([(255,140,20), (255,200,40), (255,240,80)]):
        fx = x + rng.randint(-2, 2) + flicker
        draw.ellipse([fx-6+i, y-18+i*3, fx+6-i, y+i*2], fill=flame_color)

def cobblestones(draw, y0, y1, base=(120, 115, 105)):
    """Draw cobbled street."""
    for y in range(y0, y1, 18):
        for x in range(-20, W+20, 28):
            xo = x + (18 if (y // 18) % 2 else 0)
            shade = rng.randint(-18, 18)
            c = tuple(max(0, min(255, base[i]+shade)) for i in range(3))
            draw.ellipse([xo, y, xo+26, y+16], fill=c)

def tree(draw, x, y_base, height=280, trunk_w=40, tint=0):
    """Draw a simple forest tree."""
    shade = rng.randint(-8, 8) + tint
    tc = (18+shade, 38+shade, 18+shade)
    draw.rectangle([x-trunk_w//2, y_base-height//2, x+trunk_w//2, y_base], fill=(60, 40, 20))
    for li in range(3):
        lw = trunk_w*2 + li*24
        lh = height//3 - li*15
        ly = y_base - height//2 + li*(height//5) - 20
        fc = (22+shade, 55+shade, 22+shade)
        draw.ellipse([x-lw//2, ly, x+lw//2, ly+lh+40], fill=fc)

# ─── VILLAGE scenes ───────────────────────────────────────────────────────────

def bg_tavern():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (80, 55, 30), (45, 30, 15))
    stone_wall(draw, 0, H//2+40, base=(85, 70, 50))
    # Wood floor
    for y in range(H//2+40, H, 28):
        shade = rng.randint(-10, 10)
        c = (110+shade, 72+shade, 32+shade)
        draw.rectangle([0, y, W, y+25], fill=c)
        for x in range(0, W, rng.randint(80, 140)):
            draw.line([(x, y), (x, y+25)], fill=(80, 50, 20), width=1)
    # Fireplace back wall
    draw.rectangle([W//2-100, H//2-60, W//2+100, H//2+40], fill=(50, 40, 30))
    draw.rectangle([W//2-80, H//2-40, W//2+80, H//2+40], fill=(30, 25, 20))
    # Fire glow
    for _ in range(60):
        fx = W//2 + rng.randint(-60, 60)
        fy = H//2 + rng.randint(-20, 38)
        r  = rng.randint(4, 14)
        alpha_col = (255, rng.randint(100, 220), rng.randint(0, 60))
        draw.ellipse([fx-r, fy-r, fx+r, fy+r], fill=alpha_col)
    glow_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    for i in range(8):
        r = 60 + i * 22
        alpha = max(0, 55 - i * 7)
        glow_draw.ellipse([W//2-r, H//2+10-r//4, W//2+r, H//2+10+r//4],
                          fill=(255, 140, 20, alpha))
    img.paste(Image.new("RGB", (W, H), (255, 140, 20)),
              mask=glow_img.split()[3])
    torch(draw, 180, 120)
    torch(draw, W-180, 120)
    draw.rectangle([80, H-120, 280, H-90], fill=(90, 60, 25))
    draw.rectangle([W-280, H-120, W-80, H-90], fill=(90, 60, 25))
    return img

def bg_town_square():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    # Daytime sky
    gradient(draw, 0, H*2//5, (130, 180, 230), (200, 220, 235))
    # Distant buildings
    for i, bx in enumerate([50, 180, 320, 470, 620]):
        bh = rng.randint(140, 220)
        bw = rng.randint(100, 150)
        col = (rng.randint(110, 170), rng.randint(90, 140), rng.randint(70, 110))
        draw.rectangle([bx, H*2//5 - bh, bx+bw, H*2//5+20], fill=col)
        # Roofs
        draw.polygon([(bx-10, H*2//5-bh), (bx+bw+10, H*2//5-bh),
                      (bx+bw//2, H*2//5-bh-50)], fill=(110, 50, 30))
        # Windows
        for wy in range(H*2//5-bh+30, H*2//5-30, 40):
            for wx in range(bx+20, bx+bw-20, 40):
                draw.rectangle([wx, wy, wx+16, wy+24], fill=(80, 110, 140))
    # Cobble street
    cobblestones(draw, H*2//5+20, H, base=(130, 120, 100))
    # Fountain in centre
    draw.ellipse([W//2-90, H*2//3-20, W//2+90, H*2//3+60], fill=(90, 85, 75))
    draw.ellipse([W//2-75, H*2//3-5, W//2+75, H*2//3+45], fill=(70, 110, 160))
    draw.rectangle([W//2-12, H*2//3-70, W//2+12, H*2//3-10], fill=(100, 95, 85))
    draw.ellipse([W//2-20, H*2//3-85, W//2+20, H*2//3-65], fill=(110, 105, 95))
    # Water splash
    for _ in range(20):
        sx = W//2 + rng.randint(-15, 15)
        sy = H*2//3 + rng.randint(-60, -10)
        draw.ellipse([sx-2, sy-2, sx+2, sy+2], fill=(180, 220, 240))
    # Signpost
    draw.rectangle([140, H*2//3-80, 150, H*2//3+40], fill=(100, 70, 30))
    for i, lbl_y in enumerate([H*2//3-75, H*2//3-55, H*2//3-35]):
        dx = 80 if i % 2 == 0 else -80
        draw.rectangle([140+min(dx,0), lbl_y, 150+max(dx,0), lbl_y+14], fill=(160, 120, 50))
    return img

def bg_market_square():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H*2//5, (135, 185, 230), (210, 225, 235))
    # Stone wall of shops
    for i, bx in enumerate([20, 250, 520]):
        draw.rectangle([bx, 60, bx+240, H*2//5+20], fill=(130, 110, 80))
        draw.rectangle([bx+20, 120, bx+220, H*2//5], fill=(90, 70, 40))
    cobblestones(draw, H*2//5+20, H, base=(135, 125, 105))
    # Awnings / stalls
    colors = [(180,40,40), (40,80,150), (190,140,30), (40,120,60), (120,40,150)]
    xs = [70, 220, 360, 510, 660]
    for x, col in zip(xs, colors):
        # Stall pole
        draw.rectangle([x-2, H*2//5+30, x+2, H-60], fill=(80, 50, 20))
        draw.rectangle([x+96, H*2//5+30, x+100, H-60], fill=(80, 50, 20))
        # Awning (striped)
        for i in range(6):
            sx = x + i*17
            sc = col if i % 2 == 0 else (255, 245, 225)
            draw.polygon([(sx, H*2//5+30), (sx+17, H*2//5+30),
                          (sx+14, H*2//5+60), (sx+3, H*2//5+60)], fill=sc)
        # Stall table
        draw.rectangle([x-10, H-100, x+110, H-70], fill=(110, 70, 30))
        # Wares
        for wx in range(x+5, x+95, 20):
            draw.ellipse([wx, H-115, wx+14, H-100], fill=(rng.randint(120,240), rng.randint(80,200), rng.randint(40,160)))
    return img

def bg_blacksmith():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (55, 35, 20), (30, 18, 10))
    stone_wall(draw, 0, H, base=(70, 60, 48))
    # Forge
    draw.rectangle([W//2-120, H//2-20, W//2+120, H-60], fill=(40, 25, 15))
    draw.rectangle([W//2-100, H//2, W//2+100, H-80], fill=(25, 15, 8))
    # Fire glow
    for _ in range(80):
        fx = W//2 + rng.randint(-80, 80)
        fy = H//2 + rng.randint(0, 80)
        r  = rng.randint(4, 16)
        alpha_col = (255, rng.randint(100, 220), rng.randint(0, 40))
        draw.ellipse([fx-r, fy-r, fx+r, fy+r], fill=alpha_col)
    # Anvil
    draw.rectangle([180, H-130, 300, H-100], fill=(50, 50, 55))
    draw.rectangle([200, H-100, 280, H-60], fill=(40, 40, 45))
    draw.rectangle([210, H-60, 270, H-40], fill=(60, 60, 65))
    # Weapon rack
    draw.rectangle([W-200, 80, W-40, 260], fill=(70, 45, 20))
    for i, swc in enumerate([(200,200,200), (180,180,180), (160,160,160), (180,140,40)]):
        sx = W-185 + i*38
        draw.rectangle([sx-4, 90, sx+4, 240], fill=swc)
        draw.rectangle([sx-10, 230, sx+10, 245], fill=(120, 80, 30))
    # Sparks
    for _ in range(40):
        sx = rng.randint(180, 300)
        sy = rng.randint(H-140, H-100)
        draw.ellipse([sx-2, sy-2, sx+2, sy+2], fill=(255, 220, 80))
    return img

def bg_mystics_shop():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (45, 20, 55), (20, 10, 30))
    # Velvet curtain walls
    for x in range(0, W, 40):
        shade = rng.randint(-12, 12)
        c = (80+shade, 30+shade, 100+shade)
        draw.polygon([(x, 0), (x+40, 0), (x+30, H), (x+10, H)], fill=c)
        draw.line([(x+20, 0), (x+20, H)], fill=(40, 15, 55), width=2)
    # Table with lace
    draw.ellipse([W//2-180, H-140, W//2+180, H-40], fill=(90, 30, 110))
    draw.ellipse([W//2-160, H-130, W//2+160, H-50], fill=(180, 150, 200))
    # Crystal ball
    for r in range(60, 0, -4):
        t = r/60
        col = (int(180-60*t), int(180-60*t), int(240-20*t))
        draw.ellipse([W//2-r, H-190-r, W//2+r, H-190+r], fill=col)
    # Inner glow
    draw.ellipse([W//2-20, H-210, W//2+20, H-170], fill=(250, 250, 255))
    # Tarot cards
    for i, cx in enumerate([W//2-140, W//2-100, W//2+70, W//2+120]):
        draw.rectangle([cx, H-110, cx+28, H-60], fill=(230, 210, 170))
        draw.rectangle([cx+3, H-107, cx+25, H-63], outline=(150, 100, 30))
    # Candle smoke
    for _ in range(50):
        sx = rng.randint(100, W-100)
        sy = rng.randint(40, H//2)
        r = rng.randint(6, 18)
        draw.ellipse([sx-r, sy-r, sx+r, sy+r], fill=(100, 60, 120))
    return img

def bg_temple():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (240, 220, 170), (180, 150, 100))
    # Side columns
    for cx in [90, 240, W-240, W-90]:
        draw.rectangle([cx-22, 60, cx+22, H-40], fill=(220, 210, 190))
        draw.rectangle([cx-28, 50, cx+28, 80], fill=(230, 220, 200))
        draw.rectangle([cx-28, H-60, cx+28, H-40], fill=(230, 220, 200))
    # Stained glass windows
    for wx in [W//3, 2*W//3]:
        draw.rectangle([wx-60, 60, wx+60, 220], fill=(40, 40, 30))
        for r in range(3):
            for c in range(3):
                col = rng.choice([(200,40,40),(40,80,180),(220,180,30),
                                   (40,150,80),(150,60,180)])
                draw.rectangle([wx-55+c*40, 65+r*52, wx-20+c*40, 110+r*52], fill=col)
    # Light rays
    for _ in range(30):
        lx = rng.randint(100, W-100)
        ly = H - rng.randint(100, 300)
        draw.polygon([(lx-6, 0), (lx+6, 0), (lx+30, ly), (lx-30, ly)],
                     fill=(255, 240, 180))
    # Altar
    draw.rectangle([W//2-100, H-140, W//2+100, H-60], fill=(240, 230, 210))
    draw.rectangle([W//2-80, H-160, W//2+80, H-140], fill=(250, 240, 220))
    # Candles
    for cx in [W//2-70, W//2-35, W//2, W//2+35, W//2+70]:
        draw.rectangle([cx-3, H-180, cx+3, H-160], fill=(250, 240, 220))
        draw.ellipse([cx-5, H-188, cx+5, H-176], fill=(255, 200, 60))
    return img

def bg_graveyard():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H//2, (20, 18, 35), (45, 40, 55))
    # Pale moon behind clouds
    draw.ellipse([W-200, 40, W-100, 140], fill=(200, 195, 170))
    # Wet grass ground
    gradient(draw, H//2, H, (25, 40, 25), (12, 20, 12))
    # Tombstones — scattered at varied angles
    for i in range(14):
        tx = rng.randint(40, W-60)
        ty = H - rng.randint(80, 220)
        tw = rng.randint(30, 55)
        th = rng.randint(60, 110)
        tilt = rng.randint(-4, 4)
        # Body
        col = (rng.randint(110, 150), rng.randint(110, 145), rng.randint(110, 140))
        draw.polygon([(tx, ty), (tx+tw, ty+tilt),
                      (tx+tw, ty+th), (tx, ty+th-tilt)], fill=col)
        # Cross or rounded top
        if rng.random() < 0.5:
            draw.ellipse([tx-4, ty-20, tx+tw+4, ty+14], fill=col)
        else:
            draw.rectangle([tx+tw//2-4, ty-20, tx+tw//2+4, ty+14], fill=col)
            draw.rectangle([tx+tw//2-14, ty-10, tx+tw//2+14, ty-2], fill=col)
    # Low mist
    mist = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    md = ImageDraw.Draw(mist)
    for _ in range(40):
        mx = rng.randint(0, W)
        my = rng.randint(H-150, H)
        r  = rng.randint(80, 160)
        md.ellipse([mx-r, my-r//3, mx+r, my+r//3], fill=(200, 200, 220, 40))
    img.paste(mist, mask=mist.split()[3])
    # Dead tree
    draw.rectangle([80, H-240, 100, H-60], fill=(40, 30, 20))
    for branch in [(60, H-200, 40, H-260), (120, H-180, 150, H-240),
                   (90, H-220, 60, H-280)]:
        draw.line([branch[0:2], branch[2:4]], fill=(40, 30, 20), width=5)
    return img

# ─── FOREST scenes ────────────────────────────────────────────────────────────

def bg_forest():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H//2, (8, 12, 35), (15, 25, 55))
    for _ in range(120):
        sx = rng.randint(0, W)
        sy = rng.randint(0, H//2)
        br = rng.randint(160, 255)
        r  = rng.randint(1, 2)
        draw.ellipse([sx-r, sy-r, sx+r, sy+r], fill=(br, br, br))
    draw.ellipse([W-160, 20, W-60, 120], fill=(240, 235, 200))
    draw.ellipse([W-145, 25, W-55, 115], fill=(200, 195, 160))
    draw.ellipse([W-150, 22, W-62, 118], fill=(240, 235, 200))
    gradient(draw, H//2, H, (18, 38, 18), (10, 22, 10))
    for tx in range(-40, W+40, 65):
        th = rng.randint(200, 340)
        tree(draw, tx, H, height=th, trunk_w=rng.randint(30, 55))
    for i in range(15):
        r = 30 + i*18
        draw.ellipse([W-110-r, H//2-r//6, W-110+r, H//2+r//6],
                     outline=(200, 200, 160))
    draw.ellipse([W//2-200, H//2-30, W//2+200, H//2+30], fill=(22, 48, 22))
    return img

def bg_river_crossing():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H//2, (10, 15, 40), (22, 30, 55))
    # Moon
    draw.ellipse([100, 40, 190, 130], fill=(240, 235, 200))
    # Far bank
    gradient(draw, H//2, H//2+40, (25, 40, 25), (18, 30, 18))
    # River — wide horizontal band with shimmer
    for y in range(H//2+40, H-60):
        t = (y - (H//2+40)) / ((H-60) - (H//2+40))
        col = (int(20+50*t), int(30+60*t), int(60+60*t))
        draw.line([(0, y), (W, y)], fill=col)
    # Ripples
    for _ in range(80):
        ry = rng.randint(H//2+50, H-65)
        rx = rng.randint(0, W)
        rw = rng.randint(30, 80)
        draw.line([(rx, ry), (rx+rw, ry)], fill=(160, 180, 200), width=1)
    # Near bank
    gradient(draw, H-60, H, (22, 35, 22), (12, 20, 12))
    # Footbridge
    draw.rectangle([W//3, H//2+30, 2*W//3, H//2+55], fill=(80, 55, 25))
    for px in range(W//3+10, 2*W//3, 30):
        draw.rectangle([px, H//2+20, px+6, H//2+55], fill=(60, 40, 20))
    # Rails
    draw.line([(W//3, H//2+20), (2*W//3, H//2+20)], fill=(90, 65, 30), width=3)
    # Hut on near bank
    draw.rectangle([60, H-160, 220, H-50], fill=(80, 55, 30))
    draw.polygon([(50, H-160), (230, H-160), (140, H-210)], fill=(100, 60, 30))
    # Warm window glow
    draw.rectangle([120, H-120, 160, H-90], fill=(255, 200, 80))
    # Trees
    for tx in [260, 350, 470, 560, 660]:
        tree(draw, tx, H//2+60, height=180, trunk_w=30)
    return img

def bg_ancient_ruins():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H//2, (30, 30, 50), (70, 65, 75))
    gradient(draw, H//2, H, (55, 65, 45), (30, 40, 28))
    # Moss-covered flagstones
    for y in range(H//2+20, H, 30):
        for x in range(-30, W+30, 60):
            xo = x + (30 if (y // 30) % 2 else 0)
            shade = rng.randint(-12, 12)
            c = (90+shade, 100+shade, 80+shade)
            draw.rectangle([xo, y, xo+58, y+28], fill=c)
            draw.rectangle([xo, y, xo+58, y+28], outline=(50, 60, 40), width=1)
    # Toppled pillars (horizontal)
    for i, (px, py) in enumerate([(80, H-130), (480, H-110), (620, H-140)]):
        for seg in range(4):
            draw.ellipse([px + seg*35, py, px + seg*35 + 60, py+40], fill=(180, 170, 140))
            draw.ellipse([px + seg*35 + 6, py+6, px + seg*35 + 54, py+34], fill=(150, 140, 110))
    # Standing broken pillar
    for s, py in enumerate(range(H//2-30, H-60, 45)):
        draw.rectangle([W//2-30, py, W//2+30, py+45], fill=(180, 170, 140))
        draw.rectangle([W//2-32, py, W//2+32, py+6], fill=(150, 140, 110))
    # Top — broken off
    draw.polygon([(W//2-30, H//2-30), (W//2+30, H//2-30),
                  (W//2+15, H//2-55), (W//2-18, H//2-48)], fill=(180, 170, 140))
    # Carved face stone
    draw.rectangle([300, H-110, 420, H-50], fill=(150, 140, 110))
    for ey in [H-95]:
        draw.ellipse([320, ey-8, 340, ey+8], fill=(40, 40, 40))
        draw.ellipse([380, ey-8, 400, ey+8], fill=(40, 40, 40))
    # Moss
    for _ in range(60):
        mx = rng.randint(0, W)
        my = rng.randint(H//2, H)
        draw.ellipse([mx, my, mx+rng.randint(8, 20), my+6], fill=(50, 100, 50))
    return img

def bg_wolf_den():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (30, 25, 20), (10, 8, 6))
    # Cave opening shape
    pts = [(0, H), (0, 100), (120, 40), (W-120, 40), (W, 100), (W, H)]
    draw.polygon(pts, fill=(25, 20, 18))
    # Rocky walls
    for _ in range(80):
        rx = rng.randint(0, W)
        ry = rng.randint(60, H-40)
        rr = rng.randint(15, 40)
        shade = rng.randint(-10, 10)
        draw.ellipse([rx-rr, ry-rr, rx+rr, ry+rr], fill=(45+shade, 38+shade, 32+shade))
    # Dark interior gradient
    for r in range(100, 400, 20):
        draw.ellipse([W//2-r, H//2-r//2, W//2+r, H//2+r//2], outline=(0,0,0))
    # Deep shadow
    draw.ellipse([W//2-130, H//2-60, W//2+130, H//2+60], fill=(5, 4, 3))
    # Yellow eyes
    for ex in [W//2-30, W//2+30]:
        draw.ellipse([ex-6, H//2-10, ex+6, H//2+2], fill=(255, 220, 40))
        draw.ellipse([ex-3, H//2-7, ex+3, H//2-1], fill=(255, 255, 80))
    # Bones on floor
    for _ in range(25):
        bx = rng.randint(60, W-60)
        by = rng.randint(H-80, H-20)
        l  = rng.randint(20, 50)
        draw.rectangle([bx, by, bx+l, by+4], fill=(230, 220, 200))
        draw.ellipse([bx-4, by-3, bx+4, by+7], fill=(230, 220, 200))
        draw.ellipse([bx+l-4, by-3, bx+l+4, by+7], fill=(230, 220, 200))
    return img

def bg_deep_woods():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    # Very dark canopy
    gradient(draw, 0, H//2, (5, 12, 8), (10, 18, 12))
    # Darker ground
    gradient(draw, H//2, H, (12, 20, 12), (6, 12, 6))
    # Dense trees overlapping
    for tx in range(-60, W+60, 45):
        th = rng.randint(280, 420)
        tree(draw, tx, H-40, height=th, trunk_w=rng.randint(35, 65), tint=-10)
    # A few closer, bigger trees
    for tx in [80, 420, 680]:
        th = rng.randint(360, 460)
        tree(draw, tx, H+20, height=th, trunk_w=70, tint=-20)
    # Fireflies (sparse)
    for _ in range(25):
        fx = rng.randint(0, W)
        fy = rng.randint(80, H-40)
        draw.ellipse([fx-3, fy-3, fx+3, fy+3], fill=(240, 255, 160))
        draw.ellipse([fx-1, fy-1, fx+1, fy+1], fill=(255, 255, 220))
    # Narrow path of moonlight
    draw.polygon([(W//2-25, H), (W//2+25, H), (W//2+8, H//2), (W//2-8, H//2)],
                 fill=(35, 45, 35))
    return img

def bg_hidden_grove():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (30, 45, 70), (40, 70, 55))
    # Silver-barked trees in a circle
    for ang in range(0, 360, 24):
        rad = math.radians(ang)
        cx = W//2 + int(280 * math.cos(rad))
        cy = H//2 + 60 + int(130 * math.sin(rad))
        th = rng.randint(180, 240)
        draw.rectangle([cx-14, cy-th, cx+14, cy], fill=(200, 210, 220))
        draw.ellipse([cx-50, cy-th-30, cx+50, cy-th+30], fill=(150, 200, 170))
        draw.ellipse([cx-45, cy-th-20, cx+45, cy-th+20], fill=(180, 230, 200))
    # Glowing pool at centre
    for r in range(120, 0, -10):
        t = r/120
        col = (int(120+80*t), int(200+40*t), int(200+55*t))
        draw.ellipse([W//2-r, H//2+40-r//3, W//2+r, H//2+40+r//3], fill=col)
    # Luminescent flowers in grass
    for _ in range(40):
        fx = rng.randint(60, W-60)
        fy = rng.randint(H//2+20, H-20)
        col = rng.choice([(180,220,255), (255,220,180), (220,180,255)])
        draw.ellipse([fx-4, fy-4, fx+4, fy+4], fill=col)
        draw.ellipse([fx-2, fy-2, fx+2, fy+2], fill=(255, 255, 255))
    # Mystical haze
    haze = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(haze)
    for _ in range(30):
        hx = rng.randint(0, W)
        hy = rng.randint(0, H)
        hr = rng.randint(60, 140)
        hd.ellipse([hx-hr, hy-hr//2, hx+hr, hy+hr//2], fill=(150, 220, 220, 30))
    img.paste(haze, mask=haze.split()[3])
    return img

def bg_wizard_tower():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (20, 15, 35), (10, 8, 18))
    stone_wall(draw, 0, H, base=(42, 35, 55))
    for y in range(H*2//3, H, 26):
        shade = rng.randint(-8, 8)
        c = (68+shade, 45+shade, 22+shade)
        draw.rectangle([0, y, W, y+24], fill=c)
    for bx in [40, W-180]:
        draw.rectangle([bx, 80, bx+140, H*2//3], fill=(55, 38, 18))
        for by in range(100, H*2//3-20, 32):
            for col_i, col in enumerate([(180,30,30),(30,30,180),(30,120,30),
                                          (150,100,30),(80,30,150)]):
                bk_x = bx+8 + col_i*22
                draw.rectangle([bk_x, by, bk_x+18, by+28], fill=col)
    for r in range(50, 0, -5):
        t = r/50
        col = (int(100+155*t), int(50+100*t), int(200+55*t))
        draw.ellipse([W//2-r, H//3-r, W//2+r, H//3+r], fill=col)
    for r in [30, 60, 90, 120]:
        draw.ellipse([W//2-r, H-60-r//3, W//2+r, H-60+r//3],
                     outline=(120, 80, 200), width=2)
    torch(draw, 200, 100)
    torch(draw, W-200, 100)
    draw.rectangle([W//2-80, H*2//3-20, W//2+80, H*2//3], fill=(90, 65, 30))
    for cx in [W//2-50, W//2, W//2+50]:
        draw.rectangle([cx-4, H*2//3-40, cx+4, H*2//3-20], fill=(240, 230, 200))
        draw.ellipse([cx-5, H*2//3-45, cx+5, H*2//3-38], fill=(255, 180, 40))
    return img

# ─── UPPER DUNGEON scenes ─────────────────────────────────────────────────────

def bg_dungeon_entrance():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (25, 22, 20), (12, 10, 8))
    stone_wall(draw, 0, H, base=(55, 50, 45))
    arch_x, arch_w, arch_h = W//2-120, 240, 320
    draw.rectangle([arch_x, H-arch_h, arch_x+arch_w, H], fill=(8, 6, 5))
    draw.ellipse([arch_x, H-arch_h-60, arch_x+arch_w, H-arch_h+60], fill=(8, 6, 5))
    for i in range(0, 200, 20):
        t = i / 200
        ax = arch_x + i - 10
        ay = H - arch_h - 60 + int(60*(1-math.sin(math.pi*t)))
        shade = rng.randint(-8, 8)
        bs = (68+shade, 62+shade, 55+shade)
        draw.rectangle([ax, ay, ax+22, ay+18], fill=bs)
    for i in range(20):
        r = 40 + i*8
        draw.ellipse([W//2-r, H-arch_h+40-r//4, W//2+r, H-arch_h+40+r//4],
                     outline=(30, 80, 30))
    torch(draw, arch_x-40, H-arch_h+60)
    torch(draw, arch_x+arch_w+40, H-arch_h+60)
    draw.polygon([(arch_x+20, H), (arch_x+arch_w-20, H),
                  (W//2+30, H-arch_h), (W//2-30, H-arch_h)], fill=(30, 25, 20))
    return img

def bg_dungeon_corridor():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (15, 12, 10), (8, 6, 5))
    stone_wall(draw, 0, H, base=(48, 43, 38))
    draw.rectangle([0, 0, W, 80], fill=(22, 18, 15))
    draw.rectangle([0, H-80, W, H], fill=(30, 25, 20))
    draw.polygon([(20, 80), (W//2-30, H//2-10),
                  (W//2-30, H//2+10), (20, H-80)], fill=(38, 33, 28))
    draw.polygon([(W-20, 80), (W//2+30, H//2-10),
                  (W//2+30, H//2+10), (W-20, H-80)], fill=(38, 33, 28))
    draw.ellipse([W//2-35, H//2-25, W//2+35, H//2+25], fill=(4, 3, 2))
    torch(draw, 220, 150)
    torch(draw, W-220, 150)
    return img

def bg_treasure_room():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (30, 25, 10), (15, 12, 5))
    stone_wall(draw, 0, H//2+60, base=(52, 47, 35))
    for y in range(H//2+60, H, 24):
        shade = rng.randint(-8, 8)
        c = (45+shade, 38+shade, 18+shade)
        draw.rectangle([0, y, W, y+22], fill=c)
    for cx in [180, W//2, W-180]:
        draw.rectangle([cx-45, H-160, cx+45, H-90], fill=(100, 68, 22))
        draw.rectangle([cx-48, H-175, cx+48, H-155], fill=(115, 78, 28))
        draw.rectangle([cx-40, H-168, cx+40, H-158], fill=(180, 140, 40))
        draw.ellipse([cx-8, H-167, cx+8, H-153], fill=(200, 160, 20))
    for _ in range(80):
        gx = rng.randint(60, W-60)
        gy = rng.randint(H-80, H-10)
        r  = rng.randint(4, 10)
        draw.ellipse([gx-r, gy-r//2, gx+r, gy+r//2], fill=(220, 175, 30))
    torch(draw, 120, 100)
    torch(draw, W-120, 100)
    for _ in range(30):
        gx = rng.randint(100, W-100)
        gy = rng.randint(H-120, H-20)
        draw.ellipse([gx-5, gy-3, gx+5, gy+3], fill=(255, 215, 10))
    return img

def bg_guard_room():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (22, 20, 18), (10, 9, 8))
    stone_wall(draw, 0, H, base=(55, 50, 45))
    draw.rectangle([0, H-80, W, H], fill=(30, 25, 20))
    # Weapon racks
    for bx in [60, W-210]:
        draw.rectangle([bx, 80, bx+150, H-90], fill=(70, 45, 20))
        draw.rectangle([bx-6, 80, bx+156, 100], fill=(60, 35, 15))
        # Swords / spears
        for i in range(5):
            sx = bx + 12 + i*27
            col = rng.choice([(190,190,190), (180,180,180), (160,160,160)])
            # Shaft/blade
            draw.rectangle([sx-3, 110, sx+3, H-110], fill=col)
            # Guard
            draw.rectangle([sx-10, H-110, sx+10, H-102], fill=(120, 80, 30))
        # Shield
        draw.ellipse([bx+40, H-180, bx+110, H-100], fill=(140, 40, 40))
        draw.ellipse([bx+50, H-170, bx+100, H-110], fill=(180, 60, 60))
        draw.line([(bx+75, H-175), (bx+75, H-105)], fill=(250, 220, 100), width=3)
    # Arrow target
    draw.ellipse([W//2-40, 100, W//2+40, 180], fill=(180, 180, 180))
    for r, c in zip([30, 20, 10], [(200,40,40), (240,200,40), (30,80,170)]):
        draw.ellipse([W//2-r, 140-r, W//2+r, 140+r], fill=c)
    # Stuck arrows
    for ax in [W//2-25, W//2, W//2+22]:
        draw.line([(ax, 130), (ax+40, 80)], fill=(120, 80, 30), width=3)
    torch(draw, 180, 130)
    torch(draw, W-180, 130)
    return img

def bg_mushroom_cavern():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (10, 20, 30), (5, 10, 18))
    # Rocky floor
    for _ in range(40):
        rx = rng.randint(0, W)
        ry = rng.randint(H-100, H)
        rr = rng.randint(20, 60)
        draw.ellipse([rx-rr, ry-rr//2, rx+rr, ry+rr//2],
                     fill=(30, 35, 45))
    # Giant mushrooms
    for i, (mx, scale) in enumerate([(120, 1.4), (320, 1.0), (520, 1.6),
                                      (680, 0.9), (220, 0.8), (420, 0.7)]):
        stalk_w = int(40 * scale)
        stalk_h = int(200 * scale)
        cap_r = int(90 * scale)
        base_y = H - 40
        # Stalk
        draw.rectangle([mx-stalk_w//2, base_y-stalk_h, mx+stalk_w//2, base_y],
                       fill=(230, 220, 190))
        # Cap underglow (filled halo)
        for k in range(10, 0, -1):
            r = cap_r + k*6
            col_b = max(0, min(255, 100 - k*5))
            col_g = max(0, min(255, 200 - k*10))
            draw.ellipse([mx-r, base_y-stalk_h-r//2, mx+r, base_y-stalk_h+r//2],
                         fill=(col_b, col_g, 255))
        # Cap
        draw.ellipse([mx-cap_r, base_y-stalk_h-cap_r, mx+cap_r, base_y-stalk_h+cap_r//3],
                     fill=(60, 120, 180))
        draw.ellipse([mx-cap_r+10, base_y-stalk_h-cap_r+10, mx+cap_r-10, base_y-stalk_h+cap_r//3-10],
                     fill=(80, 170, 220))
        # Spots
        for _ in range(6):
            dx = mx + rng.randint(-cap_r+15, cap_r-15)
            dy = base_y-stalk_h - rng.randint(0, cap_r-20)
            draw.ellipse([dx-6, dy-4, dx+6, dy+4], fill=(230, 240, 255))
    # Web strands
    for _ in range(15):
        x1, y1 = rng.randint(0, W), rng.randint(80, 200)
        x2, y2 = rng.randint(0, W), rng.randint(80, 200)
        draw.line([(x1, y1), (x2, y2)], fill=(200, 210, 220), width=1)
    return img

def bg_spider_queen_lair():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (18, 12, 20), (8, 5, 10))
    # Web-draped walls
    for _ in range(200):
        x1, y1 = rng.randint(0, W), rng.randint(0, H)
        x2, y2 = x1 + rng.randint(-120, 120), y1 + rng.randint(-120, 120)
        draw.line([(x1, y1), (x2, y2)], fill=(170, 170, 190), width=1)
    # Silk floor
    for y in range(H-60, H, 6):
        draw.line([(0, y), (W, y)], fill=(180, 180, 200))
    # Egg sacs hanging
    for ex in [80, 180, 320, 480, 620, 720]:
        ey = rng.randint(40, 140)
        er = rng.randint(18, 30)
        draw.line([(ex, 0), (ex, ey)], fill=(200, 200, 220), width=1)
        draw.ellipse([ex-er, ey, ex+er, ey+er*2], fill=(220, 215, 200))
        draw.ellipse([ex-er+4, ey+4, ex+er-4, ey+er*2-4], fill=(240, 235, 220))
        # Veins
        for _ in range(4):
            vx = ex + rng.randint(-er+4, er-4)
            draw.line([(vx, ey+6), (vx+rng.randint(-6,6), ey+er*2-6)],
                      fill=(180, 100, 120), width=1)
    # Large dim web at back
    for r in range(40, 300, 30):
        draw.ellipse([W//2-r, H//2-r//2, W//2+r, H//2+r//2],
                     outline=(80, 80, 100), width=1)
    for ang in range(0, 360, 30):
        rad = math.radians(ang)
        x2 = W//2 + int(290*math.cos(rad))
        y2 = H//2 + int(140*math.sin(rad))
        draw.line([(W//2, H//2), (x2, y2)], fill=(80, 80, 100), width=1)
    return img

def bg_torture_chamber():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (25, 15, 15), (12, 8, 8))
    stone_wall(draw, 0, H, base=(50, 40, 38))
    # Bloodstained floor
    draw.rectangle([0, H-80, W, H], fill=(45, 20, 18))
    for _ in range(30):
        bx = rng.randint(40, W-40)
        by = rng.randint(H-75, H-10)
        r = rng.randint(10, 30)
        draw.ellipse([bx-r, by-r//2, bx+r, by+r//2], fill=(60, 10, 10))
    # Chains from ceiling
    for cx in [120, 260, W-260, W-120]:
        for y in range(0, 180, 8):
            draw.ellipse([cx-4, y, cx+4, y+8], outline=(120, 120, 130), width=1)
        draw.ellipse([cx-12, 180, cx+12, 200], outline=(120, 120, 130), width=2)
    # Rack (central table)
    draw.rectangle([W//2-140, H-160, W//2+140, H-100], fill=(80, 55, 30))
    draw.rectangle([W//2-140, H-110, W//2+140, H-90], fill=(60, 40, 20))
    # Wheels on rack
    for wx in [W//2-130, W//2+130]:
        draw.ellipse([wx-20, H-140, wx+20, H-100], fill=(70, 45, 20))
        draw.ellipse([wx-12, H-132, wx+12, H-108], fill=(90, 65, 30))
    # Brazier
    draw.rectangle([W//2-200, H-80, W//2-120, H-50], fill=(60, 50, 45))
    draw.rectangle([W//2-196, H-120, W//2-124, H-80], fill=(80, 65, 55))
    for _ in range(25):
        fx = W//2-160 + rng.randint(-30, 30)
        fy = H-110 + rng.randint(-20, 0)
        r = rng.randint(3, 10)
        draw.ellipse([fx-r, fy-r, fx+r, fy+r], fill=(255, rng.randint(100, 220), 20))
    torch(draw, 80, 130)
    torch(draw, W-80, 130)
    return img

def bg_boss_chamber():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (10, 5, 18), (5, 2, 8))
    stone_wall(draw, 0, H, base=(35, 28, 45))
    for i in range(25):
        r = 80 + i*18
        draw.ellipse([W//2-r, H//2-r//2, W//2+r, H//2+r//2],
                     outline=(80, 20, 120, 80))
    draw.rectangle([W//2-60, H//2-120, W//2+60, H-80], fill=(18, 10, 28))
    draw.rectangle([W//2-70, H//2-140, W//2+70, H//2-120], fill=(22, 12, 35))
    draw.rectangle([W//2-80, H//2-160, W//2-60, H//2-120], fill=(22, 12, 35))
    draw.rectangle([W//2+60, H//2-160, W//2+80, H//2-120], fill=(22, 12, 35))
    for ex in [W//2-18, W//2+18]:
        draw.ellipse([ex-8, H//2-145, ex+8, H//2-125], fill=(180, 10, 10))
        draw.ellipse([ex-4, H//2-141, ex+4, H//2-129], fill=(255, 60, 60))
    for px in [120, W-120]:
        draw.rectangle([px-25, 0, px+25, H], fill=(25, 18, 38))
        draw.rectangle([px-28, 0, px+28, 40], fill=(30, 22, 45))
        draw.rectangle([px-28, H-40, px+28, H], fill=(30, 22, 45))
    return img

# ─── DEEP DUNGEON scenes ──────────────────────────────────────────────────────

def bg_underground_river():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (12, 10, 20), (5, 4, 10))
    # Cavern outline
    for _ in range(60):
        rx = rng.randint(0, W)
        ry = rng.randint(0, H//3)
        rr = rng.randint(20, 50)
        draw.ellipse([rx-rr, ry-rr, rx+rr, ry+rr], fill=(22, 18, 28))
    # Stone banks
    draw.rectangle([0, H//2, W, H//2+20], fill=(40, 35, 30))
    draw.rectangle([0, H-40, W, H], fill=(40, 35, 30))
    # Dark river
    for y in range(H//2+20, H-40):
        t = (y - (H//2+20)) / ((H-40) - (H//2+20))
        col = (int(5+10*t), int(3+8*t), int(10+20*t))
        draw.line([(0, y), (W, y)], fill=col)
    # Phosphorescent motes
    for _ in range(60):
        px = rng.randint(0, W)
        py = rng.randint(H//2+25, H-42)
        draw.ellipse([px-3, py-2, px+3, py+2], fill=(120, 220, 180))
        draw.ellipse([px-1, py-1, px+1, py+1], fill=(220, 255, 220))
    # Footpaths
    draw.line([(0, H//2+10), (W, H//2+10)], fill=(70, 60, 50), width=3)
    draw.line([(0, H-20), (W, H-20)], fill=(70, 60, 50), width=3)
    # Drip
    for _ in range(15):
        dx = rng.randint(40, W-40)
        dy = rng.randint(40, H//3)
        draw.line([(dx, dy), (dx, dy+rng.randint(10, 30))], fill=(100, 180, 180), width=1)
    return img

def bg_prison_cells():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (20, 18, 18), (8, 8, 10))
    stone_wall(draw, 0, H, base=(45, 42, 40))
    draw.rectangle([0, H-60, W, H], fill=(30, 25, 22))
    # Cell bars in the foreground along much of the wall
    for cell_x in [40, 230, 420, 610]:
        # Cell recess
        draw.rectangle([cell_x, 80, cell_x+160, H-70], fill=(12, 10, 10))
        # Bars
        for bx in range(cell_x+10, cell_x+160, 20):
            draw.rectangle([bx-3, 80, bx+3, H-70], fill=(60, 60, 70))
            draw.ellipse([bx-6, 75, bx+6, 90], fill=(70, 70, 80))
            draw.ellipse([bx-6, H-80, bx+6, H-65], fill=(70, 70, 80))
        # Horizontal cross-bar
        draw.rectangle([cell_x+5, H//2, cell_x+155, H//2+6], fill=(60, 60, 70))
        # Faint shape inside first cell
        if cell_x == 40:
            draw.ellipse([cell_x+50, H//2+20, cell_x+110, H//2+90], fill=(60, 40, 30))
    # Sputtering torches
    torch(draw, 150, 100)
    torch(draw, W//2, 100)
    torch(draw, W-150, 100)
    # Straw on floor
    for _ in range(30):
        sx = rng.randint(0, W)
        sy = rng.randint(H-55, H-10)
        draw.line([(sx, sy), (sx+rng.randint(-8, 8), sy+4)], fill=(160, 130, 60), width=1)
    return img

def bg_crypt():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (18, 20, 18), (8, 10, 8))
    stone_wall(draw, 0, H, base=(50, 48, 44))
    # Low ceiling arch
    for i in range(5):
        ay = 30 + i*8
        draw.arc([40+i*8, ay-20, W-40-i*8, ay+80], 180, 360, fill=(35, 32, 28), width=4)
    # Sarcophagi lining walls
    for i, sx in enumerate([60, 280, 520, 720]):
        if i == 1:
            # Opened
            draw.rectangle([sx-30, H-140, sx+100, H-80], fill=(100, 95, 85))
            draw.rectangle([sx-25, H-135, sx+95, H-85], fill=(130, 125, 115))
            draw.polygon([(sx+30, H-160), (sx+140, H-120),
                          (sx+145, H-115), (sx+35, H-155)], fill=(100, 95, 85))
        else:
            draw.rectangle([sx, H-140, sx+120, H-80], fill=(100, 95, 85))
            draw.rectangle([sx+5, H-135, sx+115, H-85], fill=(130, 125, 115))
            draw.rectangle([sx, H-160, sx+120, H-140], fill=(110, 105, 95))
            # Crosses
            draw.rectangle([sx+56, H-130, sx+64, H-95], fill=(70, 65, 55))
            draw.rectangle([sx+45, H-115, sx+75, H-107], fill=(70, 65, 55))
    # Green spectral light from open sarcophagus
    for r in range(10, 140, 8):
        alpha_col = (40, 180-r, 60)
        draw.ellipse([300-r, H-170-r//2, 420+r, H-70+r//2], outline=alpha_col)
    # Skull pile
    for _ in range(20):
        sx = rng.randint(100, W-100)
        sy = rng.randint(H-50, H-20)
        draw.ellipse([sx-8, sy-8, sx+8, sy+8], fill=(220, 210, 190))
        draw.ellipse([sx-3, sy-3, sx-1, sy+1], fill=(20, 20, 20))
        draw.ellipse([sx+1, sy-3, sx+3, sy+1], fill=(20, 20, 20))
    return img

def bg_alchemist_lab():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (30, 25, 30), (15, 12, 18))
    stone_wall(draw, 0, H, base=(55, 48, 45))
    # Long workbench
    draw.rectangle([40, H-160, W-40, H-100], fill=(80, 55, 30))
    draw.rectangle([40, H-100, W-40, H-80], fill=(60, 40, 20))
    # Shelves with jars
    for sy in [90, 160, 230]:
        draw.rectangle([80, sy, W-80, sy+12], fill=(70, 45, 20))
        # Jars
        for jx in range(100, W-100, 55):
            jh = rng.randint(30, 55)
            jc = rng.choice([(120,40,40), (40,120,40), (40,40,150),
                             (200,160,40), (120,40,150), (200,80,40),
                             (40,180,180), (180,220,40)])
            draw.rectangle([jx, sy-jh, jx+28, sy], fill=jc)
            draw.rectangle([jx+2, sy-jh+2, jx+26, sy-2], fill=tuple(min(c+60,255) for c in jc))
            draw.rectangle([jx+8, sy-jh-6, jx+20, sy-jh], fill=(60, 40, 20))
    # Broken glass on floor
    for _ in range(50):
        gx = rng.randint(40, W-40)
        gy = rng.randint(H-80, H-20)
        col = rng.choice([(120,180,180), (180,180,120), (180,120,120)])
        draw.polygon([(gx, gy), (gx+rng.randint(-6,6), gy+rng.randint(4,10)),
                      (gx+rng.randint(4,10), gy+rng.randint(-2,4))], fill=col)
    # Colored stains on floor
    for _ in range(10):
        sx = rng.randint(60, W-60)
        sy = rng.randint(H-70, H-20)
        r = rng.randint(20, 50)
        col = rng.choice([(100,40,40), (40,100,40), (40,40,120)])
        draw.ellipse([sx-r, sy-r//3, sx+r, sy+r//3], fill=col)
    # Bubbling retort on bench
    draw.ellipse([W//2-30, H-200, W//2+30, H-160], fill=(100, 200, 160))
    draw.rectangle([W//2-4, H-220, W//2+4, H-200], fill=(100, 200, 160))
    for _ in range(15):
        bx = W//2 + rng.randint(-20, 20)
        by = H-195 + rng.randint(-15, 5)
        draw.ellipse([bx-3, by-3, bx+3, by+3], fill=(180, 240, 220))
    # Open journal
    draw.rectangle([150, H-170, 260, H-130], fill=(230, 215, 180))
    draw.line([(205, H-170), (205, H-130)], fill=(140, 100, 50), width=2)
    for ly in range(H-165, H-135, 4):
        draw.line([(158, ly), (200, ly)], fill=(60, 40, 30), width=1)
        draw.line([(210, ly), (255, ly)], fill=(60, 40, 30), width=1)
    return img

def bg_ritual_chamber():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (20, 5, 10), (8, 2, 5))
    stone_wall(draw, 0, H//2, base=(40, 25, 30))
    # Floor
    draw.rectangle([0, H//2, W, H], fill=(35, 20, 25))
    # Pentagram
    cx, cy = W//2, H - 140
    r = 200
    pts = []
    for i in range(5):
        ang = math.radians(-90 + i*72)
        pts.append((cx + int(r*math.cos(ang)), cy + int(r*math.sin(ang)*0.45)))
    # Draw star lines
    order = [0, 2, 4, 1, 3, 0]
    for i in range(5):
        draw.line([pts[order[i]], pts[order[i+1]]], fill=(140, 20, 30), width=4)
    # Outer circle
    draw.ellipse([cx-r, cy-int(r*0.45), cx+r, cy+int(r*0.45)],
                 outline=(140, 20, 30), width=4)
    # Black candles at points
    for px, py in pts:
        draw.rectangle([px-4, py-30, px+4, py], fill=(15, 12, 15))
        draw.ellipse([px-5, py-38, px+5, py-26], fill=(255, 160, 40))
        draw.ellipse([px-3, py-36, px+3, py-30], fill=(255, 230, 120))
    # Altar at back
    draw.rectangle([W//2-80, H//2, W//2+80, H//2+80], fill=(50, 30, 35))
    draw.rectangle([W//2-70, H//2-15, W//2+70, H//2], fill=(60, 38, 42))
    # Eerie red glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for i in range(10):
        rr = 100 + i*28
        gd.ellipse([cx-rr, cy-rr//3, cx+rr, cy+rr//3],
                   fill=(180, 20, 30, max(0, 40-i*3)))
    img.paste(glow, mask=glow.split()[3])
    return img

def bg_demon_gate():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (35, 8, 5), (15, 3, 2))
    stone_wall(draw, 0, H, base=(60, 25, 20))
    # Fire pool at bottom
    for y in range(H-100, H):
        t = (y - (H-100)) / 100
        col = (int(120+80*t), int(40+30*t), int(10+10*t))
        draw.line([(0, y), (W, y)], fill=col)
    # Flames
    for _ in range(120):
        fx = rng.randint(0, W)
        fy = H - 100 + rng.randint(-40, 40)
        r = rng.randint(8, 25)
        col = (255, rng.randint(120, 240), rng.randint(0, 60))
        draw.ellipse([fx-r, fy-r, fx+r, fy+r//2], fill=col)
    # Great stone archway
    arch_x, arch_w, arch_h = W//2-160, 320, 340
    draw.rectangle([arch_x, H-arch_h, arch_x+arch_w, H-80], fill=(8, 4, 4))
    draw.ellipse([arch_x, H-arch_h-80, arch_x+arch_w, H-arch_h+80], fill=(8, 4, 4))
    # Arch stones with carved faces
    for i in range(0, 280, 25):
        t = i / 280
        ax = arch_x + i - 10
        ay = H - arch_h - 80 + int(80*(1-math.sin(math.pi*t)))
        draw.rectangle([ax, ay, ax+26, ay+22], fill=(90, 40, 30))
        # Eye sockets (screaming faces)
        draw.ellipse([ax+4, ay+6, ax+10, ay+12], fill=(10, 5, 5))
        draw.ellipse([ax+16, ay+6, ax+22, ay+12], fill=(10, 5, 5))
        # Mouth
        draw.ellipse([ax+8, ay+12, ax+18, ay+20], fill=(10, 5, 5))
    # Inner portal glow
    for r in range(20, 140, 10):
        t = r/140
        col = (int(180+75*t), int(50+50*t), int(20+40*t))
        draw.ellipse([W//2-r, H-220-r//2, W//2+r, H-220+r//2], fill=col)
    # Embers rising
    for _ in range(60):
        ex = rng.randint(50, W-50)
        ey = rng.randint(100, H-100)
        draw.ellipse([ex-2, ey-2, ex+2, ey+2], fill=(255, rng.randint(160,240), 60))
    return img

print("\nGenerating backgrounds...")
scenes = [
    # Village
    ("tavern.png",             bg_tavern()),
    ("town_square.png",        bg_town_square()),
    ("market_square.png",      bg_market_square()),
    ("blacksmith.png",         bg_blacksmith()),
    ("mystics_shop.png",       bg_mystics_shop()),
    ("temple.png",             bg_temple()),
    ("graveyard.png",          bg_graveyard()),
    # Forest
    ("forest.png",             bg_forest()),
    ("river_crossing.png",     bg_river_crossing()),
    ("ancient_ruins.png",      bg_ancient_ruins()),
    ("wolf_den.png",           bg_wolf_den()),
    ("deep_woods.png",         bg_deep_woods()),
    ("hidden_grove.png",       bg_hidden_grove()),
    ("wizard_tower.png",       bg_wizard_tower()),
    # Upper dungeon
    ("dungeon_entrance.png",   bg_dungeon_entrance()),
    ("dungeon_corridor.png",   bg_dungeon_corridor()),
    ("treasure_room.png",      bg_treasure_room()),
    ("guard_room.png",         bg_guard_room()),
    ("mushroom_cavern.png",    bg_mushroom_cavern()),
    ("spider_queen_lair.png",  bg_spider_queen_lair()),
    ("torture_chamber.png",    bg_torture_chamber()),
    # Deep dungeon
    ("underground_river.png",  bg_underground_river()),
    ("prison_cells.png",       bg_prison_cells()),
    ("crypt.png",              bg_crypt()),
    ("alchemist_lab.png",      bg_alchemist_lab()),
    ("ritual_chamber.png",     bg_ritual_chamber()),
    ("demon_gate.png",         bg_demon_gate()),
    ("boss_chamber.png",       bg_boss_chamber()),
]
for fname, img in scenes:
    img.save(os.path.join(BACKGROUNDS_DIR, fname))
    print(f"  OK {fname}")

print("\nAll assets generated successfully.")
print(f"  Characters : {CHARACTERS_DIR}/")
print(f"  Backgrounds: {BACKGROUNDS_DIR}/")
print(f"  UI icons   : {UI_DIR}/")
