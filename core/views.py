from django.shortcuts import render
from django.views.generic import TemplateView
from core.forms import ContatoForm
from django.views.generic.edit import FormView


# Create your views here.

_CONSTANTE_TEMPLATE_NAME_INICIO = "pages/index.html"
_CONSTANTE_TEMPLATE_NAME_SOBRE = "pages/about.html"




class InicioPageView(FormView, TemplateView):
    '''
    View para renderizar a page HOME e processar o formulário de contato
    '''
    template_name = _CONSTANTE_TEMPLATE_NAME_INICIO  # Substitua pelo nome do seu template
    form_class = ContatoForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_aba'] = 'Verde Fresco: O App que Traz a Natureza até Você!'
        return context
    
    def form_valid(self, form):
        nome = form.cleaned_data['nome']
        email = form.cleaned_data['email']
        assunto = form.cleaned_data['assunto']
        mensagem = form.cleaned_data['mensagem']
        
        # Mensagem de sucesso
        mensagem_sucesso = f"Obrigado, {nome}! Sua mensagem foi recebida."
        
        # Adiciona a mensagem de sucesso ao contexto e renderiza o template
        return self.render_to_response(self.get_context_data(
            form=form,
            mensagem_sucesso=mensagem_sucesso
        ))
    
    def form_invalid(self, form):
        # Se o formulário for inválido, apenas renderiza o template com erros
        return self.render_to_response(self.get_context_data(
            form=form
        ))

class SobrePageView(TemplateView):
    '''
    View para renderizar a page SOBRE
    '''
    template_name = _CONSTANTE_TEMPLATE_NAME_SOBRE
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_aba'] = 'Sobre a Verde Fresco!'
        return context
    
