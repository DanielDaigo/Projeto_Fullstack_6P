from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from .models import Livro, Leitor, Emprestimo, validar_ano_nao_futuro


class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = ['id', 'titulo', 'autor', 'ano', 'disponivel']

    def validate_ano(self, value):
        """
        Reaproveita a validação centralizada no Model (Aula 13, Slide 16),
        evitando duplicação de regra de negócio entre Form e Serializer.
        """
        try:
            validar_ano_nao_futuro(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.messages[0])
        return value

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'perfil'):
            org = request.user.perfil.organizacao
            titulo = data.get('titulo', getattr(self.instance, 'titulo', None))
            autor = data.get('autor', getattr(self.instance, 'autor', None))
            if titulo and autor:
                qs = Livro.objects.filter(organizacao=org, titulo=titulo, autor=autor)
                if self.instance:
                    qs = qs.exclude(pk=self.instance.pk)
                if qs.exists():
                    raise serializers.ValidationError(
                        "Já existe um livro cadastrado com este título e autor nesta organização."
                    )
        return data


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
