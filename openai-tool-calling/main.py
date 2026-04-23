"""
Weather Lookup Tool
Course 201 - Lesson 2: JSON Schema Tool Definitions

Build a weather assistant with a get_weather(location, unit) tool.
Demonstrates complete tool invocation, result handling, and re-prompting.

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically. Do NOT set them manually.
"""
from openai import OpenAI
import json

client = OpenAI()

# Tool schema definition
TOOLS = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get the current weather for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state or country, e.g. 'San Francisco, CA' or 'London, UK'",
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit. Defaults to fahrenheit.",
                },
            },
            "required": ["location"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]


def get_weather(location: str, unit: str = "fahrenheit") -> dict:
    """
    Simulated weather API — returns fake but realistic weather data.
    In a real app this would call a weather service.
    """
    # Simulated data keyed by city name fragment
    weather_db = {
        "san francisco": {"temp_f": 62, "temp_c": 17, "condition": "Foggy", "humidity": 85},
        "london":        {"temp_f": 55, "temp_c": 13, "condition": "Overcast", "humidity": 78},
        "tokyo":         {"temp_f": 72, "temp_c": 22, "condition": "Sunny", "humidity": 60},
        "new york":      {"temp_f": 68, "temp_c": 20, "condition": "Partly cloudy", "humidity": 55},
        "sydney":        {"temp_f": 75, "temp_c": 24, "condition": "Sunny", "humidity": 50},
        "paris":         {"temp_f": 58, "temp_c": 14, "condition": "Rainy", "humidity": 80},
    }

    loc_key = location.lower()
    data = next((v for k, v in weather_db.items() if k in loc_key), {
        "temp_f": 70, "temp_c": 21, "condition": "Clear", "humidity": 50
    })

    temp = data["temp_c"] if unit == "celsius" else data["temp_f"]
    unit_label = "°C" if unit == "celsius" else "°F"

    return {
        "location": location,
        "temperature": f"{temp}{unit_label}",
        "condition": data["condition"],
        "humidity": f"{data['humidity']}%",
        "unit": unit,
    }


def run_weather_assistant(user_query: str) -> str:
    """
    Exercise 1: Complete the tool invocation loop.

    Steps:
    1. Send user query to model with TOOLS defined
    2. If model returns a tool call, execute get_weather() with its arguments
    3. Feed the tool result back to the model
    4. Return the model's final natural language response

    Use client.responses.create() with:
    - model="gpt-4.1-mini"
    - input=[{"role": "user", "content": user_query}]
    - tools=TOOLS
    - tool_choice="auto"
    """
    print(f"\nQuery: {user_query}")

    # TODO: Call client.responses.create() with the user query and TOOLS
    # TODO: Check if response.output contains a function call
    #       (look for item.type == "function_call" in response.output)
    # TODO: If a tool call is found:
    #   - Parse item.arguments as JSON to get the function arguments
    #   - Call get_weather(**args) with those arguments
    #   - Build a follow-up input list with: the original user message,
    #     the function_call item, and a function_call_output item:
    #       {"type": "function_call_output", "call_id": item.call_id, "output": json.dumps(result)}
    #     NOTE: use item.call_id (e.g. "call_..."), NOT item.id (e.g. "fc_...").
    #     They are different fields and the API rejects mismatches.
    #   - Return response2.output_text
    # TODO: If no tool call, return response.output_text directly
    pass


def demo_weather_assistant():
    """Run the weather assistant on several test queries."""
    queries = [
        "What's the weather like in San Francisco?",
        "Is it cold in Tokyo right now? Use Celsius please.",
        "What's 2 + 2?",                           # Should answer without tool
        "Compare the weather in London and Paris.",  # May call tool twice or once
    ]

    for query in queries:
        result = run_weather_assistant(query)
        if result:
            print(f"Response: {result}\n")


if __name__ == "__main__":
    print("Weather Lookup Tool — Course 201 Lesson 2")
    print("=" * 50)
    demo_weather_assistant()
