from fastapi import APIRouter, HTTPException, Query, Body, Depends, Request
from src.database.database import get_supabase_client
from src.models.membro_model import CreateMembro, UpdateMembro
from supabase import Client
from datetime import datetime
from src.routes.auth import check_token
import json
from src.config.limiter_config import limiter

router = APIRouter()

# Método GET para buscar um membro pelo ID
@router.get("/membro/{id}")
@limiter.limit("100/minute")
async def get_membro_id(request: Request, id: int, payload: dict = Depends(check_token)):

    supabase: Client = get_supabase_client()
    tipo_administrador = payload.get("tipo")
    acesso_unidades_id = json.dumps(payload.get("acesso_unidade_id"))
    acesso_unidades_id = "{" + acesso_unidades_id[1:-1] + "}"

    if tipo_administrador == "ADMUnidade":
        response_membro = supabase.table("membros").select("*").eq("id", id).in_("unidade_id", acesso_unidades_id).execute()
    else:
        response_membro = supabase.table("membros").select("*").eq("id", id).execute()
    dados_membro = response_membro.data[0]
    response_unidade = supabase.table("unidades").select("*").eq("id", dados_membro['unidade_id']).execute()
    dados_membro['unidade'] = response_unidade.data[0]
    dados_membro.pop('unidade_id')

    if not response_membro.data:
        raise HTTPException(status_code=404, detail="Erro ao tentar buscar a unidade")

    return {"data": dados_membro}

# Método GET que retorna membros por um intervalo de ID
@router.get("/membros/intervalo")
@limiter.limit("100/minute")
async def get_unidades_intervalo(request: Request, inicio: int = Query(None, description="ID do início do intervalo"), fim: int = Query(None, description="ID do final do intervalo"), payload: dict = Depends(check_token)):

    supabase: Client = get_supabase_client()
    tipo_administrador = payload.get("tipo")
    acesso_unidades_id = json.dumps(payload.get("acesso_unidade_id"))
    acesso_unidades_id = "{" + acesso_unidades_id[1:-1] + "}"
    query = supabase.table("membros").select("*")

    if inicio is not None:
        query = query.gte("id", inicio)

    if fim is not None:
        query = query.lte("id", fim)

    if tipo_administrador == "ADMUnidade":
        query = query.in_("unidade_id", acesso_unidades_id)

    response_membro = query.execute()

    dados_membros = []

    for dados_membro in response_membro.data:
        unidade_id = dados_membro['unidade_id']
        if tipo_administrador == "ADMUnidade":
            response_unidade = supabase.table("unidades").select("*").eq("id", unidade_id).in_("id", acesso_unidades_id).execute()
        else:
            response_unidade = supabase.table("unidades").select("*").eq("id", unidade_id).execute()
        dados_membro['unidade'] = response_unidade.data[0]
        dados_membro.pop('unidade_id')
        dados_membros.append(dados_membro)

    if not response_membro.data:
        raise HTTPException(status_code=404, detail="Erro ao tentar buscar o membro")

    return {"data": dados_membros}

#Método GET para buscar membros por filtros e intervalos
@router.get("/membros/filtro")
@limiter.limit("100/minute")
async def get_membros_filtro(request: Request, nome: str = Query(None), unidade: str = Query(None), inicio: int = Query(None, description="ID do início do intervalo"), fim: int = Query(None, description="ID do final do intervalo"), payload: dict = Depends(check_token)):

    supabase: Client = get_supabase_client()
    tipo_administrador = payload.get("tipo")
    acesso_unidades_id = json.dumps(payload.get("acesso_unidade_id"))
    acesso_unidades_id = "{" + acesso_unidades_id[1:-1] + "}"
    query = supabase.table("membros").select("*")

    if inicio is not None:
        query = query.gte("id", inicio)

    if fim is not None:
        query = query.lte("id", fim)

    if nome is not None:
        query = query.ilike("nome", nome)

    if tipo_administrador == "ADMUnidade":
        query = query.in_("unidade_id", acesso_unidades_id)

    response_membros = query.execute()

    if not response_membros.data:
        raise HTTPException(status_code=404, detail="Nenhum membro encontrado com os filtros selecionados")

    dados_membros = []

    for dados_membro in response_membros.data:
        unidade_id = dados_membro['unidade_id']

        if tipo_administrador == "ADMUnidade":
            response_unidade = supabase.table("unidades").select("*").eq("id", unidade_id).in_("id", acesso_unidades_id).execute()
        else:
            response_unidade = supabase.table("unidades").select("*").eq("id", unidade_id).execute()

        if response_unidade.data:
            unidade_nome = response_unidade.data[0]['nome']
            dados_membro['unidade'] = unidade_nome
            dados_membro.pop('unidade_id')
        else:
            dados_membro['unidade'] = None

        dados_membros.append(dados_membro)

        if unidade is not None:
            dados_membros = [membro for membro in dados_membros if unidade.lower() in membro['unidade'].lower()]

    return {"data": dados_membros}

