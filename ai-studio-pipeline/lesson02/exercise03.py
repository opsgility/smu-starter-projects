"""Lesson 2, Exercise 3: Chat with system instructions."""
import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

SYSTEM_INSTRUCTION = """You are Pip, a friendly Python tutor.
Always keep answers under 100 words.
Always include a short code example.
Start every response with an encouraging acknowledgment."""

def create_tutoring_session():
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash',
        system_instruction=SYSTEM_INSTRUCTION
    )
    return model.start_chat(history=[])

def ask_pip(chat, question: str) -> str:
    response = chat.send_message(question)
    return response.text

if __name__ == '__main__':
    chat = create_tutoring_session()
    questions = [
        "What is a dictionary in Python?",
        "How do I loop through its keys?",
        "What happens if I access a key that doesn't exist?",
    ]
    for q in questions:
        print(f"\nStudent: {q}")
        answer = ask_pip(chat, q)
        print(f"Pip: {answer}")
