# src/core/infrastructure/persistence/database.py

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Base para as classes de modelo
Base = declarative_base()

# Definição do modelo da tabela de tarefas no banco de dados
class TaskModel(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

# Configuração do banco de dados SQLite
# O arquivo 'tasks.db' será criado na mesma pasta onde o script é executado.
# Para PostgreSQL: DATABASE_URL = "postgresql://user:password@host:port/database"
# Para MySQL: DATABASE_URL = "mysql+pymysql://user:password@host:port/database"
DATABASE_URL = "sqlite:///./tasks.db"

# connect_args={"check_same_thread": False} é necessário para SQLite em múltiplos threads (como o Uvicorn)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Criar uma sessão de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)