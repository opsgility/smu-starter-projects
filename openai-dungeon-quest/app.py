"""
Dungeon Quest — Flask server (base starter project, no OpenAI yet).

Run:
    python app.py

Then open the URL shown in the VS Code Ports panel.
"""
import copy, json
from flask import Flask, render_template, request, jsonify, session
from game_data import ROOMS, CHARACTERS, ENEMIES, PLAYER_START

app = Flask(__name__)
app.secret_key = "dungeon-quest-dev-key"


# ─── Helpers ───────────────────────────────────────────────────────────────────

def current_room():
    return ROOMS[session["player"]["room"]]

def reset_session():
    session["player"]             = copy.deepcopy(PLAYER_START)
    session["game_history"]       = []   # [{role, content}]  — game master thread
    session["character_histories"] = {}  # {char_id: [{role, content}]}
    session["combat"]             = None # {enemy_id, enemy_hp} or None


# ─── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/start", methods=["POST"])
def start():
    """Reset and return the opening scene."""
    reset_session()
    room = current_room()
    return jsonify({
        "narrative": (
            f"You stand at the entrance of {room['name']}.\n\n"
            f"{room['description']}\n\n"
            "Type 'help' to see what you can do."
        ),
        "room":       session["player"]["room"],
        "room_data":  _room_state(),
        "player":     session["player"],
        "combat":     None,
    })


@app.route("/api/action", methods=["POST"])
def action():
    """
    Handle a free-text player command via the game master.
    ── Exercise 1 ──────────────────────────────────────────────────────────────
    Replace the placeholder below with a real OpenAI call.

    You have access to:
      session["player"]        — current player state dict
      session["game_history"]  — list of {role, content} dicts (conversation so far)
      current_room()           — the current room dict from ROOMS
      ROOMS, CHARACTERS, ENEMIES — full world data

    Your function should:
      1. Build a system prompt describing the world, current room, player state,
         and the game master's role.
      2. Append the player's message to session["game_history"].
      3. Call the OpenAI Chat Completions API with the full history.
      4. Append the assistant reply to session["game_history"].
      5. Parse any room changes the GM described and update session["player"]["room"].
      6. Return the JSON response below.
    ────────────────────────────────────────────────────────────────────────────
    """
    data         = request.get_json()
    player_input = data.get("input", "").strip()

    if not player_input:
        return jsonify({"error": "No input provided"}), 400

    # ── Placeholder (remove in Exercise 1) ────────────────────────────────────
    narrative = (
        f'You said: "{player_input}"\n\n'
        "The dungeon waits silently. "
        "(Complete Exercise 1 to bring the game master to life.)"
    )
    # ── End placeholder ───────────────────────────────────────────────────────

    return jsonify({
        "narrative": narrative,
        "room":      session["player"]["room"],
        "room_data": _room_state(),
        "player":    session["player"],
        "combat":    session.get("combat"),
    })


@app.route("/api/talk", methods=["POST"])
def talk():
    """
    Send a message to an NPC and get their reply.
    ── Exercise 2 ──────────────────────────────────────────────────────────────
    Replace the placeholder below with a real OpenAI call.

    You have access to:
      character_id             — which NPC the player is talking to
      CHARACTERS[character_id] — the NPC's name, sprite, and system_prompt
      session["character_histories"][character_id]
                               — this NPC's private conversation history
                                 (separate from the game master thread)

    Your function should:
      1. Load or create the character's conversation history.
      2. Use CHARACTERS[character_id]["system_prompt"] as the system message.
      3. Append the player message and call the OpenAI Chat Completions API.
      4. Append the assistant reply to the character's history.
      5. Return the JSON response below.
    ────────────────────────────────────────────────────────────────────────────
    """
    data         = request.get_json()
    character_id = data.get("character_id", "")
    message      = data.get("message", "").strip()

    character = CHARACTERS.get(character_id)
    if not character:
        return jsonify({"error": "Unknown character"}), 404

    # ── Placeholder (remove in Exercise 2) ────────────────────────────────────
    reply = (
        f"{character['name']} looks at you thoughtfully. "
        "(Complete Exercise 2 to give characters their voice.)"
    )
    # ── End placeholder ───────────────────────────────────────────────────────

    return jsonify({
        "character_id": character_id,
        "reply":        reply,
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
    """
    Process one round of combat.
    ── Exercise 3 ──────────────────────────────────────────────────────────────
    Replace the placeholder below with a real OpenAI call.

    You have access to:
      session["combat"]        — {enemy_id, enemy_hp}
      session["player"]        — player stats (hp, attack, defense)
      ENEMIES[enemy_id]        — enemy stats + system_prompt for taunts
      action                   — "attack", "defend", or "flee"

    Your function should:
      1. Calculate damage using player/enemy attack & defense stats.
      2. Call OpenAI to generate a narrator description of the round (1-2 sentences),
         and separately call the enemy's system_prompt to generate a contextual taunt.
      3. Update session["combat"]["enemy_hp"] and session["player"]["hp"].
      4. If enemy_hp <= 0: award gold/xp, clear combat, remove enemy from room.
      5. If player_hp <= 0: game over.
      6. Return the JSON response below.
    ────────────────────────────────────────────────────────────────────────────
    """
    data    = request.get_json()
    action  = data.get("action", "attack")
    combat  = session.get("combat")

    if not combat:
        return jsonify({"error": "Not in combat"}), 400

    enemy = ENEMIES[combat["enemy_id"]]

    # ── Placeholder (remove in Exercise 3) ────────────────────────────────────
    narrative = (
        f"You swing at {enemy['name']}. "
        "(Complete Exercise 3 to make combat dynamic.)"
    )
    enemy_defeated = False
    game_over      = False
    # ── End placeholder ───────────────────────────────────────────────────────

    return jsonify({
        "narrative":     narrative,
        "combat":        session.get("combat"),
        "player":        session["player"],
        "enemy_defeated": enemy_defeated,
        "game_over":     game_over,
    })


# ─── Internal helpers ──────────────────────────────────────────────────────────

def _room_state():
    """Return a serialisable snapshot of the current room for the frontend."""
    room = current_room()
    return {
        "id":          session["player"]["room"],
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
    }


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
