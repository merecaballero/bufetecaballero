import random
import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.database import get_db
from backend.app.models import ContactMessage
from backend.app.schemas import ContactCreate, ContactResponse

router = APIRouter(prefix="/contact", tags=["Contacto"])

def generate_reference_code() -> str:
    year = datetime.datetime.now().year
    random_digits = random.randint(1000, 9999)
    return f"BC-{year}-{random_digits}"

@router.post(
    "",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Enviar consulta de contacto al bufete",
    description="Registra una nueva solicitud de consulta legal, genera un código de expediente único y la pone a disposición del equipo jurídico."
)
def create_contact_message(
    payload: ContactCreate,
    db: Session = Depends(get_db)
):
    ref_code = generate_reference_code()
    
    # Ensure uniqueness
    while db.query(ContactMessage).filter(ContactMessage.reference_code == ref_code).first() is not None:
        ref_code = generate_reference_code()

    new_contact = ContactMessage(
        reference_code=ref_code,
        full_name=payload.full_name.strip(),
        email=payload.email.strip().lower(),
        phone=payload.phone.strip() if payload.phone else None,
        legal_area=payload.legal_area,
        subject=payload.subject.strip(),
        message=payload.message.strip(),
        urgency=payload.urgency or "normal",
        preferred_contact=payload.preferred_contact or "email",
        status="nuevo"
    )
    
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

@router.get(
    "",
    response_model=List[ContactResponse],
    summary="Listar consultas recibidas",
    description="Permite consultar el listado de consultas de contacto recibidas con filtros opcionales."
)
def list_contact_messages(
    status: Optional[str] = Query(None, description="Filtrar por estado: nuevo, en_estudio, contactado, cerrado"),
    area: Optional[str] = Query(None, description="Filtrar por área jurídica"),
    search: Optional[str] = Query(None, description="Búsqueda por nombre o asunto"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(ContactMessage)
    if status:
        query = query.filter(ContactMessage.status == status)
    if area:
        query = query.filter(ContactMessage.legal_area.ilike(f"%{area}%"))
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (ContactMessage.full_name.ilike(search_pattern)) | 
            (ContactMessage.subject.ilike(search_pattern)) |
            (ContactMessage.reference_code.ilike(search_pattern))
        )
    
    return query.order_by(desc(ContactMessage.created_at)).offset(offset).limit(limit).all()

@router.get(
    "/{reference_code}",
    response_model=ContactResponse,
    summary="Obtener detalle de consulta por código de referencia"
)
def get_contact_by_ref(
    reference_code: str,
    db: Session = Depends(get_db)
):
    contact = db.query(ContactMessage).filter(ContactMessage.reference_code == reference_code).first()
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró ninguna consulta con el código {reference_code}"
        )
    return contact
