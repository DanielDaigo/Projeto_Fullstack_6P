# Sistema de Biblioteca 📚

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1.1-092E20?logo=django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://www.docker.com/)
[![Status](<https://img.shields.io/badge/Status-CRUD%20Parcial%20(Aulas%204%20e%205)-yellow>)]()

Aplicação web desenvolvida com **Django** e **PostgreSQL** para gerenciamento de um acervo de livros, baseada nas Aulas 4 e 5 da disciplina de Laboratório de Programação Full Stack.

O projeto contempla a arquitetura MTV (Model-Template-View), persistência relacional com Django ORM, painel administrativo nativo com Django Admin, formulários com validação via `ModelForm`, herança de templates e proteção contra CSRF.

> **Status atual:** Operações de **Listagem (Read)** e **Cadastro (Create)** implementadas e funcionais. As operações de **Atualização (Update)** e **Exclusão (Delete)** serão adicionadas na Aula 6.

---

## 🚀 Funcionalidades

- [x] Conexão com banco PostgreSQL isolada por variáveis de ambiente (`python-dotenv`)
- [x] Modelagem de dados com o model `Livro` e migrações automatizadas
- [x] Painel de gestão integrado via Django Admin
- [x] Listagem dinâmica de livros persistidos no banco de dados
- [x] Cadastro de novos títulos com validação e integridade via `ModelForm`
- [x] Proteção em formulários contra ataques CSRF (`{% csrf_token %}`)
- [x] Layout componentizado com herança de templates (`base.html`) e folha de estilos personalizada (`estilo.css`)
- [ ] Atualização/edição de livros existentes (Aula 6)
- [ ] Exclusão de livros (Aula 6)
- [ ] Testes unitários e de integração
- [ ] Configurações otimizadas para deploy em produção

---

## 🛠️ Tecnologias

| Categoria                 | Tecnologia                                   |
| ------------------------- | -------------------------------------------- |
| Linguagem                 | Python 3.12+                                 |
| Framework web             | Django 6.1.1                                 |
| Banco de dados            | PostgreSQL 16                                |
| Driver do banco           | `psycopg2-binary`                            |
| ORM                       | Django ORM                                   |
| Formulários               | Django `ModelForm`                           |
| Front-end                 | HTML5, CSS3 e DTL (Django Template Language) |
| Gerenciamento de ambiente | `python-dotenv`                              |
| Containerização           | Docker Compose                               |

---

## 📋 Pré-requisitos

Antes de iniciar a instalação, certifique-se de ter instalado em seu computador:

- [Python 3.12 ou superior](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/) e Docker Compose (para executar o PostgreSQL localmente)

---

## 📦 Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/DanielDaigo/Projeto_Fullstack_6P.git
cd Projeto_Fullstack_6P
```

### 2. Crie e ative o ambiente virtual

#### Windows (PowerShell / CMD)

```powershell
python -m venv .venv
.venv\Scripts\activate
```

#### Linux ou macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Atualize o pip e instale as dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo modelo de variáveis de ambiente `.env.example` para `.env`:

#### Linux / macOS:

```bash
cp .env.example .env
```

#### Windows:

```cmd
copy .env.example .env
```

O arquivo `.env` gerado virá pré-configurado para o ambiente de desenvolvimento:

```env
DB_NAME=biblioteca_db
DB_USER=postgres
DB_PASSWORD=senha
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=django-insecure-chave-secreta-exemplo
```

> **Nota:** Se utilizar uma instância local do PostgreSQL em vez do Docker, altere os valores conforme a sua configuração de usuário e senha.

### 5. Inicie o banco de dados com Docker

Suba o contêiner do PostgreSQL em segundo plano:

```bash
docker compose up -d
```

Para pausar ou encerrar o contêiner quando não estiver utilizando:

```bash
docker compose down
```

### 6. Execute as migrações

Crie a estrutura de tabelas no banco de dados:

```bash
python manage.py migrate
```

### 7. Crie o superusuário para o Django Admin

Para poder gerenciar os livros pelo painel administrativo:

```bash
python manage.py createsuperuser
```

_(Siga as instruções do terminal informando nome de usuário, e-mail e senha)._

### 8. Inicie o servidor de desenvolvimento

```bash
python manage.py runserver
```

Acesse a aplicação no navegador:

- **Lista de Livros:** [http://127.0.0.1:8000/livros/](http://127.0.0.1:8000/livros/)
- **Cadastro de Livro:** [http://127.0.0.1:8000/livros/novo/](http://127.0.0.1:8000/livros/novo/)
- **Painel Administrativo:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🔗 Rotas da Aplicação

| Rota                                                  | Descrição                                                         |
| ----------------------------------------------------- | ----------------------------------------------------------------- |
| [`/livros/`](http://127.0.0.1:8000/livros/)           | Exibe a listagem completa dos livros cadastrados no banco         |
| [`/livros/novo/`](http://127.0.0.1:8000/livros/novo/) | Formulário para cadastro e validação de novos livros              |
| [`/admin/`](http://127.0.0.1:8000/admin/)             | Painel administrativo do Django para controle total dos registros |

---

## 🧪 Comandos Úteis

- **Acessar o terminal interativo do Django (ORM conectado):**
  ```bash
  python manage.py shell
  ```
- **Gerar novas migrações após alterar `models.py`:**
  ```bash
  python manage.py makemigrations
  ```
- **Executar a suíte de testes:**
  ```bash
  python manage.py test
  ```
- **Coletar arquivos estáticos para produção:**
  ```bash
  python manage.py collectstatic
  ```
- **Verificar o status do banco de dados Docker:**
  ```bash
  docker compose ps
  ```

---

## 📂 Estrutura do Projeto

```text
.
├── acervo/                 # App de gerenciamento do acervo de livros
│   ├── migrations/         # Histórico e arquivos de migração do banco
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── static/acervo/      # Arquivos estáticos (CSS)
│   │   └── estilo.css
│   ├── templates/acervo/   # Templates HTML (DTL)
│   │   ├── base.html       # Template base (esqueleto comum)
│   │   ├── form.html       # Tela de formulário de cadastro
│   │   └── lista.html      # Tela de listagem de livros
│   ├── admin.py            # Registro do model Livro no Django Admin
│   ├── apps.py             # Configuração da aplicação acervo
│   ├── forms.py            # Definição do ModelForm (LivroForm)
│   ├── models.py           # Definição do model Livro
│   ├── tests.py            # Arquivo de testes automatizados
│   ├── urls.py             # Mapeamento de rotas do app
│   └── views.py            # Funções de visão (regras de negócio)
├── biblioteca/             # Configurações centrais do projeto
│   ├── asgi.py             # Interface ASGI para servidores assíncronos
│   ├── settings.py         # Configurações gerais (banco, apps, timezone)
│   ├── urls.py             # Mapeamento central de rotas (raiz)
│   └── wsgi.py             # Interface WSGI para servidores web
├── docker-compose.yml      # Configuração do contêiner PostgreSQL
├── .env.example            # Modelo versionado de variáveis de ambiente
├── manage.py               # Utilitário CLI do Django
├── requirements.txt        # Lista de dependências do Python (UTF-8)
└── README.md               # Documentação técnica do projeto
```

---

## 🔐 Boas Práticas e Segurança

- **Segredos fora do versionamento:** O arquivo `.env` está explicitamente incluído no `.gitignore`. Nunca commite senhas de banco ou chaves secretas.
- **`SECRET_KEY` dinâmica:** Carregada a partir de variável de ambiente com chave alternativa apenas para desenvolvimento local.
- **Ambiente de Produção:** Em ambientes de produção, certifique-se de configurar `DEBUG = False` e definir os domínios em `ALLOWED_HOSTS`.
- **Proteção CSRF:** Todos os formulários HTML utilizam a tag `{% csrf_token %}` para evitar requisições maliciosas forjadas entre sites.

---

## 🛠️ Próximas Etapas (Rumo à Aula 6)

- [ ] Implementar a operação de **Edição/Atualização** de livros (`Update`).
- [ ] Implementar a operação de **Exclusão** de livros (`Delete`).
- [ ] Expor o campo `disponivel` na listagem e no formulário.
- [ ] Adicionar cobertura de testes unitários para models, views e forms.

---

## 📄 Licença e Créditos

Projeto desenvolvido com fins acadêmicos para a disciplina de **Laboratório de Programação Full Stack** do curso de Engenharia de Software.
