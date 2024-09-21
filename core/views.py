from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from .models import ADOCAO, PET
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import CreateView
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.generic import ListView


class AtualizarAdocaoView(LoginRequiredMixin, UpdateView):
    model = ADOCAO
    fields = []  # Nenhum campo será modificado diretamente no formulário
    template_name = 'adocao/adocao_update.html'
    success_url = reverse_lazy('solicitacoes_adocao')  # Redireciona após aprovação/rejeição

    def post(self, request, *args, **kwargs):
        adocao = self.get_object()

        # Verifica se o usuário é a ONG responsável pela adoção
        if adocao.ong_adocao != request.user:
            return HttpResponseForbidden("Você não tem permissão para modificar essa adoção.")

        # Atualiza o estado da adoção (aprovar/rejeitar)
        estado = request.POST.get('estado')

        # Se você estiver usando BooleanField (estado_da_adocao):
        if estado == 'aprovado':
            adocao.estado_da_adocao = True
        elif estado == 'rejeitado':
            adocao.estado_da_adocao = False
        adocao.save()

        return super().post(request, *args, **kwargs)


class SolicitacoesAdocaoView(LoginRequiredMixin, ListView):
    model = ADOCAO
    template_name = 'adocao/solicitacoes_adocao_list.html'  # Defina seu template para exibir as solicitações
    context_object_name = 'solicitacoes'

    def get_queryset(self):
        # Filtra solicitações onde a ONG responsável é o usuário logado e estão pendentes
        return ADOCAO.objects.filter(ong_adocao=self.request.user, estado_da_adocao='pendente')


class AdocaoCreateView(CreateView):
    model = ADOCAO
    fields = []  # Nenhum campo de formulário direto, pois o processo é tratado no form_valid
    template_name = 'adocao/adocao_confirm.html'  # Página opcional de confirmação
    success_url = reverse_lazy('pet_list')  # Redireciona para a lista de pets após o sucesso

    def dispatch(self, request, *args, **kwargs):
        # Busca o pet pela URL (usando a PK)
        self.pet = get_object_or_404(PET, pk=self.kwargs['pk'])

        # Verifica se o usuário é uma ONG (ONGs não podem adotar pets)
        if request.user.is_ong:
            raise PermissionDenied("ONGs não podem adotar pets.")

        # Verifica se o pet está disponível para adoção
        if not self.pet.disponivel_adocao:
            raise PermissionDenied("Este pet não está disponível para adoção.")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Define os valores da solicitação de adoção
        form.instance.usuario_adotante = self.request.user
        form.instance.pet = self.pet
        form.instance.ong_adocao = self.pet.dono
        form.instance.data_solicitacao = timezone.now()
        form.instance.estado_da_adocao = 'pendente'  # Estado inicial da adoção

        # Salva a solicitação de adoção
        return super().form_valid(form)
