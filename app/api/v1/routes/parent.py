from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.parent import ParentCreate, ParentOut
from app.services import parent as parent_service

router = APIRouter(prefix="/parents", tags=["Parents"])

# 🔹 Criar novo responsável
@router.post("/", response_model=ParentOut)
def create_parent(payload: ParentCreate, db: Session = Depends(get_db)):
    return parent_service.register_parent(db, payload)

# 🔹 Login simples
@router.post("/login", response_model=ParentOut)
def login_parent(email: str, senha: str, db: Session = Depends(get_db)):
    return parent_service.login_parent(db, email, senha)

# 🔹 Listar todos os pais
@router.get("/", response_model=list[ParentOut])
def list_parents(db: Session = Depends(get_db)):
    return parent_service.list_parents(db)
