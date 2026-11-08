from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import Livro
from .forms import LivroForm

def org_atual(request):
    """
    Recupera a organização do usuário logado através do seu Perfil (Aula 14).
    Garante que toda consulta e operação no sistema seja delimitada a esta organização.
    """
    if not hasattr(request.user, 'perfil'):
        raise PermissionDenied("O usuário conectado não possui um Perfil vinculado a uma Organização.")
    return request.user.perfil.organizacao

@login_required
def home(request):
    org = org_atual(request)
    total_livros = Livro.objects.filter(organizacao=org).count()
    livros_disponiveis = Livro.objects.filter(organizacao=org, disponivel=True).count()
    ultimos_livros = Livro.objects.filter(organizacao=org).order_by('-id')[:5]
    context = {
        'total_livros': total_livros,
        'livros_disponiveis': livros_disponiveis,
        'livros_indisponiveis': total_livros - livros_disponiveis,
        'ultimos_livros': ultimos_livros,
        'organizacao': org,
    }
    return render(request, 'acervo/home.html', context)

@login_required
def lista_livros(request):
    """
    Feature 1 (P1) + Isolamento Multi-tenant (Aula 14):
    - Filtra estritamente pelo tenant atual (organizacao=org)
    - Captura 'q' (busca textual) e 'status' (disponibilidade) via request.GET
    - Utiliza icontains e objetos Q para busca simultânea em título OU autor
    - Permite combinar busca textual com filtro de status de forma aditiva
    """
    org = org_atual(request)
    termo_busca = request.GET.get('q', '').strip()
    filtro_status = request.GET.get('status', '').strip()

    # REGRA DE OURO: toda consulta parte de filter(organizacao=org)
    livros = Livro.objects.filter(organizacao=org)

    # Busca textual simultânea em título OU autor usando Q objects
    if termo_busca:
        livros = livros.filter(
            Q(titulo__icontains=termo_busca) | Q(autor__icontains=termo_busca)
        )

    # Filtro por status de disponibilidade
    if filtro_status == 'disponivel':
        livros = livros.filter(disponivel=True)
    elif filtro_status == 'emprestado':
        livros = livros.filter(disponivel=False)

    livros = livros.order_by('titulo')

    return render(
        request, 
        'acervo/lista.html', 
        {
            'livros': livros,
            'termo_busca': termo_busca,
            'filtro_status': filtro_status,
            'organizacao': org,
        }
    )

@login_required
def novo_livro(request):
    """
    Criação com isolamento (Aula 14):
    A organização NUNCA vem do formulário (prevenindo tampering).
    É injetada via servidor com form.save(commit=False).
    """
    org = org_atual(request)
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.organizacao = org
            livro.save()
            form.save_m2m()
            messages.success(request, f'Livro "{livro.titulo}" cadastrado com sucesso!')
            return redirect('lista')
    else:
        form = LivroForm()
    
    return render(request, 'acervo/form.html', {
        'form': form,
        'titulo_pagina': 'Cadastrar Novo Livro',
        'botao_texto': 'Salvar Livro',
        'organizacao': org,
    })

@login_required
def editar_livro(request, pk):
    """
    Edição com proteção contra IDOR (Aula 14):
    get_object_or_404 filtra tanto por pk quanto por organizacao.
    Tentar acessar livro de outra organização resulta em HTTP 404.
    """
    org = org_atual(request)
    livro = get_object_or_404(Livro, pk=pk, organizacao=org)
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            messages.success(request, f'Livro "{livro.titulo}" atualizado com sucesso!')
            return redirect('lista')
    else:
        form = LivroForm(instance=livro)
    
    return render(request, 'acervo/form.html', {
        'form': form,
        'livro': livro,
        'titulo_pagina': f'Editar: {livro.titulo}',
        'botao_texto': 'Salvar Alterações',
        'organizacao': org,
    })

@login_required
def excluir_livro(request, pk):
    """
    Exclusão com proteção contra IDOR (Aula 14):
    get_object_or_404 filtra por pk e organizacao.
    """
    org = org_atual(request)
    livro = get_object_or_404(Livro, pk=pk, organizacao=org)
    if request.method == 'POST':
        titulo = livro.titulo
        livro.delete()
        messages.success(request, f'Livro "{titulo}" excluído com sucesso!')
        return redirect('lista')
    
    return render(request, 'acervo/confirmar_exclusao.html', {'livro': livro, 'organizacao': org})
