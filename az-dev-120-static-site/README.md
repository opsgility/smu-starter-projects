# az-dev-120-static-site

Anchorline product listing — a tiny static SPA that lives in the `$web` container.

## Files

- `site/index.html` — the entry page (no-cache)
- `site/app.abc123.js` — content-hashed JS (1-year immutable cache)
- `site/app.abc123.css` — content-hashed CSS (1-year immutable cache)
- `site/404.html` — fallback

## Deploy

```bash
./scripts/deploy.sh <storage-account>
```

The script enables static-website hosting on the account, uploads the fingerprinted assets with a 1-year `Cache-Control: public, max-age=31536000, immutable`, and uploads the HTML with `no-cache`.
