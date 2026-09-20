"""Lesson 4, Exercise 2: NaturalLanguageClient wrapper class."""
import os
import requests

API_KEY = os.environ.get('GOOGLE_API_KEY')


class NaturalLanguageClient:
    """
    Wrapper around the Cloud Natural Language REST API.
    Supports sentiment analysis, entity extraction, and content classification.
    """

    BASE_URL = "https://language.googleapis.com/v1/documents"

    def __init__(self, api_key: str = None):
        # TODO: Store api_key (fall back to API_KEY env var if None)
        pass

    def _post(self, endpoint: str, text: str) -> dict:
        """
        POST to BASE_URL/{endpoint}?key=... with PLAIN_TEXT document.
        Return the parsed JSON dict. Raises HTTPError on failure.
        """
        # TODO: Build URL: f"{self.BASE_URL}:{endpoint}?key={self.api_key}"
        # TODO: Build payload: {document: {type: 'PLAIN_TEXT', content: text}, encodingType: 'UTF8'}
        # TODO: POST, raise_for_status, return .json()
        pass

    def analyze_sentiment(self, text: str) -> dict:
        """
        Return {score, magnitude, sentences} where sentences is a list of
        {text, score, magnitude} dicts for per-sentence breakdown.
        """
        # TODO: Call self._post('analyzeSentiment', text)
        # TODO: Extract documentSentiment.score and .magnitude
        # TODO: Extract sentences array: each has .text.content, .sentiment.score, .sentiment.magnitude
        # TODO: Return {score, magnitude, sentences: [{text, score, magnitude}]}
        pass

    def extract_entities(self, text: str) -> list:
        """
        Return list of {name, type, salience, wikipedia_url} dicts,
        sorted by salience descending. wikipedia_url may be None.
        """
        # TODO: Call self._post('analyzeEntities', text)
        # TODO: Extract entities array
        # TODO: For each entity, get metadata.wikipedia_url (may not exist)
        # TODO: Return sorted by salience descending
        pass

    def classify_content(self, text: str) -> list:
        """
        Return list of {name, confidence} dicts for content categories.
        Note: text must be at least 20 tokens for classification to work.
        """
        # TODO: Call self._post('classifyText', text)
        # TODO: Extract categories array
        # TODO: Return [{name, confidence}] sorted by confidence descending
        pass


if __name__ == '__main__':
    client = NaturalLanguageClient()
    
    sample = (
        "Google CEO Sundar Pichai announced record-breaking quarterly results today. "
        "Revenue grew 28% year-over-year, driven by cloud and advertising. "
        "Investors reacted positively, pushing shares up 5% in after-hours trading."
    )
    
    print("=== Sentiment ===")
    sentiment = client.analyze_sentiment(sample)
    print(f"  Document: score={sentiment['score']}, magnitude={sentiment['magnitude']}")
    for s in sentiment['sentences']:
        print(f"  [{s['score']:+.2f}] {s['text'][:60]}")
    
    print("\n=== Entities ===")
    for e in client.extract_entities(sample):
        wiki = f" ({e['wikipedia_url']})" if e.get('wikipedia_url') else ""
        print(f"  [{e['type']:15s}] {e['name']:20s} salience={e['salience']:.3f}{wiki}")
    
    print("\n=== Content Classification ===")
    for cat in client.classify_content(sample):
        print(f"  {cat['confidence']:.3f}  {cat['name']}")
