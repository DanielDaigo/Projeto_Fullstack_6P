from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Organizacao, Perfil
from acervo.models import Livro

class IsolamentoOrganizacaoTest(TestCase):
    """
    Roteiro de Testes da Aula 14:
    Valida o isolamento de dados entre organizações (Multi-tenancy).
    Dois usuários, duas organizações, quatro verificações essenciais.
    """

    def setUp(self):
        # 1. Criação das duas organizações
        self.org_a = Organizacao.objects.create(nome="Biblioteca Central")
        self.org_b = Organizacao.objects.create(nome="Biblioteca Universitária")

        # 2. Criação dos dois usuários com senhas e perfis
        self.user_a = User.objects.create_user(username="usuario_a", password="password123")
        Perfil.objects.create(usuario=self.user_a, organizacao=self.org_a)

        self.user_b = User.objects.create_user(username="usuario_b", password="password123")
        Perfil.objects.create(usuario=self.user_b, organizacao=self.org_b)

        # 3. Criação de livros para cada organização
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

        # 4. Clients HTTP de teste
        self.client_a = Client()
        self.client_a.login(username="usuario_a", password="password123")

        self.client_b = Client()
        self.client_b.login(username="usuario_b", password="password123")

    def test_usuario_a_ve_somente_livros_da_organizacao_a(self):
        """Cenário 1: Usuário A abre a lista de livros e vê apenas os da organização A."""
        response = self.client_a.get(reverse('lista'))
        self.assertEqual(response.status_code, 200)
        livros_listados = response.context['livros']
        self.assertIn(self.livro_a, livros_listados)
        self.assertNotIn(self.livro_b, livros_listados)

    def test_usuario_a_tenta_editar_livro_da_organizacao_b_recebe_404(self):
        """Cenário 2: Usuário A abre /livros/ID-da-B/editar/ e recebe 404 (Blindagem IDOR)."""
        url_editar_b = reverse('editar_livro', kwargs={'pk': self.livro_b.pk})
        response = self.client_a.get(url_editar_b)
        self.assertEqual(response.status_code, 404)

    def test_usuario_a_cria_livro_gravado_com_sua_organizacao(self):
        """Cenário 3: Usuário A cria um livro e o sistema grava com a organização A no servidor."""
        url_novo = reverse('novo_livro')
        dados = {
            'titulo': 'Novo Livro Central',
            'autor': 'Machado de Assis',
            'ano': 1899,
            'disponivel': True
        }
        response = self.client_a.post(url_novo, dados)
        self.assertEqual(response.status_code, 302) # Redireciona para lista
        novo_livro = Livro.objects.get(titulo='Novo Livro Central')
        self.assertEqual(novo_livro.organizacao, self.org_a)

    def test_usuario_a_tenta_excluir_livro_da_organizacao_b_recebe_404(self):
        """Cenário 4: Usuário A tenta abrir ou submeter /livros/ID-da-B/excluir/ e recebe 404."""
        url_excluir_b = reverse('excluir_livro', kwargs={'pk': self.livro_b.pk})
        response_get = self.client_a.get(url_excluir_b)
        self.assertEqual(response_get.status_code, 404)

        response_post = self.client_a.post(url_excluir_b)
        self.assertEqual(response_post.status_code, 404)
        # Garante que o livro B não foi apagado
        self.assertTrue(Livro.objects.filter(pk=self.livro_b.pk).exists())

    def test_usuario_nao_autenticado_redirecionado_para_login(self):
        """Garante que rotas de negócio exigem autenticação."""
        client_anonimo = Client()
        response = client_anonimo.get(reverse('lista'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)
