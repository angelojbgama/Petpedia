from django.urls import path
from .views import PETCreateView, PETListView, PETadotarView
from django.conf.urls.static import static


urlpatterns = [
    path('cadastrar/', PETCreateView.as_view(), name='cadastrodepet'),
    path('listadepets/', PETListView.as_view(), name='pet_list'),
    path('adotar/', PETadotarView.as_view(), name='pet_adotar'),

] 
