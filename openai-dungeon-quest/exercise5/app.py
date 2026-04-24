"""
Dungeon Quest — Exercise 5 complete solution.

What was added vs Exercise 4:
  - /api/action: streaming GM responses using Server-Sent Events (SSE)
    * text streams to the browser word-by-word instead of waiting for the full response
    * client-side updated to handle the stream and append tokens as they arrive
  - Automatic conversation summary when history exceeds 10 messages
    * uses a separate OpenAI call to compress old history into a single summary message
    * demonstrates context window management — essential for long-running AI apps
  - /api/summarize endpoint for manual history inspection

Run:
    python app.py

Then open the URL shown in the VS Code Ports panel.
"""
import copy, json, os, re, random
from flask import Flask, render_template, request, jsonify, session, Response, stream_with_context
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

RESPONSE FORMAT — you MUST respond with valid JSON only. No extra text outside the JSON object.

{{
  "narrative":   "2-4 sentences describing what happens. Atmospheric and vivid.",
  "room_change": "room_id if the player successfully moves to another room, else null",
  "item_found":  "name of item the player finds, else null",
  "gold_found":  0
}}

RULES:
- room_change must be a valid room_id from the world map above, or null.
- If the exit doesn't exist, set room_change to null and explain in the narrative.
- item_found: only grant an item if the player specifically searches or story warrants it.
- gold_found: only grant gold for specific discoveries. Usually 0.
- Keep the narrative atmospheric: torchlight, echoes, smells, sounds."""


def summarize_history():
    """
    Compress conversation history when it grows long.

    Instead of truncating (which loses context), we ask OpenAI to summarize
    everything that happened so far. The summary becomes a single system-level
    message that replaces the old turns.

    This is the standard technique for long-running AI sessions that would
    otherwise exceed the context window.
    """
    history = session["game_history"]
    if len(history) <= 10:
        return  # Not long enough to need summarizing

    # Build a transcript of the conversation to summarize
    transcript = "\n".join(
        f"{'Player' if m['role'] == 'user' else 'GM'}: {m['content']}"
        for m in history[:-4]  # Keep the 4 most recent turns fresh
    )

    summary_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content":
                "You are a dungeon quest game assistant. Summarize the player's adventure "
                "so far in 3-5 sentences. Include: rooms visited, key events, items obtained, "
                "enemies defeated, and important NPC interactions. Write in past tense."},
            {"role": "user", "content": f"Summarize this adventure log:\n\n{transcript}"},
        ],
        max_tokens=200,
        temperature=0.3,
    )

    summary = summary_response.choices[0].message.content.strip()

    # Replace old history with summary + the 4 most recent turns
    session["game_history"] = [
        {"role": "system", "content": f"[ADVENTURE SUMMARY] {summary}"},
    ] + history[-4:]


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
    Exercise 5: Streaming GM responses + automatic history summarization.

    Key concepts demonstrated:
    - stream=True returns a generator that yields tokens as they're produced
    - Server-Sent Events (SSE) let us push tokens to the browser in real time
    - Accumulating the full response from a stream (needed to parse JSON at the end)
    - summarize_history() compresses old turns to prevent context window overflow
    - The final JSON-in-stream pattern: stream the text, parse structure after stream ends

    NOTE: Because we're using json_object response format AND streaming, we must
    accumulate the full stream before parsing the JSON. The streaming benefit here
    is demonstrating the pattern — in production you might stream the narrative
    field separately from the structured fields.
    """
    data         = request.get_json()
    player_input = data.get("input", "").strip()

    if not player_input:
        return jsonify({"error": "No input provided"}), 400

    # Summarize history if it's getting long
    summarize_history()

    session["game_history"].append({"role": "user", "content": player_input})

    messages = [
        {"role": "system", "content": build_gm_system_prompt()}
    ] + session["game_history"]

    def generate():
        """Generator that yields SSE-formatted token chunks, then a final state event."""
        full_text = ""

        # Step 1: Open a streaming chat completion
        with client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=400,
            temperature=0.8,
            response_format={"type": "json_object"},
            stream=True,
        ) as stream:
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta.content:
                    full_text += delta.content
                    # Send each token as an SSE "token" event
                    yield f"event: token\ndata: {json.dumps({'text': delta.content})}\n\n"

        # Step 2: Parse the accumulated JSON once the stream is complete
        try:
            gm_data = json.loads(full_text)
        except json.JSONDecodeError:
            gm_data = {"narrative": full_text, "room_change": None, "item_found": None, "gold_found": 0}

        narrative   = gm_data.get("narrative", "The dungeon is silent.")
        room_change = gm_data.get("room_change")
        item_found  = gm_data.get("item_found")
        gold_found  = gm_data.get("gold_found", 0)

        # Step 3: Apply state changes
        session["game_history"].append({"role": "assistant", "content": narrative})

        if room_change and room_change in ROOMS:
            session["player"]["room"] = room_change

        if item_found:
            session["player"]["inventory"].append(item_found)
            narrative += f"\n\n📦 You picked up: {item_found}!"

        if gold_found and gold_found > 0:
            session["player"]["gold"] += gold_found
            narrative += f"\n\n💰 You found {gold_found} gold coins!"

        # Step 4: Send a final SSE "done" event with the full game state
        state = {
            "narrative": narrative,
            "room":      session["player"]["room"],
            "room_data": _room_state(),
            "player":    session["player"],
            "combat":    session.get("combat"),
        }
        yield f"event: done\ndata: {json.dumps(state)}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.route("/api/summarize", methods=["POST"])
def get_summary():
    """Return the current conversation history (for debugging/inspection)."""
    return jsonify({
        "history_length": len(session.get("game_history", [])),
        "history":        session.get("game_history", []),
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
        narrator_prompt = f"The player defeated {enemy['name']} with {player_damage_dealt} final damage. 1-2 sentences."
    elif game_over:
        narrator_prompt = f"{enemy['name']} killed the player with {player_damage_taken} damage. 1-2 sentences."
    elif action == "attack":
        narrator_prompt = (
            f"Player dealt {player_damage_dealt} to {enemy['name']} ({enemy_hp} HP left). "
            f"{enemy['name']} dealt {player_damage_taken} back ({player_hp} HP left). "
            f"Describe in 1-2 vivid sentences."
        )
    else:
        narrator_prompt = f"Player defended against {enemy['name']}, taking only {player_damage_taken} damage. 1-2 sentences."

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
                    f"Your HP is {enemy_hp}/{enemy['max_hp']}. Player has {player_hp} HP. "
                    f"One-sentence in-character taunt."},
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
