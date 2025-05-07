from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Tarea, Proyecto


def actualizar_estado_tarea(request, pk):
    """
    Cambia el estado de una tarea entre 'pdte' y 'completada'.
    Y actualiza automáticamente el estado del proyecto asociado.
    """
    tarea = get_object_or_404(Tarea, pk=pk)
    nuevo_estado = request.GET.get('estado_completado')

    estados_validos = dict(Tarea.ESTADOS_COMPLETADO).keys()

    if nuevo_estado in estados_validos:
        tarea.estado_completado = nuevo_estado
        tarea.save(update_fields=['estado_completado'])

        
        proyecto = tarea.proyecto
        proyecto.actualizar_estado()  
        messages.success(
            request,
            f"Estado de '{tarea.titulo}' actualizado a: {tarea.get_estado_completado_display()}"
        )
    else:
        messages.error(request, "Estado inválido para la tarea.")

    return redirect('proyectos:tarea_detail', pk=tarea.pk)


def actualizar_estado_proyecto(request, pk):
    """
    Cambia manualmente el estado del proyecto entre: pendiente / en progreso / completado.
    Útil desde el detalle del proyecto o desde un botón en la interfaz.
    """
    proyecto = get_object_or_404(Proyecto, pk=pk)
    nuevo_estado = request.GET.get('estado')

    estados_validos = dict(Proyecto.ESTADOS).keys()

    if nuevo_estado in estados_validos:
        proyecto.estado = nuevo_estado
        proyecto.save(update_fields=['estado'])

        messages.success(
            request,
            f"Estado del proyecto '{proyecto.nombre}' actualizado a: {proyecto.get_estado_display()}"
        )
    else:
        messages.error(request, "Estado inválido para el proyecto.")

    return redirect('proyectos:proyecto_detail', pk=proyecto.pk)