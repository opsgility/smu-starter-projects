# agy-100-l5 — Meridian Devworks shared TypeScript utilities (empty)

Starter project for **AGY-100 Lesson 10 — "Author a SKILL.md and try /boost"** in the Google Antigravity IDE path.

You're playing **Dana** at Meridian Devworks. The team is spinning up a new internal utilities package for shared TypeScript code. The project is intentionally empty — just a `tsconfig.json`, a `package.json`, and an empty `src/` directory. Your task in the lab is to author a `SKILL.md` that encodes a specific convention, prompt Antigravity to create a new module, verify the agent respects your SKILL.md, and then try `/boost` on a tricky refactor so you can see the reasoning-depth difference with your own eyes.

## Shape

- `package.json` — `type: "module"`, TypeScript 5.4 devDep, `build` + `typecheck` scripts.
- `tsconfig.json` — strict mode on, ES2022 target, source in `src/`, output in `dist/`.
- `src/.gitkeep` — keeps the empty directory in git.
- `README.md` — this file.

Everything else — your SKILL.md, your first module, the agent's `/boost` work — the student creates during the lab.

## Lab convention to encode in SKILL.md

The lab's suggested convention is "every TypeScript file starts with a path header comment of the form `// <path/from/src>`". This is deliberately simple to make it easy to verify the agent respected it (open the generated file and look at line 1). You can pick a different convention if you prefer; just make it a convention the agent would NOT follow by default and would benefit from being told explicitly.

## Running the project

Before any lab work:

```
npm install
```

To type-check:

```
npm run typecheck
```

To build (after the agent writes code):

```
npm run build
```

## Deployment path

This starter is auto-downloaded onto the lab VM at `C:\labs\agy-100-l5\` via the SkillMeUp `downloadfiles.ps1` CSE pipeline.

Related: `Plans/ANTIGRAVITY_IDE_PATH_PLAN.md` in the `opsgilitylabs-core-claude` repo.
