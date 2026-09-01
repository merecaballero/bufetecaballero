from sqlalchemy.orm import Session
from backend.app.models import Lawyer, PracticeArea, ContactMessage, ConsultationBooking
import datetime

def seed_database(db: Session):
    """Seed initial practice areas, lawyers and demonstration inquiries if tables are empty."""
    
    # 1. Seed Lawyers
    if db.query(Lawyer).count() == 0:
        lawyers_data = [
            Lawyer(
                slug="manuel-caballero-caballero",
                full_name="Manuel Caballero Caballero",
                role="Abogado Socio Fundador",
                colegiado_info="Colegiado nº 804 · ICALI · 54 años de ejercicio",
                experience_years=54,
                avatar_initials="MC",
                profile_url="staff/manuel-caballero-caballero.html",
                bio="Especialista en Derecho Civil, Sucesiones, Propiedad y Contratación. Más de 50 años defendiendo los intereses de familias y empresas en Alicante.",
                specialties="Derecho Civil, Herencias y Testamentos, Propiedad Horizontal, Arrendamientos",
                is_active=True
            ),
            Lawyer(
                slug="mariano-caballero-caballero",
                full_name="Mariano Caballero Caballero",
                role="Abogado Socio",
                colegiado_info="Colegiado ICA Alicante desde 1967",
                experience_years=57,
                avatar_initials="MC",
                profile_url="staff/mariano-caballero-caballero.html",
                bio="Amplia trayectoria en litigios mercantiles, societarios y derecho bancario. Referente jurídico en la provincia de Alicante.",
                specialties="Derecho Mercantil, Sociedades, Contratos Comerciales, Derecho Bancario",
                is_active=True
            ),
            Lawyer(
                slug="patricia-garcia-alcocel",
                full_name="Patricia García Alcocel",
                role="Abogada Especialista",
                colegiado_info="Colegiada nº 4319 · ICALI · desde julio de 1995",
                experience_years=29,
                avatar_initials="PG",
                profile_url="staff/patricia-garcia-alcocel.html",
                bio="Especialista en Derecho de Familia, Custodia, Divorcios, Medidas Paternofiliales y Mediación Familiar con trato cercano y personalizado.",
                specialties="Derecho de Familia, Divorcios, Custodia de Hijos, Liquidación de Gananciales",
                is_active=True
            ),
            Lawyer(
                slug="pedro-antonio-sillero-olmedo",
                full_name="Pedro Antonio Sillero Olmedo",
                role="Abogado Especialista",
                colegiado_info="Colegiado nº 3777 · ICALI · desde julio de 1993",
                experience_years=31,
                avatar_initials="PS",
                profile_url="staff/pedro-antonio-sillero-olmedo.html",
                bio="Experto en Responsabilidad Civil, Accidentes de Tráfico, Derecho Sanitario y Reclamaciones a Compañías Aseguradoras.",
                specialties="Responsabilidad Civil, Negligencias Médicas, Accidentes de Tráfico, Seguros",
                is_active=True
            ),
            Lawyer(
                slug="david-caballero-vidal",
                full_name="David Caballero Vidal",
                role="Abogado Penalista y Litigación",
                colegiado_info="Colegiado nº 5368 · ICALI · desde 1999",
                experience_years=25,
                avatar_initials="DC",
                profile_url="staff/david-caballero-vidal.html",
                bio="Especializado en Derecho Penal económico, delitos contra el patrimonio, defensa penal integral y derecho deportivo.",
                specialties="Derecho Penal, Delitos Económicos, Derecho Deportivo, Litigios",
                is_active=True
            ),
            Lawyer(
                slug="nuria-mas-marcos",
                full_name="Nuria Mas Marcos",
                role="Abogada Especialista",
                colegiado_info="Colegiada ICALI · más de 20 años de ejercicio",
                experience_years=22,
                avatar_initials="NM",
                profile_url="staff/nuria-mas-marcos.html",
                bio="Abogada especialista en diversas materias del derecho civil y administrativo, con dilatada experiencia en asesoramiento y litigios.",
                specialties="Derecho Civil, Administrativo, Reclamaciones Patrimoniales",
                is_active=True
            ),
        ]
        db.add_all(lawyers_data)
        db.commit()

    # 2. Seed Practice Areas
    if db.query(PracticeArea).count() == 0:
        areas_data = [
            PracticeArea(
                slug="derecho-civil",
                title="Derecho Civil",
                short_desc="Contratos, herencias, desahucios, servidumbres y propiedad horizontal con satisfacción integral.",
                full_desc="Asesoramiento experto en obligaciones, contratos de compraventa, permuta, reclamaciones de cantidad y derecho sucesorio.",
                page_url="derecho-civil.html",
                icon_name="file-text"
            ),
            PracticeArea(
                slug="responsabilidad-civil-seguros",
                title="Responsabilidad Civil y Seguros",
                short_desc="Reclamaciones en siniestros, accidentes de tráfico, negligencias y cobertura de pólizas aseguradoras.",
                full_desc="Defensa en procesos judiciales y extrajudiciales relativos a daños personales, materiales y responsabilidad profesional.",
                page_url="responsabilidad-civil-seguros.html",
                icon_name="shield"
            ),
            PracticeArea(
                slug="derecho-mercantil",
                title="Derecho Mercantil",
                short_desc="Constitución de sociedades, compliance, redacción de pactos de socios, acuerdos comerciales y actas.",
                full_desc="Acompañamiento integral a la empresa desde su constitución hasta operaciones corporativas complejas.",
                page_url="derecho-mercantil.html",
                icon_name="briefcase"
            ),
            PracticeArea(
                slug="derecho-de-familia",
                title="Derecho de Familia",
                short_desc="Separaciones, divorcios de mutuo acuerdo o contenciosos, custodia compartida y pensiones.",
                full_desc="Protegemos el bienestar de la unidad familiar y los menores con un enfoque empático, riguroso y conciliador.",
                page_url="derecho-de-familia.html",
                icon_name="users"
            ),
            PracticeArea(
                slug="derecho-penal",
                title="Derecho Penal",
                short_desc="Defensa letrada y acusación particular en todas las fases del proceso penal y tribunales.",
                full_desc="Asistencia inmediata a detenidos, procedimientos abreviados, delitos patrimoniales y juicios orales.",
                page_url="derecho-penal.html",
                icon_name="scale"
            )
        ]
        db.add_all(areas_data)
        db.commit()

    # 3. Seed Demonstration Inquiries and Bookings if empty
    if db.query(ContactMessage).count() == 0:
        demo_contacts = [
            ContactMessage(
                reference_code="BC-2026-8941",
                full_name="Carlos Martínez Navarro",
                email="carlos.martinez@ejemplo.es",
                phone="611 22 33 44",
                legal_area="Derecho Civil",
                subject="Revisión de testamento y adjudicación de herencia",
                message="Estimados letrados, quisiéramos consultar sobre la partición de una herencia con inmuebles situados en Alicante y un desacuerdo entre herederos.",
                urgency="normal",
                preferred_contact="email",
                status="en_estudio",
                admin_notes="Asignado a Manuel Caballero para estudio de la documentación notarial."
            ),
            ContactMessage(
                reference_code="BC-2026-3412",
                full_name="Helena Soler Gomis",
                email="helena.soler@ejemplo.es",
                phone="699 88 77 66",
                legal_area="Responsabilidad Civil y Seguros",
                subject="Indemnización por siniestro de tráfico con secuelas",
                message="Sufrí un accidente de tráfico en la A-70 hace un mes. La aseguradora contraria me ofrece una cuantía que no cubre el tratamiento rehabilitador.",
                urgency="urgente",
                preferred_contact="telefono",
                status="nuevo"
            ),
            ContactMessage(
                reference_code="BC-2026-5520",
                full_name="Inversiones Levantinas S.L.",
                email="administracion@inversioneslevantinas.es",
                phone="965 99 00 11",
                legal_area="Derecho Mercantil",
                subject="Modificación de estatutos sociales y pacto de socios",
                message="Necesitamos asesoramiento para redactar una cláusula de bloqueo y salida en nuestra sociedad limitada.",
                urgency="normal",
                preferred_contact="email",
                status="contactado",
                admin_notes="Contactado por teléfono el jueves. Se le solicitan las escrituras constitutivas."
            )
        ]
        db.add_all(demo_contacts)
        db.commit()

    if db.query(ConsultationBooking).count() == 0:
        demo_bookings = [
            ConsultationBooking(
                reference_code="CITA-7812",
                client_name="María José Ferrández",
                email="mj.ferrandez@ejemplo.es",
                phone="644 55 66 77",
                practice_area="Derecho de Familia",
                preferred_lawyer_name="Patricia García Alcocel",
                consultation_type="presencial",
                booking_date="2026-09-02",
                time_slot="11:00 - 12:00",
                brief_summary="Consulta sobre modificación de medidas de convenio regulador de custodia.",
                status="confirmada"
            ),
            ConsultationBooking(
                reference_code="CITA-9104",
                client_name="Antonio Beltrán Ruiz",
                email="antonio.beltran@ejemplo.es",
                phone="622 33 44 55",
                practice_area="Derecho Penal",
                preferred_lawyer_name="David Caballero Vidal",
                consultation_type="presencial",
                booking_date="2026-09-03",
                time_slot="17:00 - 18:00",
                brief_summary="Asesoramiento preventivo ante citación judicial en juzgado de instrucción.",
                status="confirmada"
            )
        ]
        db.add_all(demo_bookings)
        db.commit()