# Método DELETE para deletar um membro de acordo com um ID
@router.delete("/membro/{id}")
@limiter.limit("100/minute")
async def delete_membro(request: Request, id: int, payload: dict = Depends(check_token)):
    supabase: Client = get_supabase_client()
    tipo_administrador = payload.get("tipo")
    acesso_unidades_id = json.dumps(payload.get("acesso_unidade_id"))
    acesso_unidades_id = "{" + acesso_unidades_id[1:-1] + "}"
    if tipo_administrador == "ADMUnidade":
        response_membro = supabase.table("membros").select("*").eq("id", id).in_("unidade_id", acesso_unidades_id).execute()
    else:
        response_membro = supabase.table("membros").select("*").eq("id", id).execute()

    if not response_membro.data:
        raise HTTPException(status_code=404, detail="Membro não encontrado")

    delete_response = supabase.table("membros").delete().eq("id", id).execute()

    if not delete_response.data:
        raise HTTPException(status_code=500, detail="Erro ao deletar o membro")

    return {"detail": f"Unidade {response_membro.data[0]['id']} deletado com sucesso"}

# Método PUT para atualizar um membro
@router.put("/membro/{id}")
@limiter.limit("100/minute")
async def update_membro(request: Request, id: int, dados: UpdateMembro = Body(...), payload: dict = Depends(check_token)):

    supabase: Client = get_supabase_client()
    tipo_administrador = payload.get("tipo")
    acesso_unidades_id = json.dumps(payload.get("acesso_unidade_id"))
    acesso_unidades_id = "{" + acesso_unidades_id[1:-1] + "}"
    if tipo_administrador == "ADMUnidade":
        response_membro = supabase.table("membros").select("*").eq("id", id).in_("unidade_id", acesso_unidades_id).execute()
    else:
        response_membro = supabase.table("membros").select("*").eq("id", id).execute()

    if not response_membro.data:
        raise HTTPException(status_code=404, detail="Membro não encontrado")

    dados = dados.dict(exclude_unset=True)
    dados['modified_at'] = datetime.now().isoformat()
    update_response = supabase.table("membros").update(dados).eq("id", id).execute()

    if not update_response.data:
        raise HTTPException(status_code=500, detail="Erro ao atualizar o membro")

    return {"detail": update_response.data[0]}

# Método POST para criar um membro
@router.post("/membro")
@limiter.limit("100/minute")
async def create_unidade(request: Request, dados: CreateMembro = Body(...), payload: dict = Depends(check_token)):

    supabase: Client = get_supabase_client()
    dados = dados.dict()
    dados['created_at'] = datetime.now().isoformat()
    dados['modified_at'] = datetime.now().isoformat()
    response_membro = supabase.table("membros").select("email").eq("email", dados["email"]).execute()
    if response_membro.data:
        raise HTTPException(status_code=409, detail="Já existe um membro com este email")

    create_response = supabase.table("membros").insert(dados).execute()

    if not create_response.data:
        raise HTTPException(status_code=500, detail="Erro ao criar o membro")

    return {"detail": create_response.data[0]}

@router.post("/membro_formulario")
@limiter.limit("5/minute")
async def create_unidade(request: Request, dados: CreateMembro = Body(...)):

    supabase: Client = get_supabase_client()
    dados = dados.dict()
    dados['created_at'] = datetime.now().isoformat()
    dados['modified_at'] = datetime.now().isoformat()
    response_membro = supabase.table("membros").select("email").eq("email", dados["email"]).execute()
    if response_membro.data:
        raise HTTPException(status_code=409, detail="Já existe um membro com este email")

    create_response = supabase.table("membros").insert(dados).execute()

    if not create_response.data:
        raise HTTPException(status_code=500, detail="Erro ao criar o membro")

    return {"detail": create_response.data[0]}
