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
    Implement this handler in the INSERT block below — do not edit anything
    above or below the marked block.
    """
    data         = request.get_json()
    player_input = data.get("input", "").strip()

    if not player_input:
        return jsonify({"error": "No input provided"}), 400

    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║                                                                      ║
    # ║           EXERCISE 1 — INSERT YOUR CODE BELOW THIS LINE              ║
    # ║                                                                      ║
    # ╚══════════════════════════════════════════════════════════════════════╝
    #
    # By the end of this block you MUST define:
    #   narrative : str   — the game master's reply to show the player
    #
    # You MAY also update (all optional):
    #   session["game_history"]     — append {"role": "user", "content": ...}
    #                                  and {"role": "assistant", "content": ...}
    #                                  so the next turn has context.
    #   session["player"]["room"]   — if the GM moved the player to a new room.
    #
    # ⚠️  Flask's cookie session only auto-saves top-level key assignments.
    #     After you mutate a nested value (list.append, dict[k] = v, etc.),
    #     set `session.modified = True` before returning.
    #
    # Already in scope for you:
    #   player_input              — the player's message (trimmed, non-empty)
    #   session["player"]         — {"room","hp","max_hp","gold","attack",
    #                                "defense","inventory","xp"}
    #   session["game_history"]   — list of {"role","content"} dicts so far
    #   current_room()            — dict for the room the player is in
    #   ROOMS, CHARACTERS, ENEMIES — full world data from game_data.py
    #
    # Typical approach:
    #   1. Build a system prompt from current_room() + session["player"].
    #   2. Append the user message to session["game_history"].
    #   3. Call the OpenAI Chat Completions API with
    #      [{"role":"system",...}] + session["game_history"].
    #   4. Append the assistant reply to session["game_history"].
    #   5. Assign the assistant reply text to `narrative`.
    #   6. (Optional) Parse any room change the GM announced and update
    #      session["player"]["room"].
    # ──────────────────────────────────────────────────────────────────────────


    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║           END EXERCISE 1 — INSERT YOUR CODE ABOVE THIS LINE          ║
    # ╚══════════════════════════════════════════════════════════════════════╝

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
    Implement this handler in the INSERT block below — do not edit anything
    above or below the marked block.
    """
    data         = request.get_json()
    character_id = data.get("character_id", "")
    message      = data.get("message", "").strip()

    character = CHARACTERS.get(character_id)
    if not character:
        return jsonify({"error": "Unknown character"}), 404

    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║                                                                      ║
    # ║           EXERCISE 2 — INSERT YOUR CODE BELOW THIS LINE              ║
    # ║                                                                      ║
    # ╚══════════════════════════════════════════════════════════════════════╝
    #
    # By the end of this block you MUST define:
    #   reply : str   — the NPC's response to show the player
    #
    # You SHOULD also update:
    #   session["character_histories"][character_id]
    #       — this NPC's PRIVATE conversation history (separate from the
    #         game master thread). Append the player message and the NPC's
    #         reply so the next turn has context.
    #
    # ⚠️  Flask's cookie session only auto-saves top-level key assignments.
    #     After you mutate the nested history list/dict, set
    #     `session.modified = True` before returning.
    #
    # Already in scope for you:
    #   character_id                — the NPC the player is talking to
    #   message                     — the player's message (trimmed, may be "")
    #   character                   — CHARACTERS[character_id] (guaranteed exists);
    #                                 has keys: name, title, sprite,
    #                                 system_prompt, greeting
    #   session["character_histories"]
    #                               — dict keyed by character_id; may or may not
    #                                 already have an entry for this NPC
    #
    # Typical approach:
    #   1. Initialise session["character_histories"][character_id] = []
    #      if this is the first turn with this NPC.
    #   2. Append {"role":"user","content": message} to that history.
    #   3. Build the messages list:
    #         [{"role":"system","content": character["system_prompt"]}]
    #         + session["character_histories"][character_id]
    #   4. Call the OpenAI Chat Completions API.
    #   5. Append {"role":"assistant","content": ...} to the history.
    #   6. Assign the assistant reply text to `reply`.
    # ──────────────────────────────────────────────────────────────────────────


    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║           END EXERCISE 2 — INSERT YOUR CODE ABOVE THIS LINE          ║
    # ╚══════════════════════════════════════════════════════════════════════╝

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
    Implement this handler in the INSERT block below — do not edit anything
    above or below the marked block.
    """
    data    = request.get_json()
    action  = data.get("action", "attack")
    combat  = session.get("combat")

    if not combat:
        return jsonify({"error": "Not in combat"}), 400

    enemy = ENEMIES[combat["enemy_id"]]

    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║                                                                      ║
    # ║           EXERCISE 3 — INSERT YOUR CODE BELOW THIS LINE              ║
    # ║                                                                      ║
    # ╚══════════════════════════════════════════════════════════════════════╝
    #
    # By the end of this block you MUST define:
    #   narrative      : str   — the combat round description shown to the player
    #   enemy_defeated : bool  — True if this round killed the enemy
    #   game_over      : bool  — True if this round killed the player
    #
    # You SHOULD also update:
    #   session["combat"]["enemy_hp"]   — subtract damage dealt to the enemy
    #   session["player"]["hp"]         — subtract damage taken by the player
    #   session["player"]["gold"]       — add enemy["gold_drop"] on defeat
    #   session["player"]["xp"]         — add enemy["xp_drop"] on defeat
    #   session["combat"]               — set to None when the fight ends
    #                                      (enemy defeated, player fled, or died)
    #
    # ⚠️  Flask's cookie session only auto-saves top-level key assignments.
    #     After you mutate nested values (session["combat"]["enemy_hp"] -= n,
    #     session["player"]["hp"] -= n, etc.), set `session.modified = True`
    #     before returning.
    #
    # ⚠️  Do NOT call current_room()["enemies"].remove(...) — ROOMS is a
    #     module-level global and that edit leaks across all sessions.
    #     If you want the defeated enemy to disappear from the room panel,
    #     track it in session (e.g. session["defeated_enemies"]) and filter
    #     _room_state() accordingly — or simply leave it; a defeated enemy
    #     with 0 hp is an acceptable starter behaviour.
    #
    # Already in scope for you:
    #   action            — "attack", "defend", or "flee"
    #   combat            — session["combat"] (guaranteed non-None here)
    #   enemy             — ENEMIES[combat["enemy_id"]] with keys:
    #                         name, sprite, max_hp, attack, defense,
    #                         gold_drop, xp_drop, system_prompt, taunt
    #   session["player"] — player stats (hp, max_hp, attack, defense, gold, xp)
    #
    # Typical approach:
    #   1. Compute damage:
    #        attack → max(1, player.attack − enemy.defense) dealt to enemy,
    #                 then max(1, enemy.attack − player.defense) back to player
    #        defend → player takes half damage, deals none
    #        flee   → 50% chance to escape (set combat to None, narrative
    #                 describes the escape); on fail, take a hit
    #   2. Apply damage to session["combat"]["enemy_hp"] and
    #      session["player"]["hp"].
    #   3. Call OpenAI twice:
    #        a) a narrator prompt to describe the round in 1-2 sentences
    #        b) the enemy's system_prompt to generate a contextual taunt
    #      Concatenate them into `narrative`.
    #   4. Set flags:
    #        enemy_defeated = session["combat"]["enemy_hp"] <= 0
    #        game_over      = session["player"]["hp"] <= 0
    #   5. If enemy_defeated: award gold/xp, set session["combat"] = None.
    #   6. If game_over: set session["combat"] = None.
    # ──────────────────────────────────────────────────────────────────────────


    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║           END EXERCISE 3 — INSERT YOUR CODE ABOVE THIS LINE          ║
    # ╚══════════════════════════════════════════════════════════════════════╝

    return jsonify({
        "narrative":      narrative,
        "combat":         session.get("combat"),
        "player":         session["player"],
        "enemy_defeated": enemy_defeated,
        "game_over":      game_over,
        "room_data":      _room_state(),
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
