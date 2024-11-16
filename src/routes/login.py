import os
from fastapi import APIRouter, HTTPException, Request
from src.database.database import get_supabase_client
from supabase import Client
import bcrypt
#import jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
from src.config.limiter_config import limiter
from jose import jwt


load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

router = APIRouter()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def check_senha(senha_fornecida: str, hash_armazenado: str) -> bool:
    return bcrypt.checkpw(senha_fornecida.encode('utf-8'), hash_armazenado.encode('utf-8'))

class LoginRequest(BaseModel):
    email: str
    senha: str

@router.post("/login")
@limiter.limit("30/minute")
async def login(login_request: LoginRequest, request: Request):
    email = login_request.email
    senha = login_request.senha

    supabase: Client = get_supabase_client()
    response_membro = supabase.table("membros").select("id").eq("email", email).execute()

    if not response_membro.data:
        raise HTTPException(status_code=404, detail="Membro não encontrado")

    response_administrador = supabase.table("administradores").select("*").eq("membro_id", response_membro.data[0]['id']).execute()

    if not response_administrador.data:
        raise HTTPException(status_code=404, detail="Administrador não encontrado")

    hash_armazenado = response_administrador.data[0]["senha"]

    if check_senha(senha, hash_armazenado):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": email, "tipo": response_administrador.data[0]["tipo"], "acesso_unidade_id": response_administrador.data[0]["acesso_unidade_id"]}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Senha incorreta")
