# backend/services/auth_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.repository.user_repository import (
    get_user_by_matricula, get_user_by_email, create_user
)
from backend.utils.security import verify_password, create_access_token


def register_user(db: Session, nombre: str, matricula: str, email: str, password: str):
    if get_user_by_matricula(db, matricula):
        raise HTTPException(status_code=400, detail="La matrícula ya está registrada.")
    if get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="El email ya está registrado.")
    user = create_user(db, nombre, matricula, email, password)
    token = create_access_token({"sub": user.matricula})
    return {"access_token": token, "token_type": "bearer", "user": _user_out(user)}


def login_user(db: Session, matricula: str, password: str):
    user = get_user_by_matricula(db, matricula)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Matrícula o contraseña incorrectos.",
        )
    token = create_access_token({"sub": user.matricula})
    return {"access_token": token, "token_type": "bearer", "user": _user_out(user)}


def _user_out(user):
    return {
        "id": user.id,
        "nombre": user.nombre,
        "matricula": user.matricula,
        "email": user.email,
    }
