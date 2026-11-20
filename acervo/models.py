import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from core.models import DaOrganizacao


def validar_ano_nao_futuro(valor):
    """
    Regra de negócio centralizada (P1 / Aula 13, Slide 16):
    Mantida em um único lugar para valer no Model, Django Admin, ModelForm e DRF Serializer.
    """
    ano_atual = datetime.date.today().year
    if valor is not None and valor > ano_atual:
        raise ValidationError("O ano de publicação não pode ser superior ao ano atual.")


class Livro(DaOrganizacao):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    ano = models.IntegerField(validators=[validar_ano_nao_futuro])
    disponivel = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['organizacao', 'titulo', 'autor'],
                name='livro_unico_por_org',
            ),
        ]

    def clean(self):
        super().clean()
        validar_ano_nao_futuro(self.ano)

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
