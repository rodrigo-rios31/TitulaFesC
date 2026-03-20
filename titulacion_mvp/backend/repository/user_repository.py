# backend/repository/user_repository.py
from sqlalchemy.orm import Session
from backend.database import User
from backend.utils.security import hash_password


def get_user_by_matricula(db: Session, matricula: str):
    return db.query(User).filter(User.matricula == matricula).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, nombre: str, matricula: str, email: str, password: str):
    user = User(
        nombre=nombre,
        matricula=matricula,
        email=email,
        hashed_password=hash_password(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
