from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM
from app.db.session import get_db
from app.models.user import User
from app.models.permission import Permission

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def permission_required(endpoint_name: str):
    def wrapper(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> User:
        # superadmin bypass
        if current_user.role == "superadmin":
            return current_user

        perm = db.query(Permission).filter(Permission.endpoint_name == endpoint_name).first()
        if not perm:
            raise HTTPException(status_code=404, detail="Permission not configured")

        allowed_groups = [g.strip() for g in perm.allowed_groups.split(",") if g.strip()]
        user_groups = [g.name for g in current_user.groups]

        if not set(allowed_groups).intersection(user_groups):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return current_user
    return wrapper
