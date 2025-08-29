from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM
from app.schemas.user import UserCreate, UserOut
from app.models import User, Group

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(400, "Username already exists")

    user = User(
        username=user_in.username,
        email=user_in.email,
        password=hash_password(user_in.password),
        role="user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # attach groups by name (create if missing)
    for gname in user_in.groups:
        group = db.query(Group).filter(Group.name == gname).first()
        if not group:
            group = Group(name=gname)
            db.add(group)
            db.commit()
            db.refresh(group)
        if group not in user.groups:
            user.groups.append(group)
    db.commit()
    db.refresh(user)

    return UserOut(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        groups=[g.name for g in user.groups],
    )

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.password):
        raise HTTPException(400, "Invalid credentials")

    access = create_access_token({"sub": user.username, "role": user.role})
    refresh = create_refresh_token({"sub": user.username, "role": user.role})
    user.refresh_token = refresh
    db.commit()
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

@router.post("/refresh-token")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        if payload.get("typ") != "refresh":
            raise HTTPException(401, "Invalid token type")
        username = payload.get("sub")
        user = db.query(User).filter(User.username == username).first()
        if not user or user.refresh_token != refresh_token:
            raise HTTPException(401, "Invalid refresh token")
        access = create_access_token({"sub": user.username, "role": user.role})
        return {"access_token": access, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(401, "Invalid refresh token")

@router.post("/logout")
def logout(db: Session = Depends(get_db), form: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.username == form.username).first()
    if not user:
        raise HTTPException(404, "User not found")
    user.refresh_token = None
    db.commit()
    return {"message": "Logged out"}
