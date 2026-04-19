# URL Shortener — Pull Requests Starter

A simple URL shortener service built with Node.js.

## Files

- `urlShortener.js` — Basic URL shortener with `shorten` and `resolve` functions (no URL validation yet)

## Features

- Shorten long URLs to a short ID
- Redirect short URLs to original destinations

## What You Will Do

In the exercises you will practice creating and reviewing pull requests:
1. Push this project to GitHub and create issues for planned features
2. Create a `feature/url-validation` branch
3. Add URL validation (must start with `http://` or `https://`)
4. Add a `test.js` file with comprehensive validation tests
5. Push the branch and open a pull request with `gh pr create` (linking it to your issue)
6. Review the PR diff with `gh pr diff` and add comments
7. Merge the PR and watch the linked issue auto-close
8. Practice code review: request changes, approve, and explore squash vs. rebase merge strategies

## Running the App

```bash
node -e "const {shorten, resolve} = require('./urlShortener'); const result = shorten('https://github.com'); console.log('Short ID:', result.id); console.log('Resolved:', resolve(result.id));"
```
