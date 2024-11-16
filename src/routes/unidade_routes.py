from fastapi import APIRouter, HTTPException, Query, Body, Depends, Request
from src.database.database import get_supabase_client
from src.models.unidade_model import CreateUnidade, UpdateUnidade
from supabase import Client
from datetime import datetime
from src.routes.auth import check_token
import json
from src.config.limiter_config import limiter

router = APIRouter()

# Método GET para buscar unidade pelo ID
@router.get("/unidade/{id}")
@limiter.limit("100/minute")
async def get_unidade_id(request: Request, id: int, payload: dict = Depends(check_token)):

    supabase: Client = get_supabase_client()
    tipo_administrador = payload.get("tipo")
    acesso_unidades_id = json.dumps(payload.get("acesso_unidade_id"))
    acesso_unidades_id = "{" + acesso_unidades_id[1:-1] + "}"
    if tipo_administrador == "ADMUnidade":
        response_unidade = supabase.table("unidades").select("*").eq("id", id).in_("id", acesso_unidades_id).execute()
    else:
        response_unidade = supabase.table("unidades").select("*").eq("id", id).execute()
    dados_unidade = response_unidade.data[0]

    if not response_unidade.data:
        raise HTTPException(status_code=404, detail="Erro ao tentar buscar a unidade")

    return {"data": dados_unidade}

# Método GET para buscar unidade pelo ID e listar os membros e administradores
@router.get("/unidade-completa/{id}")
@limiter.limit("100/minute")
async def get_unidade_completa_id(request: Request, id: int, payload: dict = Depends(check_token)):

    supabase: Client = get_supabase_client()
    tipo_administrador = payload.get("tipo")
    acesso_unidades_id = json.dumps(payload.get("acesso_unidade_id"))
    acesso_unidades_id = "{" + acesso_unidades_id[1:-1] + "}"
    if tipo_administrador == "ADMUnidade":
        response_unidade = supabase.table("unidades").select("*").eq("id", id).in_("id", acesso_unidades_id).execute()
        response_membro = supabase.table("membros").select("nome").eq("unidade_id", id).in_("unidade_id", acesso_unidades_id).execute()
        response_administrador = supabase.table("administradores").select("membro_id").eq("unidade_id", id).in_("unidade_id", acesso_unidades_id).execute()
    else:
        response_unidade = supabase.table("unidades").select("*").eq("id", id).execute()
        response_membro = supabase.table("membros").select("nome").eq("unidade_id", id).execute()
        response_administrador = supabase.table("administradores").select("membro_id").eq("unidade_id", id).execute()

    lista_nomes_administrador = []
    for administrador in response_administrador.data:
        membro_id = administrador['membro_id']
        if tipo_administrador == "ADMUnidade":
            response_membros = supabase.table("membros").select("nome").eq("id", membro_id).in_("unidade_id", acesso_unidades_id).execute()
        else:
            response_membros = supabase.table("membros").select("nome").eq("id", membro_id).execute()

        if not response_membros.data:
            raise HTTPException(status_code=404, detail=f"Erro ao tentar acessar o membro {membro_id}")
        lista_nomes_administrador.append(response_membros.data[0]['nome'])

    lista_nomes_membro = [membro["nome"] for membro in response_membro.data]

    dados_unidade = response_unidade.data[0]
    #dados_unidade['membros'] = response_membro.data
    dados_unidade['membros'] = lista_nomes_membro
    dados_unidade['administradores'] = lista_nomes_administrador
    if not response_unidade.data:
        raise HTTPException(status_code=404, detail="Erro ao tentar buscar a unidade")

    return {"data": dados_unidade}

# Método GET que retorna unidades por um intervalo de ID
@router.get("/unidades/intervalo")
@limiter.limit("100/minute")
async def get_unidades_intervalo(request: Request, inicio: int = Query(None, description="ID do início do intervalo"), fim: int = Query(None, description="ID do final do intervalo"), payload: dict = Depends(check_token)):

    supabase: Client = get_supabase_client()
    tipo_administrador = payload.get("tipo")
    acesso_unidades_id = json.dumps(payload.get("acesso_unidade_id"))
    acesso_unidades_id = "{" + acesso_unidades_id[1:-1] + "}"
    query = supabase.table("unidades").select("*")

    if inicio is not None:
        query = query.gte("id", inicio)

    if fim is not None:
        query = query.lte("id", fim)

    if tipo_administrador == "ADMUnidade":
        query = query.in_("id", acesso_unidades_id)

    response_unidade = query.execute()

    if not response_unidade.data:
        raise HTTPException(status_code=404, detail="Erro ao tentar buscar a unidade")

    return {"data": response_unidade.data}

