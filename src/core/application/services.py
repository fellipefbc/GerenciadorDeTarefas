# src/core/application/services.py

from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.core.domain.models import Task
from src.core.infrastructure.persistence.daos import TaskDAO

class TaskService:
    def __init__(self, dao: TaskDAO):
        self.dao = dao

    def get_all_tasks(self, db: Session) -> List[Task]:
        return self.dao.get_all(db)

    def get_task_by_id(self, db: Session, task_id: int) -> Task:
        task = self.dao.get_by_id(db, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    def create_new_task(self, db: Session, title: str, description: Optional[str]) -> Task:
        # O DAO vai lidar com a geração do ID
        return self.dao.create(db, {"title": title, "description": description, "completed": False})

    def update_existing_task(self, db: Session, task_id: int, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None) -> Task:
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if completed is not None:
            update_data["completed"] = completed

        updated_task = self.dao.update(db, task_id, update_data)
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")
        return updated_task

    def delete_task(self, db: Session, task_id: int) -> bool:
        if not self.dao.delete(db, task_id):
            raise HTTPException(status_code=404, detail="Task not found")
        return True