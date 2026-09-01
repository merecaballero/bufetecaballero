from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import Lawyer
from backend.app.schemas import LawyerOut

router = APIRouter(prefix="/lawyers", tags=["Equipo Jurídico"])

@router.get(
    "",
    response_model=List[LawyerOut],
    summary="Listado de abogados y letrados del despacho"
)
def get_all_lawyers(
    db: Session = Depends(get_db)
):
    return db.query(Lawyer).filter(Lawyer.is_active == True).order_by(Lawyer.id).all()

@router.get(
    "/{slug}",
    response_model=LawyerOut,
    summary="Obtener perfil de un abogado por su identificador"
)
def get_lawyer_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    lawyer = db.query(Lawyer).filter(Lawyer.slug == slug, Lawyer.is_active == True).first()
    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Abogado con slug '{slug}' no encontrado"
        )
    return lawyer
