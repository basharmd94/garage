from pydantic import BaseModel

class PermissionCreate(BaseModel):
    module: str
    endpoint_name: str
    allowed_groups: str  # CSV

    class Config:
        json_schema_extra = {
            "example": {
                "module": "items",
                "endpoint_name": "create-item",
                "allowed_groups": "admin,manager"
            }
        }

class PermissionOut(BaseModel):
    id: int
    module: str
    endpoint_name: str
    allowed_groups: str
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "module": "items",
                "endpoint_name": "create-item",
                "allowed_groups": "admin,manager"
            }
        }
