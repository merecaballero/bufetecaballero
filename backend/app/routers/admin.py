import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from backend.app.database import get_db
from backend.app.models import ContactMessage, ConsultationBooking, CaseEvaluation
from backend.app.schemas import ContactResponse, ConsultationResponse, StatusUpdate, DashboardStats

router = APIRouter(prefix="/admin", tags=["Administración del Bufete"])

@router.get(
    "/dashboard",
    response_model=DashboardStats,
    summary="Métricas y estadísticas del despacho en tiempo real"
)
@router.get(
    "/stats",
    response_model=DashboardStats,
    include_in_schema=False
)
def get_dashboard_metrics(db: Session = Depends(get_db)):
    total_inquiries = db.query(ContactMessage).count()
    total_consultations = db.query(ConsultationBooking).count()
    new_inquiries = db.query(ContactMessage).filter(ContactMessage.status == "nuevo").count()
    pending_consultations = db.query(ConsultationBooking).filter(ConsultationBooking.status == "confirmada").count()

    # Area distribution
    area_counts = db.query(ContactMessage.legal_area, func.count(ContactMessage.id)).group_by(ContactMessage.legal_area).all()
    area_distribution = {area: count for area, count in area_counts}

    # Urgency distribution
    urgency_counts = db.query(ContactMessage.urgency, func.count(ContactMessage.id)).group_by(ContactMessage.urgency).all()
    urgency_distribution = {urg: count for urg, count in urgency_counts}

    return DashboardStats(
        total_inquiries=total_inquiries,
        total_consultations=total_consultations,
        new_inquiries=new_inquiries,
        pending_consultations=pending_consultations,
        area_distribution=area_distribution,
        urgency_distribution=urgency_distribution,
        server_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

@router.get(
    "/inquiries",
    response_model=List[ContactResponse],
    summary="Listado completo de expedientes de contacto para abogados"
)
def get_admin_inquiries(
    status: Optional[str] = Query(None),
    urgency: Optional[str] = Query(None),
    area: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(ContactMessage)
    if status:
        query = query.filter(ContactMessage.status == status)
    if urgency:
        query = query.filter(ContactMessage.urgency == urgency)
    if area:
        query = query.filter(ContactMessage.legal_area.ilike(f"%{area}%"))
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            (ContactMessage.full_name.ilike(pattern)) |
            (ContactMessage.email.ilike(pattern)) |
            (ContactMessage.reference_code.ilike(pattern)) |
            (ContactMessage.subject.ilike(pattern))
        )
    return query.order_by(desc(ContactMessage.created_at)).all()

@router.patch(
    "/inquiries/{inquiry_id}",
    response_model=ContactResponse,
    summary="Actualizar estado o notas de un expediente"
)
def update_inquiry_status(
    inquiry_id: int,
    payload: StatusUpdate,
    db: Session = Depends(get_db)
):
    inquiry = db.query(ContactMessage).filter(ContactMessage.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Consulta con ID {inquiry_id} no encontrada"
        )
    
    inquiry.status = payload.status
    if payload.admin_notes is not None:
        inquiry.admin_notes = payload.admin_notes
    
    db.commit()
    db.refresh(inquiry)
    return inquiry

@router.delete(
    "/inquiries/{inquiry_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un expediente de contacto"
)
def delete_inquiry(
    inquiry_id: int,
    db: Session = Depends(get_db)
):
    inquiry = db.query(ContactMessage).filter(ContactMessage.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Consulta con ID {inquiry_id} no encontrada"
        )
    db.delete(inquiry)
    db.commit()
    return None

@router.patch(
    "/consultations/{consultation_id}",
    response_model=ConsultationResponse,
    summary="Actualizar estado de una cita jurídica"
)
def update_consultation_status(
    consultation_id: int,
    payload: StatusUpdate,
    db: Session = Depends(get_db)
):
    booking = db.query(ConsultationBooking).filter(ConsultationBooking.id == consultation_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cita con ID {consultation_id} no encontrada"
        )
    
    booking.status = payload.status
    db.commit()
    db.refresh(booking)
    return booking
