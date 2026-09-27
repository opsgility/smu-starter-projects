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

    # The response body is a list of content blocks. For a simple text call
    # like this one there is exactly one block, of type 'text'.
    print(response.content[0].text)


if __name__ == "__main__":
    main()
