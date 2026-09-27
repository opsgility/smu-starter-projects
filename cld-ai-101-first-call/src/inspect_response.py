"""Exercise 3 — inspect a Claude response.

Fill in the TODOs below to print the parts of the response that matter
for a working engineer: the text content, the stop_reason, and the token
usage bill.

Run: `python src/inspect_response.py`
"""

import os

from dotenv import load_dotenv
import anthropic


def main() -> None:
    load_dotenv()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

    client = anthropic.Anthropic()

    response = client.messages.create(
        model=model,
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": (
                    "In three sentences, explain what a large language model is "
                    "to a new engineer at Orion Analytics who has never used one."
                ),
            }
        ],
    )

    # TODO 1: print the model's text output. `response.content` is a LIST
    # of typed blocks. For Haiku 4.5 and Sonnet 5 (on a simple prompt), the
    # list has one block of type "text" — so `response.content[0].text`
    # works. But adaptive-thinking models (Opus 5.5, sometimes Fable 5.1)
    # may emit a `ThinkingBlock` first — then `content[0]` is the thinking
    # block and `.text` raises AttributeError.
    #
    # The safe pattern (works for every current Claude model) is:
    #   text = next((b.text for b in response.content if b.type == "text"), "")
    #   print(text)
    #
    # You'll swap models in Exercise 5 — the safe pattern above prevents
    # a crash when you point ANTHROPIC_MODEL at claude-opus-5-5.
    print("=== response text ===")
    # print(...)  <-- your line here

    # TODO 2: print the stop_reason. For an ordinary text completion this
    # will usually be "end_turn". If the response hit the max_tokens cap you
    # set above it will be "max_tokens".
    print("\n=== stop_reason ===")
    # print(response.stop_reason)  <-- your line here

    # TODO 3: print the token usage bill. response.usage has these attributes:
    #   .input_tokens    — how many tokens your prompt cost you to send
    #   .output_tokens   — how many tokens Claude produced in reply
    #   .cache_read_input_tokens, .cache_creation_input_tokens (0 for us today)
    #
    # In L6 you'll multiply these by the per-model rates from
    # https://platform.claude.com/docs/en/docs/about-claude/pricing to
    # compute what the call actually cost.
    print("\n=== usage ===")
    # print(f"input_tokens = {response.usage.input_tokens}")   <-- your line here
    # print(f"output_tokens = {response.usage.output_tokens}") <-- your line here


if __name__ == "__main__":
    main()
