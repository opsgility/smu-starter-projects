"""Translator wrapper — REST is simplest."""
import os

import requests
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = "https://api.cognitive.microsofttranslator.com/translate"
KEY = os.environ["TRANSLATOR_KEY"]
REGION = os.environ["TRANSLATOR_REGION"]


def translate(text: str, to_lang: str) -> str:
    headers = {
        "Ocp-Apim-Subscription-Key": KEY,
        "Ocp-Apim-Subscription-Region": REGION,
        "Content-type": "application/json",
    }
    # TODO 1: requests.post(ENDPOINT, params={"api-version": "3.0", "to": to_lang},
    #                          headers=headers, json=[{"text": text}]).
    # TODO 2: return response.json()[0]["translations"][0]["text"].
    raise NotImplementedError
