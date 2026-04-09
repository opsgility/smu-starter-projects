# URL Shortener — Code Review Starter

A Node.js URL shortener service. The code works but is missing JSDoc documentation — a reviewer will request it.

## Files

- `app.js` — URL shortener with validation (missing JSDoc — to be added via PR review)
- `test.js` — Full test suite (11 tests)
- `package.json` — Node.js project config

## Running Tests

```bash
node test.js
# or
npm test
```

## What You Will Do

In the exercises you will practice the full code review workflow:
1. List and view open pull requests with `gh pr list` and `gh pr view`
2. Examine PR diffs with `gh pr diff`
3. Add a general comment with `gh pr comment`
4. Submit a formal **request for changes** review with `gh pr review --request-changes`
5. Check out the PR branch and add JSDoc comments to `app.js` (addressing the review)
6. Push the fix — the PR updates automatically
7. Approve the PR with `gh pr review --approve`
8. Merge using **squash strategy** with `gh pr merge --squash`
9. Create a second PR for click tracking and merge using **rebase strategy**
10. Verify that linked issues auto-close when PRs are merged

## Merge Strategies

| Strategy | Flag | Result |
|----------|------|--------|
| Merge commit | `--merge` | Preserves all commits + adds a merge commit |
| Squash | `--squash` | Combines all PR commits into one clean commit |
| Rebase | `--rebase` | Replays commits on top of main — linear history |
