"""
Semantic Similarity Search Engine
Course 202 - Lesson 2: Text Embeddings & Semantic Similarity

Build a semantic search engine over a product catalog.
Returns top-5 most similar results for any natural language query.

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically. Do NOT set them manually.
"""
from openai import OpenAI
import numpy as np
import json

client = OpenAI()

# Sample product catalog (100 products for quick demo)
PRODUCTS = [
    {"id": 1, "name": "Wireless Noise-Cancelling Headphones", "description": "Over-ear headphones with active noise cancellation, 30-hour battery, and premium sound quality for music and calls."},
    {"id": 2, "name": "Mechanical Gaming Keyboard", "description": "Tenkeyless mechanical keyboard with Cherry MX switches, RGB backlighting, and programmable macros for gaming."},
    {"id": 3, "name": "Ergonomic Office Chair", "description": "Adjustable lumbar support, breathable mesh back, and 4D armrests for all-day comfort during long work sessions."},
    {"id": 4, "name": "Portable Bluetooth Speaker", "description": "Waterproof IPX7 speaker with 360-degree sound, 24-hour playback, and rugged design for outdoor adventures."},
    {"id": 5, "name": "Standing Desk Converter", "description": "Adjustable height desk riser that converts any desk to a standing workstation, with a spacious keyboard tray."},
    {"id": 6, "name": "USB-C Hub 10-in-1", "description": "Multiport adapter with HDMI 4K, 3 USB-A, SD card reader, Ethernet, and 100W PD charging for laptops."},
    {"id": 7, "name": "Webcam 4K Ultra HD", "description": "4K 30fps webcam with autofocus, noise-cancelling dual microphones, and privacy shutter for video conferencing."},
    {"id": 8, "name": "Smart LED Desk Lamp", "description": "Color-adjustable LED lamp with USB charging port, eye-care mode, and touch-sensitive dimmer control."},
    {"id": 9, "name": "Laptop Stand Adjustable", "description": "Portable aluminum laptop stand with 6 height settings for improved posture and ergonomics at any workspace."},
    {"id": 10, "name": "Wireless Charging Pad", "description": "Qi-compatible 15W fast wireless charger for smartphones, AirPods, and other Qi-enabled devices."},
    {"id": 11, "name": "Monitor Privacy Screen", "description": "Anti-glare privacy filter that blocks side views for 27-inch monitors, reducing eye strain in open offices."},
    {"id": 12, "name": "Cable Management Kit", "description": "Desk cable organizer with 100 cable ties, 10 cable clips, and a cable sleeve for a clean, tidy workspace."},
    {"id": 13, "name": "Noise-Cancelling Earbuds", "description": "True wireless earbuds with ANC, 8-hour battery (32 with case), and IPX5 water resistance for workouts."},
    {"id": 14, "name": "Smart Notebook", "description": "Reusable smart notebook that digitizes your handwritten notes via companion app and microwave-erases pages."},
    {"id": 15, "name": "Mechanical Pencil Set", "description": "Professional drafting pencils in 0.3, 0.5, and 0.7mm with non-slip grip and smooth retractable tips."},
    {"id": 16, "name": "Monitor Light Bar", "description": "Screen-mounted LED light bar with automatic dimming, no-glare illumination, and USB power for late-night work."},
    {"id": 17, "name": "Portable SSD 2TB", "description": "2TB external SSD with USB-C, 1050 MB/s read speeds, and shock-resistant housing for fast file transfers."},
    {"id": 18, "name": "Wireless Mouse Ergonomic", "description": "Vertical ergonomic mouse that reduces wrist strain with customizable DPI, 6 buttons, and silent clicks."},
    {"id": 19, "name": "Blue Light Blocking Glasses", "description": "Computer glasses that filter 40% of blue light to reduce eye strain and improve sleep quality after screen time."},
    {"id": 20, "name": "Desk Whiteboard Pad", "description": "Large reusable whiteboard desk mat for brainstorming, note-taking, and drawing without paper waste."},
]


def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """
    Exercise 1: Get an embedding vector for a text string.

    Use client.embeddings.create() with:
    - model=model
    - input=text

    Returns:
        List of floats (the embedding vector)
    """
    # TODO: Call client.embeddings.create(model=model, input=text)
    # TODO: Return response.data[0].embedding
    pass


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """
    Exercise 2: Compute cosine similarity between two embedding vectors.

    Cosine similarity = dot(a, b) / (||a|| * ||b||)
    Returns a value between -1 and 1 (higher = more similar).

    Use numpy for the computation.
    """
    # TODO: Convert to numpy arrays
    # TODO: Compute dot product divided by product of norms
    # TODO: Return the scalar similarity score
    pass


def build_product_index(products: list[dict]) -> list[dict]:
    """
    Exercise 3: Embed all products and build a searchable index.

    For each product, combine name + description into a single string,
    get its embedding, and store it alongside the product data.

    Returns:
        List of dicts: [{...product fields..., "embedding": [...]}]
    """
    print(f"Building index for {len(products)} products...")
    indexed = []
    for i, product in enumerate(products):
        text = f"{product['name']}: {product['description']}"
        # TODO: Call get_embedding(text)
        # TODO: Append {**product, "embedding": embedding} to indexed
        if (i + 1) % 5 == 0:
            print(f"  Embedded {i + 1}/{len(products)}")
    return indexed


def semantic_search(query: str, index: list[dict], top_k: int = 5) -> list[dict]:
    """
    Exercise 4: Search the index for the most semantically similar products.

    Steps:
    1. Embed the query
    2. Compute cosine similarity between query embedding and each product embedding
    3. Sort by similarity descending
    4. Return top_k results with their similarity scores

    Returns:
        List of dicts: [{...product fields..., "score": float}]
    """
    # TODO: Get query embedding
    # TODO: For each item in index, compute cosine_similarity(query_emb, item["embedding"])
    # TODO: Sort by similarity descending, return top_k
    pass


if __name__ == "__main__":
    print("Semantic Similarity Search Engine — Course 202 Lesson 2")
    print("=" * 55)

    # Build the product index
    index = build_product_index(PRODUCTS)

    # Run test queries
    queries = [
        "comfortable chair for long work sessions",
        "wireless audio for music",
        "reduce eye strain at computer",
        "fast storage for large files",
    ]

    for query in queries:
        print(f"\nQuery: '{query}'")
        results = semantic_search(query, index, top_k=3)
        if results:
            for i, r in enumerate(results, 1):
                print(f"  {i}. [{r['score']:.3f}] {r['name']}")
