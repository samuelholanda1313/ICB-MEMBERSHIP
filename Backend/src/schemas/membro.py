from pydantic import BaseModel
from typing import Optional
from datetime import date
from src.schemas.unidade import UnidadeBase

class MembroBase(BaseModel):
    nome: str
    email: str
    data_nascimento: date
    sexo: str
    unidade_id: int
    posicao: str
    endereco: str
    bairro: str
    estado_civil: str
    telefone: str
    profissao: str
    batismo: str
    data_batismo: Optional[date] = None

class MembroCreate(MembroBase):
    senha: str

class Membro(MembroBase):
    id: int
    unidade: UnidadeBase

    class Config:
        orm_mode = True
