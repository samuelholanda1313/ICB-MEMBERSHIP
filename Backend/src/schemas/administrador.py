from pydantic import BaseModel
from typing import List, Optional
from src.schemas.unidade import Unidade

class AdministradorBase(BaseModel):
    nome: str
    email: str
    tipo: str

class AdministradorCreate(AdministradorBase):
    senha: str

class Administrador(AdministradorBase):
    id: int
    unidades: List[Unidade] = []

    class Config:
        orm_mode = True
