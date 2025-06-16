# src/core/infrastructure/persistence/daos.py

from sqlalchemy.orm import Session
from typing import List, Optional
from src.core.domain.models import Task
from src.core.infrastructure.persistence.database import TaskModel

class TaskDAO:
    def get_all(self, db: Session) -> List[Task]: # <--- VERIFIQUE AQUI! O 'db: Session' é crucial
        return [Task.from_orm(task) for task in db.query(TaskModel).all()]

    def get_by_id(self, db: Session, task_id: int) -> Optional[Task]: # <--- VERIFIQUE AQUI!
        task_model = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        return Task.from_orm(task_model) if task_model else None

    def create(self, db: Session, task_data: dict) -> Task: # <--- VERIFIQUE AQUI!
        # Removendo 'id' se presente e for None ou 0, para o banco de dados gerar.
        if 'id' in task_data and (task_data['id'] is None or task_data['id'] == 0):
            del task_data['id']

        new_task_model = TaskModel(**task_data)
        db.add(new_task_model)
        db.commit()
        db.refresh(new_task_model)
        return Task.from_orm(new_task_model)

    def update(self, db: Session, task_id: int, updated_data: dict) -> Optional[Task]: # <--- VERIFIQUE AQUI!
        task_model = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task_model:
            return None
        for key, value in updated_data.items():
            setattr(task_model, key, value)
        db.commit()
        db.refresh(task_model)
        return Task.from_orm(task_model)

    def delete(self, db: Session, task_id: int) -> bool: # <--- VERIFIQUE AQUI!
        task_model = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task_model:
            return False
        db.delete(task_model)
        db.commit()
        return True