# proyecto_app/views_inicio.py

from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class PaginaInicioView(TemplateView):
    template_name = 'proyecto_app/inicio.html'