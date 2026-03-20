# backend/database.py
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
import enum

DATABASE_URL = "sqlite:///./titulacion.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class EstadoDocumento(str, enum.Enum):
    pendiente = "pendiente"
    completo = "completo"
    rechazado = "rechazado"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    matricula = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    carpetas = relationship("Carpeta", back_populates="alumno")


class Carrera(Base):
    __tablename__ = "carreras"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    clave = Column(String, unique=True, nullable=False)
    opciones = relationship("OpcionTitulacion", back_populates="carrera")


class OpcionTitulacion(Base):
    __tablename__ = "opciones_titulacion"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    carrera_id = Column(Integer, ForeignKey("carreras.id"))
    carrera = relationship("Carrera", back_populates="opciones")
    requisitos = relationship("Requisito", back_populates="opcion")


class Requisito(Base):
    __tablename__ = "requisitos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    instrucciones = Column(Text, nullable=True)   # Guía específica para el alumno
    obligatorio = Column(Boolean, default=True)
    permite_archivo = Column(Boolean, default=True)
    opcion_id = Column(Integer, ForeignKey("opciones_titulacion.id"))
    opcion = relationship("OpcionTitulacion", back_populates="requisitos")
    orden = Column(Integer, default=0)


class Carpeta(Base):
    __tablename__ = "carpetas"
    id = Column(Integer, primary_key=True, index=True)
    alumno_id = Column(Integer, ForeignKey("users.id"))
    opcion_id = Column(Integer, ForeignKey("opciones_titulacion.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    lista_para_entrega = Column(Boolean, default=False)
    alumno = relationship("User", back_populates="carpetas")
    opcion = relationship("OpcionTitulacion")
    documentos = relationship("DocumentoAlumno", back_populates="carpeta", cascade="all, delete-orphan")
    historial = relationship("HistorialCarpeta", back_populates="carpeta", cascade="all, delete-orphan")


class DocumentoAlumno(Base):
    __tablename__ = "documentos_alumno"
    id = Column(Integer, primary_key=True, index=True)
    carpeta_id = Column(Integer, ForeignKey("carpetas.id"))
    requisito_id = Column(Integer, ForeignKey("requisitos.id"))
    estado = Column(String, default=EstadoDocumento.pendiente)
    archivo_nombre = Column(String, nullable=True)
    archivo_path = Column(String, nullable=True)
    notas = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    carpeta = relationship("Carpeta", back_populates="documentos")
    requisito = relationship("Requisito")


class HistorialCarpeta(Base):
    __tablename__ = "historial_carpeta"
    id = Column(Integer, primary_key=True, index=True)
    carpeta_id = Column(Integer, ForeignKey("carpetas.id"))
    accion = Column(String, nullable=False)
    detalle = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    carpeta = relationship("Carpeta", back_populates="historial")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
