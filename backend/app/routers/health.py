import datetime
import sys
import platform
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.app.database import get_db
from backend.app.config import settings

router = APIRouter(prefix="/health", tags=["Salud del Sistema"])

START_TIME = datetime.datetime.now(datetime.timezone.utc)

@router.get(
    "",
    summary="Verificar estado del servicio FastAPI y base de datos"
)
def health_check(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"

    now = datetime.datetime.now(datetime.timezone.utc)
    uptime_seconds = int((now - START_TIME).total_seconds())

    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": db_status,
        "uptime_seconds": uptime_seconds,
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "timestamp": now.isoformat()
    }
