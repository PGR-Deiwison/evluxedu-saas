from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Aluno, Professor, AdminEscolar, Escola, Responsavel, Turma, Disciplina
from .forms import CustomUserCreationForm, CustomUserChangeForm, AlunoForm, ProfessorForm, AdminEscolarForm, EscolaForm


# ----------------------------
# CUSTOMIZAÇÃO USER ADMIN
# ----------------------------
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('username', 'get_full_name_display', 'tipo_colored', 'escola', 'email', 'is_staff')
    list_filter = ('tipo', 'escola', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'cpf')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email', 'cpf')}),
        ('Tipo de Usuário', {'fields': ('tipo', 'escola')}),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Datas Importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email', 'cpf')}),
        ('Tipo de Usuário', {'fields': ('tipo', 'escola')}),
    )

    def get_full_name_display(self, obj):
        return obj.get_full_name() or obj.username
    get_full_name_display.short_description = 'Nome Completo'

    def tipo_colored(self, obj):
        colors = {
            'ADMIN': '#28a745',
            'PROFESSOR': '#007bff',
            'ALUNO': '#ffc107',
        }
        color = colors.get(obj.tipo, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_tipo_display()
        )
    tipo_colored.short_description = 'Tipo'


# ----------------------------
# RESPONSÁVEL INLINE (para Aluno)
# ----------------------------
class ResponsavelInline(admin.TabularInline):
    model = Responsavel
    extra = 1
    fields = ('nome', 'cpf', 'email', 'telefone')
    verbose_name = 'Responsável'
    verbose_name_plural = 'Responsáveis'


# ----------------------------
# TURMA ADMIN
# ----------------------------
@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao_preview', 'alunos_count')
    search_fields = ('nome',)
    ordering = ('nome',)

    def descricao_preview(self, obj):
        if obj.descricao:
            return obj.descricao[:50] + '...' if len(obj.descricao) > 50 else obj.descricao
        return '-'
    descricao_preview.short_description = 'Descrição'

    def alunos_count(self, obj):
        count = Aluno.objects.filter(turma=obj).count()
        return format_html(
            '<span style="background-color: #e3f2fd; color: #1976d2; padding: 3px 8px; border-radius: 3px;">{}</span>',
            count
        )
    alunos_count.short_description = 'Alunos'


# ----------------------------
# DISCIPLINA ADMIN
# ----------------------------
@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'professores_count')
    search_fields = ('nome',)
    ordering = ('nome',)

    def professores_count(self, obj):
        count = Professor.objects.filter(disciplinas=obj).count()
        return format_html(
            '<span style="background-color: #f3e5f5; color: #7b1fa2; padding: 3px 8px; border-radius: 3px;">{}</span>',
            count
        )
    professores_count.short_description = 'Professores'



# ----------------------------
# ALUNO ADMIN
# ----------------------------
@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    form = AlunoForm
    list_display = ('matricula', 'nome_completo', 'user', 'turma', 'responsavel', 'data_nascimento')
    search_fields = ('user__first_name', 'user__last_name', 'cpf', 'matricula')
    list_filter = ('turma', 'user__escola', 'data_criacao')
    ordering = ('-data_criacao',)
    readonly_fields = ('matricula', 'data_criacao', 'data_atualizacao', 'get_foto_preview')

    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Informações Pessoais', {
            'fields': ('cpf', 'data_nascimento', 'foto', 'get_foto_preview')
        }),
        ('Endereço', {
            'fields': ('rua', 'numero', 'complemento', 'bairro', 'cep', 'cidade', 'estado'),
            'classes': ('collapse',)
        }),
        ('Turma e Matrícula', {
            'fields': ('turma', 'matricula')
        }),
        ('Responsável', {
            'fields': ('responsavel',)
        }),
        ('Datas', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )

    def nome_completo(self, obj):
        return obj.user.get_full_name() or obj.user.username
    nome_completo.short_description = 'Nome Completo'

    def get_foto_preview(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" width="100" height="100" style="border-radius: 5px;" />',
                obj.foto.url
            )
        return 'Sem foto'
    get_foto_preview.short_description = 'Prévia da Foto'


