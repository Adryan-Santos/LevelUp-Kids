from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.hash import bcrypt

from app.repositories import parent as parent_repo
from app.schemas.parent import ParentCreate


#Registrar novo responsável (com senha criptografada)
def register_parent(db: Session, data: ParentCreate):
    data.senha = bcrypt.hash(data.senha)
    return parent_repo.create_parent(db, data)


#Login básico (sem JWT, apenas validação simples)
def login_parent(db: Session, email: str, senha: str):
    parent = parent_repo.get_parent_by_email(db, email)
    if not parent or not bcrypt.verify(senha, parent.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
    return parent


#Listar todos os pais cadastrados
def list_parents(db: Session):
    return parent_repo.get_all_parents(db)
