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


# ─── Exercise 1 → Task 1 Start ────────────────────────────────────────────────

# ─── Exercise 1 → Task 1 End ──────────────────────────────────────────────────


# ─── Exercise 2 → Task 1 Start ────────────────────────────────────────────────

# ─── Exercise 2 → Task 1 End ──────────────────────────────────────────────────


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


# ─── Exercise 3 → Task 1 Start ────────────────────────────────────────────────

# ─── Exercise 3 → Task 1 End ──────────────────────────────────────────────────


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
