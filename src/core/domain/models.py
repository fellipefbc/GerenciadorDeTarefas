# src/core/domain/models.py

from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    # O id pode ser opcional para criação, pois o banco de dados o gerará
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

    class Config:
        # orm_mode = True  # Para Pydantic v1 (FastAPI padrão)
        from_attributes = True # Preferível para Pydantic v2 (mais moderno, pode ser usado com FastAPI)
        # Você pode manter orm_mode = True ou usar from_attributes = True.
        # Se for Pydantic v1, orm_mode=True é o correto.
        # Se for Pydantic v2, from_attributes=True é o correto.
        # O FastAPI geralmente ainda usa Pydantic v1 por padrão em muitas instalações, então orm_mode=True deve funcionar.