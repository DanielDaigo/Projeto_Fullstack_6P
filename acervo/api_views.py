from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Livro, Leitor, Emprestimo
from .serializers import LivroSerializer, LeitorSerializer, EmprestimoSerializer
from .dashboard import calcular_metricas_dashboard


def _org_api(request):
    if not hasattr(request.user, 'perfil'):
        raise PermissionDenied("Usuário autenticado não possui Perfil vinculado a uma Organização.")
    return request.user.perfil.organizacao


class LivroListCreate(generics.ListCreateAPIView):
    serializer_class = LivroSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Livro.objects.filter(organizacao=_org_api(self.request)).order_by('titulo')

    def perform_create(self, serializer):
        serializer.save(organizacao=_org_api(self.request))


class LivroDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LivroSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Livro.objects.filter(organizacao=_org_api(self.request))


class LeitorListCreate(generics.ListCreateAPIView):
    serializer_class = LeitorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Leitor.objects.filter(organizacao=_org_api(self.request)).order_by('nome')

    def perform_create(self, serializer):
        serializer.save(organizacao=_org_api(self.request))


class LeitorDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LeitorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Leitor.objects.filter(organizacao=_org_api(self.request))


class EmprestimoListCreate(generics.ListCreateAPIView):
    serializer_class = EmprestimoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Emprestimo.objects.filter(organizacao=_org_api(self.request))
            .select_related('livro', 'leitor')
            .order_by('-data_saida', '-id')
        )

    def perform_create(self, serializer):
        serializer.save(organizacao=_org_api(self.request))


class EmprestimoDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmprestimoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Emprestimo.objects.filter(
            organizacao=_org_api(self.request)
        ).select_related('livro', 'leitor')


class DashboardApi(APIView):
    """
    API do Dashboard (Aula 17, Slide 35):
    Reaproveita calcular_metricas_dashboard() de acervo/dashboard.py sem duplicar consultas ORM.
    Respeita isolamento multi-tenant, filtro de período (?inicio=...&fim=...) e papel do usuário.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        org = _org_api(request)
        incluir_series = request.user.perfil.eh_admin
        metricas = calcular_metricas_dashboard(request, org, incluir_series=incluir_series)
        return Response({
            'organizacao': org.nome,
            **metricas,
        })
