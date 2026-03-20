# backend/routers/carpeta_router.py
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.database import get_db
from backend.utils.security import get_current_user
from backend.services import carpeta_service

router = APIRouter(prefix="/api/carpeta", tags=["Carpeta"])


class IniciarCarpetaRequest(BaseModel):
    opcion_id: int


class MarcarDocumentoRequest(BaseModel):
    requisito_id: int
    estado: str  # pendiente | completo
    notas: Optional[str] = None


@router.post("/iniciar")
def iniciar_carpeta(
    body: IniciarCarpetaRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return carpeta_service.iniciar_carpeta(db, user.id, body.opcion_id)


@router.get("/resumen")
def get_resumen(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return carpeta_service.get_resumen(db, user.id)


@router.patch("/documento/marcar")
def marcar_documento(
    body: MarcarDocumentoRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return carpeta_service.marcar_documento(
        db, user.id, body.requisito_id, body.estado, body.notas
    )


@router.post("/documento/subir")
async def subir_archivo(
    requisito_id: int = Form(...),
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return await carpeta_service.subir_archivo(db, user.id, requisito_id, archivo)


@router.get("/historial")
def get_historial(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return carpeta_service.get_historial(db, user.id)
