from django.contrib import admin
from .models import Livro, Leitor, Emprestimo


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'ano', 'disponivel', 'organizacao')
    list_filter = ('organizacao', 'disponivel')
    search_fields = ('titulo', 'autor')
    ordering = ('titulo',)


@admin.register(Leitor)
class LeitorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'organizacao', 'criado_em')
    list_filter = ('organizacao',)
    search_fields = ('nome', 'email')
    ordering = ('nome',)


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('livro', 'leitor', 'data_saida', 'devolvido_em', 'organizacao')
    list_filter = ('organizacao', 'data_saida')
    list_select_related = ('livro', 'leitor', 'organizacao')
    search_fields = ('livro__titulo', 'leitor__nome')
    date_hierarchy = 'data_saida'
