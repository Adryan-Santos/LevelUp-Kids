from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.kid import KidCreate, KidOut
from app.repositories import kid as kid_repo

router = APIRouter(prefix="/v1/kid", tags=["kid"])

# ✅ Cadastrar novo herói (criança)
@router.post("/", response_model=KidOut, status_code=status.HTTP_201_CREATED)
def create_kid(payload: KidCreate, db: Session = Depends(get_db)):
    return kid_repo.create_kid(db, payload)

# ✅ Buscar todos os heróis de um pai
@router.get("/", response_model=list[KidOut])
def get_kids_by_parent(parent_id: int = Query(None), db: Session = Depends(get_db)):
    if parent_id:
        return kid_repo.get_kids_by_parent(db, parent_id)
    return kid_repo.get_all_kids(db)

# ✅ Buscar um herói específico
@router.get("/{kid_id}", response_model=KidOut)
def get_kid(kid_id: int, db: Session = Depends(get_db)):
    kid = kid_repo.get_kid_by_id(db, kid_id)
    if not kid:
        raise HTTPException(status_code=404, detail="Herói não encontrado.")
    return kid

# ✅ Excluir um herói
@router.delete("/{kid_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_kid(kid_id: int, db: Session = Depends(get_db)):
    success = kid_repo.delete_kid(db, kid_id)
    if not success:
        raise HTTPException(status_code=404, detail="Herói não encontrado.")
