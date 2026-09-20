"""Exercise 5 — barge-in interruption.

Streams `tent_setup_windy.wav` (a long question) into Voice Live, then
partway through the assistant's spoken reply streams a second WAV
(`barge_in_followup.wav`) into the same session. On
`azure_semantic_vad_multilingual`, `interrupt_response=True` by default,
so the assistant should truncate the first reply and start answering the
second question.

Output: `audio/barge_in_reply.wav` — a single WAV containing whatever
audio arrived from the assistant across both turns, in order.
"""
from __future__ import annotations

import asyncio
import base64
import os
import sys
import wave
from pathlib import Path

from azure.ai.voicelive.aio import AgentSessionConfig, connect
from azure.ai.voicelive.models import (
    AudioEchoCancellation,
    AzureSemanticVadMultilingual,
    AzureStandardVoice,
    InputAudioFormat,
    Modality,
    OutputAudioFormat,
    RequestSession,
    ServerEventType,
)
from azure.identity.aio import DefaultAzureCredential

VOICE_LIVE_SAMPLE_RATE = 24_000
INPUT_FRAME_BYTES = int(VOICE_LIVE_SAMPLE_RATE * 0.02) * 2  # 20 ms PCM16
REPO_ROOT = Path(__file__).resolve().parent.parent


def _read_pcm(p: Path) -> bytes:
    with wave.open(str(p), "rb") as w:
        return w.readframes(w.getnframes())


def _write_pcm(p: Path, data: bytes) -> None:
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(VOICE_LIVE_SAMPLE_RATE)
        w.writeframes(data)


async def _stream(conn, pcm: bytes, then_commit: bool = True) -> None:
    for i in range(0, len(pcm), INPUT_FRAME_BYTES):
        await conn.input_audio_buffer.append(
            audio=base64.b64encode(pcm[i : i + INPUT_FRAME_BYTES]).decode()
        )
    if then_commit:
        await conn.input_audio_buffer.commit()


async def run() -> int:
    first = REPO_ROOT / "audio" / "tent_setup_windy.wav"
    second = REPO_ROOT / "audio" / "barge_in_followup.wav"
    out = REPO_ROOT / "audio" / "barge_in_reply.wav"

    cred = DefaultAzureCredential()
    reply = bytearray()
    interrupted = False

    try:
        async with connect(
            endpoint=os.environ["AZURE_SPEECH_ENDPOINT"],
            credential=cred,
            agent_config=AgentSessionConfig(
                agent_name=os.environ["AZURE_AI_AGENT_NAME"],
                project_name=os.environ["AZURE_AI_PROJECT_NAME"],
            ),
        ) as conn:
            await conn.session.update(
                session=RequestSession(
                    modalities=[Modality.TEXT, Modality.AUDIO],
                    voice=AzureStandardVoice(name=os.environ["VOICE_LIVE_VOICE"]),
                    input_audio_format=InputAudioFormat.PCM16,
                    output_audio_format=OutputAudioFormat.PCM16,
                    # interrupt_response defaults to True; showing it explicitly.
                    turn_detection=AzureSemanticVadMultilingual(interrupt_response=True),
                    input_audio_echo_cancellation=AudioEchoCancellation(),
                )
            )
            print("Turn 1: sending tent_setup_windy.wav")
            await _stream(conn, _read_pcm(first))

            deltas_before_interrupt = 0
            async for event in conn:
                if event.type == ServerEventType.RESPONSE_AUDIO_DELTA:
                    reply.extend(base64.b64decode(event.delta))
                    deltas_before_interrupt += 1
                    # After ~15 audio chunks (~1.5s), barge in with the second WAV.
                    if deltas_before_interrupt == 15 and not interrupted:
                        interrupted = True
                        print("BARGE-IN: streaming barge_in_followup.wav mid-reply")
                        # Do NOT wait for RESPONSE_DONE — send NOW so the VAD
                        # sees user speech and interrupts the current response.
                        await _stream(conn, _read_pcm(second))
                elif event.type == ServerEventType.RESPONSE_CANCELLED:
                    print("Server acknowledged interrupt (RESPONSE_CANCELLED).")
                elif event.type == ServerEventType.RESPONSE_DONE and interrupted:
                    # Second turn is done; break out.
                    print("Turn 2 complete.")
                    break
                elif event.type == ServerEventType.ERROR:
                    print(f"ERROR: {event.error.message}")
                    break

            _write_pcm(out, bytes(reply))
            print(f"Wrote {out.name} ({len(reply)} bytes PCM)")
    finally:
        await cred.close()
    return 0 if interrupted else 4


if __name__ == "__main__":
    sys.exit(asyncio.run(run()))
