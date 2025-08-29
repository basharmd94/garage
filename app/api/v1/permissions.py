from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionOut
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

# ---- helpers ----
def require_admin(curr: User = Depends(get_current_user)) -> User:
    if curr.role in ("admin", "superadmin"):
        return curr
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")

def _normalize_csv(csv: str) -> str:
    # trim, dedupe, keep order
    seen = set()
    out = []
    for g in [x.strip() for x in csv.split(",") if x.strip()]:
        if g not in seen:
            seen.add(g)
            out.append(g)
    return ",".join(out)

# ---- endpoints ----
@router.post("/", response_model=PermissionOut)
def create_permission(
    payload: PermissionCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    existing = db.query(Permission).filter(Permission.endpoint_name == payload.endpoint_name).first()
    if existing:
        raise HTTPException(400, "Permission for this endpoint already exists")
    perm = Permission(
        module=payload.module,
        endpoint_name=payload.endpoint_name,
        allowed_groups=_normalize_csv(payload.allowed_groups),
    )
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return perm

@router.get("/", response_model=List[PermissionOut])
def list_permissions(
    module: Optional[str] = Query(None, description="Filter by module"),
    q: Optional[str] = Query(None, description="Search in endpoint_name"),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    query = db.query(Permission)
    if module:
        query = query.filter(Permission.module == module)
    if q:
        query = query.filter(Permission.endpoint_name.ilike(f"%{q}%"))
    return query.order_by(Permission.module.asc(), Permission.endpoint_name.asc()).all()

@router.get("/{perm_id}", response_model=PermissionOut)
def get_permission(
    perm_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    perm = db.get(Permission, perm_id)
    if not perm:
        raise HTTPException(404, "Permission not found")
    return perm

# simple update schema inline to avoid changing shared schemas
from pydantic import BaseModel
class PermissionUpdate(BaseModel):
    module: Optional[str] = None
    endpoint_name: Optional[str] = None
    allowed_groups: Optional[str] = None

@router.put("/{perm_id}", response_model=PermissionOut)
def update_permission(
    perm_id: int,
    payload: PermissionUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    perm = db.get(Permission, perm_id)
    if not perm:
        raise HTTPException(404, "Permission not found")

    if payload.endpoint_name and payload.endpoint_name != perm.endpoint_name:
        # ensure uniqueness
        dup = db.query(Permission).filter(Permission.endpoint_name == payload.endpoint_name).first()
        if dup:
            raise HTTPException(400, "Permission for this endpoint already exists")

    if payload.module is not None:
        perm.module = payload.module
    if payload.endpoint_name is not None:
        perm.endpoint_name = payload.endpoint_name
    if payload.allowed_groups is not None:
        perm.allowed_groups = _normalize_csv(payload.allowed_groups)

    db.commit()
    db.refresh(perm)
    return perm

@router.delete("/{perm_id}", status_code=204)
def delete_permission(
    perm_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    perm = db.get(Permission, perm_id)
    if not perm:
        raise HTTPException(404, "Permission not found")
    db.delete(perm)
    db.commit()
    return None

# Optional bulk upsert for convenience
class PermissionBulkIn(BaseModel):
    permissions: List[PermissionCreate]

@router.post("/bulk", response_model=List[PermissionOut])
def bulk_upsert_permissions(
    payload: PermissionBulkIn,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    out: List[Permission] = []
    for p in payload.permissions:
        norm_groups = _normalize_csv(p.allowed_groups)
        existing = db.query(Permission).filter(Permission.endpoint_name == p.endpoint_name).first()
        if existing:
            existing.module = p.module
            existing.allowed_groups = norm_groups
            db.add(existing)
            out.append(existing)
        else:
            newp = Permission(module=p.module, endpoint_name=p.endpoint_name, allowed_groups=norm_groups)
            db.add(newp)
            out.append(newp)
    db.commit()
    for p in out:
        db.refresh(p)
    return out
