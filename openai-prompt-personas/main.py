"""
Persona-Based Assistants with System Prompts
Course 102 - Lesson 2: Persona-Based Assistants

Exercises:
1. Build three assistants with distinct personas using system prompts
2. Demonstrate how system prompt design changes output format and tone
3. Measure token usage differences between personas

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
from openai import OpenAI
import json

client = OpenAI()

# The same question answered by all three personas
SHARED_QUESTION = "A customer is trying to reset their password but the email link isn't working. How should I help them?"

# System prompts for each persona - you will modify and extend these
PERSONA_PROMPTS = {
    "customer_support": """You are Alex, a friendly and empathetic customer support agent at TechFlow SaaS.
Your communication style:
- Warm, patient, and reassuring
- Use clear numbered steps for any procedures
- Always end with asking if the customer needs anything else
- Respond in plain text (no markdown)
- Keep responses under 150 words""",

    "code_reviewer": """You are Dr. Chen, a strict senior software engineer conducting a technical code review.
Your communication style:
- Direct and technical, no pleasantries
- Reference security best practices (OWASP, etc.) when relevant
- Use structured markdown with ## headings and bullet points
- Grade severity: [CRITICAL] [HIGH] [MEDIUM] [LOW]
- Keep responses under 200 words""",

    "technical_writer": """You are Jordan, a professional technical writer creating user documentation.
Your communication style:
- Clear, precise, and formal
- Structure output as: Overview, Prerequisites, Steps, Troubleshooting
- Use markdown formatting with numbered steps and code blocks
- Target audience: non-technical end users
- Keep responses under 250 words""",
}


def create_persona_response(persona_name: str, question: str) -> dict:
    """
    Exercise 1: Create a response using the specified persona's system prompt.

    Use the Responses API with a system message to set the persona.
    The input should be a list with system and user messages:
    [
        {"role": "system", "content": PERSONA_PROMPTS[persona_name]},
        {"role": "user",   "content": question}
    ]

    Return a dict with:
      - persona: str
      - response_text: str (the output_text)
      - input_tokens: int
      - output_tokens: int

    Args:
        persona_name: Key in PERSONA_PROMPTS ("customer_support", "code_reviewer", "technical_writer")
        question: The user's question
    """
    # TODO: Call client.responses.create() with:
    #   model = "gpt-4.1-mini"
    #   input = [
    #       {"role": "system", "content": PERSONA_PROMPTS[persona_name]},
    #       {"role": "user",   "content": question}
    #   ]
    # TODO: Return the dict described above
    return {}


def compare_personas(question: str) -> None:
    """
    Exercise 2: Run all three personas on the same question and compare.

    For each persona:
    - Call create_persona_response()
    - Print the persona name, token usage, and the response text
    - Check that each response differs from the others

    Also verify that:
    - All responses are non-empty strings
    - Output format constraints are honored (plain text vs markdown)

    Args:
        question: The question to ask all three personas
    """
    responses = {}

    for persona_name in PERSONA_PROMPTS:
        print(f"\n{'='*50}")
        print(f"Persona: {persona_name.replace('_', ' ').title()}")
        print("=" * 50)

        # TODO: Call create_persona_response(persona_name, question)
        # TODO: Store result in responses[persona_name]
        # TODO: Print the response text and token usage

    # TODO: Verify all three responses are different from each other
    # Compare response texts pairwise and print whether they differ
    print("\n" + "=" * 50)
    print("Verification: Responses differ from each other?")
    print("=" * 50)
    # TODO: Compare responses['customer_support'] vs responses['code_reviewer']
    # TODO: Compare responses['customer_support'] vs responses['technical_writer']
    # TODO: Compare responses['code_reviewer'] vs responses['technical_writer']
    # Print PASS or FAIL for each comparison


def build_custom_persona(role: str, style: str, format_instruction: str, question: str) -> str:
    """
    Exercise 3: Build a custom persona from components and query it.

    Construct a system prompt dynamically from three components:
    - role: The character's job title and name
    - style: Communication style guidelines (bullet points)
    - format_instruction: Output format requirement

    Call the API with the constructed system prompt and return the response text.

    Args:
        role: e.g., "You are Sam, a data analyst at a healthcare startup."
        style: e.g., "Use precise numbers. Be concise. Never use jargon."
        format_instruction: e.g., "Respond only in JSON with keys: summary, action_items"
        question: The user question
    """
    system_prompt = f"{role}\n\nCommunication style:\n{style}\n\nFormat: {format_instruction}"

    # TODO: Call client.responses.create() with the constructed system prompt
    # TODO: Return response.output_text
    return ""


if __name__ == "__main__":
    print("EXERCISE 1 & 2: Compare Three Personas on the Same Question")
    print(f"Question: {SHARED_QUESTION}\n")
    compare_personas(SHARED_QUESTION)

    print("\n\nEXERCISE 3: Custom Persona Builder")
    print("=" * 50)
    custom_response = build_custom_persona(
        role="You are Sam, a data analyst at a healthcare startup.",
        style="Use precise numbers. Be concise. Avoid jargon.",
        format_instruction='Respond only in JSON with keys: "summary" (str) and "next_steps" (list of str)',
        question=SHARED_QUESTION
    )
    print(custom_response)
