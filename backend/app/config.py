import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "caballero_bufete.db"

class Settings(BaseModel):
    APP_NAME: str = "Bufete Caballero — API Jurídica"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "Backend profesional para Bufete Caballero (Alicante, desde 1947). "
        "Construido con FastAPI y servido mediante Uvicorn."
    )
    API_PREFIX: str = "/api/v1"
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")
    CORS_ORIGINS: list[str] = ["*"]
    
    ADMIN_API_KEY: str = os.getenv("ADMIN_API_KEY", "caballero-admin-1947")
    OFFICE_EMAIL: str = "caballero@icali.es"
    OFFICE_PHONE: str = "+34 965 21 87 44"
    OFFICE_ADDRESS: str = "Avda. General Marvá, 20, 1ºB, 03004 Alicante"

settings = Settings()