#Método GET para buscar unidades por filtros e intervalos
@router.get("/unidades/filtro")
@limiter.limit("100/minute")
async def get_unidades_filtro(request: Request, nome: str = Query(None), cidade: str = Query(None), estado: str = Query(None), inicio: int = Query(None, description="ID do início do intervalo"), fim: int = Query(None, description="ID do final do intervalo"), payload: dict = Depends(check_token)):

    supabase: Client = get_supabase_client()
    tipo_administrador = payload.get("tipo")
    acesso_unidades_id = json.dumps(payload.get("acesso_unidade_id"))
    acesso_unidades_id = "{" + acesso_unidades_id[1:-1] + "}"
    query = supabase.table("unidades").select("*")

    if inicio is not None:
        query = query.gte("id", inicio)

    if fim is not None:
        query = query.lte("id", fim)

    if nome is not None:
        query = query.ilike("nome", nome)

    if cidade is not None:
        query = query.ilike("cidade", cidade)

    if estado is not None:
        query = query.ilike("estado", estado)

    if tipo_administrador == "ADMUnidade":
        query = query.in_("id", acesso_unidades_id)

    response_unidade = query.execute()

    if not response_unidade.data:
        raise HTTPException(status_code=404, detail="Erro ao tentar buscar a unidade com os filtros selecionados")

    return {"data": response_unidade.data}

# Método DELETE para deletar uma unidade de acordo com um ID
@router.delete("/unidade/{id}")
@limiter.limit("100/minute")
async def delete_unidade(request: Request, id: int, payload: dict = Depends(check_token)):
    supabase: Client = get_supabase_client()
    tipo_administrador = payload.get("tipo")
    acesso_unidades_id = json.dumps(payload.get("acesso_unidade_id"))
    acesso_unidades_id = "{" + acesso_unidades_id[1:-1] + "}"
    if tipo_administrador == "ADMUnidade":
        response_unidade = supabase.table("unidades").select("*").eq("id", id).in_("id", acesso_unidades_id).execute()
    else:
        response_unidade = supabase.table("unidades").select("*").eq("id", id).execute()

    if not response_unidade.data:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")

    delete_response = supabase.table("unidades").delete().eq("id", id).execute()

    if not delete_response.data:
        raise HTTPException(status_code=500, detail="Erro ao deletar a unidade")

    return {"detail": f"Unidade {response_unidade.data[0]['id']} deletada com sucesso"}

# Método PUT para atualizar uma unidade
@router.put("/unidade/{id}")
@limiter.limit("100/minute")
async def update_unidade(request: Request, id: int, dados: UpdateUnidade = Body(...), payload: dict = Depends(check_token)):

    supabase: Client = get_supabase_client()
    tipo_administrador = payload.get("tipo")
    acesso_unidades_id = json.dumps(payload.get("acesso_unidade_id"))
    acesso_unidades_id = "{" + acesso_unidades_id[1:-1] + "}"
    if tipo_administrador == "ADMUnidade":
        response_unidade = supabase.table("unidades").select("*").eq("id", id).in_("id", acesso_unidades_id).execute()
    else:
        response_unidade = supabase.table("unidades").select("*").eq("id", id).execute()

    if not response_unidade.data:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")

    dados = dados.dict(exclude_unset=True)
    dados['modified_at'] = datetime.now().isoformat()
    update_response = supabase.table("unidades").update(dados).eq("id", id).execute()

    if not update_response.data:
        raise HTTPException(status_code=500, detail="Erro ao atualizar a unidade")

    return {"detail": update_response.data[0]}

# Método POST para criar uma unidade
@router.post("/unidade")
@limiter.limit("100/minute")
async def create_unidade(request: Request, dados: CreateUnidade = Body(...), payload: dict = Depends(check_token)):

    supabase: Client = get_supabase_client()
    tipo_administrador = payload.get("tipo")
    acesso_unidades_id = json.dumps(payload.get("acesso_unidade_id"))
    acesso_unidades_id = "{" + acesso_unidades_id[1:-1] + "}"
    dados = dados.dict()
    dados['created_at'] = datetime.now().isoformat()
    dados['modified_at'] = datetime.now().isoformat()
    response_unidade = supabase.table("unidades").select("*").eq("nome", dados["nome"]).execute()
    if response_unidade.data:
        raise HTTPException(status_code=409, detail="Já existe uma unidade com este nome")

    create_response = supabase.table("unidades").insert(dados).execute()

    if not create_response.data:
        raise HTTPException(status_code=500, detail="Erro ao criar a unidade")

    return {"detail": create_response.data[0]}
