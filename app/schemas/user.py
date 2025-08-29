from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None
    groups: List[str] = []   # names of groups to attach

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "securepass123",
                "email": "john.doe@example.com",
                "groups": ["admin", "manager"]
            }
        }

class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None
    role: str
    groups: List[str]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john.doe@example.com",
                "role": "admin",
                "groups": ["admin", "manager"]
            }
        }
