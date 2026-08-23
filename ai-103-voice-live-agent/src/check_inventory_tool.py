"""Exercise 6 — function tool: check_inventory(sku).

Registers a `check_inventory` function tool on the Voice Live session,
streams `inventory_check.wav` (which asks about SKU ALP-60-01), watches
for a `response.function_call_arguments.done` event, executes the tool
locally, returns the result, and lets the agent speak the stock number.

Note: this bypasses the hosted-agent flow — Voice Live's function-calling
event model is per-session tool definitions, not agent-registered tools.
We connect with a raw `model=` config instead of `agent_config`.
"""
from __future__ import annotations

import asyncio
import base64
import json
import os
import sys
import wave
from pathlib import Path

from azure.ai.voicelive.aio import connect
from azure.ai.voicelive.models import (
    AudioEchoCancellation,
    AzureSemanticVadMultilingual,
    AzureStandardVoice,
    FunctionTool,
    InputAudioFormat,
    Modality,
    OutputAudioFormat,
    RequestSession,
    ServerEventType,
)
from azure.identity.aio import DefaultAzureCredential

VOICE_LIVE_SAMPLE_RATE = 24_000
INPUT_FRAME_BYTES = int(VOICE_LIVE_SAMPLE_RATE * 0.02) * 2
REPO_ROOT = Path(__file__).resolve().parent.parent

# Deterministic "database" so grading is stable.
STOCK: dict[str, int] = {
    "RDG-2-01": 3,
    "ALP-60-01": 7,
    "CIR-15-01": 0,
    "SUM-SH-01": 12,
    "TRM-MD-01": 4,
}


def check_inventory(sku: str) -> dict:
    """Local implementation the agent calls."""
    sku_up = sku.upper().replace(" ", "").replace(".", "")
    qty = STOCK.get(sku_up)
    if qty is None:
        return {"sku": sku_up, "found": False, "message": "SKU not recognized"}
    return {"sku": sku_up, "found": True, "in_stock": qty, "store_id": "SEA-01"}


TOOL_DEFINITION = FunctionTool(
    name="check_inventory",
    description="Look up current in-store stock for a Summitline SKU. "
                "Call this whenever a customer asks 'do you have X in stock'.",
    parameters={
        "type": "object",
        "properties": {
            "sku": {
                "type": "string",
                "description": "The Summitline SKU, e.g. 'ALP-60-01'.",
            }
        },
        "required": ["sku"],
    },
)


def _read_pcm(p: Path) -> bytes:
    with wave.open(str(p), "rb") as w:
        return w.readframes(w.getnframes())


def _write_pcm(p: Path, data: bytes) -> None:
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(VOICE_LIVE_SAMPLE_RATE)
        w.writeframes(data)


async def _stream(conn, pcm: bytes) -> None:
    for i in range(0, len(pcm), INPUT_FRAME_BYTES):
        await conn.input_audio_buffer.append(
            audio=base64.b64encode(pcm[i : i + INPUT_FRAME_BYTES]).decode()
        )
    await conn.input_audio_buffer.commit()


async def run() -> int:
    in_wav = REPO_ROOT / "audio" / "inventory_check.wav"
    out_wav = REPO_ROOT / "audio" / "inventory_reply.wav"

    cred = DefaultAzureCredential()
    reply = bytearray()
    tool_called = False

    try:
        async with connect(
            endpoint=os.environ["AZURE_SPEECH_ENDPOINT"],
            credential=cred,
            model="gpt-realtime-mini",
        ) as conn:
            await conn.session.update(
                session=RequestSession(
                    modalities=[Modality.TEXT, Modality.AUDIO],
                    voice=AzureStandardVoice(name=os.environ["VOICE_LIVE_VOICE"]),
                    input_audio_format=InputAudioFormat.PCM16,
                    output_audio_format=OutputAudioFormat.PCM16,
                    turn_detection=AzureSemanticVadMultilingual(),
                    input_audio_echo_cancellation=AudioEchoCancellation(),
                    instructions=(
                        "You are the Summitline product assistant. When the "
                        "associate asks whether an item is in stock, use the "
                        "check_inventory tool with the SKU they said. Then "
                        "speak the result back concisely (1 sentence)."
                    ),
                    tools=[TOOL_DEFINITION],
                )
            )
            print("Sending inventory_check.wav...")
            await _stream(conn, _read_pcm(in_wav))

            async for event in conn:
                if event.type == ServerEventType.RESPONSE_FUNCTION_CALL_ARGUMENTS_DONE:
                    tool_called = True
                    args = json.loads(event.arguments)
                    print(f"Agent called check_inventory({args!r})")
                    result = check_inventory(args["sku"])
                    print(f"  -> {result}")
                    await conn.conversation.item.create(
                        item={
                            "type": "function_call_output",
                            "call_id": event.call_id,
                            "output": json.dumps(result),
                        }
                    )
                    await conn.response.create()
                elif event.type == ServerEventType.RESPONSE_AUDIO_DELTA:
                    reply.extend(base64.b64decode(event.delta))
                elif event.type == ServerEventType.RESPONSE_AUDIO_TRANSCRIPT_DONE:
                    print(f"  Agent said: {event.transcript!r}")
                elif event.type == ServerEventType.RESPONSE_DONE and tool_called:
                    # Only stop after the POST-tool response finishes.
                    break
                elif event.type == ServerEventType.ERROR:
                    print(f"ERROR: {event.error.message}")
                    break

            _write_pcm(out_wav, bytes(reply))
            print(f"Wrote {out_wav.name} ({len(reply)} bytes PCM)")
    finally:
        await cred.close()

    return 0 if tool_called else 5


if __name__ == "__main__":
    sys.exit(asyncio.run(run()))
