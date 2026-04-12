"""Lesson 4, Exercise 1: VisionAPIClient wrapper class."""
import os
import requests

API_KEY = os.environ.get('GOOGLE_API_KEY')


class VisionAPIClient:
    """
    A clean wrapper around the Cloud Vision REST API.
    Supports label detection, OCR, object localization, and safe search.
    All methods return parsed Python dicts/lists.
    """

    BASE_URL = "https://vision.googleapis.com/v1/images:annotate"

    def __init__(self, api_key: str = None):
        # TODO: Store api_key (fall back to API_KEY env var if None)
        # TODO: Build self.url = f"{self.BASE_URL}?key={self.api_key}"
        pass

    def _post(self, image_url: str, features: list) -> dict:
        """
        Make a Vision API call with the given features.
        Return the first element of the responses array.
        Raises requests.HTTPError on non-2xx responses.
        """
        # TODO: Build the payload: {requests: [{image: {source: {imageUri: ...}}, features: [...]}]}
        # TODO: POST to self.url
        # TODO: Call response.raise_for_status()
        # TODO: Return response.json()['responses'][0]
        pass

    def detect_labels(self, image_url: str, max_results: int = 10) -> list:
        """Return list of {description, score} dicts sorted by score descending."""
        # TODO: Call self._post with LABEL_DETECTION feature
        # TODO: Extract 'labelAnnotations' from result (default to [])
        # TODO: Return [{description, score}] sorted by score descending
        pass

    def extract_text(self, image_url: str) -> str:
        """Return full OCR text from image, or empty string if none."""
        # TODO: Call self._post with TEXT_DETECTION feature
        # TODO: Extract first textAnnotation description, or return ""
        pass

    def detect_safe_search(self, image_url: str) -> dict:
        """
        Return safe search annotations dict with keys:
        adult, spoof, medical, violence, racy
        Each value is a likelihood string: VERY_UNLIKELY, UNLIKELY, POSSIBLE, LIKELY, VERY_LIKELY
        """
        # TODO: Call self._post with SAFE_SEARCH_DETECTION feature
        # TODO: Return result.get('safeSearchAnnotation', {})
        pass

    def localize_objects(self, image_url: str) -> list:
        """
        Return list of {name, score} dicts for detected objects.
        Object localization differs from label detection: it finds specific
        object instances with bounding boxes (we return just name+score here).
        """
        # TODO: Call self._post with OBJECT_LOCALIZATION feature
        # TODO: Extract 'localizedObjectAnnotations' (default [])
        # TODO: Return [{name, score}] sorted by score descending
        pass


if __name__ == '__main__':
    client = VisionAPIClient()
    
    test_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/320px-Cat03.jpg"
    
    print("=== Labels ===")
    for label in client.detect_labels(test_url, max_results=5):
        print(f"  {label['score']:.3f}  {label['description']}")
    
    print("\n=== Objects ===")
    for obj in client.localize_objects(test_url):
        print(f"  {obj['score']:.3f}  {obj['name']}")
    
    print("\n=== Safe Search ===")
    ss = client.detect_safe_search(test_url)
    for key, val in ss.items():
        print(f"  {key}: {val}")
