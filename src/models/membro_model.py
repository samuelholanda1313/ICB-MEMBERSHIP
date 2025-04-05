from pydantic import BaseModel
from typing import Optional
from datetime import date

class UpdateMembro(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    data_nascimento: Optional[date] = None
    sexo: Optional[str] = None
    unidade_id: Optional[int] = None
    posicao: Optional[str] = None
    cep: Optional[str] = None
    estado: Optional[str] = None
    cidade: Optional[str] = None
    numero: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    estado_civil: Optional[str] = None
    telefone: Optional[str] = None
    profissao: Optional[str] = None
    batismo: Optional[str] = None
    data_batismo: Optional[date] = None

class CreateMembro(BaseModel):
    nome: str
    email: str
    data_nascimento: date
    sexo: str
    unidade_id: str
    posicao: str
    cep: str
    estado: str
    cidade: str
    numero: str
    endereco: str
    bairro: str
    estado_civil: str
    telefone: str
    profissao: Optional[str] = None
    batismo: Optional[str] = None
    data_batismo: Optional[date] = None