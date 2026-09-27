"""Create a 3-page invoice PDF."""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

c = canvas.Canvas("invoice.pdf", pagesize=letter)
c.setFont("Helvetica-Bold", 16)

# Page 1 - header + first items
c.drawString(50, 750, "Orion Analytics - Invoice #Q3-2026-0891")
c.setFont("Helvetica", 11)
c.drawString(50, 720, "Bill to: Halcyon Insurance | Date: 2026-08-31")
c.drawString(50, 700, "Line items (page 1 of 3):")
items_p1 = [("Cloud compute Q3", 12500), ("Data ingestion", 4200), ("Support tier: Gold", 8500)]
y = 670
for desc, price in items_p1:
    c.drawString(50, y, f"  {desc:<30} ${price:>8,.2f}")
    y -= 20
c.showPage()

# Page 2
c.setFont("Helvetica", 11)
c.drawString(50, 750, "Line items (page 2 of 3):")
items_p2 = [("ML training hours", 15200), ("Storage overage", 890), ("API gateway", 2100)]
y = 720
for desc, price in items_p2:
    c.drawString(50, y, f"  {desc:<30} ${price:>8,.2f}")
    y -= 20
c.showPage()

# Page 3 - totals
c.setFont("Helvetica-Bold", 12)
c.drawString(50, 750, "Totals")
c.setFont("Helvetica", 11)
c.drawString(50, 720, "Subtotal:        $43,390.00")
c.drawString(50, 700, "Tax (8%):         $3,471.20")
c.drawString(50, 680, "TOTAL DUE:       $46,861.20")
c.drawString(50, 640, "Due: 2026-09-30")
c.save()
print("wrote invoice.pdf")
