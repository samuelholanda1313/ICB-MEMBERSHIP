from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.administrador_routes import router as administrador_router
from src.routes.membro_routes import router as membro_router
from src.routes.unidade_routes import router as unidade_router
from src.routes.login import router as login_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(administrador_router, tags=["Administradores"])
app.include_router(membro_router, tags=["Membros"])
app.include_router(unidade_router, tags=["Unidades"])
app.include_router(login_router, tags=["Login"])
