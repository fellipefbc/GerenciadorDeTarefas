# src/api/endpoints.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session

# Importações dos módulos da sua estrutura de src/
# core/domain/models.py
from src.core.domain.models import Task

# core/application/services.py
from src.core.application.services import TaskService

# core/infrastructure/persistence/daos.py
from src.core.infrastructure.persistence.daos import TaskDAO

# core/infrastructure/common/dependencies.py
from src.core.infrastructure.common.dependencies import get_db

# Criar uma instância de APIRouter
# APIRouter é como um "mini-FastAPI" que pode ser incluído em um FastAPI principal
router = APIRouter()

# Instanciando o DAO e o Service fora dos endpoints, como antes
# NOTA: Em aplicações maiores, você pode querer injetar o Service e o DAO via Depends também,
# mas para este escopo, instanciar aqui e passar a dependência 'db' para os métodos do service é suficiente.
task_dao = TaskDAO()
task_service = TaskService(task_dao)


# Endpoints da API RESTful (agora usando 'router' em vez de 'app')

@router.get("/tasks", response_model=List[Task], summary="Lista todas as tarefas")
async def get_tasks(db: Session = Depends(get_db)):
    """
    Retorna uma lista de todas as tarefas cadastradas.
    """
    return task_service.get_all_tasks(db)

@router.post("/tasks", response_model=Task, status_code=201, summary="Cria uma nova tarefa")
async def create_task(title: str, description: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Cria uma nova tarefa no sistema.
    - **title**: Título da tarefa (obrigatório).
    - **description**: Descrição detalhada da tarefa (opcional).
    """
    return task_service.create_new_task(db, title, description)

@router.get("/tasks/{task_id}", response_model=Task, summary="Busca uma tarefa por ID")
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Busca uma tarefa específica pelo seu ID.
    - **task_id**: O ID numérico da tarefa.
    """
    try:
        return task_service.get_task_by_id(db, task_id)
    except HTTPException as e:
        raise e

@router.put("/tasks/{task_id}", response_model=Task, summary="Atualiza uma tarefa existente")
async def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados de uma tarefa existente.
    - **task_id**: O ID numérico da tarefa a ser atualizada.
    - **title**: Novo título da tarefa (opcional).
    - **description**: Nova descrição da tarefa (opcional).
    - **completed**: Status de conclusão da tarefa (true/false, opcional).
    """
    try:
        return task_service.update_existing_task(db, task_id, title, description, completed)
    except HTTPException as e:
        raise e

@router.delete("/tasks/{task_id}", status_code=204, summary="Deleta uma tarefa")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Deleta uma tarefa específica pelo seu ID.
    - **task_id**: O ID numérico da tarefa a ser deletada.
    """
    try:
        task_service.delete_task(db, task_id)
    except HTTPException as e:
        raise e
    return {}
