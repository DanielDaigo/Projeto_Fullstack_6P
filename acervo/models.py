from django.db import models
from django.utils import timezone
from core.models import DaOrganizacao


class Livro(DaOrganizacao):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    ano = models.IntegerField()
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo


class Leitor(DaOrganizacao):
    nome = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Leitor"
        verbose_name_plural = "Leitores"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Emprestimo(DaOrganizacao):
    livro = models.ForeignKey(
        Livro,
        on_delete=models.PROTECT,
        related_name='emprestimos',
        verbose_name="Livro"
    )
    leitor = models.ForeignKey(
        Leitor,
        on_delete=models.PROTECT,
        related_name='emprestimos',
        verbose_name="Leitor"
    )
    data_saida = models.DateField(default=timezone.localdate, verbose_name="Data de Saída")
    devolvido_em = models.DateField(null=True, blank=True, verbose_name="Devolvido em")

    class Meta:
        verbose_name = "Empréstimo"
        verbose_name_plural = "Empréstimos"
        ordering = ['-data_saida', '-id']
        indexes = [
            models.Index(fields=['data_saida']),
        ]

    @property
    def em_aberto(self):
        return self.devolvido_em is None

    def __str__(self):
        return f"{self.livro.titulo} → {self.leitor.nome} ({self.data_saida})"
