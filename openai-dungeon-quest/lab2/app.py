"""
Dungeon Quest — Flask server (Lab 2 starter).

Lab 1 work is already wired up below:
    ✓ Exercise 1 — OpenAI client + GM system prompt + /api/action with ROOM_CHANGE regex
    ✓ Exercise 2 — /api/talk with per-character histories

In Lab 2 you'll add:
    Exercise 3 — Make combat actually hurt (damage + narrator + taunt + defeat)
    Exercise 4 — Structured output (JSON mode replaces the regex parser)

Run:
    python app.py

Then open the URL shown in the VS Code Ports panel.
"""
import copy, hashlib, json, os, re
from flask import Flask, render_template, request, jsonify, session
from game_data import ROOMS, CHARACTERS, ENEMIES, PLAYER_START, ROOM_COORDS

# ─── Exercise 1 - Part 1: Set Up the OpenAI Client (✓ Completed in Lab 1) ─────
from openai import OpenAI

client = OpenAI()
# ──────────────────────────────────────────────────────────────────────────────

app = Flask(__name__)
app.secret_key = "dungeon-quest-dev-key"

AUDIO_DIR = os.path.join("static", "generated", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)


# ─── Helpers ───────────────────────────────────────────────────────────────────

def current_room():
    return ROOMS[session["player"]["room"]]

def reset_session():
    session["player"]             = copy.deepcopy(PLAYER_START)
    session["game_history"]       = []   # [{role, content}]  — game master thread
    session["character_histories"] = {}  # {char_id: [{role, content}]}
    session["combat"]             = None # {enemy_id, enemy_hp} or None
    session["visited"]            = [PLAYER_START["room"]]


# ─── Exercise 1 - Part 2: Build the System Prompt (✓ Completed in Lab 1) ──────
def build_gm_system_prompt():
    room   = current_room()
    player = session["player"]

    room_chars   = [CHARACTERS[c]["name"] for c in room["characters"] if c in CHARACTERS]
    room_enemies = [ENEMIES[e]["name"]    for e in room["enemies"]    if e in ENEMIES]
    exits        = ", ".join(f"{d} -> {dest}" for d, dest in room["exits"].items())

    world_summary = []
    for rid, rdata in ROOMS.items():
        world_summary.append(f"  {rid}: {rdata['name']} (exits: {', '.join(rdata['exits'].keys())})")

    return f"""You are the game master for Dungeon Quest, a dark-fantasy text RPG.

WORLD MAP:
{chr(10).join(world_summary)}

CURRENT ROOM: {room['name']} ({session['player']['room']})
{room['description']}
Exits: {exits}
Characters here: {', '.join(room_chars) if room_chars else 'none'}
Enemies here: {', '.join(room_enemies) if room_enemies else 'none'}

PLAYER STATE:
  HP: {player['hp']} / {player['max_hp']}
  Gold: {player['gold']}
  Inventory: {', '.join(player['inventory'])}

RULES:
- Respond in 2-4 vivid sentences. Be atmospheric and concise.
- If the player moves and the exit exists, narrate it and end with: ROOM_CHANGE:<room_id>
  Example: "You descend the stone steps... ROOM_CHANGE:dungeon_corridor"
- If the exit does not exist, say so.
- Keep descriptions atmospheric: torchlight, echoes, smells, sounds."""
# ──────────────────────────────────────────────────────────────────────────────


# ─── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/start", methods=["POST"])
def start():
    """Reset and return the opening scene."""
    reset_session()
    room = current_room()
    exits_str = ", ".join(room["exits"].keys()) or "none"
    return jsonify({
        "narrative": (
            f"You stand at the entrance of {room['name']}.\n\n"
            f"{room['description']}\n\n"
            f"Exits: {exits_str}.  (Click an exit badge or type `go east`, `go north`, etc.)\n\n"
            "Quick path to the Skeleton Warrior: from the tavern, go EAST to the "
            "Dungeon Entrance, then NORTH into the Corridor.\n\n"
            "Type 'help' to see all commands."
        ),
        "room":       session["player"]["room"],
        "room_data":  _room_state(),
        "map_layout": _map_layout(),
        "player":     session["player"],
        "combat":     None,
    })


