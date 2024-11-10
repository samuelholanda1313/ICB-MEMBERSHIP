from pydantic import BaseModel
from src.schemas.unidade import Unidade
from src.schemas.membro import Membro

# Define um schema base para a entidade Administrador
class AdministradorBase(BaseModel):
    tipo: str

# Define o schema para caso de criar novo administrador, herdando atributos do AdministradorBase
class AdministradorCreate(AdministradorBase):
    senha: str
    membro_id: int
    unidade_id: int

# Define o schema para caso de ler informações do administrador
class Administrador(AdministradorBase):
    id: int
    unidade: Unidade
    membro: Membro

    class Config:
        orm_mode = True
