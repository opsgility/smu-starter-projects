# Node.js Codespace Starter

A pre-configured development environment for GitHub Codespaces.

## Files

- `.devcontainer/devcontainer.json` — Dev container configuration (Node.js 18 + GitHub CLI)
- `app.js` — Simple Node.js app to verify the environment works

## Devcontainer Features

This devcontainer includes:
- **Node.js 18** — Pre-installed runtime
- **GitHub CLI** — `gh` command available in the terminal
- **VS Code extensions** — ESLint, Prettier, GitHub Copilot, GitHub Pull Requests

## Running the App

```bash
node app.js
```

## What You Will Do

In the exercises you will:
1. Review this `.devcontainer/devcontainer.json` configuration
2. Modify the devcontainer to add new tools or extensions
3. Create a Codespace from this repository on GitHub.com
4. Explore the Codespace environment (terminal, extensions, ports)
5. Understand the difference between **Codespaces** (full cloud VM with terminal) and **github.dev** (browser editor only — no terminal)
6. Manage Codespace lifecycle: stop, restart, and delete with `gh codespace` commands

## Key Devcontainer Properties

| Property | Purpose |
|----------|---------|
| `image` | Base Docker image for the environment |
| `features` | Additional tools to install (GitHub CLI, Docker, etc.) |
| `customizations.vscode.extensions` | VS Code extensions auto-installed |
| `postCreateCommand` | Command that runs after the container is created |
| `remoteUser` | The user inside the container |
