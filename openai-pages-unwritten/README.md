# Pages Unwritten

A choose-your-own-adventure visual novel powered by the OpenAI API.

This is the starter project — the UI, routing, and game state are already in place. Across six exercises you will progressively wire up the OpenAI API to:

1. Generate the opening scene of any genre
2. Branch the story with structured-output choices
3. Paint each scene with `gpt-image-1`
4. Track act, plot flags, and ending conditions
5. Stream the narration and compress story memory
6. Voice the narration with the OpenAI Speech (TTS) API

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
│   └── generated/      # AI-generated scene images cache (Exercise 3)
│       └── audio/      # AI-generated narration mp3 cache (Exercise 6)
└── templates/
    └── index.html
```
