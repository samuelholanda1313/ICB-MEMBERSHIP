from pydantic import BaseModel
from typing import List

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

    class Config:
        orm_mode = True
