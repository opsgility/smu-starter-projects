"""
Semantic Similarity Search Engine
Course 202 - Lesson 2: Semantic Similarity Search Engine

Exercises:
1. Generate text embeddings using text-embedding-3-small
2. Compute cosine similarity between embeddings
3. Build a semantic search engine over a product catalog
4. Return top-5 results for any natural language query

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
from openai import OpenAI
import numpy as np
import json
import math

client = OpenAI()

# -----------------------------------------------------------------------
# Sample product catalog (50 products)
# -----------------------------------------------------------------------
PRODUCT_CATALOG = [
    {"id": 1,  "name": "Wireless Noise-Canceling Headphones",       "description": "Over-ear headphones with 30-hour battery and active noise cancellation"},
    {"id": 2,  "name": "Mechanical Gaming Keyboard",                 "description": "RGB backlit keyboard with Cherry MX switches and N-key rollover"},
    {"id": 3,  "name": "4K Webcam",                                  "description": "Ultra HD webcam with built-in microphone for streaming and video calls"},
    {"id": 4,  "name": "Ergonomic Office Chair",                     "description": "Lumbar support chair with adjustable height and armrests"},
    {"id": 5,  "name": "Standing Desk Converter",                    "description": "Adjustable height desk riser for sitting and standing work positions"},
    {"id": 6,  "name": "Dual Monitor Stand",                         "description": "Adjustable arm mount for two monitors up to 27 inches"},
    {"id": 7,  "name": "USB-C Docking Station",                      "description": "12-in-1 hub with HDMI, USB-A, Ethernet, SD card, and power delivery"},
    {"id": 8,  "name": "Portable SSD 2TB",                           "description": "NVMe external drive with 2000MB/s read speed in compact form factor"},
    {"id": 9,  "name": "Wireless Charging Pad",                      "description": "15W fast charging pad compatible with Qi devices"},
    {"id": 10, "name": "Mechanical Pencil Set",                      "description": "Professional drafting pencils with 0.5mm and 0.7mm tips"},
    {"id": 11, "name": "Blue Light Blocking Glasses",                "description": "Non-prescription glasses that filter harmful blue light from screens"},
    {"id": 12, "name": "Desk Cable Management Kit",                  "description": "Cable clips, velcro ties, and cable box for organizing workspace cables"},
    {"id": 13, "name": "Smart LED Desk Lamp",                        "description": "Color temperature adjustable lamp with USB charging port and timer"},
    {"id": 14, "name": "Laptop Cooling Stand",                       "description": "Aluminum stand with dual fans for laptops up to 17 inches"},
    {"id": 15, "name": "Portable Bluetooth Speaker",                 "description": "Waterproof speaker with 360-degree sound and 24-hour battery"},
    {"id": 16, "name": "Privacy Screen Filter",                      "description": "Anti-peeping film for 15.6-inch laptops that blocks side-angle viewing"},
    {"id": 17, "name": "Wrist Rest Pad",                             "description": "Memory foam wrist support for keyboard and mouse"},
    {"id": 18, "name": "Noise-Canceling Earbuds",                    "description": "True wireless earbuds with ANC, transparency mode, and 32h total battery"},
    {"id": 19, "name": "4K Portable Monitor",                        "description": "15.6-inch USB-C portable display with HDR and 144Hz refresh rate"},
    {"id": 20, "name": "Thunderbolt 4 Hub",                          "description": "4-port Thunderbolt 4 hub with 100W pass-through charging"},
    {"id": 21, "name": "Mesh WiFi System",                           "description": "Tri-band mesh router covering up to 6000 sq ft with 10Gbps backhaul"},
    {"id": 22, "name": "Smart Plug with Energy Monitor",             "description": "Wi-Fi outlet with power usage tracking and schedule control"},
    {"id": 23, "name": "Programmable Macro Keypad",                  "description": "15-key OLED display pad for shortcuts, macros, and stream control"},
    {"id": 24, "name": "Vertical Mouse",                             "description": "Ergonomic vertical mouse design reduces arm pronation and wrist strain"},
    {"id": 25, "name": "Fingerprint USB Security Key",               "description": "FIDO2 hardware key with biometric fingerprint sensor for passwordless login"},
    {"id": 26, "name": "3D Printer Filament Bundle",                 "description": "10-pack of PLA filament in assorted colors, 1.75mm diameter"},
    {"id": 27, "name": "Smart Home Hub",                             "description": "Zigbee and Z-Wave controller compatible with Alexa, Google, and Apple HomeKit"},
    {"id": 28, "name": "Digital Drawing Tablet",                     "description": "10-inch pressure-sensitive tablet for illustration and photo editing"},
    {"id": 29, "name": "Laptop Stand Adjustable",                    "description": "Portable aluminum stand with 6 height levels for MacBook and laptops"},
    {"id": 30, "name": "USB Microphone",                             "description": "Cardioid condenser microphone for podcasting, streaming, and recording"},
    {"id": 31, "name": "Keyboard Tray Under Desk",                   "description": "Sliding drawer mount for keyboard and mouse with negative tilt"},
    {"id": 32, "name": "Anti-Fatigue Floor Mat",                     "description": "Cushioned mat for standing desks, reduces leg and back fatigue"},
    {"id": 33, "name": "NAS Storage Device 4-Bay",                   "description": "Network-attached storage with RAID support for home and small office"},
    {"id": 34, "name": "Webcam Privacy Cover",                       "description": "Universal sliding shutter cover for laptop and desktop cameras"},
    {"id": 35, "name": "Wireless Trackball Mouse",                   "description": "Ergonomic trackball with customizable scroll wheel and Bluetooth/USB connectivity"},
    {"id": 36, "name": "Monitor Calibration Tool",                   "description": "Colorimeter for accurate color profiles on photo and video work monitors"},
    {"id": 37, "name": "Power Bank 30000mAh",                        "description": "High-capacity portable charger with 65W USB-C PD and dual USB-A ports"},
    {"id": 38, "name": "Smart LED Strip Lights",                     "description": "WiFi-enabled RGB LED strips with music sync and app control"},
    {"id": 39, "name": "Document Scanner",                           "description": "Portable sheet-fed scanner for receipts, business cards, and A4 documents"},
    {"id": 40, "name": "Surge Protector Power Strip",                "description": "8-outlet strip with 4 USB ports, 4000J surge protection, and flat plug"},
    {"id": 41, "name": "Bamboo Desk Organizer",                      "description": "Desktop storage with compartments for pens, phones, and office supplies"},
    {"id": 42, "name": "USB-C to HDMI Cable",                        "description": "8K capable cable for connecting laptops to monitors and TVs"},
    {"id": 43, "name": "Wireless Presenter Remote",                  "description": "Laser pointer with slide control, compatible with PowerPoint and Keynote"},
    {"id": 44, "name": "Acoustic Foam Panels",                       "description": "Sound-absorbing panels for home studio and recording space treatment"},
    {"id": 45, "name": "Mini PC Desktop",                            "description": "Compact desktop with Intel Core i7, 16GB RAM, 512GB SSD, 4K output"},
    {"id": 46, "name": "Wireless Number Pad",                        "description": "Slim Bluetooth numeric keypad for laptop users without a numpad"},
    {"id": 47, "name": "Laptop Privacy Webcam with LED Ring",        "description": "1080p webcam with built-in ring light and privacy shutter"},
    {"id": 48, "name": "Cable Management Box",                       "description": "Wood-finish box to hide surge protectors and cable clutter"},
    {"id": 49, "name": "Wireless Keyboard and Mouse Combo",          "description": "Full-size quiet keyboard and precision mouse with USB nano receiver"},
    {"id": 50, "name": "Monitor Light Bar",                          "description": "USB-powered screen bar lamp with no screen glare, adjustable color temperature"},
]

# Test queries for the search engine
TEST_QUERIES = [
    "headphones for blocking out office noise",
    "keyboard for gaming with RGB lights",
    "reduce eye strain from screen",
    "organize cables on my desk",
    "security for logging into my computer without a password",
    "record audio for a podcast",
    "ergonomic equipment for wrist pain",
    "external storage with fast speeds",
    "video calls and meetings",
    "charge multiple devices at once",
]


def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """
    Exercise 1: Generate an embedding vector for the given text.

    Use client.embeddings.create() with the specified model.
    Return response.data[0].embedding as a list of floats.

    Args:
        text: The text to embed
        model: The embedding model to use

    Returns:
        Embedding vector as a list of floats
    """
    # TODO: Call client.embeddings.create(model=model, input=text)
    # TODO: Return response.data[0].embedding
    return []


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Exercise 2: Compute cosine similarity between two embedding vectors.

    Formula: dot(a, b) / (norm(a) * norm(b))
    Values range from -1 (opposite) to 1 (identical).
    A score >= 0.75 indicates strong semantic similarity.

    Args:
        vec_a: First embedding vector
        vec_b: Second embedding vector

    Returns:
        Cosine similarity score between -1 and 1
    """
    # Option A: Manual implementation using math module
    # dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    # norm_a = math.sqrt(sum(x**2 for x in vec_a))
    # norm_b = math.sqrt(sum(x**2 for x in vec_b))
    # return dot_product / (norm_a * norm_b)

    # Option B: NumPy implementation
    # TODO: Use np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return 0.0


