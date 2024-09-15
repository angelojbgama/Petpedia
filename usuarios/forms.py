from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import USUARIO
from django.contrib.auth.forms import AuthenticationForm


class PasswordResetCustomForm(forms.Form):
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu e-mail'
        })
    )

class CustomSetNewPasswordForm(SetPasswordForm):
    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')

        # Valida a complexidade da senha
        if len(password) < 8:
            raise ValidationError("A nova senha deve ter pelo menos 8 caracteres.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("A nova senha deve conter pelo menos um número.")
        if not any(char.isalpha() for char in password):
            raise ValidationError("A nova senha deve conter pelo menos uma letra.")
        
        return password

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = USUARIO
        fields = ('username', 'email', 'password1', 'password2', 'localidade', 'telefone', 'is_ong', 'nome_ong')

class CustomAuthenticationForm(AuthenticationForm):
    # Remover o campo de e-mail e manter apenas usuário e senha
    username = forms.CharField(label='Nome de Usuário')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    class Meta:
        fields = ['username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = self.get_user()
            if not user or not user.check_password(password):
                raise forms.ValidationError("Credenciais inválidas.")
            if not user.is_active:
                raise forms.ValidationError("Este usuário está inativo.")
        
        return cleaned_data
