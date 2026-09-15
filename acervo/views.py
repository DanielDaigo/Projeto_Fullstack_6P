from django.shortcuts import render, redirect
from .models import Livro
from .forms import LivroForm

def lista_livros(request):
    livros = Livro.objects.all()
    return render(
        request, 
        'acervo/lista.html', 
        {'livros': livros}
    )

def novo_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()          # grava no banco PostgreSQL
            return redirect('lista')  # redireciona de volta para a lista
    else:
        form = LivroForm()       # requisição GET: formulário em branco
    
    return render(request, 'acervo/form.html', {'form': form})