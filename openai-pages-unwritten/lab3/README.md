# Pages Unwritten — Lab 3

A choose-your-own-adventure visual novel powered by the OpenAI API.

This folder is the **Lab 3 starting point**. Exercises 1-4 from Labs 1 and 2 are already implemented in `app.py`: the storyteller, JSON-mode branching choices, `gpt-image-1` backgrounds, and three-act structure with ending detection. In Lab 3 you'll add:

5. Streaming narration over Server-Sent Events with bounded memory compression
6. Voiced narration with the OpenAI Speech (TTS) API, mapped per genre

## Run it

```
python app.py
```

Then open the URL shown in the VS Code Ports panel.

## Project layout

```
.
├── app.py              # Flask server (Ex 1-4 already wired up; Ex 5+6 placeholders)
├── story_data.py       # Genre presets, fallback scenes, tuning constants
├── requirements.txt
├── static/
│   ├── css/style.css
│   ├── js/novel.js
│   └── generated/      # Cached gpt-image-1 PNGs (already generating)
│       └── audio/      # AI-generated narration mp3 cache (Exercise 6)
└── templates/
    └── index.html
```
