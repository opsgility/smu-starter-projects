#!/usr/bin/env python3
"""
Lesson 4, Exercise 3: Function Calling

Use Gemini's function calling (tool use) to let the model invoke your Python functions.
Gemini does NOT call functions directly — it returns a function_call object,
your code executes the function, then you send the result back for a final answer.

TODO: Implement the TODOs below. See the exercise instructions for the full pattern.
"""
import os
import json
import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))


# ─── Python Functions (the actual implementations) ──────────────────────────
# Gemini never sees this code — only the FunctionDeclaration schemas below.

def get_weather(city: str) -> dict:
    """Simulated weather data — no real API call needed."""
    weather_data = {
        "London":   {"temperature_c": 12, "condition": "Cloudy",       "humidity_pct": 75},
        "Tokyo":    {"temperature_c": 22, "condition": "Sunny",        "humidity_pct": 60},
        "New York": {"temperature_c": 18, "condition": "Partly Cloudy","humidity_pct": 65},
        "Sydney":   {"temperature_c": 25, "condition": "Sunny",        "humidity_pct": 55},
        "Paris":    {"temperature_c": 15, "condition": "Rainy",        "humidity_pct": 80},
    }
    data = weather_data.get(city, {"temperature_c": 20, "condition": "Unknown", "humidity_pct": 70})
    return {"city": city, **data}


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """Simulated currency conversion with fixed rates."""
    rates = {"USD": 1.0, "EUR": 0.92, "GBP": 0.79, "JPY": 149.5, "AUD": 1.53}
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    if from_currency not in rates or to_currency not in rates:
        return {"error": f"Unsupported currency. Supported: {list(rates.keys())}"}
    converted = amount * (rates[to_currency] / rates[from_currency])
    return {
        "original": f"{amount} {from_currency}",
        "converted": f"{converted:.2f} {to_currency}",
        "rate": rates[to_currency] / rates[from_currency]
    }


# ─── Function Declarations (what Gemini sees) ────────────────────────────────

# TODO: Create a FunctionDeclaration for get_weather
# Name: "get_weather"
# Description: "Get the current weather for a city. Use this when the user asks about weather, temperature, or conditions in a specific location."
# Parameters: city (string, required) — "The city name, e.g. 'London' or 'Tokyo'"
get_weather_declaration = None  # Replace with FunctionDeclaration(...)

# TODO: Create a FunctionDeclaration for convert_currency
# Name: "convert_currency"
# Description: "Convert an amount from one currency to another. Use when the user asks to convert money or exchange rates."
# Parameters:
#   amount (number, required) — "The amount to convert"
#   from_currency (string, required) — "The source currency code (USD, EUR, GBP, JPY, AUD)"
#   to_currency (string, required) — "The target currency code (USD, EUR, GBP, JPY, AUD)"
convert_currency_declaration = None  # Replace with FunctionDeclaration(...)

# TODO: Create a Tool containing both declarations
# tools_list = Tool(function_declarations=[get_weather_declaration, convert_currency_declaration])
tools_list = None  # Replace with Tool(...)

# TODO: Create the model with tools
# model_with_tools = genai.GenerativeModel('gemini-2.0-flash', tools=[tools_list])
model_with_tools = None  # Replace with GenerativeModel(...)


# ─── Two-Turn Function Calling Handler ───────────────────────────────────────

def execute_function_call(function_call) -> dict:
    """
    TODO: Execute the function that Gemini requested and return the result.

    Steps:
    1. Get the function name: function_call.name
    2. Get the arguments: dict(function_call.args)
    3. Call get_weather(**args) or convert_currency(**args) based on the name
    4. Return the result dict
    """
    pass  # Replace with your implementation


def chat_with_tools(user_message: str) -> str:
    """
    TODO: Complete the two-turn function calling cycle.

    Turn 1: Send user_message to model_with_tools via a chat session
    Check: does the response contain a function call?
      - If finish_reason is 'STOP' and no function_call part: return response.text directly
      - If there IS a function_call part:
          1. Call execute_function_call() with the function_call object
          2. Send the result back using:
             chat.send_message(genai.protos.Part(
                 function_response=genai.protos.FunctionResponse(
                     name=fn_name,
                     response={"result": result}
                 )
             ))
          3. Return the second response's .text

    Hint: Check for function call with:
      parts = response.candidates[0].content.parts
      has_fn_call = any(hasattr(p, 'function_call') and p.function_call.name for p in parts)
    """
    pass  # Replace with your implementation


def main():
    test_queries = [
        "What's the weather like in Tokyo?",
        "Convert 100 USD to EUR",
        "What's the weather in London and how much is 50 GBP in Japanese Yen?",
        "What is the capital of France?",  # No function needed — tests text fallback
    ]

    for query in test_queries:
        print(f"\nUser: {query}")
        result = chat_with_tools(query)
        print(f"Gemini: {result}")
        print("-" * 50)


if __name__ == '__main__':
    main()
