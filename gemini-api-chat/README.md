# Gemini API Chat Application — Lesson 4 Starter

This workspace contains completed code from Lesson 2 and skeleton files for Lesson 4.

## Workspace Structure

```
lesson02/          ← Completed exercises from Lesson 2 (reference code)
  exercise01.py   ← SDK setup and model listing
  exercise02.py   ← Text generation and response inspection
  exercise03.py   ← GenerationConfig and model parameters
  exercise04.py   ← Streaming responses

lesson04/          ← Your work for this lesson (Lesson 4)
  exercise01.py   ← Multi-turn chat with history (TODO)
  exercise02.py   ← Image analysis with Gemini Vision (TODO)
  exercise03.py   ← Function calling implementation (TODO)
  exercise04.py   ← Complete chat application (TODO)

requirements.txt   ← Dependencies (all pre-installed)
```

## Getting Started

1. Open a terminal: `Ctrl+backtick`
2. Verify your API key: `echo $GOOGLE_API_KEY`
3. Run a Lesson 2 reference file: `python3 lesson02/exercise01.py`
4. Open `lesson04/exercise01.py` and follow the exercise instructions

## Key SDK Reference

```python
import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

# Text generation
response = model.generate_content('Your prompt')
print(response.text)

# Chat session
chat = model.start_chat(history=[])
response = chat.send_message('Hello!')
print(response.text)

# Streaming
for chunk in model.generate_content('prompt', stream=True):
    if chunk.text:
        print(chunk.text, end='', flush=True)
```
