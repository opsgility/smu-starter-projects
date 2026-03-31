"""FastAPI application with intentional performance issues for profiling exercises."""
from fastapi import FastAPI, Depends
from app.database import get_db, create_tables, ProductDB
from sqlalchemy.orm import Session
import time
import hashlib
import json
import httpx

app = FastAPI(title="StreamForge Product Service — Unoptimized")

@app.on_event("startup")
def startup():
    create_tables()

@app.get("/products")
def list_products(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    # Intentionally slow: creates new DB connection each time (no pooling)
    products = db.query(ProductDB).offset(skip).limit(limit).all()
    # Intentionally slow: serializes each product individually
    results = []
    for p in products:
        results.append({
            "id": p.id, "name": p.name, "price": p.price,
            "category": p.category, "hash": hashlib.sha256(p.name.encode()).hexdigest()
        })
    return results

@app.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        return {"error": "not found"}
    return {"id": product.id, "name": product.name, "price": product.price}

@app.get("/products/{product_id}/price/{currency}")
def get_price_in_currency(product_id: int, currency: str, db: Session = Depends(get_db)):
    # Intentionally slow: makes external API call on every request (no caching)
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        return {"error": "not found"}
    # Simulate slow external call
    time.sleep(0.1)
    rate = 1.0 if currency == "USD" else 0.85 if currency == "EUR" else 0.79
    return {"id": product.id, "price": round(product.price * rate, 2), "currency": currency}

@app.get("/slow-report")
def generate_report(db: Session = Depends(get_db)):
    """Intentionally unoptimized report generation for profiling exercise."""
    products = db.query(ProductDB).all()
    report = {"categories": {}, "total_value": 0}
    for p in products:
        # Intentionally slow: recalculates hash for each product
        p_hash = hashlib.sha256(json.dumps({"name": p.name, "price": p.price}).encode()).hexdigest()
        if p.category not in report["categories"]:
            report["categories"][p.category] = {"count": 0, "total": 0, "products": []}
        report["categories"][p.category]["count"] += 1
        report["categories"][p.category]["total"] += p.price
        report["categories"][p.category]["products"].append({"name": p.name, "hash": p_hash})
        report["total_value"] += p.price
    return report
