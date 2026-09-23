# Sistema de Biblioteca 📚

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1.1-092E20?logo=django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://www.docker.com/)
[![Status](https://img.shields.io/badge/Status-P1%20Conclu%C3%ADda%20%7C%20CRUD%20Completo-brightgreen)]()

Aplicação web desenvolvida com **Django** e **PostgreSQL** para gerenciamento completo de um acervo de livros, com foco em arquitetura limpa, segurança e experiência do usuário (UI/UX contemporânea), atendendo a todos os requisitos da entrega da **P1** de Laboratório de Programação Full Stack (Universidade de Vassouras).

O projeto contempla a arquitetura MTV (Model-Template-View), persistência com Django ORM, operações completas de CRUD (Create, Read, Update, Delete), busca textual com objetos `Q`, filtro dinâmico de status, validações customizadas no `ModelForm`, homepage integrada na raiz (`/`), painel administrativo nativo com Django Admin, herança de templates e proteção contra CSRF.

> **Status atual:** CRUD 100% implementado e funcional, com busca, filtros dinâmicos e validação customizada para a P1.

---

## 🚀 Funcionalidades

- [x] **Homepage intuitiva na raiz (`/`)**: dashboard com métricas do acervo (total, disponíveis, indisponíveis) e títulos recentes
- [x] **Busca Textual Inteligente (Feature P1)**: pesquisa simultânea por título OU autor com insensibilidade a maiúsculas/minúsculas usando objetos `Q` (`Q(titulo__icontains=...) | Q(autor__icontains=...)`)
- [x] **Filtro Dinâmico por Status (Feature P1)**: refinamento de livros por disponibilidade (Disponíveis / Emprestados) combinável com a busca textual
- [x] **Preservação de Estado nos Filtros**: inputs de busca e seletores mantêm os valores após a submissão via parâmetros HTTP GET (`request.GET`)
- [x] **Tratamento de Lista Vazia com `{% empty %}`**: exibição amigável e opção de limpar filtros quando nenhum exemplar corresponde à busca
- [x] **CRUD Completo de Livros**:
  - **Create**: cadastro com validação via `ModelForm` e feedback visual
  - **Read**: listagem com badge de status, busca textual e filtros
  - **Update**: edição completa de título, autor, ano e status de disponibilidade
  - **Delete**: exclusão com tela dedicada de confirmação segura (prevenção contra deleções acidentais via `POST`)
- [x] **Validação Customizada de Negócio (Feature P1)**: método `clean_ano()` no `LivroForm` impedindo que livros sejam cadastrados com ano de publicação futuro (`datetime.date.today().year`)
- [x] **Feedback visual instantâneo**: integração com o framework `django.contrib.messages` (alertas toast de sucesso, erro e atenção)
- [x] **Painel de gestão integrado**: Django Admin habilitado e configurado para o model `Livro`
- [x] **Interface moderna e responsiva**: design system com paleta equilibrada, tipografia Inter, cards, micro-interações e compatibilidade mobile
- [x] **Segurança e boas práticas**: proteção contra CSRF em todos os formulários e segredos isolados via `python-dotenv`

---

## 🛠️ Tecnologias

| Categoria                 | Tecnologia                                           |
| ------------------------- | ---------------------------------------------------- |
| Linguagem                 | Python 3.12+                                         |
| Framework web             | Django 6.1.1                                         |
| Banco de dados            | PostgreSQL 16                                        |
| Driver do banco           | `psycopg2-binary`                                    |
| ORM                       | Django ORM                                           |
| Formulários               | Django `ModelForm`                                   |
| Front-end                 | HTML5, CSS3 moderno e DTL (Django Template Language) |
| Gerenciamento de ambiente | `python-dotenv`                                      |
| Containerização           | Docker Compose                                       |

---

## 📋 Pré-requisitos

Antes de iniciar a instalação, certifique-se de possuir instalado:

- [Python 3.12 ou superior](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/) e Docker Compose (para subir o PostgreSQL)

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

Copie o modelo de variáveis de ambiente `.env.example` para `.env`:

#### Linux / macOS:

```bash
cp .env.example .env
```

#### Windows:

```cmd
copy .env.example .env
```

O arquivo `.env` virá pré-configurado para o banco de dados Docker:

```env
DB_NAME=biblioteca_db
DB_USER=postgres
DB_PASSWORD=senha
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=django-insecure-chave-secreta-exemplo
```

### 5. Inicie o banco de dados com Docker

Suba o contêiner do PostgreSQL em segundo plano:

```bash
docker compose up -d
```

Para pausar o contêiner:

```bash
docker compose down
```

### 6. Execute as migrações

```bash
python manage.py migrate
```

### 7. Crie o superusuário para o Django Admin (Opcional)

Para gerenciar o sistema também pelo painel administrativo:

```bash
python manage.py createsuperuser
```

### 8. Inicie o servidor de desenvolvimento

```bash
python manage.py runserver
```

Acesse a aplicação diretamente pelo navegador:

- **Homepage / Início:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Catálogo de Livros:** [http://127.0.0.1:8000/livros/](http://127.0.0.1:8000/livros/)
- **Cadastro de Livro:** [http://127.0.0.1:8000/livros/novo/](http://127.0.0.1:8000/livros/novo/)
- **Painel Administrativo:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🔗 Mapa de Rotas da Aplicação

| Rota                                                  |   Método   | Descrição                                                |
| ----------------------------------------------------- | :--------: | -------------------------------------------------------- |
| [`/`](http://127.0.0.1:8000/)                         |    GET     | Homepage com estatísticas do acervo e livros recentes    |
| [`/livros/`](http://127.0.0.1:8000/livros/)           |    GET     | Listagem de livros com busca textual (Q objects), filtros de status e ações |
| [`/livros/novo/`](http://127.0.0.1:8000/livros/novo/) | GET / POST | Formulário de criação de novo livro                      |
| `/livros/<id>/editar/`                                | GET / POST | Formulário de edição dos dados de um livro existente     |
| `/livros/<id>/excluir/`                               | GET / POST | Tela de confirmação e exclusão definitiva do livro       |
| [`/admin/`](http://127.0.0.1:8000/admin/)             | GET / POST | Painel administrativo nativo do Django                   |

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
- **Executar os testes automatizados:**
  ```bash
  python manage.py test
  ```
- **Verificar o status dos contêineres Docker:**
  ```bash
  docker compose ps
  ```

---

## 📂 Estrutura do Projeto

```text
.
├── acervo/                         # Aplicação de gestão do acervo
│   ├── migrations/                 # Histórico de migrações do banco
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── static/acervo/              # Folhas de estilo (CSS moderno)
│   │   └── estilo.css
│   ├── templates/acervo/           # Templates HTML integrados ao DTL
│   │   ├── base.html               # Layout base e navbar global
│   │   ├── home.html               # Página inicial (dashboard de métricas)
│   │   ├── lista.html              # Listagem de livros e ações
│   │   ├── form.html               # Formulário unificado (cadastro e edição)
│   │   └── confirmar_exclusao.html # Tela de confirmação segura de deleção
│   ├── admin.py                    # Registro no Django Admin
│   ├── apps.py                     # Configuração do app
│   ├── forms.py                    # Definição do ModelForm (LivroForm)
│   ├── models.py                   # Model Livro (ORM)
│   ├── tests.py                    # Suíte de testes automatizados
│   ├── urls.py                     # Rotas internas do app
│   └── views.py                    # Lógica de negócio e CRUD
├── biblioteca/                     # Núcleo de configuração do projeto
│   ├── asgi.py                     # Interface ASGI
│   ├── settings.py                 # Configurações do Django e banco
│   ├── urls.py                     # Roteador central raiz
│   └── wsgi.py                     # Interface WSGI
├── docker-compose.yml              # Serviço PostgreSQL em contêiner
├── .env.example                    # Modelo versionado de variáveis de ambiente
├── .prettierignore                 # Proteção de formatação para templates DTL
├── manage.py                       # CLI do Django
├── requirements.txt                # Dependências Python (UTF-8)
└── README.md                       # Documentação técnica do projeto
```

---

## 🔐 Boas Práticas e Segurança

- **Credenciais protegidas:** O arquivo `.env` nunca é commitado no repositório.
- **SECRET_KEY dinâmica:** Configurada via variáveis de ambiente com fallback para desenvolvimento local.
- **Proteção CSRF:** Formulários protegidos com token obrigatório `{% csrf_token %}`.
- **Deleção Segura:** A exclusão de registros requer confirmação expressa e envio via método `POST`, prevenindo exclusões acidentais via requisições diretas `GET`.

---

## 📄 Licença e Créditos

Projeto desenvolvido para fins acadêmicos na disciplina de **Laboratório de Programação Full Stack** do curso de Engenharia de Software.
