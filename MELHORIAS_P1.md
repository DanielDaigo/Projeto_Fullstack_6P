# Revisão da P1 e Evolução para o Trabalho Final (P2)

Documento elaborado conforme diretriz da **Aula 13 (Slide 5)** da disciplina de **Laboratório de Programação Full Stack** (Universidade de Vassouras — Prof. Márcio Garrido), registrando os 5 pontos de fragilidade identificados na entrega da **P1** e como cada um foi corrigido na consolidação do **Trabalho Final P2 (Mini-SaaS)**.

---

## 📋 Itens de Melhoria Identificados na P1

### 1. Centralização da Regra de Negócio no Model (Dívida Técnica)
* **O que estava frágil na P1:** A validação de ano de publicação futuro (`clean_ano()`) existia apenas no `LivroForm`. Qualquer cadastro feito pelo Django Admin ou pela futura API REST conseguiria burlar a regra ou exigiria duplicação de código.
* **Correção aplicada na P2:** A função `validar_ano_nao_futuro` foi movida para `acervo/models.py` (como validator do campo `ano` e no método `Livro.clean()`), sendo reaproveitada tanto pelo `LivroForm` quanto pelo `LivroSerializer` do DRF.

### 2. Modelagem Incompleta de Relacionamentos (Modelagem)
* **O que estava frágil na P1:** O sistema possuía apenas o model `Livro` com um campo booleano `disponivel`, sem registrar quem pegou o livro nem quando ocorreu o empréstimo ou devolução.
* **Correção aplicada na P2:** Foram adicionados os models `Leitor` e `Emprestimo` (com `ForeignKey` para `Livro` e `Leitor`, `data_saida` indexada via `models.Index` e `devolvido_em`), viabilizando histórico real, séries temporais (`TruncMonth`) e rankings no dashboard.

### 3. Ausência de Isolamento Multi-organização e Unicidade por Tenant (Segurança)
* **O que estava frágil na P1:** Todos os livros ficavam em uma base única e as views de edição/exclusão buscavam apenas por `pk` (`get_object_or_404(Livro, pk=pk)`), permitindo acesso indevido entre clientes (IDOR).
* **Correção aplicada na P2:** Criado o app `core` com `Organizacao`, classe abstrata `DaOrganizacao` e `Perfil`. Aplicada migração segura em 3 etapas sem perda dos registros da P1, `UniqueConstraint(fields=['organizacao', 'titulo', 'autor'])`, filtragem obrigatória por `org_atual(request)` em todas as views/API e proteção contra IDOR retornando HTTP 404.

### 4. Controle de Acesso Genérico sem Papéis Definidos (Autenticação e Permissões)
* **O que estava frágil na P1:** Não havia distinção entre perfis operacionais e administrativos nem fluxo próprio de login/logout fora do Django Admin.
* **Correção aplicada na P2:** Adicionado o campo `papel` (`admin` / `operador`) e a propriedade `eh_admin` em `Perfil`, criado o decorator `@papel_requerido('admin')`, implementadas telas dedicadas de `/login/` e `/logout/` e aplicadas permissões diferenciadas no dashboard e na exportação CSV.

### 5. Ausência de Testes Automatizados e Otimização de Consultas (Qualidade e Desempenho)
* **O que estava frágil na P1:** A validação do sistema era apenas manual e não havia proteção automatizada contra regressões ou consultas N+1.
* **Correção aplicada na P2:** Aplicado `select_related('livro', 'leitor')` nas consultas de empréstimos e construída suíte com **19 testes automatizados** (`python manage.py test`) cobrindo isolamento multi-tenant, unicidade por organização, validação centralizada no Model, métricas do dashboard, bloqueio por papel, exportação CSV sanitizada, API REST e `assertNumQueries(1)`.

---

## ✅ Resumo de Entrega — Trabalho Final P2

| # | Item de Revisão da P1 | Status no Trabalho Final P2 |
| :-: | :--- | :---: |
| 1 | Validação centralizada no Model (`validar_ano_nao_futuro`) | ✅ Concluído |
| 2 | Novos models relacionais (`Leitor`, `Emprestimo` + índice em `data_saida`) | ✅ Concluído |
| 3 | Multi-organização, migração em 3 etapas, `UniqueConstraint` e blindagem IDOR | ✅ Concluído |
| 4 | Perfis de acesso (`admin`/`operador`), `@papel_requerido` e Login/Logout | ✅ Concluído |
| 5 | Otimização contra N+1 (`select_related`) e 19 testes automatizados (`assertNumQueries`) | ✅ Concluído |
