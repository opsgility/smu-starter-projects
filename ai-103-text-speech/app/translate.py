"""Azure Translator v3.0 REST helper for Summitline Outfitters.

Exercise 2 implements ``translate(text, to_lang)`` which POSTs to the
Translator ``/translate`` endpoint and unwraps the doubly-nested response
shape ``[{"translations":[{"text":"...","to":"..."}]}]``.

The single biggest gotcha is that regional Translator resources require
BOTH the key header AND the region header — omitting the region header
yields a misleading ``401 Credentials Missing``.
"""

from __future__ import annotations

import os

import requests
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Environment wiring.
# ---------------------------------------------------------------------------
KEY = os.environ["TRANSLATOR_KEY"]
REGION = os.environ["TRANSLATOR_REGION"]
# Global Translator hostname; pair with the resource's regional key + region.
ENDPOINT = os.environ.get(
    "TRANSLATOR_ENDPOINT",
    "https://api.cognitive.microsofttranslator.com/translate",
)


def translate(text: str, to_lang: str) -> str:
    """Translate ``text`` into ``to_lang`` using the Translator v3.0 REST API.

    ``to_lang`` must be a BCP-47 / ISO 639-1 code — ``fr``, ``es``, ``ja``,
    ``de``, ``zh-Hans`` — NOT ``french`` / ``japanese``.
    """
    # TODO (Exercise 2 Step 7 - TODO 1): build the request headers dict with
    #   "Ocp-Apim-Subscription-Key":    KEY,
    #   "Ocp-Apim-Subscription-Region": REGION,   # required — #1 cause of 401
    #   "Content-type":                 "application/json",
    # then POST to ENDPOINT with
    #   params={"api-version": "3.0", "to": to_lang},
    #   headers=headers,
    #   json=[{"text": text}],
    #   timeout=30,
    # Call response.raise_for_status() so 4xx/5xx surface as exceptions.
    raise NotImplementedError("Exercise 2 TODO 1: POST to Translator v3.0")

    # TODO (Exercise 2 Step 7 - TODO 2): parse the nested response and return
    # ``response.json()[0]["translations"][0]["text"]`` — a single translation
    # for a single input document.