# ─── Exercise 1 - Part 3: Wire Up the API Call (✓ Completed in Lab 1) ────────
@app.route("/api/action", methods=["POST"])
def action():
    data         = request.get_json()
    player_input = data.get("input", "").strip()

    if not player_input:
        return jsonify({"error": "No input provided"}), 400

    # Step 1: Add the player's message to history
    session["game_history"].append({"role": "user", "content": player_input})

    # Step 2: Build the full messages list
    messages = [
        {"role": "system", "content": build_gm_system_prompt()}
    ] + session["game_history"]

    # Step 3: Call the API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300,
        temperature=0.8,
    )

    raw_reply = response.choices[0].message.content.strip()

    # Step 4: Save the reply to history
    session["game_history"].append({"role": "assistant", "content": raw_reply})

    # Step 5: Check for a room change signal
    narrative = raw_reply
    match = re.search(r"ROOM_CHANGE:(\w+)", raw_reply)
    if match:
        new_room_id = match.group(1)
        if new_room_id in ROOMS:
            session["player"]["room"] = new_room_id
        narrative = re.sub(r"\s*ROOM_CHANGE:\w+", "", narrative).strip()

    # Keep history from growing forever
    if len(session["game_history"]) > 20:
        session["game_history"] = session["game_history"][-20:]

    return jsonify({
        "narrative": narrative,
        "room":      session["player"]["room"],
        "room_data": _room_state(),
        "player":    session["player"],
        "combat":    session.get("combat"),
    })
# ──────────────────────────────────────────────────────────────────────────────


# ─── Exercise 2 - Part 1: Wire Up the Talk Endpoint (✓ Completed in Lab 1) ───
@app.route("/api/talk", methods=["POST"])
def talk():
    data         = request.get_json()
    character_id = data.get("character_id", "")
    message      = data.get("message", "").strip()

    character = CHARACTERS.get(character_id)
    if not character:
        return jsonify({"error": "Unknown character"}), 404

    # Step 1: Load or create this character's private history
    if "character_histories" not in session:
        session["character_histories"] = {}
    if character_id not in session["character_histories"]:
        session["character_histories"][character_id] = []

    history = session["character_histories"][character_id]

    # Step 2: Append the player's message
    history.append({"role": "user", "content": message})

    # Step 3: Build messages — character's system prompt + their history
    messages = [
        {"role": "system", "content": character["system_prompt"]}
    ] + history

    # Step 4: Call the API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=200,
        temperature=0.9,
    )

    reply = response.choices[0].message.content.strip()

    # Step 5: Save the reply back to this character's history
    history.append({"role": "assistant", "content": reply})
    session["character_histories"][character_id] = history

    # Trim to keep things manageable
    if len(session["character_histories"][character_id]) > 16:
        session["character_histories"][character_id] = \
            session["character_histories"][character_id][-16:]

    return jsonify({"character_id": character_id, "reply": reply})
# ──────────────────────────────────────────────────────────────────────────────


@app.route("/api/move", methods=["POST"])
def move():
    """Deterministic room-to-room movement. No LLM involved."""
    if session.get("combat"):
        return jsonify({"error": "You can't leave while in combat."}), 400

    data      = request.get_json() or {}
    direction = (data.get("direction") or "").strip().lower()
    room      = current_room()
    exits     = room["exits"]

    if direction not in exits:
        available = ", ".join(exits.keys()) or "none"
        return jsonify({
            "narrative": f"You can't go {direction or 'that way'}. Exits: {available}.",
            "room":      session["player"]["room"],
            "room_data": _room_state(),
            "player":    session["player"],
            "combat":    None,
        })

    session["player"]["room"] = exits[direction]
    session.modified = True

    new_room  = current_room()
    exits_str = ", ".join(new_room["exits"].keys()) or "none"
    return jsonify({
        "narrative": (
            f"You head {direction} into {new_room['name']}.\n\n"
            f"{new_room['description']}\n\n"
            f"Exits: {exits_str}."
        ),
        "room":      session["player"]["room"],
        "room_data": _room_state(),
        "player":    session["player"],
        "combat":    None,
    })


