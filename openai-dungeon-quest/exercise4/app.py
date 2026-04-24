"""
Dungeon Quest — Exercise 4 complete solution.

What was added vs Exercise 3:
  - /api/action: upgraded GM to return structured JSON output
    * uses response_format={"type": "json_object"} so the model returns parseable JSON
    * GM now returns {narrative, room_change, item_found, gold_found} in one call
    * structured output lets the GM grant items/gold and update state reliably
    * demonstrates why structured output beats "parse the text with regex" at scale

Run:
    python app.py

Then open the URL shown in the VS Code Ports panel.
"""
import copy, json, os, re, random
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


def build_gm_system_prompt():
    """
    Updated for Exercise 4: tells the model to return JSON with specific fields
    instead of free text with an embedded ROOM_CHANGE token.
    """
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

RESPONSE FORMAT — you MUST respond with valid JSON only. No extra text outside the JSON object.

{{
  "narrative":   "2-4 sentences describing what happens. Atmospheric and vivid.",
  "room_change": "room_id if the player successfully moves to another room, else null",
  "item_found":  "name of item the player finds (e.g. 'Health Potion'), else null",
  "gold_found":  0
}}

RULES:
- room_change must be a valid room_id from the world map above, or null.
- If the exit doesn't exist, set room_change to null and explain in the narrative.
- item_found: only grant an item if the player specifically searches or if the story
  warrants it (e.g. finding a chest). Usually null.
- gold_found: only grant gold for specific discoveries. Usually 0.
- Keep the narrative atmospheric: torchlight, echoes, smells, sounds."""


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
    Exercise 4: Structured JSON output from the game master.

    Key concepts demonstrated:
    - response_format={"type": "json_object"} forces the model to return valid JSON
    - The system prompt describes the exact JSON schema the model must follow
    - Parsing the structured response lets us reliably update multiple game state fields
    - Compare to Exercise 1 where we had to regex-parse "ROOM_CHANGE:" from free text
    - Structured output is more robust, extensible, and easier to test
    """
    data         = request.get_json()
    player_input = data.get("input", "").strip()

    if not player_input:
        return jsonify({"error": "No input provided"}), 400

    # Append player message to history
    session["game_history"].append({"role": "user", "content": player_input})

    messages = [
        {"role": "system", "content": build_gm_system_prompt()}
    ] + session["game_history"]

    # Step 1: Call with json_object response format — model MUST return valid JSON
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=400,
        temperature=0.8,
        response_format={"type": "json_object"},
    )

    raw_reply = response.choices[0].message.content.strip()

    # Step 2: Parse the structured response — no regex needed, it's always valid JSON
    try:
        gm_data = json.loads(raw_reply)
    except json.JSONDecodeError:
        # Fallback: treat the whole thing as narrative if parsing fails
        gm_data = {"narrative": raw_reply, "room_change": None, "item_found": None, "gold_found": 0}

    # Append to history as a plain string summary (not JSON, to keep history readable)
    narrative    = gm_data.get("narrative", "The dungeon is silent.")
    room_change  = gm_data.get("room_change")
    item_found   = gm_data.get("item_found")
    gold_found   = gm_data.get("gold_found", 0)

    session["game_history"].append({"role": "assistant", "content": narrative})

    # Step 3: Apply structured state changes
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


@app.route("/api/talk", methods=["POST"])
def talk():
    data         = request.get_json()
    character_id = data.get("character_id", "")
    message      = data.get("message", "").strip()

    character = CHARACTERS.get(character_id)
    if not character:
        return jsonify({"error": "Unknown character"}), 404

    if "character_histories" not in session:
        session["character_histories"] = {}
    if character_id not in session["character_histories"]:
        session["character_histories"][character_id] = []

    history = session["character_histories"][character_id]
    history.append({"role": "user", "content": message})

    messages = [{"role": "system", "content": character["system_prompt"]}] + history

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=200,
        temperature=0.9,
    )

    reply = response.choices[0].message.content.strip()
    history.append({"role": "assistant", "content": reply})
    session["character_histories"][character_id] = history

    if len(session["character_histories"][character_id]) > 16:
        session["character_histories"][character_id] = \
            session["character_histories"][character_id][-16:]

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
    data   = request.get_json()
    action = data.get("action", "attack")
    combat = session.get("combat")

    if not combat:
        return jsonify({"error": "Not in combat"}), 400

    enemy  = ENEMIES[combat["enemy_id"]]
    player = session["player"]

    enemy_hp  = combat["enemy_hp"]
    player_hp = player["hp"]

    player_damage_dealt = 0
    player_damage_taken = 0
    enemy_defeated      = False
    game_over           = False
    fled                = False

    if action == "attack":
        raw = player["attack"] - enemy["defense"]
        player_damage_dealt = max(1, raw + random.randint(-2, 3))
        enemy_hp -= player_damage_dealt
        raw = enemy["attack"] - player["defense"]
        player_damage_taken = max(1, raw + random.randint(-2, 3))
        player_hp -= player_damage_taken
    elif action == "defend":
        raw = enemy["attack"] - player["defense"] * 2
        player_damage_taken = max(0, raw + random.randint(-1, 2))
        player_hp -= player_damage_taken
    elif action == "flee":
        fled = random.random() < 0.4

    if enemy_hp <= 0:
        enemy_hp = 0
        enemy_defeated = True
    if player_hp <= 0:
        player_hp = 0
        game_over = True

    combat["enemy_hp"] = enemy_hp
    session["player"]["hp"] = player_hp
    session["combat"] = None if (enemy_defeated or fled) else combat

    if fled:
        narrator_prompt = f"The player {'escaped from' if fled else 'failed to flee from'} {enemy['name']}. Describe in 1-2 sentences."
    elif enemy_defeated:
        narrator_prompt = f"The player defeated {enemy['name']} with {player_damage_dealt} final damage. Describe the defeat in 1-2 sentences."
    elif game_over:
        narrator_prompt = f"{enemy['name']} killed the player with {player_damage_taken} damage. Describe the defeat in 1-2 sentences."
    elif action == "attack":
        narrator_prompt = (
            f"Player dealt {player_damage_dealt} to {enemy['name']} ({enemy_hp} HP left). "
            f"{enemy['name']} dealt {player_damage_taken} back ({player_hp} HP left). "
            f"Describe in 1-2 vivid sentences."
        )
    else:
        narrator_prompt = f"Player defended against {enemy['name']}, taking only {player_damage_taken} damage. Describe in 1-2 sentences."

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

    room_data = None
    if enemy_defeated:
        player["gold"] += enemy["gold_drop"]
        player["xp"]   += enemy["xp_drop"]
        session["player"] = player
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
