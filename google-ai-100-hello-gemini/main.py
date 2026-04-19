"""
Google AI 100 — Lesson 1: Your First Vertex AI Call

Complete the TODOs to call Gemini on Vertex AI.
"""
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")


def main() -> None:
    if not PROJECT:
        raise SystemExit(
            "GOOGLE_CLOUD_PROJECT is not set. Copy .env.example to .env and set it,\n"
            "or run:  export GOOGLE_CLOUD_PROJECT=$(gcloud config get project)"
        )

    # TODO (Part 2): instantiate the Vertex AI-backed Gen AI client
    # Hint: genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
    client = None

    # TODO (Part 2): call client.models.generate_content with model="gemini-2.5-flash"
    # Ask: "In one sentence, explain what Vertex AI is to a new developer."
    response = None

    # TODO (Part 2): print response.text
    # TODO (Part 3): print response.usage_metadata (input/output/total tokens)
    print("Not implemented yet — complete the TODOs in main.py")


if __name__ == "__main__":
    main()
