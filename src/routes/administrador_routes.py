import json
from fastapi import APIRouter, HTTPException, Query, Body, Depends, Request
from src.database.database import get_supabase_client
from src.models.administrador_model import CreateAdministrador, UpdateAdministrador
from supabase import Client
from datetime import datetime
import bcrypt
from src.routes.auth import check_token
from src.config.limiter_config import limiter

router = APIRouter()

# Método GET para buscar administrador pelo ID
@router.get("/administrador/{id}")
@limiter.limit("100/minute")
async def get_administrador_id(request: Request, id: int, payload: dict = Depends(check_token)):

    tipo_administrador = payload.get("tipo")
    supabase: Client = get_supabase_client()
    response_administrador = supabase.table("administradores").select("id", "membro_id", "unidade_id", "acesso_unidade_id").eq("id", id).execute()

    if response_administrador.data:
        raise HTTPException(status_code=404, detail="Erro ao tentar recuperar o perfil do administrador")

    dados_administrador = response_administrador.data[0]

    if response_administrador.data:

        if tipo_administrador == "ADMGeral":
            response_membro = supabase.table("membros").select("id", "nome", "unidade_id", "email", "sexo", "posicao", "telefone").eq("id", dados_administrador['membro_id']).execute()
        elif tipo_administrador == "ADMUnidade":
            response_membro = supabase.table("membros").select("id", "nome", "unidade_id", "acesso_unidade_id", "sexo", "posicao", "telefone").eq("id", dados_administrador['membro_id']).in_("unidade_id", dados_administrador['acesso_unidade_id']).execute()
        elif tipo_administrador is None:
            raise HTTPException(status_code=404, detail="Tipo de administrador incorreto, buscar suporte para ajustar no banco de dados")

        if response_membro.data:
            dados_membro = response_membro.data[0]
            dados_administrador['membro'] = dados_membro

        elif not response_membro.data:
            raise HTTPException(status_code=404, detail="Erro ao tentar recuperar o perfil de membro do administrador")

        response_unidade = supabase.table("unidades").select("id", "nome").eq("id", dados_administrador['unidade_id']).execute()

        if response_unidade.data:
            dados_unidade = response_unidade.data[0]
            dados_administrador['unidade'] = dados_unidade

        elif not response_unidade.data:
            raise HTTPException(status_code=404, detail="Erro ao tentar recuperar o perfil da unidade do administrador")

        dados_administrador.pop('senha', None)
        dados_administrador.pop('membro_id', None)
        dados_administrador.pop('unidade_id', None)

        return {"data": dados_administrador}
    raise HTTPException(status_code=404, detail="Erro ao tentar buscar o perfil do administrador")

# Método GET para me retornar administradores por um intervalo de ID
@router.get("/administradores/intervalo")
@limiter.limit("100/minute")
async def get_administradores_intervalo(request: Request, inicio: int = Query(None, description="ID do início do intervalo"), fim: int = Query(None, description="ID do final do intervalo"), payload: dict = Depends(check_token)):

    supabase: Client = get_supabase_client()
    tipo_administrador = payload.get("tipo")
    acesso_unidades_id = json.dumps(payload.get("acesso_unidade_id"))
    acesso_unidades_id = "{" + acesso_unidades_id[1:-1] + "}"
    query = supabase.table("administradores").select("id", "unidade_id", "membro_id", "acesso_unidade_id").order("id").range(inicio, fim)

    if tipo_administrador == "ADMUnidade":
        query = query.filter("acesso_unidade_id", "ov", acesso_unidades_id)

    response_administrador = query.execute()

    if not response_administrador.data:
        raise HTTPException(status_code=404, detail="Erro ao tentar recuperar o perfil de membro do administrador")

    dados_administradores = []

    for dados_administrador in response_administrador.data:
        membro_id = dados_administrador['membro_id']
        unidade_id = dados_administrador['unidade_id']
        response_membro = supabase.table("membros").select("id", "unidade_id").eq("id", membro_id).execute()

        if response_membro.data:
            membro_data = response_membro.data[0]
            dados_administrador['membro'] = membro_data

        elif not response_membro.data:
            raise HTTPException(status_code=404, detail="Erro ao tentar recuperar o perfil de membro do administrador")

        response_unidade = supabase.table("unidades").select("id", "nome").eq("id", unidade_id).execute()

        if response_unidade.data:
            unidade_data = response_unidade.data[0]
            dados_administrador['unidade'] = unidade_data

        elif not response_unidade.data:
            raise HTTPException(status_code=404, detail="Erro ao tentar recuperar o perfil da unidade do administrador")

        dados_administrador.pop('senha', None)
        dados_administrador.pop('membro_id', None)
        dados_administrador.pop('unidade_id', None)
        dados_administradores.append(dados_administrador)

    return {"data": dados_administradores}

