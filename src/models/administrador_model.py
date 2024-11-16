from pydantic import BaseModel
from typing import Optional, List

class UpdateAdministrador(BaseModel):
    membro_id: Optional[int] = None
    unidade_id: Optional[int] = None
    tipo: Optional[str] = None
    senha: Optional[str] = None
    acesso_unidade_id: Optional[List[int]] = None

class CreateAdministrador(BaseModel):
    membro_id: int
    unidade_id: int
    tipo: str
    senha: str
    acesso_unidade_id: Optional[List[int]] = None
