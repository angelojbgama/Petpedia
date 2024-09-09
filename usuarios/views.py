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
from .forms import PasswordResetCustomForm
from django.contrib.auth import views as auth_views
from .forms import CustomSetNewPasswordForm
from .forms import CustomUserCreationForm  # Importe o formulário personalizado

User = get_user_model()


class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'registration/cadastro.html'
    success_url = reverse_lazy('login')  
    

class CustomPasswordResetView(FormView):
    template_name = 'registration/password_reset.html'
    form_class = PasswordResetCustomForm
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        User = get_user_model()
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(self.request, "Este e-mail não está cadastrado.")
            return redirect('password_reset')

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        password_reset_url = self.request.build_absolute_uri(
            reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        )

        subject = 'Redefinição de Senha'
        message = render_to_string('registration/password_reset_email.html', {
            'user': user,
            'password_reset_url': password_reset_url,
            'uid': uid,
            'token': token,
            'protocol': self.request.scheme,
            'domain': self.request.get_host(),
            'site_name': 'Seu Site'
        })
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        messages.success(self.request, "Link de redefinição de senha enviado para o e-mail fornecido.")
        return super().form_valid(form)



class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'registration/password_reset_realized.html'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_confirm_new_reset.html'
    form_class = CustomSetNewPasswordForm
    success_url = reverse_lazy('password_reset_complete')

from django.contrib.auth import views as auth_views

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/password_reset_c.html'
