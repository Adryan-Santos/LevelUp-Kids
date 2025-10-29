from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.parent import Parent
from app.schemas.parent import ParentCreate, ParentOut, ParentLogin
from app.repositories import parent as parent_repo

router = APIRouter(prefix="/v1/parent", tags=["parent"])

# ✅ Registro de novo responsável
@router.post("/", response_model=ParentOut, status_code=status.HTTP_201_CREATED)
def create_parent(payload: ParentCreate, db: Session = Depends(get_db)):
    existing = db.query(Parent).filter(Parent.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    return parent_repo.create_parent(db, payload)

# ✅ Login simples (sem JWT ainda)
@router.post("/login", response_model=ParentOut)
def login_parent(payload: ParentLogin, db: Session = Depends(get_db)):
    parent = db.query(Parent).filter(Parent.email == payload.email).first()
    if not parent or parent.senha != payload.senha:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")
    return parent

# ✅ Buscar todos os responsáveis
@router.get("/", response_model=list[ParentOut])
def list_parents(db: Session = Depends(get_db)):
    return parent_repo.get_all_parents(db)

# ✅ Buscar responsável por ID
@router.get("/{parent_id}", response_model=ParentOut)
def get_parent(parent_id: int, db: Session = Depends(get_db)):
    parent = parent_repo.get_parent_by_id(db, parent_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Responsável não encontrado.")
    return parent
