"""Generate trivial image fixtures for the Image Generation lab.

- base_image.png: 1024x1024 RGBA gradient
- mask.png: 1024x1024 RGBA with a white circle = "inpaint this region",
  transparent elsewhere = "keep as-is"

Idempotent: skips if files already exist.
"""
import os
from PIL import Image, ImageDraw

SIZE = 1024


def make_base() -> None:
    if os.path.exists("base_image.png"):
        print("[fixtures] base_image.png exists, skipping")
        return
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 255))
    px = img.load()
    for y in range(SIZE):
        for x in range(SIZE):
            px[x, y] = (int(255 * x / SIZE), int(255 * y / SIZE), 128, 255)
    img.save("base_image.png")
    print("[fixtures] wrote base_image.png")


def make_mask() -> None:
    if os.path.exists("mask.png"):
        print("[fixtures] mask.png exists, skipping")
        return
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    r = SIZE // 4
    cx, cy = SIZE // 2, SIZE // 2
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 255))
    img.save("mask.png")
    print("[fixtures] wrote mask.png")


if __name__ == "__main__":
    make_base()
    make_mask()
