from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine, Base
from app.models import Group, User, UserGroup, Permission
from app.core.security import hash_password

Base.metadata.create_all(bind=engine)
db: Session = SessionLocal()

# Groups
group_names = ["staff", "officer", "admin", "superadmin"]
for name in group_names:
    if not db.query(Group).filter(Group.name == name).first():
        db.add(Group(name=name))
db.commit()

# Users
seed_users = [
    ("staff1", "staff123", "user", ["staff"]),
    ("officer1", "officer123", "user", ["officer"]),
    ("admin1", "admin123", "admin", ["admin"]),
    ("super1", "super123", "superadmin", ["superadmin"]),
]
for username, password, role, groups in seed_users:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = User(username=username, password=hash_password(password), role=role)
        db.add(user)
        db.commit()
        db.refresh(user)
    # attach groups
    for gname in groups:
        g = db.query(Group).filter(Group.name == gname).first()
        if g and g not in user.groups:
            user.groups.append(g)
    db.commit()

# Permissions (CSV allowed_groups)
permissions = [
    ("customer", "create-customer", "staff,admin,officer"),
    ("customer", "customer-upload-images", "staff,admin"),
    ("item", "create-item", "admin,officer"),
    ("item", "item-upload-images", "admin,officer"),
]
for module, endpoint, csv_groups in permissions:
    if not db.query(Permission).filter(Permission.endpoint_name == endpoint).first():
        db.add(Permission(module=module, endpoint_name=endpoint, allowed_groups=csv_groups))
db.commit()

print("Seeding complete.")
db.close()
