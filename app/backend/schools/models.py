from django.db import models

# Criando um modelo para representar uma escola

class Escola(models.Model):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True, help_text="Formato: 00.000.000/0000-00")
    responsanvel_financeiro = models.CharField(max_length=255, help_text="Nome do responsável financeiro")
    cpf_responsavel = models.CharField(max_length=14, help_text="Formato: 000.000.000-00")
    endereco = models.TextField()
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    data_vencimento_padrao = models.PositiveSmallIntegerField(default=10)  # Dias padrão para vencimento de faturas
    ativa = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
