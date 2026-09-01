import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from backend.app.database import Base

def current_time():
    return datetime.datetime.now(datetime.timezone.utc)

class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    reference_code = Column(String(32), unique=True, index=True, nullable=False)
    full_name = Column(String(120), nullable=False)
    email = Column(String(120), index=True, nullable=False)
    phone = Column(String(30), nullable=True)
    legal_area = Column(String(80), nullable=False, default="General")
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    urgency = Column(String(30), default="normal") # baja, normal, urgente
    preferred_contact = Column(String(30), default="email") # email, telefono, whatsapp
    status = Column(String(30), default="nuevo", index=True) # nuevo, en_estudio, contactado, cerrado
    admin_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=current_time)
    updated_at = Column(DateTime, default=current_time, onupdate=current_time)

class ConsultationBooking(Base):
    __tablename__ = "consultation_bookings"

    id = Column(Integer, primary_key=True, index=True)
    reference_code = Column(String(32), unique=True, index=True, nullable=False)
    client_name = Column(String(120), nullable=False)
    email = Column(String(120), index=True, nullable=False)
    phone = Column(String(30), nullable=False)
    practice_area = Column(String(80), nullable=False)
    preferred_lawyer_name = Column(String(120), nullable=True, default="Cualquiera disponible")
    consultation_type = Column(String(40), default="presencial") # presencial, videoconferencia, telefonica
    booking_date = Column(String(20), nullable=False) # YYYY-MM-DD
    time_slot = Column(String(30), nullable=False) # e.g. "10:00 - 11:00"
    brief_summary = Column(Text, nullable=True)
    status = Column(String(30), default="confirmada", index=True) # confirmada, en_espera, realizada, cancelada
    created_at = Column(DateTime, default=current_time)

class CaseEvaluation(Base):
    __tablename__ = "case_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    reference_code = Column(String(32), unique=True, index=True, nullable=False)
    area_type = Column(String(80), nullable=False)
    has_deadline = Column(Boolean, default=False)
    matter_scope = Column(String(100), nullable=False) # particular, empresa, herencia, reclamacion, etc.
    description = Column(Text, nullable=False)
    estimated_urgency = Column(String(30), default="media")
    triage_score = Column(Integer, default=50)
    recommended_lawyer = Column(String(120), nullable=True)
    recommended_action = Column(Text, nullable=True)
    client_email = Column(String(120), nullable=True)
    created_at = Column(DateTime, default=current_time)

class Lawyer(Base):
    __tablename__ = "lawyers"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(80), unique=True, index=True, nullable=False)
    full_name = Column(String(120), nullable=False)
    role = Column(String(80), default="Abogado")
    colegiado_info = Column(String(150), nullable=False)
    experience_years = Column(Integer, default=20)
    avatar_initials = Column(String(10), default="BC")
    profile_url = Column(String(200), nullable=False)
    bio = Column(Text, nullable=False)
    specialties = Column(String(300), nullable=False)
    is_active = Column(Boolean, default=True)

class PracticeArea(Base):
    __tablename__ = "practice_areas"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(80), unique=True, index=True, nullable=False)
    title = Column(String(120), nullable=False)
    short_desc = Column(Text, nullable=False)
    full_desc = Column(Text, nullable=True)
    page_url = Column(String(200), nullable=False)
    icon_name = Column(String(50), default="balance")
