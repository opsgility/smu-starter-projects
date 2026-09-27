"""Exercise 4 — convert the REPL to a streaming response.

Fill in the TODOs to stream Claude's reply token-by-token instead of
waiting for the whole message to come back at once.

Run: `python src/streaming.py`. Type messages at the prompt.
"""

import os
import sys

from dotenv import load_dotenv
import anthropic


SYSTEM_PROMPT = (
    "You are a support-triage helper for Orion Analytics' on-call engineers. "
    "Categorize each incoming ticket into one of: Billing, Technical, Feature "
    "Request, Other. Suggest one specific next step. Keep replies under 4 "
    "sentences. No filler."
)


def main() -> None:
    load_dotenv()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

    client = anthropic.Anthropic()
    messages: list[dict] = []

    print(f"Orion triage REPL (streaming, model={model}). Empty line to exit.\n")

    while True:
        try:
            user_input = input("you: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            break

        messages.append({"role": "user", "content": user_input})

        print("claude: ", end="", flush=True)

        # TODO 1: open a streaming request with client.messages.stream(...).
        # Use it as a context manager (`with client.messages.stream(...) as stream:`).
        # Pass the same model / max_tokens / system / messages you used in
        # repl.py.
        #
        # HINT: skeleton
        #   with client.messages.stream(
        #       model=model,
        #       max_tokens=512,
        #       system=SYSTEM_PROMPT,
        #       messages=messages,
        #   ) as stream:
        #       for text in stream.text_stream:
        #           print(text, end="", flush=True)
        #       final = stream.get_final_message()
        #
        # After the `with` block, `final` is the assembled Message object —
        # filter for the text block (adaptive-thinking models like Opus 5.5
        # may prepend a ThinkingBlock) to grab the whole assistant reply and
        # append it to `messages` (TODO 2), and inspect final.stop_reason
        # and final.usage to see what happened (TODO 3). Note: streaming's
        # `stream.text_stream` above ALREADY filters to only text deltas, so
        # what you see printed live is text-only; the ThinkingBlock only
        # shows up in `final.content` for post-hoc inspection.
        final = None  # <-- replace with real streaming call

        if final is None:
            print("\n(TODO 1 still stubbed — implement the streaming call and retry.)",
                  file=sys.stderr)
            break

        assistant_text = next((b.text for b in final.content if b.type == "text"), "")
        print()  # newline after the streamed text

        # TODO 2: append the assistant's reply to `messages`.
        # messages.append({"role": "assistant", "content": assistant_text})

        # TODO 3: print the stop_reason and token usage. Real production
        # apps log both — stop_reason so you can distinguish a natural
        # finish (end_turn) from a truncation (max_tokens), and usage so
        # you can track cost per user.
        # print(f"  stop_reason={final.stop_reason}  usage={final.usage}")


if __name__ == "__main__":
    main()
