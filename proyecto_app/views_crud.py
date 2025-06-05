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
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.contrib import messages


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
        """
        Filtra los proyectos según el rol del usuario:
        - Admin / Superuser → todos los proyectos
        - Usuario común → solo proyectos asignados
        Además permite buscar por nombre, descripción, fechas o estado
        """
        user = self.request.user
        q = self.request.GET.get('q', '').strip()

        if user.groups.filter(name='Admin').exists() or user.is_superuser:
            queryset = Proyecto.objects.all().order_by('nombre')
        else:
            queryset = Proyecto.objects.filter(usuarios=user).order_by('nombre')

        if q:
            queryset = queryset.filter(
                Q(nombre__icontains=q) |
                Q(descripcion__icontains=q) |
                Q(fecha_inicio__icontains=q) |
                Q(fecha_fin__icontains=q) |
                Q(estado__icontains=q)
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Solo Admin ve proyectos agrupados por estado
        if user.groups.filter(name='Admin').exists() or user.is_superuser:
            context['proyectos_pendientes'] = Proyecto.objects.filter(estado='pdte').order_by('nombre')
            context['proyectos_en_progreso'] = Proyecto.objects.filter(estado='en_progreso').order_by('nombre')
            context['proyectos_completados'] = Proyecto.objects.filter(estado='completado').order_by('nombre')
        else:
            context['proyectos_pendientes'] = Proyecto.objects.filter(usuarios=self.request.user, estado='pdte').order_by('nombre')
            context['proyectos_en_progreso'] = Proyecto.objects.filter(usuarios=self.request.user, estado='en_progreso').order_by('nombre')
            context['proyectos_completados'] = Proyecto.objects.filter(usuarios=self.request.user, estado='completado').order_by('nombre')

        return context


@method_decorator(login_required, name='dispatch')
class ProyectoDetailView(DetailView):
    """
    Vista detallada de un proyecto.
    Los usuarios comunes solo pueden ver proyectos donde están asignados.
    """
    model = Proyecto
    template_name = 'proyecto_app/proyecto_detail.html'
    context_object_name = 'proyecto'

    def get_queryset(self):
        """
        Filtra los proyectos según el usuario logueado
        """
        qs = super().get_queryset()
        user = self.request.user

        if user.groups.filter(name='Admin').exists() or user.is_superuser:
            return qs

        return qs.filter(usuarios=user)

    def get_context_data(self, **kwargs):
        """
        Obtiene las tareas asociadas al proyecto.
        """
        context = super().get_context_data(**kwargs)
        proyecto = context['proyecto']

        if self.request.user.groups.filter(name='Admin').exists() or self.request.user.is_superuser:
            context['tareas'] = Tarea.objects.filter(proyecto=proyecto).order_by('titulo')
        else:
            context['tareas'] = Tarea.objects.filter(proyecto=proyecto, proyecto__usuarios=self.request.user).order_by('titulo')

        return context

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, "❌ No tienes acceso a este proyecto.")
            return redirect('proyectos:inicio')


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
    paginate_by = 10

    def get_queryset(self):
        """
        Los usuarios solo ven tareas de proyectos asignados.
        Admin y Superuser ven todas las tareas.
        """
        user = self.request.user

        if user.groups.filter(name='Admin').exists() or user.is_superuser:
            return Tarea.objects.select_related('proyecto').all().order_by('titulo')

        return Tarea.objects.select_related('proyecto').filter(proyecto__usuarios=user).order_by('titulo')


@method_decorator(login_required, name='dispatch')
class TareaDetailView(DetailView):
    model = Tarea
    template_name = 'proyecto_app/tarea_detail.html'
    context_object_name = 'tarea'

    def get_queryset(self):
        """
        Restringimos edición solo a tareas de proyectos asignados al usuario
        """
        user = self.request.user
        qs = super().get_queryset()

        if user.groups.filter(name='Admin').exists() or user.is_superuser:
            return qs

        return qs.filter(proyecto__usuarios=user)

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
                context['proyecto'] = Proyecto.objects.get(pk=int(proyecto_id))
            except (ValueError, Proyecto.DoesNotExist):
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
            return reverse('proyectos:proyecto_detail', kwargs={'pk': int(proyecto_id)})
        return reverse_lazy('proyectos:inicio')


@method_decorator(login_required, name='dispatch')
class TareaUpdateView(UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'proyecto_app/tarea_form.html'

    def get_queryset(self):
        """
        Restringimos edición solo a tareas de proyectos asignados al usuario
        """
        qs = super().get_queryset()
        user = self.request.user

        if user.groups.filter(name='Admin').exists() or user.is_superuser:
            return qs

        return qs.filter(proyecto__usuarios=user)

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

        if self.request.user == obj.usuario or self.request.user.groups.filter(name='Admin').exists() or self.request.user.is_superuser:
            return obj
        else:
            raise PermissionDenied("No tienes permiso para eliminar esta tarea.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tarea = self.get_object()

        if tarea.proyecto:
            context['volver_a'] = reverse('proyectos:proyecto_detail', kwargs={'pk': tarea.proyecto.pk})
        else:
            context['volver_a'] = reverse('proyectos:inicio')

        return context

    def get_success_url(self):
        if hasattr(self, 'object') and self.object and self.object.proyecto:
            return reverse('proyectos:proyecto_detail', kwargs={'pk': self.object.proyecto.pk})
        return reverse_lazy('proyectos:inicio')