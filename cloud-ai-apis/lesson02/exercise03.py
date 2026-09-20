"""Lesson 2, Exercise 3: Translation API — detect language and translate."""
import os
import requests

API_KEY = os.environ.get('GOOGLE_API_KEY')
TRANSLATE_BASE = "https://translation.googleapis.com/language/translate/v2"


def detect_language(text: str) -> dict:
    """Return {language, confidence} for the detected language."""
    response = requests.post(
        f"{TRANSLATE_BASE}/detect?key={API_KEY}",
        json={"q": text}
    )
    response.raise_for_status()
    detection = response.json()['data']['detections'][0][0]
    return {
        "language": detection['language'],
        "confidence": round(detection['confidence'], 3)
    }


def translate_text(text: str, target_language: str = 'en') -> dict:
    """Translate text to target_language. Returns {translatedText, detectedSourceLanguage}."""
    response = requests.post(
        f"{TRANSLATE_BASE}?key={API_KEY}",
        json={"q": text, "target": target_language, "format": "text"}
    )
    response.raise_for_status()
    translation = response.json()['data']['translations'][0]
    return {
        "translatedText": translation['translatedText'],
        "detectedSourceLanguage": translation.get('detectedSourceLanguage', 'unknown')
    }


if __name__ == '__main__':
    samples = [
        ("Bonjour le monde!", "French sample"),
        ("Hola, ¿cómo estás?", "Spanish sample"),
        ("こんにちは世界", "Japanese sample"),
        ("Hello, world!", "English sample"),
    ]
    
    for text, label in samples:
        detected = detect_language(text)
        translation = translate_text(text, target_language='en')
        print(f"{label}:")
        print(f"  Detected: {detected['language']} (confidence: {detected['confidence']})")
        print(f"  English:  {translation['translatedText']}")
        print()
