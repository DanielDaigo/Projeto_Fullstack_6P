from django.shortcuts import render, redirect
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