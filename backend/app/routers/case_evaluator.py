import random
import datetime
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import CaseEvaluation
from backend.app.schemas import CaseEvaluationRequest, CaseEvaluationResponse

router = APIRouter(prefix="/case-evaluator", tags=["Evaluador de Casos / Triage"])

def evaluate_case_triage(data: CaseEvaluationRequest):
    desc_lower = data.description.lower()
    score = 40
    urgency = "media"
    
    # Check deadline urgency
    if data.has_deadline:
        score += 35
        urgency = "urgente"

    # Analyze critical legal keywords
    urgent_keywords = ["citación", "juzgado", "notificación", "embargo", "detenido", "denuncia", "querella", "desahucio", "plazo", "días hábiles", "accidente", "lesiones"]
    if any(kw in desc_lower for kw in urgent_keywords):
        score += 20
        urgency = "urgente"

    # Determine recommended lawyer based on area and keywords
    area = data.area_type.lower()
    if "penal" in area or "delito" in desc_lower or "policía" in desc_lower:
        lawyer = "David Caballero Vidal"
        action = "Revisión inmediata del atestado o notificación penal. Le recomendamos no realizar declaraciones sin asistencia letrada previa y agendar consulta prioritaria."
    elif "familia" in area or "divorcio" in desc_lower or "custodia" in desc_lower or "pensión" in desc_lower:
        lawyer = "Patricia García Alcocel"
        action = "Estudio del régimen patrimonial y situación de los menores. Se aconseja preparar padrón, libro de familia y movimientos económicos previos a la primera reunión."
    elif "seguro" in area or "responsabilidad" in area or "accidente" in desc_lower or "médic" in desc_lower or "secuela" in desc_lower:
        lawyer = "Pedro Antonio Sillero Olmedo"
        action = "Auditoría de póliza y peritaje de daños. Fundamental conservar informes de urgencias y no aceptar indemnizaciones a la baja sin baremación legal independiente."
    elif "mercantil" in area or "sociedad" in desc_lower or "empresa" in desc_lower or "socio" in desc_lower or "contrato" in desc_lower:
        lawyer = "Mariano Caballero Caballero"
        action = "Examen de estatutos sociales, actas de juntas y cláusulas contractuales. Asesoramiento estratégico mercantil para mitigar riesgos patrimoniales."
    else:
        lawyer = "Manuel Caballero Caballero"
        action = "Análisis documental de títulos de propiedad, contratos o escrituras de herencia. Determinación de la vía judicial o extrajudicial más eficaz para sus intereses."

    score = min(score, 99)
    return urgency, score, lawyer, action

@router.post(
    "",
    response_model=CaseEvaluationResponse,
    status_code=status.HTTP_200_OK,
    summary="Evaluar caso y obtener orientación jurídica preliminar",
    description="Algoritmo de triage legal que analiza la tipología, plazos y urgencia del conflicto y recomienda al especialista del despacho."
)
@router.post(
    "/evaluate",
    response_model=CaseEvaluationResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False
)
def evaluate_case(
    payload: CaseEvaluationRequest,
    db: Session = Depends(get_db)
):
    urgency, score, lawyer, action = evaluate_case_triage(payload)
    ref_code = f"EVAL-{random.randint(1000, 9999)}"

    evaluation_record = CaseEvaluation(
        reference_code=ref_code,
        area_type=payload.area_type,
        has_deadline=payload.has_deadline,
        matter_scope=payload.matter_scope,
        description=payload.description,
        estimated_urgency=urgency,
        triage_score=score,
        recommended_lawyer=lawyer,
        recommended_action=action,
        client_email=payload.client_email
    )

    db.add(evaluation_record)
    db.commit()
    db.refresh(evaluation_record)

    return CaseEvaluationResponse(
        reference_code=ref_code,
        area_type=payload.area_type,
        estimated_urgency=urgency,
        triage_score=score,
        recommended_lawyer=lawyer,
        recommended_action=action,
        created_at=evaluation_record.created_at
    )
