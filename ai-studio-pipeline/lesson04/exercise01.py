"""Lesson 4, Exercise 1: System instructions — export from AI Studio and run here."""
import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

# TODO: Define your system instruction string here.
# This should match what you wrote in AI Studio's System Instructions panel.
SYSTEM_INSTRUCTION = None  # Replace with your system instruction string

# TODO: Create a GenerativeModel with the system_instruction parameter.
# Hint: genai.GenerativeModel(model_name='gemini-2.0-flash', system_instruction=...)
def create_model_with_system_instruction(instruction: str):
    pass

# TODO: Start a chat session and run a 3-turn conversation.
# Each response should demonstrate that the system instruction is active.
def run_guided_conversation(model, questions: list) -> list:
    """
    Start a chat session on the model and send each question.
    Return a list of (question, answer) tuples.
    """
    pass

if __name__ == '__main__':
    # Test questions — modify to match your AI Studio persona
    questions = [
        "Introduce yourself.",
        "What is your main purpose?",
        "Give me one tip for today.",
    ]
    if SYSTEM_INSTRUCTION is None:
        print("ERROR: Set SYSTEM_INSTRUCTION before running.")
    else:
        model = create_model_with_system_instruction(SYSTEM_INSTRUCTION)
        results = run_guided_conversation(model, questions)
        for q, a in results:
            print(f"Q: {q}")
            print(f"A: {a}\n")
