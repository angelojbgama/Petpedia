from django import forms

class ContatoForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='Email')
    assunto = forms.CharField(label='Assunto', max_length=100, required=False)
    mensagem = forms.CharField(widget=forms.Textarea, label='Mensagem')
    
    def format_email_content(self):
        """
        Método para formatar o conteúdo do e-mail.
        """
        nome = self.cleaned_data.get('nome')
        email = self.cleaned_data.get('email')
        assunto = self.cleaned_data.get('assunto')
        mensagem = self.cleaned_data.get('mensagem')

        return f"""
        Você recebeu uma nova mensagem de contato:

        Nome: {nome}
        E-mail: {email}
        Assunto: {assunto}

        Mensagem:
        {mensagem}
        """
