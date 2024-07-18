from functools import wraps
from django.shortcuts import redirect

def role_required(role_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')  # Redirigir al usuario a la página de inicio de sesión si no está autenticado
            if request.user.rol.nombre != role_name:
                return redirect('error_403')  # Redirigir al usuario a la página de error 403 si no tiene el rol adecuado
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
