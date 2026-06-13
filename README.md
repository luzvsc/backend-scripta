# Scripta Backend

## Sobre o Projeto

O Scripta é uma plataforma acadêmica para gerenciamento de Projetos Integradores do Senac.

O sistema permite:

* Cadastro e autenticação de alunos
* Cadastro e autenticação de professores
* Cadastro e autenticação de empresas
* Gerenciamento de projetos
* Avaliação de projetos
* Geração de portfólios
* Emissão de certificados
* Contato entre empresas e alunos
* Relatórios acadêmicos
* Auditoria de ações do sistema

---

# Tecnologias Utilizadas

* Python 3.14
* FastAPI
* MySQL
* PyMySQL
* Pydantic
* Bcrypt
* JWT (python-jose)
* Uvicorn

---

# Instalação do Projeto

## 1. Clonar o repositório

git clone URL_DO_REPOSITORIO

## 2. Entrar na pasta backend

cd backend

## 3. Criar ambiente virtual

python -m venv venv

## 4. Ativar ambiente virtual

Windows:

venv\Scripts\activate

## 5. Instalar dependências

pip install -r requirements.txt

---

# Configuração do Banco de Dados

Instalar MySQL Server.

Criar banco:

CREATE DATABASE scripta;

Executar o arquivo:

scripta.sql

para criar todas as tabelas.

---

# Configurar Variáveis de Ambiente

Criar arquivo .env na raiz do backend:

DATABASE_HOST=localhost
DATABASE_USER=root
DATABASE_PASSWORD=sua_senha
DATABASE_NAME=scripta

JWT_SECRET_KEY=scripta_secret_key

---

# Testar Conexão com Banco

Executar:

python -m app.database.test_db

Resultado esperado:

Conexão realizada com sucesso

---

# Executar API

uvicorn app.main:app --reload

---

# Swagger

Acessar:

http://127.0.0.1:8000/docs

---

# Arquitetura

## Models

Representam os schemas Pydantic.

Responsabilidade:

* validar dados
* definir respostas da API

## Repository

Responsável exclusivamente pelo acesso ao banco.

Responsabilidade:

* SELECT
* INSERT
* UPDATE
* DELETE

Não deve conter regras de negócio.

## Service

Responsável pelas regras de negócio.

Exemplos:

* verificar email duplicado
* validar login
* gerar token JWT
* validar permissões

## Routes

Responsável pelos endpoints da API.

Exemplos:

* GET
* POST
* PUT
* DELETE

Não deve acessar banco diretamente.

Fluxo correto:

Route → Service → Repository → Banco

---

# Fluxo Git

Antes de começar:

git pull

Após finalizar tarefa:

git add .

git commit -m "descrição da alteração"

git push

---

# Regra da Equipe

Nunca alterar código de outro módulo sem alinhamento prévio.

Exemplo:

Quem estiver responsável por Professor não deve modificar Projeto sem comunicar a equipe.

Sempre testar as rotas no Swagger antes de enviar commit.
