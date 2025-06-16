# src/core/infrastructure/common/dependencies.py

from src.core.infrastructure.persistence.database import SessionLocal
from sqlalchemy.orm import Session

# Função para obter uma sessão de banco de dados (usada com FastAPI Depends)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()