"""
Dungeon Quest — Exercise 3 complete solution.

What was added vs Exercise 2:
  - /api/combat/action: full combat loop with OpenAI narration + enemy taunts
    * deterministic stat-based damage calculation (not random — AI controls narrative only)
    * two separate OpenAI calls per round: narrator + enemy taunt
    * enemy defeated: awards gold/xp, removes from room, clears combat state
    * player death: game over flag
    * demonstrates making multiple AI calls in a single request handler

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
    data         = request.get_json()
    player_input = data.get("input", "").strip()

    if not player_input:
        return jsonify({"error": "No input provided"}), 400

    session["game_history"].append({"role": "user", "content": player_input})

    messages = [
        {"role": "system", "content": build_gm_system_prompt()}
    ] + session["game_history"]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300,
        temperature=0.8,
    )

    raw_reply = response.choices[0].message.content.strip()
    session["game_history"].append({"role": "assistant", "content": raw_reply})

    narrative = raw_reply
    room_change_match = re.search(r"ROOM_CHANGE:(\w+)", raw_reply)
    if room_change_match:
        new_room_id = room_change_match.group(1)
        if new_room_id in ROOMS:
            session["player"]["room"] = new_room_id
        narrative = re.sub(r"\s*ROOM_CHANGE:\w+", "", narrative).strip()

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
    """
    Exercise 3: Full combat round with stat-based damage and OpenAI narration.

    Key concepts demonstrated:
    - Keeping game logic deterministic (stats decide outcomes) while using AI for flavor
    - Making two parallel-concept AI calls per round: narrator + enemy taunter
    - Using the enemy's own system_prompt as its "voice" — same technique as NPC dialogue
    - Updating session state (hp values) based on calculated outcomes, not AI decisions
    - Handling the "flee" action without combat damage
    """
    data   = request.get_json()
    action = data.get("action", "attack")
    combat = session.get("combat")

    if not combat:
        return jsonify({"error": "Not in combat"}), 400

    enemy  = ENEMIES[combat["enemy_id"]]
    player = session["player"]

    enemy_hp = combat["enemy_hp"]
    player_hp = player["hp"]

    player_damage_dealt  = 0
    player_damage_taken  = 0
    enemy_defeated       = False
    game_over            = False
    fled                 = False

    # ── Step 1: Calculate this round's outcome based on stats ────────────────
    if action == "attack":
        # Player attacks: base damage minus enemy defense, with small variance
        raw = player["attack"] - enemy["defense"]
        player_damage_dealt = max(1, raw + random.randint(-2, 3))
        enemy_hp -= player_damage_dealt

        # Enemy counter-attacks
        raw = enemy["attack"] - player["defense"]
        player_damage_taken = max(1, raw + random.randint(-2, 3))
        player_hp -= player_damage_taken

    elif action == "defend":
        # Player defends: halves incoming damage but deals none
        raw = enemy["attack"] - player["defense"] * 2
        player_damage_taken = max(0, raw + random.randint(-1, 2))
        player_hp -= player_damage_taken

    elif action == "flee":
        # 40% chance to escape
        fled = random.random() < 0.4

    # ── Step 2: Apply HP changes and check win/loss conditions ───────────────
    if enemy_hp <= 0:
        enemy_hp = 0
        enemy_defeated = True

    if player_hp <= 0:
        player_hp = 0
        game_over = True

    combat["enemy_hp"] = enemy_hp
    session["player"]["hp"] = player_hp
    session["combat"] = None if (enemy_defeated or fled) else combat

    # ── Step 3: Call OpenAI for a vivid narrator description of the round ────
    if fled:
        narrator_prompt = (
            f"The player attempted to flee from {enemy['name']} and {'escaped!' if fled else 'failed to escape.'} "
            f"Describe the desperate scramble in 1-2 sentences."
        )
    elif enemy_defeated:
        narrator_prompt = (
            f"The player just defeated {enemy['name']}! "
            f"They dealt {player_damage_dealt} damage in the final blow. "
            f"Describe the enemy's dramatic defeat in 1-2 vivid sentences."
        )
    elif game_over:
        narrator_prompt = (
            f"{enemy['name']} has slain the player! "
            f"The player took {player_damage_taken} fatal damage. "
            f"Describe the hero's grim defeat in 1-2 sentences."
        )
    elif action == "attack":
        narrator_prompt = (
            f"Combat round: player attacked {enemy['name']}, dealing {player_damage_dealt} damage. "
            f"{enemy['name']} counter-attacked for {player_damage_taken} damage. "
            f"Enemy has {enemy_hp} HP remaining. Player has {player_hp} HP remaining. "
            f"Describe this exchange in 1-2 vivid sentences."
        )
    else:  # defend
        narrator_prompt = (
            f"Combat round: player took a defensive stance against {enemy['name']}, "
            f"absorbing {player_damage_taken} damage. "
            f"Describe this defensive moment in 1-2 sentences."
        )

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

    # ── Step 4: Call OpenAI for an enemy taunt (uses the enemy's own personality) ──
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

    # ── Step 5: Handle enemy defeat (award loot, remove from room) ───────────
    room_data = None
    if enemy_defeated:
        player["gold"] += enemy["gold_drop"]
        player["xp"]   += enemy["xp_drop"]
        session["player"] = player

        # Remove defeated enemy from the room
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
