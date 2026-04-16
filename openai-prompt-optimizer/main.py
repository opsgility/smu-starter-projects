"""
Prompt Optimization Lab
Course 102 - Lesson 8: Prompt Optimization

Exercises:
1. Measure the token count of a baseline verbose prompt
2. Apply compression techniques to reduce token count by >= 30%
3. Measure quality retention using LLM-as-judge (>= 90% of baseline quality)
4. Generate an optimization log comparing baseline vs compressed

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
from openai import OpenAI
from pydantic import BaseModel
import tiktoken
import json
from datetime import datetime, timezone

client = OpenAI()
encoder = tiktoken.encoding_for_model("gpt-4.1-mini")

# BASELINE: A verbose, redundant prompt that needs optimization
BASELINE_PROMPT = """You are an extremely helpful, knowledgeable, and friendly AI assistant.
I need you to help me with a very important task. Please be very detailed and thorough in
your response. I want you to carefully analyze and summarize the following text for me.
Please make sure to include all the main points and key ideas. Also, please ensure that
your summary is comprehensive and covers everything that is mentioned in the text. It is
very important that you capture all the important information and don't miss anything.
Please also make sure your summary is clear and easy to understand.

Text to summarize:
{{TEXT}}

Please provide a thorough, detailed, and comprehensive summary of the above text, making
sure to include all the main ideas, key points, and important information mentioned in
the text above. Thank you for your assistance with this task."""

# Sample text to insert into the prompt
SAMPLE_TEXT = """Machine learning is a subset of artificial intelligence that enables
systems to learn from data and improve over time without being explicitly programmed.
It uses algorithms to parse data, learn from it, and make decisions with minimal human
intervention. Common approaches include supervised learning (using labeled training data),
unsupervised learning (finding patterns in unlabeled data), and reinforcement learning
(learning through trial and error with rewards)."""


class QualityScore(BaseModel):
    score: float        # 0.0 to 1.0
    reasoning: str      # Why this score was given
    missing_points: list[str]  # Key points from baseline missing in compressed output


class OptimizationResult(BaseModel):
    technique: str
    original_tokens: int
    compressed_tokens: int
    token_reduction_pct: float
    quality_score: float
    quality_retained_pct: float
    passes_threshold: bool


def count_tokens(text: str) -> int:
    """Count tokens using tiktoken."""
    return len(encoder.encode(text))


def get_response(prompt: str, text: str) -> str:
    """
    Exercise 1a: Get a response using the given prompt template.

    Replace {{TEXT}} in the prompt with the actual text.
    Call client.responses.create() with model="gpt-4.1-mini".
    Return response.output_text.

    Args:
        prompt: The prompt template (may contain {{TEXT}} placeholder)
        text: The text to insert into the template

    Returns:
        The model's response text
    """
    filled_prompt = prompt.replace("{{TEXT}}", text)
    # TODO: Call client.responses.create(model="gpt-4.1-mini", input=filled_prompt)
    # TODO: Return response.output_text
    return ""


def compress_prompt(verbose_prompt: str) -> str:
    """
    Exercise 2: Compress the prompt by removing redundancy.

    Apply these compression techniques:
    1. Remove filler phrases ("very", "extremely", "please", "thank you")
    2. Remove redundant instructions (deduplicate similar instructions)
    3. Shorten verbose phrasing to concise equivalents
    4. Remove meta-commentary ("I need you to", "It is very important that")

    The compressed prompt must:
    - Retain the core task instruction
    - Retain the {{TEXT}} placeholder
    - Be at least 30% shorter in token count

    You can write this manually (hard-coding compression rules) or
    use the model to compress it - either approach works.

    Args:
        verbose_prompt: The original verbose prompt

    Returns:
        The compressed prompt (still containing {{TEXT}} placeholder)
    """
    # Option A: Use the model to compress the prompt
    meta_prompt = f"""Compress this prompt to reduce token count by at least 30%.
Keep the core instruction and {{{{TEXT}}}} placeholder.
Remove: filler words, redundant instructions, verbose phrasing.
Return ONLY the compressed prompt, no explanation.

