"""Generate a simple invoice image fixture for the Vision lab.

- invoice_sample.jpg: 1024x768 PIL-rendered fake invoice with header,
  parties, two line items, and totals.

Idempotent: skips if the file already exists.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 768


def _load_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def make_invoice() -> None:
    if os.path.exists("invoice_sample.jpg"):
        print("[fixtures] invoice_sample.jpg exists, skipping")
        return

    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    title_font = _load_font(44)
    header_font = _load_font(26)
    body_font = _load_font(22)
    total_font = _load_font(24)

    # Header
    draw.text((40, 30), "ACME CORP", fill=(20, 30, 80), font=title_font)
    draw.text((40, 90), "INVOICE #INV-2025-0042", fill=(30, 30, 30), font=header_font)
    draw.text((40, 125), "Date: 2025-11-15", fill=(60, 60, 60), font=body_font)

    # Parties
    draw.text((40, 190), "From:", fill=(20, 20, 20), font=header_font)
    draw.text((40, 225), "Acme Corp, 123 Main St", fill=(40, 40, 40), font=body_font)
    draw.text((540, 190), "To:", fill=(20, 20, 20), font=header_font)
    draw.text((540, 225), "Beta LLC, 456 Elm St", fill=(40, 40, 40), font=body_font)

    # Divider
    draw.line((40, 290, W - 40, 290), fill=(180, 180, 180), width=2)

    # Line items
    draw.text((40, 310), "Description", fill=(20, 20, 20), font=header_font)
    draw.text((540, 310), "Qty", fill=(20, 20, 20), font=header_font)
    draw.text((680, 310), "Price", fill=(20, 20, 20), font=header_font)
    draw.text((860, 310), "Amount", fill=(20, 20, 20), font=header_font)

    draw.text((40, 360), "Widget", fill=(40, 40, 40), font=body_font)
    draw.text((540, 360), "10", fill=(40, 40, 40), font=body_font)
    draw.text((680, 360), "$25.00", fill=(40, 40, 40), font=body_font)
    draw.text((860, 360), "$250.00", fill=(40, 40, 40), font=body_font)

    draw.text((40, 400), "Gadget", fill=(40, 40, 40), font=body_font)
    draw.text((540, 400), "5", fill=(40, 40, 40), font=body_font)
    draw.text((680, 400), "$40.00", fill=(40, 40, 40), font=body_font)
    draw.text((860, 400), "$200.00", fill=(40, 40, 40), font=body_font)

    draw.line((40, 460, W - 40, 460), fill=(180, 180, 180), width=2)

    # Totals
    draw.text((640, 490), "Subtotal:", fill=(30, 30, 30), font=total_font)
    draw.text((860, 490), "$450.00", fill=(30, 30, 30), font=total_font)
    draw.text((640, 530), "Tax:", fill=(30, 30, 30), font=total_font)
    draw.text((860, 530), "$36.00", fill=(30, 30, 30), font=total_font)
    draw.text((640, 580), "Total:", fill=(20, 30, 80), font=total_font)
    draw.text((860, 580), "$486.00", fill=(20, 30, 80), font=total_font)

    img.save("invoice_sample.jpg", quality=90)
    print("[fixtures] wrote invoice_sample.jpg")


if __name__ == "__main__":
    make_invoice()
