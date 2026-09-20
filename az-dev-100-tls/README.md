# az-dev-100-tls

Anchorline Outdoors storefront — starter for the TLS hardening module.

## Endpoints

- `GET /health`
- `GET /version`
- `GET /tls` — reports the request scheme, `X-Forwarded-Proto`, and (when present) `X-Forwarded-TlsVersion` header set by App Service front end
- `GET /headers` — echoes the response headers the app WILL send (used to verify HSTS header presence after the exercise adds it)

## What you'll do

- Enforce TLS 1.3 minimum on the Web App (ARM update)
- Add HSTS middleware to `Program.cs`
- Enable HTTP/3
- Verify each with `openssl s_client` and `curl` from your terminal
