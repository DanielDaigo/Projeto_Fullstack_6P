# Melhorias P1 & Débito Técnico &bull; Road to Mini-SaaS (P2)

Este documento registra a revisão técnica da entrega da **P1** do projeto **Biblioteca / Acervo** (Laboratório de Programação Full Stack - Prof. Márcio Garrido), apontando os itens de fragilidade identificados e o plano de evolução incremental até a **P2** (Aulas 13 a 20).

---

## 📌 Diagnóstico da P1 e Ações Corretivas

### 1. Ausência de Isolamento de Dados entre Clientes (Multi-tenancy)
* **Diagnóstico na P1:** Todos os livros cadastrados pertenciam a uma base global única. Qualquer usuário no sistema visualizava, editava ou excluía registros de outros estabelecimentos/inquilinos.
* **Impacto:** Inviabilidade de operação como SaaS e risco crítico de vazamento de dados (*data leak*).
* **Solução Implementada (Aula 14):** Criação do app `core` com os modelos `Organizacao`, classe abstrata `DaOrganizacao` e `Perfil` (OneToOne com `User`). Migração segura em 3 etapas sem perda dos dados da P1 e filtro compulsório `filter(organizacao=org)` em todas as consultas.

### 2. Vulnerabilidade a IDOR (Insecure Direct Object Reference)
* **Diagnóstico na P1:** As rotas de edição (`/livros/<id>/editar/`) e exclusão (`/livros/<id>/excluir/`) recuperavam instâncias apenas pela chave primária (`get_object_or_404(Livro, pk=pk)`).
* **Impacto:** Alterando o número do ID na URL, um usuário de uma biblioteca poderia editar ou excluir livros de outra.
* **Solução Implementada (Aula 14):** Blindagem via `get_object_or_404(Livro, pk=pk, organizacao=org_atual(request))`, retornando HTTP 404 (Not Found) caso o registro pertença a outro inquilino, não revelando sequer sua existência.

### 3. Autenticação Genérica e Falta de Controle de Acesso por Papel (RBAC)
* **Diagnóstico na P1:** Dependência do login nativo do Django Admin; ausência de diferenciação entre quem pode apenas operar/consultar e quem pode administrar o sistema.
* **Impacto:** Falta de rastreabilidade e incapacidade de conceder permissões parciais aos colaboradores da biblioteca.
* **Plano de Solução (Aula 15):** Implementação de tela própria de Login/Logout integrada ao design system e adição de papéis (`admin` vs `operador`) no modelo `Perfil`, com decoradores de permissão customizados.

### 4. Interface Estritamente Server-Side sem API REST
* **Diagnóstico na P1:** A aplicação funcionava apenas via DTL (Django Template Language), sem oferecer pontos de integração para terceiros, front-ends desacoplados ou aplicativos móveis.
* **Impacto:** Acoplamento monolítico rígido e impossibilidade de integração automatizada com outros serviços.
* **Plano de Solução (Aulas 16 a 19):** Instalação do Django REST Framework (DRF), criação de `LivroSerializer`, `ModelViewSet`, paginação, filtros e autenticação por token com isolamento estrito por tenant.

### 5. Métricas Analíticas Básicas no Dashboard
* **Diagnóstico na P1:** A tela inicial calculava apenas contagens diretas (`count()`) sem métricas de agregação avançadas.
* **Impacto:** Pouco valor gerencial para os gestores da biblioteca.
* **Plano de Solução (Aula 17):** Enriquecimento do Dashboard com consultas ORM analíticas (`aggregate`, `annotate`, `Count`, agrupamentos por autor e histórico).

---

> Documento de controle e rastreabilidade da P2. Atualizado continuamente a cada aula.
