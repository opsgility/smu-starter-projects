"""Lesson 2, Exercise 4: Export code from AI Studio and run it here."""
# This file is a placeholder — students paste their AI Studio
# exported code here and adapt it to use the env var API key.
import os
import google.generativeai as genai

# Replace any hardcoded API key from the export with this:
genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

# === PASTE YOUR AI STUDIO EXPORTED CODE BELOW ===

# Example structure after export:
# model = genai.GenerativeModel(model_name='gemini-2.0-flash')
# response = model.generate_content('Your prompt here')
# print(response.text)
