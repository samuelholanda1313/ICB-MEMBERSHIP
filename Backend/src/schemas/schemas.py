from pydantic import BaseModel
from typing import List

class Administrador(BaseModel):
    nome: str
    email: str
    senha: str
    tipo: str
    unidade_id: int

class Membro(BaseModel):
    nome: str
    email: str
    data_nascimento: str
    sexo: str
    unidade_id: int

class Unidade(BaseModel):
    nome: str
    cidade: str
