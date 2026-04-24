"""
Dungeon Quest — Exercise 1 complete solution.

What was added vs the starter:
  - OpenAI client setup with environment key
  - /api/action: game master using Chat Completions with full conversation history
    * system prompt describes the world, room, player stats
    * appends every turn to session["game_history"] for multi-turn memory
    * GM response is parsed for room-change keywords to update player position

Run:
    python app.py

Then open the URL shown in the VS Code Ports panel.
"""
import copy, json, os, re
from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
from game_data import ROOMS, CHARACTERS, ENEMIES, PLAYER_START

app = Flask(__name__)
app.secret_key = "dungeon-quest-dev-key"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# ─── Helpers ───────────────────────────────────────────────────────────────────

def current_room():
    return ROOMS[session["player"]["room"]]

def reset_session():
    session["player"]             = copy.deepcopy(PLAYER_START)
    session["game_history"]       = []
    session["character_histories"] = {}
    session["combat"]             = None


# ─── System prompt builder ─────────────────────────────────────────────────────

def build_gm_system_prompt():
    """Build a rich system prompt that describes the whole world to the GM."""
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
  Attack: {player['attack']} | Defense: {player['defense']}
  Inventory: {', '.join(player['inventory'])}
  XP: {player['xp']}

RULES:
- Respond in 2-4 vivid sentences. Be atmospheric and concise.
- If the player tries to move (go north/south/east/west) and that exit exists, narrate the
  movement and end your reply with exactly: ROOM_CHANGE:<room_id>
  Example: "You descend the stone steps... ROOM_CHANGE:dungeon_corridor"
- If the exit doesn't exist, tell them they can't go that way.
- Do not invent rooms or exits beyond the world map above.
- Do not handle combat or NPC dialogue directly — those are handled by other systems.
- Keep descriptions atmospheric: torchlight, echoes, smells, sounds."""


# ─── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/start", methods=["POST"])
def start():
    reset_session()
    room = current_room()
    return jsonify({
        "narrative": (
            f"You stand at the entrance of {room['name']}.\n\n"
            f"{room['description']}\n\n"
            "Type 'help' to see what you can do."
        ),
        "room":      session["player"]["room"],
        "room_data": _room_state(),
        "player":    session["player"],
        "combat":    None,
    })


@app.route("/api/action", methods=["POST"])
def action():
    """
    Exercise 1: Game master using Chat Completions with conversation history.

    Key concepts demonstrated:
    - Building a detailed system prompt with world state
    - Maintaining multi-turn conversation history in session
    - Parsing the GM's response for structured signals (ROOM_CHANGE)
    - Updating game state based on AI output
    """
    data         = request.get_json()
    player_input = data.get("input", "").strip()

    if not player_input:
        return jsonify({"error": "No input provided"}), 400

    # Step 1: Append the player's message to history
    session["game_history"].append({"role": "user", "content": player_input})

    # Step 2: Build messages list — system prompt (fresh each turn for current state)
    #         followed by the full conversation history
    messages = [
        {"role": "system", "content": build_gm_system_prompt()}
    ] + session["game_history"]

    # Step 3: Call the OpenAI Chat Completions API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300,
        temperature=0.8,
    )

    raw_reply = response.choices[0].message.content.strip()

    # Step 4: Append the assistant's reply to history
    session["game_history"].append({"role": "assistant", "content": raw_reply})

    # Step 5: Parse ROOM_CHANGE signal from the GM's response
    narrative = raw_reply
    room_change_match = re.search(r"ROOM_CHANGE:(\w+)", raw_reply)
    if room_change_match:
        new_room_id = room_change_match.group(1)
        if new_room_id in ROOMS:
            session["player"]["room"] = new_room_id
        # Strip the signal tag from the displayed narrative
        narrative = re.sub(r"\s*ROOM_CHANGE:\w+", "", narrative).strip()

    # Trim history to last 20 messages to avoid token bloat
    if len(session["game_history"]) > 20:
        session["game_history"] = session["game_history"][-20:]

    return jsonify({
        "narrative": narrative,
        "room":      session["player"]["room"],
        "room_data": _room_state(),
        "player":    session["player"],
        "combat":    session.get("combat"),
    })


@app.route("/api/talk", methods=["POST"])
def talk():
    """Exercise 2 not yet implemented — uses placeholder."""
    data         = request.get_json()
    character_id = data.get("character_id", "")
    message      = data.get("message", "").strip()

    character = CHARACTERS.get(character_id)
    if not character:
        return jsonify({"error": "Unknown character"}), 404

    reply = (
        f"{character['name']} looks at you thoughtfully. "
        "(Complete Exercise 2 to give characters their voice.)"
    )

    return jsonify({"character_id": character_id, "reply": reply})


@app.route("/api/combat/start", methods=["POST"])
def combat_start():
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
    """Exercise 3 not yet implemented — uses placeholder."""
    data   = request.get_json()
    action = data.get("action", "attack")
    combat = session.get("combat")

    if not combat:
        return jsonify({"error": "Not in combat"}), 400

    enemy = ENEMIES[combat["enemy_id"]]

    narrative = (
        f"You swing at {enemy['name']}. "
        "(Complete Exercise 3 to make combat dynamic.)"
    )

    return jsonify({
        "narrative":      narrative,
        "combat":         session.get("combat"),
        "player":         session["player"],
        "enemy_defeated": False,
        "game_over":      False,
    })


# ─── Internal helpers ──────────────────────────────────────────────────────────

def _room_state():
    room = current_room()
    return {
        "id":         session["player"]["room"],
        "name":       room["name"],
        "background": room["background"],
        "exits":      room["exits"],
        "characters": [
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
