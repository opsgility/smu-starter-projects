"""
Tool Calling with the OpenAI Responses API
Course 201 - Lesson 2: Weather Lookup Tool

Exercises:
1. Define a JSON Schema tool for get_weather(location, unit)
2. Make the model invoke the tool automatically for weather questions
3. Feed the tool result back into the conversation
4. Verify the model answers non-weather questions WITHOUT invoking the tool

The weather data in this exercise uses a mock function (no real API key needed).

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
from openai import OpenAI
import json

client = OpenAI()

# -----------------------------------------------------------------------
# Mock weather service - simulates a real weather API
# -----------------------------------------------------------------------

MOCK_WEATHER_DATA = {
    "paris": {"temperature": 18, "condition": "Partly cloudy", "humidity": 65, "wind_mph": 12},
    "new york": {"temperature": 22, "condition": "Sunny", "humidity": 55, "wind_mph": 8},
    "london": {"temperature": 14, "condition": "Overcast", "humidity": 78, "wind_mph": 15},
    "tokyo": {"temperature": 25, "condition": "Clear", "humidity": 60, "wind_mph": 5},
    "sydney": {"temperature": 20, "condition": "Mostly sunny", "humidity": 70, "wind_mph": 18},
    "berlin": {"temperature": 16, "condition": "Rainy", "humidity": 85, "wind_mph": 10},
}


def get_weather(location: str, unit: str = "celsius") -> dict:
    """
    Mock weather function - simulates a real weather API call.
    Returns weather data for the location or a 'not found' message.

    This function is called by your tool execution logic, NOT by the model.
    The model only generates the tool call arguments; you execute the function.
    """
    location_key = location.lower().strip()
    if location_key in MOCK_WEATHER_DATA:
        data = MOCK_WEATHER_DATA[location_key].copy()
        temp = data["temperature"]
        if unit == "fahrenheit":
            temp = round(temp * 9/5 + 32, 1)
        data["temperature"] = temp
        data["unit"] = unit
        data["location"] = location
        return data
    return {"error": f"Weather data not available for '{location}'"}


# -----------------------------------------------------------------------
# Exercise 1: Tool Schema Definition
# -----------------------------------------------------------------------

# Define the get_weather tool schema for the Responses API
# The schema must match the JSON Schema spec exactly
WEATHER_TOOL = {
    "type": "function",
    "name": "get_weather",
    "description": "Get the current weather for a specific location. Returns temperature, conditions, humidity, and wind speed.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. 'Paris', 'New York', 'Tokyo'"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit. Default is celsius."
            }
        },
        "required": ["location"],
        "additionalProperties": False
    },
    "strict": True
}


def handle_tool_call(tool_name: str, tool_args: dict) -> str:
    """
    Exercise 2: Execute the tool call and return the result as a JSON string.

    When the model decides to call get_weather, this function is invoked
    with the tool name and the arguments the model generated.

    Check tool_name == "get_weather", then call get_weather(**tool_args).
    Return the result as a JSON string (json.dumps(result)).

    Args:
        tool_name: The name of the tool the model wants to call
        tool_args: The arguments parsed from the model's response

    Returns:
        JSON string of the tool execution result
    """
    if tool_name == "get_weather":
        # TODO: Call get_weather(**tool_args) and return json.dumps(result)
        pass
    return json.dumps({"error": f"Unknown tool: {tool_name}"})


def ask_weather_assistant(user_question: str) -> str:
    """
    Exercise 3: Full tool-calling conversation loop.

    1. Send the user question with the WEATHER_TOOL available
    2. Check if the model wants to call a tool (response.output[0].type == "function_call")
    3. If yes: execute the tool, then send the result back to get the final answer
    4. If no tool call: return the response text directly

    The second API call includes the tool result and asks the model to
    formulate a natural language response.

    Args:
        user_question: The user's natural language question

    Returns:
        The assistant's final answer as a string
    """
    print(f"\nUser: {user_question}")

    # First call: give the model the question and available tools
    # TODO: Call client.responses.create() with:
    #   model = "gpt-4.1-mini"
    #   input = user_question
    #   tools = [WEATHER_TOOL]
    #   tool_choice = "auto"

    # TODO: Check if the model called a tool:
    #   Look for an item in response.output where item.type == "function_call"

    # TODO: If tool called:
    #   - Get tool_call = the function_call item
    #   - Execute: result_json = handle_tool_call(tool_call.name, json.loads(tool_call.arguments))
    #   - Make a second call with the tool result:
    #     client.responses.create(
    #       model="gpt-4.1-mini",
    #       input=user_question,
    #       tools=[WEATHER_TOOL],
    #       previous_response_id=response.id  # maintains conversation state
    #     )
    #     But also include the tool result. Refer to the Responses API docs for
    #     how to pass function_call_output back to the model.

    # TODO: Return the final response text (response.output_text)
    return "Not implemented yet"


# -----------------------------------------------------------------------
# Test queries
# -----------------------------------------------------------------------
WEATHER_QUESTIONS = [
    "What's the weather like in Paris right now?",
    "Is it hot in Tokyo today?",
    "Should I bring an umbrella to London?",
    "What's the temperature in New York in Fahrenheit?",
]

NON_WEATHER_QUESTIONS = [
    "What is the capital of France?",
    "Explain what a REST API is in one sentence.",
    "What year was Python created?",
]


if __name__ == "__main__":
    print("=" * 60)
    print("Exercise 1: Verify Tool Schema")
    print("=" * 60)
    print(f"Tool name: {WEATHER_TOOL['name']}")
    print(f"Strict mode: {WEATHER_TOOL['strict']}")
    print(f"Required params: {WEATHER_TOOL['parameters']['required']}")
    print(f"Unit options: {WEATHER_TOOL['parameters']['properties']['unit']['enum']}")

    print("\n" + "=" * 60)
    print("Exercise 2 & 3: Weather Tool Invocation")
    print("=" * 60)
    for question in WEATHER_QUESTIONS:
        answer = ask_weather_assistant(question)
        print(f"Assistant: {answer}\n")

    print("\n" + "=" * 60)
    print("Exercise 4: Non-Weather Questions (No Tool Should Fire)")
    print("=" * 60)
    for question in NON_WEATHER_QUESTIONS:
        answer = ask_weather_assistant(question)
        print(f"Assistant: {answer}\n")
