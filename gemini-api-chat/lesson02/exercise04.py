#!/usr/bin/env python3
"""
Lesson 2, Exercise 4: Streaming Responses
Reference implementation — completed.
"""
import os
import time
import google.generativeai as genai

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

LONG_PROMPT = (
    "Explain the history of artificial intelligence from the 1950s to today. "
    "Cover: the Turing Test, the AI winters, the rise of machine learning, "
    "deep learning breakthroughs, transformer architecture, and the current era of LLMs. "
    "Be thorough — aim for at least 400 words."
)

def stream_response(prompt: str) -> None:
    print(f"Prompt: {prompt[:80]}...\n")
    print("Streaming response:")
    print("-" * 50)
    start = time.time()
    first_token_time = None
    total_chunks = 0
    response = model.generate_content(prompt, stream=True)
    for chunk in response:
        if chunk.text:
            if first_token_time is None:
                first_token_time = time.time() - start
            print(chunk.text, end='', flush=True)
            total_chunks += 1
    total_time = time.time() - start
    print("\n" + "-" * 50)
    print(f"\nTime to first token: {first_token_time:.2f}s")
    print(f"Total time:          {total_time:.2f}s")
    print(f"Chunks received:     {total_chunks}")
    print(f"Total tokens:        {response.usage_metadata.total_token_count}")

def stream_with_aggregation(prompt: str) -> str:
    response = model.generate_content(prompt, stream=True)
    full_text = ""
    for chunk in response:
        if chunk.text:
            print(chunk.text, end='', flush=True)
            full_text += chunk.text
    print()
    return full_text

if __name__ == '__main__':
    print("=== Streaming Demo ===")
    stream_response(LONG_PROMPT)
    print("\n\n=== Stream and Aggregate ===")
    full = stream_with_aggregation("List 5 key facts about the Python programming language.")
    print(f"\n[Full text: {len(full)} characters]")
