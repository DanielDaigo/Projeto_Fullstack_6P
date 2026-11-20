import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.http import HttpResponse
from core.decorators import papel_requerido
from .models import Livro, Emprestimo
from .forms import LivroForm, EmprestimoForm, PeriodoForm
from .dashboard import base_emprestimos, calcular_metricas_dashboard


def org_atual(request):
    """
    Recupera a organização do usuário logado através do seu Perfil (Aula 14).
    Garante que toda consulta e operação no sistema seja delimitada a esta organização.
    """
    if not hasattr(request.user, 'perfil'):
        raise PermissionDenied("O usuário conectado não possui um Perfil vinculado a uma Organização.")
    return request.user.perfil.organizacao


def _sanitizar_celula_csv(valor):
    """
    Proteção contra CSV Formula Injection (Aula 17, Slide 34):
    Prefixa com apóstrofo valores textuais que comecem com =, +, - ou @.
    """
    texto = str(valor) if valor is not None else ''
    if texto and texto[0] in ('=', '+', '-', '@'):
        return f"'{texto}"
    return texto


@login_required
def home(request):
    org = org_atual(request)
    resumo = Livro.objects.filter(organizacao=org).aggregate(
        total=Count('id'),
        disponiveis=Count('id', filter=Q(disponivel=True)),
    )
    total_livros = resumo['total']
    livros_disponiveis = resumo['disponiveis']
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
def dashboard(request):
    """
    Dashboard Gerencial (Aula 17):
    - Base filtrada por organização e período validado (PeriodoForm)
    - 4 métricas ORM: KPIs (aggregate), Ranking (values+annotate), Série Mensal (TruncMonth) e Distribuição
    - Controle por papel: Administrador vê séries e exportação CSV; Operador vê KPIs e Ranking
    """
    org = org_atual(request)
    mostra_series = request.user.perfil.eh_admin
    metricas = calcular_metricas_dashboard(request, org, incluir_series=mostra_series)

    contexto = {
        **metricas,
        'form': PeriodoForm(request.GET),
        'mostra_series': mostra_series,
        'organizacao': org,
    }
    return render(request, 'acervo/dashboard.html', contexto)


@papel_requerido('admin')
def exportar_csv(request):
    """
    Exportação de relatório em CSV (Aula 17):
    - Restrito ao papel Administrador (@papel_requerido('admin'))
    - Reutiliza exatamente a mesma base filtrada (organização + período)
    - Usa select_related('livro', 'leitor') para evitar N+1
    - Protege células contra CSV Formula Injection (= + - @)
    """
    org = org_atual(request)
    qs = base_emprestimos(request, org).select_related('livro', 'leitor')

    resp = HttpResponse(content_type='text/csv; charset=utf-8')
    resp['Content-Disposition'] = 'attachment; filename="emprestimos.csv"'
    resp.write('\ufeff')  # BOM UTF-8 para abertura correta de acentos no Excel

    writer = csv.writer(resp)
    writer.writerow(['Livro', 'Leitor', 'Saída', 'Devolvido em', 'Status'])
    for e in qs:
        status = 'Em aberto' if e.devolvido_em is None else 'Devolvido'
        writer.writerow([
            _sanitizar_celula_csv(e.livro.titulo),
            _sanitizar_celula_csv(e.leitor.nome),
            e.data_saida.strftime('%Y-%m-%d'),
            e.devolvido_em.strftime('%Y-%m-%d') if e.devolvido_em else '',
            status,
        ])
    return resp


@login_required
def lista_emprestimos(request):
    """
    Listagem de empréstimos da organização usando select_related('livro', 'leitor')
    para evitar o problema N+1 (Aula 17, Slides 19-32).
    """
    org = org_atual(request)
    emprestimos = (
        Emprestimo.objects.filter(organizacao=org)
        .select_related('livro', 'leitor')
        .order_by('-data_saida', '-id')
    )
    return render(request, 'acervo/emprestimos_lista.html', {
        'emprestimos': emprestimos,
        'organizacao': org,
    })


@login_required
def novo_emprestimo(request):
    org = org_atual(request)
    if request.method == 'POST':
        form = EmprestimoForm(request.POST, org=org)
        if form.is_valid():
            emprestimo = form.save(commit=False)
            emprestimo.organizacao = org
            emprestimo.save()
            messages.success(request, f'Empréstimo de "{emprestimo.livro.titulo}" registrado com sucesso!')
            return redirect('lista_emprestimos')
    else:
        form = EmprestimoForm(org=org)

    return render(request, 'acervo/form.html', {
        'form': form,
        'titulo_pagina': 'Registrar Novo Empréstimo',
        'botao_texto': 'Salvar Empréstimo',
        'organizacao': org,
    })


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
        form = LivroForm(request.POST, org=org)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.organizacao = org
            livro.save()
            form.save_m2m()
            messages.success(request, f'Livro "{livro.titulo}" cadastrado com sucesso!')
            return redirect('lista')
    else:
        form = LivroForm(org=org)

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
        form = LivroForm(request.POST, instance=livro, org=org)
        if form.is_valid():
            form.save()
            messages.success(request, f'Livro "{livro.titulo}" atualizado com sucesso!')
            return redirect('lista')
    else:
        form = LivroForm(instance=livro, org=org)

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
