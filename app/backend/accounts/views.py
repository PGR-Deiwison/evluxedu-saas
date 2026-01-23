from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .decorators import admin_required, professor_required, aluno_required


def escolher_tipo_de_usuario(request):
    """
    Renderiza a página para escolher o tipo de usuário.
    Tipos: Administrador, Professor, Aluno
    """
    return render(request, 'accounts/escolher_tipo_de_usuario.html')


def login_usuario(request):
    """
    View de login universal. Usa backend customizado que autentica por username, email ou CPF.
    """
    if request.method == 'POST':
        username_or_email_or_cpf = request.POST.get('username_or_email', '').strip()
        password = request.POST.get('password', '')
        
        # Usar o backend customizado para autenticar
        user = authenticate(request, username=username_or_email_or_cpf, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard_redirect')
        else:
            messages.error(request, 'Usuário, email, CPF ou senha inválidos.')
    
    return render(request, 'accounts/login.html')






@login_required(login_url='login_usuario')
def dashboard_redirect(request):
    """
    Redireciona o usuário para o dashboard apropriado conforme seu tipo.
    """
    tipo_usuario = request.user.tipo
    
    if tipo_usuario == 'ADMIN':
        return redirect('dashboard_admin')
    elif tipo_usuario == 'PROFESSOR':
        return redirect('dashboard_professor')
    elif tipo_usuario == 'ALUNO':
        return redirect('dashboard_aluno')
    else:
        return redirect('escolher_tipo_de_usuario')


@admin_required
def dashboard_admin(request):
    """
    Dashboard para Administrador.
    """
    return render(request, 'accounts/dashboard_admin.html')


@professor_required
def dashboard_professor(request):
    """
    Dashboard para Professor.
    """
    return render(request, 'accounts/dashboard_professor.html')


@aluno_required
def dashboard_aluno(request):
    """
    Dashboard para Aluno.
    """
    return render(request, 'accounts/dashboard_aluno.html')


def logout_usuario(request):
    """
    Realiza logout do usuário.
    """
    logout(request)
    return redirect('escolher_tipo_de_usuario')


def login_admin(request):
    """
    Renderiza a página de login para Administrador.
    """
    return render(request, 'accounts/login_admin.html')


def login_professor(request):
    """
    Renderiza a página de login para Professor.
    """
    return render(request, 'accounts/login_professor.html')


def login_aluno(request):
    """
    Renderiza a página de login para Aluno.
    """
    return render(request, 'accounts/login_aluno.html')