Original prompt:
{verbose_prompt}"""

    # TODO: Call client.responses.create(model="gpt-4.1-mini", input=meta_prompt)
    # TODO: Return response.output_text (the compressed prompt)
    return verbose_prompt  # Replace with your implementation


def score_quality(baseline_output: str, compressed_output: str) -> QualityScore:
    """
    Exercise 3: Use LLM-as-judge to score the quality of the compressed output.

    Ask GPT-4.1 to compare the baseline output (gold standard) against the
    compressed output. Score from 0.0 to 1.0 where:
    - 1.0 = identical quality, all points covered
    - 0.9 = very minor omissions, still high quality
    - 0.8 = some points missing but core content intact
    - < 0.8 = significant quality loss

    Use client.responses.parse() with QualityScore schema.
    Target: >= 0.90 quality score (retain 90% of baseline quality).

    Args:
        baseline_output: The response from the verbose baseline prompt
        compressed_output: The response from the compressed prompt

    Returns:
        QualityScore with score, reasoning, and missing_points
    """
    judge_prompt = f"""You are a quality evaluator. Score the COMPRESSED response compared to the BASELINE.

BASELINE (gold standard):
{baseline_output}

COMPRESSED response to evaluate:
{compressed_output}

Score the compressed response from 0.0 to 1.0:
- 1.0 = all key information preserved, equal quality
- 0.9 = minor omissions but effectively equivalent
- 0.8 = some notable omissions
- 0.7 or below = significant quality loss"""

    # TODO: Call client.responses.parse() with:
    #   model = "gpt-4.1"
    #   input = judge_prompt
    #   text_format = QualityScore
    # TODO: Return response.output_parsed
    pass


def run_optimization_experiment(text: str = SAMPLE_TEXT) -> None:
    """
    Exercise 4: Run the full optimization experiment and generate a report.

    Steps:
    1. Get baseline response and count tokens
    2. Compress the prompt (reduce >= 30%)
    3. Get compressed response and count tokens
    4. Score quality (target >= 90% retained)
    5. Print an optimization log:

    OPTIMIZATION REPORT
    ===================
    Original tokens:   XXX
    Compressed tokens: XXX
    Token reduction:   XX.X%   [PASS/FAIL: target >= 30%]

    Quality score:     X.XX
    Quality retained:  XX.X%   [PASS/FAIL: target >= 90%]

    VERDICT: [PASS/FAIL - both thresholds met]
    """
    print("Running baseline...")
    baseline_prompt_filled = BASELINE_PROMPT.replace("{{TEXT}}", text)
    baseline_tokens = count_tokens(baseline_prompt_filled)
    baseline_output = get_response(BASELINE_PROMPT, text)

    print("Compressing prompt...")
    compressed_prompt = compress_prompt(BASELINE_PROMPT)
    compressed_prompt_filled = compressed_prompt.replace("{{TEXT}}", text)
    compressed_tokens = count_tokens(compressed_prompt_filled)
    compressed_output = get_response(compressed_prompt, text)

    # Calculate reduction
    reduction_pct = (baseline_tokens - compressed_tokens) / baseline_tokens * 100

    print("Scoring quality (LLM-as-judge)...")
    quality = score_quality(baseline_output, compressed_output)
    quality_retained_pct = (quality.score if quality else 0.0) * 100

    # TODO: Print the optimization report as described above
    print("\n" + "=" * 50)
    print("OPTIMIZATION REPORT")
    print("=" * 50)
    print(f"Original tokens:   {baseline_tokens}")
    print(f"Compressed tokens: {compressed_tokens}")
    print(f"Token reduction:   {reduction_pct:.1f}%  {'✓ PASS' if reduction_pct >= 30 else '✗ FAIL'} (target >= 30%)")
    if quality:
        print(f"\nQuality score:     {quality.score:.2f}")
        print(f"Quality retained:  {quality_retained_pct:.1f}% {'✓ PASS' if quality.score >= 0.90 else '✗ FAIL'} (target >= 90%)")
        print(f"\nVerdict: {'✓ PASS - Both thresholds met!' if reduction_pct >= 30 and quality.score >= 0.90 else '✗ FAIL - Threshold(s) not met'}")


if __name__ == "__main__":
    print("=" * 60)
    print("EXERCISE 1: Measure Baseline Token Count")
    print("=" * 60)
    baseline_filled = BASELINE_PROMPT.replace("{{TEXT}}", SAMPLE_TEXT)
    print(f"Baseline prompt token count: {count_tokens(baseline_filled)}")
    print(f"Sample text token count: {count_tokens(SAMPLE_TEXT)}")

    print("\n" + "=" * 60)
    print("EXERCISE 2-4: Full Optimization Experiment")
    print("=" * 60)
    run_optimization_experiment(SAMPLE_TEXT)
