from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine, Base
from app.api.v1 import auth, customers, items
from app.core.config import API_PREFIX

app = FastAPI(title="FastAPI RBAC Starter")

# Create tables in dev/demo (use Alembic in real projects)
Base.metadata.create_all(bind=engine)

# CORS (tighten in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix=f"{API_PREFIX}/auth", tags=["auth"])
app.include_router(customers.router, prefix=f"{API_PREFIX}/customers", tags=["customers"])
app.include_router(items.router, prefix=f"{API_PREFIX}/items", tags=["items"])

@app.get("/")
def root():
    return {"status": "ok", "name": "FastAPI RBAC Starter"}
