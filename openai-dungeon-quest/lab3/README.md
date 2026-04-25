# Dungeon Quest — Lab 3

A choose-your-path text RPG powered by the OpenAI API.

This folder is the **Lab 3 starting point**. Exercises 1-4 from Labs 1 and 2 are already implemented in `app.py`: the GM with structured JSON output, NPC dialogue with per-character histories, and combat with AI narration and enemy taunts. In Lab 3 you'll add:

5. Streaming narration over Server-Sent Events with JSON-aware token forwarding + history summarization
6. Voiced narration with the OpenAI Speech (TTS) API, mapped per character

## Run it

```
python app.py
```

Then open the URL shown in the VS Code Ports panel.

## Project layout

```
.
├── app.py              # Flask server (Ex 1-4 already wired up; Ex 5+6 placeholders)
├── game_data.py        # World, NPCs, enemies, room layout
├── generate_assets.py  # One-off image generator for room backgrounds
├── requirements.txt
├── static/
│   ├── assets/         # Pre-generated room backgrounds + character sprites
│   ├── css/style.css
│   ├── js/game.js
│   └── generated/
│       └── audio/      # AI-generated TTS mp3 cache (Exercise 6)
└── templates/
    └── index.html
```
