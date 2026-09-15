# Sistema de Biblioteca 📚

Aplicação web desenvolvida com **Django** e **PostgreSQL** para gerenciamento de um acervo de livros. O projeto implementa listagem e cadastro de livros, utilizando Django ORM, `ModelForm`, templates reutilizáveis, validação de formulários e proteção CSRF.

> **Status atual:** CRUD parcial. As operações de atualização e exclusão ainda não estão implementadas.

---

## 🚀 Funcionalidades

- [x] Conexão com PostgreSQL configurada por variáveis de ambiente
- [x] Modelagem do livro com Django ORM
- [x] Listagem de livros persistidos no banco de dados
- [x] Cadastro de novos livros com validação via `ModelForm`
- [x] Proteção de formulários com CSRF
- [x] Interface responsiva com templates e arquivos estáticos
- [ ] Atualização de livros
- [ ] Exclusão de livros
- [ ] Testes automatizados
- [ ] Configurações específicas para produção

---

## 🛠️ Tecnologias

| Categoria | Tecnologia |
| --- | --- |
| Linguagem | Python 3.12+ |
| Framework web | Django 6.1.1 |
| Banco de dados | PostgreSQL 16 |
| ORM | Django ORM |
| Formulários | Django `ModelForm` |
| Front-end | HTML5 e CSS3 |
| Ambiente | `python-dotenv` |
| Containerização | Docker Compose |

---

## 📋 Pré-requisitos

Antes de executar o projeto, instale:

- [Python 3.12 ou superior](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/) e Docker Compose, para subir o PostgreSQL localmente

---

## 📦 Instalação e execução

### 1. Clone o repositório

```bash
git clone https://github.com/DanielDaigo/Projeto_Fullstack_6P.git
cd Projeto_Fullstack_6P
```

### 2. Crie e ative o ambiente virtual

#### Windows — PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
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

### 4. Suba o banco de dados com Docker

O arquivo `docker-compose.yml` inicia apenas o PostgreSQL. A aplicação Django continua sendo executada localmente.

```bash
docker compose up -d
```

Para parar o banco de dados:

```bash
docker compose down
```

### 5. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto. Ele não deve ser commitado, pois pode conter credenciais sensíveis.

Use valores compatíveis com o `docker-compose.yml`:

```env
DB_NAME=biblioteca_db
DB_USER=postgres
DB_PASSWORD=senha
DB_HOST=localhost
DB_PORT=5432
```

> Se você utilizar um PostgreSQL instalado localmente em vez do Docker, ajuste `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` e `DB_PORT` conforme a sua configuração.

### 6. Execute as migrações

```bash
python manage.py migrate
```

Se alterar os modelos posteriormente, execute também:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Inicie o servidor de desenvolvimento

```bash
python manage.py runserver
```

Acesse a aplicação em:

- Lista de livros: [http://127.0.0.1:8000/livros/](http://127.0.0.1:8000/livros/)
- Cadastro de livro: [http://127.0.0.1:8000/livros/novo/](http://127.0.0.1:8000/livros/novo/)

---

## 🔗 Rotas principais

| URL | Descrição |
| --- | --- |
| `/livros/` | Exibe a lista de livros cadastrados |
| `/livros/novo/` | Exibe o formulário para cadastrar um novo livro |

---

## 📂 Estrutura do projeto

```text
.
├── acervo/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── static/
│   │   └── acervo/
│   │       └── estilo.css
│   ├── templates/
│   │   └── acervo/
│   │       ├── base.html
│   │       ├── form.html
│   │       └── lista.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── biblioteca/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .env
├── .gitignore
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🧪 Comandos úteis

Executar testes:

```bash
python manage.py test
```

Coletar arquivos estáticos para produção:

```bash
python manage.py collectstatic
```

Verificar o status do banco Docker:

```bash
docker compose ps
```

---

## 🔐 Boas práticas de segurança

- Nunca commitar o arquivo `.env`.
- Não expor credenciais reais no repositório.
- Em produção, definir `DEBUG = False`.
- Configurar corretamente `ALLOWED_HOSTS`.
- Utilizar uma `SECRET_KEY` segura e exclusiva por ambiente.
- Preferir variáveis de ambiente ou um serviço de secrets para configurações sensíveis.

---

## 🛠️ Próximas melhorias

- Implementar atualização e exclusão de livros.
- Expor o campo `disponivel` na interface e no formulário.
- Criar um `.env.example` para orientar novas instalações.
- Adicionar testes automatizados para models, forms e views.
- Preparar configurações específicas para deploy em produção.

---

## 📄 Licença

Projeto desenvolvido para fins acadêmicos e práticos na disciplina de Engenharia de Software / Full Stack.