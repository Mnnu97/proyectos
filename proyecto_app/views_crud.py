# proyecto_app/views_crud.py

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Proyecto, Tarea
from .forms import ProyectoForm, TareaForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


# ========================
# 📁 VISTAS DE PROYECTOS
# ========================

class ProyectoListView(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'proyecto_app/proyecto_list.html'
    context_object_name = 'proyectos'
    paginate_by = 10

    def get_queryset(self):
        # Si es Admin → mostrar todos los proyectos
        if self.request.user.groups.filter(name='Admin').exists():
            return Proyecto.objects.all().order_by('nombre')
        else:
            # Usuario común → solo ver sus proyectos asignados
            return Proyecto.objects.filter(usuarios=self.request.user).order_by('nombre')


# Vista Detalle de Proyecto (opcionalmente protegida)
class ProyectoDetailView(LoginRequiredMixin, DetailView):
    model = Proyecto
    template_name = 'proyecto_app/proyecto_detail.html'
    context_object_name = 'proyecto'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        # Solo Admin o usuarios asignados pueden ver el detalle del proyecto
        if not self.request.user.groups.filter(name='Admin').exists() and not obj.usuarios.filter(id=self.request.user.id).exists():
            raise PermissionDenied("No tienes acceso a este proyecto.")

        return obj


class ProyectoCreateView(CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyecto_app/proyecto_form.html'
    success_url = reverse_lazy('proyectos:inicio')  # ← Ahora lleva a inicio


# ✅ Vista nueva: Actualizar Proyecto
class ProyectoUpdateView(LoginRequiredMixin, UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyecto_app/proyecto_form.html'
    success_url = reverse_lazy('proyectos:inicio')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        # Solo Admin o usuarios asignados al proyecto pueden editar
        if not self.request.user.groups.filter(name='Admin').exists() and not obj.usuarios.filter(id=self.request.user.id).exists():
            raise PermissionDenied("No tienes permiso para editar este proyecto.")

        return obj


class ProyectoDeleteView(DeleteView):
    model = Proyecto
    template_name = 'proyecto_app/proyecto_confirm_delete.html'
    success_url = reverse_lazy('proyectos:inicio')


# ====================
# 📝 VISTAS DE TAREAS
# ====================

class TareaListView(ListView):
    model = Tarea
    template_name = 'proyecto_app/tarea_list.html'
    context_object_name = 'tareas'


class TareaDetailView(DetailView):
    model = Tarea
    template_name = 'proyecto_app/tarea_detail.html'
    context_object_name = 'tarea'


class TareaCreateView(CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'proyecto_app/tarea_form.html'

    def get_success_url(self):
        proyecto_id = self.kwargs.get('proyecto_id') or self.request.POST.get('proyecto', None)
        if proyecto_id:
            return reverse_lazy('proyectos:proyecto_detail', kwargs={'pk': proyecto_id})
        return reverse_lazy('proyectos:inicio')


class TareaUpdateView(UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'proyecto_app/tarea_form.html'

    def get_success_url(self):
        return reverse_lazy('proyectos:inicio')


class TareaDeleteView(DeleteView):
    model = Tarea
    template_name = 'proyecto_app/tarea_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('proyectos:inicio')