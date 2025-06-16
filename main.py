# main.py

from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from typing import List, Optional

# Importações dos módulos da sua estrutura de src/
# core/domain/models.py
from src.core.domain.models import Task

# core/application/services.py
from src.core.application.services import TaskService

# core/infrastructure/persistence/daos.py
from src.core.infrastructure.persistence.daos import TaskDAO

# core/infrastructure/persistence/database.py (para obter a sessão de DB)
from src.core.infrastructure.persistence.database import SessionLocal, engine, Base

# core/infrastructure/common/dependencies.py
from src.core.infrastructure.common.dependencies import get_db

# Cria as tabelas no banco de dados quando a aplicação é iniciada
# (Isso é feito uma vez na inicialização)
Base.metadata.create_all(bind=engine)

# Instância da aplicação FastAPI
app = FastAPI(
    title="API de Gerenciamento de Tarefas",
    description="Uma API RESTful completa para gerenciar tarefas, utilizando Clean Architecture e princípios SOLID.",
    version="1.0.0"
)

# Instanciando o DAO e o Service fora dos endpoints
# Para o serviço, passamos uma instância do DAO
# Em um cenário mais complexo, você usaria injeção de dependência mais avançada (ex: para testar)
task_dao = TaskDAO()
task_service = TaskService(task_dao)


# Endpoints da API RESTful

@app.get("/tasks", response_model=List[Task], summary="Lista todas as tarefas")
async def get_tasks(db: SessionLocal = Depends(get_db)):
    """
    Retorna uma lista de todas as tarefas cadastradas.
    """
    # O serviço agora recebe a sessão do banco de dados para repassar ao DAO
    return task_service.get_all_tasks(db)

@app.post("/tasks", response_model=Task, status_code=201, summary="Cria uma nova tarefa")
async def create_task(title: str, description: Optional[str] = None, db: SessionLocal = Depends(get_db)):
    """
    Cria uma nova tarefa no sistema.
    - **title**: Título da tarefa (obrigatório).
    - **description**: Descrição detalhada da tarefa (opcional).
    """
    return task_service.create_new_task(db, title, description)

@app.get("/tasks/{task_id}", response_model=Task, summary="Busca uma tarefa por ID")
async def get_task(task_id: int, db: SessionLocal = Depends(get_db)):
    """
    Busca uma tarefa específica pelo seu ID.
    - **task_id**: O ID numérico da tarefa.
    """
    try:
        return task_service.get_task_by_id(db, task_id)
    except HTTPException as e:
        raise e # Repassa a exceção HTTP (404) do serviço

@app.put("/tasks/{task_id}", response_model=Task, summary="Atualiza uma tarefa existente")
async def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
    db: SessionLocal = Depends(get_db)
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
        raise e # Repassa a exceção HTTP (404) do serviço

@app.delete("/tasks/{task_id}", status_code=204, summary="Deleta uma tarefa")
async def delete_task(task_id: int, db: SessionLocal = Depends(get_db)):
    """
    Deleta uma tarefa específica pelo seu ID.
    - **task_id**: O ID numérico da tarefa a ser deletada.
    """
    try:
        task_service.delete_task(db, task_id)
    except HTTPException as e:
        raise e # Repassa a exceção HTTP (404) do serviço
    return {} # Retorna vazio com status 204 (No Content) para DELETE bem-sucedido


if __name__ == "__main__":
    # Para rodar a aplicação: uvicorn main:app --reload
    # O host 0.0.0.0 permite acesso de outras máquinas na rede,
    # mas para desenvolvimento local, 127.0.0.1 ou localhost é suficiente.
    uvicorn.run(app, host="0.0.0.0", port=8000)