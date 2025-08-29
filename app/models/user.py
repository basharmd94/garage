from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.session import Base

class UserGroup(Base):
    __tablename__ = "user_groups"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), index=True)
    UniqueConstraint("user_id", "group_id", name="uq_user_group")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)  # user | admin | superadmin
    refresh_token = Column(String, nullable=True)

    groups = relationship("Group", secondary="user_groups", back_populates="users", lazy="joined")
