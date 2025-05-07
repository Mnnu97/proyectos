from django.db import models
from django.utils import timezone


class Proyecto(models.Model):
    """
    Modelo que representa un Proyecto.
    Un proyecto puede contener múltiples tareas y su estado se actualiza automáticamente según ellas.
    """

    ESTADOS = (
        ('pdte', 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('completado', 'Completado')
    )

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField(default=timezone.now)  
    fecha_fin = models.DateField(blank=True, null=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pdte'
    )

    def __str__(self):
        return self.nombre

    def get_estado_display(self):
        """
        Devuelve el valor legible del estado del proyecto.
        Ejemplo: 'En progreso' en lugar de 'en_progreso'.
        """
        return dict(Proyecto.ESTADOS).get(self.estado, "Desconocido")

    def actualizar_estado(self):
        """
        Actualiza automáticamente el estado del proyecto basándose en el estado de sus tareas.
        - Pendiente: si no tiene tareas o todas están pendientes.
        - En progreso: si hay una mezcla de completadas y pendientes.
        - Completado: si todas las tareas están completadas.
        """
        from .models import Tarea  

        total_tareas = self.tareas.count()

        if total_tareas == 0:
            self.estado = 'pdte'
        else:
            tareas_completadas = self.tareas.filter(estado_completado='completada').count()
            if tareas_completadas == 0:
                self.estado = 'pdte'
            elif tareas_completadas < total_tareas:
                self.estado = 'en_progreso'
            else:
                self.estado = 'completado'

        self.save(update_fields=['estado'])


class Tarea(models.Model):
    """
    Modelo que representa una Tarea dentro de un Proyecto.
    Cada tarea tiene un estado que afecta al estado general del proyecto.
    """

    ESTADOS_COMPLETADO = (
        ('pdte', 'Pendiente'),
        ('completada', 'Completada')
    )

    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name='tareas'
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    estado_completado = models.CharField(
        max_length=20,
        choices=ESTADOS_COMPLETADO,
        default='pdte'
    )
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo}"

    def get_estado_completado_display(self):
        """
        Devuelve el valor legible del estado de completado.
        Ejemplo: 'Completada' en lugar de 'completada'.
        """
        return dict(Tarea.ESTADOS_COMPLETADO).get(self.estado_completado, "Desconocido")