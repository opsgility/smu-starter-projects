#!/usr/bin/env bash
# Quick post-deploy smoke test used in the lab "Verify" section.
set -euo pipefail

if [[ -z "${APP_URL:-}" ]]; then
  echo "APP_URL must be set (e.g. https://nw-classifier-xxxx.azurewebsites.net)" >&2
  exit 1
fi

echo "[1/3] GET $APP_URL/healthz"
curl -fsS "$APP_URL/healthz"
echo

echo "[2/3] GET $APP_URL/secrets-check"
curl -fsS "$APP_URL/secrets-check" | python -m json.tool

echo "[3/3] POST $APP_URL/classify"
curl -fsS -X POST "$APP_URL/classify" \
  -H 'content-type: application/json' \
  -d '{"shipment_id":"verify-1","description":"crate crushed in transit"}' | python -m json.tool
