# backend/repository/catalog_repository.py
from sqlalchemy.orm import Session
from backend.database import Carrera, OpcionTitulacion, Requisito


def get_all_carreras(db: Session):
    return db.query(Carrera).all()


def get_carrera_by_id(db: Session, carrera_id: int):
    return db.query(Carrera).filter(Carrera.id == carrera_id).first()


def get_opciones_by_carrera(db: Session, carrera_id: int):
    return db.query(OpcionTitulacion).filter(OpcionTitulacion.carrera_id == carrera_id).all()


def get_opcion_by_id(db: Session, opcion_id: int):
    return db.query(OpcionTitulacion).filter(OpcionTitulacion.id == opcion_id).first()


def get_requisitos_by_opcion(db: Session, opcion_id: int):
    return (
        db.query(Requisito)
        .filter(Requisito.opcion_id == opcion_id)
        .order_by(Requisito.orden)
        .all()
    )


def get_requisito_by_id(db: Session, requisito_id: int):
    return db.query(Requisito).filter(Requisito.id == requisito_id).first()
