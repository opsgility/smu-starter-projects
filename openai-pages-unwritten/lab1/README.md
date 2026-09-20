# Pages Unwritten — Lab 1

A choose-your-own-adventure visual novel powered by the OpenAI API.

This folder is the **Lab 1 starting point** — the UI, routing, and game state are in place; no OpenAI calls have been wired up yet. The course is split across three labs, six exercises:

- **Lab 1 (this folder)** — Exercises 1-2: storyteller system prompt + JSON-mode branching choices
- **Lab 2** — Exercises 3-4: `gpt-image-1` backgrounds + structured story-arc tracking
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
├── story_data.py       # Genre presets, fallback scenes, tuning constants
├── requirements.txt
├── static/
│   ├── css/style.css
│   ├── js/novel.js
│   └── generated/      # AI-generated scene images cache (Exercise 3 / Lab 2)
│       └── audio/      # AI-generated narration mp3 cache (Exercise 6 / Lab 3)
└── templates/
    └── index.html
```
