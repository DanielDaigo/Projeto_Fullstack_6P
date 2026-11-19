from django.contrib import admin
from .models import Organizacao, Perfil


@admin.register(Organizacao)
class OrganizacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'criada_em')
    search_fields = ('nome',)
    ordering = ('nome',)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'organizacao', 'papel')
    list_filter = ('organizacao', 'papel')
    search_fields = ('usuario__username', 'usuario__email', 'organizacao__nome')
