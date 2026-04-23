"""
Google AI 100 — Lesson 2: verify your auth setup.

Runs one Gemini call. On success, prints the model response and the
authenticated principal. On failure, prints the full error so you can
recognize the error class (DefaultCredentialsError, PERMISSION_DENIED,
SERVICE_DISABLED, ...).
"""
import os
import sys
import traceback

import google.auth
from google import genai

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT") or ""
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")


def print_principal() -> None:
    try:
        creds, project = google.auth.default()
        principal = getattr(creds, "service_account_email", None) or getattr(
            creds, "signer_email", None
        )
        print(f"[auth] ADC project: {project}")
        print(f"[auth] principal  : {principal or 'user credentials'}")
    except Exception as exc:
        print(f"[auth] default() failed: {exc}")


def main() -> int:
    if not PROJECT:
        print("[config] GOOGLE_CLOUD_PROJECT is not set.")
        print("         export GOOGLE_CLOUD_PROJECT=$(gcloud config get project)")
        return 2

    print_principal()

    try:
        client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
        response = client.models.generate_content(
            model="gemini-3.1-flash",
            contents="Respond with exactly: AUTH OK",
        )
        print(f"[gemini] response: {response.text.strip()}")
        print("[result] SUCCESS")
        return 0
    except Exception:
        print("[result] FAILURE — full traceback follows so you can recognize the error class:")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
