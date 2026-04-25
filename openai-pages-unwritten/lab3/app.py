"""
Pages Unwritten — Flask server.

Lab 3 starting point: Exercises 1-4 are already wired up — storyteller system
prompt, JSON-mode scene generation, gpt-image-1 backgrounds, and three-act
structure with ending detection. In this lab you will add streaming with
bounded memory (Exercise 5) and voiced narration (Exercise 6).

Run:
    python app.py

Then open the URL shown in the VS Code Ports panel.
"""
import base64, copy, hashlib, json, os
from flask import Flask, render_template, request, jsonify, session
from story_data import (
    GENRES, DEFAULT_GENRE, PLAYER_START,
    FALLBACK_OPENINGS, ACT_BOUNDARIES, SCENE_LIMIT,
    IMAGE_PROMPT_TEMPLATE,
)

# ─── Exercise 1 - Part 1: Set Up the OpenAI Client Start ──────────────────────
# ✓ Completed in Lab 1.
from openai import OpenAI

client = OpenAI()
# ─── Exercise 1 - Part 1: Set Up the OpenAI Client End ────────────────────────


app = Flask(__name__)
app.secret_key = "pages-unwritten-dev-key"

GENERATED_DIR = os.path.join("static", "generated")
AUDIO_DIR     = os.path.join("static", "generated", "audio")
os.makedirs(GENERATED_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)


# ─── Helpers ───────────────────────────────────────────────────────────────────

def reset_session(genre_id: str):
    session["genre"]   = genre_id
    session["player"]  = copy.deepcopy(PLAYER_START)
    session["history"] = []      # [{narration, speaker, choices, choice_made}]
    session["summary"] = ""      # Compressed "story so far" (Exercise 5)
    session["ending"]  = False


def current_act(scene_no: int) -> int:
    """Return which act the story is in based on scene_no."""
    if scene_no <= ACT_BOUNDARIES[1]:
        return 1
    if scene_no <= ACT_BOUNDARIES[2]:
        return 2
    return 3


# ─── Exercise 1 - Part 2: Build the Storyteller System Prompt Start ───────────
# ✓ Completed in Lab 1, then upgraded in Exercises 2 (JSON output) and 4
# (act guidance + flags_set + is_ending).
def build_storyteller_prompt(genre_id: str) -> str:
    genre  = GENRES[genre_id]
    player = session["player"]

    flags_seen   = player.get("flags") or {}
    flag_summary = ", ".join(f"{k}={v}" for k, v in flags_seen.items()) or "(none yet)"

    act_guidance = {
        1: "ACT 1 — SETUP: introduce the world, the protagonist's normal life, "
           "and the inciting event. Stakes are personal, not yet cosmic.",
        2: "ACT 2 — RISING ACTION: complications stack up. New characters, "
           "betrayals, surprises. Each scene should raise the stakes. NEVER end "
           "the story in act 2.",
        3: "ACT 3 — CLIMAX & RESOLUTION: drive toward the final confrontation. "
           "Within the next 2-4 scenes, set is_ending=true on the scene that "
           "delivers the final beat — triumph, tragedy, or twist. Do not extend "
           "past the natural ending point.",
    }[player["act"]]

    return f"""You are the storyteller for an interactive choose-your-own-adventure novel.

GENRE: {genre['name']}
TONE: {genre['tone']}
OPENING SETUP: {genre['opening_setup']}
PROTAGONIST: {genre['protagonist_archetype']}

CURRENT POSITION IN THE STORY:
  Scene number: {player['scene_no']}
  Act:          {player['act']} of 3
  Plot flags:   {flag_summary}

{act_guidance}

RULES:
- Write in second person ("You step out into the rain...").
- Each scene is 2-4 short paragraphs of vivid, atmospheric prose.
- Always end on a moment of decision UNLESS this is the final scene.
- Stay tightly inside the genre's tone and vocabulary.
- Honor the plot flags you've set in earlier scenes — do not contradict them.

OUTPUT FORMAT (REQUIRED):
You MUST respond with a single JSON object with exactly these keys:
{{
  "narration": "The full prose for this scene, 2-4 paragraphs.",
  "speaker":   "Narrator",
  "choices":   ["First choice.", "Second choice.", "Third choice."],
  "flags_set": {{"flag_name": true}},
  "is_ending": false
}}

CHOICE RULES:
- Provide 2 to 4 choices, each one short sentence in second person.
- If is_ending is true, return choices: [] (empty list — the story is over).

FLAG RULES:
- flags_set is a dict of plot facts you want to remember in later scenes.
  Example: {{"met_navigator": true, "owes_a_debt": true}}.
- Use snake_case names. Set true to record a fact, or omit to leave unchanged.
- Return {{}} if nothing new happened worth remembering.

ENDING RULES:
- Set is_ending=true ONLY on the scene that delivers the story's final beat.
- When is_ending is true, the narration should feel like a closed book —
  resolution, not cliffhanger.

Return ONLY the JSON object. No prose before or after, no markdown fences."""
# ─── Exercise 1 - Part 2: Build the Storyteller System Prompt End ─────────────


