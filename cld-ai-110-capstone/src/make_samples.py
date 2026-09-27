"""Generate the two sample fixtures the capstone pipeline processes.

Run this ONCE before `python invoice_pipeline.py invoice.pdf receipt.png`.
The generated files match the shapes used in CLD-AI-110 L4 (receipt) and L6
(3-page invoice) so the capstone router + validator have realistic inputs
without depending on files from earlier labs.
"""

from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def make_receipt():
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


def make_invoice():
    c = canvas.Canvas("invoice.pdf", pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Orion Analytics - Invoice #Q3-2026-0891")
    c.setFont("Helvetica", 11)
    c.drawString(50, 720, "Bill to: Halcyon Insurance | Date: 2026-08-31")
    c.drawString(50, 700, "Line items (page 1 of 3):")
    p1 = [("Cloud compute Q3", 12500), ("Data ingestion", 4200), ("Support tier: Gold", 8500)]
    y = 670
    for desc, price in p1:
        c.drawString(50, y, f"  {desc:<30} ${price:>8,.2f}")
        y -= 20
    c.showPage()

    c.setFont("Helvetica", 11)
    c.drawString(50, 750, "Line items (page 2 of 3):")
    p2 = [("ML training hours", 15200), ("Storage overage", 890), ("API gateway", 2100)]
    y = 720
    for desc, price in p2:
        c.drawString(50, y, f"  {desc:<30} ${price:>8,.2f}")
        y -= 20
    c.showPage()

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 750, "Totals")
    c.setFont("Helvetica", 11)
    c.drawString(50, 720, "Subtotal:        $43,390.00")
    c.drawString(50, 700, "Tax (8%):         $3,471.20")
    c.drawString(50, 680, "TOTAL DUE:       $46,861.20")
    c.drawString(50, 640, "Due: 2026-09-30")
    c.save()
    print("wrote invoice.pdf")


if __name__ == "__main__":
    make_receipt()
    make_invoice()
