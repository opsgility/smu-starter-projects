from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = ""
    price: float = Field(gt=0)
    category: str = "General"
    in_stock: bool = True

class ProductUpdate(BaseModel):
    name: str = None
    description: str = None
    price: float = None
    category: str = None
    in_stock: bool = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str
    in_stock: bool

    class Config:
        from_attributes = True
