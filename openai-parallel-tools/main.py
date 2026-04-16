"""
Parallel Tool Calls & Multi-Source Aggregation
Course 201 - Lesson 4: Multi-Source Aggregation Pipeline

Exercises:
1. Define tools for weather, news headlines, and stock price
2. Make a single API call that triggers all three tools in parallel
3. Execute tools concurrently, map results by tool_call_id
4. Send all results back to get the final aggregated briefing

All data uses mock functions - no external API keys required.

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
from openai import OpenAI
import json
import time
import concurrent.futures
from datetime import datetime, timezone

client = OpenAI()

# -----------------------------------------------------------------------
# Mock data services
# -----------------------------------------------------------------------

def mock_get_weather(location: str, unit: str = "celsius") -> dict:
    data = {
        "new york": {"temp": 22, "condition": "Sunny", "humidity": 55},
        "london":   {"temp": 14, "condition": "Overcast", "humidity": 78},
        "tokyo":    {"temp": 25, "condition": "Clear", "humidity": 60},
    }
    result = data.get(location.lower(), {"temp": 20, "condition": "Unknown", "humidity": 50})
    if unit == "fahrenheit":
        result["temp"] = round(result["temp"] * 9/5 + 32, 1)
    result.update({"location": location, "unit": unit})
    return result


def mock_get_news_headlines(topic: str, count: int = 3) -> dict:
    headlines_db = {
        "technology": [
            "OpenAI Launches GPT-5 with Enhanced Reasoning Capabilities",
            "Apple Vision Pro Sales Surpass 1 Million Units",
            "Google DeepMind Achieves Breakthrough in Protein Folding",
            "Microsoft Azure AI Services Revenue Doubles YoY",
        ],
        "finance": [
            "S&P 500 Reaches All-Time High Amid Tech Rally",
            "Federal Reserve Holds Rates Steady in Q2 2026",
            "Bitcoin Surpasses $100,000 for Third Time",
            "Venture Capital Investment in AI Startups Hits Record $50B",
        ],
        "health": [
            "FDA Approves First AI-Designed Drug for Cancer Treatment",
            "New Study Links Sleep Quality to Cognitive Performance",
            "Telehealth Adoption Remains High Post-Pandemic",
        ],
    }
    topic_lower = topic.lower()
    headlines = headlines_db.get(topic_lower, [f"No news found for topic: {topic}"])
    return {
        "topic": topic,
        "headlines": headlines[:count],
        "source": "MockNewsAPI",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


def mock_get_stock_price(symbol: str) -> dict:
    prices = {
        "AAPL":  {"price": 189.50, "change": +2.30, "change_pct": +1.23, "volume": "45.2M"},
        "GOOGL": {"price": 172.80, "change": -1.20, "change_pct": -0.69, "volume": "22.1M"},
        "MSFT":  {"price": 415.90, "change": +5.60, "change_pct": +1.37, "volume": "31.8M"},
        "NVDA":  {"price": 875.20, "change": +22.40, "change_pct": +2.63, "volume": "58.3M"},
        "AMZN":  {"price": 192.40, "change": -0.80, "change_pct": -0.41, "volume": "35.6M"},
    }
    upper = symbol.upper()
    if upper in prices:
        data = prices[upper].copy()
        data["symbol"] = upper
        data["market"] = "NASDAQ"
        return data
    return {"error": f"Symbol not found: {symbol}", "symbol": symbol}


# -----------------------------------------------------------------------
# Tool definitions
# -----------------------------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get current weather conditions for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["location"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "get_news_headlines",
        "description": "Get the latest news headlines for a topic",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "News topic: technology, finance, health"},
                "count": {"type": "integer", "description": "Number of headlines (1-5)", "default": 3}
            },
            "required": ["topic"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "get_stock_price",
        "description": "Get the current stock price and daily change for a ticker symbol",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "Stock ticker symbol, e.g. AAPL, MSFT, NVDA"}
            },
            "required": ["symbol"],
            "additionalProperties": False
        },
        "strict": True
    }
]


def execute_tool(tool_name: str, tool_args: dict) -> str:
    """Execute a single tool and return result as JSON string."""
    if tool_name == "get_weather":
        return json.dumps(mock_get_weather(**tool_args))
    elif tool_name == "get_news_headlines":
        return json.dumps(mock_get_news_headlines(**tool_args))
    elif tool_name == "get_stock_price":
        return json.dumps(mock_get_stock_price(**tool_args))
    return json.dumps({"error": f"Unknown tool: {tool_name}"})


def execute_tools_concurrently(tool_calls: list) -> dict[str, str]:
    """
    Exercise 2: Execute multiple tool calls concurrently using ThreadPoolExecutor.

    Use concurrent.futures.ThreadPoolExecutor to run all tool calls in parallel.
    Record start_time before submitting and elapsed_ms after completing all futures.
    Print timing to confirm concurrent (not sequential) execution.

    Args:
        tool_calls: List of function_call items from response.output

    Returns:
        Dict mapping tool_call_id -> result_json_string
    """
    results = {}
    start_time = time.time()

    # TODO: Use concurrent.futures.ThreadPoolExecutor(max_workers=len(tool_calls))
    # TODO: Submit a future for each tool_call: executor.submit(execute_tool, tc.name, json.loads(tc.arguments))
    # TODO: Collect results: results[tc.id] = future.result()
    # TODO: After all complete: elapsed_ms = (time.time() - start_time) * 1000
    # TODO: Print f"Executed {len(tool_calls)} tools in {elapsed_ms:.0f}ms (concurrent)"

    return results


def generate_briefing(user_request: str) -> str:
    """
    Exercise 3: Full parallel tool call pipeline.

    1. Send request to model with all TOOLS available
    2. Collect all function_call items from response.output
    3. Execute all tools concurrently with execute_tools_concurrently()
    4. Send tool results back to model for final synthesis
    5. Return the final briefing text

    For step 4, you need to pass the tool outputs back.
    Look at the Responses API docs for how to pass function call outputs.

    Args:
        user_request: The user's briefing request

    Returns:
        The assembled briefing from the model
    """
    print(f"Request: {user_request}\n")

    # TODO: First call - get tool invocations
    # client.responses.create(model="gpt-4.1", input=user_request, tools=TOOLS, tool_choice="required")

    # TODO: Collect all tool calls from response.output where item.type == "function_call"

    # TODO: Execute tools concurrently

    # TODO: Build tool outputs and make second call to synthesize

    # TODO: Return final response.output_text
    return "Not implemented yet"


if __name__ == "__main__":
    print("=" * 60)
    print("Exercise 1: Tool Schema Verification")
    print("=" * 60)
    print(f"Defined {len(TOOLS)} tools: {[t['name'] for t in TOOLS]}")
    for tool in TOOLS:
        print(f"  {tool['name']}: strict={tool['strict']}, required={tool['parameters']['required']}")

    print("\n" + "=" * 60)
    print("Exercise 2 & 3: Parallel Tool Execution")
    print("=" * 60)

    briefing = generate_briefing(
        "Give me a morning briefing: weather in New York, "
        "top 3 technology headlines, and NVDA stock price."
    )
    print("\nFinal Briefing:")
    print("-" * 40)
    print(briefing)
