# backend/routers/auth_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from backend.database import get_db
from backend.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["Auth"])


class RegisterRequest(BaseModel):
    nombre: str
    matricula: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    matricula: str
    password: str


@router.post("/register")
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register_user(db, body.nombre, body.matricula, body.email, body.password)


@router.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login_user(db, body.matricula, body.password)