def build_search_index(products: list[dict]) -> list[dict]:
    """
    Exercise 3a: Build a semantic search index from the product catalog.

    For each product, concatenate name + description and generate an embedding.
    Add the embedding to the product dict as a new "embedding" key.
    Print progress every 10 products.

    Args:
        products: List of product dicts with "name" and "description"

    Returns:
        Products list with "embedding" added to each product
    """
    indexed = []
    print(f"Building embeddings for {len(products)} products...")
    for i, product in enumerate(products):
        text = f"{product['name']}: {product['description']}"
        # TODO: Call get_embedding(text)
        # TODO: Add embedding to a copy of the product dict
        # TODO: Append to indexed list
        # TODO: Print progress every 10 items: f"  Embedded {i+1}/{len(products)}"
        indexed.append(product)  # Replace with your implementation
    return indexed


def semantic_search(query: str, index: list[dict], top_k: int = 5) -> list[dict]:
    """
    Exercise 3b: Find the top-k most semantically similar products.

    1. Generate embedding for the query
    2. Compute cosine similarity between query embedding and each product embedding
    3. Sort by similarity descending
    4. Return the top_k results

    Each result should include: id, name, description, and similarity_score.

    Args:
        query: Natural language search query
        index: Indexed products with embeddings
        top_k: Number of results to return

    Returns:
        List of top-k product dicts with similarity_score added
    """
    # TODO: Get query_embedding = get_embedding(query)
    # TODO: For each product in index: compute similarity between query_embedding and product["embedding"]
    # TODO: Sort products by similarity descending
    # TODO: Return top_k results with similarity_score added
    return []


