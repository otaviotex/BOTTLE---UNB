from sqlalchemy import create_engine, Column, Integer, String, Date, Time
from sqlalchemy.orm import declarative_base, sessionmaker
import hashlib
import os

# Banco SQLite
engine = create_engine("sqlite:///clinica.db", echo=False)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# =============================
#        TABELAS
# =============================

class Medico(Base):
    __tablename__ = "medicos"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    genero = Column(String, nullable=False)
    crm = Column(String, unique=True, nullable=False)
    especialidade = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    salt = Column(String, nullable=False)



class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False) 
    idade = Column(Integer, nullable=False)
    convenio = Column(String, nullable=False)
    especialidade = Column(String, nullable=False)
    data = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)


# Criar tabelas caso não existam
Base.metadata.create_all(engine)
