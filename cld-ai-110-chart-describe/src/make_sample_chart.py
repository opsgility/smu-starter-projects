"""Create a sample chart.png if you don't have one handy."""

from PIL import Image, ImageDraw, ImageFont

img = Image.new("RGB", (600, 400), "white")
d = ImageDraw.Draw(img)
d.text((20, 20), "Orion Q3 revenue by region ($M)", fill="black")
bars = [("NA", 145), ("EU", 89), ("APAC", 62), ("LATAM", 24)]
for i, (label, val) in enumerate(bars):
    x = 60 + i * 130
    h = val * 2
    d.rectangle([x, 380 - h, x + 80, 380], fill="steelblue")
    d.text((x + 20, 385 - h - 15), f"${val}", fill="black")
    d.text((x + 30, 385), label, fill="black")
img.save("chart.png")
print("wrote chart.png")
