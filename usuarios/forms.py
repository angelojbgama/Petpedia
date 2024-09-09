from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


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


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='Confirme a Senha',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("As senhas não coincidem")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
