"""Lesson 4, Exercise 3: PromptPipeline — parameterized, reusable prompt runner."""
import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))


class PromptPipeline:
    """
    A reusable prompt runner that takes a template string with {variable}
    placeholders and runs it against the Gemini API with supplied values.

    Example:
        pipeline = PromptPipeline(
            template="Summarize the following in {num_sentences} sentences:\n\n{text}",
            model_name='gemini-2.0-flash',
            temperature=0.3
        )
        result = pipeline.run(num_sentences=3, text="...long article...")
    """

    def __init__(self, template: str, model_name: str = 'gemini-2.0-flash',
                 temperature: float = 1.0, max_output_tokens: int = 1024,
                 system_instruction: str = None):
        # TODO: Store all parameters as instance attributes.
        # TODO: Create the GenerativeModel with generation_config and system_instruction.
        # Hint: genai.GenerationConfig(temperature=..., max_output_tokens=...)
        pass

    def run(self, **kwargs) -> str:
        """
        Fill the template with kwargs and call generate_content().
        Return response.text.
        Raise ValueError if a required template variable is missing from kwargs.
        """
        # TODO: Use self.template.format(**kwargs) to fill in variables.
        # TODO: Catch KeyError and raise a ValueError with a helpful message.
        # TODO: Call self.model.generate_content(filled_prompt) and return .text
        pass

    def run_batch(self, inputs: list) -> list:
        """
        Run the pipeline on a list of kwarg dicts. Return a list of response strings.
        inputs: [{'var1': val1, 'var2': val2}, ...]
        """
        # TODO: Call self.run(**item) for each item in inputs.
        # TODO: Return the list of results.
        pass


if __name__ == '__main__':
    # Test 1: single run
    summarizer = PromptPipeline(
        template="Summarize the following text in {num_sentences} sentences:\n\n{text}",
        temperature=0.3,
        max_output_tokens=512
    )
    article = (
        "Python is a high-level, general-purpose programming language. "
        "Its design philosophy emphasizes code readability with the use of significant indentation. "
        "Python is dynamically typed and garbage-collected. "
        "It supports multiple programming paradigms, including structured, object-oriented and functional programming."
    )
    print("=== Single Run ===")
    print(summarizer.run(num_sentences=2, text=article))

    # Test 2: batch run
    classifier = PromptPipeline(
        template="Classify the sentiment of this review as Positive, Negative, or Neutral:\n\n{review}",
        temperature=0.0,
        max_output_tokens=10
    )
    reviews = [
        {"review": "Absolutely fantastic product!"},
        {"review": "Broken out of the box."},
        {"review": "Average, nothing special."},
    ]
    print("\n=== Batch Run ===")
    results = classifier.run_batch(reviews)
    for review, result in zip(reviews, results):
        print(f"{result.strip():10s} | {review['review']}")
