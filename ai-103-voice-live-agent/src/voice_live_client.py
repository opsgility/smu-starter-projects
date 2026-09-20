"""Exercises 3 & 4 — connect Voice Live to the Foundry hosted agent.

Reads a WAV file, streams its PCM16 frames to the Voice Live WebSocket,
collects the assistant's audio response, and writes it to an output WAV.

The Voice Live SDK is async-only (v1.0+); we use `azure.ai.voicelive.aio`.
Voice Live is fully managed — the model that speaks is NOT a Foundry
deployment. The hosted agent (which OWNS the RAG index) is invoked per turn.

Usage:
    python src/voice_live_client.py audio/tent_setup_windy.wav audio/tent_setup_windy_reply.wav
"""
from __future__ import annotations

import asyncio
import base64
import os
import struct
import sys
import wave
from pathlib import Path

from azure.ai.voicelive.aio import AgentSessionConfig, connect
from azure.ai.voicelive.models import (
    AudioEchoCancellation,
    AudioNoiseReduction,
    AzureSemanticVadMultilingual,
    AzureStandardVoice,
    InputAudioFormat,
    Modality,
    OutputAudioFormat,
    RequestSession,
    ServerEventType,
)
from azure.identity.aio import DefaultAzureCredential

# Voice Live streams PCM16 at 24 kHz mono. Match on input.
VOICE_LIVE_SAMPLE_RATE = 24_000
INPUT_FRAME_MS = 20  # ~20 ms per chunk keeps the buffer well under the limit
INPUT_FRAME_BYTES = int(VOICE_LIVE_SAMPLE_RATE * (INPUT_FRAME_MS / 1000)) * 2  # 16-bit


def _read_wav_pcm(path: Path) -> bytes:
    """Return raw PCM16 mono @ 24 kHz. Errors loudly on format mismatch."""
    with wave.open(str(path), "rb") as w:
        if w.getnchannels() != 1:
            raise ValueError(f"{path}: expected mono, got {w.getnchannels()} channels")
        if w.getsampwidth() != 2:
            raise ValueError(f"{path}: expected 16-bit PCM, got {w.getsampwidth()*8}-bit")
        if w.getframerate() != VOICE_LIVE_SAMPLE_RATE:
            raise ValueError(
                f"{path}: expected {VOICE_LIVE_SAMPLE_RATE} Hz, got {w.getframerate()} Hz"
            )
        return w.readframes(w.getnframes())


def _write_wav_pcm(path: Path, pcm: bytes) -> None:
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(VOICE_LIVE_SAMPLE_RATE)
        w.writeframes(pcm)


async def send_wav(conn, pcm: bytes) -> None:
    """Base64-encode + send the WAV in ~20 ms PCM16 frames."""
    for i in range(0, len(pcm), INPUT_FRAME_BYTES):
        frame = pcm[i : i + INPUT_FRAME_BYTES]
        await conn.input_audio_buffer.append(audio=base64.b64encode(frame).decode())
    # Server VAD ends the turn on silence; commit forces it immediately.
    await conn.input_audio_buffer.commit()


async def collect_response(conn) -> bytes:
    """Drain events until RESPONSE_DONE; return concatenated PCM."""
    out = bytearray()
    async for event in conn:
        etype = event.type
        if etype == ServerEventType.RESPONSE_AUDIO_DELTA:
            out.extend(base64.b64decode(event.delta))
        elif etype == ServerEventType.RESPONSE_AUDIO_TRANSCRIPT_DONE:
            print(f"  Agent said: {event.transcript!r}")
        elif etype == ServerEventType.ERROR:
            print(f"  ERROR: {event.error.message}")
            break
        elif etype == ServerEventType.RESPONSE_DONE:
            break
    return bytes(out)


async def run(in_wav: Path, out_wav: Path) -> int:
    endpoint = os.environ["AZURE_SPEECH_ENDPOINT"]
    agent_name = os.environ["AZURE_AI_AGENT_NAME"]
    project_name = os.environ["AZURE_AI_PROJECT_NAME"]
    voice = os.environ["VOICE_LIVE_VOICE"]

    cred = DefaultAzureCredential()
    try:
        async with connect(
            endpoint=endpoint,
            credential=cred,
            agent_config=AgentSessionConfig(
                agent_name=agent_name,
                project_name=project_name,
            ),
        ) as conn:
            await conn.session.update(
                session=RequestSession(
                    modalities=[Modality.TEXT, Modality.AUDIO],
                    voice=AzureStandardVoice(name=voice),
                    input_audio_format=InputAudioFormat.PCM16,
                    output_audio_format=OutputAudioFormat.PCM16,
                    turn_detection=AzureSemanticVadMultilingual(),
                    input_audio_echo_cancellation=AudioEchoCancellation(),
                    input_audio_noise_reduction=AudioNoiseReduction(
                        type="azure_deep_noise_suppression"
                    ),
                )
            )
            print(f"Sending {in_wav.name}...")
            pcm_in = _read_wav_pcm(in_wav)
            await send_wav(conn, pcm_in)
            print("Waiting for response...")
            pcm_out = await collect_response(conn)
            _write_wav_pcm(out_wav, pcm_out)
            print(f"Wrote {out_wav.name} ({len(pcm_out)} bytes PCM)")
    finally:
        await cred.close()
    return 0


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python src/voice_live_client.py <input.wav> <output.wav>")
        return 1
    return asyncio.run(run(Path(sys.argv[1]), Path(sys.argv[2])))


if __name__ == "__main__":
    sys.exit(main())
