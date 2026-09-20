"""Lesson 4, Exercise 4: PromptPipeline with error handling and retry logic."""
import os
import time
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))


class RobustPromptPipeline:
    """
    A production-ready prompt pipeline with:
    - Exponential backoff retry for rate limit (429) errors
    - Graceful handling of safety filter blocks
    - Input validation before API call
    - Structured result objects (success + metadata)
    """

    def __init__(self, template: str, model_name: str = 'gemini-2.0-flash',
                 temperature: float = 1.0, max_output_tokens: int = 1024,
                 max_retries: int = 3, base_delay: float = 1.0):
        # TODO: Store all parameters as instance attributes.
        # TODO: Create the GenerativeModel with generation_config.
        pass

    def _validate_inputs(self, kwargs: dict):
        """
        Check that all {variables} in self.template are present in kwargs.
        Raise ValueError with a message listing the missing variables.
        """
        # TODO: Use string.Formatter().parse(self.template) to extract field names.
        # TODO: Raise ValueError if any required variable is missing from kwargs.
        pass

    def _run_with_retry(self, prompt: str) -> dict:
        """
        Call generate_content() with exponential backoff on ResourceExhausted (429).
        Return a dict: {'text': str, 'input_tokens': int, 'output_tokens': int,
                        'blocked': bool, 'attempts': int}
        """
        # TODO: Loop up to self.max_retries times.
        # TODO: On ResourceExhausted, sleep base_delay * (2 ** attempt) and retry.
        # TODO: On InvalidArgument, return {'text': None, 'blocked': True, 'attempts': attempt+1}
        # TODO: On success, return the result dict with usage_metadata token counts.
        # Hint: google_exceptions.ResourceExhausted catches 429
        # Hint: google_exceptions.InvalidArgument catches safety blocks
        pass

    def run(self, **kwargs) -> dict:
        """
        Validate inputs, fill template, call _run_with_retry.
        Return the result dict from _run_with_retry.
        """
        # TODO: Call self._validate_inputs(kwargs)
        # TODO: Fill template: prompt = self.template.format(**kwargs)
        # TODO: Return self._run_with_retry(prompt)
        pass


if __name__ == '__main__':
    pipeline = RobustPromptPipeline(
        template="Summarize this article in {sentences} sentences:\n\n{article}",
        temperature=0.3,
        max_output_tokens=512,
        max_retries=3,
        base_delay=1.0
    )

    article = (
        "Artificial intelligence is transforming industries worldwide. "
        "From healthcare to finance, AI systems are automating complex tasks, "
        "enabling faster decision-making, and uncovering patterns in vast datasets "
        "that would be impossible for humans to detect manually."
    )

    print("=== Running with retry and error handling ===")
    result = pipeline.run(sentences=2, article=article)

    if result['blocked']:
        print("Response was blocked by safety filters.")
    else:
        print(f"Response ({result['attempts']} attempt(s)):")
        print(result['text'])
        print(f"\nTokens used: {result['input_tokens']} in / {result['output_tokens']} out")

    # Test validation
    print("\n=== Testing input validation ===")
    try:
        pipeline.run(sentences=2)  # missing 'article'
    except ValueError as e:
        print(f"Caught expected error: {e}")
