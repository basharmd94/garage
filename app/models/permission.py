from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    module = Column(String, nullable=False)               # e.g. 'customer'
    endpoint_name = Column(String, unique=True, nullable=False)  # e.g. 'create-customer'
    allowed_groups = Column(String, nullable=False)       # CSV: 'staff,admin,officer'
