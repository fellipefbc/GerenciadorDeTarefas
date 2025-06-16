# main.py

from fastapi import FastAPI
import uvicorn

# Importa a Base e o engine do banco de dados para criar as tabelas
from src.core.infrastructure.persistence.database import Base, engine

# Importa o roteador de endpoints que criamos
from src.api.endpoints import router as api_router

# Cria as tabelas no banco de dados quando a aplicação é iniciada
# (Isso é feito uma vez na inicialização)
Base.metadata.create_all(bind=engine)

# Instância da aplicação FastAPI
app = FastAPI(
    title="API de Gerenciamento de Tarefas",
    description="Uma API RESTful completa para gerenciar tarefas, utilizando Clean Architecture e princípios SOLID.",
    version="1.0.0"
)

# Incluir o roteador de endpoints na aplicação principal
# Tudo que está no 'api_router' (seus /tasks, /tasks/{id}) será agora parte da 'app'
app.include_router(api_router)


if __name__ == "__main__":
    # Para rodar a aplicação: uvicorn main:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)
