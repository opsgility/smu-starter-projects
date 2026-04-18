"""Speech SDK helpers — TTS, STT, speech translation."""
import os
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

KEY = os.environ["SPEECH_KEY"]
REGION = os.environ["SPEECH_REGION"]
VOICE = "en-US-AriaNeural"


def _config() -> speechsdk.SpeechConfig:
    cfg = speechsdk.SpeechConfig(subscription=KEY, region=REGION)
    cfg.speech_synthesis_voice_name = VOICE
    return cfg


def synthesize(text: str, out_path: Path) -> Path:
    # TODO 1: AudioOutputConfig(filename=str(out_path)) + SpeechSynthesizer +
    #         speak_text_async(text).get(); raise on failure; return out_path.
    raise NotImplementedError


def transcribe(audio_path: Path) -> str:
    # TODO 2: AudioConfig(filename=str(audio_path)) + SpeechRecognizer +
    #         recognize_once_async().get(); raise on failure; return result.text.
    raise NotImplementedError


def translate_speech(audio_path: Path, target_lang: str) -> dict:
    # TODO 3: SpeechTranslationConfig(subscription=KEY, region=REGION); add target_lang.
    #         AudioConfig(filename=str(audio_path)). TranslationRecognizer.
    #         recognize_once_async().get(); return {"source_text": result.text,
    #         "translations": dict(result.translations)}.
    raise NotImplementedError
