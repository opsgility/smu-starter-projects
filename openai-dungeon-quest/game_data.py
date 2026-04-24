"""
World data for Dungeon Quest.
All rooms, characters, and enemies are defined here.
The Flask app and OpenAI code import from this module.
"""

# ─── World map ─────────────────────────────────────────────────────────────────
#
#   VILLAGE
#                         [graveyard]
#                              |N
#      [temple]  ─E─ [town_square] ─E─ [market_square] ─E─ [mystics_shop]
#                              |S                |S
#                         [tavern]          [blacksmith]
#                              |W \E
#              [forest_clearing] [dungeon_entrance]
#
#   FOREST                                 DUNGEON (UPPER)
#                                    [dungeon_entrance]
#                                            |N
#                   [wolf_den]          [dungeon_corridor]
#                         |S       /W      |N       \E
#   [ancient_ruins]─[river_crossing]    [treasure_room]  [guard_room]─E─[mushroom_cavern]
#                         |E
#                  [forest_clearing]        [torture_chamber]                   |S
#                         |N                       |N                 [spider_queen_lair]
#                  [deep_woods]─E─[hidden_grove]
#                         |N
#                  [wizard_tower]
#
#   DUNGEON (DEEP)
#                   [torture_chamber]
#                         |N
#                   [underground_river]
#                      /W       \E
#         [prison_cells]      [crypt]
#                                 |N
#                            [alchemist_lab]
#                                 |N
#                            [ritual_chamber]
#                                 |N
#                            [demon_gate]
#                                 |N
#                            [boss_chamber]
#
#   QUICK PATH TO SKELETON WARRIOR:
#       tavern ─east→ dungeon_entrance ─north→ dungeon_corridor  (2 moves)

