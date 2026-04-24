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

def save_sprite(grid, filename):
    sprite_from_grid(grid).save(os.path.join(CHARACTERS_DIR, filename))
    print(f"  ✓ {filename}")

print("Generating character sprites...")
save_sprite(HERO,      "hero.png")
save_sprite(INNKEEPER, "innkeeper.png")
save_sprite(GOBLIN,    "goblin.png")
save_sprite(WIZARD,    "wizard.png")
save_sprite(SKELETON,  "skeleton.png")
save_sprite(TROLL,     "troll.png")
save_sprite(DRAGON,    "dragon.png")

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
draw_heart().save(os.path.join(UI_DIR, "heart.png")); print("  ✓ heart.png")
draw_coin().save(os.path.join(UI_DIR, "coin.png"));   print("  ✓ coin.png")
draw_sword_icon().save(os.path.join(UI_DIR, "sword.png")); print("  ✓ sword.png")

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
    for i, (fc, fh) in enumerate([(255,140,20), (255,200,40), (255,240,80)]):
        fx = x + rng.randint(-2, 2) + flicker
        draw.ellipse([fx-6+i, y-18+i*3, fx+6-i, y+i*2], fill=(*[fc//1]*3, 255)[:3])

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
    # Glow overlay on floor
    for i in range(30):
        r = 120 + i*6
        alpha = max(0, 60 - i*2)
        draw.ellipse([W//2-r, H//2+20-r//3, W//2+r, H//2+20+r//3],
                     outline=(255, 160, 40))
    # Torches
    torch(draw, 180, 120)
    torch(draw, W-180, 120)
    # Tables suggestion
    draw.rectangle([80, H-120, 280, H-90], fill=(90, 60, 25))
    draw.rectangle([W-280, H-120, W-80, H-90], fill=(90, 60, 25))
    return img

def bg_dungeon_entrance():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (25, 22, 20), (12, 10, 8))
    stone_wall(draw, 0, H, base=(55, 50, 45))
    # Archway opening
    arch_x, arch_w, arch_h = W//2-120, 240, 320
    draw.rectangle([arch_x, H-arch_h, arch_x+arch_w, H], fill=(8, 6, 5))
    draw.ellipse([arch_x, H-arch_h-60, arch_x+arch_w, H-arch_h+60], fill=(8, 6, 5))
    # Arch stonework
    for i in range(0, 200, 20):
        t = i / 200
        ax = arch_x + i - 10
        ay = H - arch_h - 60 + int(60*(1-math.sin(math.pi*t)))
        shade = rng.randint(-8, 8)
        bs = (68+shade, 62+shade, 55+shade)
        draw.rectangle([ax, ay, ax+22, ay+18], fill=bs)
    # Eerie green glow from beyond
    for i in range(20):
        r = 40 + i*8
        draw.ellipse([W//2-r, H-arch_h+40-r//4, W//2+r, H-arch_h+40+r//4],
                     outline=(30, 80, 30))
    torch(draw, arch_x-40, H-arch_h+60)
    torch(draw, arch_x+arch_w+40, H-arch_h+60)
    # Ground path
    draw.polygon([(arch_x+20, H), (arch_x+arch_w-20, H),
                  (W//2+30, H-arch_h), (W//2-30, H-arch_h)], fill=(30, 25, 20))
    return img

def bg_dungeon_corridor():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (15, 12, 10), (8, 6, 5))
    # Side walls
    stone_wall(draw, 0, H, base=(48, 43, 38))
    # Ceiling
    draw.rectangle([0, 0, W, 80], fill=(22, 18, 15))
    # Floor
    draw.rectangle([0, H-80, W, H], fill=(30, 25, 20))
    # Corridor opening (perspective)
    pts = [(W//2-30, H//2-10), (W//2+30, H//2-10),
           (W-20, H-80), (W-20, 80), (20, 80), (20, H-80)]
    # Left/right perspective walls
    draw.polygon([(20, 80), (W//2-30, H//2-10),
                  (W//2-30, H//2+10), (20, H-80)], fill=(38, 33, 28))
    draw.polygon([(W-20, 80), (W//2+30, H//2-10),
                  (W//2+30, H//2+10), (W-20, H-80)], fill=(38, 33, 28))
    # Dark end
    draw.ellipse([W//2-35, H//2-25, W//2+35, H//2+25], fill=(4, 3, 2))
    torch(draw, 220, 150)
    torch(draw, W-220, 150)
    return img

def bg_treasure_room():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (30, 25, 10), (15, 12, 5))
    stone_wall(draw, 0, H//2+60, base=(52, 47, 35))
    # Gold-tinted floor
    for y in range(H//2+60, H, 24):
        shade = rng.randint(-8, 8)
        c = (45+shade, 38+shade, 18+shade)
        draw.rectangle([0, y, W, y+22], fill=c)
    # Treasure chests
    for cx in [180, W//2, W-180]:
        draw.rectangle([cx-45, H-160, cx+45, H-90], fill=(100, 68, 22))
        draw.rectangle([cx-48, H-175, cx+48, H-155], fill=(115, 78, 28))
        draw.rectangle([cx-40, H-168, cx+40, H-158], fill=(180, 140, 40))
        draw.ellipse([cx-8, H-167, cx+8, H-153], fill=(200, 160, 20))
    # Scattered gold coins
    for _ in range(80):
        gx = rng.randint(60, W-60)
        gy = rng.randint(H-80, H-10)
        r  = rng.randint(4, 10)
        draw.ellipse([gx-r, gy-r//2, gx+r, gy+r//2], fill=(220, 175, 30))
    # Glow
    torch(draw, 120, 100)
    torch(draw, W-120, 100)
    for _ in range(30):
        gx = rng.randint(100, W-100)
        gy = rng.randint(H-120, H-20)
        draw.ellipse([gx-5, gy-3, gx+5, gy+3], fill=(255, 215, 10))
    return img

def bg_boss_chamber():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (10, 5, 18), (5, 2, 8))
    stone_wall(draw, 0, H, base=(35, 28, 45))
    # Eerie purple atmosphere
    for i in range(25):
        r = 80 + i*18
        draw.ellipse([W//2-r, H//2-r//2, W//2+r, H//2+r//2],
                     outline=(80, 20, 120, 80))
    # Throne silhouette
    draw.rectangle([W//2-60, H//2-120, W//2+60, H-80], fill=(18, 10, 28))
    draw.rectangle([W//2-70, H//2-140, W//2+70, H//2-120], fill=(22, 12, 35))
    draw.rectangle([W//2-80, H//2-160, W//2-60, H//2-120], fill=(22, 12, 35))
    draw.rectangle([W//2+60, H//2-160, W//2+80, H//2-120], fill=(22, 12, 35))
    # Red glowing eyes (high up)
    for ex in [W//2-18, W//2+18]:
        draw.ellipse([ex-8, H//2-145, ex+8, H//2-125], fill=(180, 10, 10))
        draw.ellipse([ex-4, H//2-141, ex+4, H//2-129], fill=(255, 60, 60))
    # Dark pillars
    for px in [120, W-120]:
        draw.rectangle([px-25, 0, px+25, H], fill=(25, 18, 38))
        draw.rectangle([px-28, 0, px+28, 40], fill=(30, 22, 45))
        draw.rectangle([px-28, H-40, px+28, H], fill=(30, 22, 45))
    return img

def bg_forest():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    # Night sky
    gradient(draw, 0, H//2, (8, 12, 35), (15, 25, 55))
    # Stars
    for _ in range(120):
        sx = rng.randint(0, W)
        sy = rng.randint(0, H//2)
        br = rng.randint(160, 255)
        r  = rng.randint(1, 2)
        draw.ellipse([sx-r, sy-r, sx+r, sy+r], fill=(br, br, br))
    # Moon
    draw.ellipse([W-160, 20, W-60, 120], fill=(240, 235, 200))
    draw.ellipse([W-145, 25, W-55, 115], fill=(200, 195, 160))  # crater
    draw.ellipse([W-150, 22, W-62, 118], fill=(240, 235, 200))
    # Ground
    gradient(draw, H//2, H, (18, 38, 18), (10, 22, 10))
    # Trees (background)
    for tx in range(-40, W+40, 65):
        th = rng.randint(200, 340)
        tw = rng.randint(30, 55)
        shade = rng.randint(-10, 10)
        tc = (18+shade, 38+shade, 18+shade)
        draw.rectangle([tx-tw//2, H//2-th//2, tx+tw//2, H], fill=tc)
        # Foliage layers
        for li in range(3):
            lw = tw*2 + li*20
            lh = th//3 - li*15
            ly = H//2-th//2 + li*(th//5) - 20
            fc = (22+shade, 55+shade, 22+shade)
            draw.ellipse([tx-lw//2, ly, tx+lw//2, ly+lh+40], fill=fc)
    # Moon glow on ground
    for i in range(15):
        r = 30 + i*18
        draw.ellipse([W-110-r, H//2-r//6, W-110+r, H//2+r//6],
                     outline=(200, 200, 160))
    # Clearing
    draw.ellipse([W//2-200, H//2-30, W//2+200, H//2+30], fill=(22, 48, 22))
    return img

def bg_wizard_tower():
    img  = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, 0, H, (20, 15, 35), (10, 8, 18))
    stone_wall(draw, 0, H, base=(42, 35, 55))
    # Wooden floor
    for y in range(H*2//3, H, 26):
        shade = rng.randint(-8, 8)
        c = (68+shade, 45+shade, 22+shade)
        draw.rectangle([0, y, W, y+24], fill=c)
    # Bookshelves
    for bx in [40, W-180]:
        draw.rectangle([bx, 80, bx+140, H*2//3], fill=(55, 38, 18))
        for by in range(100, H*2//3-20, 32):
            for col_i, col in enumerate([(180,30,30),(30,30,180),(30,120,30),
                                          (150,100,30),(80,30,150)]):
                bk_x = bx+8 + col_i*22
                draw.rectangle([bk_x, by, bk_x+18, by+28], fill=col)
    # Glowing orb
    for r in range(50, 0, -5):
        t = r/50
        col = (int(100+155*t), int(50+100*t), int(200+55*t))
        draw.ellipse([W//2-r, H//3-r, W//2+r, H//3+r], fill=col)
    # Arcane circles on floor
    for r in [30, 60, 90, 120]:
        draw.ellipse([W//2-r, H-60-r//3, W//2+r, H-60+r//3],
                     outline=(120, 80, 200), width=2)
    torch(draw, 200, 100)
    torch(draw, W-200, 100)
    # Candles on desk
    draw.rectangle([W//2-80, H*2//3-20, W//2+80, H*2//3], fill=(90, 65, 30))
    for cx in [W//2-50, W//2, W//2+50]:
        draw.rectangle([cx-4, H*2//3-40, cx+4, H*2//3-20], fill=(240, 230, 200))
        draw.ellipse([cx-5, H*2//3-45, cx+5, H*2//3-38], fill=(255, 180, 40))
    return img

print("\nGenerating backgrounds...")
scenes = [
    ("tavern.png",            bg_tavern()),
    ("dungeon_entrance.png",  bg_dungeon_entrance()),
    ("dungeon_corridor.png",  bg_dungeon_corridor()),
    ("treasure_room.png",     bg_treasure_room()),
    ("boss_chamber.png",      bg_boss_chamber()),
    ("forest.png",            bg_forest()),
    ("wizard_tower.png",      bg_wizard_tower()),
]
for fname, img in scenes:
    img.save(os.path.join(BACKGROUNDS_DIR, fname))
    print(f"  ✓ {fname}")

print("\nAll assets generated successfully.")
print(f"  Characters : {CHARACTERS_DIR}/")
print(f"  Backgrounds: {BACKGROUNDS_DIR}/")
print(f"  UI icons   : {UI_DIR}/")
