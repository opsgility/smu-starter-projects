"""Exercise 2 — build a small multi-turn REPL against Claude.

Fill in the TODOs to (a) supply a good system prompt for an Orion Analytics
support-triage helper, and (b) build the conversation-state loop.

Run: `python src/repl.py`. Type messages at the prompt. Press Enter on an
empty line (or Ctrl+C) to exit.
"""

import os
import sys

from dotenv import load_dotenv
import anthropic


# TODO 1: write a good system prompt for an on-call support-triage helper
# at Orion Analytics. It should tell Claude: who it's talking to (an on-call
# engineer, not a customer), what its job is (categorize incoming tickets
# into Billing / Technical / Feature Request / Other, and suggest next
# steps), and what tone to use (concise, direct, no filler). Keep it under
# 100 words.
SYSTEM_PROMPT = "TODO: replace this with your system prompt."


def main() -> None:
    load_dotenv()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

    client = anthropic.Anthropic()

    # Conversation state — a list of {"role": ..., "content": ...} dicts.
    # This IS Claude's memory of the conversation; nothing else persists.
    messages: list[dict] = []

    print(f"Orion triage REPL (model={model}). Empty line to exit.\n")

    while True:
        try:
            user_input = input("you: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            break

        # TODO 2: append the user's message to the `messages` list. The
        # shape is {"role": "user", "content": <str>}.
        # messages.append(...)  <-- your line here

        # TODO 3: call client.messages.create() with:
        #   - model=model
        #   - max_tokens=512
        #   - system=SYSTEM_PROMPT   (this is a TOP-LEVEL parameter, NOT a
        #                             message with role="system" — see notes)
        #   - messages=messages
        # Assign the result to `response`.
        response = None  # <-- replace this line
        if response is None:
            print("(TODOs 2 and 3 still stubbed — fill them in and retry.)", file=sys.stderr)
            break

        # Adaptive-thinking models (Opus 5.5, sometimes Fable 5.1) may emit a
        # ThinkingBlock first — filter for the text block explicitly so a
        # model swap via ANTHROPIC_MODEL doesn't crash mid-conversation.
        assistant_text = next((b.text for b in response.content if b.type == "text"), "")
        print(f"claude: {assistant_text}\n")

        # TODO 4: append Claude's reply to `messages` so the next turn sees
        # it. The shape is {"role": "assistant", "content": <str>}. If you
        # skip this step, every turn is treated as a fresh conversation —
        # Claude will not remember what it just said.
        # messages.append(...)  <-- your line here


if __name__ == "__main__":
    main()
