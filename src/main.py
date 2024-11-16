from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.administrador_routes import router as administrador_router
from src.routes.membro_routes import router as membro_router
from src.routes.unidade_routes import router as unidade_router
from src.routes.login import router as login_router
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

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
