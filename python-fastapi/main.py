"""FastAPI web application."""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="SkillMeUp Labs API")


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float


items: list[Item] = []


@app.get("/")
def root():
    return {"message": "Hello from FastAPI!", "docs": "/docs"}


@app.get("/items")
def list_items():
    return items


@app.post("/items", status_code=201)
def create_item(item: Item):
    items.append(item)
    return item


@app.get("/items/{index}")
def get_item(index: int):
    if 0 <= index < len(items):
        return items[index]
    return {"error": "Item not found"}
