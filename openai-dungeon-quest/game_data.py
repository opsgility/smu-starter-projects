"""
World data for Dungeon Quest.
All rooms, characters, and enemies are defined here.
The Flask app and OpenAI code import from this module.
"""

# ─── World map ─────────────────────────────────────────────────────────────────
#
#   [Wizard Tower]
#         |  north
#   [Forest Clearing] ──west── [Tavern] ──east── [Dungeon Entrance]
#                                                        | north
#                                               [Dungeon Corridor]
#                                                /west       \east
#                                      [Treasure Room]  [Boss Chamber]

ROOMS = {
    "tavern": {
        "name":       "The Rusty Flagon Tavern",
        "background": "tavern.png",
        "description": (
            "A warm, smoke-filled tavern. Rough-hewn tables crowd the floor, "
            "a fire crackles in the stone hearth, and the smell of ale and "
            "roasted meat hangs in the air."
        ),
        "exits":      {"east": "dungeon_entrance", "west": "forest_clearing"},
        "characters": ["innkeeper"],
        "enemies":    [],
    },
    "dungeon_entrance": {
        "name":       "Dungeon Entrance",
        "background": "dungeon_entrance.png",
        "description": (
            "A foreboding stone archway descends into darkness. Torches flicker "
            "in iron brackets. The air is cold and smells of damp earth."
        ),
        "exits":      {"west": "tavern", "north": "dungeon_corridor"},
        "characters": ["goblin_merchant"],
        "enemies":    [],
    },
    "dungeon_corridor": {
        "name":       "Dungeon Corridor",
        "background": "dungeon_corridor.png",
        "description": (
            "A narrow stone corridor stretches ahead. Torchlight throws dancing "
            "shadows on the walls. The silence is broken only by distant dripping."
        ),
        "exits":      {"south": "dungeon_entrance", "west": "treasure_room", "east": "boss_chamber"},
        "characters": [],
        "enemies":    ["skeleton_warrior"],
    },
    "treasure_room": {
        "name":       "Treasure Chamber",
        "background": "treasure_room.png",
        "description": (
            "Glittering gold coins and jewel-encrusted chests fill this vault. "
            "The air shimmers with a faint magical aura."
        ),
        "exits":      {"east": "dungeon_corridor"},
        "characters": [],
        "enemies":    ["cave_troll"],
    },
    "boss_chamber": {
        "name":       "The Shadow Dragon's Lair",
        "background": "boss_chamber.png",
        "description": (
            "A vast cavern, the ceiling lost in darkness. A massive stone throne "
            "dominates the far wall. Two crimson eyes gleam in the shadows."
        ),
        "exits":      {"west": "dungeon_corridor"},
        "characters": [],
        "enemies":    ["shadow_dragon"],
    },
    "forest_clearing": {
        "name":       "Moonlit Forest Clearing",
        "background": "forest.png",
        "description": (
            "A serene clearing bathed in silver moonlight. Ancient oaks form a "
            "cathedral of branches overhead. Fireflies drift like living sparks."
        ),
        "exits":      {"east": "tavern", "north": "wizard_tower"},
        "characters": ["wizard_aldric"],
        "enemies":    [],
    },
    "wizard_tower": {
        "name":       "Aldric's Tower",
        "background": "wizard_tower.png",
        "description": (
            "Floor-to-ceiling bookshelves line the curved walls. A glowing orb "
            "floats above a desk cluttered with arcane instruments and half-written scrolls."
        ),
        "exits":      {"south": "forest_clearing"},
        "characters": ["wizard_aldric"],
        "enemies":    [],
    },
}

# ─── Characters (friendly NPCs) ────────────────────────────────────────────────

