"""Exercise 2 — your first Claude API call from Python.

Fill in the TODO below with a single client.messages.create() call. Then
run the file three times back-to-back and read the varying output.

Run: `python src/first_call.py`
"""

import os

from dotenv import load_dotenv
import anthropic


def main() -> None:
    load_dotenv()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

    client = anthropic.Anthropic()

    # TODO: replace this stub with a real call to client.messages.create().
    # Use the `model` variable above. Set max_tokens=64. Ask Claude to
    # suggest a single short name for Orion Analytics' new client dashboard,
    # and to reply with just the name (no preamble).
    #
    # The call should return a Message object; assign it to `response`.
    #
    # HINT: the client.messages.create() signature is:
    #   client.messages.create(
    #       model=<str>,
    #       max_tokens=<int>,
    #       messages=[{"role": "user", "content": "<your prompt>"}],
    #   )
    response = None  # <-- replace this line

    if response is None:
        raise SystemExit(
            "first_call.py: the TODO in main() is still a stub. Replace it with a "
            "real client.messages.create(...) call, then re-run."
        )

    # The response body is a LIST of content blocks. Most calls return a
    # single text block, but adaptive-thinking models (Opus 5.5, sometimes
    # Fable 5.1) can emit a `ThinkingBlock` FIRST — so `response.content[0]`
    # is not always the text. Filter for the first block whose type is
    # "text" to be safe across all models:
    text = next((b.text for b in response.content if b.type == "text"), "")
    print(text)


if __name__ == "__main__":
    main()
