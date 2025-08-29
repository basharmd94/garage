from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.customer import CustomerCreate, CustomerOut
from app.models import Customer, CustomerImage
from app.api.deps import permission_required, get_current_user
from app.core.config import UPLOAD_DIR, CUSTOMER_UPLOAD_SUBDIR
import os
import uuid
import shutil

router = APIRouter()

@router.post("/", response_model=CustomerOut)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
    _=Depends(permission_required("create-customer"))
):
    if payload.email and db.query(Customer).filter(Customer.email == payload.email).first():
        raise HTTPException(400, "Email already exists")
    customer = Customer(name=payload.name, email=payload.email, phone=payload.phone)
    db.add(customer)
    db.commit()
    db.refresh(customer)

    for img in payload.images:
        db.add(CustomerImage(customer_id=customer.id, image_url=img.image_url))
    db.commit()
    db.refresh(customer)
    return customer

@router.get("/", response_model=List[CustomerOut])
def list_customers(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Customer).all()

@router.post("/{customer_id}/images/upload", response_model=CustomerOut)
def upload_customer_images(
    customer_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    _=Depends(permission_required("customer-upload-images"))  # configure in permissions table
):
    customer = db.query(Customer).get(customer_id)
    if not customer:
        raise HTTPException(404, "Customer not found")

    base_path = os.path.join(UPLOAD_DIR, CUSTOMER_UPLOAD_SUBDIR, str(customer_id))
    os.makedirs(base_path, exist_ok=True)

    for f in files:
        ext = os.path.splitext(f.filename)[1].lower()
        fname = f"{uuid.uuid4().hex}{ext}"
        path = os.path.join(base_path, fname)
        with open(path, "wb") as out:
            shutil.copyfileobj(f.file, out)
        rel_path = os.path.relpath(path, start=UPLOAD_DIR)
        db.add(CustomerImage(customer_id=customer.id, image_url=rel_path))
    db.commit()
    db.refresh(customer)
    return customer
