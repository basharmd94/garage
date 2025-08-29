from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.item import ItemCreate, ItemOut
from app.models import Item, ItemImage
from app.api.deps import permission_required, get_current_user
from app.core.config import UPLOAD_DIR, ITEM_UPLOAD_SUBDIR
import os
import uuid
import shutil

router = APIRouter()

@router.post("/", response_model=ItemOut)
def create_item(
    payload: ItemCreate,
    db: Session = Depends(get_db),
    _=Depends(permission_required("create-item"))
):
    if payload.sku and db.query(Item).filter(Item.sku == payload.sku).first():
        raise HTTPException(400, "SKU already exists")
    item = Item(name=payload.name, sku=payload.sku, price=payload.price)
    db.add(item)
    db.commit()
    db.refresh(item)

    for img in payload.images:
        db.add(ItemImage(item_id=item.id, image_url=img.image_url))
    db.commit()
    db.refresh(item)
    return item

@router.get("/", response_model=List[ItemOut])
def list_items(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Item).all()

@router.post("/{item_id}/images/upload", response_model=ItemOut)
def upload_item_images(
    item_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    _=Depends(permission_required("item-upload-images"))
):
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(404, "Item not found")

    base_path = os.path.join(UPLOAD_DIR, ITEM_UPLOAD_SUBDIR, str(item_id))
    os.makedirs(base_path, exist_ok=True)

    for f in files:
        ext = os.path.splitext(f.filename)[1].lower()
        fname = f"{uuid.uuid4().hex}{ext}"
        path = os.path.join(base_path, fname)
        with open(path, "wb") as out:
            shutil.copyfileobj(f.file, out)
        rel_path = os.path.relpath(path, start=UPLOAD_DIR)
        db.add(ItemImage(item_id=item.id, image_url=rel_path))
    db.commit()
    db.refresh(item)
    return item
