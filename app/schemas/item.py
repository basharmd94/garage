from pydantic import BaseModel
from typing import List

class ItemImageCreate(BaseModel):
    image_url: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "image_url": "items/example.jpg"
            }
        }

class ItemImageOut(BaseModel):
    id: int
    image_url: str
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "image_url": "items/1/abc123.jpg"
            }
        }

class ItemCreate(BaseModel):
    name: str
    sku: str | None = None
    price: float = 0
    images: List[ItemImageCreate] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Gaming Mouse",
                "sku": "GM001",
                "price": 59.99,
                "images": [
                    {"image_url": "items/mouse-front.jpg"},
                    {"image_url": "items/mouse-side.jpg"}
                ]
            }
        }

class ItemOut(BaseModel):
    id: int
    name: str
    sku: str | None = None
    price: float
    images: List[ItemImageOut] = []
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Gaming Mouse",
                "sku": "GM001",
                "price": 59.99,
                "images": [
                    {
                        "id": 1,
                        "image_url": "items/1/abc123.jpg"
                    },
                    {
                        "id": 2,
                        "image_url": "items/1/def456.jpg"
                    }
                ]
            }
        }
