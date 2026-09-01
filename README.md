# 🏛️ Bufete Caballero — Plataforma Web Full-Stack

Aplicación web profesional para **Bufete Caballero** (despacho de abogados en Alicante fundado en 1947). Construida con un backend moderno en **FastAPI**, servidor ASGI **Uvicorn**, persistencia **SQLAlchemy / SQLite**, y un frontend enriquecido con asistente de evaluación de casos (*legal triage*), reserva de citas en tiempo real, formulario de contacto asíncrono y panel administrativo para letrados.

---

## 🚀 Puesta en Marcha Rápida

### 1. Iniciar el servidor con un solo comando:
```bash
python run.py
```
*O alternativamente con Uvicorn directamente:*
```bash
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Acceso a las interfaces:
- 🌐 **Sitio Web Público:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- ⚖️ **Panel Administrativo del Despacho:** [http://127.0.0.1:8000/admin.html](http://127.0.0.1:8000/admin.html)
- 📖 **Documentación Swagger / OpenAPI interactiva:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- 📜 **Documentación ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- 🩺 **Health Check API:** [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)

---

## 📁 Estructura del Proyecto

```
bufete-caballero-web/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Inicialización del paquete
│   │   ├── main.py              # Aplicación FastAPI, lifespan, CORS, montaje de estáticos y rutas
│   │   ├── config.py            # Configuración de entorno y variables
│   │   ├── database.py          # Conexión SQLite con SQLAlchemy (Engine, SessionLocal)
│   │   ├── models.py            # Modelos ORM: ContactMessage, ConsultationBooking, CaseEvaluation, Lawyer, PracticeArea
│   │   ├── schemas.py           # Validación estricta Pydantic V2
│   │   ├── seeds.py             # Semillero inicial de datos (6 letrados, áreas, demostración)
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── contact.py       # POST /api/v1/contact, GET /api/v1/contact
│   │       ├── consultations.py # POST /api/v1/consultations, GET /api/v1/consultations/available-slots
│   │       ├── case_evaluator.py# POST /api/v1/case-evaluator (Triage legal inteligente)
│   │       ├── lawyers.py       # GET /api/v1/lawyers, GET /api/v1/lawyers/{slug}
│   │       ├── practice_areas.py# GET /api/v1/practice-areas
│   │       ├── admin.py         # Métricas, gestión de expedientes y cambio de estados
│   │       └── health.py        # Diagnóstico y estado del sistema
│   ├── requirements.txt         # Dependencias Python
│   ├── run.py                   # Lanzador backend con detección inteligente de puertos
│   └── main.py                  # Entrypoint ASGI
├── images/                      # Logotipo oficial en múltiples formatos (PNG, SVG, White, Navy, Gold)
│   ├── logo-caballero-navy.png
│   ├── logo-caballero-navy.svg
│   ├── logo-caballero-white.png
│   ├── logo-caballero-white.svg
│   └── logo-caballero-gold.png
├── index.html                   # Página principal institucional
├── nosotros.html                # Historia y trayectoria desde 1947
├── areas.html                   # Áreas de práctica jurídica y especialidades
├── equipo.html                  # Equipo de 6 letrados con reserva de cita individual
├── contacto.html                # Formulario oficial asíncrono con validación y sede en Alicante
├── publicaciones.html           # El Rincón Jurídico / Artículos del despacho
├── admin.html                   # Dashboard de gestión interna de expedientes para letrados
├── derecho-civil.html           # Especialidad Civil
├── derecho-de-familia.html      # Especialidad Familia
├── derecho-mercantil.html       # Especialidad Mercantil
├── derecho-penal.html           # Especialidad Penal
├── responsabilidad-civil-seguros.html # Especialidad Seguros y Responsabilidad Civil
├── staff/                       # Perfiles individuales de los 6 abogados
│   ├── david-caballero-vidal.html
│   ├── manuel-caballero-caballero.html
│   ├── mariano-caballero-caballero.html
│   ├── nuria-mas-marcos.html
│   ├── patricia-garcia-alcocel.html
│   └── pedro-antonio-sillero-olmedo.html
├── css/
│   └── style.css                # Sistema de diseño sobrio (Navy, White, Soft Gold) y componentes UI
├── js/
│   ├── main.js                  # Menú móvil, FAQs nativas, modales, scroll animado y formularios
│   ├── api.js                   # Cliente API centralizado
│   └── admin.js                 # Lógica interactiva del panel de administración
├── run.py                       # Lanzador principal
├── requirements.txt             # Dependencias del proyecto
├── .gitignore                   # Exclusiones de control de versiones
└── README.md                    # Documentación técnica
```

---

## ⚖️ Endpoints de la API REST (`/api/v1`)

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Estado del servidor, tiempo de actividad y conexión a base de datos |
| `POST` | `/api/v1/contact` | Envío de formulario de contacto con generación de código `BC-YYYY-XXXX` |
| `GET` | `/api/v1/contact` | Listado de consultas recibidas con filtros por estado y área |
| `GET` | `/api/v1/consultations/available-slots` | Franjas horarias disponibles para una fecha y letrado |
| `POST` | `/api/v1/consultations` | Reserva de consulta legal (presencial, videollamada o telefónica) |
| `POST` | `/api/v1/case-evaluator` | Algoritmo de orientación jurídica, urgencia y letrado asignado |
| `GET` | `/api/v1/lawyers` | Directorio de abogados y letrados del despacho |
| `GET` | `/api/v1/practice-areas` | Áreas de especialidad jurídica |
| `GET` | `/api/v1/admin/dashboard` | Métricas y estadísticas en tiempo real para el despacho |
| `GET` | `/api/v1/admin/inquiries` | Expedientes para revisión de letrados con filtros avanzados |
| `PATCH` | `/api/v1/admin/inquiries/{id}` | Actualización de estado (*nuevo*, *en estudio*, *contactado*, *cerrado*) y notas |
| `PATCH` | `/api/v1/admin/consultations/{id}` | Actualización de estado de citas (*confirmada*, *realizada*, *cancelada*) |
| `DELETE` | `/api/v1/admin/inquiries/{id}` | Eliminación de expediente de prueba |

---

## ✨ Características Principales

1. **Backend ASGI con FastAPI & Uvicorn**: Alto rendimiento, tipado estricto con Pydantic V2 y documentación Swagger OpenAPI autogenerada.
2. **Evaluador Jurídico Preliminar (Triage)**: Los usuarios pueden indicar su materia, si tienen un plazo judicial en curso y obtener un dictamen orientativo con asignación de letrado especialista.
3. **Reserva Inteligente de Citas**: Verificación en tiempo real de disponibilidad por día y franja horaria.
4. **Panel de Gestión para el Bufete (`admin.html`)**: Permite a los letrados visualizar nuevas solicitudes, modificar estados, añadir notas internas confidenciales y revisar la agenda.
5. **Estética Clásica y Premium**: Paleta basada en pergamino (`#F1E9D8`), tinta bosque (`#172922`), bronce y tipografías *Fraunces* y *Work Sans*.
