import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import User

print("=" * 70)
print("VERIFICAÇÃO DE USUÁRIOS NO BANCO DE DADOS")
print("=" * 70)

users = User.objects.all()
print(f"\nTotal de usuários: {users.count()}\n")

if users.count() == 0:
    print("❌ Nenhum usuário encontrado!")
else:
    for u in users:
        print(f"┌─ Username: {u.username}")
        print(f"├─ Tipo: {u.tipo if u.tipo else '⚠️  NÃO DEFINIDO'}")
        print(f"├─ Email: {u.email}")
        print(f"├─ CPF: {u.cpf if u.cpf else '⚠️  VAZIO'}")
        print(f"├─ is_superuser: {u.is_superuser}")
        print(f"└─ is_staff: {u.is_staff}\n")

print("=" * 70)
print("DELETANDO USUÁRIOS ANTIGOS")
print("=" * 70)

deleted_count, _ = User.objects.filter(username__in=['admin', 'professor', 'aluno']).delete()
print(f"✓ {deleted_count} usuários deletados\n")

print("=" * 70)
print("CRIANDO NOVOS USUÁRIOS")
print("=" * 70)

try:
    # Criar Admin
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
    print("✓ ADMIN criado com sucesso!")
    
    # Verificar admin
    admin_check = User.objects.get(username='admin')
    print(f"  ├─ Username: {admin_check.username}")
    print(f"  ├─ Email: {admin_check.email}")
    print(f"  ├─ CPF: {admin_check.cpf}")
    print(f"  ├─ Tipo: {admin_check.tipo}")
    print(f"  ├─ Senha testável: {'Sim' if admin_check.check_password('admin123') else 'Não'}")
    print()

except Exception as e:
    print(f"❌ Erro ao criar ADMIN: {e}\n")

try:
    # Criar Professor
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
    print("✓ PROFESSOR criado com sucesso!")
    
    # Verificar professor
    prof_check = User.objects.get(username='professor')
    print(f"  ├─ Username: {prof_check.username}")
    print(f"  ├─ Email: {prof_check.email}")
    print(f"  ├─ CPF: {prof_check.cpf}")
    print(f"  ├─ Tipo: {prof_check.tipo}")
    print(f"  ├─ Senha testável: {'Sim' if prof_check.check_password('professor123') else 'Não'}")
    print()

except Exception as e:
    print(f"❌ Erro ao criar PROFESSOR: {e}\n")

try:
    # Criar Aluno
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
    print("✓ ALUNO criado com sucesso!")
    
    # Verificar aluno
    aluno_check = User.objects.get(username='aluno')
    print(f"  ├─ Username: {aluno_check.username}")
    print(f"  ├─ Email: {aluno_check.email}")
    print(f"  ├─ CPF: {aluno_check.cpf}")
    print(f"  ├─ Tipo: {aluno_check.tipo}")
    print(f"  ├─ Senha testável: {'Sim' if aluno_check.check_password('aluno123') else 'Não'}")
    print()

except Exception as e:
    print(f"❌ Erro ao criar ALUNO: {e}\n")

print("=" * 70)
print("✅ VERIFICAÇÃO COMPLETA")
print("=" * 70)
