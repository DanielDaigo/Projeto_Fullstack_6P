# Melhorias P1 & Débito Técnico &bull; Road to Mini-SaaS (P2)

Este documento registra a revisão técnica da entrega da **P1** do projeto **Biblioteca / Acervo** (Laboratório de Programação Full Stack - Prof. Márcio Garrido), acompanhando a resolução incremental de cada débito técnico até a **P2** (Aulas 13 a 17).

---

## 📌 Diagnóstico da P1 e Ações Corretivas

### 1. Ausência de Isolamento de Dados entre Clientes (Multi-tenancy) — ✅ Resolvido (Aula 14)
* **Diagnóstico na P1:** Todos os livros cadastrados pertenciam a uma base global única.
* **Solução Implementada:** Criação do app `core` com `Organizacao`, classe abstrata `DaOrganizacao` e `Perfil`. Migração segura em 3 etapas (`null=True` → `RunPython` → `null=False`) sem perda de dados da P1 e filtro compulsório `filter(organizacao=org)` em todas as consultas.

### 2. Vulnerabilidade a IDOR (Insecure Direct Object Reference) — ✅ Resolvido (Aula 14)
* **Diagnóstico na P1:** Edição e exclusão recuperavam instâncias apenas por `pk`.
* **Solução Implementada:** Blindagem via `get_object_or_404(Livro, pk=pk, organizacao=org_atual(request))`, retornando HTTP 404 para registros de outras organizações, e filtragem de querysets nos `ModelForm` (`EmprestimoForm`).

### 3. Autenticação Genérica e Falta de Controle de Acesso por Papel (RBAC) — ✅ Resolvido (Aulas 13/15/17)
* **Diagnóstico na P1:** Dependência do login nativo do Django Admin e ausência de distinção de papéis.
* **Solução Implementada:** Adição do campo `papel` (`admin` / `operador`) e propriedade `eh_admin` em `Perfil`, decorator `@papel_requerido('admin')` em `core/decorators.py`, tela própria de login/logout e restrição de séries temporais e exportação CSV apenas para administradores.

### 4. Interface Estritamente Server-Side sem API REST — ✅ Resolvido (Aula 13 + Aula 17)
* **Diagnóstico na P1:** A aplicação operava apenas com renderização HTML via templates DTL.
* **Solução Implementada:** Instalação do Django REST Framework (DRF), `LivroSerializer` (replicando a validação de ano futuro), `LeitorSerializer`, `EmprestimoSerializer`, endpoints CRUD isolados por tenant em `/api/` e `DashboardApi` (`/api/dashboard/`) reaproveitando `acervo/dashboard.py`.

### 5. Métricas Analíticas Básicas e Risco de Consultas N+1 — ✅ Resolvido (Aula 17)
* **Diagnóstico na P1:** A tela inicial fazia apenas contagens simples e não havia métricas analíticas nem proteção contra consultas N+1.
* **Solução Implementada:** Dashboard completo em `/dashboard/` com 4 métricas ORM (`aggregate`, `Count` com `filter=Q(...)`, `values` + `annotate`, `TruncMonth`), filtro por período validado (`PeriodoForm`), gráficos em Chart.js via `json_script`, índice em `Emprestimo.data_saida`, uso de `select_related('livro', 'leitor')`, exportação CSV sanitizada contra formula injection e testes automatizados com `assertNumQueries`.

---

> Todos os 5 débitos técnicos levantados após a P1 foram integralmente solucionados e validados por 16 testes automatizados.
