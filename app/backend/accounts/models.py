from django.contrib.auth.models import AbstractUser
from django.db import models

# Criando um modelo de usuário personalizado

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('admin_escola', 'Administrador da Escola'),
        ('professor', 'Professor'),
        ('aluno', 'Aluno'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    
    escola = models.ForeignKey('schools.Escola', on_delete=models.SET_NULL, null=True, blank=True)
    
    
