from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, nullable=True)

    images = relationship("CustomerImage", back_populates="customer", cascade="all, delete-orphan")

class CustomerImage(Base):
    __tablename__ = "customer_images"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"))
    image_url = Column(String, nullable=False)  # file path or external URL

    customer = relationship("Customer", back_populates="images")
