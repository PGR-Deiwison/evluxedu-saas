import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import User
from django.contrib.auth import authenticate

print("=" * 80)
print("VERIFICAÇÃO DO PROFESSOR2")
print("=" * 80)

# Verificar se existe
try:
    prof2 = User.objects.get(username='professor2')
    print(f"\n✓ Professor2 encontrado no banco:")
    print(f"  Username: {prof2.username}")
    print(f"  Email: {prof2.email}")
    print(f"  CPF: {prof2.cpf}")
    print(f"  Tipo: {prof2.tipo}")
    print(f"  is_active: {prof2.is_active}")
    
    # Testar senha
    print(f"\n✓ Testando senha 'professor123':")
    if prof2.check_password('professor123'):
        print(f"  ✓ Senha correta!")
    else:
        print(f"  ❌ Senha incorreta!")
    
    # Testar autenticação
    print(f"\n✓ Testando autenticação:")
    
    auth = authenticate(username='professor2', password='professor123')
    if auth:
        print(f"  ✓ Login com username: OK")
    else:
        print(f"  ❌ Login com username: FALHA")
    
    auth_email = authenticate(username='professor2@test.com', password='professor123')
    if auth_email:
        print(f"  ✓ Login com email: OK")
    else:
        print(f"  ❌ Login com email: FALHA")
    
    auth_cpf = authenticate(username='456.789.012-34', password='professor123')
    if auth_cpf:
        print(f"  ✓ Login com CPF: OK")
    else:
        print(f"  ❌ Login com CPF: FALHA")
    
except User.DoesNotExist:
    print(f"\n❌ Professor2 NÃO foi encontrado no banco de dados!")
    print(f"   Ele não foi criado corretamente.")

print("\n" + "=" * 80)
