import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator
import re

EMAIL_REGEX = re.compile(r"^[\w\.\+\-]+@[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,}$")

def validate_email_str(v: str) -> str:
    if not v:
        raise ValueError("El correo electrónico es obligatorio.")
    v = v.strip().lower()
    if not EMAIL_REGEX.match(v):
        raise ValueError("Formato de correo electrónico inválido (ejemplo: contacto@ejemplo.es).")
    return v

# --- CONTACT SCHEMAS ---
class ContactCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120, description="Nombre y apellidos del solicitante")
    email: str = Field(..., description="Correo electrónico de contacto")
    phone: Optional[str] = Field(None, max_length=30, description="Teléfono de contacto")
    legal_area: str = Field("General", max_length=80, description="Área legal de consulta")
    subject: str = Field(..., min_length=3, max_length=200, description="Asunto resumido")
    message: str = Field(..., min_length=10, max_length=5000, description="Descripción detallada de la consulta")
    urgency: Optional[str] = Field("normal", description="Nivel de urgencia: baja, normal, urgente")
    preferred_contact: Optional[str] = Field("email", description="Preferencia de contacto: email, telefono, whatsapp")

    @field_validator("email")
    @classmethod
    def check_email(cls, v: str) -> str:
        return validate_email_str(v)

class ContactResponse(BaseModel):
    id: int
    reference_code: str
    full_name: str
    email: str
    phone: Optional[str]
    legal_area: str
    subject: str
    message: str
    urgency: str
    preferred_contact: str
    status: str
    admin_notes: Optional[str] = None
    created_at: datetime.datetime

    class Config:
        from_attributes = True

# --- CONSULTATION SCHEMAS ---
class ConsultationCreate(BaseModel):
    client_name: str = Field(..., min_length=2, max_length=120, description="Nombre completo del cliente")
    email: str = Field(..., description="Correo electrónico de contacto")
    phone: str = Field(..., min_length=6, max_length=30, description="Número de teléfono de contacto")
    practice_area: str = Field(..., max_length=80, description="Especialidad o materia")
    preferred_lawyer_name: Optional[str] = Field("Cualquiera disponible", max_length=120)
    consultation_type: str = Field("presencial", description="Tipo: presencial, videoconferencia, telefonica")
    booking_date: str = Field(..., description="Fecha deseada en formato YYYY-MM-DD")
    time_slot: str = Field(..., description="Franja horaria: ej. 10:00 - 11:00")
    brief_summary: Optional[str] = Field(None, max_length=2000, description="Breve descripción del caso")

    @field_validator("email")
    @classmethod
    def check_email(cls, v: str) -> str:
        return validate_email_str(v)

class ConsultationResponse(BaseModel):
    id: int
    reference_code: str
    client_name: str
    email: str
    phone: str
    practice_area: str
    preferred_lawyer_name: Optional[str]
    consultation_type: str
    booking_date: str
    time_slot: str
    brief_summary: Optional[str]
    status: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

# --- CASE EVALUATION / TRIAGE SCHEMAS ---
class CaseEvaluationRequest(BaseModel):
    area_type: str = Field(..., description="Área temática (Civil, Penal, Familia, Mercantil, Seguros)")
    has_deadline: bool = Field(False, description="¿Tiene un plazo judicial o administrativo abierto?")
    matter_scope: str = Field("particular", description="Ámbito: particular, empresa, herencia, reclamacion, judicial")
    description: str = Field(..., min_length=15, description="Breve resumen del problema")
    client_email: Optional[str] = None

    @field_validator("client_email")
    @classmethod
    def check_email(cls, v: Optional[str]) -> Optional[str]:
        if v:
            return validate_email_str(v)
        return v

class CaseEvaluationResponse(BaseModel):
    reference_code: str
    area_type: str
    estimated_urgency: str
    triage_score: int
    recommended_lawyer: str
    recommended_action: str
    created_at: datetime.datetime

# --- LAWYERS SCHEMAS ---
class LawyerOut(BaseModel):
    id: int
    slug: str
    full_name: str
    role: str
    colegiado_info: str
    experience_years: int
    avatar_initials: str
    profile_url: str
    bio: str
    specialties: str
    is_active: bool

    class Config:
        from_attributes = True

# --- PRACTICE AREAS SCHEMAS ---
class PracticeAreaOut(BaseModel):
    id: int
    slug: str
    title: str
    short_desc: str
    full_desc: Optional[str]
    page_url: str
    icon_name: str

    class Config:
        from_attributes = True

# --- ADMIN & MANAGEMENT SCHEMAS ---
class StatusUpdate(BaseModel):
    status: str = Field(..., description="Nuevo estado")
    admin_notes: Optional[str] = Field(None, description="Notas internas del letrado")

class DashboardStats(BaseModel):
    total_inquiries: int
    total_consultations: int
    new_inquiries: int
    pending_consultations: int
    area_distribution: Dict[str, int]
    urgency_distribution: Dict[str, int]
    server_time: str