@app.route("/api/combat/start", methods=["POST"])
def combat_start():
    """Initiate combat with an enemy in the current room."""
    data     = request.get_json()
    enemy_id = data.get("enemy_id", "")
    enemy    = ENEMIES.get(enemy_id)

    if not enemy:
        return jsonify({"error": "Unknown enemy"}), 404
    if enemy_id not in current_room()["enemies"]:
        return jsonify({"error": "That enemy is not here"}), 400

    session["combat"] = {"enemy_id": enemy_id, "enemy_hp": enemy["max_hp"]}

    return jsonify({
        "narrative": f"⚔️  {enemy['taunt']}\n\nCombat begins! Type 'attack', 'defend', or 'flee'.",
        "combat":    session["combat"],
        "enemy":     {k: v for k, v in enemy.items() if k != "system_prompt"},
        "player":    session["player"],
    })


@app.route("/api/combat/action", methods=["POST"])
def combat_action():
    data   = request.get_json()
    action = data.get("action", "")
    combat = session.get("combat")

    if not combat:
        return jsonify({"error": "Not in combat"}), 400

    # ─── Exercise 3 - Part 1: The Damage Calculation Start ───────────────────

    # ─── Exercise 3 - Part 1: The Damage Calculation End ─────────────────────


    # ─── Exercise 3 - Part 2: Narrate the Round Start ────────────────────────

    # ─── Exercise 3 - Part 2: Narrate the Round End ──────────────────────────


    # ─── Exercise 3 - Part 3: The Enemy Taunts You Start ─────────────────────

    # ─── Exercise 3 - Part 3: The Enemy Taunts You End ───────────────────────


    # ─── Exercise 3 - Part 4: Handle Enemy Defeat and Return Start ───────────

    # ─── Exercise 3 - Part 4: Handle Enemy Defeat and Return End ─────────────


# ─── Exercise 6 - Part 1: Generate Speech Narration Start ─────────────────────

def generate_narration_audio(text: str, voice_id: str):
    """Return a URL path to a generated mp3 of the narration, or None."""
    return None

# ─── Exercise 6 - Part 1: Generate Speech Narration End ───────────────────────


# ─── Exercise 6 - Part 2: Speech API Route Start ──────────────────────────────
# In Exercise 6 (Lab 3), this route turns log lines into spoken audio. Until
# the student wires it up, generate_narration_audio() returns None so the
# frontend stays silent — no 404, no error, just no voice.

@app.route("/api/speech", methods=["POST"])
def speech():
    """Return a URL to a generated mp3 of the narration text, or None."""
    data    = request.get_json() or {}
    text    = (data.get("text") or "").strip()
    speaker = (data.get("speaker") or "").strip().lower()  # "" = narrator, else char/enemy id
    if not text:
        return jsonify({"audio_url": None})
    audio_url = generate_narration_audio(text, speaker)
    return jsonify({"audio_url": audio_url})

# ─── Exercise 6 - Part 2: Speech API Route End ────────────────────────────────


# ─── Internal helpers ──────────────────────────────────────────────────────────

def _room_state():
    """Return a serialisable snapshot of the current room for the frontend."""
    room_id = session["player"]["room"]
    visited = session.get("visited") or []
    if room_id not in visited:
        visited.append(room_id)
        session["visited"] = visited
        session.modified = True

    room = current_room()
    return {
        "id":          room_id,
        "name":        room["name"],
        "background":  room["background"],
        "exits":       room["exits"],
        "characters":  [
            {"id": cid, "name": CHARACTERS[cid]["name"],
             "sprite": CHARACTERS[cid]["sprite"]}
            for cid in room["characters"] if cid in CHARACTERS
        ],
        "enemies": [
            {"id": eid, "name": ENEMIES[eid]["name"],
             "sprite": ENEMIES[eid]["sprite"],
             "hp": ENEMIES[eid]["max_hp"]}
            for eid in room["enemies"] if eid in ENEMIES
        ],
        "visited":     list(visited),
    }


def _map_layout():
    """Static topology — sent once on /api/start so the minimap can render."""
    return {
        rid: {
            "name":   r["name"],
            "coords": list(ROOM_COORDS.get(rid, (0, 0))),
            "exits":  r["exits"],
        }
        for rid, r in ROOMS.items()
    }


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
