#!/usr/bin/env python3
"""
Lesson 4, Exercise 1: Multi-Turn Conversation with History

Build a chatbot that remembers the conversation context across multiple turns.
Use model.start_chat() to create a session that maintains history automatically.

TODO: Implement the functions below. See the exercise instructions for details.
"""
import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')


def create_chat_session(initial_context: str = None):
    """
    TODO: Create and return a chat session.

    If initial_context is provided, pre-seed the history with it:
    - Role 'user': the context message
    - Role 'model': a brief acknowledgement

    Hint: model.start_chat(history=[...])
    Each history item: {"role": "user" or "model", "parts": "message text"}
    """
    pass  # Replace with your implementation


def send_message(chat, message: str) -> str:
    """
    TODO: Send a message to the chat session and return the response text.
    Hint: chat.send_message(message) — then access .text on the response
    """
    pass  # Replace with your implementation


def display_history(chat) -> None:
    """Display the full conversation history in a readable format."""
    print("\n=== Conversation History ===")
    if not chat.history:
        print("  (empty)")
        return
    for i, turn in enumerate(chat.history, 1):
        role = "You    " if turn.role == "user" else "Gemini "
        text = turn.parts[0].text
        preview = text[:100] + ('...' if len(text) > 100 else '')
        print(f"  [{i}] {role}: {preview}")
    print(f"  Total turns: {len(chat.history)}")


def main():
    print("Gemini Chat (commands: 'history', 'clear', 'quit')\n")

    # TODO: Create a chat session with this context:
    # "I am a Python developer with 2 years of experience. I am learning about AI APIs."
    chat = None  # Replace with create_chat_session(initial_context=...)

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        elif user_input.lower() == 'history':
            display_history(chat)
            continue
        elif user_input.lower() == 'clear':
            # TODO: Reset the chat session (create a new one)
            print("Chat cleared. Starting fresh.\n")
            continue

        # TODO: Send the message and print the response
        response = None  # Replace with send_message(chat, user_input)
        print(f"Gemini: {response}\n")


if __name__ == '__main__':
    main()
