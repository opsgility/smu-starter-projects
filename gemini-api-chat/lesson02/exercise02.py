#!/usr/bin/env python3
"""
Lesson 2, Exercise 2: Generate Text with Gemini 2.0 Flash
Reference implementation — completed.
"""
import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_and_inspect(prompt: str) -> None:
    print(f"\nPrompt: {prompt}")
    print("-" * 60)
    response = model.generate_content(prompt)
    print(f"Response:\n{response.text}")
    usage = response.usage_metadata
    print(f"\nToken usage:")
    print(f"  Prompt tokens:   {usage.prompt_token_count}")
    print(f"  Response tokens: {usage.candidates_token_count}")
    print(f"  Total:           {usage.total_token_count}")
    finish = response.candidates[0].finish_reason
    print(f"\nFinish reason: {finish}")
    print("Safety ratings:")
    for rating in response.candidates[0].safety_ratings:
        print(f"  {rating.category.name}: {rating.probability.name}")

def safe_generate(prompt: str) -> str:
    response = model.generate_content(prompt)
    if not response.candidates:
        return f"[Response blocked] Feedback: {response.prompt_feedback}"
    candidate = response.candidates[0]
    if candidate.finish_reason.name == 'SAFETY':
        return f"[Output filtered] Safety ratings: {candidate.safety_ratings}"
    return response.text

if __name__ == '__main__':
    prompts = [
        "What is the Gemini API in one sentence?",
        "List three popular uses of generative AI in business applications.",
        "Write a Python function that reverses a string.",
    ]
    for prompt in prompts:
        generate_and_inspect(prompt)
        print("=" * 60)
