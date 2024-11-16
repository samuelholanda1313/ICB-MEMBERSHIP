from pydantic import BaseModel
from typing import Optional

class UpdateUnidade(BaseModel):
    nome: Optional[str] = None
    cidade: Optional[str] = None
    cep: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    estado: Optional[str] = None

class CreateUnidade(BaseModel):
    nome: str
    cidade: str
    cep: str
    endereco: str
    bairro: str
    estado: str