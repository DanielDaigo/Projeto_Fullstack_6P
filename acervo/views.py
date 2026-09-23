from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
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
    livros = Livro.objects.all().order_by('titulo')
    return render(
        request, 
        'acervo/lista.html', 
        {'livros': livros}
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