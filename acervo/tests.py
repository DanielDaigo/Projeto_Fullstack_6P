import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Organizacao, Perfil
from acervo.models import Livro, Leitor, Emprestimo


class IsolamentoOrganizacaoTest(TestCase):
    """
    Roteiro de Testes da Aula 14:
    Valida o isolamento de dados entre organizações (Multi-tenancy).
    """

    def setUp(self):
        self.org_a = Organizacao.objects.create(nome="Biblioteca Central")
        self.org_b = Organizacao.objects.create(nome="Biblioteca Universitária")

        self.user_a = User.objects.create_user(username="usuario_a", password="password123")
        Perfil.objects.create(usuario=self.user_a, organizacao=self.org_a, papel='operador')

        self.user_b = User.objects.create_user(username="usuario_b", password="password123")
        Perfil.objects.create(usuario=self.user_b, organizacao=self.org_b, papel='operador')

        self.livro_a = Livro.objects.create(
            titulo="Livro Exclusivo A",
            autor="Autor A",
            ano=2020,
            disponivel=True,
            organizacao=self.org_a
        )
        self.livro_b = Livro.objects.create(
            titulo="Livro Exclusivo B",
            autor="Autor B",
            ano=2021,
            disponivel=True,
            organizacao=self.org_b
        )

        self.client_a = Client()
        self.client_a.login(username="usuario_a", password="password123")

        self.client_b = Client()
        self.client_b.login(username="usuario_b", password="password123")

    def test_usuario_a_ve_somente_livros_da_organizacao_a(self):
        response = self.client_a.get(reverse('lista'))
        self.assertEqual(response.status_code, 200)
        livros_listados = response.context['livros']
        self.assertIn(self.livro_a, livros_listados)
        self.assertNotIn(self.livro_b, livros_listados)

    def test_usuario_a_tenta_editar_livro_da_organizacao_b_recebe_404(self):
        url_editar_b = reverse('editar_livro', kwargs={'pk': self.livro_b.pk})
        response = self.client_a.get(url_editar_b)
        self.assertEqual(response.status_code, 404)

    def test_usuario_a_cria_livro_gravado_com_sua_organizacao(self):
        url_novo = reverse('novo_livro')
        dados = {
            'titulo': 'Novo Livro Central',
            'autor': 'Machado de Assis',
            'ano': 1899,
            'disponivel': True
        }
        response = self.client_a.post(url_novo, dados)
        self.assertEqual(response.status_code, 302)
        novo_livro = Livro.objects.get(titulo='Novo Livro Central')
        self.assertEqual(novo_livro.organizacao, self.org_a)

    def test_usuario_a_tenta_excluir_livro_da_organizacao_b_recebe_404(self):
        url_excluir_b = reverse('excluir_livro', kwargs={'pk': self.livro_b.pk})
        response_get = self.client_a.get(url_excluir_b)
        self.assertEqual(response_get.status_code, 404)

        response_post = self.client_a.post(url_excluir_b)
        self.assertEqual(response_post.status_code, 404)
        self.assertTrue(Livro.objects.filter(pk=self.livro_b.pk).exists())

    def test_usuario_nao_autenticado_redirecionado_para_login(self):
        client_anonimo = Client()
        response = client_anonimo.get(reverse('lista'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_unicidade_por_organizacao_permite_outro_tenant_e_bloqueia_duplicado_no_mesmo(self):
        """Aula 14, Slides 16 e 18: Org A pode cadastrar o mesmo livro da Org B, mas não duplicar o próprio."""
        url_novo = reverse('novo_livro')
        # 1. Org A cadastra mesmo título e autor já existente na Org B -> Permitido!
        resp_ok = self.client_a.post(url_novo, {
            'titulo': self.livro_b.titulo,
            'autor': self.livro_b.autor,
            'ano': 2021,
            'disponivel': True,
        })
        self.assertEqual(resp_ok.status_code, 302)
        self.assertEqual(
            Livro.objects.filter(organizacao=self.org_a, titulo=self.livro_b.titulo).count(), 1
        )

        # 2. Org A tenta cadastrar novamente o mesmo livro -> Erro de validação no form (sem IntegrityError)
        resp_dup = self.client_a.post(url_novo, {
            'titulo': self.livro_b.titulo,
            'autor': self.livro_b.autor,
            'ano': 2021,
            'disponivel': True,
        })
        self.assertEqual(resp_dup.status_code, 200)
        self.assertFalse(resp_dup.context['form'].is_valid())

    def test_selects_do_emprestimo_form_isolados_por_organizacao(self):
        """Aula 14, Slides 15 e 18: Selects do formulário mostram apenas opções da organização A."""
        from acervo.forms import EmprestimoForm
        leitor_a = Leitor.objects.create(nome="Leitor A", organizacao=self.org_a)
        leitor_b = Leitor.objects.create(nome="Leitor B", organizacao=self.org_b)

        form = EmprestimoForm(org=self.org_a)
        self.assertIn(self.livro_a, form.fields['livro'].queryset)
        self.assertNotIn(self.livro_b, form.fields['livro'].queryset)
        self.assertIn(leitor_a, form.fields['leitor'].queryset)
        self.assertNotIn(leitor_b, form.fields['leitor'].queryset)

    def test_validacao_ano_futuro_centralizada_no_model(self):
        """Aula 13, Slide 16: Regra de negócio centralizada no Model vale também fora dos forms."""
        from django.core.exceptions import ValidationError
        livro_futuro = Livro(
            titulo="Livro do Futuro",
            autor="Autor",
            ano=datetime.date.today().year + 2,
            organizacao=self.org_a,
        )
        with self.assertRaises(ValidationError):
            livro_futuro.full_clean()


class DashboardTest(TestCase):
    """
    Testes das métricas, filtros, papéis e exportação CSV do Dashboard (Aula 17, Slide 37).
    Dados conhecidos criados no setUp: 3 empréstimos na Org A, 5 empréstimos na Org B.
    """

    def setUp(self):
        self.org_a = Organizacao.objects.create(nome="Biblioteca Central")
        self.org_b = Organizacao.objects.create(nome="Biblioteca do Bairro")
        self.org_vazia = Organizacao.objects.create(nome="Biblioteca Nova")

        self.admin_a = User.objects.create_user(username="admin_a", password="password123")
        Perfil.objects.create(usuario=self.admin_a, organizacao=self.org_a, papel='admin')

        self.operador_a = User.objects.create_user(username="operador_a", password="password123")
        Perfil.objects.create(usuario=self.operador_a, organizacao=self.org_a, papel='operador')

        self.user_vazia = User.objects.create_user(username="user_vazia", password="password123")
        Perfil.objects.create(usuario=self.user_vazia, organizacao=self.org_vazia, papel='admin')

        self.livro_a1 = Livro.objects.create(titulo="Dom Casmurro", autor="Machado", ano=1899, organizacao=self.org_a)
        self.livro_a2 = Livro.objects.create(titulo="=FormulaMaliciosa", autor="Teste", ano=2020, organizacao=self.org_a)
        self.leitor_a = Leitor.objects.create(nome="Ana", email="ana@ex.com", organizacao=self.org_a)

        # 3 empréstimos na Org A (2 em agosto/2026, 1 em outubro/2026)
        Emprestimo.objects.create(
            organizacao=self.org_a, livro=self.livro_a1, leitor=self.leitor_a,
            data_saida=datetime.date(2026, 8, 10), devolvido_em=datetime.date(2026, 8, 20)
        )
        Emprestimo.objects.create(
            organizacao=self.org_a, livro=self.livro_a1, leitor=self.leitor_a,
            data_saida=datetime.date(2026, 8, 25), devolvido_em=None
        )
        Emprestimo.objects.create(
            organizacao=self.org_a, livro=self.livro_a2, leitor=self.leitor_a,
            data_saida=datetime.date(2026, 10, 5), devolvido_em=None
        )

        # 5 empréstimos na Org B
        livro_b = Livro.objects.create(titulo="O Cortiço", autor="Aluísio", ano=1890, organizacao=self.org_b)
        leitor_b = Leitor.objects.create(nome="Bruno", email="bruno@ex.com", organizacao=self.org_b)
        for dia in range(1, 6):
            Emprestimo.objects.create(
                organizacao=self.org_b, livro=livro_b, leitor=leitor_b,
                data_saida=datetime.date(2026, 8, dia), devolvido_em=None
            )

    def test_total_da_organizacao(self):
        self.client.force_login(self.admin_a)
        r = self.client.get(reverse('dashboard'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['kpis']['total'], 3)
        self.assertEqual(r.context['kpis']['abertos'], 2)
        self.assertEqual(r.context['kpis']['leitores'], 1)
        self.assertEqual(r.context['ranking'][0]['livro__titulo'], 'Dom Casmurro')
        self.assertEqual(r.context['ranking'][0]['total'], 2)

    def test_filtro_por_periodo(self):
        self.client.force_login(self.admin_a)
        r = self.client.get(reverse('dashboard') + '?inicio=2026-08-01&fim=2026-08-31')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['kpis']['total'], 2)
        self.assertEqual(len(r.context['por_mes']), 1)
        self.assertEqual(r.context['por_mes'][0]['mes'], '08/2026')

    def test_data_invalida_na_url_nao_quebra_dashboard(self):
        self.client.force_login(self.admin_a)
        r = self.client.get(reverse('dashboard') + '?inicio=abc&fim=invalida')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['kpis']['total'], 3)

    def test_dashboard_vazio_sem_erro(self):
        self.client.force_login(self.user_vazia)
        r = self.client.get(reverse('dashboard'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['kpis']['total'], 0)
        self.assertEqual(r.context['ranking'], [])

    def test_operador_nao_ve_series_e_nao_pode_exportar_csv(self):
        self.client.force_login(self.operador_a)
        r_dash = self.client.get(reverse('dashboard'))
        self.assertEqual(r_dash.status_code, 200)
        self.assertFalse(r_dash.context['mostra_series'])
        self.assertEqual(r_dash.context['por_mes'], [])

        r_csv = self.client.get(reverse('exportar_csv'))
        self.assertEqual(r_csv.status_code, 403)

    def test_admin_exporta_csv_isolado_e_sanitizado(self):
        self.client.force_login(self.admin_a)
        r = self.client.get(reverse('exportar_csv'))
        self.assertEqual(r.status_code, 200)
        self.assertIn('text/csv', r['Content-Type'])
        conteudo = r.content.decode('utf-8-sig')
        self.assertIn('Dom Casmurro', conteudo)
        self.assertIn("'=FormulaMaliciosa", conteudo)  # Protegido contra formula injection
        self.assertNotIn('O Cortiço', conteudo)  # Não vaza dados da Org B


class ConsultasNPlusOneTest(TestCase):
    """
    Teste de desempenho com assertNumQueries (Aula 17, Slide 31):
    Garante que o uso de select_related('livro', 'leitor') executa apenas 1 consulta SQL.
    """

    def setUp(self):
        self.org = Organizacao.objects.create(nome="Biblioteca Performance")
        leitor = Leitor.objects.create(nome="Leitor Perf", organizacao=self.org)
        for i in range(5):
            livro = Livro.objects.create(titulo=f"Livro {i}", autor="Autor", ano=2020, organizacao=self.org)
            Emprestimo.objects.create(organizacao=self.org, livro=livro, leitor=leitor)

    def test_select_related_executa_apenas_uma_consulta(self):
        with self.assertNumQueries(1):
            titulos = [
                f"{e.livro.titulo} - {e.leitor.nome}"
                for e in Emprestimo.objects.filter(organizacao=self.org).select_related('livro', 'leitor')
            ]
        self.assertEqual(len(titulos), 5)


class ApiRestTest(TestCase):
    """
    Testes da API REST com DRF (Aula 13 + Aula 17 Slide 35).
    """

    def setUp(self):
        self.org_a = Organizacao.objects.create(nome="Org API A")
        self.org_b = Organizacao.objects.create(nome="Org API B")

        self.user_a = User.objects.create_user(username="api_a", password="password123")
        Perfil.objects.create(usuario=self.user_a, organizacao=self.org_a, papel='admin')

        self.livro_a = Livro.objects.create(titulo="Livro API A", autor="Autor A", ano=2022, organizacao=self.org_a)
        self.livro_b = Livro.objects.create(titulo="Livro API B", autor="Autor B", ano=2022, organizacao=self.org_b)
        leitor_a = Leitor.objects.create(nome="Leitor API", organizacao=self.org_a)
        Emprestimo.objects.create(organizacao=self.org_a, livro=self.livro_a, leitor=leitor_a)

    def test_api_exige_autenticacao(self):
        r = self.client.get(reverse('api_livro_list'))
        self.assertEqual(r.status_code, 403)

    def test_api_livros_isolada_por_organizacao(self):
        self.client.force_login(self.user_a)
        r = self.client.get(reverse('api_livro_list'))
        self.assertEqual(r.status_code, 200)
        titulos = [item['titulo'] for item in r.json()]
        self.assertIn('Livro API A', titulos)
        self.assertNotIn('Livro API B', titulos)

        r_detail_b = self.client.get(reverse('api_livro_detail', kwargs={'pk': self.livro_b.pk}))
        self.assertEqual(r_detail_b.status_code, 404)

    def test_api_livro_valida_ano_futuro(self):
        self.client.force_login(self.user_a)
        ano_futuro = datetime.date.today().year + 5
        r = self.client.post(
            reverse('api_livro_list'),
            data={'titulo': 'Livro Futuro', 'autor': 'Autor', 'ano': ano_futuro, 'disponivel': True},
            content_type='application/json',
        )
        self.assertEqual(r.status_code, 400)
        self.assertIn('ano', r.json())

    def test_api_dashboard_retorna_metricas_json(self):
        self.client.force_login(self.user_a)
        r = self.client.get(reverse('api_dashboard'))
        self.assertEqual(r.status_code, 200)
        dados = r.json()
        self.assertEqual(dados['organizacao'], 'Org API A')
        self.assertEqual(dados['kpis']['total'], 1)
        self.assertEqual(len(dados['ranking']), 1)
