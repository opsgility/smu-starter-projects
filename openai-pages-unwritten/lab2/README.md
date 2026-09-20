# Pages Unwritten — Lab 2

A choose-your-own-adventure visual novel powered by the OpenAI API.

This folder is the **Lab 2 starting point**. Exercises 1 (storyteller) and 2 (JSON-mode branching choices) from Lab 1 are already implemented in `app.py`. In Lab 2 you'll add:

3. Per-scene background art with `gpt-image-1`
4. Story-arc tracking with `flags_set` and `is_ending` plus a hard scene limit

## Run it

```
python app.py
```

Then open the URL shown in the VS Code Ports panel.

## Project layout

```
.
├── app.py              # Flask server (Ex 1+2 already wired up; Ex 3+4 placeholders)
├── story_data.py       # Genre presets, fallback scenes, tuning constants
├── requirements.txt
├── static/
│   ├── css/style.css
│   ├── js/novel.js
│   └── generated/      # AI-generated scene images cache (Exercise 3)
│       └── audio/      # AI-generated narration mp3 cache (Exercise 6 / Lab 3)
└── templates/
    └── index.html
```
