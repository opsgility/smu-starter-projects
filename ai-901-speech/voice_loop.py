"""
Voice loop: transcribe a WAV -> send to a Foundry chat model -> synthesize the reply.
"""
import os
from pathlib import Path

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from speech_to_text import transcribe
from text_to_speech import synthesize

load_dotenv()

ENDPOINT = os.environ["PROJECT_ENDPOINT"]
DEPLOYMENT = os.environ.get("DEPLOYMENT_NAME", "ai901-chat")

HERE = Path(__file__).parent
INPUT_WAV = HERE / "sample_data" / "question.wav"
REPLY_WAV = HERE / "reply.wav"


def ask_model(question: str) -> str:
    # TODO 1: build a ChatCompletionsClient and send
    #         [SystemMessage("You are a Northwind Horizon kiosk assistant."), UserMessage(question)]
    # TODO 2: return the assistant reply text.
    raise NotImplementedError


def main() -> None:
    question = transcribe(INPUT_WAV)
    print(f"User said: {question}")
    reply = ask_model(question)
    print(f"Assistant: {reply}")
    synthesize(reply, REPLY_WAV)
    print(f"Wrote {REPLY_WAV}")


if __name__ == "__main__":
    main()
