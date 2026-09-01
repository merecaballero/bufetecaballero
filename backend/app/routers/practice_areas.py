from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import PracticeArea
from backend.app.schemas import PracticeAreaOut

router = APIRouter(prefix="/practice-areas", tags=["Áreas de Práctica"])

@router.get(
    "",
    response_model=List[PracticeAreaOut],
    summary="Listado de áreas legales especializadas"
)
def get_practice_areas(
    db: Session = Depends(get_db)
):
    return db.query(PracticeArea).order_by(PracticeArea.id).all()

@router.get(
    "/{slug}",
    response_model=PracticeAreaOut,
    summary="Obtener información de un área de práctica"
)
def get_practice_area_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    area = db.query(PracticeArea).filter(PracticeArea.slug == slug).first()
    if not area:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Área jurídica '{slug}' no encontrada"
        )
    return area
