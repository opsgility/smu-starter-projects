#!/usr/bin/env python3
"""
Lesson 2, Exercise 3: Tune Model Parameters
Reference implementation — completed.
"""
import os
import google.generativeai as genai
from google.generativeai.types import GenerationConfig

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

PROMPT = "Write a short creative story (3-4 sentences) about a robot discovering music for the first time."

def generate_with_config(temperature: float, max_tokens: int,
                         top_p: float = 0.95, top_k: int = 40) -> str:
    config = GenerationConfig(
        temperature=temperature,
        max_output_tokens=max_tokens,
        top_p=top_p,
        top_k=top_k,
    )
    response = model.generate_content(PROMPT, generation_config=config)
    return response.text

if __name__ == '__main__':
    print("=== Temperature Comparison ===")
    print(f"Prompt: {PROMPT}\n")
    print("--- temperature=0.1 ---")
    print(generate_with_config(temperature=0.1, max_tokens=300))
    print("\n--- temperature=1.0 ---")
    print(generate_with_config(temperature=1.0, max_tokens=300))
    print("\n--- temperature=1.8 ---")
    print(generate_with_config(temperature=1.8, max_tokens=300))
    print("\n=== Token Limit ===")
    short = model.generate_content(
        PROMPT, generation_config=GenerationConfig(max_output_tokens=20)
    )
    print(f"Text: {short.text}")
    print(f"Finish reason: {short.candidates[0].finish_reason}")
    print("\n=== Factual Config ===")
    factual_model = genai.GenerativeModel(
        'gemini-2.0-flash',
        generation_config=GenerationConfig(temperature=0.2, max_output_tokens=512, top_p=0.8, top_k=20)
    )
    response = factual_model.generate_content(
        "What year was Python first released, and who created it?"
    )
    print(response.text)
