from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.app.config import settings
from backend.app.database import engine, Base, SessionLocal
from backend.app.seeds import seed_database
from backend.app.routers import (
    contact,
    consultations,
    case_evaluator,
    lawyers,
    practice_areas,
    admin,
    health,
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables and seed initial data
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield
    # Teardown logic if needed

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers under /api/v1
api_prefix = settings.API_PREFIX
app.include_router(health.router, prefix=api_prefix)
app.include_router(contact.router, prefix=api_prefix)
app.include_router(consultations.router, prefix=api_prefix)
app.include_router(case_evaluator.router, prefix=api_prefix)
app.include_router(lawyers.router, prefix=api_prefix)
app.include_router(practice_areas.router, prefix=api_prefix)
app.include_router(admin.router, prefix=api_prefix)

# Mount static asset folders
css_dir = BASE_DIR / "css"
if css_dir.exists():
    app.mount("/css", StaticFiles(directory=str(css_dir)), name="css")

js_dir = BASE_DIR / "js"
if js_dir.exists():
    app.mount("/js", StaticFiles(directory=str(js_dir)), name="js")

images_dir = BASE_DIR / "images"
if images_dir.exists():
    app.mount("/images", StaticFiles(directory=str(images_dir)), name="images")

staff_dir = BASE_DIR / "staff"
if staff_dir.exists():
    app.mount("/staff", StaticFiles(directory=str(staff_dir), html=True), name="staff")

# Specific HTML routes for friendly URLs
@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse(BASE_DIR / "index.html")

@app.get("/index.html", include_in_schema=False)
async def serve_index_html():
    return FileResponse(BASE_DIR / "index.html")

@app.get("/nosotros.html", include_in_schema=False)
@app.get("/nosotros", include_in_schema=False)
async def serve_nosotros():
    return FileResponse(BASE_DIR / "nosotros.html")

@app.get("/areas.html", include_in_schema=False)
@app.get("/areas", include_in_schema=False)
async def serve_areas():
    return FileResponse(BASE_DIR / "areas.html")

@app.get("/equipo.html", include_in_schema=False)
@app.get("/equipo", include_in_schema=False)
async def serve_equipo():
    return FileResponse(BASE_DIR / "equipo.html")

@app.get("/contacto.html", include_in_schema=False)
@app.get("/contacto", include_in_schema=False)
async def serve_contacto():
    return FileResponse(BASE_DIR / "contacto.html")

@app.get("/publicaciones.html", include_in_schema=False)
@app.get("/publicaciones", include_in_schema=False)
async def serve_publicaciones():
    return FileResponse(BASE_DIR / "publicaciones.html")

@app.get("/admin.html", include_in_schema=False)
@app.get("/admin", include_in_schema=False)
async def serve_admin():
    return FileResponse(BASE_DIR / "admin.html")

@app.get("/derecho-civil.html", include_in_schema=False)
@app.get("/derecho-civil", include_in_schema=False)
async def serve_civil():
    return FileResponse(BASE_DIR / "derecho-civil.html")

@app.get("/derecho-mercantil.html", include_in_schema=False)
@app.get("/derecho-mercantil", include_in_schema=False)
async def serve_mercantil():
    return FileResponse(BASE_DIR / "derecho-mercantil.html")

@app.get("/derecho-de-familia.html", include_in_schema=False)
@app.get("/derecho-de-familia", include_in_schema=False)
async def serve_familia():
    return FileResponse(BASE_DIR / "derecho-de-familia.html")

@app.get("/derecho-penal.html", include_in_schema=False)
@app.get("/derecho-penal", include_in_schema=False)
async def serve_penal():
    return FileResponse(BASE_DIR / "derecho-penal.html")

@app.get("/responsabilidad-civil-seguros.html", include_in_schema=False)
@app.get("/responsabilidad-civil-seguros", include_in_schema=False)
async def serve_seguros():
    return FileResponse(BASE_DIR / "responsabilidad-civil-seguros.html")
