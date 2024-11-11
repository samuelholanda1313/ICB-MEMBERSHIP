from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session, joinedload
from src.model import models
from src.schemas.schemas import Administrador, AdministradorCreate
from src.database.database import get_db

router = APIRouter()

# Método GET para obter um administrador pelo ID
@router.get("/{id}", response_model=Administrador)
def get_administrador(id: int, db: Session = Depends(get_db)):
    administrador = db.query(models.Administrador).filter(models.Administrador.id == id).first()
    if administrador is None:
        raise HTTPException(status_code=404, detail="Administrador não encontrado")
    return administrador

# Método GET para retornar todos os administradores com paginacao e filtros de nome do membro ou unidade.
@router.get("/", response_model=list[Administrador])
def get_administradores(skip: int = Query(0, ge=0), limit: int = Query(10, gt=0), membro_nome: str = None, unidade_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Administrador).options(joinedload(models.Administrador.membro))
    if membro_nome is not None:
        query = query.join(models.Membro).filter(models.Membro.nome.ilike(f"{membro_nome}%"))
    if unidade_id is not None:
        query = query.filter(models.Administrador.unidade_id == unidade_id)
    administradores = query.offset(skip).limit(limit).all()
    if not administradores:
        raise HTTPException(status_code=404, detail="Nenhum administrador encontrado")
    return administradores

# Método POST para criacao de um novo administrador
@router.post("/", response_model=Administrador)
def create_administrador(administrador: AdministradorCreate, db: Session = Depends(get_db)):
    novo_administrador = models.Administrador(**administrador.dict())
    db.add(novo_administrador)
    db.commit()
    db.refresh(novo_administrador)
    return novo_administrador

# Método PUT um administrador conforme o ID.
@router.put("/{id}", response_model=Administrador)
def update_administrador(id: int, administrador: AdministradorCreate, db: Session = Depends(get_db)):
    busca_administrador = db.query(models.Administrador).filter(models.Administrador.id == id).first()
    if busca_administrador is None:
        raise HTTPException(status_code=404, detail="Administrador não encontrado")
    for key, value in administrador.dict().items():
        setattr(busca_administrador, key, value)
    db.commit()
    db.refresh(busca_administrador)
    return busca_administrador

# Método DELETE para deletar um administrador conforme o ID.
@router.delete("/{id}")
def delete_administrador(id: int, db: Session = Depends(get_db)):
    busca_administrador = db.query(models.Administrador).filter(models.Administrador.id == id).first()
    if busca_administrador is None:
        raise HTTPException(status_code=404, detail="Administrador não encontrado")
    db.delete(busca_administrador)
    db.commit()
    return {"detail": "Administrador deletado com sucesso"}
