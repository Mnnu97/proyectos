from django.urls import path
from .views import home, perfil  # Importa ambas vistas
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('perfil/', perfil, name='perfil'),  # Ahora 'perfil' está definido
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]