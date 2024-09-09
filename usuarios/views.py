# usuarios/views.py
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.views.generic.edit import FormView
from .forms import PasswordResetCustomForm  # Seu formulário customizado

User = get_user_model()
from .forms import PasswordResetCustomForm


class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/cadastro.html'
    success_url = reverse_lazy('login')  # Redireciona para a página de login após o registro



class CustomPasswordResetView(FormView):
    template_name = 'registration/password_reset.html'
    form_class = PasswordResetCustomForm
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        
        # Tenta buscar o usuário associado ao e-mail
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Exibe uma mensagem se o e-mail não for encontrado
            messages.error(self.request, "Este e-mail não está cadastrado.")
            return redirect('password_reset')

        # Gera o token de redefinição de senha
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Cria a URL completa para resetar a senha
        password_reset_url = self.request.build_absolute_uri(
            reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        )

        # Envia o e-mail com o link de redefinição de senha
        subject = 'Redefinição de Senha'
        message = render_to_string('registration/password_reset_email.html', {
            'user': user,
            'password_reset_url': password_reset_url,
        })
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        # Mensagem de sucesso após o envio do e-mail
        messages.success(self.request, "Link de redefinição de senha enviado para o e-mail fornecido.")
        return super().form_valid(form)
