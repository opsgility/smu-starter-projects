"""Lesson 4, Exercise 3: Speech-to-Text and Translation API wrappers."""
import os
import base64
import requests

API_KEY = os.environ.get('GOOGLE_API_KEY')


def transcribe_audio_url(audio_url: str, language_code: str = 'en-US',
                          encoding: str = 'FLAC', sample_rate: int = 16000) -> dict:
    """
    Download audio from audio_url, base64-encode it, and send to Speech-to-Text
    synchronous recognize endpoint.
    Return {transcript, confidence, words} where words is a list of
    {word, startTime, endTime} dicts (if word timestamps available).
    """
    # TODO: Download the audio file: requests.get(audio_url).content
    # TODO: base64 encode: base64.b64encode(audio_bytes).decode('utf-8')
    # TODO: Build RecognitionConfig with encoding, sampleRateHertz, languageCode,
    #       enableAutomaticPunctuation=True, enableWordTimeOffsets=True
    # TODO: POST to https://speech.googleapis.com/v1/speech:recognize?key={API_KEY}
    # TODO: Extract first result: data['results'][0]['alternatives'][0]
    # TODO: Return {transcript, confidence, words: [{word, startTime, endTime}]}
    pass


def detect_language(text: str) -> dict:
    """
    Detect the language of the given text.
    Return {language, confidence}.
    """
    # TODO: POST to https://translation.googleapis.com/language/translate/v2/detect?key={API_KEY}
    # TODO: Send {q: text}
    # TODO: Return {language, confidence} from data['data']['detections'][0][0]
    pass


def translate_to_english(text: str) -> dict:
    """
    Translate text to English. Return {translatedText, detectedSourceLanguage}.
    If text is already English, return it unchanged with detectedSourceLanguage='en'.
    """
    # TODO: First detect language using detect_language()
    # TODO: If language is 'en', return {translatedText: text, detectedSourceLanguage: 'en'}
    # TODO: Otherwise, POST to https://translation.googleapis.com/language/translate/v2?key={API_KEY}
    # TODO: Send {q: text, target: 'en', format: 'text'}
    # TODO: Return {translatedText, detectedSourceLanguage}
    pass


if __name__ == '__main__':
    # Test Translation
    test_texts = [
        "Merci beaucoup pour votre aide!",
        "Gracias por la ayuda.",
        "Thank you for your help.",  # already English
    ]
    
    print("=== Language Detection & Translation ===")
    for text in test_texts:
        lang = detect_language(text)
        translation = translate_to_english(text)
        print(f"  [{lang['language']}] {text[:40]:40s} -> {translation['translatedText']}")
    
    # Note: Speech-to-Text requires a publicly accessible audio file URL
    # If you have one, uncomment and test:
    # AUDIO_URL = "https://storage.googleapis.com/cloud-samples-data/speech/brooklyn_bridge.raw"
    # result = transcribe_audio_url(AUDIO_URL, encoding='LINEAR16', sample_rate=16000)
    # print(f"\nTranscript: {result['transcript']}")
    # print(f"Confidence: {result['confidence']:.3f}")
