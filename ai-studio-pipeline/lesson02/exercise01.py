"""Lesson 2, Exercise 1: Run a freeform prompt via the SDK."""
import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

def run_freeform_prompt(prompt: str, temperature: float = 1.0) -> str:
    """Run a freeform prompt with configurable temperature."""
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash',
        generation_config=genai.GenerationConfig(temperature=temperature)
    )
    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    result = run_freeform_prompt(
        "Explain the difference between a list and a tuple in Python in 2 sentences.",
        temperature=0.2
    )
    print(result)