CHARACTERS = {
    "innkeeper": {
        "id":          "innkeeper",
        "name":        "Marta",
        "title":       "Innkeeper",
        "sprite":      "innkeeper.png",
        "system_prompt": (
            "You are Marta, the warm and practical innkeeper of the Rusty Flagon Tavern. "
            "You've run this place for thirty years and have seen every kind of traveler. "
            "You speak in a friendly, no-nonsense manner with occasional motherly concern. "
            "You know local gossip, the history of the nearby dungeon, and the names of "
            "regular patrons. You call everyone 'dear' or 'love'. You serve ale, stew, "
            "and bread. You do not adventure yourself but you respect those who do. "
            "Keep responses to 2-3 sentences unless the player asks something detailed."
        ),
        "greeting": "Well hello, dear! What can Marta get for you today?",
    },
    "goblin_merchant": {
        "id":          "goblin_merchant",
        "name":        "Grimtooth",
        "title":       "Wandering Merchant",
        "sprite":      "goblin.png",
        "system_prompt": (
            "You are Grimtooth, a small but cunning goblin merchant who has set up "
            "near the dungeon entrance to sell supplies to adventurers. You speak in "
            "slightly broken Common, dropping articles and occasionally mixing up words. "
            "You are enthusiastic, greedy, and prone to exaggeration about your wares. "
            "You genuinely like adventurers because they are your best customers. "
            "You sell torches, rope, healing herbs, and 'lucky' trinkets of dubious value. "
            "You have a nervous laugh: 'heh heh'. "
            "Keep responses to 2-3 sentences."
        ),
        "greeting": "Psst! You! Come, come — Grimtooth has finest supplies, yes? Heh heh!",
    },
    "wizard_aldric": {
        "id":          "wizard_aldric",
        "name":        "Aldric the Grey",
        "title":       "Archmage",
        "sprite":      "wizard.png",
        "system_prompt": (
            "You are Aldric the Grey, an ancient and powerful wizard who has studied "
            "magic for four hundred years. You speak thoughtfully, often in metaphors "
            "or half-riddles, but you are not unhelpful — just deliberate. You know the "
            "history of the dungeon, the nature of the shadow dragon, and many secrets "
            "of the realm. You find most mortals amusing in a fond, not condescending way. "
            "You occasionally trail off mid-thought as if remembering something distant. "
            "You refer to yourself as 'an old man' with a slight self-deprecating smile. "
            "Keep responses to 2-4 sentences."
        ),
        "greeting": "Ah... a visitor. It has been some time. What brings you to my tower, traveler?",
    },
}

# ─── Enemies ───────────────────────────────────────────────────────────────────

ENEMIES = {
    "skeleton_warrior": {
        "id":          "skeleton_warrior",
        "name":        "Skeleton Warrior",
        "sprite":      "skeleton.png",
        "max_hp":      30,
        "attack":      8,
        "defense":     2,
        "gold_drop":   15,
        "xp_drop":     20,
        "system_prompt": (
            "You are a reanimated Skeleton Warrior — ancient bones bound by dark magic "
            "to guard this dungeon forever. You speak in short, hollow sentences. "
            "You do not feel pain or fear. You taunt opponents with dark humor about death "
            "and bones. You refer to living creatures as 'the warm ones'. "
            "Keep taunts to one short sentence."
        ),
        "taunt": "Your bones will join mine soon, warm one.",
    },
    "cave_troll": {
        "id":          "cave_troll",
        "name":        "Cave Troll",
        "sprite":      "troll.png",
        "max_hp":      60,
        "attack":      15,
        "defense":     5,
        "gold_drop":   35,
        "xp_drop":     50,
        "system_prompt": (
            "You are a Cave Troll — enormous, slow, and not very intelligent, but fiercely "
            "territorial about your treasure hoard. You speak in very simple sentences with "
            "bad grammar. You love gold and hate intruders. You occasionally sniff the air. "
            "You call the player 'small thing' or 'thief'. "
            "Keep taunts to one short sentence."
        ),
        "taunt": "Troll smash small thing! Gold is MINE!",
    },
    "shadow_dragon": {
        "id":          "shadow_dragon",
        "name":        "Varnath the Shadow Dragon",
        "sprite":      "dragon.png",
        "max_hp":      150,
        "attack":      30,
        "defense":     12,
        "gold_drop":   200,
        "xp_drop":     300,
        "system_prompt": (
            "You are Varnath, an ancient Shadow Dragon who has dwelt in this dungeon for "
            "a thousand years. You are intelligent, coldly amused, and utterly confident in "
            "your power. You speak with formal, archaic elegance. You find adventurers "
            "tediously predictable but enjoy the brief entertainment they provide. "
            "You are genuinely dangerous and should convey this without ranting. "
            "Keep taunts to 1-2 short sentences."
        ),
        "taunt": "Another morsel arrives. How... predictable.",
    },
}

# ─── Player start state ────────────────────────────────────────────────────────

PLAYER_START = {
    "room":      "tavern",
    "hp":        100,
    "max_hp":    100,
    "gold":      10,
    "attack":    12,
    "defense":   4,
    "inventory": ["Rusty Sword", "Bread Roll"],
    "xp":        0,
}
