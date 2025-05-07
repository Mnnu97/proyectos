from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Proyecto, Tarea

def actualizar_estado_proyecto(request, pk):
    """
    Cambia manualmente el estado del proyecto (pendiente/en progreso/completado)
    """
    proyecto = get_object_or_404(Proyecto, pk=pk)
    nuevo_estado = request.GET.get('estado')

    
    estados_validos = dict(Proyecto.ESTADOS).keys()

    if nuevo_estado in estados_validos:
        proyecto.estado = nuevo_estado
        proyecto.save(update_fields=['estado'])

        messages.success(request, f"Estado del proyecto '{proyecto.nombre}' actualizado a: {proyecto.get_estado_display()}")
    else:
        messages.error(request, "Estado no válido.")

    return redirect('proyectos:proyecto_detail', pk=proyecto.id)


def actualizar_estado_tarea(request, pk):
    """
    Cambia el estado de la tarea y actualiza automáticamente el estado del proyecto asociado
    """
    tarea = get_object_or_404(Tarea, pk=pk)
    nuevo_estado = request.GET.get('estado_completado')

    # Validamos que el estado sea uno de los permitidos
    estados_validos = dict(Tarea.ESTADOS_COMPLETADO).keys()

    if nuevo_estado in estados_validos:
        tarea.estado_completado = nuevo_estado
        tarea.save(update_fields=['estado_completado'])

        proyecto = tarea.proyecto
        proyecto.actualizar_estado()  # Actualizamos el estado del proyecto basado en sus tareas

        messages.success(
            request,
            f"Estado de la tarea '{tarea.titulo}' actualizado a: {tarea.get_estado_completado_display()}"
        )
    else:
        messages.error(request, "Estado de tarea no válido.")

    return redirect('proyectos:tarea_detail', pk=tarea.id)