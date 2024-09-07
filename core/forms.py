from django import forms

class ContatoForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='Email')
    assunto = forms.CharField(label='Assunto', max_length=100, required=False)
    mensagem = forms.CharField(widget=forms.Textarea, label='Mensagem')
