from sqlalchemy import Column, Integer, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    status = Column(String, default="pending")
    total = Column(Numeric(10, 2), default=0)

    customer = relationship("Customer")
    details = relationship("OrderDetail", back_populates="order", cascade="all, delete-orphan")
