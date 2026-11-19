import datetime
from django import forms
from .models import Livro, Leitor, Emprestimo


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'ano', 'disponivel']
        labels = {
            'titulo': 'Título do Livro',
            'autor': 'Autor(a)',
            'ano': 'Ano de Publicação',
            'disponivel': 'Disponível para empréstimo/consulta',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: Dom Casmurro',
                'autocomplete': 'off',
            }),
            'autor': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: Machado de Assis',
                'autocomplete': 'off',
            }),
            'ano': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: 1899',
            }),
            'disponivel': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
            }),
        }

    def clean_ano(self):
        """
        Regra de negócio obrigatória (P1):
        O ano de publicação do livro não pode ser um ano futuro.
        """
        ano = self.cleaned_data.get('ano')
        ano_atual = datetime.date.today().year
        if ano is not None and ano > ano_atual:
            raise forms.ValidationError("O ano de publicação não pode ser superior ao ano atual.")
        return ano


class LeitorForm(forms.ModelForm):
    class Meta:
        model = Leitor
        fields = ['nome', 'email']
        labels = {
            'nome': 'Nome Completo',
            'email': 'E-mail',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Maria Silva'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'maria@exemplo.com'}),
        }


class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['livro', 'leitor', 'data_saida', 'devolvido_em']
        labels = {
            'livro': 'Livro',
            'leitor': 'Leitor',
            'data_saida': 'Data de Saída',
            'devolvido_em': 'Data de Devolução (opcional)',
        }
        widgets = {
            'livro': forms.Select(attrs={'class': 'form-select'}),
            'leitor': forms.Select(attrs={'class': 'form-select'}),
            'data_saida': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'devolvido_em': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }

    def __init__(self, *args, org=None, **kwargs):
        """
        Isolamento de Selects em formulários (Aula 14):
        Filtra os querysets de Livro e Leitor estritamente pela organização ativa.
        """
        super().__init__(*args, **kwargs)
        if org is not None:
            self.fields['livro'].queryset = Livro.objects.filter(organizacao=org).order_by('titulo')
            self.fields['leitor'].queryset = Leitor.objects.filter(organizacao=org).order_by('nome')
        else:
            self.fields['livro'].queryset = Livro.objects.none()
            self.fields['leitor'].queryset = Leitor.objects.none()


class PeriodoForm(forms.Form):
    """
    Filtro por Período Validado (Aula 17):
    Valida e converte datas da querystring (?inicio=YYYY-MM-DD&fim=YYYY-MM-DD),
    evitando erros 500 caso o usuário passe valores malformados na URL.
    """
    inicio = forms.DateField(
        required=False,
        label='Início',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'})
    )
    fim = forms.DateField(
        required=False,
        label='Fim',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'})
    )


def filtrar_periodo(request, qs):
    """
    Aplica filtro de data_saida em um queryset de Emprestimo de forma segura via PeriodoForm.
    """
    form = PeriodoForm(request.GET)
    if form.is_valid():
        if form.cleaned_data.get('inicio'):
            qs = qs.filter(data_saida__gte=form.cleaned_data['inicio'])
        if form.cleaned_data.get('fim'):
            qs = qs.filter(data_saida__lte=form.cleaned_data['fim'])
    return qs
