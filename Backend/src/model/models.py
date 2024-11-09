from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base

# Criação do Model para a entidade de Administrador
class Administrador(Base):
    __tablename__ = "administradores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    tipo = Column(String(255), nullable=False)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    membros_id = Column(Integer, ForeignKey("membros.id"), nullable=False)
    unidade = relationship("Unidade", back_populates="administradores")
    membro = relationship("Membro", back_populates="administradores")
