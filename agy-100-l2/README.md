# agy-100-l2 — Meridian Devworks geometry helper starter

Starter project for **AGY-100 Lesson 4 — "Steer the agent through artifact feedback"** in the Google Antigravity IDE path.

You're playing **Priya**, a senior engineer at Meridian Devworks. Priya noticed the warehouse team's pallet-footprint numbers looked low and traced the problem back to the `Rectangle.area()` method in this tiny geometry helper. The method has a bug — AND the test for it is wrong in a way that lets the buggy behavior pass. Your task in the lab is to drive Google Antigravity to find both bugs, and to steer the agent via inline feedback to also handle the degenerate case of negative dimensions.

## Shape

- `rectangle.py` — a `Rectangle` class with `area()` and `perimeter()`. The `area()` method is wrong (returns `width + height` instead of `width * height`). An author note in a comment hints at the issue.
- `tests/test_rectangle.py` — one wrong test (`test_area_small` asserts `area() == 7` for a 3×4 rectangle, matching the bug) and one correct test (`test_perimeter`).
- `pyproject.toml` — basic project metadata.
- `README.md` — this file.

## Current behavior

```
pytest tests/
.. 2 passed
```

(Both tests pass because the broken `area()` returns `3 + 4 = 7`, which happens to match the test's wrong expected value. The suite is green, but the production math is still wrong — a classic "the test proves the implementation matches the test, not that the implementation is correct" trap.)

## Target behavior after the lab

```
pytest tests/
...... 3+ passed (expanded coverage, including negative-dimension handling)
```

- `area()` returns `width * height`.
- `test_area_small` asserts `area() == 12` (3 × 4 = 12), not 7.
- A new test covers `area()` with negative dimensions, which the agent's revised plan addresses after Priya steers it via inline feedback.

## Deployment path

This starter is auto-downloaded onto the lab VM at `C:\labs\agy-100-l2\` via the SkillMeUp `downloadfiles.ps1` CSE pipeline. Students never clone this repo manually.

Related: `Plans/ANTIGRAVITY_IDE_PATH_PLAN.md` in the `opsgilitylabs-core-claude` repo.
