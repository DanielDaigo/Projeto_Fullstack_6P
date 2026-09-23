from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('livros/', views.lista_livros, name='lista'),
    path('livros/novo/', views.novo_livro, name='novo_livro'),
]