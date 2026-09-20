"""Lesson 4, Exercise 4: ContentAnalyzer — multi-API pipeline."""
import os
from lesson04.exercise01 import VisionAPIClient
from lesson04.exercise02 import NaturalLanguageClient
from lesson04.exercise03 import detect_language, translate_to_english


class ContentAnalyzer:
    """
    A multi-API content analysis pipeline.

    Given an image URL, this analyzer:
    1. Detects labels and objects (Vision API)
    2. Runs safe search to flag inappropriate content (Vision API)
    3. Extracts any text in the image (Vision API OCR)
    4. If text found: detects language, translates to English (Translation API)
    5. Analyzes sentiment and extracts entities from English text (NL API)
    6. Returns a structured analysis report
    """

    def __init__(self):
        # TODO: Create self.vision = VisionAPIClient()
        # TODO: Create self.nl = NaturalLanguageClient()
        pass

    def analyze_image(self, image_url: str) -> dict:
        """
        Run the full multi-API pipeline on the given image URL.
        Return a dict with keys:
          url, labels, objects, safe_search,
          extracted_text, text_language, english_text,
          sentiment, entities, flagged
        
        'flagged' is True if any safe_search field is LIKELY or VERY_LIKELY.
        """
        # TODO: Step 1 - detect_labels, localize_objects, detect_safe_search
        # TODO: Step 2 - determine flagged: any(v in ('LIKELY','VERY_LIKELY') for v in safe_search.values())
        # TODO: Step 3 - extract_text
        # TODO: Step 4 - if text: detect_language(), translate_to_english()
        # TODO: Step 5 - if english_text: analyze_sentiment(), extract_entities()
        # TODO: Return the complete result dict
        pass

    def print_report(self, result: dict):
        """
        Print a human-readable report from analyze_image() output.
        """
        # TODO: Print URL, flagged status, top 5 labels, top 3 objects
        # TODO: If extracted_text: print language, english translation, sentiment score
        # TODO: If entities: print top 3 entities with type and salience
        pass


if __name__ == '__main__':
    analyzer = ContentAnalyzer()
    
    # Test images — try different types to exercise all code paths:
    test_images = [
        # An image with visible text:
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Camponotus_flavomarginatus_ant.jpg/320px-Camponotus_flavomarginatus_ant.jpg",
    ]
    
    for url in test_images:
        print(f"\n{'='*60}")
        result = analyzer.analyze_image(url)
        analyzer.print_report(result)
