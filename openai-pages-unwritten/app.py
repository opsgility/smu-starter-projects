"""
Pages Unwritten — Flask server (base starter project, no OpenAI yet).

Run:
    python app.py

Then open the URL shown in the VS Code Ports panel.
"""
import copy, hashlib, json, os
from flask import Flask, render_template, request, jsonify, session
from story_data import (
    GENRES, DEFAULT_GENRE, PLAYER_START,
    FALLBACK_OPENINGS, ACT_BOUNDARIES, SCENE_LIMIT,
    IMAGE_PROMPT_TEMPLATE,
)

# ─── Exercise 1 - Part 1: Set Up the OpenAI Client Start ──────────────────────

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

# ─── Exercise 1 - Part 2: Build the Storyteller System Prompt End ─────────────


# ─── Exercise 3 - Part 1: Build the Image Prompt Start ────────────────────────

# ─── Exercise 3 - Part 1: Build the Image Prompt End ──────────────────────────


# ─── Exercise 3 - Part 2: Generate and Cache the Scene Image Start ────────────

def generate_scene_image(scene_text: str, genre_id: str):
    """Return a URL path to a generated background image, or None."""
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
    # Until you wire up the OpenAI API, every scene falls back to canned text.
    # In Exercise 1 you'll generate `narration` for the opening scene from the
    # storyteller prompt. In Exercise 2 you'll switch to JSON-mode so the LLM
    # also returns the next set of choices.
    if last_choice is None:
        opening   = FALLBACK_OPENINGS[genre_id]
        narration = opening["narration"]
        speaker   = opening["speaker"]
        choices   = list(opening["choices"])
    else:
        narration = (
            f"You chose: \"{last_choice}\".\n\n"
            "[The story would continue from here. Wire up the OpenAI API in "
            "Exercise 2 so the storyteller can decide what happens next.]"
        )
        speaker = "Narrator"
        choices = []
    is_ending = (last_choice is not None)  # Starter: chapter ends after one choice.
    # ─── Exercise 1 - Part 3: Generate the Opening Scene End ──────────────────


    # ─── Exercise 2 - Part 1: Generate Next Scene with Choices Start ──────────
    # In Exercise 2, replace the block above with a single chat.completions
    # call that returns BOTH narration and choices via JSON-mode. After that,
    # this section becomes the post-processing step: parse the JSON, set
    # `narration`, `speaker`, `choices` from the model's response.
    # ─── Exercise 2 - Part 1: Generate Next Scene with Choices End ────────────


    # ─── Exercise 4 - Part 1: Track Story Arc with Structured Output Start ────
    # In Exercise 4, extend the JSON schema so the LLM also returns:
    #   - flags_set:  dict of plot flags it wants to remember
    #   - is_ending:  true when this scene is the final beat of the story
    # Apply them to session here.
    # ─── Exercise 4 - Part 1: Track Story Arc with Structured Output End ──────


    # ─── Exercise 4 - Part 2: Detect Ending Conditions Start ──────────────────
    # In Exercise 4, also force `is_ending = True` once we hit SCENE_LIMIT,
    # so the story always closes even if the model wants to keep going.
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
