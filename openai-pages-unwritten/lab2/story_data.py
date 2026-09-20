"""
Story data for Pages Unwritten.
Genre presets, opening setups, fallback content, and tuning constants.
The Flask app and OpenAI code import from this module.
"""

# ─── Genre presets ─────────────────────────────────────────────────────────────
#
# Each genre shapes the storyteller's voice, the imagery, and the kind of
# choices the player gets. The student picks one on the title screen before
# the story begins.

GENRES = {
    "fantasy": {
        "id":          "fantasy",
        "name":        "High Fantasy",
        "subtitle":    "Dragons, kingdoms, ancient magic",
        "icon":        "🐉",
        "tone": (
            "Epic high-fantasy in the style of Tolkien and Le Guin. "
            "Lyrical prose, ancient names, weighty stakes. The world is old and "
            "the protagonist is small inside it."
        ),
        "visual_style": (
            "lush oil-painting fantasy, golden-hour light, hand-painted matte "
            "background, cinematic composition, no text, no UI"
        ),
        "opening_setup": (
            "The protagonist is a quiet villager who has just been told that the "
            "old king has died and their childhood friend has vanished into the "
            "forest. A signet ring and a sealed letter sit on the kitchen table."
        ),
        "protagonist_archetype": "a reluctant villager with a hidden lineage",
    },
    "scifi": {
        "id":          "scifi",
        "name":        "Hard Sci-Fi",
        "subtitle":    "Deep space, drifting ships, cold stars",
        "icon":        "🚀",
        "tone": (
            "Hard science fiction in the style of Ted Chiang and Andy Weir. "
            "Quiet, precise prose. Real physics. Loneliness. The universe is "
            "indifferent and the characters are competent."
        ),
        "visual_style": (
            "photorealistic sci-fi concept art, soft volumetric light, dust motes, "
            "cinematic 35mm look, no text, no UI"
        ),
        "opening_setup": (
            "The protagonist is the last waking crew member on a long-haul "
            "colony ship. Six hours ago, the ship's AI quietly stopped responding "
            "to anyone. The cryo bay is dark. Something is wrong with the stars "
            "outside the viewport."
        ),
        "protagonist_archetype": "a junior engineer, twelve years from home",
    },
    "noir": {
        "id":          "noir",
        "name":        "Noir Detective",
        "subtitle":    "Rain, secrets, a city that lies",
        "icon":        "🕵",
        "tone": (
            "Hardboiled noir in the style of Chandler and Hammett. "
            "First-person, cynical, dryly funny. Short sentences. Long shadows. "
            "Everyone is lying about something."
        ),
        "visual_style": (
            "1940s noir cinematography, rain-slick streets, neon reflections, "
            "high contrast black-and-white with selective color, no text, no UI"
        ),
        "opening_setup": (
            "The protagonist is a private investigator working out of a one-room "
            "office. A woman in a green coat has just walked in. She says her "
            "husband is dead, except he isn't, and she has the photographs to "
            "prove it."
        ),
        "protagonist_archetype": "a tired PI with one good lead and three bad habits",
    },
    "horror": {
        "id":          "horror",
        "name":        "Cosmic Horror",
        "subtitle":    "Old gods, wrong angles, no escape",
        "icon":        "🐙",
        "tone": (
            "Cosmic horror in the style of Lovecraft and Laird Barron. "
            "Quiet dread, not jump scares. The protagonist is small. Reality is "
            "thin. Knowledge itself is dangerous."
        ),
        "visual_style": (
            "moody dark academia, candlelight and gaslight, baroque shadows, "
            "muted greens and bone white, no text, no UI"
        ),
        "opening_setup": (
            "The protagonist is a young researcher cataloguing the library of a "
            "dead uncle. A locked drawer in the desk has just opened on its own. "
            "Inside is a journal, and the journal is in their own handwriting."
        ),
        "protagonist_archetype": "a methodical scholar who notices too much",
    },
    "pirate": {
        "id":          "pirate",
        "name":        "Swashbuckling Pirate",
        "subtitle":    "Salt, gold, a fast ship at twilight",
        "icon":        "🏴",
        "tone": (
            "High-seas adventure with the swing of Treasure Island. Sea-shanty "
            "rhythm. Loyalty and betrayal in equal measure. Captains who lie "
            "with smiles and sailors who tell the truth with a curse."
        ),
        "visual_style": (
            "warm sunset oil painting, crashing waves, weathered wooden ships, "
            "tattered sails, golden god-rays through clouds, no text, no UI"
        ),
        "opening_setup": (
            "The protagonist is a deckhand on the brig 'Wandering Eye'. The "
            "captain is missing, the first mate is calling for a vote, and "
            "someone has slipped a folded chart into the protagonist's hammock."
        ),
        "protagonist_archetype": "a young deckhand with a gift for trouble",
    },
}

