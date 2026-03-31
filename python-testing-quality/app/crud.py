from sqlalchemy.orm import Session
from app.database import ProductDB
from app.models import ProductCreate, ProductUpdate

def get_products(db, skip=0, limit=10, category=None):
    query = db.query(ProductDB)
    if category:
        query = query.filter(ProductDB.category == category)
    return query.offset(skip).limit(limit).all()

def get_product(db, product_id):
    return db.query(ProductDB).filter(ProductDB.id == product_id).first()

def create_product(db, product):
    db_product = ProductDB(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db, product_id, product):
    db_product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not db_product:
        return None
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db, product_id):
    db_product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not db_product:
        return False
    db.delete(db_product)
    db.commit()
    return True
