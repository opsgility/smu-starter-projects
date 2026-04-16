"""
Image Generation with gpt-image-1
Course 203 - Lesson 8: Image Generation Exercises

Exercises:
1. Generate an image from a text prompt with gpt-image-1
2. Control output format and quality settings
3. Edit an existing image with a mask (inpainting)
4. Generate image variations and compare outputs

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically. Do NOT set them manually.
"""
from openai import OpenAI
import base64
import os
import json
from pathlib import Path

client = OpenAI()

# Sample prompts for exercises
BASIC_PROMPT = "A futuristic cityscape at sunset with flying vehicles and neon lights, photorealistic"
PRODUCT_PROMPT = "A sleek silver smartwatch on a white background, product photography style, studio lighting"
LOGO_PROMPT = "A minimalist mountain logo for a tech startup, clean lines, blue and white color scheme, vector style"

# Paths for edit exercise
EDIT_IMAGE_PATH = "base_image.png"   # Original image (1024x1024 RGBA PNG)
EDIT_MASK_PATH = "mask.png"          # Mask: transparent where edits should occur


# -----------------------------------------------------------------------
# Exercise 1: Basic image generation
# -----------------------------------------------------------------------

def generate_image(prompt: str, output_path: str = "generated.png") -> str:
    """
    Exercise 1: Generate an image from a text prompt.

    Use client.images.generate() with:
    - model="gpt-image-1"
    - prompt=prompt
    - size="1024x1024"

    The response uses base64 encoding by default with gpt-image-1.
    Access image data via: response.data[0].b64_json

    Decode and save to output_path.

    Returns:
        output_path (the saved file path)
    """
    # TODO: Call client.images.generate(
    #   model="gpt-image-1",
    #   prompt=prompt,
    #   size="1024x1024"
    # )
    # TODO: Get b64_data = response.data[0].b64_json
    # TODO: Decode: image_bytes = base64.b64decode(b64_data)
    # TODO: Write image_bytes to output_path in "wb" mode
    # TODO: Return output_path
    pass


# -----------------------------------------------------------------------
# Exercise 2: Quality and size options
# -----------------------------------------------------------------------

def generate_with_quality(prompt: str, quality: str = "standard",
                           size: str = "1024x1024") -> tuple[str, dict]:
    """
    Exercise 2: Generate image with explicit quality and size settings.

    gpt-image-1 quality options: "low", "medium", "high", "auto"
    Size options: "1024x1024", "1536x1024", "1024x1536", "auto"

    Use client.images.generate() with quality and size parameters.

    Also capture usage info from response.usage if available.

    Returns:
        Tuple of (output_path, usage_dict)
        usage_dict: {"input_tokens": int, "output_tokens": int, "total_tokens": int}
    """
    output_path = f"quality_{quality}_{size.replace('x', '_')}.png"

    # TODO: Call client.images.generate() with model, prompt, quality, size
    # TODO: Decode and save b64_json data
    # TODO: Extract usage: getattr(response, "usage", None)
    # TODO: Return (output_path, usage dict or {})
    pass


def compare_quality_settings(prompt: str) -> None:
    """
    Exercise 2 driver: Generate same prompt at different quality levels.
    """
    print("\nComparing quality settings:")
    for quality in ["low", "medium", "high"]:
        path, usage = generate_with_quality(prompt, quality=quality, size="1024x1024")
        if path and os.path.exists(path):
            size_bytes = os.path.getsize(path)
            print(f"  {quality:8s}: {size_bytes:,} bytes | Tokens: {usage.get('total_tokens', 'N/A')}")


# -----------------------------------------------------------------------
# Exercise 3: Image editing (inpainting)
# -----------------------------------------------------------------------

def edit_image(image_path: str, mask_path: str, prompt: str,
               output_path: str = "edited.png") -> str:
    """
    Exercise 3: Edit an image using inpainting.

    Use client.images.edit() with:
    - model="gpt-image-1"
    - image=open(image_path, "rb")  — original image (RGBA PNG)
    - mask=open(mask_path, "rb")    — mask where alpha=0 means edit here
    - prompt=prompt                  — describe what to put in the masked area
    - size="1024x1024"

    The mask must be an RGBA PNG where transparent pixels indicate
    the area to be edited.

    Returns:
        output_path
    """
    # TODO: Open both image and mask files
    # TODO: Call client.images.edit(
    #   model="gpt-image-1",
    #   image=image_file,
    #   mask=mask_file,
    #   prompt=prompt,
    #   size="1024x1024"
    # )
    # TODO: Decode b64_json and save to output_path
    # TODO: Return output_path
    pass


# -----------------------------------------------------------------------
# Exercise 4: Multiple images and variations
# -----------------------------------------------------------------------

def generate_variations(prompt: str, count: int = 3) -> list[str]:
    """
    Exercise 4: Generate multiple image variations of the same prompt.

    gpt-image-1 supports n=1..10 in client.images.generate().
    Each response.data[i].b64_json is a separate image.

    Generate count images in a single API call.

    Returns:
        List of saved file paths: ["variation_0.png", "variation_1.png", ...]
    """
    # TODO: Call client.images.generate() with n=count
    # TODO: Loop over response.data to decode and save each image
    # TODO: Save as f"variation_{i}.png"
    # TODO: Return list of saved paths
    pass


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------

if __name__ == "__main__":
    print("Image Generation Exercises")
    print("=" * 60)

    # Exercise 1
    print("\nExercise 1: Basic Image Generation")
    path = generate_image(BASIC_PROMPT, output_path="basic_generated.png")
    if path and os.path.exists(path):
        print(f"  Generated: {path} ({os.path.getsize(path):,} bytes)")

    # Exercise 2
    print("\nExercise 2: Quality Comparison")
    compare_quality_settings(PRODUCT_PROMPT)

    # Exercise 3
    print("\nExercise 3: Image Editing")
    if os.path.exists(EDIT_IMAGE_PATH) and os.path.exists(EDIT_MASK_PATH):
        edited = edit_image(
            EDIT_IMAGE_PATH, EDIT_MASK_PATH,
            "Replace the masked area with a beautiful garden",
            output_path="edited_result.png"
        )
        if edited and os.path.exists(edited):
            print(f"  Edited image saved: {edited}")
    else:
        print(f"  (Skipped — place {EDIT_IMAGE_PATH} and {EDIT_MASK_PATH} in the workspace)")

    # Exercise 4
    print("\nExercise 4: Multiple Variations")
    variations = generate_variations(LOGO_PROMPT, count=3)
    for i, vpath in enumerate(variations or []):
        if vpath and os.path.exists(vpath):
            print(f"  Variation {i}: {vpath} ({os.path.getsize(vpath):,} bytes)")
