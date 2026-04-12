#!/usr/bin/env python3
"""
Lesson 2, Exercise 1: Set Up the SDK and Verify Your API Key
Reference implementation — completed.
"""
import os
import google.generativeai as genai

def main():
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY is not set. Check the Environment tab in the lab sidebar."
        )

    genai.configure(api_key=api_key)
    print("SDK configured successfully")

    print("\nAvailable Gemini models:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"  - {model.name}")
            print(f"    Input limit:  {model.input_token_limit:,} tokens")
            print(f"    Output limit: {model.output_token_limit:,} tokens")

    print("\nConnection to Gemini API confirmed!")

if __name__ == '__main__':
    main()
