from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from .models import Proyecto, Tarea
from .forms import ProyectoForm, TareaForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required



#  Vistas para Proyectos


@method_decorator(login_required, name='dispatch')
class ProyectoListView(ListView):
    """
    Muestra una lista de todos los proyectos ordenados por nombre.
    """
    model = Proyecto
    template_name = 'proyecto_app/proyecto_list.html'
    context_object_name = 'proyectos'

    def get_queryset(self):
        return Proyecto.objects.all().order_by('nombre')


@method_decorator(login_required, name='dispatch')
class ProyectoDetailView(DetailView):
    """
    Muestra los detalles de un proyecto específico.
    """
    model = Proyecto
    template_name = 'proyecto_app/proyecto_detail.html'
    context_object_name = 'proyecto'


@method_decorator(login_required, name='dispatch')
class ProyectoCreateView(CreateView):
    """
    Vista para crear un nuevo proyecto.
    """
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyecto_app/proyecto_form.html'
    success_url = reverse_lazy('proyectos:proyecto_list')


@method_decorator(login_required, name='dispatch')
class ProyectoUpdateView(UpdateView):
    """
    Vista para editar un proyecto existente.
    """
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyecto_app/proyecto_form.html'
    success_url = reverse_lazy('proyectos:proyecto_list')


@method_decorator(login_required, name='dispatch')
class ProyectoDeleteView(DeleteView):
    """
    Vista para eliminar un proyecto.
    """
    model = Proyecto
    template_name = 'proyecto_app/proyecto_confirm_delete.html'
    success_url = reverse_lazy('proyectos:proyecto_list')



#  Vistas para Tareas

@method_decorator(login_required, name='dispatch')
class TareaListView(ListView):
    """
    Muestra una lista de todas las tareas con optimización de consultas.
    """
    model = Tarea
    template_name = 'proyecto_app/tarea_list.html'
    context_object_name = 'tareas'

    def get_queryset(self):
        return Tarea.objects.select_related('proyecto').all().order_by('titulo')


@method_decorator(login_required, name='dispatch')
class TareaDetailView(DetailView):
    """
    Muestra los detalles de una tarea específica.
    """
    model = Tarea
    template_name = 'proyecto_app/tarea_detail.html'
    context_object_name = 'tarea'


@method_decorator(login_required, name='dispatch')
class TareaCreateView(CreateView):
    """
    Vista para crear una nueva tarea.
    """
    model = Tarea
    form_class = TareaForm
    template_name = 'proyecto_app/tarea_form.html'
    success_url = reverse_lazy('proyectos:tarea_list')


@method_decorator(login_required, name='dispatch')
class TareaUpdateView(UpdateView):
    """
    Vista para editar una tarea existente.
    """
    model = Tarea
    form_class = TareaForm
    template_name = 'proyecto_app/tarea_form.html'
    success_url = reverse_lazy('proyectos:tarea_list')


@method_decorator(login_required, name='dispatch')
class TareaDeleteView(DeleteView):
    """
    Vista para eliminar una tarea.
    """
    model = Tarea
    template_name = 'proyecto_app/tarea_confirm_delete.html'
    success_url = reverse_lazy('proyectos:tarea_list')