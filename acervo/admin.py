from django.contrib import admin
from .models import Livro

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'ano', 'disponivel', 'organizacao')
    list_filter = ('organizacao', 'disponivel')
    search_fields = ('titulo', 'autor')
    ordering = ('titulo',)
