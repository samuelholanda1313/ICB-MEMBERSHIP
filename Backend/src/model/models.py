from sqlalchemy import Column, Integer, String, ForeignKey, Date, CheckConstraint
from sqlalchemy.orm import relationship
from src.database.database import Base

# Criação do Model para a entidade de Administrador
class Administrador(Base):
    __tablename__ = "administradores"
    id = Column(Integer, primary_key=True, index=True)
    senha = Column(String(255), nullable=False)
    tipo = Column(String(255), nullable=False)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    membros_id = Column(Integer, ForeignKey("membros.id"), nullable=False)
    unidade = relationship("Unidade", back_populates="Administrador")
    membro = relationship("Membro", back_populates="Administrador")

# Criação do Model para a entidade de Membro
class Membro(Base):
    __tablename__ = "membros"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    sexo = Column(String(10), CheckConstraint("sexo IN ('Masculino', 'Feminino')"), nullable=False)
    unidade_id = Column(Integer, ForeignKey("unidades.id"))
    posicao = Column(String(255), nullable=False)
    endereco = Column(String(255), nullable=False)
    bairro = Column(String(255), nullable=False)
    estado_civil = Column(String(255), nullable=False)
    telefone = Column(String(255), nullable=False)
    profissao = Column(String(255), nullable=False)
    data_conversao = Column(Date)
    batismo = Column(String(255), nullable=False)
    data_batismo = Column(Date)
    unidade = relationship("Unidade", back_populates="Membro")
    administradores = relationship("Administrador", back_populates="Membro")

class Unidade(Base):
    __tablename__ = "unidades"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    cidade = Column(String(255), nullable=False)
    cep = Column(String(255), nullable=False)
    endereco = Column(String(255), nullable=False)
    bairro = Column(String(255), nullable=False)
    estado = Column(String(255), nullable=False)
    administradores = relationship("Administrador", back_populates="Unidade")
    membros = relationship("Membro", back_populates="Unidade")
