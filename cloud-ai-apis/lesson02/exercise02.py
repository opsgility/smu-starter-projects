"""Lesson 2, Exercise 2: Natural Language API — sentiment and entity analysis."""
import os
import requests

API_KEY = os.environ.get('GOOGLE_API_KEY')
NL_BASE = f"https://language.googleapis.com/v1/documents"


def analyze_sentiment(text: str) -> dict:
    """Return {score, magnitude} for the text."""
    payload = {
        "document": {"type": "PLAIN_TEXT", "content": text},
        "encodingType": "UTF8"
    }
    response = requests.post(
        f"{NL_BASE}:analyzeSentiment?key={API_KEY}",
        json=payload
    )
    response.raise_for_status()
    sentiment = response.json()['documentSentiment']
    return {
        "score": round(sentiment['score'], 3),
        "magnitude": round(sentiment['magnitude'], 3)
    }


def extract_entities(text: str) -> list:
    """Return list of {name, type, salience} dicts."""
    payload = {
        "document": {"type": "PLAIN_TEXT", "content": text},
        "encodingType": "UTF8"
    }
    response = requests.post(
        f"{NL_BASE}:analyzeEntities?key={API_KEY}",
        json=payload
    )
    response.raise_for_status()
    entities = response.json().get('entities', [])
    return [
        {"name": e['name'], "type": e['type'], "salience": round(e['salience'], 3)}
        for e in sorted(entities, key=lambda x: x['salience'], reverse=True)
    ]


if __name__ == '__main__':
    sample_text = (
        "Google CEO Sundar Pichai announced excellent quarterly results today in "
        "Mountain View. The company exceeded analyst expectations by a wide margin."
    )
    
    print("=== Sentiment Analysis ===")
    sentiment = analyze_sentiment(sample_text)
    print(f"  Score: {sentiment['score']} | Magnitude: {sentiment['magnitude']}")
    
    print("\n=== Entity Extraction ===")
    entities = extract_entities(sample_text)
    for e in entities:
        print(f"  [{e['type']:15s}] {e['name']:25s} (salience: {e['salience']})")
