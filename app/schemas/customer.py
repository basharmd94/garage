from pydantic import BaseModel, EmailStr
from typing import List, Optional

class CustomerImageCreate(BaseModel):
    image_url: str

class CustomerImageOut(BaseModel):
    id: int
    image_url: str
    class Config:
        from_attributes = True

class CustomerCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    images: List[CustomerImageCreate] = []

class CustomerOut(BaseModel):
    id: int
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    images: List[CustomerImageOut] = []
    class Config:
        from_attributes = True
