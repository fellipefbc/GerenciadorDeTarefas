# database.py (ou integre no main.py para simplicidade no trabalho)

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List, Optional

# Base para as classes de modelo
Base = declarative_base()

# Definição do modelo da tabela de tarefas
class TaskModel(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

# Configuração do banco de dados SQLite (para PostgreSQL/MySQL, a string de conexão muda)
# Para SQLite, criará um arquivo 'tasks.db' na mesma pasta.
# Para PostgreSQL: DATABASE_URL = "postgresql://user:password@host:port/database"
DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) # Necessário para SQLite em FastAPI

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Criar uma sessão de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe Task (modelo de dados para a aplicação, independente do banco de dados)
from pydantic import BaseModel

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

# DAO (Data Access Object) atualizado para usar SQLAlchemy
class TaskDAO:
    def get_db(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_all(self) -> List[Task]:
        db = next(self.get_db())
        return [Task.from_orm(task) for task in db.query(TaskModel).all()]

    def get_by_id(self, task_id: int) -> Optional[Task]:
        db = next(self.get_db())
        task_model = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        return Task.from_orm(task_model) if task_model else None

    def create(self, task_data: dict) -> Task:
        db = next(self.get_db())
        # Removendo 'id' se estiver presente, para o banco de dados gerar.
        if 'id' in task_data:
            del task_data['id']
        new_task_model = TaskModel(**task_data)
        db.add(new_task_model)
        db.commit()
        db.refresh(new_task_model)
        return Task.from_orm(new_task_model)

    def update(self, task_id: int, updated_data: dict) -> Optional[Task]:
        db = next(self.get_db())
        task_model = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task_model:
            return None
        for key, value in updated_data.items():
            setattr(task_model, key, value)
        db.commit()
        db.refresh(task_model)
        return Task.from_orm(task_model)

    def delete(self, task_id: int) -> bool:
        db = next(self.get_db())
        task_model = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task_model:
            return False
        db.delete(task_model)
        db.commit()
        return True