# Actions Demo — GitHub Actions Starter

A simple Node.js app with tests, ready for a CI/CD pipeline.

## Files

- `app.js` — Simple app with `add` and `multiply` functions
- `test.js` — Test runner using Node's built-in `process.exit` for CI feedback

## Running Tests Locally

```bash
node test.js
```

## What You Will Do

In the exercises you will:
1. Push this project to GitHub
2. Create a `.github/workflows/ci.yml` workflow that runs on push and pull requests
3. Use `actions/checkout@v4` and `actions/setup-node@v4` marketplace actions
4. Run `node test.js` as a workflow step and watch it pass
5. Watch the workflow run live with `gh run watch`
6. Create a feature branch that adds a `subtract` function — watch CI run on the PR
7. Intentionally add a buggy `divide` function and watch CI catch the bug
8. Fix the bug and see the workflow go green

The CI pipeline runs `node test.js` — a non-zero exit code means failure.
