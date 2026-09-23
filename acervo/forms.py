import datetime
from django import forms
from .models import Livro

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