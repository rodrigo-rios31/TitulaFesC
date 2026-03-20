# backend/repository/carpeta_repository.py
from sqlalchemy.orm import Session
from backend.database import Carpeta, DocumentoAlumno, HistorialCarpeta, EstadoDocumento
from datetime import datetime


def get_carpeta_activa(db: Session, alumno_id: int):
    """Obtiene la carpeta más reciente del alumno."""
    return (
        db.query(Carpeta)
        .filter(Carpeta.alumno_id == alumno_id)
        .order_by(Carpeta.created_at.desc())
        .first()
    )


def get_carpeta_by_id(db: Session, carpeta_id: int, alumno_id: int):
    return db.query(Carpeta).filter(
        Carpeta.id == carpeta_id, Carpeta.alumno_id == alumno_id
    ).first()


def create_carpeta(db: Session, alumno_id: int, opcion_id: int):
    carpeta = Carpeta(alumno_id=alumno_id, opcion_id=opcion_id)
    db.add(carpeta)
    db.commit()
    db.refresh(carpeta)
    # Registro en historial
    _add_historial(db, carpeta.id, "carpeta_creada", "Se inició la carpeta de titulación.")
    return carpeta


def inicializar_documentos(db: Session, carpeta_id: int, requisitos: list):
    """Crea un DocumentoAlumno (pendiente) por cada requisito."""
    for req in requisitos:
        doc = DocumentoAlumno(
            carpeta_id=carpeta_id,
            requisito_id=req.id,
            estado=EstadoDocumento.pendiente,
        )
        db.add(doc)
    db.commit()


def get_documentos(db: Session, carpeta_id: int):
    return db.query(DocumentoAlumno).filter(DocumentoAlumno.carpeta_id == carpeta_id).all()


def get_documento(db: Session, carpeta_id: int, requisito_id: int):
    return db.query(DocumentoAlumno).filter(
        DocumentoAlumno.carpeta_id == carpeta_id,
        DocumentoAlumno.requisito_id == requisito_id,
    ).first()


def update_documento(
    db: Session,
    documento: DocumentoAlumno,
    estado: str = None,
    archivo_nombre: str = None,
    archivo_path: str = None,
    notas: str = None,
):
    if estado:
        documento.estado = estado
    if archivo_nombre:
        documento.archivo_nombre = archivo_nombre
    if archivo_path:
        documento.archivo_path = archivo_path
    if notas is not None:
        documento.notas = notas
    documento.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(documento)
    return documento


def recalcular_lista_para_entrega(db: Session, carpeta: Carpeta) -> bool:
    """Verifica si todos los requisitos obligatorios están completos."""
    docs = get_documentos(db, carpeta.id)
    doc_map = {d.requisito_id: d for d in docs}
    for doc in docs:
        req = doc.requisito
        if req.obligatorio and doc.estado != EstadoDocumento.completo:
            carpeta.lista_para_entrega = False
            db.commit()
            return False
    carpeta.lista_para_entrega = True
    db.commit()
    return True


def get_historial(db: Session, carpeta_id: int):
    return (
        db.query(HistorialCarpeta)
        .filter(HistorialCarpeta.carpeta_id == carpeta_id)
        .order_by(HistorialCarpeta.timestamp.desc())
        .all()
    )


def _add_historial(db: Session, carpeta_id: int, accion: str, detalle: str = None):
    h = HistorialCarpeta(carpeta_id=carpeta_id, accion=accion, detalle=detalle)
    db.add(h)
    db.commit()
