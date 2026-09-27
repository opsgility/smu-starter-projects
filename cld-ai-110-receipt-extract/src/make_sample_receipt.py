"""Generate a sample receipt.png."""

from PIL import Image, ImageDraw

img = Image.new("RGB", (400, 500), "white")
d = ImageDraw.Draw(img)
lines = [
    "ORION SUPPLY CO",
    "123 Data Street",
    "Aug 14, 2026",
    "-" * 30,
    "USB-C Cable x2   $24.00",
    "HDMI Adapter x1  $18.50",
    "Notebook x3      $30.00",
    "-" * 30,
    "Subtotal:        $72.50",
    "Tax:              $6.00",
    "TOTAL:           $78.50",
]
for i, line in enumerate(lines):
    d.text((20, 20 + i * 25), line, fill="black")
img.save("receipt.png")
print("wrote receipt.png")
