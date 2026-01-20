from django.contrib import admin
from .models import Escola

# Registrar o modelo Escola no admin do Django
@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'ativa')
    search_fields = ('nome', 'cnpj')