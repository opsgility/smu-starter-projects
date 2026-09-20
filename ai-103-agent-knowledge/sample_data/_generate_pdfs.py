"""Regenerate the two sample PDFs used by AI-103 Lesson 9 exercises.

Run from this folder:
    python _generate_pdfs.py

Produces:
    product-catalog.pdf  — used by Ex 1 FileSearchTool
    invoice.pdf          — used by Ex 3 Content Understanding extract_invoice
"""
from pathlib import Path

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors


HERE = Path(__file__).parent


def build_catalog():
    doc = SimpleDocTemplate(
        str(HERE / "product-catalog.pdf"),
        pagesize=LETTER,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title="Summitline Outfitters Product Catalog",
    )
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "title", parent=styles["Title"], fontSize=20, spaceAfter=6
    )
    h2 = ParagraphStyle(
        "h2", parent=styles["Heading2"], fontSize=14, spaceBefore=10, spaceAfter=4
    )
    body = styles["BodyText"]

    story = [
        Paragraph("Summitline Outfitters &mdash; Product Catalog", title),
        Paragraph(
            "Season 2026 lineup. All prices in USD. Lifetime warranty on "
            "frames and zippers; see warranty sheet for coverage details.",
            body,
        ),
        Spacer(1, 0.15 * inch),
    ]

    products = [
        (
            "Alpine 4S Tent",
            "$649",
            "4-season, double-wall mountaineering tent. Packed weight 4.6 lbs. "
            "DAC Featherlite NSL poles, 20D ripstop fly, seam-taped bathtub floor. "
            "Sleeps two with vestibule storage. Color: glacier blue.",
        ),
        (
            "Ridgeline Daypack",
            "$129",
            "28 L hiking daypack. Hydration-compatible with internal sleeve for "
            "2 L reservoir. Vented back panel, adjustable sternum strap, "
            "trekking-pole loops. Color: slate / ember.",
        ),
        (
            "Cascade 600 Sleeping Bag",
            "$299",
            "15 &deg;F 3-season mummy bag. 800-fill hydrophobic down, "
            "ripstop 20D shell, anti-snag draft tube. Fits up to 6&rsquo;2&rdquo;. "
            "Compression sack included.",
        ),
        (
            "Summit 30L Rain Shell",
            "$189",
            "3-layer waterproof / breathable shell. Fully seam-sealed, "
            "adjustable storm hood, pit zips, two zippered hand pockets. "
            "Men&rsquo;s and women&rsquo;s cuts in sizes XS&ndash;XXL.",
        ),
        (
            "Trailhead Insulated Flask",
            "$45",
            "24 oz double-wall vacuum-insulated stainless flask. "
            "Keeps coffee hot 12 hours, ice water cold 24 hours. "
            "BPA-free leakproof lid. Colors: matte black, forest, rust.",
        ),
    ]

    for name, price, desc in products:
        story.append(Paragraph(f"{name} &mdash; {price}", h2))
        story.append(Paragraph(desc, body))

    story.append(Spacer(1, 0.2 * inch))
    story.append(
        Paragraph(
            "For questions about sizing, fit, or warranty coverage, email "
            "concierge@summitline.example or chat with our concierge agent.",
            body,
        )
    )

    doc.build(story)


def build_invoice():
    doc = SimpleDocTemplate(
        str(HERE / "invoice.pdf"),
        pagesize=LETTER,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title="Cascadia Textile Supply Invoice",
    )
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "title", parent=styles["Title"], fontSize=18, spaceAfter=6
    )
    body = styles["BodyText"]
    small = ParagraphStyle("small", parent=body, fontSize=9)

    story = [
        Paragraph("INVOICE", title),
        Spacer(1, 0.05 * inch),
        Paragraph(
            "<b>From:</b> Cascadia Textile Supply Co.<br/>"
            "1402 Industrial Way, Tacoma, WA 98401<br/>"
            "accounts@cascadia-textile.example",
            body,
        ),
        Spacer(1, 0.1 * inch),
        Paragraph(
            "<b>Bill To:</b> Summitline Outfitters<br/>"
            "225 Summit Ridge Rd, Bend, OR 97701",
            body,
        ),
        Spacer(1, 0.1 * inch),
        Paragraph(
            "<b>Invoice Number:</b> CTS-2025-10418<br/>"
            "<b>Invoice Date:</b> 2025-11-03<br/>"
            "<b>Due Date:</b> 2025-12-03<br/>"
            "<b>Terms:</b> Net 30",
            body,
        ),
        Spacer(1, 0.25 * inch),
    ]

    data = [
        ["Description", "Qty", "Unit Price", "Amount"],
        ["Bolt - 400D ripstop nylon (50 yd)", "5", "290.00", "1,450.00"],
        ["Zipper assemblies (100 ct)", "3", "204.00", "612.00"],
        ["Reflective trim spool (500 m)", "1", "225.50", "225.50"],
        ["Heavy-duty thread (1 lb cone)", "10", "40.00", "400.00"],
        ["Freight & handling", "1", "160.00", "160.00"],
        ["", "", "Subtotal", "2,847.50"],
        ["", "", "Tax (Oregon, exempt)", "0.00"],
        ["", "", "Prior balance", "1,440.00"],
        ["", "", "Invoice Total", "4,287.50"],
    ]
    table = Table(data, colWidths=[3.3 * inch, 0.6 * inch, 1.3 * inch, 1.2 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("GRID", (0, 0), (-1, 5), 0.25, colors.grey),
                ("LINEABOVE", (2, 6), (-1, 6), 0.5, colors.grey),
                ("FONTNAME", (2, 9), (-1, 9), "Helvetica-Bold"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 0.25 * inch))
    story.append(
        Paragraph(
            "Please remit payment to Cascadia Textile Supply Co., "
            "ACH routing 325081403, account 00942-118. "
            "Thank you for your business.",
            small,
        )
    )

    doc.build(story)


if __name__ == "__main__":
    build_catalog()
    build_invoice()
    print("Wrote product-catalog.pdf and invoice.pdf")
