# Lesson 8 Starter: Resources, URI Templates, and Prompts

This starter contains the **completed code from Lessons 4 and 6** (greet, add_numbers, fetch_url, format_json, calculate — all fully implemented with input + output schemas) plus a `data/` directory with sample wiki content and an outage playbook.

## What you will build

1. **Static resource** at `playbook://outage` reading `data/playbooks/outage.md`.
2. **Templated resource** at `wiki://{slug}` reading `data/wiki/{slug}.md`.
3. **Prompt template** `incident-triage` (severity + service args, returns a 2-message conversation).
4. *(Bonus)* Wire up `notifications/resources/list_changed` when the wiki contents change.

## How to start

```
npm install
npm run build
npm run inspect
```

Then add to Claude Code at project scope so the config is committed:

```
claude mcp add --scope project resources-prompts node ./dist/server.js
```

In Claude Code, type `@play` — `playbook://outage` should appear in the autocomplete. Type `/incident` — your `/mcp__resources-prompts__incident-triage` prompt should appear.
