# SGHSS - Sistema de Gestão Hospitalar e de Serviços de Saúde

Este projeto consiste em uma API RESTful desenvolvida com Flask para o gerenciamento de pacientes, profissionais, consultas, teleconsultas, internações, prescrições, prontuários e notificações em uma instituição de saúde.

---

## 🛠 Tecnologias Utilizadas

- [Python 3.x](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [SQLite](https://www.sqlite.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Postman](https://www.postman.com/) (para testes da API)

---

## 📦 Estrutura do Projeto

```
Back-End/
│
├── app.py                  # Arquivo principal da aplicação
├── config.py               # Configurações da aplicação
├── instance/
│   └── app.db              # Banco de dados SQLite
│
├── models/                 # Modelos de dados (SQLAlchemy)
│   └── __init__.py
│
├── routes/                 # Rotas da aplicação
│   └── __init__.py
│
├── requirements.txt        # Dependências do projeto
└── README.md               # Este arquivo
```

---

## 📌 Funcionalidades Principais

- Cadastro e autenticação de usuários com JWT
- CRUD de pacientes e profissionais
- Agendamento e cancelamento de consultas
- Criação de teleconsultas vinculadas às consultas
- Registro e alta de internações
- Geração e listagem de prescrições e prontuários
- Notificações associadas a pacientes

---

## 🔐 Autenticação

A API utiliza **JWT (JSON Web Tokens)** para proteger as rotas.  
Após o login, é necessário enviar o token no cabeçalho das requisições autenticadas:

```
Authorization: Bearer <seu_token_aqui>
```

---

## ▶️ Como Rodar o Projeto

1. Clone o repositório:

```bash
git clone https://github.com/EdneyPaess/ProjetoUninter.git
cd ProjetoUninter/Back-End/
```

2. Crie o ambiente virtual e ative:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Inicialize o banco de dados:

```bash
# Essa parte já está dentro do código app.py,
# então também é possivel apenas pular para o passo 5
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
...
```

5. Execute o servidor:

```bash
python app.py
```

---

## 🧪 Testes

Você pode testar todos os endpoints utilizando o [Postman](https://www.postman.com/).  
As rotas estão documentadas no plano de testes disponível no repositório.

---

## 📄 Documentação de Endpoints

| Método | Rota                         | Descrição                 |
| ------ | ---------------------------- | ------------------------- |
| POST   | /cadastro                    | Cadastro de usuários      |
| POST   | /login                       | Autenticação de usuários  |
| POST   | /pacientes                   | Cadastro de pacientes     |
| GET    | /pacientes                   | Listagem de pacientes     |
| POST   | /profissionais               | Cadastro de profissionais |
| GET    | /profissionais               | Listagem de profissionais |
| POST   | /consultas                   | Agendamento de consultas  |
| GET    | /consultas                   | Listagem de consultas     |
| PUT    | /consultas/{id}              | Cancelamento de consulta  |
| POST   | /internacoes                 | Registrar internação      |
| PUT    | /internacoes/{id}            | Registrar alta            |
| GET    | /internacoes                 | Listagem de internações   |
| POST   | /notificacoes                | Criar notificação         |
| GET    | /notificacoes/{paciente_id}  | Listar notificações       |
| POST   | /teleconsultas               | Criar teleconsulta        |
| GET    | /teleconsultas/{paciente_id} | Listar teleconsultas      |
| POST   | /prontuarios                 | Criar prontuário          |
| GET    | /prontuarios/{paciente_id}   | Listar prontuários        |
| POST   | /prescricoes                 | Criar prescrição          |
| GET    | /prescricoes/{paciente_id}   | Listar prescrições        |

---

## 🧠 Autor

Este projeto foi desenvolvido por Edney Paes, como parte da Trilha Eletiva de Desenvolvimento com enfâse em Back-End.

---

## 📄 Licença

Este projeto é apenas para fins acadêmicos.
