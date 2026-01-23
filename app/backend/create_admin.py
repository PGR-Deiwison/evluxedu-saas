import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import User

# Deletar usuários de teste antigos se existirem
User.objects.filter(username__in=['admin', 'professor', 'aluno']).delete()
print("Usuários antigos deletados.\n")

# Dados dos usuários
usuarios_dados = [
    {
        'username': 'admin',
        'email': 'admin@test.com',
        'password': 'admin123',
        'cpf': '123.456.789-10',
        'tipo': 'ADMIN',
        'first_name': 'Admin',
        'last_name': 'Escolar',
        'is_superuser': True
    },
    {
        'username': 'professor',
        'email': 'professor@test.com',
        'password': 'professor123',
        'cpf': '234.567.890-11',
        'tipo': 'PROFESSOR',
        'first_name': 'Professor',
        'last_name': 'Silva',
        'is_superuser': False
    },
    {
        'username': 'aluno',
        'email': 'aluno@test.com',
        'password': 'aluno123',
        'cpf': '345.678.901-12',
        'tipo': 'ALUNO',
        'first_name': 'Aluno',
        'last_name': 'Santos',
        'is_superuser': False
    }
]

# Criar os usuários
for usuario_info in usuarios_dados:
    try:
        username = usuario_info['username']
        email = usuario_info['email']
        password = usuario_info['password']
        cpf = usuario_info['cpf']
        tipo = usuario_info['tipo']
        first_name = usuario_info['first_name']
        last_name = usuario_info['last_name']
        is_superuser = usuario_info['is_superuser']
        
        # Deletar se existir
        User.objects.filter(username=username).delete()
        
        # Criar usuário com todos os campos de uma vez
        if is_superuser:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                cpf=cpf,
                tipo=tipo,
                first_name=first_name,
                last_name=last_name
            )
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                cpf=cpf,
                tipo=tipo,
                first_name=first_name,
                last_name=last_name
            )
        
        user.save()
        
        # Verificar se foi salvo corretamente
        user_check = User.objects.get(username=username)
        print(f'✓ Usuário {tipo} criado com sucesso!')
        print(f'  Username: {user_check.username} | Email: {user_check.email}')
        print(f'  CPF: {user_check.cpf} | Tipo: {user_check.tipo}')
        print(f'  Senha: {password}')
        print()
        
    except Exception as e:
        print(f'❌ Erro ao criar usuário: {str(e)}')
        print()

print('=' * 70)
print('✅ USUÁRIOS DE TESTE CRIADOS COM SUCESSO!')
print('=' * 70)
print('\nCredenciais para Login:')
print('\n  ADMIN:')
print('    Username/Email/CPF: admin | admin@test.com | 123.456.789-10')
print('    Senha: admin123')
print('\n  PROFESSOR:')
print('    Username/Email/CPF: professor | professor@test.com | 234.567.890-11')
print('    Senha: professor123')
print('\n  ALUNO:')
print('    Username/Email/CPF: aluno | aluno@test.com | 345.678.901-12')
print('    Senha: aluno123')