# ----------------------------
# PROFESSOR ADMIN
# ----------------------------
@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    form = ProfessorForm
    list_display = ('nome_completo', 'user', 'email', 'disciplinas_display', 'data_criacao')
    search_fields = ('user__first_name', 'user__last_name', 'cpf', 'email')
    list_filter = ('user__escola', 'disciplinas', 'data_criacao')
    filter_horizontal = ('disciplinas',)
    ordering = ('-data_criacao',)
    readonly_fields = ('data_criacao', 'data_atualizacao', 'get_foto_preview')

    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Informações Pessoais', {
            'fields': ('cpf', 'email', 'telefone', 'foto', 'get_foto_preview')
        }),
        ('Endereço', {
            'fields': ('rua', 'numero', 'complemento', 'bairro', 'cep', 'cidade', 'estado'),
            'classes': ('collapse',)
        }),
        ('Profissional', {
            'fields': ('disciplinas', 'registro_conselho')
        }),
        ('Datas', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )

    def nome_completo(self, obj):
        return obj.user.get_full_name() or obj.user.username
    nome_completo.short_description = 'Nome Completo'

    def disciplinas_display(self, obj):
        disciplinas = obj.disciplinas.all()
        if disciplinas:
            return ', '.join([d.nome for d in disciplinas])
        return '-'
    disciplinas_display.short_description = 'Disciplinas'

    def get_foto_preview(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" width="100" height="100" style="border-radius: 5px;" />',
                obj.foto.url
            )
        return 'Sem foto'
    get_foto_preview.short_description = 'Prévia da Foto'


# ----------------------------
# ADMIN ESCOLAR ADMIN
# ----------------------------
@admin.register(AdminEscolar)
class AdminEscolarAdmin(admin.ModelAdmin):
    form = AdminEscolarForm
    list_display = ('nome_completo', 'cargo_colored', 'user', 'email', 'user__escola')
    search_fields = ('user__first_name', 'user__last_name', 'cpf', 'email')
    list_filter = ('user__escola', 'cargo', 'data_criacao')
    ordering = ('-data_criacao',)
    readonly_fields = ('data_criacao', 'data_atualizacao', 'get_foto_preview')

    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Informações Pessoais', {
            'fields': ('cpf', 'email', 'telefone', 'foto', 'get_foto_preview')
        }),
        ('Endereço', {
            'fields': ('rua', 'numero', 'complemento', 'bairro', 'cep', 'cidade', 'estado'),
            'classes': ('collapse',)
        }),
        ('Cargo', {
            'fields': ('cargo',)
        }),
        ('Datas', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )

    def nome_completo(self, obj):
        return obj.user.get_full_name() or obj.user.username
    nome_completo.short_description = 'Nome Completo'

    def cargo_colored(self, obj):
        colors = {
            'DIRETOR': '#dc3545',
            'COORDENADOR': '#fd7e14',
            'SECRETARIA': '#20c997',
            'OUTRO': '#6c757d',
        }
        color = colors.get(obj.cargo, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_cargo_display()
        )
    cargo_colored.short_description = 'Cargo'

    def get_foto_preview(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" width="100" height="100" style="border-radius: 5px;" />',
                obj.foto.url
            )
        return 'Sem foto'
    get_foto_preview.short_description = 'Prévia da Foto'


# ----------------------------
# ESCOLA ADMIN
# ----------------------------
@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    form = EscolaForm
    list_display = ('nome', 'cnpj', 'prefixo', 'plano_contratado', 'usuarios_count', 'termo_concordancia_display')
    search_fields = ('nome', 'cnpj', 'prefixo', 'email')
    list_filter = ('plano_contratado', 'termo_concordancia', 'data_criacao')
    ordering = ('-data_criacao',)
    readonly_fields = ('data_criacao', 'data_atualizacao', 'get_logo_preview')

    fieldsets = (
        ('Informações Gerais', {
            'fields': ('nome', 'cnpj', 'registro_mec_inep')
        }),
        ('Contato', {
            'fields': ('fone', 'email')
        }),
        ('Endereço', {
            'fields': ('rua', 'numero', 'complemento', 'bairro', 'cep', 'cidade', 'estado'),
        }),
        ('Sistema', {
            'fields': ('logomarca', 'get_logo_preview', 'prefixo', 'plano_contratado')
        }),
        ('Termos de Uso', {
            'fields': ('termo_concordancia',)
        }),
        ('Datas', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )

    def usuarios_count(self, obj):
        count = User.objects.filter(escola=obj).count()
        return format_html(
            '<span style="background-color: #e1f5fe; color: #01579b; padding: 3px 8px; border-radius: 3px;">{}</span>',
            count
        )
    usuarios_count.short_description = 'Usuários'

    def termo_concordancia_display(self, obj):
        if obj.termo_concordancia:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Concordado</span>'
            )
        return format_html(
            '<span style="color: red; font-weight: bold;">✗ Não Concordado</span>'
        )
    termo_concordancia_display.short_description = 'Termo de Uso'

    def get_logo_preview(self, obj):
        if obj.logomarca:
            return format_html(
                '<img src="{}" width="150" height="100" style="border-radius: 5px; object-fit: contain;" />',
                obj.logomarca.url
            )
        return 'Sem logo'
    get_logo_preview.short_description = 'Prévia da Logomarca'

