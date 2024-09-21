from django.urls import path
from .views import AtualizarAdocaoView, SolicitacoesAdocaoView, AdocaoCreateView

urlpatterns = [
    path('adocao/<int:pk>/atualizar/', AtualizarAdocaoView.as_view(), name='atualizar_adocao'),
    path('adocao/solicitacoes/', SolicitacoesAdocaoView.as_view(), name='solicitacoes_adocao'),
    path('pets/<int:pk>/adotar/', AdocaoCreateView.as_view(), name='solicitar_adocao'),

]