if __name__ == "__main__":
    print("=" * 60)
    print("Exercise 1 & 2: Embedding and Cosine Similarity Demo")
    print("=" * 60)

    # Test similarity between related and unrelated phrases
    text_a = "noise-canceling headphones for music"
    text_b = "wireless earbuds with active noise cancellation"
    text_c = "standing desk ergonomic chair"

    emb_a = get_embedding(text_a)
    emb_b = get_embedding(text_b)
    emb_c = get_embedding(text_c)

    if emb_a and emb_b and emb_c:
        print(f"Embedding dimension: {len(emb_a)}")
        print(f"Similarity(A,B) [related]: {cosine_similarity(emb_a, emb_b):.4f}")
        print(f"Similarity(A,C) [unrelated]: {cosine_similarity(emb_a, emb_c):.4f}")

    print("\n" + "=" * 60)
    print("Exercise 3: Semantic Search Engine")
    print("=" * 60)

    # Build the search index
    search_index = build_search_index(PRODUCT_CATALOG)
    print(f"Index ready with {len(search_index)} products\n")

    # Run test queries
    for query in TEST_QUERIES[:3]:  # Run 3 for demo (more API calls)
        print(f"\nQuery: '{query}'")
        results = semantic_search(query, search_index, top_k=5)
        for rank, result in enumerate(results, 1):
            score = result.get("similarity_score", 0)
            print(f"  {rank}. [{score:.4f}] {result['name']}")
