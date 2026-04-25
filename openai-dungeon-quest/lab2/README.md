# Dungeon Quest — Lab 2

A choose-your-path text RPG powered by the OpenAI API.

This folder is the **Lab 2 starting point**. Exercises 1-2 from Lab 1 are already implemented in `app.py`: the OpenAI client, the GM system prompt, the `/api/action` endpoint with `ROOM_CHANGE:` regex parsing, and the `/api/talk` endpoint with per-character histories. In Lab 2 you'll add:

3. Combat that actually hurts — damage calculations + AI-narrated rounds + in-character enemy taunts + defeat handling
4. Structured output (JSON mode) — replaces the fragile `ROOM_CHANGE:` regex with a JSON schema covering room changes, item discovery, and gold drops

## Run it

```
python app.py
```

Then open the URL shown in the VS Code Ports panel.

## Project layout

```
.
├── app.py              # Flask server (Ex 1+2 already wired up; Ex 3+4 placeholders)
├── game_data.py        # World, NPCs, enemies, room layout
├── generate_assets.py  # One-off image generator for room backgrounds
├── requirements.txt
├── static/
│   ├── assets/         # Pre-generated room backgrounds + character sprites
│   ├── css/style.css
│   ├── js/game.js
│   └── generated/
│       └── audio/      # AI-generated TTS mp3 cache (Exercise 6 / Lab 3)
└── templates/
    └── index.html
```
