# Sistema de Biblioteca 📚

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1.1-092E20?logo=django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://www.docker.com/)
[![Status](https://img.shields.io/badge/Status-Aula%2014%20Conclu%C3%ADda%20%7C%20Multi--tenancy-blue)]()

Aplicação web desenvolvida com **Django** e **PostgreSQL** para gerenciamento de um acervo de livros em formato **Mini-SaaS Multi-tenant**, atendendo aos requisitos práticos da disciplina de Laboratório de Programação Full Stack (Universidade de Vassouras - Prof. Márcio Garrido).

O projeto evoluiu da entrega da P1 (CRUD, filtros com objetos `Q` e validações em `ModelForm`) para uma arquitetura multi-organização (Aula 14), com isolamento estrito de dados por inquilino (*tenant*), herança de modelo via classe abstrata `DaOrganizacao`, proteção contra IDOR (*Insecure Direct Object Reference*), migração em 3 etapas com zero perda de dados e suíte de testes automatizados.

> **Status atual:** Aula 14 concluída com sucesso. Multi-tenancy implementado via coluna discriminadora (`organizacao_id`), consultas 100% isoladas e 5 testes automatizados aprovados.

---

## 🚀 Funcionalidades

### Multi-organização & Isolamento de Dados (Aula 14)
- [x] **Arquitetura Multi-tenant (Coluna Discriminadora)**: Cada inquilino/organização possui acesso estritamente aos seus próprios dados.
- [x] **App `core` Transversal**: Modelos `Organizacao`, classe abstrata `DaOrganizacao` e `Perfil` (OneToOne com `User`).
- [x] **Migração Segura em 3 Etapas**: Inclusão de chave estrangeira permitindo nulo (`null=True`), preenchimento via `RunPython` com a *"Organização Padrão"* e transição final para não nulo (`null=False`) com zero perda dos dados legados da P1.
- [x] **Regra de Ouro nas Consultas**: Todas as views e listagens filtram com `filter(organizacao=org_atual(request))`.
- [x] **Prevenção de IDOR (Insecure Direct Object Reference)**: Rotas de edição e exclusão usam `get_object_or_404(Livro, pk=pk, organizacao=org)`, retornando 404 seguro ao tentar manipular IDs de outros inquilinos.
- [x] **Injeção Segura na Criação**: O campo `organizacao` nunca é exposto no formulário HTML; é injetado diretamente no servidor via `form.save(commit=False)`.
- [x] **Suíte de Testes Automatizados de Isolamento**: 5 testes cobrindo isolamento de leitura, blindagem contra IDOR na edição/exclusão, criação vinculada ao tenant e bloqueio anônimo.

### Funcionalidades do Acervo (P1)
- [x] **Homepage intuitiva na raiz (`/`)**: dashboard com métricas do acervo do tenant (total, disponíveis, indisponíveis) e títulos recentes
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
- [x] **Painel de gestão integrado**: Django Admin habilitado com filtros por organização e disponibilidade
- [x] **Interface moderna e responsiva**: design system com paleta equilibrada, tipografia Inter, cards, micro-interações e identificador visual da organização ativa

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

| Rota                                                  |   Método   | Descrição                                                                   |
| ----------------------------------------------------- | :--------: | --------------------------------------------------------------------------- |
| [`/`](http://127.0.0.1:8000/)                         |    GET     | Homepage com estatísticas do acervo e livros recentes                       |
| [`/livros/`](http://127.0.0.1:8000/livros/)           |    GET     | Listagem de livros com busca textual (Q objects), filtros de status e ações |
| [`/livros/novo/`](http://127.0.0.1:8000/livros/novo/) | GET / POST | Formulário de criação de novo livro                                         |
| `/livros/<id>/editar/`                                | GET / POST | Formulário de edição dos dados de um livro existente                        |
| `/livros/<id>/excluir/`                               | GET / POST | Tela de confirmação e exclusão definitiva do livro                          |
| [`/admin/`](http://127.0.0.1:8000/admin/)             | GET / POST | Painel administrativo nativo do Django                                      |

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

## 🏢 Arquitetura Multi-Tenant & Roteiro de Testes (Aula 14)

### Estratégia de Isolamento
Foi adotada a estratégia de **Coluna Discriminadora** (`organizacao_id` via chave estrangeira com `on_delete=models.PROTECT`), centralizada na classe abstrata `DaOrganizacao` do app `core`. Todo modelo de negócio herda de `DaOrganizacao`.

O usuário do Django (`User`) é estendido através de um relacionamento `OneToOneField` com `Perfil`, associando cada operador/administrador à sua organização.

### Migração em 3 Etapas (Zero Perda de Dados)
1. **Etapa 1 (`0002_livro_org_null`):** Adicionou a foreign key `organizacao` permitindo valores nulos temporariamente.
2. **Etapa 2 (`0003_dados_org`):** Migração de dados com `migrations.RunPython`, criando a *"Organização Padrão"* e vinculando tanto os livros legados da P1 quanto os usuários existentes.
3. **Etapa 3 (`0004_livro_org_not_null`):** Tornou a chave estrangeira estritamente obrigatória (`null=False`).

### Roteiro de Testes Executado
A suíte em `acervo/tests.py` foi executada e validou os 4 cenários fundamentais:

| Cenário de Teste | Ação Executada | Resultado Esperado | Status |
| :--- | :--- | :--- | :---: |
| **1. Isolamento de Listagem** | Usuário A consulta a listagem em `/livros/` | Enxerga apenas os livros pertencentes à Organização A | ✅ Aprovado |
| **2. Blindagem contra IDOR na Edição** | Usuário A tenta abrir `/livros/<ID-da-B>/editar/` | Retorna status **404 Not Found** (sem revelar existência do ID) | ✅ Aprovado |
| **3. Injeção Servidor na Criação** | Usuário A submete formulário de novo livro | Livro gravado automaticamente com FK vinculada à Organização A | ✅ Aprovado |
| **4. Blindagem contra IDOR na Exclusão** | Usuário A tenta GET ou POST em `/livros/<ID-da-B>/excluir/` | Retorna status **404 Not Found** e registro da Organização B preservado | ✅ Aprovado |
| **5. Bloqueio de Acesso Anônimo** | Usuário deslogado tenta acessar telas de negócio | Redirecionamento 302 compulsório para o fluxo de autenticação | ✅ Aprovado |

Para rodar os testes:
```bash
python manage.py test acervo
```

### Usuários de Teste Configurados
- **Usuário 1:** `operador_central` (Senha: `senha123`) &bull; Organização: **Biblioteca Central**
- **Usuário 2:** `operador_universitaria` (Senha: `senha123`) &bull; Organização: **Biblioteca Universitária**
- **Superusuário:** `Daniel` &bull; Organização: **Organização padrão**

---

## 📂 Estrutura do Projeto

```text
.
├── acervo/                         # Aplicação de gestão do acervo de livros
│   ├── migrations/                 # Histórico de migrações (inclui migração de dados)
│   │   ├── 0001_initial.py
│   │   ├── 0002_livro_org_null.py
│   │   ├── 0003_dados_org.py
│   │   └── 0004_livro_org_not_null.py
│   ├── static/acervo/              # Folhas de estilo (CSS moderno)
│   │   └── estilo.css
│   ├── templates/acervo/           # Templates HTML integrados ao DTL
│   │   ├── base.html               # Layout base com badge da organização ativa
│   │   ├── home.html               # Página inicial (dashboard de métricas da org)
│   │   ├── lista.html              # Listagem isolada por organização e ações
│   │   ├── form.html               # Formulário unificado (cadastro e edição)
│   │   └── confirmar_exclusao.html # Confirmação segura de deleção com proteção IDOR
│   ├── admin.py                    # Registro no Django Admin com filtros por organização
│   ├── apps.py                     # Configuração do app
│   ├── forms.py                    # ModelForm sem expor o campo organizacao
│   ├── models.py                   # Model Livro herdando de DaOrganizacao
│   ├── tests.py                    # Suíte de testes de isolamento multi-tenant
│   ├── urls.py                     # Rotas internas do app
│   └── views.py                    # Lógica de negócio, org_atual e @login_required
├── biblioteca/                     # Núcleo de configuração do projeto
│   ├── settings.py                 # Configurações do Django, banco e autenticação
│   ├── urls.py                     # Roteador central raiz
│   └── wsgi.py                     # Interface WSGI
├── core/                           # App transversal de infraestrutura e multi-tenancy
│   ├── migrations/                 # Migração inicial dos modelos do core
│   │   └── 0001_initial.py
│   ├── admin.py                    # Administração de Organizacao e Perfil
│   └── models.py                   # Modelos Organizacao, DaOrganizacao e Perfil
├── docker-compose.yml              # Serviço PostgreSQL em contêiner
├── MELHORIAS_P1.md                 # Documento de débito técnico e melhorias pós-P1
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
