from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from pets.forms import PETForm
from core.models import PET, ADOCAO
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


class PETCreateView(LoginRequiredMixin, CreateView):
    model = PET
    form_class = PETForm
    template_name = 'pet/pet_form.html'
    success_url = reverse_lazy('pet_list')  # Redireciona para uma lista de PETs após sucesso

    def form_valid(self, form):
        # Verifica se o usuário é uma ONG
        if not self.request.user.is_ong:
            raise PermissionDenied("Apenas ONGs podem cadastrar pets.")
        
        # Define o dono do pet como o usuário logado (ONG)
        form.instance.dono = self.request.user
        
        # Salva o pet no banco de dados
        response = super().form_valid(form)
        
        # Após o pet ser salvo, criar uma solicitação de adoção automaticamente
        pet = form.instance  # Pet recém-criado
        
        # Criar a solicitação de adoção associando o pet à própria ONG que o cadastrou
        ADOCAO.objects.create(
            usuario_adotante=self.request.user,  # Neste caso, a ONG seria a solicitante (ou um placeholder)
            pet=pet,
            ong_adocao=self.request.user,  # A ONG também é a responsável pela adoção
            data_solicitacao=timezone.now(),
            estado_da_adocao=False  # Estado inicial da adoção como "pendente"
        )
        
        return response



class PETListView(ListView):
    model = PET
    template_name = 'pet/petlistview.html'
    context_object_name = 'pets'

class PETadotarView(LoginRequiredMixin, ListView):
    model = ADOCAO
    