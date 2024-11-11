from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from database.database import Base
from database.database import engine
from routes.administradores_routes import router as administradores_router
#from src.routes.membros_routes import router as membros_router
#from src.routes.unidades_routes import router as unidades_router
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(administradores_router, prefix="/administradores", tags=["Administradores"])
#app.include_router(membros_router, prefix="/membros", tags=["Membros"])
#app.include_router(unidades_router, prefix="/unidades", tags=["Unidades"])