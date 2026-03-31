from fastapi import FastAPI, HTTPException, Depends
from app.models import ProductCreate, ProductResponse, ProductUpdate
from app.database import get_db, create_tables
from app import crud

app = FastAPI(title="SwiftRoute Product Service")

@app.on_event("startup")
def startup():
    create_tables()

@app.get("/products")
def list_products(skip=0, limit=10, category=None, db=Depends(get_db)):
    return crud.get_products(db, skip=skip, limit=limit, category=category)

@app.get("/products/{product_id}")
def get_product(product_id, db=Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products", status_code=201)
def create_product(product: ProductCreate, db=Depends(get_db)):
    return crud.create_product(db, product)

@app.put("/products/{product_id}")
def update_product(product_id, product: ProductUpdate, db=Depends(get_db)):
    updated = crud.update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id, db=Depends(get_db)):
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
