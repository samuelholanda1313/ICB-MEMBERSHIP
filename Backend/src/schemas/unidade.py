from pydantic import BaseModel
from typing import List
from src.schemas.membro import Membro
from src.schemas.administrador import Administrador

# Criação da base para a entidade de Unidade. A criação utilizará este mesmo schema.
class UnidadeBase(BaseModel):
    nome: str
    cidade: str
    cep: str
    endereco: str
    bairro: str
    estado: str

class Unidade(UnidadeBase):
    id: int
    membros: List[Membro] = []
    administradores: List[Administrador] = []

    class Config:
        orm_mode = True
