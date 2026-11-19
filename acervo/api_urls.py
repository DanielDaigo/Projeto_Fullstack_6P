from django.urls import path
from .api_views import (
    LivroListCreate,
    LivroDetail,
    LeitorListCreate,
    LeitorDetail,
    EmprestimoListCreate,
    EmprestimoDetail,
    DashboardApi,
)

urlpatterns = [
    path('livros/', LivroListCreate.as_view(), name='api_livro_list'),
    path('livros/<int:pk>/', LivroDetail.as_view(), name='api_livro_detail'),
    path('leitores/', LeitorListCreate.as_view(), name='api_leitor_list'),
    path('leitores/<int:pk>/', LeitorDetail.as_view(), name='api_leitor_detail'),
    path('emprestimos/', EmprestimoListCreate.as_view(), name='api_emprestimo_list'),
    path('emprestimos/<int:pk>/', EmprestimoDetail.as_view(), name='api_emprestimo_detail'),
    path('dashboard/', DashboardApi.as_view(), name='api_dashboard'),
]
