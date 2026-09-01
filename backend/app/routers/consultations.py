import random
import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.database import get_db
from backend.app.models import ConsultationBooking
from backend.app.schemas import ConsultationCreate, ConsultationResponse

router = APIRouter(prefix="/consultations", tags=["Citas y Consultas"])

ALL_SLOTS = [
    "09:30 - 10:30",
    "10:30 - 11:30",
    "11:30 - 12:30",
    "12:30 - 13:30",
    "16:30 - 17:30",
    "17:30 - 18:30",
    "18:30 - 19:30",
]

def generate_booking_code() -> str:
    random_num = random.randint(1000, 9999)
    return f"CITA-{random_num}"

@router.get(
    "/available-slots",
    summary="Consultar franjas horarias disponibles para una fecha",
    description="Devuelve las franjas horarias del despacho para el día indicado indicando disponibilidad."
)
def get_available_slots(
    date: str = Query(..., description="Fecha en formato YYYY-MM-DD", pattern=r"^\d{4}-\d{2}-\d{2}$"),
    lawyer_name: Optional[str] = Query(None, description="Nombre del abogado opcional"),
    db: Session = Depends(get_db)
):
    query = db.query(ConsultationBooking).filter(
        ConsultationBooking.booking_date == date,
        ConsultationBooking.status.in_(["confirmada", "en_espera"])
    )
    if lawyer_name and lawyer_name != "Cualquiera disponible":
        query = query.filter(ConsultationBooking.preferred_lawyer_name == lawyer_name)
        
    booked_records = query.all()
    booked_slots = [b.time_slot for b in booked_records]

    slot_statuses = []
    for slot in ALL_SLOTS:
        is_available = slot not in booked_slots
        slot_statuses.append({
            "slot": slot,
            "available": is_available
        })

    return {
        "date": date,
        "lawyer": lawyer_name or "Cualquiera disponible",
        "slots": slot_statuses,
        "total_available": sum(1 for s in slot_statuses if s["available"])
    }

@router.post(
    "",
    response_model=ConsultationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Reservar consulta jurídica",
    description="Programa una cita de asesoramiento legal (presencial, telefónica o videollamada) con los letrados del despacho."
)
def create_consultation(
    payload: ConsultationCreate,
    db: Session = Depends(get_db)
):
    # Verify slot is not already taken for this date and lawyer
    existing = db.query(ConsultationBooking).filter(
        ConsultationBooking.booking_date == payload.booking_date,
        ConsultationBooking.time_slot == payload.time_slot,
        ConsultationBooking.preferred_lawyer_name == payload.preferred_lawyer_name,
        ConsultationBooking.status.in_(["confirmada", "en_espera"])
    ).first()

    if existing and payload.preferred_lawyer_name != "Cualquiera disponible":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"La franja horaria {payload.time_slot} para el día {payload.booking_date} con {payload.preferred_lawyer_name} ya está reservada. Por favor seleccione otra hora."
        )

    ref_code = generate_booking_code()
    while db.query(ConsultationBooking).filter(ConsultationBooking.reference_code == ref_code).first() is not None:
        ref_code = generate_booking_code()

    new_booking = ConsultationBooking(
        reference_code=ref_code,
        client_name=payload.client_name.strip(),
        email=payload.email.strip().lower(),
        phone=payload.phone.strip(),
        practice_area=payload.practice_area,
        preferred_lawyer_name=payload.preferred_lawyer_name or "Cualquiera disponible",
        consultation_type=payload.consultation_type,
        booking_date=payload.booking_date,
        time_slot=payload.time_slot,
        brief_summary=payload.brief_summary.strip() if payload.brief_summary else None,
        status="confirmada"
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.get(
    "",
    response_model=List[ConsultationResponse],
    summary="Listar citas programadas"
)
def list_consultations(
    date: Optional[str] = Query(None, description="Filtrar por fecha"),
    status: Optional[str] = Query(None, description="Filtrar por estado"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(ConsultationBooking)
    if date:
        query = query.filter(ConsultationBooking.booking_date == date)
    if status:
        query = query.filter(ConsultationBooking.status == status)
    
    return query.order_by(desc(ConsultationBooking.booking_date)).offset(offset).limit(limit).all()
