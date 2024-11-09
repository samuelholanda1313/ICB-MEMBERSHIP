from pydantic import BaseModel
from typing import Optional
from src.schemas.unidade import Unidade

# Define um schema base para a entidade Administrador
class AdministradorBase(BaseModel):
    membro_id: int
    tipo: str
    unidade_id: int

# Define o schema para caso de criar novo administrador, herdando atributos do AdministradorBase
class AdministradorCreate(AdministradorBase):
    senha: str

# Define o schema para caso de ler informações do administrador
class Administrador(AdministradorBase):
    id: int
    unidade: Unidade

    class Config:
        orm_mode = True
