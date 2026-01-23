import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import User

print("=" * 70)
print("VERIFICAÇÃO DE USUÁRIOS CRIADOS")
print("=" * 70)

users = User.objects.filter(username__in=['admin', 'professor', 'aluno'])
print(f"\nTotal de usuários encontrados: {users.count()}\n")

if users.count() == 0:
    print("❌ NENHUM USUÁRIO FOI CRIADO!")
else:
    for u in users:
        print(f"┌─ Username: {u.username}")
        print(f"├─ Email: {u.email}")
        print(f"├─ CPF: {u.cpf}")
        print(f"├─ Tipo: {u.tipo if u.tipo else '❌ NÃO DEFINIDO'}")
        print(f"├─ First Name: {u.first_name}")
        print(f"├─ Last Name: {u.last_name}")
        print(f"├─ Senha testável (admin123): {u.check_password('admin123')}")
        print(f"├─ Senha testável (professor123): {u.check_password('professor123')}")
        print(f"└─ Senha testável (aluno123): {u.check_password('aluno123')}")
        print()
