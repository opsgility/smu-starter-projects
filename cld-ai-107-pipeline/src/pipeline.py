"""3-stage sequential pipeline."""

import os, sys
from dotenv import load_dotenv
import anthropic


def stage(client, model, system_prompt: str, user_content: str, max_tokens: int = 1000) -> str:
    resp = client.messages.create(model=model, max_tokens=max_tokens,
        system=system_prompt, messages=[{"role":"user","content":user_content}])
    return next((b.text for b in resp.content if b.type == "text"), "")


def drafter(client, model, topic: str, outline: str) -> str:
    return stage(client, model,
        "You are a technical blog writer. Produce a rough first draft based on the topic and outline. 300-400 words. Prioritize completeness over polish.",
        f"Topic: {topic}\n\nOutline:\n{outline}")


def editor(client, model, draft: str) -> str:
    """TODO: rewrite for clarity + tightness. Same shape as drafter but with editor system prompt."""
    # HINT:
    #   return stage(client, model,
    #       "You are a copy editor. Tighten this draft: remove filler, sharpen verbs, cut redundancy. Preserve all technical points.",
    #       draft)
    raise NotImplementedError("TODO: editor")


def formatter(client, model, edited: str) -> str:
    return stage(client, model,
        "You are a docs formatter. Add ## headers where appropriate. Wrap any code in ``` fences. Keep body identical otherwise.",
        edited)


def main():
    load_dotenv()
    client = anthropic.Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

    topic = "How Claude's tool_use protocol enables agents"
    outline = "- what tool_use is\n- how the loop works\n- when to use it (agents) vs skip (chatbots)"

    print("=== DRAFT ===")
    d = drafter(client, model, topic, outline)
    print(d[:400], "...")

    print("\n=== EDITED ===")
    try:
        e = editor(client, model, d)
    except NotImplementedError as ex:
        print(f"TODO: {ex}"); return 1
    print(e[:400], "...")

    print("\n=== FORMATTED ===")
    f = formatter(client, model, e)
    print(f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
