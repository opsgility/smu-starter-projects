"""Lesson 4, Exercise 2: Model comparison benchmark."""
import os
import time
import google.generativeai as genai

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

MODELS_TO_COMPARE = [
    'gemini-2.0-flash',
    'gemini-1.5-flash',
]

# TODO: Implement run_prompt_on_model().
# It should call generate_content() with the given prompt on the given model,
# measure elapsed time, and return a dict with keys:
#   'model', 'response_text', 'elapsed_seconds',
#   'input_tokens', 'output_tokens'
# Hint: response.usage_metadata has input_token_count and candidates_token_count
def run_prompt_on_model(model_name: str, prompt: str, temperature: float = 0.0) -> dict:
    pass

# TODO: Implement compare_models().
# For each model in MODELS_TO_COMPARE, call run_prompt_on_model().
# Return a list of result dicts.
def compare_models(prompt: str, temperature: float = 0.0) -> list:
    pass

# TODO: Implement print_comparison_table().
# Print a formatted table showing model name, elapsed time,
# token counts, and the first 120 chars of the response.
def print_comparison_table(results: list):
    pass

if __name__ == '__main__':
    test_prompt = (
        "Explain the concept of recursion in programming. "
        "Include a Python example and explain when NOT to use it."
    )
    results = compare_models(test_prompt, temperature=0.2)
    print_comparison_table(results)
