import datetime
from rest_framework import serializers
from .models import Livro, Leitor, Emprestimo


class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = ['id', 'titulo', 'autor', 'ano', 'disponivel']

    def validate_ano(self, value):
        """
        Regra de negócio da P1 aplicada também na API REST (Aula 13, Slide 16):
        O ano de publicação não pode ser superior ao ano atual.
        """
        ano_atual = datetime.date.today().year
        if value > ano_atual:
            raise serializers.ValidationError(
                "O ano de publicação não pode ser superior ao ano atual."
            )
        return value


class LeitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leitor
        fields = ['id', 'nome', 'email', 'criado_em']
        read_only_fields = ['criado_em']


class EmprestimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprestimo
        fields = ['id', 'livro', 'leitor', 'data_saida', 'devolvido_em']

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'perfil'):
            org = request.user.perfil.organizacao
            livro = data.get('livro')
            leitor = data.get('leitor')
            if livro and livro.organizacao_id != org.id:
                raise serializers.ValidationError(
                    {'livro': 'O livro informado não pertence à sua organização.'}
                )
            if leitor and leitor.organizacao_id != org.id:
                raise serializers.ValidationError(
                    {'leitor': 'O leitor informado não pertence à sua organização.'}
                )
        return data
