import os
from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv()

# Database
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "fastapi_rbac")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey_change_me")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", str(60 * 24 * 7))
)

# API
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")

# File uploads
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
CUSTOMER_UPLOAD_SUBDIR = "customers"
ITEM_UPLOAD_SUBDIR = "items"

# Ensure folders exist
os.makedirs(os.path.join(UPLOAD_DIR, CUSTOMER_UPLOAD_SUBDIR), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, ITEM_UPLOAD_SUBDIR), exist_ok=True)
