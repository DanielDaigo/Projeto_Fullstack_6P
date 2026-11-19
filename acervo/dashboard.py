from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from .models import Emprestimo, Livro
from .forms import filtrar_periodo


def base_emprestimos(request, org):
    """
    Base única filtrada por organização e período validado.
    Todas as métricas do dashboard derivam desta base.
    """
    qs = Emprestimo.objects.filter(organizacao=org)
    return filtrar_periodo(request, qs)


def calcular_metricas_dashboard(request, org, incluir_series=True):
    """
    Calcula as 4 métricas obrigatórias do Dashboard (Aula 17):
    1. Total (KPIs) via aggregate + Count com filter=Q(...)
    2. Ranking (Top 5 livros mais emprestados) via values + annotate + order_by
    3. Série temporal (empréstimos por mês) via TruncMonth + order_by
    4. Distribuição (empréstimos em aberto vs devolvidos + status do acervo)
    """
    base = base_emprestimos(request, org)

    # 1. KPIs em uma única consulta SQL
    kpis = base.aggregate(
        total=Count('id'),
        leitores=Count('leitor', distinct=True),
        abertos=Count('id', filter=Q(devolvido_em__isnull=True)),
        devolvidos=Count('id', filter=Q(devolvido_em__isnull=False)),
    )

    # 2. Ranking dos 5 livros mais emprestados
    ranking = list(
        base.values('livro__titulo')
        .annotate(total=Count('id'))
        .order_by('-total', 'livro__titulo')[:5]
    )

    # 3. Série temporal agrupada por mês (somente se permitido pelo papel)
    por_mes = []
    if incluir_series:
        por_mes_qs = (
            base.annotate(mes=TruncMonth('data_saida'))
            .values('mes')
            .annotate(total=Count('id'))
            .order_by('mes')
        )
        por_mes = [
            {
                'mes': r['mes'].strftime('%m/%Y'),
                'total': r['total'],
            }
            for r in por_mes_qs
            if r['mes'] is not None
        ]

    # 4. Distribuição (status dos empréstimos + acervo da organização)
    acervo_kpis = Livro.objects.filter(organizacao=org).aggregate(
        total_livros=Count('id'),
        disponiveis=Count('id', filter=Q(disponivel=True)),
        indisponiveis=Count('id', filter=Q(disponivel=False)),
    )
    distribuicao = [
        {'status': 'Em aberto', 'total': kpis['abertos']},
        {'status': 'Devolvidos', 'total': kpis['devolvidos']},
    ]

    return {
        'kpis': kpis,
        'acervo_kpis': acervo_kpis,
        'ranking': ranking,
        'por_mes': por_mes,
        'distribuicao': distribuicao,
    }
