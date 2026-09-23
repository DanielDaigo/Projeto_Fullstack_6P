from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Livro
from .forms import LivroForm

def home(request):
    total_livros = Livro.objects.count()
    livros_disponiveis = Livro.objects.filter(disponivel=True).count()
    ultimos_livros = Livro.objects.order_by('-id')[:5]
    context = {
        'total_livros': total_livros,
        'livros_disponiveis': livros_disponiveis,
        'livros_indisponiveis': total_livros - livros_disponiveis,
        'ultimos_livros': ultimos_livros,
    }
    return render(request, 'acervo/home.html', context)

def lista_livros(request):
    """
    Feature 1 (P1): Busca e Filtro na Listagem de Livros
    - Captura 'q' (busca textual) e 'status' (disponibilidade) via request.GET
    - Utiliza icontains e objetos Q para busca simultânea em título OU autor
    - Permite combinar busca textual com filtro de status de forma aditiva
    """
    termo_busca = request.GET.get('q', '').strip()
    filtro_status = request.GET.get('status', '').strip()

    livros = Livro.objects.all()

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
        }
    )

def novo_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            livro = form.save()
            messages.success(request, f'Livro "{livro.titulo}" cadastrado com sucesso!')
            return redirect('lista')
    else:
        form = LivroForm()
    
    return render(request, 'acervo/form.html', {
        'form': form,
        'titulo_pagina': 'Cadastrar Novo Livro',
        'botao_texto': 'Salvar Livro',
    })

def editar_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
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
    })

def excluir_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        titulo = livro.titulo
        livro.delete()
        messages.success(request, f'Livro "{titulo}" excluído com sucesso!')
        return redirect('lista')
    
    return render(request, 'acervo/confirmar_exclusao.html', {'livro': livro})