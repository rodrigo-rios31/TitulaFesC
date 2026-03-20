# backend/routers/catalog_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.repository import catalog_repository as repo
from backend.utils.security import get_current_user

router = APIRouter(prefix="/api/catalogo", tags=["Catálogo"])


@router.get("/carreras")
def listar_carreras(db: Session = Depends(get_db), _=Depends(get_current_user)):
    carreras = repo.get_all_carreras(db)
    return [{"id": c.id, "nombre": c.nombre, "clave": c.clave} for c in carreras]


@router.get("/carreras/{carrera_id}/opciones")
def listar_opciones(carrera_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    opciones = repo.get_opciones_by_carrera(db, carrera_id)
    return [{"id": o.id, "nombre": o.nombre} for o in opciones]


@router.get("/opciones/{opcion_id}/requisitos")
def listar_requisitos(opcion_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    requisitos = repo.get_requisitos_by_opcion(db, opcion_id)
    return [
        {
            "id": r.id,
            "nombre": r.nombre,
            "descripcion": r.descripcion,
            "instrucciones": r.instrucciones,
            "obligatorio": r.obligatorio,
            "permite_archivo": r.permite_archivo,
        }
        for r in requisitos
    ]
