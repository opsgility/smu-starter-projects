"""Stream tool_use JSON progressively."""

import os, sys
from dotenv import load_dotenv
import anthropic


SCHEMA = {"name":"submit",
  "input_schema":{"type":"object",
    "properties":{"summary":{"type":"string"},"key_points":{"type":"array","items":{"type":"string"}}},
    "required":["summary","key_points"]}}


def main():
    load_dotenv()
    client = anthropic.Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

    prompt = "Summarize CLD-AI-108 course structure: what does it teach? Return summary + 3 key_points."

    with client.messages.stream(model=model, max_tokens=800,
        tools=[SCHEMA], tool_choice={"type":"tool","name":"submit"},
        messages=[{"role":"user","content":prompt}]) as stream:
        print("Streaming chunks:")
        for event in stream:
            if event.type == "content_block_delta" and getattr(event.delta, "type", None) == "input_json_delta":
                print(event.delta.partial_json, end="", flush=True)
        print("\n\nFinal message:")
        final = stream.get_final_message()
        for b in final.content:
            if b.type == "tool_use":
                print(f"  block.input = {dict(b.input)}")


if __name__ == "__main__":
    main()
