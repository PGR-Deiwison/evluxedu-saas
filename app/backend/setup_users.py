import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import User

# Verificar usuários existentes
print("=" * 60)
print("USUÁRIOS EXISTENTES NO BANCO DE DADOS")
print("=" * 60)

users = User.objects.all()
print(f"\nTotal de usuários: {users.count()}\n")

for u in users:
    print(f"Username: {u.username}")
    print(f"  Tipo: {u.tipo}")
    print(f"  Email: {u.email}")
    print(f"  CPF: {u.cpf}")
    print(f"  Superuser: {u.is_superuser}")
    print(f"  Staff: {u.is_staff}")
    print()

# Deletar usuários antigos se existirem
print("=" * 60)
print("CRIANDO NOVOS USUÁRIOS")
print("=" * 60)

User.objects.filter(username__in=['admin', 'professor', 'aluno']).delete()
print("Usuários antigos deletados.\n")

# Criar admin
admin = User.objects.create_superuser(
    username='admin',
    email='admin@test.com',
    password='admin123'
)
admin.tipo = 'ADMIN'
admin.cpf = '123.456.789-10'
admin.first_name = 'Admin'
admin.last_name = 'Escolar'
admin.save()
print("✓ ADMIN criado")
print(f"  Username: admin | Senha: admin123")
print(f"  Email: admin@test.com")
print(f"  CPF: 123.456.789-10\n")

# Criar professor
professor = User.objects.create_user(
    username='professor',
    email='professor@test.com',
    password='professor123'
)
professor.tipo = 'PROFESSOR'
professor.cpf = '234.567.890-11'
professor.first_name = 'Professor'
professor.last_name = 'Silva'
professor.save()
print("✓ PROFESSOR criado")
print(f"  Username: professor | Senha: professor123")
print(f"  Email: professor@test.com")
print(f"  CPF: 234.567.890-11\n")

# Criar aluno
aluno = User.objects.create_user(
    username='aluno',
    email='aluno@test.com',
    password='aluno123'
)
aluno.tipo = 'ALUNO'
aluno.cpf = '345.678.901-12'
aluno.first_name = 'Aluno'
aluno.last_name = 'Santos'
aluno.save()
print("✓ ALUNO criado")
print(f"  Username: aluno | Senha: aluno123")
print(f"  Email: aluno@test.com")
print(f"  CPF: 345.678.901-12\n")

print("=" * 60)
print("✅ TODOS OS USUÁRIOS FORAM CRIADOS COM SUCESSO!")
print("=" * 60)
