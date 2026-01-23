from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Aluno, Professor, AdminEscolar, Escola, Responsavel, Turma, Disciplina


# ----------------------------
# FORMULÁRIO CUSTOMIZADO DE USUÁRIO
# ----------------------------
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'tipo', 'escola', 'cpf')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primeiro nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF (XXX.XXX.XXX-XX)'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'escola': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar senha'})


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'tipo', 'escola', 'cpf', 'is_active', 'is_staff')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'escola': forms.Select(attrs={'class': 'form-control'}),
        }


# ----------------------------
# FORMULÁRIO RESPONSÁVEL
# ----------------------------
class ResponsavelForm(forms.ModelForm):
    class Meta:
        model = Responsavel
        fields = ('nome', 'cpf', 'email', 'telefone')
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF (XXX.XXX.XXX-XX)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email (opcional)'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone com DDD'}),
        }


# ----------------------------
# FORMULÁRIO ALUNO
# ----------------------------
class AlunoForm(forms.ModelForm):
    user_first_name = forms.CharField(
        label='Primeiro Nome',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primeiro nome'})
    )
    user_last_name = forms.CharField(
        label='Sobrenome',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'})
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite a senha'})
    )
    password_confirm = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a senha'})
    )

    class Meta:
        model = Aluno
        fields = ('user', 'data_nascimento', 'foto', 'rua', 'numero', 'complemento', 
                  'bairro', 'cep', 'cidade', 'estado', 'turma', 'responsavel')
        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF (XXX.XXX.XXX-XX)'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'rua': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da rua'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apto, sala, etc'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'turma': forms.Select(attrs={'class': 'form-control'}),
            'responsavel': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("As senhas não correspondem.")
        return cleaned_data


# ----------------------------
# FORMULÁRIO PROFESSOR
# ----------------------------
class ProfessorForm(forms.ModelForm):
    user_first_name = forms.CharField(
        label='Primeiro Nome',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primeiro nome'})
    )
    user_last_name = forms.CharField(
        label='Sobrenome',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'})
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite a senha'})
    )
    password_confirm = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a senha'})
    )

    class Meta:
        model = Professor
        fields = ('user', 'email', 'telefone', 'foto', 'rua', 'numero', 'complemento',
                  'bairro', 'cep', 'cidade', 'estado', 'disciplinas', 'registro_conselho')
        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF (XXX.XXX.XXX-XX)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone com DDD'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'rua': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da rua'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apto, sala, etc'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'disciplinas': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'registro_conselho': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: CREF 123456'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("As senhas não correspondem.")
        return cleaned_data


# ----------------------------
# FORMULÁRIO ESCOLA
# ----------------------------
class EscolaForm(forms.ModelForm):
    class Meta:
        model = Escola
        fields = ('nome', 'cnpj', 'registro_mec_inep', 'rua', 'numero', 'complemento',
                  'bairro', 'cep', 'cidade', 'estado', 'fone', 'email', 'logomarca',
                  'prefixo', 'plano_contratado', 'termo_concordancia')
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da instituição'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ (XX.XXX.XXX/XXXX-XX)'}),
            'registro_mec_inep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Registro MEC/INEP (opcional)'}),
            'rua': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da rua'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Complemento (opcional)'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'fone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone com DDD'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'logomarca': forms.FileInput(attrs={'class': 'form-control'}),
            'prefixo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '3-5 letras maiúsculas (Ex: ABC)'}),
            'plano_contratado': forms.Select(attrs={'class': 'form-control'}),
            'termo_concordancia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ----------------------------
# FORMULÁRIO ADMIN ESCOLAR
# ----------------------------
class AdminEscolarForm(forms.ModelForm):
    user_first_name = forms.CharField(
        label='Primeiro Nome',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primeiro nome'})
    )
    user_last_name = forms.CharField(
        label='Sobrenome',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'})
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite a senha'})
    )
    password_confirm = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a senha'})
    )

    class Meta:
        model = AdminEscolar
        fields = ('user', 'email', 'telefone', 'foto', 'rua', 'numero', 'complemento', 'bairro', 'cep', 'cidade', 'estado', 'cargo')
        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF (XXX.XXX.XXX-XX)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone com DDD'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'rua': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da rua'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apto, sala, etc'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("As senhas não correspondem.")
        return cleaned_data
