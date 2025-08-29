from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None
    groups: List[str] = []   # names of groups to attach

class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None
    role: str
    groups: List[str]

    class Config:
        from_attributes = True
