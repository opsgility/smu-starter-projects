"""
Dungeon Quest — Flask server (Lab 3 starter).

Lab 1 + Lab 2 work is already wired up below:
    ✓ Exercise 1 — OpenAI client + GM system prompt + /api/action
    ✓ Exercise 2 — /api/talk with per-character histories
    ✓ Exercise 3 — Combat: damage calc + narrator + enemy taunt + defeat handling
    ✓ Exercise 4 — Structured output (JSON mode replaces the ROOM_CHANGE regex)

In Lab 3 you'll add:
    Exercise 5 — Streaming narration with bounded memory (history summarization)
    Exercise 6 — Voiced narration with the OpenAI Speech (TTS) API

Run:
    python app.py

Then open the URL shown in the VS Code Ports panel.
"""
import copy, hashlib, json, os, random, re
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


# ─── Exercise 4 - Part 1: GM System Prompt — JSON mode (✓ Completed in Lab 2) ─
def build_gm_system_prompt():
    room   = current_room()
    player = session["player"]

    room_chars   = [CHARACTERS[c]["name"] for c in room["characters"] if c in CHARACTERS]
    room_enemies = [ENEMIES[e]["name"]    for e in room["enemies"]    if e in ENEMIES]
    exits        = ", ".join(f"{d} → {dest}" for d, dest in room["exits"].items())

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

RESPONSE FORMAT — respond with valid JSON only, no text outside the object:

{{
  "narrative":   "2-4 vivid atmospheric sentences.",
  "room_change": "room_id if the player moves to a new room, else null",
  "item_found":  "item name if the player finds something, else null",
  "gold_found":  0
}}

