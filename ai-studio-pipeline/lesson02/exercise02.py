"""Lesson 2, Exercise 2: Few-shot sentiment classifier exported from AI Studio."""
import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

# Few-shot examples used in AI Studio Structured prompt
FEW_SHOT_EXAMPLES = [
    ("I absolutely love this product!", "Positive"),
    ("The worst experience I've ever had.", "Negative"),
    ("It arrived on time, nothing special.", "Neutral"),
    ("Exceeded all my expectations!", "Positive"),
    ("Broken on arrival, very disappointed.", "Negative"),
]

def build_few_shot_prompt(text: str) -> str:
    examples = "\n".join(
        f"Input: {inp}\nOutput: {out}" for inp, out in FEW_SHOT_EXAMPLES
    )
    return f"{examples}\n\nInput: {text}\nOutput:"

def classify_sentiment(text: str) -> str:
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash',
        generation_config=genai.GenerationConfig(
            temperature=0.0,
            max_output_tokens=10,
            stop_sequences=["\n"]
        )
    )
    prompt = build_few_shot_prompt(text)
    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == '__main__':
    tests = [
        "This is the best coffee I've ever tasted!",
        "Package was damaged and customer service didn't help.",
        "Decent quality for the price.",
    ]
    for text in tests:
        sentiment = classify_sentiment(text)
        print(f"{sentiment:10s} | {text}")
