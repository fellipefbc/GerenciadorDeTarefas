# Projeto Tarefas: API de Gerenciamento de Tarefas

## Descrição do Projeto

Este projeto consiste no desenvolvimento de uma aplicação RESTful completa para gerenciamento de tarefas, criada como trabalho final da disciplina de Aplicações para Internet da Uniube. [cite_start]O objetivo é consolidar os conhecimentos em arquitetura de software, APIs RESTful, padrões de projeto e consumo de serviços web[cite: 2]. [cite_start]A aplicação segue princípios de boas práticas de desenvolvimento, arquitetura limpa (Clean Architecture) e exposição de serviços via HTTP[cite: 1].

O sistema permite realizar operações básicas de CRUD (Criar, Ler, Atualizar, Deletar) em tarefas, oferecendo uma interface programática para interação através de uma API RESTful. [cite_start]Para simplicidade e conformidade com o requisito de cliente, a API é exposta via Swagger/OpenAPI, que também serve como uma ferramenta interativa para testes. [cite: 8]

## Requisitos Atendidos

* **Estrutura e Arquitetura:**
    * [cite_start]Arquitetura Limpa (Clean Architecture) aplicada. [cite: 4]
    * [cite_start]Aplicação dos princípios SOLID. [cite: 4]
    * [cite_start]Utilização dos padrões de design Service e DAO (Data Access Object). [cite: 4]
    * [cite_start]Utilização adequada de Injeção de Dependência. [cite: 4]
* **API RESTful:**
    * [cite_start]Recursos expostos como uma API RESTful. [cite: 5]
    * [cite_start]Endpoints HTTP implementados com métodos GET, POST, PUT, DELETE. [cite: 5]
    * [cite_start]Retorno de códigos de status HTTP apropriados. [cite: 5]
    * [cite_start]Tratamento de erros padronizado (ex: 404, 400, 500). [cite: 6]
    * [cite_start]Troca de dados em formato JSON. [cite: 7]
* **Persistência de Dados:**
    * [cite_start]Utilização de banco de dados relacional (SQLite para desenvolvimento, facilmente configurável para PostgreSQL/MySQL). [cite: 7]
    * [cite_start]Aplicação do padrão DAO para acesso aos dados. [cite: 8]
* **Cliente para Consumo da API:**
    * [cite_start]Documentação interativa da API via Swagger/OpenAPI, com suporte a testes. [cite: 8]

## Tecnologias Utilizadas

* **Backend:**
    * **Linguagem:** Python
    * **Framework Web:** FastAPI
    * **ORM (Object-Relational Mapper):** SQLAlchemy
    * **Servidor ASGI:** Uvicorn
* **Banco de Dados:**
    * [cite_start]SQLite (para desenvolvimento e testes locais, arquivo `tasks.db`) [cite: 7]
    * *Configurável para PostgreSQL/MySQL através da string de conexão do SQLAlchemy.*

## Como Executar a Aplicação

Siga os passos abaixo para configurar e rodar o projeto em seu ambiente local.

### Pré-requisitos

Certifique-se de ter o Python 3.8+ instalado em sua máquina.

### Passos

1.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/[SEU_USUARIO_GITHUB]/[SEU_NOME_DO_PROJETO].git
    cd [SEU_NOME_DO_PROJETO]
    ```

2.  **Crie um Ambiente Virtual (Recomendado):**
    ```bash
    python -m venv venv
    ```

3.  **Ative o Ambiente Virtual:**
    * **Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
    * **Windows (CMD):**
        ```cmd
        .\venv\Scripts\activate.bat
        ```
    * **Linux / macOS:**
        ```bash
        source venv/bin/activate
        ```

4.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Execute a Aplicação:**
    ```bash
    uvicorn main:app --reload
    ```
    * A aplicação estará disponível em `http://127.0.0.1:8000`.
    * O `--reload` faz com que o servidor reinicie automaticamente ao detectar mudanças nos arquivos do projeto.

## Instruções para Testar os Endpoints

A API possui uma documentação interativa integrada com o Swagger UI, que pode ser acessada através do seu navegador.

1.  **Acesse a Documentação:**
    * Com a aplicação rodando (ver passo 5 acima), abra seu navegador e navegue para:
        `http://127.0.0.1:8000/docs`

2.  **Utilizando o Swagger UI:**
    * Nesta página, você verá todos os endpoints disponíveis (`/tasks` com os métodos GET, POST, PUT, DELETE).
    * **Para testar um endpoint:**
        1.  Clique no endpoint desejado para expandi-lo.
        2.  Clique no botão **"Try it out"**.
        3.  Preencha os campos de parâmetros (se houver, como `title` e `description` para POST, ou `task_id` para GET, PUT, DELETE).
        4.  Clique no botão **"Execute"**.
        5.  A resposta da API (código de status, corpo da resposta e cabeçalhos) será exibida logo abaixo.

### Exemplos de Requisições:

* **POST /tasks:**
    * **Objetivo:** Criar uma nova tarefa.
    * **Parâmetros:** `title` (obrigatório, string), `description` (opcional, string).
    * **Exemplo:**
        * `title`: "Comprar leite"
        * `description`: "Na padaria antes das 18h"
    * **Resposta esperada (201 Created):** Retornará a tarefa criada com um `id`.

* **GET /tasks:**
    * **Objetivo:** Listar todas as tarefas.
    * **Parâmetros:** Nenhum.
    * **Resposta esperada (200 OK):** Uma lista de objetos de tarefa.

* **GET /tasks/{task_id}:**
    * **Objetivo:** Buscar uma tarefa específica por ID.
    * **Parâmetros:** `task_id` (numérico, do ID de uma tarefa existente).
    * **Resposta esperada (200 OK):** O objeto da tarefa correspondente.
    * **Tratamento de erro (404 Not Found):** Se o ID não existir.

* **PUT /tasks/{task_id}:**
    * **Objetivo:** Atualizar uma tarefa existente.
    * **Parâmetros:** `task_id` (do ID da tarefa a ser atualizada), `title`, `description`, `completed` (todos opcionais para atualização).
    * **Exemplo:** Para marcar uma tarefa como concluída:
        * `task_id`: `[ID_DA_TAREFA_EXISTENTE]`
        * `completed`: `true`
    * **Resposta esperada (200 OK):** O objeto da tarefa atualizada.
    * **Tratamento de erro (404 Not Found):** Se o ID não existir.

* **DELETE /tasks/{task_id}:**
    * **Objetivo:** Deletar uma tarefa.
    * **Parâmetros:** `task_id` (do ID da tarefa a ser deletada).
    * **Resposta esperada (204 No Content):** Sucesso na exclusão.
    * **Tratamento de erro (404 Not Found):** Se o ID não existir.

## Grupo

* Fellipe Freitas 5161168
* Douglas Almeida 5160386
* Tamyris Vitoria 5160937

---
