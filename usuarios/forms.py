from django import forms

class PasswordResetCustomForm(forms.Form):
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu e-mail'})
    )
