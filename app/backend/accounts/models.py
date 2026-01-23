from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator


# ----------------------------
# DISCIPLINA
# ----------------------------
class Disciplina(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
        ordering = ['nome']

    def __str__(self):
        return self.nome


# ----------------------------
# TURMA
# ----------------------------
class Turma(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"
        ordering = ['nome']

    def __str__(self):
        return self.nome


# ----------------------------
# ESCOLA
# ----------------------------
class Escola(models.Model):
    PLANO_CHOICES = (
        ('BASICO', 'Plano Básico'),
        ('PROFISSIONAL', 'Plano Profissional'),
        ('PREMIUM', 'Plano Premium'),
    )

    nome = models.CharField(max_length=200, verbose_name="Nome da Instituição")
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="CNPJ",
        validators=[RegexValidator(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$|^\d{14}$', 'CNPJ inválido')]
    )
    registro_mec_inep = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Registro MEC/INEP"
    )
    
    # ENDEREÇO INLINE
    rua = models.CharField(max_length=200, verbose_name="Rua")
    numero = models.CharField(max_length=10, verbose_name="Número")
    complemento = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Complemento (Apto, etc)"
    )
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cep = models.CharField(max_length=10, verbose_name="CEP")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(
        max_length=2,
        verbose_name="Estado",
        choices=[
            ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
            ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
            ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
        ]
    )
    
    fone = models.CharField(max_length=15, verbose_name="Telefone")
    email = models.EmailField(verbose_name="Email")
    logomarca = models.ImageField(
        upload_to="escolas/",
        blank=True,
        null=True,
        verbose_name="Logomarca"
    )

    prefixo = models.CharField(
        max_length=5,
        unique=True,
        verbose_name="Prefixo para Matrícula (3-5 letras)",
        validators=[RegexValidator(r'^[A-Z]{3,5}$', 'Use apenas 3-5 letras maiúsculas')]
    )
    plano_contratado = models.CharField(
        max_length=20,
        choices=PLANO_CHOICES,
        verbose_name="Plano Contratado"
    )

    termo_concordancia = models.BooleanField(
        default=False,
        verbose_name="Concordo com os Termos de Uso"
    )
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Escola"
        verbose_name_plural = "Escolas"
        ordering = ['nome']

    def __str__(self):
        return self.nome



# ----------------------------
# USUÁRIO CUSTOMIZADO
# ----------------------------
class User(AbstractUser):
    ADMIN = 'ADMIN'
    PROFESSOR = 'PROFESSOR'
    ALUNO = 'ALUNO'
    
    TIPO_USUARIO = [
        (ADMIN, "Admin Escolar"),
        (PROFESSOR, "Professor"),
        (ALUNO, "Aluno"),
    ]

    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True,
        verbose_name="CPF",
        validators=[RegexValidator(r'^\d{11}$', 'CPF deve conter 11 dígitos numéricos')])
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.cpf} - {self.get_tipo_display()}"


# ----------------------------
# RESPONSÁVEL DO ALUNO
# ----------------------------
class Responsavel(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome do Responsável")
    cpf = models.CharField(
        max_length=14,
        verbose_name="CPF",
        validators=[RegexValidator(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{11}$', 'CPF inválido')]
    )
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    telefone = models.CharField(max_length=15, verbose_name="Telefone")

    class Meta:
        verbose_name = "Responsável"
        verbose_name_plural = "Responsáveis"
        ordering = ['nome']

    def __str__(self):
        return self.nome


# ----------------------------
# ALUNO
# ----------------------------
class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    foto = models.ImageField(
        upload_to="alunos/",
        blank=True,
        null=True,
        verbose_name="Foto"
    )

    # ENDEREÇO INLINE
    rua = models.CharField(max_length=200, verbose_name="Rua")
    numero = models.CharField(max_length=10, verbose_name="Número")
    complemento = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Complemento (Apto, etc)"
    )
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cep = models.CharField(max_length=10, verbose_name="CEP")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(
        max_length=2,
        verbose_name="Estado",
        choices=[
            ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
            ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
            ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
        ]
    )

    turma = models.ForeignKey(
        Turma,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Turma"
    )
    matricula = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Matrícula",
        editable=False
    )

    responsavel = models.ForeignKey(
        Responsavel,
        on_delete=models.CASCADE,
        verbose_name="Responsável"
    )

    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        ordering = ['user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.matricula})"


# ----------------------------
# PROFESSOR
# ----------------------------
class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(verbose_name="Email")
    telefone = models.CharField(max_length=15, verbose_name="Telefone")
    foto = models.ImageField(
        upload_to="professores/",
        blank=True,
        null=True,
        verbose_name="Foto"
    )

    # ENDEREÇO INLINE
    rua = models.CharField(max_length=200, verbose_name="Rua")
    numero = models.CharField(max_length=10, verbose_name="Número")
    complemento = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Complemento (Apto, etc)"
    )
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cep = models.CharField(max_length=10, verbose_name="CEP")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(
        max_length=2,
        verbose_name="Estado",
        choices=[
            ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
            ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
            ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
        ]
    )

    disciplinas = models.ManyToManyField(
        Disciplina,
        blank=True,
        verbose_name="Disciplinas",
        help_text="Selecione uma ou mais disciplinas"
    )
    registro_conselho = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Registro no Conselho (CREF, CRECI, etc)"
    )

    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"
        ordering = ['user__first_name']

    def __str__(self):
        return self.user.get_full_name() or self.user.username


# ----------------------------
# ADMIN ESCOLAR
# ----------------------------
class AdminEscolar(models.Model):
    CARGO_CHOICES = (
        ('DIRETOR', 'Diretor(a)'),
        ('COORDENADOR', 'Coordenador(a)'),
        ('SECRETARIA', 'Secretária(o)'),
        ('OUTRO', 'Outro'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(verbose_name="Email")
    telefone = models.CharField(max_length=15, verbose_name="Telefone")
    foto = models.ImageField(
        upload_to="admin_escolar/",
        blank=True,
        null=True,
        verbose_name="Foto"
    )

    # ENDEREÇO INLINE
    rua = models.CharField(max_length=200, verbose_name="Rua")
    numero = models.CharField(max_length=10, verbose_name="Número")
    complemento = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Complemento (Apto, etc)"
    )
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cep = models.CharField(max_length=10, verbose_name="CEP")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(
        max_length=2,
        verbose_name="Estado",
        choices=[
            ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
            ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
            ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
        ]
    )

    cargo = models.CharField(
        max_length=20,
        choices=CARGO_CHOICES,
        verbose_name="Cargo"
    )

    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Admin Escolar"
        verbose_name_plural = "Admins Escolares"
        ordering = ['user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_cargo_display()}"


# ----------------------------
# SINAIS - GERAR MATRÍCULA AUTOMÁTICA
# ----------------------------
@receiver(post_save, sender=Aluno)
def gerar_matricula(sender, instance, created, **kwargs):
    if created and not instance.matricula:
        escola = instance.user.escola
        if escola:
            total = Aluno.objects.filter(user__escola=escola).count()
            instance.matricula = f"{escola.prefixo}{total:08d}"
            instance.save()
