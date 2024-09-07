from django.urls import path
from .views import InicioPageView, SobrePageView , CaracteristicasPageView , TimePageView , TestemUnhosPageView , FAQPageView , ContatoPageView

urlpatterns = [
    path("", InicioPageView.as_view(), name="index"),
    path("about/", SobrePageView.as_view(), name="about"),
    path("features/", CaracteristicasPageView.as_view(), name="caracteristicas"),
    path("team/", TimePageView.as_view(), name="time"),
    path("testimonies/", TestemUnhosPageView.as_view(), name="testemunhos"),
    path("faq/", FAQPageView.as_view(), name="faq"),
    path("contact/", ContatoPageView.as_view(), name="contato"),
]
