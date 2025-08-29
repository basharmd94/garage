from pydantic import BaseModel

class PermissionCreate(BaseModel):
    module: str
    endpoint_name: str
    allowed_groups: str  # CSV

class PermissionOut(BaseModel):
    id: int
    module: str
    endpoint_name: str
    allowed_groups: str
    class Config:
        from_attributes = True
