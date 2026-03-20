# backend/services/carpeta_service.py
import os, shutil
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from backend.repository import carpeta_repository as repo
from backend.repository import catalog_repository as cat_repo
from backend.database import EstadoDocumento
from backend.utils.config import settings
from backend.repository.carpeta_repository import _add_historial


def iniciar_carpeta(db: Session, alumno_id: int, opcion_id: int):
    """Crea una nueva carpeta e inicializa todos sus documentos."""
    opcion = cat_repo.get_opcion_by_id(db, opcion_id)
    if not opcion:
        raise HTTPException(status_code=404, detail="Opción de titulación no encontrada.")

    # Si ya existe una carpeta activa para la misma opción, la retornamos
    carpeta = repo.get_carpeta_activa(db, alumno_id)
    if carpeta and carpeta.opcion_id == opcion_id:
        return _build_resumen(db, carpeta)

    carpeta = repo.create_carpeta(db, alumno_id, opcion_id)
    requisitos = cat_repo.get_requisitos_by_opcion(db, opcion_id)
    repo.inicializar_documentos(db, carpeta.id, requisitos)
    return _build_resumen(db, carpeta)


def get_resumen(db: Session, alumno_id: int):
    carpeta = repo.get_carpeta_activa(db, alumno_id)
    if not carpeta:
        raise HTTPException(status_code=404, detail="No tienes una carpeta activa. Selecciona tu carrera y opción.")
    return _build_resumen(db, carpeta)


def marcar_documento(db: Session, alumno_id: int, requisito_id: int, estado: str, notas: str = None):
    carpeta = _get_carpeta_or_404(db, alumno_id)
    doc = repo.get_documento(db, carpeta.id, requisito_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado en tu carpeta.")

    if estado not in [e.value for e in EstadoDocumento]:
        raise HTTPException(status_code=400, detail="Estado inválido.")

    repo.update_documento(db, doc, estado=estado, notas=notas)
    _add_historial(
        db, carpeta.id, f"documento_{estado}",
        f"Requisito '{doc.requisito.nombre}' marcado como {estado}."
    )
    listo = repo.recalcular_lista_para_entrega(db, carpeta)
    return _build_resumen(db, carpeta)


async def subir_archivo(db: Session, alumno_id: int, requisito_id: int, archivo: UploadFile):
    carpeta = _get_carpeta_or_404(db, alumno_id)
    doc = repo.get_documento(db, carpeta.id, requisito_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado.")
    if not doc.requisito.permite_archivo:
        raise HTTPException(status_code=400, detail="Este requisito no admite archivos.")

    # Validar extensión permitida
    ext = os.path.splitext(archivo.filename)[1].lower()
    allowed = {".pdf", ".jpg", ".jpeg", ".png", ".docx", ".zip"}
    if ext not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no permitido. Usa: {', '.join(allowed)}"
        )

    # Guardar archivo
    upload_path = os.path.join(settings.UPLOAD_DIR, str(alumno_id), str(carpeta.id))
    os.makedirs(upload_path, exist_ok=True)
    filename = f"req_{requisito_id}{ext}"
    file_path = os.path.join(upload_path, filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(archivo.file, f)

    repo.update_documento(
        db, doc,
        estado=EstadoDocumento.completo,
        archivo_nombre=archivo.filename,
        archivo_path=file_path,
    )
    _add_historial(
        db, carpeta.id, "archivo_subido",
        f"Archivo '{archivo.filename}' subido para '{doc.requisito.nombre}'."
    )
    repo.recalcular_lista_para_entrega(db, carpeta)
    return _build_resumen(db, carpeta)


def get_historial(db: Session, alumno_id: int):
    carpeta = _get_carpeta_or_404(db, alumno_id)
    historial = repo.get_historial(db, carpeta.id)
    return [
        {"accion": h.accion, "detalle": h.detalle, "timestamp": h.timestamp.isoformat()}
        for h in historial
    ]


# ── helpers ──────────────────────────────────────────────────────────────────

def _get_carpeta_or_404(db, alumno_id):
    carpeta = repo.get_carpeta_activa(db, alumno_id)
    if not carpeta:
        raise HTTPException(status_code=404, detail="No tienes una carpeta activa.")
    return carpeta


def _build_resumen(db: Session, carpeta):
    docs = repo.get_documentos(db, carpeta.id)
    total = len(docs)
    completos = sum(1 for d in docs if d.estado == EstadoDocumento.completo)
    porcentaje = round((completos / total) * 100) if total else 0

    items = []
    for doc in sorted(docs, key=lambda d: d.requisito.orden):
        req = doc.requisito
        items.append({
            "requisito_id": req.id,
            "nombre": req.nombre,
            "descripcion": req.descripcion,
            "instrucciones": req.instrucciones,
            "obligatorio": req.obligatorio,
            "permite_archivo": req.permite_archivo,
            "estado": doc.estado,
            "archivo_nombre": doc.archivo_nombre,
            "notas": doc.notas,
            "updated_at": doc.updated_at.isoformat() if doc.updated_at else None,
        })

    return {
        "carpeta_id": carpeta.id,
        "opcion": carpeta.opcion.nombre,
        "carrera": carpeta.opcion.carrera.nombre,
        "lista_para_entrega": carpeta.lista_para_entrega,
        "progreso": {"completos": completos, "total": total, "porcentaje": porcentaje},
        "documentos": items,
        "created_at": carpeta.created_at.isoformat(),
        "updated_at": carpeta.updated_at.isoformat() if carpeta.updated_at else None,
    }
