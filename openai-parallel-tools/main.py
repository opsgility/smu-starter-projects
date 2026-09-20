"""
Multi-Source Aggregation Pipeline
Course 201 - Lesson 4: Parallel Tool Calls & Tool Execution Loops

Build a research aggregator that calls weather, news, and stock price
tools in parallel — assembling a combined briefing from concurrent results.

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically. Do NOT set them manually.
"""
from openai import OpenAI
from pydantic import BaseModel
import json
import time

client = OpenAI()

TOOLS = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get current weather conditions for a location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City and country, e.g. 'Austin, TX'"},
            },
            "required": ["location"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_news_headlines",
        "description": "Get top news headlines for a given topic.",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "News topic, e.g. 'AI', 'economy', 'tech'"},
                "count": {"type": "integer", "description": "Number of headlines to return (1-5)"},
            },
            "required": ["topic", "count"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_stock_price",
        "description": "Get the current stock price for a ticker symbol.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {"type": "string", "description": "Stock ticker symbol, e.g. 'AAPL', 'MSFT'"},
            },
            "required": ["ticker"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


# ---- Simulated tool implementations ----

def get_weather(location: str) -> dict:
    """Simulated weather data."""
    data = {
        "austin": {"temp": "78°F", "condition": "Sunny"},
        "seattle": {"temp": "55°F", "condition": "Rainy"},
        "miami":   {"temp": "85°F", "condition": "Humid"},
    }
    key = next((k for k in data if k in location.lower()), None)
    result = data.get(key, {"temp": "72°F", "condition": "Clear"})
    return {"location": location, **result}


def get_news_headlines(topic: str, count: int = 3) -> dict:
    """Simulated news headlines."""
    headlines = {
        "ai":      ["OpenAI releases GPT-5", "Anthropic raises $3B", "Google DeepMind achieves AGI milestone"],
        "tech":    ["Apple Vision Pro 2 announced", "NVIDIA H200 ships to data centers", "Microsoft Azure outage resolved"],
        "economy": ["Fed holds rates steady", "Inflation drops to 2.1%", "S&P 500 hits all-time high"],
    }
    key = next((k for k in headlines if k in topic.lower()), "tech")
    return {"topic": topic, "headlines": headlines[key][:count]}


def get_stock_price(ticker: str) -> dict:
    """Simulated stock prices."""
    prices = {
        "AAPL": 211.50, "MSFT": 425.30, "NVDA": 875.00,
        "GOOGL": 175.20, "AMZN": 195.60, "TSLA": 245.80,
    }
    price = prices.get(ticker.upper(), 100.00)
    return {"ticker": ticker.upper(), "price": f"${price:.2f}", "change": "+1.2%"}


# ---- Tool dispatcher ----

def execute_tool(name: str, arguments: dict) -> str:
    """
    Route a tool call to the correct function and return JSON result.
    Called once per tool call in the parallel execution loop.
    """
    if name == "get_weather":
        result = get_weather(**arguments)
    elif name == "get_news_headlines":
        result = get_news_headlines(**arguments)
    elif name == "get_stock_price":
        result = get_stock_price(**arguments)
    else:
        result = {"error": f"Unknown tool: {name}"}
    return json.dumps(result)


def run_briefing_assistant(user_query: str) -> str:
    """
    Exercise 1: Implement the parallel tool execution loop.

    Steps:
    1. Send user query to model with TOOLS
    2. Collect ALL function call items from response.output
       (there may be multiple — the model can call tools in parallel)
    3. For each function call, execute the tool immediately
    4. Build the follow-up request including:
       - The original user message
       - The full response.output (contains the tool calls)
       - One function_call_output item per call:
         {"type": "function_call_output", "call_id": call.call_id, "output": result_str}
         NOTE: use call.call_id (e.g. "call_..."), NOT call.id (e.g. "fc_...").
         They are different fields and the API rejects mismatches.
    5. Send follow-up, return final output_text

    Use client.responses.create() with model="gpt-4.1-mini".
    """
    print(f"\nQuery: {user_query}")
    start = time.time()

    # TODO: Call client.responses.create() with user_query and TOOLS
    # TODO: Collect all function_call items from response.output
    # TODO: Execute each tool call using execute_tool(name, args)
    # TODO: Build function_call_output items (call_id=call.call_id) and make follow-up call
    # TODO: Print elapsed time and return final response text
    pass


def demo_parallel_tools():
    """Run the briefing assistant on a compound query."""
    query = (
        "Give me a morning briefing: "
        "What's the weather in Austin? "
        "What are the top 3 AI news headlines? "
        "And what's the current price of NVDA stock?"
    )
    result = run_briefing_assistant(query)
    if result:
        print(f"\nBriefing:\n{result}")


if __name__ == "__main__":
    print("Multi-Source Aggregation Pipeline — Course 201 Lesson 4")
    print("=" * 55)
    demo_parallel_tools()
