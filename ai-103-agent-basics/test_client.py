"""Run a multi-turn conversation through the agent."""
from app.agent import converse

CONVO = [
    "Hi! What's the weather in Seattle?",
    "What's 47 * 12?",
    "Do we have any NW-001 in stock?",
]

for msg in converse(CONVO):
    print(f"{msg['role'].upper():9} | {msg['text']}")
