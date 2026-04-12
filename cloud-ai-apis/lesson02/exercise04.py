"""Lesson 2, Exercise 4: Combined image content analyzer."""
import os
from lesson02.exercise01 import detect_labels, extract_text
from lesson02.exercise02 import analyze_sentiment
from lesson02.exercise03 import detect_language, translate_text


def analyze_image(image_url: str) -> dict:
    """
    Run Vision API (labels + OCR), then if text is found:
    - Detect its language
    - Translate to English if not already English
    - Analyze sentiment of the (English) text
    """
    print(f"Analyzing: {image_url[:60]}...")
    
    # Step 1: Vision API
    labels = detect_labels(image_url, max_results=5)
    extracted_text = extract_text(image_url)
    
    result = {
        "labels": labels,
        "extracted_text": extracted_text,
        "text_language": None,
        "english_text": None,
        "sentiment": None,
    }
    
    if extracted_text:
        # Step 2: Language detection
        lang_info = detect_language(extracted_text)
        result["text_language"] = lang_info["language"]
        
        # Step 3: Translate if not English
        if lang_info["language"] != "en":
            translation = translate_text(extracted_text, target_language="en")
            result["english_text"] = translation["translatedText"]
        else:
            result["english_text"] = extracted_text
        
        # Step 4: Sentiment on English text
        result["sentiment"] = analyze_sentiment(result["english_text"])
    
    return result


if __name__ == '__main__':
    test_images = [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/280px-PNG_transparency_demonstration_1.png",
    ]
    for url in test_images:
        r = analyze_image(url)
        print(f"Labels: {[l['description'] for l in r['labels']]}")
        print(f"Text: {repr(r['extracted_text'][:100]) if r['extracted_text'] else '(none)'}")
        if r['sentiment']:
            print(f"Sentiment: score={r['sentiment']['score']}, magnitude={r['sentiment']['magnitude']}")
        print()