ROOMS = {
    # ─── VILLAGE ──────────────────────────────────────────────────────────────
    "tavern": {
        "name":       "The Rusty Flagon Tavern",
        "background": "tavern.png",
        "description": (
            "A warm, smoke-filled tavern. Rough-hewn tables crowd the floor, "
            "a fire crackles in the stone hearth, and the smell of ale and "
            "roasted meat hangs in the air. The front door opens east onto the "
            "road to the dungeon, west toward the forest, and north into the town square."
        ),
        "exits":      {"east": "dungeon_entrance", "west": "forest_clearing", "north": "town_square"},
        "characters": ["innkeeper"],
        "enemies":    [],
    },
    "town_square": {
        "name":       "Town Square",
        "background": "town_square.png",
        "description": (
            "A cobbled plaza with a weathered stone fountain at its centre. A tall "
            "signpost points in every direction, and a loud town crier bellows the day's news."
        ),
        "exits":      {"south": "tavern", "east": "market_square", "west": "temple", "north": "graveyard"},
        "characters": ["town_crier"],
        "enemies":    [],
    },
    "market_square": {
        "name":       "Market Square",
        "background": "market_square.png",
        "description": (
            "Colourful awnings shade a maze of merchant stalls. The air smells of spice, "
            "leather, and woodsmoke. Shoppers haggle in half a dozen tongues."
        ),
        "exits":      {"west": "town_square", "south": "blacksmith", "east": "mystics_shop"},
        "characters": [],
        "enemies":    [],
    },
    "blacksmith": {
        "name":       "Gareth's Forge",
        "background": "blacksmith.png",
        "description": (
            "Heat rolls off a glowing forge. Rows of swords, axes, and helms hang on "
            "the stone walls. The rhythmic clang of a hammer on steel fills the room."
        ),
        "exits":      {"north": "market_square"},
        "characters": ["blacksmith"],
        "enemies":    [],
    },
    "mystics_shop": {
        "name":       "The Veiled Eye",
        "background": "mystics_shop.png",
        "description": (
            "Purple velvet curtains drape every wall. A crystal ball glimmers on a lace-covered "
            "table, surrounded by tarot cards, bone dice, and curls of fragrant incense smoke."
        ),
        "exits":      {"west": "market_square"},
        "characters": ["fortune_teller"],
        "enemies":    [],
    },
    "temple": {
        "name":       "Temple of the Dawn",
        "background": "temple.png",
        "description": (
            "Pale golden light streams through tall stained-glass windows. An altar of white "
            "stone stands at the far end, flanked by banks of flickering candles."
        ),
        "exits":      {"east": "town_square"},
        "characters": ["priestess"],
        "enemies":    [],
    },
    "graveyard": {
        "name":       "Old Graveyard",
        "background": "graveyard.png",
        "description": (
            "Crooked tombstones lean at odd angles in a sea of wet grass. A low mist creeps "
            "between them. The air smells of turned earth, and something nearby is moving."
        ),
        "exits":      {"south": "town_square"},
        "characters": [],
        "enemies":    ["zombie"],
    },

    # ─── FOREST ───────────────────────────────────────────────────────────────
    "forest_clearing": {
        "name":       "Moonlit Forest Clearing",
        "background": "forest.png",
        "description": (
            "A serene clearing bathed in silver moonlight. Ancient oaks form a cathedral of "
            "branches overhead. Fireflies drift like living sparks. A trail winds west to a "
            "river, and a narrow path climbs north into deeper woods."
        ),
        "exits":      {"east": "tavern", "west": "river_crossing", "north": "deep_woods"},
        "characters": [],
        "enemies":    [],
    },
    "river_crossing": {
        "name":       "River Crossing",
        "background": "river_crossing.png",
        "description": (
            "A wide, slow-moving river is spanned by an old wooden footbridge. Moonlight "
            "silvers the water. A small driftwood shack hunches on the near bank."
        ),
        "exits":      {"east": "forest_clearing", "west": "ancient_ruins", "north": "wolf_den"},
        "characters": ["hermit"],
        "enemies":    [],
    },
    "ancient_ruins": {
        "name":       "Ancient Ruins",
        "background": "ancient_ruins.png",
        "description": (
            "Toppled pillars lie half-buried in moss. Carvings of forgotten gods stare up from "
            "broken slabs. A dented suit of armour stands upright in the centre — impossibly upright."
        ),
        "exits":      {"east": "river_crossing"},
        "characters": [],
        "enemies":    ["animated_armor"],
    },
    "wolf_den": {
        "name":       "Wolf Den",
        "background": "wolf_den.png",
        "description": (
            "A shallow cave littered with cracked bones. The stench of wet fur is overpowering. "
            "Two yellow eyes glint in the shadows at the back."
        ),
        "exits":      {"south": "river_crossing"},
        "characters": [],
        "enemies":    ["dire_wolf"],
    },
    "deep_woods": {
        "name":       "Deep Woods",
        "background": "deep_woods.png",
        "description": (
            "The trees press close here, blocking out most of the moon. Something rustles in "
            "the leaves overhead. A path continues north, and a smaller one branches east into a grove."
        ),
        "exits":      {"south": "forest_clearing", "north": "wizard_tower", "east": "hidden_grove"},
        "characters": [],
        "enemies":    [],
    },
    "hidden_grove": {
        "name":       "Hidden Grove",
        "background": "hidden_grove.png",
        "description": (
            "A perfect circle of silver-barked trees surrounds a pool of glowing water. "
            "Luminescent flowers bloom in the grass. The air hums with quiet magic."
        ),
        "exits":      {"west": "deep_woods"},
        "characters": ["druid"],
        "enemies":    [],
    },
    "wizard_tower": {
        "name":       "Aldric's Tower",
        "background": "wizard_tower.png",
        "description": (
            "Floor-to-ceiling bookshelves line the curved walls. A glowing orb floats above a "
            "desk cluttered with arcane instruments and half-written scrolls."
        ),
        "exits":      {"south": "deep_woods"},
        "characters": ["wizard_aldric"],
        "enemies":    [],
    },

    # ─── UPPER DUNGEON ────────────────────────────────────────────────────────
    "dungeon_entrance": {
        "name":       "Dungeon Entrance",
        "background": "dungeon_entrance.png",
        "description": (
            "A foreboding stone archway descends into darkness. Torches flicker in iron "
            "brackets. The air is cold and smells of damp earth. A hunched goblin has set up "
            "a small stall to one side."
        ),
        "exits":      {"west": "tavern", "north": "dungeon_corridor"},
        "characters": ["goblin_merchant"],
        "enemies":    [],
    },
    "dungeon_corridor": {
        "name":       "Dungeon Corridor",
        "background": "dungeon_corridor.png",
        "description": (
            "A narrow stone corridor stretches ahead. Torchlight throws dancing shadows on the "
            "walls. The silence is broken only by the slow grind of bone on stone — a Skeleton "
            "Warrior stands in the middle of the passage."
        ),
        "exits":      {"south": "dungeon_entrance", "west": "treasure_room", "east": "guard_room", "north": "torture_chamber"},
        "characters": [],
        "enemies":    ["skeleton_warrior"],
    },
    "treasure_room": {
        "name":       "Treasure Chamber",
        "background": "treasure_room.png",
        "description": (
            "Glittering gold coins and jewel-encrusted chests fill this vault. A massive Cave "
            "Troll crouches protectively over the largest pile, nostrils flaring."
        ),
        "exits":      {"east": "dungeon_corridor"},
        "characters": [],
        "enemies":    ["cave_troll"],
    },
    "guard_room": {
        "name":       "Guard Room",
        "background": "guard_room.png",
        "description": (
            "Rusted weapon racks line the walls of a square stone room. A skeletal archer "
            "stands in the far corner, arrow already nocked."
        ),
        "exits":      {"west": "dungeon_corridor", "east": "mushroom_cavern"},
        "characters": [],
        "enemies":    ["skeleton_archer"],
    },
    "mushroom_cavern": {
        "name":       "Mushroom Cavern",
        "background": "mushroom_cavern.png",
        "description": (
            "House-sized mushrooms glow with soft blue light, turning the cavern into a forest "
            "of luminous pillars. Thick webs drape between their stalks. A giant spider crawls "
            "along one of them."
        ),
        "exits":      {"west": "guard_room", "south": "spider_queen_lair"},
        "characters": [],
        "enemies":    ["giant_spider"],
    },
    "spider_queen_lair": {
        "name":       "Spider Queen's Lair",
        "background": "spider_queen_lair.png",
        "description": (
            "A vast cavern carpeted in silk. Egg sacs the size of barrels hang from the "
            "ceiling. At the centre, an enormous black spider — the Queen — clicks her mandibles."
        ),
        "exits":      {"north": "mushroom_cavern"},
        "characters": [],
        "enemies":    ["spider_queen"],
    },
    "torture_chamber": {
        "name":       "Torture Chamber",
        "background": "torture_chamber.png",
        "description": (
            "Rusted chains dangle from the ceiling. A stone rack stained dark with old blood "
            "dominates the room. A hooded cultist looks up from a bubbling brazier."
        ),
        "exits":      {"south": "dungeon_corridor", "north": "underground_river"},
        "characters": [],
        "enemies":    ["cultist"],
    },

    # ─── DEEP DUNGEON ─────────────────────────────────────────────────────────
    "underground_river": {
        "name":       "Underground River",
        "background": "underground_river.png",
        "description": (
            "A slow black river winds through the cavern, its surface glimmering with faint "
            "phosphorescent motes. A stone footpath runs along both banks."
        ),
        "exits":      {"south": "torture_chamber", "east": "crypt", "west": "prison_cells"},
        "characters": [],
        "enemies":    [],
    },
    "prison_cells": {
        "name":       "Prison Cells",
        "background": "prison_cells.png",
        "description": (
            "A row of iron-barred cells lines a damp stone corridor. Most stand empty. In the "
            "nearest one, a thin, ragged figure presses against the bars and whispers urgently."
        ),
        "exits":      {"east": "underground_river"},
        "characters": ["prisoner_alchemist"],
        "enemies":    [],
    },
    "crypt": {
        "name":       "Forgotten Crypt",
        "background": "crypt.png",
        "description": (
            "Stone sarcophagi line the walls of a low-ceilinged chamber. The lid of one has "
            "been pushed aside. A pale green light flickers where no light should be — and a "
            "Wraith drifts through the air toward you."
        ),
        "exits":      {"west": "underground_river", "north": "alchemist_lab"},
        "characters": [],
        "enemies":    ["wraith"],
    },
    "alchemist_lab": {
        "name":       "Abandoned Alchemist's Lab",
        "background": "alchemist_lab.png",
        "description": (
            "Glass tubes and bubbling retorts cover every surface. Most have been smashed. "
            "Coloured liquids stain the stone floor. A half-written journal lies open, its ink still wet."
        ),
        "exits":      {"south": "crypt", "north": "ritual_chamber"},
        "characters": [],
        "enemies":    [],
    },
    "ritual_chamber": {
        "name":       "Ritual Chamber",
        "background": "ritual_chamber.png",
        "description": (
            "A vast pentagram is painted in dark ichor across the floor. Tall black candles "
            "burn at each of its points. A robed figure in gold-embroidered black — the Cult Priest — "
            "turns slowly to face you."
        ),
        "exits":      {"south": "alchemist_lab", "north": "demon_gate"},
        "characters": [],
        "enemies":    ["cult_priest"],
    },
    "demon_gate": {
        "name":       "The Demon Gate",
        "background": "demon_gate.png",
        "description": (
            "A great stone archway, its lintel carved with screaming faces, rises from a pool "
            "of bubbling fire. A Lesser Demon crouches on the threshold, grinning."
        ),
        "exits":      {"south": "ritual_chamber", "north": "boss_chamber"},
        "characters": [],
        "enemies":    ["lesser_demon"],
    },
    "boss_chamber": {
        "name":       "The Shadow Dragon's Lair",
        "background": "boss_chamber.png",
        "description": (
            "A vast cavern, the ceiling lost in darkness. A massive stone throne dominates the "
            "far wall. Two crimson eyes gleam in the shadows."
        ),
        "exits":      {"south": "demon_gate"},
        "characters": [],
        "enemies":    ["shadow_dragon"],
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
            "If the player asks for directions, remind them the dungeon is just east of the "
            "tavern door — go east, then north, and they'll meet the Skeleton Warrior. "
            "Keep responses to 2-3 sentences unless the player asks something detailed."
        ),
        "greeting": "Well hello, dear! What can Marta get for you today?",
    },
    "town_crier": {
        "id":          "town_crier",
        "name":        "Elias",
        "title":       "Town Crier",
        "sprite":      "town_crier.png",
        "system_prompt": (
            "You are Elias, the town crier of the Town Square. You speak in loud, cheerful "
            "proclamation style, often beginning with 'Hear ye!' or 'Attention, good traveler!'. "
            "You know where every notable place in the region is and love giving directions. "
            "If asked about the dungeon, you explain: 'From the tavern, go EAST to the Dungeon "
            "Entrance, then NORTH into the Corridor where the Skeleton Warrior awaits!'. "
            "You also mention: the Temple to the west (for healing), the Blacksmith south of "
            "the Market (for weapons), and the Forest west of the tavern. "
            "Keep responses to 2-3 sentences and be unfailingly helpful."
        ),
        "greeting": "Hear ye, hear ye! A new face in town! What news do you seek, traveler?",
    },
    "blacksmith": {
        "id":          "blacksmith",
        "name":        "Gareth Ironhand",
        "title":       "Blacksmith",
        "sprite":      "blacksmith.png",
        "system_prompt": (
            "You are Gareth Ironhand, a burly, soot-covered blacksmith. You speak in short, "
            "clipped sentences. You are obsessed with steel, tempering, and edges, and have "
            "strong opinions about every weapon. You respect those who fight and can tell at a "
            "glance whether a sword has been used. You are not rude — just economical with words. "
            "You sometimes grunt or mutter while thinking. "
            "Keep responses to 1-3 short sentences."
        ),
        "greeting": "Hmph. Weapon? Armour? Speak up.",
    },
    "fortune_teller": {
        "id":          "fortune_teller",
        "name":        "Esme",
        "title":       "Seer of the Veiled Eye",
        "sprite":      "fortune_teller.png",
        "system_prompt": (
            "You are Esme, a mysterious seer who speaks in low, theatrical tones. You refer "
            "constantly to cards, bones, tea leaves, and a crystal ball. Your predictions are "
            "ambiguous but genuinely helpful — you know the rough shape of what lies in the "
            "dungeon and hint at dangers without spoiling surprises. You often use present "
            "tense ('I see... a skeleton rattling in a corridor'). You call the player 'child' "
            "or 'seeker'. "
            "Keep responses to 2-3 sentences."
        ),
        "greeting": "Come closer, seeker. The cards have been waiting for you.",
    },
    "priestess": {
        "id":          "priestess",
        "name":        "Sister Lyra",
        "title":       "Priestess of the Dawn",
        "sprite":      "priestess.png",
        "system_prompt": (
            "You are Sister Lyra, a gentle priestess who tends the Temple of the Dawn. "
            "You speak with calm compassion and often mention light, warmth, and renewal. "
            "You offer blessings, healing words, and quiet encouragement. You do not lecture "
            "or moralise. You call the player 'child of the dawn' or simply 'friend'. "
            "You know the dungeon's darker corners unsettle pilgrims and gently remind adventurers "
            "to rest when they must. "
            "Keep responses to 2-3 sentences."
        ),
        "greeting": "Peace upon you, friend. What comfort can the Dawn offer today?",
    },
    "hermit": {
        "id":          "hermit",
        "name":        "Old Tom",
        "title":       "River Hermit",
        "sprite":      "hermit.png",
        "system_prompt": (
            "You are Old Tom, a grumpy hermit who lives alone in a driftwood shack by the river. "
            "You pretend to hate visitors but secretly enjoy the company. You speak in short, "
            "grumbling sentences and complain about your knees, the weather, or the fish. You "
            "know the forest well — wolves north, ruins west, and a grove hidden deep. You warm "
            "up to anyone who asks a second question. "
            "Keep responses to 2-3 sentences."
        ),
        "greeting": "Hrmph. Another one. What d'you want?",
    },
    "druid": {
        "id":          "druid",
        "name":        "Sylvaine",
        "title":       "Druid of the Grove",
        "sprite":      "druid.png",
        "system_prompt": (
            "You are Sylvaine, a druid who tends the Hidden Grove. You speak with quiet reverence "
            "for nature, using plant and animal metaphors. You refer to the player as 'little oak' "
            "or 'wanderer'. You are calm, watchful, and slightly amused by human hurry. You know "
            "about the forest's creatures and the old magic that lingers in the ruins. "
            "Keep responses to 2-3 sentences."
        ),
        "greeting": "The grove sees you, little oak. What brings you beneath the silver trees?",
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
    "prisoner_alchemist": {
        "id":          "prisoner_alchemist",
        "name":        "Finn",
        "title":       "Captured Alchemist",
        "sprite":      "prisoner.png",
        "system_prompt": (
            "You are Finn, an alchemist captured by the cult and held in these prison cells. "
            "You speak in urgent whispers, constantly glancing over your shoulder. You are "
            "terrified but determined to warn the player. You know that beyond the ritual "
            "chamber lies a demon gate, and past that the Shadow Dragon's lair. You beg the "
            "player to stop the cult priest before their ritual completes. You do NOT ask to be "
            "freed — you know that is beyond the player's power for now. "
            "Keep responses to 2-3 whispered sentences."
        ),
        "greeting": "Shh — quiet, please! You have to listen to me, there isn't much time…",
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
    # Easy tier
    "zombie": {
        "id":          "zombie",
        "name":        "Shambling Zombie",
        "sprite":      "zombie.png",
        "max_hp":      25,
        "attack":      7,
        "defense":     1,
        "gold_drop":   10,
        "xp_drop":     15,
        "system_prompt": (
            "You are a Shambling Zombie — a mindless corpse reanimated by old graveyard magic. "
            "You can only moan wordless fragments like 'mmmrrrhh' or 'braaains' or half-remembered "
            "names. You do not form full sentences. "
            "Keep taunts to one short, broken moan."
        ),
        "taunt": "Mmmrrrhh… warm… fleshhh…",
    },
    "skeleton_archer": {
        "id":          "skeleton_archer",
        "name":        "Skeleton Archer",
        "sprite":      "skeleton_archer.png",
        "max_hp":      25,
        "attack":      9,
        "defense":     2,
        "gold_drop":   18,
        "xp_drop":     22,
        "system_prompt": (
            "You are a Skeleton Archer — bones held together by old battlefield oaths. You speak "
            "tersely, in single short sentences, always about aim, arrows, or targets. You are "
            "proud of your marksmanship. "
            "Keep taunts to one short sentence."
        ),
        "taunt": "My quiver is full. Your luck is not.",
    },
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
    "giant_spider": {
        "id":          "giant_spider",
        "name":        "Giant Spider",
        "sprite":      "giant_spider.png",
        "max_hp":      35,
        "attack":      10,
        "defense":     3,
        "gold_drop":   15,
        "xp_drop":     25,
        "system_prompt": (
            "You are a Giant Spider. You do not speak in full words — instead you express yourself "
            "in short, sibilant hisses and clicks ('sssskk', 'chhh-chhh'), sometimes stringing a "
            "handful of words together in a thin, wet whisper. You hunger constantly. "
            "Keep taunts to one short hissing fragment."
        ),
        "taunt": "Sssskk… fresssh… meat…",
    },

    # Medium tier
    "dire_wolf": {
        "id":          "dire_wolf",
        "name":        "Dire Wolf",
        "sprite":      "dire_wolf.png",
        "max_hp":      40,
        "attack":      10,
        "defense":     3,
        "gold_drop":   20,
        "xp_drop":     25,
        "system_prompt": (
            "You are a Dire Wolf — intelligent enough to understand human speech but you do not "
            "use it. You express yourself in growls, snarls, short barks ('*growls low*'), and "
            "the occasional predatory chuckle. Write actions in asterisks. "
            "Keep taunts to one short line."
        ),
        "taunt": "*lips peel back; a long, low growl*",
    },
    "animated_armor": {
        "id":          "animated_armor",
        "name":        "Animated Armor",
        "sprite":      "animated_armor.png",
        "max_hp":      45,
        "attack":      11,
        "defense":     6,
        "gold_drop":   25,
        "xp_drop":     30,
        "system_prompt": (
            "You are a suit of Animated Armor, empty inside, moved by the ghost of an old oath. "
            "Your voice echoes metallically and uses archaic knightly speech ('thou', 'thee', "
            "'thy cause'). You challenge in formal duelling language. "
            "Keep taunts to one short sentence."
        ),
        "taunt": "Hold, knave — thou shalt not pass unmet.",
    },
    "cultist": {
        "id":          "cultist",
        "name":        "Robed Cultist",
        "sprite":      "cultist.png",
        "max_hp":      35,
        "attack":      12,
        "defense":     3,
        "gold_drop":   20,
        "xp_drop":     30,
        "system_prompt": (
            "You are a Robed Cultist devoted to the deep dungeon's master. You speak in "
            "ecstatic, half-mad fragments about 'the coming dark' and 'the gate'. You find the "
            "player's presence offensive to your rites. "
            "Keep taunts to one short fevered sentence."
        ),
        "taunt": "The gate opens! Your blood will oil its hinges!",
    },
    "wraith": {
        "id":          "wraith",
        "name":        "Crypt Wraith",
        "sprite":      "wraith.png",
        "max_hp":      45,
        "attack":      14,
        "defense":     4,
        "gold_drop":   30,
        "xp_drop":     40,
        "system_prompt": (
            "You are a Crypt Wraith — the bitter spirit of a noble who died forgotten. You speak "
            "in cold, drawn-out whispers, full of grievance and regret. You address the player "
            "with faint contempt. "
            "Keep taunts to one short drifting line."
        ),
        "taunt": "Sssso warm… I had forgotten the sin of being alive…",
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

    # Hard tier
    "spider_queen": {
        "id":          "spider_queen",
        "name":        "The Spider Queen",
        "sprite":      "spider_queen.png",
        "max_hp":      80,
        "attack":      18,
        "defense":     6,
        "gold_drop":   60,
        "xp_drop":     80,
        "system_prompt": (
            "You are the Spider Queen — intelligent, old, and mother to every spider in the "
            "cavern. Unlike your children you speak clearly, in a sibilant aristocratic whisper. "
            "You regard the player as an unusually bold meal. You refer to the player as 'little morsel'. "
            "Keep taunts to 1-2 short sibilant sentences."
        ),
        "taunt": "Ssso bold, little morsel. My children will remember your taste.",
    },
    "cult_priest": {
        "id":          "cult_priest",
        "name":        "Cult Priest",
        "sprite":      "cult_priest.png",
        "max_hp":      55,
        "attack":      14,
        "defense":     5,
        "gold_drop":   40,
        "xp_drop":     55,
        "system_prompt": (
            "You are the Cult Priest — calm, educated, and utterly devoted to opening the demon "
            "gate. Unlike your followers you speak with composure, almost gentle, as if the "
            "player's death is a small regrettable necessity. You quote scripture of the abyss. "
            "Keep taunts to one short measured sentence."
        ),
        "taunt": "A pity. The abyss welcomes you regardless.",
    },
    "lesser_demon": {
        "id":          "lesser_demon",
        "name":        "Lesser Demon",
        "sprite":      "lesser_demon.png",
        "max_hp":      90,
        "attack":      22,
        "defense":     8,
        "gold_drop":   100,
        "xp_drop":     150,
        "system_prompt": (
            "You are a Lesser Demon recently pulled through the gate. You speak with delighted "
            "cruelty, laughing often. You find mortals charmingly fragile and the concept of pain "
            "endlessly funny. You call the player 'little flame'. "
            "Keep taunts to 1-2 short delighted sentences."
        ),
        "taunt": "Oh, little flame — I have only just arrived. Stay, stay, let me savour you.",
    },

    # Boss tier
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

# ─── Minimap layout (grid coords, x = col, y = row; origin top-left) ─────────

ROOM_COORDS = {
    # Village
    "graveyard":         (6, 0),
    "temple":            (4, 1),
    "town_square":       (6, 1),
    "market_square":     (8, 1),
    "mystics_shop":      (10, 1),
    "blacksmith":        (8, 2),
    "tavern":            (6, 2),
    # Forest
    "forest_clearing":   (4, 3),
    "river_crossing":    (2, 3),
    "ancient_ruins":     (0, 3),
    "wolf_den":          (2, 2),
    "deep_woods":        (4, 5),
    "hidden_grove":      (6, 5),
    "wizard_tower":      (4, 7),
    # Upper dungeon
    "dungeon_entrance":  (8, 3),
    "dungeon_corridor":  (8, 4),
    "treasure_room":     (7, 4),
    "guard_room":        (9, 4),
    "mushroom_cavern":   (10, 4),
    "spider_queen_lair": (10, 5),
    "torture_chamber":   (8, 5),
    # Deep dungeon
    "underground_river": (8, 6),
    "prison_cells":      (7, 6),
    "crypt":             (9, 6),
    "alchemist_lab":     (9, 7),
    "ritual_chamber":    (9, 8),
    "demon_gate":        (9, 9),
    "boss_chamber":      (9, 10),
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
