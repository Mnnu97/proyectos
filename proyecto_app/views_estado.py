# proyecto_app/views_estado.py

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Tarea, Proyecto


def actualizar_estado_tarea(request, proyecto_id, tarea_id):
    """
    Cambia el estado de una tarea entre 'pdte' y 'completada'.
    Y actualiza automáticamente el estado del proyecto asociado.
    """
    # Obtener la tarea desde el ID proporcionado en la URL
    tarea = get_object_or_404(Tarea, id=tarea_id)

    # Validar que el proyecto_id sea coherente con la tarea
    if tarea.proyecto.id != proyecto_id:
        messages.error(request, "La tarea no pertenece al proyecto especificado.")
        return redirect('proyectos:tarea_detail_en_proyecto', proyecto_id=tarea.proyecto.id, pk=tarea.id)

    nuevo_estado = request.GET.get('estado_completado')
    estados_validos_tarea = dict(Tarea.ESTADOS_COMPLETADO).keys()

    if nuevo_estado in estados_validos_tarea:
        tarea.estado_completado = nuevo_estado
        tarea.save(update_fields=['estado_completado'])

        # Actualizar estado del proyecto
        proyecto = tarea.proyecto
        proyecto.actualizar_estado()
        proyecto.save(update_fields=['estado'])

        # Mostrar mensaje de éxito
        messages.success(
            request,
            f"Estado de '{tarea.titulo}' actualizado a: {tarea.get_estado_completado_display()}"
        )
    else:
        messages.error(request, "Estado inválido para la tarea.")

    return redirect('proyectos:tarea_detail_en_proyecto', proyecto_id=proyecto_id, pk=tarea_id)


def actualizar_estado_proyecto(request, proyecto_id):
    """
    Cambia manualmente el estado del proyecto entre pendiente / en progreso / completado.
    Útil desde el botón o formulario en la interfaz.
    """
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    nuevo_estado = request.GET.get('estado')

    # Validar que sea un estado válido
    estados_validos_proyecto = dict(Proyecto.ESTADOS).keys()

    if nuevo_estado in estados_validos_proyecto:
        proyecto.estado = nuevo_estado
        proyecto.save(update_fields=['estado'])

        # Mostrar mensaje de éxito
        messages.success(
            request,
            f"Estado del proyecto '{proyecto.nombre}' actualizado a: {proyecto.get_estado_display()}"
        )
    else:
        messages.error(request, "Estado inválido para el proyecto.")

    return redirect('proyectos:proyecto_detail', pk=proyecto.id)