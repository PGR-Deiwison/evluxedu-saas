import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import User

try:
    # Deletar se existir
    User.objects.filter(username='professor2').delete()
    
    # Criar novo Professor
    professor2 = User.objects.create_user(
        username='professor2',
        email='professor2@test.com',
        password='professor123',
        cpf='456.789.012-34',
        tipo='PROFESSOR',
        first_name='Professor',
        last_name='Oliveira'
    )
    professor2.save()
    
    # Verificar se foi criado
    prof_check = User.objects.get(username='professor2')
    
    print('✓ Novo Professor criado com sucesso!')
    print(f'  Username: {prof_check.username}')
    print(f'  Email: {prof_check.email}')
    print(f'  CPF: {prof_check.cpf}')
    print(f'  Tipo: {prof_check.tipo}')
    print(f'  Senha: professor123')
    print(f'  is_active: {prof_check.is_active}')
    
except Exception as e:
    print(f'❌ Erro ao criar professor2: {str(e)}')
    import traceback
    traceback.print_exc()