RULES:
- room_change must be a valid room_id from the world map, or null.
- item_found: only grant an item if the player searches or the story warrants it.
- gold_found: only for specific discoveries. Usually 0.
- Keep narrative atmospheric."""
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


# ─── Exercise 4 - Part 2: /api/action — JSON mode (✓ Completed in Lab 2) ─────
@app.route("/api/action", methods=["POST"])
def action():
    data         = request.get_json()
    player_input = data.get("input", "").strip()

    if not player_input:
        return jsonify({"error": "No input provided"}), 400

    session["game_history"].append({"role": "user", "content": player_input})

    messages = [
        {"role": "system", "content": build_gm_system_prompt()}
    ] + session["game_history"]

    # response_format enforces JSON output
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=400,
        temperature=0.8,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content.strip()

    # Parse the JSON — no regex needed
    try:
        gm_data = json.loads(raw)
    except json.JSONDecodeError:
        gm_data = {"narrative": raw, "room_change": None, "item_found": None, "gold_found": 0}

    narrative   = gm_data.get("narrative", "The dungeon is silent.")
    room_change = gm_data.get("room_change")
    item_found  = gm_data.get("item_found")
    gold_found  = gm_data.get("gold_found", 0)

    # Save a clean text version to history (not raw JSON)
    session["game_history"].append({"role": "assistant", "content": narrative})

    # Apply all state changes from structured fields
    if room_change and room_change in ROOMS:
        session["player"]["room"] = room_change

    if item_found:
        session["player"]["inventory"].append(item_found)
        narrative += f"\n\n📦 You picked up: {item_found}!"

    if gold_found and gold_found > 0:
        session["player"]["gold"] += gold_found
        narrative += f"\n\n💰 You found {gold_found} gold coins!"

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

    # ─── Exercise 3 - Part 1: The Damage Calculation (✓ Completed in Lab 2) ──
    enemy  = ENEMIES[combat["enemy_id"]]
    player = session["player"]

    enemy_hp  = combat["enemy_hp"]
    player_hp = player["hp"]

    player_damage_dealt = 0
    player_damage_taken = 0
    enemy_defeated = False
    game_over      = False
    fled           = False

    if action == "attack":
        raw = player["attack"] - enemy["defense"]
        player_damage_dealt = max(1, raw + random.randint(-2, 3))
        enemy_hp -= player_damage_dealt
        raw = enemy["attack"] - player["defense"]
        player_damage_taken = max(1, raw + random.randint(-2, 3))
        player_hp -= player_damage_taken

    elif action == "defend":
        # Defending halves incoming damage but deals none
        raw = enemy["attack"] - player["defense"] * 2
        player_damage_taken = max(0, raw + random.randint(-1, 2))
        player_hp -= player_damage_taken

    elif action == "flee":
        fled = random.random() < 0.4   # 40% escape chance

    if enemy_hp <= 0:
        enemy_hp = 0
        enemy_defeated = True

    if player_hp <= 0:
        player_hp = 0
        game_over = True

    combat["enemy_hp"]       = enemy_hp
    session["player"]["hp"]  = player_hp
    session["combat"] = None if (enemy_defeated or fled) else combat
    # ──────────────────────────────────────────────────────────────────────────


    # ─── Exercise 3 - Part 2: Narrate the Round (✓ Completed in Lab 2) ───────
    if fled:
        narrator_prompt = f"The player {'escaped from' if fled else 'failed to flee from'} {enemy['name']}. Describe in 1-2 sentences."
    elif enemy_defeated:
        narrator_prompt = f"The player defeated {enemy['name']} with {player_damage_dealt} final damage. Describe the defeat vividly in 1-2 sentences."
    elif game_over:
        narrator_prompt = f"{enemy['name']} killed the player with {player_damage_taken} damage. Describe the defeat in 1-2 grim sentences."
    elif action == "attack":
        narrator_prompt = (
            f"Player dealt {player_damage_dealt} damage to {enemy['name']} ({enemy_hp} HP remaining). "
            f"{enemy['name']} counter-attacked for {player_damage_taken} damage ({player_hp} HP remaining). "
            f"Describe this exchange in 1-2 vivid sentences."
        )
    else:
        narrator_prompt = f"Player took a defensive stance, absorbing only {player_damage_taken} damage from {enemy['name']}. 1-2 sentences."

    narrator_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a dramatic fantasy combat narrator. Be vivid and concise."},
            {"role": "user",   "content": narrator_prompt},
        ],
        max_tokens=120,
        temperature=0.85,
    )
    narrative = narrator_response.choices[0].message.content.strip()
    # ──────────────────────────────────────────────────────────────────────────


    # ─── Exercise 3 - Part 3: The Enemy Taunts You (✓ Completed in Lab 2) ────
    if not enemy_defeated and not fled and not game_over:
        taunt_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": enemy["system_prompt"]},
                {"role": "user",   "content":
                    f"You just fought the player. Your HP is {enemy_hp}/{enemy['max_hp']}. "
                    f"The player has {player_hp}/{player['max_hp']} HP. "
                    f"Give a one-sentence in-character taunt."},
            ],
            max_tokens=60,
            temperature=0.9,
        )
        taunt = taunt_response.choices[0].message.content.strip()
        narrative = f"{narrative}\n\n{enemy['name']}: \"{taunt}\""
    # ──────────────────────────────────────────────────────────────────────────


    # ─── Exercise 3 - Part 4: Defeat Handling + Return (✓ Completed in Lab 2) ─
    room_data = None
    if enemy_defeated:
        session["player"]["gold"] += enemy["gold_drop"]
        session["player"]["xp"]   += enemy["xp_drop"]

        room_id = session["player"]["room"]
        if combat["enemy_id"] in ROOMS[room_id]["enemies"]:
            ROOMS[room_id]["enemies"].remove(combat["enemy_id"])

        room_data = _room_state()
        narrative += f"\n\n✨ You gained {enemy['gold_drop']} gold and {enemy['xp_drop']} XP!"

    return jsonify({
        "narrative":      narrative,
        "combat":         session.get("combat"),
        "player":         session["player"],
        "enemy_defeated": enemy_defeated,
        "game_over":      game_over,
        "room_data":      room_data,
    })
    # ──────────────────────────────────────────────────────────────────────────


# ─── Exercise 6 - Part 1: Generate Speech Narration Start ─────────────────────

def generate_narration_audio(text: str, voice_id: str):
    """Return a URL path to a generated mp3 of the narration, or None."""
    return None

# ─── Exercise 6 - Part 1: Generate Speech Narration End ───────────────────────


# ─── Exercise 6 - Part 2: Speech API Route Start ──────────────────────────────
# In Exercise 6, this route turns log lines into spoken audio. Until the
# student wires it up, generate_narration_audio() returns None so the frontend
# stays silent — no 404, no error, just no voice.

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