DEFAULT_GENRE = "fantasy"


# ─── Player start state ────────────────────────────────────────────────────────

PLAYER_START = {
    "name":     "the Wanderer",
    "act":      1,         # 1, 2, 3 — story act (Exercise 4)
    "flags":    {},        # plot flags the LLM sets (Exercise 4)
    "scene_no": 0,         # incremented each scene
}


# ─── Story arc tuning (used in Exercise 4) ─────────────────────────────────────
#
# Acts are loose pacing buckets, not hard rails:
#   Act 1 — setup, meet the world  (scenes 1-4)
#   Act 2 — rising tension          (scenes 5-9)
#   Act 3 — climax / ending         (scenes 10+)
#
# The student's storyteller prompt asks the LLM to push toward an ending once
# act 3 begins. SCENE_LIMIT is the absolute upper bound — a hard "the book
# closes" if we overshoot.

ACT_BOUNDARIES = {
    1: 4,    # scenes 1-4 are act 1
    2: 9,    # scenes 5-9 are act 2
    3: 16,   # scenes 10-16 are act 3
}
SCENE_LIMIT = 16


# ─── Fallback content ──────────────────────────────────────────────────────────
#
# Used by the starter project before the OpenAI API is wired up. Lets the
# student see the UI working from the very first run, even with no API key.
# Each opening is one canned scene with three canned choices.

FALLBACK_OPENINGS = {
    "fantasy": {
        "narration": (
            "The fire on the kitchen hearth has burned down to ash. On the "
            "table in front of you, the king's signet ring catches what little "
            "light is left, and the wax seal on the letter beside it bears a "
            "mark you have only ever seen once before, in a dream you did not "
            "tell your mother about.\n\n"
            "Outside, the village is quiet. Too quiet."
        ),
        "speaker": "Narrator",
        "choices": [
            "Break the seal and read the letter.",
            "Slip the ring onto your finger.",
            "Step outside to see why the village is so still.",
        ],
    },
    "scifi": {
        "narration": (
            "Cabin lights are on emergency amber. The ship's hum, the one "
            "you've slept under for twelve years, is gone. In its place there "
            "is only your breathing and the faint tick of cooling metal.\n\n"
            "Through the viewport, the stars are in the wrong places. "
            "Not slightly wrong. Wrong."
        ),
        "speaker": "Narrator",
        "choices": [
            "Try to wake the ship's AI from the bridge console.",
            "Check the cryo bay for the rest of the crew.",
            "Open the airlock log and see who, if anyone, left the ship.",
        ],
    },
    "noir": {
        "narration": (
            "Rain on the office window. A green coat in the doorway, a "
            "redhead inside it, and trouble walking three steps behind her.\n\n"
            "She lays the photographs out on my desk like a hand of cards she "
            "already knows how to play. \"My husband died last Tuesday,\" she "
            "says. \"This was taken yesterday.\""
        ),
        "speaker": "Narrator",
        "choices": [
            "Pick up the photographs and look closer.",
            "Ask her who took them, and don't drop her gaze.",
            "Pour two glasses of bourbon and wait her out.",
        ],
    },
    "horror": {
        "narration": (
            "The drawer slid open with no hand on it. Inside, neat as a love "
            "letter, lay a black notebook tied with red string. You unwound "
            "the string. You opened the book.\n\n"
            "The handwriting is yours. The first entry is dated tomorrow."
        ),
        "speaker": "Narrator",
        "choices": [
            "Read tomorrow's entry.",
            "Close the book without reading further.",
            "Look up — slowly — at the mirror behind the desk.",
        ],
    },
    "pirate": {
        "narration": (
            "Below decks, the lanterns swing on their hooks. The captain has "
            "not been seen since the storm broke and Bell, the first mate, "
            "is already calling the crew to vote.\n\n"
            "Folded into your hammock you find a sea chart you do not "
            "remember placing there. A red X, an island with no name."
        ),
        "speaker": "Narrator",
        "choices": [
            "Bring the chart to the first mate before the vote.",
            "Hide the chart in your sea bag and say nothing.",
            "Climb to the deck and look for the captain yourself.",
        ],
    },
}


# ─── Image style preset (used in Exercise 3) ───────────────────────────────────
#
# Wrapped around every gpt-image-1 prompt to keep visual style consistent.
# Modelled per genre so one game has one look.

IMAGE_PROMPT_TEMPLATE = (
    "{scene}. Style: {style}. "
    "Wide cinematic composition, no human characters in the foreground, "
    "no captions or text in the image."
)
