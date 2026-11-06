# agy-100-l1 — Meridian Devworks CLI starter

Starter project for **AGY-100 Lesson 2 — "Sign in, create a Project, drive your first task"** in the Google Antigravity IDE path.

You're playing **Dana**, a senior engineer at Meridian Devworks (a fictional small-business logistics SaaS team). The team's internal `meridian-cli` command-line tool currently only supports `--inspect <tracking>`. Your task in the lab is to drive Google Antigravity to add a `--version` flag that prints both the app version from `pyproject.toml` and the current Python runtime version.

## Shape

- `cli.py` — the CLI entry point. Uses `argparse`. One flag today (`--inspect`); the lab adds `--version`.
- `pyproject.toml` — project metadata. `version = "1.0.0"`.
- `README.md` — this file.

## Current behavior

```
python cli.py --inspect SHIP123
[meridian-cli] inspecting shipment SHIP123
```

## Target behavior after the lab

```
python cli.py --version
meridian-cli 1.0.0 (Python 3.12.x)
```

Plus a smoke test under `tests/test_cli.py` that invokes `--version` and asserts both version components print.

## Deployment path

This starter is auto-downloaded onto the lab VM at `C:\labs\agy-100-l1\` via the SkillMeUp `downloadfiles.ps1` CSE pipeline. Students never clone this repo manually.

Related: `Plans/ANTIGRAVITY_IDE_PATH_PLAN.md` in the `opsgilitylabs-core-claude` repo.
