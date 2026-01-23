from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAuthenticationBackend(ModelBackend):
    """
    Backend de autenticação customizado que permite login por:
    - username
    - email
    - cpf
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        user = None
        login_input = username.strip()
        
        # Normalizar o CPF de entrada (remover pontos e traços)
        login_normalized = login_input.replace('.', '').replace('-', '')
        
        # Tentar por CPF (normalizado)
        # Busca tanto pelo CPF normalizado quanto pelo formatado
        try:
            user = User.objects.get(cpf=login_input)  # Tenta com a formatação fornecida
        except User.DoesNotExist:
            try:
                # Se o CPF foi fornecido sem formatação, tenta buscar no banco
                # buscando tanto formatado quanto não
                user = User.objects.filter(
                    cpf__in=[login_input, login_normalized]
                ).first()
            except User.DoesNotExist:
                pass
        
        # Tentar por email
        if user is None:
            try:
                user = User.objects.get(email__iexact=login_input)
            except User.DoesNotExist:
                pass
        
        # Tentar por username
        if user is None:
            try:
                user = User.objects.get(username=login_input)
            except User.DoesNotExist:
                pass
        
        # Verificar a senha e se o usuário está ativo
        if user is not None and user.check_password(password) and user.is_active:
            return user
        
        return None

    def get_user(self, user_id):
        """
        Retorna o usuário por ID.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
