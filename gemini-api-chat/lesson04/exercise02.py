#!/usr/bin/env python3
"""
Lesson 4, Exercise 2: Image Analysis with Gemini Vision

Analyze images using Gemini's multimodal capabilities.
Gemini 2.0 Flash accepts PIL Image objects alongside text prompts.

TODO: Implement the functions below. See the exercise instructions for details.
"""
import os
import requests
from io import BytesIO
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

# Sample images to work with
SAMPLE_IMAGES = {
    "scones": "https://storage.googleapis.com/generativeai-downloads/images/scones.jpg",
    "city":   "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=800",
    "chart":  "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Camponotus_flavomarginatus_ant.jpg/800px-Camponotus_flavomarginatus_ant.jpg",
}


def load_image_from_url(url: str) -> Image.Image:
    """Load a PIL Image from a URL. Already implemented — use this in your functions."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))


def describe_image(image: Image.Image) -> str:
    """
    TODO: Ask Gemini to provide a detailed description of the image.

    Use model.generate_content() with a list containing:
    1. A text prompt asking for a description
    2. The PIL image object

    Return the response text.
    """
    pass  # Replace with your implementation


def answer_question_about_image(image: Image.Image, question: str) -> str:
    """
    TODO: Answer a specific question about the image.

    Use model.generate_content() with a list: [question, image]
    Return the response text.
    """
    pass  # Replace with your implementation


def compare_images(image1: Image.Image, image2: Image.Image) -> str:
    """
    TODO: Compare two images and describe the key differences.

    Use model.generate_content() with a list containing:
    [comparison_prompt, image1, label_text, image2]

    Example prompt: "Compare these two images. What are the main differences?"
    Return the response text.
    """
    pass  # Replace with your implementation


def main():
    print("Loading sample images...")
    scones_img = load_image_from_url(SAMPLE_IMAGES["scones"])
    city_img = load_image_from_url(SAMPLE_IMAGES["city"])
    print(f"Image 1 size: {scones_img.size}")
    print(f"Image 2 size: {city_img.size}")

    print("\n--- Image Description ---")
    # TODO: Call describe_image() with scones_img and print the result

    print("\n--- Specific Question ---")
    # TODO: Call answer_question_about_image() with scones_img and question:
    # "What ingredients can you identify in this image? List each item."

    print("\n--- Image Comparison ---")
    # TODO: Call compare_images() with scones_img and city_img and print the result

    print("\n--- Your Own Question ---")
    # TODO: Load any image and ask Gemini a creative question about it
    # Try: "Write a short poem inspired by this image"


if __name__ == '__main__':
    main()
