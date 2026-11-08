from django.db import models
from django.contrib.auth.models import User

class Organizacao(models.Model):
    nome = models.CharField(max_length=120)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Organização"
        verbose_name_plural = "Organizações"

    def __str__(self):
        return self.nome


class DaOrganizacao(models.Model):
    organizacao = models.ForeignKey(
        'core.Organizacao',
        on_delete=models.PROTECT,
        verbose_name="Organização"
    )

    class Meta:
        abstract = True


class Perfil(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
        verbose_name="Usuário"
    )
    organizacao = models.ForeignKey(
        Organizacao,
        on_delete=models.PROTECT,
        related_name='perfis',
        verbose_name="Organização"
    )

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self):
        return f"{self.usuario.username} ({self.organizacao.nome})"
