"""Synthesize the three lab WAV files from data/transcripts.json.

Run once early in Exercise 1. Uses the Foundry-hosted Speech (TTS) surface
via the azure-cognitiveservices-speech SDK; the same Foundry account that
serves Voice Live also serves classic Speech TTS.

Output: audio/<clip>.wav — 24 kHz, 16-bit, mono PCM WAV. Voice Live wants
PCM16 24 kHz — using the same rate here keeps the input clips zero-copy
against the WebSocket frame format.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk
from azure.identity import DefaultAzureCredential

REPO_ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPTS = REPO_ROOT / "data" / "transcripts.json"
OUT_DIR = REPO_ROOT / "audio"


def _resource_from_endpoint(endpoint: str) -> tuple[str, str]:
    """Return (resource_name, region) for a Foundry endpoint.

    Foundry AIServices resources expose Speech at
    <name>.cognitiveservices.azure.com. The classic Speech SDK wants
    (resource_id / auth-token) plus a region — we look up region via ARM at
    lab-provision time and pass it in via AZURE_LOCATION.
    """
    host = urllib.parse.urlparse(endpoint).hostname or ""
    return host.split(".")[0], os.environ.get("AZURE_LOCATION", "eastus2")


def main() -> int:
    if not TRANSCRIPTS.exists():
        print(f"Missing {TRANSCRIPTS}"); return 1
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    endpoint = os.environ["AZURE_SPEECH_ENDPOINT"]
    resource_name, region = _resource_from_endpoint(endpoint)

    cred = DefaultAzureCredential()
    token = cred.get_token("https://cognitiveservices.azure.com/.default").token
    # Speech SDK wants an "aad#<resourceId>#<token>" auth token when using
    # AAD directly against a Cognitive Services resource:
    #   see learn.microsoft.com/azure/ai-services/speech-service/how-to-configure-azure-ad-auth
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    resource_group = os.environ["AZURE_RESOURCE_GROUP"]
    resource_id = (
        f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}"
        f"/providers/Microsoft.CognitiveServices/accounts/{resource_name}"
    )
    auth_token = f"aad#{resource_id}#{token}"

    speech_config = speechsdk.SpeechConfig(auth_token=auth_token, region=region)
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm
    )

    manifest = json.loads(TRANSCRIPTS.read_text(encoding="utf-8"))
    voice = manifest["voice"]
    speech_config.speech_synthesis_voice_name = voice

    for clip in manifest["clips"]:
        out_path = OUT_DIR / clip["filename"]
        audio_config = speechsdk.audio.AudioOutputConfig(filename=str(out_path))
        synth = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=audio_config
        )
        print(f"Synthesizing {clip['filename']} ({len(clip['text'])} chars)...")
        result = synth.speak_text_async(clip["text"]).get()
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"  FAILED: {result.reason} — {result.cancellation_details}")
            return 2
        print(f"  Wrote {out_path.relative_to(REPO_ROOT)} ({out_path.stat().st_size} bytes)")

    print("\nAll clips generated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