# ─── Exercise 3 - Part 1: Build the Image Prompt Start ────────────────────────
# ✓ Completed in Lab 2.
def build_image_prompt(scene_text: str, genre_id: str) -> str:
    """Turn the scene narration into a single image prompt for gpt-image-1."""
    genre = GENRES[genre_id]

    # Use the first ~280 chars of narration as the visual subject. Image models
    # do better with concise, vivid descriptions than with multi-paragraph prose.
    subject = scene_text.strip().replace("\n", " ")
    if len(subject) > 280:
        subject = subject[:280].rsplit(" ", 1)[0] + "…"

    return IMAGE_PROMPT_TEMPLATE.format(
        scene=subject,
        style=genre["visual_style"],
    )
# ─── Exercise 3 - Part 1: Build the Image Prompt End ──────────────────────────


# ─── Exercise 3 - Part 2: Generate and Cache the Scene Image Start ────────────
# ✓ Completed in Lab 2.
def generate_scene_image(scene_text: str, genre_id: str):
    """Return a URL path to a generated background image, or None."""
    # Cache key: hash of (genre, scene text) so identical scenes reuse the same PNG.
    key      = hashlib.sha1(f"{genre_id}|{scene_text}".encode("utf-8")).hexdigest()[:16]
    filename = f"{genre_id}_{key}.png"
    filepath = os.path.join(GENERATED_DIR, filename)
    url      = f"static/generated/{filename}"

    # Already generated? Return the cached URL — no API call.
    if os.path.exists(filepath):
        return url

    prompt = build_image_prompt(scene_text, genre_id)

    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1536x1024",
            n=1,
        )
        png_bytes = base64.b64decode(result.data[0].b64_json)
        with open(filepath, "wb") as f:
            f.write(png_bytes)
        return url
    except Exception as e:
        # If image gen fails for any reason, fall back to the genre gradient.
        print(f"[image] generation failed: {e}")
        return None
# ─── Exercise 3 - Part 2: Generate and Cache the Scene Image End ──────────────


# ─── Exercise 6 - Part 1: Generate Speech Narration Start ─────────────────────

def generate_narration_audio(text: str, genre_id: str):
    """Return a URL path to a generated mp3 of the narration, or None."""
    return None

# ─── Exercise 6 - Part 1: Generate Speech Narration End ───────────────────────


# ─── Exercise 5 - Part 2: Compress Story Memory Start ─────────────────────────

def maybe_compress_memory():
    """Summarise old history into session['summary'] when it gets long."""
    return  # No-op until Exercise 5.

# ─── Exercise 5 - Part 2: Compress Story Memory End ───────────────────────────


# ─── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/genres", methods=["GET"])
def list_genres():
    """Return the available genre presets for the title screen."""
    return jsonify({
        "genres": [
            {
                "id":       g["id"],
                "name":     g["name"],
                "subtitle": g["subtitle"],
                "icon":     g["icon"],
            }
            for g in GENRES.values()
        ],
        "default": DEFAULT_GENRE,
    })


@app.route("/api/begin", methods=["POST"])
def begin():
    """Start a new story in the chosen genre."""
    data     = request.get_json() or {}
    genre_id = data.get("genre", DEFAULT_GENRE)
    if genre_id not in GENRES:
        return jsonify({"error": f"Unknown genre: {genre_id}"}), 400

    reset_session(genre_id)
    scene = build_scene(genre_id, last_choice=None)
    save_scene(scene, choice_made=None)
    return jsonify({**scene, "genre": GENRES[genre_id]})


@app.route("/api/choice", methods=["POST"])
def choice():
    """Pick a choice from the current scene; the story moves forward."""
    if "genre" not in session:
        return jsonify({"error": "No story in progress. Pick a genre to begin."}), 400
    if session.get("ending"):
        return jsonify({"error": "The story has ended. Restart to begin again."}), 400

    data     = request.get_json() or {}
    idx      = int(data.get("choice_index", 0))
    history  = session.get("history") or []
    if not history:
        return jsonify({"error": "No scene to choose from."}), 400

    last_scene = history[-1]
    choices    = last_scene.get("choices") or []
    if not (0 <= idx < len(choices)):
        return jsonify({"error": f"Invalid choice index {idx}."}), 400

    chosen_text = choices[idx]
    history[-1]["choice_made"] = chosen_text
    session["history"] = history
    session.modified   = True

    scene = build_scene(session["genre"], last_choice=chosen_text)
    save_scene(scene, choice_made=None)
    return jsonify(scene)


@app.route("/api/restart", methods=["POST"])
def restart():
    """Clear the current story and return to the title screen."""
    session.clear()
    return jsonify({"ok": True})


# ─── Exercise 6 - Part 2: Speech API Route Start ──────────────────────────────
# In Exercise 6, this route turns scene narration into spoken audio. Until the
# student wires it up, generate_narration_audio() returns None so the frontend
# stays silent — no 404, no error, just no voice.

