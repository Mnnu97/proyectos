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
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


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

        # Pasamos proyectos separados por estado al template
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
    success_url = reverse_lazy('proyectos:inicio')


@method_decorator(login_required, name='dispatch')
class ProyectoUpdateView(UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyecto_app/proyecto_form.html'
    success_url = reverse_lazy('proyectos:inicio')


@method_decorator(login_required, name='dispatch')
class ProyectoDeleteView(DeleteView):
    model = Proyecto
    template_name = 'proyecto_app/proyecto_confirm_delete.html'
    success_url = reverse_lazy('proyectos:inicio')


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
        tarea = self.get_object()
        
        if tarea.proyecto:
            context['volver_a'] = reverse('proyectos:proyecto_detail', kwargs={'pk': tarea.proyecto.pk})
        else:
            context['volver_a'] = reverse('proyectos:inicio')
        
        return context


@method_decorator(login_required, name='dispatch')
class TareaCreateView(CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'proyecto_app/tarea_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        proyecto_id = self.kwargs.get('proyecto_id') or self.request.GET.get('proyecto') or self.request.POST.get('proyecto')

        if proyecto_id:
            try:
                context['proyecto'] = Proyecto.objects.get(pk=proyecto_id)
            except Proyecto.DoesNotExist:
                context['proyecto'] = None
        else:
            context['proyecto'] = None

        return context

    def form_valid(self, form):
        proyecto_id = self.kwargs.get('proyecto_id') or self.request.POST.get('proyecto', None)

        if not proyecto_id:
            raise PermissionDenied("No se ha especificado un proyecto.")

        proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
        form.instance.proyecto = proyecto
        form.instance.usuario = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        proyecto_id = self.kwargs.get('proyecto_id') or self.request.POST.get('proyecto', None)
        if proyecto_id:
            return reverse('proyectos:proyecto_detail', kwargs={'pk': proyecto_id})
        return reverse_lazy('proyectos:inicio')


@method_decorator(login_required, name='dispatch')
class TareaUpdateView(UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'proyecto_app/tarea_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tarea = self.get_object()

        if tarea and tarea.proyecto:
            context['proyecto'] = tarea.proyecto
            context['volver_a'] = reverse('proyectos:proyecto_detail', kwargs={'pk': tarea.proyecto.pk})
        else:
            context['volver_a'] = reverse('proyectos:inicio')

        return context

    def get_success_url(self):
        if hasattr(self, 'object') and self.object and self.object.proyecto:
            return reverse('proyectos:proyecto_detail', kwargs={'pk': self.object.proyecto.pk})
        return reverse_lazy('proyectos:inicio')


@method_decorator(login_required, name='dispatch')
class TareaDeleteView(DeleteView):
    model = Tarea
    template_name = 'proyecto_app/tarea_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if not self.request.user.groups.filter(name='Admin').exists():
            raise PermissionDenied("Solo los administradores pueden eliminar tareas.")

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tarea = self.get_object()

        if tarea and tarea.proyecto:
            context['volver_a'] = reverse('proyectos:proyecto_detail', kwargs={'pk': tarea.proyecto.pk})
        else:
            context['volver_a'] = reverse('proyectos:inicio')

        return context

    def get_success_url(self):
        if hasattr(self, 'object') and self.object and self.object.proyecto:
            return reverse('proyectos:proyecto_detail', kwargs={'pk': self.object.proyecto.pk})
        return reverse_lazy('proyectos:inicio')