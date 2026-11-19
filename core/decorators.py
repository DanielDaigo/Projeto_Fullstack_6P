from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def papel_requerido(*papeis):
    """
    Decorator para restringir o acesso a views com base no papel do Perfil do usuário.
    Exemplo: @papel_requerido('admin')
    """
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, 'perfil'):
                raise PermissionDenied("O usuário conectado não possui um Perfil vinculado.")
            if request.user.perfil.papel not in papeis:
                raise PermissionDenied("Você não tem permissão para acessar este recurso.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
