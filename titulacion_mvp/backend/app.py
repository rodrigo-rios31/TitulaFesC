# backend/app.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.database import create_tables, SessionLocal
from backend.utils.seed import run_seed
from backend.routers import auth_router, catalog_router, carpeta_router
from backend.utils.config import settings

app = FastAPI(
    title="Validador de Carpeta de Titulación",
    description="API para gestionar el proceso de titulación de alumnos.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router.router)
app.include_router(catalog_router.router)
app.include_router(carpeta_router.router)

# Archivos estáticos del frontend
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def root():
    index = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index):
        return FileResponse(index)
    return {"message": "API Titulación OK. Docs en /docs"}


@app.on_event("startup")
def startup():
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    create_tables()
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()
    print("🚀 Servidor iniciado correctamente.")
