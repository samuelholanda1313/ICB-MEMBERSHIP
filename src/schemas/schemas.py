from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# Definicao dos schemas Bases, de Criacao e os utilizados pela API para as entidades de Unidade, Administrador e Membro.
class UnidadeBase(BaseModel):
    nome: str
    cidade: str
    cep: str
    endereco: str
    bairro: str
    estado: str

class AdministradorBase(BaseModel):
    tipo: str

class AdministradorCreate(AdministradorBase):
    senha: str
    membro_id: int
    unidade_id: int

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

class Unidade2(UnidadeBase):
    id: int

    class Config:
        from_attributes = True

class Membro(MembroBase):
    id: int
    unidade: Unidade2

    class Config:
        from_attributes = True

# Define o schema para caso de ler informacoes do administrador
class Administrador(AdministradorBase):
    id: int
    unidade: Unidade2
    membro: Membro

    class Config:
        from_attributes = True

class Unidade(UnidadeBase):
    id: int
    membros: List[Membro] = []
    administradores: List[Administrador] = []

    class Config:
        from_attributes = True
