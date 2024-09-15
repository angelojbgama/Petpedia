from django.urls import path
from django.contrib.auth import views as auth_views

from .views import RegisterView, CustomPasswordResetUpdateView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, CustomLoginView, CustomUserUpdadteView, PerfilUsuarioView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('password_reset/', CustomPasswordResetUpdateView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('login/', CustomLoginView.as_view(), name='login'),  # Adiciona a URL de login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('updadteuser/', CustomUserUpdadteView.as_view(), name='update_user'),  # Adiciona a URL de login
    path('perfil/', PerfilUsuarioView.as_view(), name='usuarioviewlist'),


]
