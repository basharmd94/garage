from pydantic import BaseModel
from typing import List

class ItemImageCreate(BaseModel):
    image_url: str

class ItemImageOut(BaseModel):
    id: int
    image_url: str
    class Config:
        from_attributes = True

class ItemCreate(BaseModel):
    name: str
    sku: str | None = None
    price: float = 0
    images: List[ItemImageCreate] = []

class ItemOut(BaseModel):
    id: int
    name: str
    sku: str | None = None
    price: float
    images: List[ItemImageOut] = []
    class Config:
        from_attributes = True