#Método GET para buscar administrador por filtros e intervalos
@router.get("/administradores/filtro")
@limiter.limit("100/minute")
async def get_administradores_filtro(request: Request, tipo: str, filtro: str = Query(None, description="ID do final do intervalo"), inicio: int = Query(None, description="ID do início do intervalo"), fim: int = Query(None, description="ID do final do intervalo"), payload: dict = Depends(check_token)):

    supabase: Client = get_supabase_client()
    tipo_administrador = payload.get("tipo")
    acesso_unidades_id = json.dumps(payload.get("acesso_unidade_id"))
    acesso_unidades_id = "{" + acesso_unidades_id[1:-1] + "}"
    query = supabase.table("administradores").select("*")

    if inicio is not None:
        query = query.gte("id", inicio)

    if fim is not None:
        query = query.lte("id", fim)

    if tipo_administrador == "ADMUnidade":
        query = query.filter("acesso_unidade_id", "ov", acesso_unidades_id)

    response_administrador = query.execute()

    if not response_administrador.data:
        raise HTTPException(status_code=404, detail="Erro ao tentar recuperar o perfil do administrador")

    dados_administradores = []

    for dados_administrador in response_administrador.data:

        if tipo == "membro":
            membro_id = dados_administrador['membro_id']
            response_membro = supabase.table("membros").select("*").eq("id", membro_id).execute()
            if not response_membro:
                raise HTTPException(status_code=404, detail="Erro ao tentar recuperar o perfil de membro do administrador ")

            if response_membro.data:
                dados_membro = response_membro.data[0]

                if filtro and filtro.lower() not in dados_membro['nome'].lower():
                    continue
                dados_administrador['membro'] = dados_membro

            dados_administrador.pop('senha', None)
            dados_administradores.append(dados_administrador)

        elif tipo == "unidade":
            unidade_id = dados_administrador['unidade_id']
            response_unidade = supabase.table("unidades").select("*").eq("id", unidade_id).execute()
            if not response_unidade:
                raise HTTPException(status_code=404, detail="Erro ao tentar recuperar o perfil da unidade do administrador ")

            if response_unidade.data:
                dados_unidade = response_unidade.data[0]

                if filtro and filtro.lower() not in dados_unidade['nome'].lower():
                    continue
                dados_administrador['unidade'] = dados_unidade

            dados_administrador.pop('senha', None)
            dados_administrador.pop('membro_id', None)
            dados_administrador.pop('unidade_id', None)
            dados_administradores.append(dados_administrador)

    return {"data": dados_administradores}

# Método DELETE para deletar um administrador de acordo com um ID
@router.delete("/administrador/{id}")
@limiter.limit("100/minute")
async def delete_administrador(request: Request, id: int, payload: dict = Depends(check_token)):
    supabase: Client = get_supabase_client()
    tipo_administrador = payload.get("tipo")
    acesso_unidades_id = json.dumps(payload.get("acesso_unidade_id"))
    acesso_unidades_id = "{" + acesso_unidades_id[1:-1] + "}"

    if tipo_administrador == "ADMGeral":
        response_administrador = supabase.table("administradores").select("id").eq("id", id).execute()
    else:
        response_administrador = supabase.table("administradores").select("id", "acesso_unidade_id").eq("id", id).filter("acesso_unidade_id", "ov", acesso_unidades_id).execute()

    if not response_administrador.data:
        raise HTTPException(status_code=404, detail="Administrador não encontrado")

    delete_response = supabase.table("administradores").delete().eq("id", id).execute()

    if not delete_response.data:
        raise HTTPException(status_code=500, detail="Erro ao deletar o administrador")

    return {"detail": f"Administrador {response_administrador.data[0]['id']} deletado com sucesso"}

# Método PUT para atualizar um administrador
@router.put("/administrador/{id}")
@limiter.limit("100/minute")
async def update_administrador(request: Request, id: int, dados: UpdateAdministrador = Body(...), payload: dict = Depends(check_token)):

    supabase: Client = get_supabase_client()
    tipo_administrador = payload.get("tipo")
    acesso_unidades_id = json.dumps(payload.get("acesso_unidade_id"))
    acesso_unidades_id = "{" + acesso_unidades_id[1:-1] + "}"

    if tipo_administrador == "ADMGeral":
        response_administrador = supabase.table("administradores").select("id").eq("id", id).execute()
    else:
        response_administrador = supabase.table("administradores").select("id", "acesso_unidade_id").eq("id", id).filter("acesso_unidade_id", "ov", acesso_unidades_id).execute()


    if not response_administrador.data:
        raise HTTPException(status_code=404, detail="Administrador não encontrado")

    dados = dados.dict(exclude_unset=True)
    dados['modified_at'] = datetime.now().isoformat()
    dados['senha'] = hash_senha(dados['senha'])
    update_response = supabase.table("administradores").update(dados).eq("id", id).execute()

    if not update_response.data:
        raise HTTPException(status_code=500, detail="Erro ao atualizar o administrador")

    return {"detail": update_response.data[0]}

# Método POST para criar um administrador
@router.post("/administrador")
@limiter.limit("100/minute")
async def create_administrador(request: Request, dados: CreateAdministrador = Body(...), payload: dict = Depends(check_token)):

    supabase: Client = get_supabase_client()
    dados = dados.dict()
    dados['created_at'] = datetime.now().isoformat()
    dados['modified_at'] = datetime.now().isoformat()
    dados['senha'] = hash_senha(dados['senha'])

    response_administrador = supabase.table("administradores").select('membro_id').eq("membro_id", dados["membro_id"]).execute()

    if response_administrador.data:
        raise HTTPException(status_code=409, detail="Já existe um membro cadastrado para este administrador")

    create_response = supabase.table("administradores").insert(dados).execute()

    if not create_response.data:
        raise HTTPException(status_code=500, detail="Erro ao criar o administrador")

    return {"detail": create_response.data[0]}

def hash_senha(senha: str) -> str:
    hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')