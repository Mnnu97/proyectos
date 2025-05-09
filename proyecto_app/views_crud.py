# proyecto_app/views_crud.py

from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView,
    DeleteView
)
from django.urls import reverse_lazy, reverse
from .models import Proyecto, Tarea
from .forms import ProyectoForm, TareaForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# ========================
# 📁 VISTAS DE PROYECTOS
# ========================

@method_decorator(login_required, name='dispatch')
class ProyectoListView(ListView):
    model = Proyecto
    template_name = 'proyecto_app/proyecto_list.html'
    context_object_name = 'proyectos'
    paginate_by = 10

    def get_queryset(self):
        return Proyecto.objects.all().order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pasamos proyectos separados por estado al template (opcional)
        context['proyectos_pendientes'] = Proyecto.objects.filter(estado='pdte').order_by('nombre')
        context['proyectos_en_progreso'] = Proyecto.objects.filter(estado='en_progreso').order_by('nombre')
        context['proyectos_completados'] = Proyecto.objects.filter(estado='completado').order_by('nombre')

        return context


@method_decorator(login_required, name='dispatch')
class ProyectoDetailView(DetailView):
    model = Proyecto
    template_name = 'proyecto_app/proyecto_detail.html'
    context_object_name = 'proyecto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyecto = context['proyecto']
        context['tareas'] = Tarea.objects.filter(proyecto=proyecto).order_by('titulo')
        return context


@method_decorator(login_required, name='dispatch')
class ProyectoCreateView(CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyecto_app/proyecto_form.html'
    success_url = reverse_lazy('proyectos:proyecto_list')


@method_decorator(login_required, name='dispatch')
class ProyectoUpdateView(UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyecto_app/proyecto_form.html'
    success_url = reverse_lazy('proyectos:proyecto_list')


@method_decorator(login_required, name='dispatch')
class ProyectoDeleteView(DeleteView):
    model = Proyecto
    template_name = 'proyecto_app/proyecto_confirm_delete.html'
    success_url = reverse_lazy('proyectos:proyecto_list')


# ====================
# 📝 VISTAS DE TAREAS
# ====================

@method_decorator(login_required, name='dispatch')
class TareaListView(ListView):
    model = Tarea
    template_name = 'proyecto_app/tarea_list.html'
    context_object_name = 'tareas'

    def get_queryset(self):
        return Tarea.objects.select_related('proyecto').all().order_by('titulo')


@method_decorator(login_required, name='dispatch')
class TareaDetailView(DetailView):
    model = Tarea
    template_name = 'proyecto_app/tarea_detail.html'
    context_object_name = 'tarea'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['volver_a'] = reverse('proyectos:proyecto_list')  # ← Ahora vuelve a la lista
        return context


@method_decorator(login_required, name='dispatch')
class TareaCreateView(CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'proyecto_app/tarea_form.html'

    def get_success_url(self):
        proyecto_id = self.kwargs.get('proyecto_id') or self.request.POST.get('proyecto', None)
        if proyecto_id:
            try:
                proyecto = Proyecto.objects.get(id=proyecto_id)
                return reverse('proyectos:proyecto_detail', kwargs={'pk': proyecto.id})
            except Proyecto.DoesNotExist:
                pass
        return reverse_lazy('proyectos:proyecto_list')  # ← Ahora redirige a proyecto_list si no hay proyecto


@method_decorator(login_required, name='dispatch')
class TareaUpdateView(UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'proyecto_app/tarea_form.html'

    def get_success_url(self):
        return reverse_lazy('proyectos:proyecto_list')  # ← Siempre vuelve a la lista


@method_decorator(login_required, name='dispatch')
class TareaDeleteView(DeleteView):
    model = Tarea
    template_name = 'proyecto_app/tarea_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('proyectos:proyecto_list')  # ← Ahora siempre vuelve a proyecto_list