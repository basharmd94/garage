from pydantic import BaseModel, EmailStr
from typing import List, Optional

class CustomerImageCreate(BaseModel):
    image_url: str

    class Config:
        json_schema_extra = {
            "example": {
                "image_url": "customers/profile.jpg"
            }
        }

class CustomerImageOut(BaseModel):
    id: int
    image_url: str
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "image_url": "customers/1/profile.jpg"
            }
        }

class CustomerCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    images: List[CustomerImageCreate] = []

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1-555-123-4567",
                "images": [
                    {"image_url": "customers/profile.jpg"},
                    {"image_url": "customers/id.jpg"}
                ]
            }
        }

class CustomerOut(BaseModel):
    id: int
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    images: List[CustomerImageOut] = []
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1-555-123-4567",
                "images": [
                    {
                        "id": 1,
                        "image_url": "customers/1/profile.jpg"
                    },
                    {
                        "id": 2,
                        "image_url": "customers/1/id.jpg"
                    }
                ]
            }
        }
