from django.urls import path
from .views import InicioPageView, SobrePageView

urlpatterns = [
    path("", InicioPageView.as_view(), name="index"),
    path("about/", SobrePageView.as_view(), name="about"),

]