@app.route("/api/speech", methods=["POST"])
def speech():
    """Return a URL to a generated mp3 of the narration text, or None."""
    if "genre" not in session:
        return jsonify({"audio_url": None})
    data = request.get_json() or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"audio_url": None})
    audio_url = generate_narration_audio(text, session["genre"])
    return jsonify({"audio_url": audio_url})

# ─── Exercise 6 - Part 2: Speech API Route End ────────────────────────────────


# ─── Exercise 5 - Part 1: Stream the Narration Start ──────────────────────────

# ─── Exercise 5 - Part 1: Stream the Narration End ────────────────────────────


# ─── Scene generation ─────────────────────────────────────────────────────────

def build_scene(genre_id: str, last_choice: str | None) -> dict:
    """
    Build the next scene of the story.

    last_choice=None  → opening scene of the chosen genre.
    last_choice=text  → continuation, given what the player just chose.

    Returns a dict ready to send to the frontend with keys:
        narration, speaker, choices, image_url, scene_no, act, is_ending.
    """
    genre   = GENRES[genre_id]
    player  = session["player"]
    player["scene_no"] += 1
    player["act"]       = current_act(player["scene_no"])
    session["player"]   = player

    # ─── Exercise 1 - Part 3: Generate the Opening Scene Start ────────────────
    # ✓ Completed in Lab 1, then unified in Exercise 2 with continuations.
    # Build the message list: system prompt, then a replay of the story so far.
    messages = [
        {"role": "system", "content": build_storyteller_prompt(genre_id)},
    ]
    for entry in session.get("history", []):
        messages.append({"role": "assistant", "content": entry["narration"]})
        if entry.get("choice_made"):
            messages.append({
                "role":    "user",
                "content": f'The reader chose: "{entry["choice_made"]}". Continue.',
            })

    if last_choice is None:
        messages.append({"role": "user", "content": "Begin the story with the opening scene."})
    else:
        messages.append({
            "role":    "user",
            "content": f'The reader chose: "{last_choice}". Continue the story.',
        })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=500,
        temperature=0.85,
        response_format={"type": "json_object"},
    )
    payload   = json.loads(response.choices[0].message.content)
    narration = payload["narration"].strip()
    speaker   = payload.get("speaker", "Narrator")
    choices   = list(payload.get("choices", []))
    is_ending = False
    # ─── Exercise 1 - Part 3: Generate the Opening Scene End ──────────────────


    # ─── Exercise 2 - Part 1: Generate Next Scene with Choices Start ──────────
    # ✓ Completed in Lab 1 — JSON-mode call lives in the block above so opening
    # scenes and continuations share one code path.
    # ─── Exercise 2 - Part 1: Generate Next Scene with Choices End ────────────


    # ─── Exercise 4 - Part 1: Track Story Arc with Structured Output Start ────
    # ✓ Completed in Lab 2.
    # The model returned flags_set and is_ending in the JSON payload — apply them.
    new_flags = payload.get("flags_set") or {}
    if isinstance(new_flags, dict) and new_flags:
        player          = session["player"]
        player["flags"] = {**(player.get("flags") or {}), **new_flags}
        session["player"] = player
        session.modified  = True

    if payload.get("is_ending") is True:
        is_ending = True
        choices   = []
    # ─── Exercise 4 - Part 1: Track Story Arc with Structured Output End ──────


    # ─── Exercise 4 - Part 2: Detect Ending Conditions Start ──────────────────
    # ✓ Completed in Lab 2.
    # Soft nudge — deep into act 3, force closure before hitting the hard ceiling.
    # Gives the narration room to feel like a real ending rather than a cutoff.
    if player["act"] == 3 and player["scene_no"] >= SCENE_LIMIT - 3:
        is_ending = True
        choices   = []

    # Hard cap — absolute ceiling regardless of act or what the model returned.
    if player["scene_no"] >= SCENE_LIMIT:
        is_ending = True
        choices   = []
    # ─── Exercise 4 - Part 2: Detect Ending Conditions End ────────────────────


    image_url = generate_scene_image(narration, genre_id)

    if is_ending:
        session["ending"] = True
        session.modified  = True

    return {
        "narration":  narration,
        "speaker":    speaker,
        "choices":    choices,
        "image_url":  image_url,
        "scene_no":   player["scene_no"],
        "act":        player["act"],
        "is_ending":  is_ending,
        "genre_id":   genre_id,
    }


def save_scene(scene: dict, choice_made: str | None):
    """Append a scene to the running history."""
    history = session.get("history") or []
    history.append({
        "narration":   scene["narration"],
        "speaker":     scene["speaker"],
        "choices":     list(scene["choices"]),
        "image_url":   scene.get("image_url"),
        "scene_no":    scene["scene_no"],
        "act":         scene["act"],
        "is_ending":   scene["is_ending"],
        "choice_made": choice_made,
    })
    session["history"] = history
    session.modified   = True
    maybe_compress_memory()


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
