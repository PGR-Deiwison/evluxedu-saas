from functools import wraps
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


def user_type_required(user_type):
    """
    Decorador que verifica se o usuário logado é do tipo especificado.
    Se não for, renderiza página 403 com opções de voltar e sair.
    
    Uso:
    @user_type_required('ADMIN')
    def minha_view(request):
        ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='login_usuario')
        def wrapper(request, *args, **kwargs):
            if request.user.tipo != user_type:
                return render(request, 'accounts/forbidden.html', status=403)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def admin_required(view_func):
    """
    Decorador que restringe o acesso apenas para usuários ADMIN.
    """
    @wraps(view_func)
    @login_required(login_url='login_usuario')
    def wrapper(request, *args, **kwargs):
        if request.user.tipo != 'ADMIN':
            return render(request, 'accounts/forbidden.html', status=403)
        return view_func(request, *args, **kwargs)
    return wrapper


def professor_required(view_func):
    """
    Decorador que restringe o acesso apenas para usuários PROFESSOR.
    """
    @wraps(view_func)
    @login_required(login_url='login_usuario')
    def wrapper(request, *args, **kwargs):
        if request.user.tipo != 'PROFESSOR':
            return render(request, 'accounts/forbidden.html', status=403)
        return view_func(request, *args, **kwargs)
    return wrapper


def aluno_required(view_func):
    """
    Decorador que restringe o acesso apenas para usuários ALUNO.
    """
    @wraps(view_func)
    @login_required(login_url='login_usuario')
    def wrapper(request, *args, **kwargs):
        if request.user.tipo != 'ALUNO':
            return render(request, 'accounts/forbidden.html', status=403)
        return view_func(request, *args, **kwargs)
    return wrapper
