"""Lesson 2, Exercise 1: Cloud Vision API — label detection and OCR."""
import os
import requests

API_KEY = os.environ.get('GOOGLE_API_KEY')
VISION_URL = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}"


def detect_labels(image_url: str, max_results: int = 10) -> list:
    """Return list of {description, score} dicts for detected labels."""
    payload = {
        "requests": [{
            "image": {"source": {"imageUri": image_url}},
            "features": [{"type": "LABEL_DETECTION", "maxResults": max_results}]
        }]
    }
    response = requests.post(VISION_URL, json=payload)
    response.raise_for_status()
    data = response.json()
    annotations = data['responses'][0].get('labelAnnotations', [])
    return [{"description": a['description'], "score": round(a['score'], 3)} for a in annotations]


def extract_text(image_url: str) -> str:
    """Return the full text extracted from the image (OCR)."""
    payload = {
        "requests": [{
            "image": {"source": {"imageUri": image_url}},
            "features": [{"type": "TEXT_DETECTION"}]
        }]
    }
    response = requests.post(VISION_URL, json=payload)
    response.raise_for_status()
    data = response.json()
    text_annotations = data['responses'][0].get('textAnnotations', [])
    return text_annotations[0]['description'].strip() if text_annotations else ""


if __name__ == '__main__':
    test_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/280px-PNG_transparency_demonstration_1.png"
    
    print("=== Label Detection ===")
    labels = detect_labels(test_image)
    for label in labels:
        print(f"  {label['score']:.3f}  {label['description']}")
    
    print("\n=== OCR Text Extraction ===")
    text = extract_text("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Mudra-Naruto-KageBunshin.svg/250px-Mudra-Naruto-KageBunshin.svg.png")
    print(repr(text) if text else "(no text detected)")
