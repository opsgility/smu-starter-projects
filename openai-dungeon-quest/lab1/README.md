# Dungeon Quest — Lab 1

A choose-your-path text RPG powered by the OpenAI API.

This folder is the **Lab 1 starting point** — the UI, routing, and game state are in place; no OpenAI calls have been wired up yet. The course is split across three labs, six exercises:

- **Lab 1 (this folder)** — Exercises 1-2: GM narration with conversation history + NPC dialogue with per-character system prompts
- **Lab 2** — Exercises 3-4: combat with AI narrator + structured JSON output
- **Lab 3** — Exercises 5-6: streaming with bounded memory + voiced narration with TTS

Each lab folder ships with the previous lab's exercises pre-completed in `app.py`, so you can pick up exactly where you left off.

## Run it

```
python app.py
```

Then open the URL shown in the VS Code Ports panel.

## Project layout

```
.
├── app.py              # Flask server + exercise placeholders
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
