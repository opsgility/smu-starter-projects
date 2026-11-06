# agy-100-l3 — Meridian Devworks greeter Flask app

Starter project for **AGY-100 Lesson 6 — "Autopilot refactor + browser-driven QA"** in the Google Antigravity IDE path.

You're playing **Marcus** at Meridian Devworks. The team switched its naming convention from `app_name` to `service_name` three months ago, but `app.py` never got updated — the variable still reads as `app_name` across five usage sites in the file. Your task in the lab has two beats: rename the variable using Antigravity's **Tab features** (Supercomplete should propagate the rename across all five sites in one Tab), and then start the Flask dev server and prompt Antigravity's **Browser Subagent** to verify the home page renders correctly.

## Shape

- `app.py` — a Flask application with one `GET /` route. The variable `app_name = "meridian-greeter"` is used in five positions in this one file (the welcome `<h1>`, the subtitle, the log message in `home()`, and the startup `print`). All within the current file — exactly Supercomplete's sweet spot.
- `requirements.txt` — just `flask>=3.0.0`.
- `README.md` — this file.

## Current behavior

```
python app.py
[meridian] starting meridian-greeter on http://127.0.0.1:5000
```

Then `curl http://127.0.0.1:5000`:
```
<h1>Welcome to meridian-greeter</h1><p>Hello from Meridian Devworks!</p><p><small>Service: meridian-greeter</small></p>
```

## Target behavior after the lab

After the Tab-features rename, `app_name` is `service_name` everywhere in the file. The home page HTML and the log message both reference `service_name`. The content ("meridian-greeter") does not change — just the variable identifier.

After the Browser Subagent verification, Antigravity's walkthrough contains a screenshot of the running home page confirming the "Welcome to meridian-greeter" header renders correctly, plus a short action video of the subagent's navigation.

## Deployment path

This starter is auto-downloaded onto the lab VM at `C:\labs\agy-100-l3\` via the SkillMeUp `downloadfiles.ps1` CSE pipeline.

Related: `Plans/ANTIGRAVITY_IDE_PATH_PLAN.md` in the `opsgilitylabs-core-claude` repo.
