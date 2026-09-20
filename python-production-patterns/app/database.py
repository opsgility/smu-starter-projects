"""Database setup — intentionally uses default pool settings for optimization exercises."""
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./products.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ProductDB(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String, default="General")
    in_stock = Column(Boolean, default=True)

def create_tables():
    Base.metadata.create_all(bind=engine)
    # Seed data if empty
    db = SessionLocal()
    if db.query(ProductDB).count() == 0:
        categories = ["Electronics", "Furniture", "Stationery", "Tools"]
        for i in range(200):
            db.add(ProductDB(
                name=f"Product-{i:04d}",
                price=round(9.99 + (i * 3.33) % 500, 2),
                category=categories[i % len(categories)],
                in_stock=i % 7 != 0
            ))
        db.commit()
    db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
