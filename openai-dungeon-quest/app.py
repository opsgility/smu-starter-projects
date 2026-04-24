"""
Dungeon Quest — Flask server (base starter project, no OpenAI yet).

Run:
    python app.py

Then open the URL shown in the VS Code Ports panel.
"""
import copy, json
from flask import Flask, render_template, request, jsonify, session
from game_data import ROOMS, CHARACTERS, ENEMIES, PLAYER_START

# ─── Exercise 1 - Part 1: Set Up the OpenAI Client Start ──────────────────────

# ─── Exercise 1 - Part 1: Set Up the OpenAI Client End ────────────────────────

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


# ─── Exercise 1 - Part 2: Build the System Prompt Start ───────────────────────

# ─── Exercise 1 - Part 2: Build the System Prompt End ─────────────────────────


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
        "player":     session["player"],
        "combat":     None,
    })


# ─── Exercise 1 - Part 3: Wire Up the API Call Start ─────────────────────────

# ─── Exercise 1 - Part 3: Wire Up the API Call End ───────────────────────────


# ─── Exercise 2 - Part 1: Wire Up the Talk Endpoint Start ────────────────────

# ─── Exercise 2 - Part 1: Wire Up the Talk Endpoint End ──────────────────────


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
