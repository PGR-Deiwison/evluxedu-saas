import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import User

print("=" * 80)
print("VERIFICAÇÃO DE USUÁRIOS NO BANCO DE DADOS")
print("=" * 80)

users = User.objects.all()
print(f"\nTotal de usuários: {users.count()}\n")

if users.count() == 0:
    print("❌ Nenhum usuário encontrado no banco de dados!")
else:
    for u in users:
        print(f"┌─ Username: {u.username}")
        print(f"├─ Email: {u.email}")
        print(f"├─ CPF: {u.cpf if u.cpf else '❌ VAZIO'}")
        print(f"├─ Tipo: {u.tipo if u.tipo else '❌ VAZIO'}")
        print(f"├─ is_active: {u.is_active}")
        print(f"├─ is_superuser: {u.is_superuser}")
        
        # Testar senha
        senha_admin = u.check_password('admin123')
        senha_professor = u.check_password('professor123')
        senha_aluno = u.check_password('aluno123')
        
        if senha_admin:
            print(f"├─ Senha: admin123 ✓")
        elif senha_professor:
            print(f"├─ Senha: professor123 ✓")
        elif senha_aluno:
            print(f"├─ Senha: aluno123 ✓")
        else:
            print(f"├─ Senha: ❌ NENHUMA TESTADA")
        
        print()

print("=" * 80)
print("TESTES DE AUTENTICAÇÃO")
print("=" * 80)

from django.contrib.auth import authenticate

# Testar admin
print("\n✓ Testando ADMIN:")
admin = authenticate(username='admin', password='admin123')
if admin:
    print(f"  ✓ Login com username: OK")
else:
    print(f"  ❌ Login com username: FALHA")

admin_email = authenticate(username='admin@test.com', password='admin123')
if admin_email:
    print(f"  ✓ Login com email: OK")
else:
    print(f"  ❌ Login com email: FALHA")

admin_cpf = authenticate(username='123.456.789-10', password='admin123')
if admin_cpf:
    print(f"  ✓ Login com CPF (formatado): OK")
else:
    print(f"  ❌ Login com CPF (formatado): FALHA")

# Testar professor
print("\n✓ Testando PROFESSOR:")
prof = authenticate(username='professor', password='professor123')
if prof:
    print(f"  ✓ Login com username: OK")
else:
    print(f"  ❌ Login com username: FALHA")

prof_email = authenticate(username='professor@test.com', password='professor123')
if prof_email:
    print(f"  ✓ Login com email: OK")
else:
    print(f"  ❌ Login com email: FALHA")

prof_cpf = authenticate(username='234.567.890-11', password='professor123')
if prof_cpf:
    print(f"  ✓ Login com CPF (formatado): OK")
else:
    print(f"  ❌ Login com CPF (formatado): FALHA")

# Testar aluno
print("\n✓ Testando ALUNO:")
aluno = authenticate(username='aluno', password='aluno123')
if aluno:
    print(f"  ✓ Login com username: OK")
else:
    print(f"  ❌ Login com username: FALHA")

aluno_email = authenticate(username='aluno@test.com', password='aluno123')
if aluno_email:
    print(f"  ✓ Login com email: OK")
else:
    print(f"  ❌ Login com email: FALHA")

aluno_cpf = authenticate(username='345.678.901-12', password='aluno123')
if aluno_cpf:
    print(f"  ✓ Login com CPF (formatado): OK")
else:
    print(f"  ❌ Login com CPF (formatado): FALHA")

print("\n" + "=" * 80)
