# gh200-contexts-expressions — Contexts, Expressions, and Advanced YAML

Starter project for **GH-200 Module 3: Contexts Expressions and Advanced YAML** hands-on lab.

## What's here

| File | Purpose |
|---|---|
| `package.json` | Node project with `test` and `build` scripts your workflow steps will reference |
| `src/app.js` | `greet(name, env)` — accepts inputs that pair naturally with `${{ inputs.* }}` / `${{ env.* }}` |
| `tests/test.js` | Smoke test the workflow can run |
| `.github/workflows/` | Empty — you'll create `contexts.yml` through the exercise |

## What you will build

Workflows demonstrating:

1. `github`, `runner`, `env`, `vars`, `secrets`, `inputs`, `matrix`, `needs`, `job`, `steps` contexts
2. Expression operators (`==`, `!=`, `&&`, `||`, `!`), functions (`contains()`, `startsWith()`, `hashFiles()`), and type coercion
3. YAML anchors (`&`), aliases (`*`), and merge keys (`<<:`) to dry up repeated mappings
4. Static-parse vs runtime-evaluation distinction
5. Safe expression patterns that prevent secret leakage in logs

## Skip Task 1

This starter replaces "Task 1: Create the Workspace Repository". Push this folder to a new GitHub repo and start at Task 2.
