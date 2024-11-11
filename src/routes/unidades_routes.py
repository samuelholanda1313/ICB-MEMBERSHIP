from src.schemas.schemas import UnidadeBase, Unidade
from src.database.database import get_db
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session, joinedload
from src.model import models

router = APIRouter()