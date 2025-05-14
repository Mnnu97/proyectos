# proyecto_app/models.py

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # Importamos User para la relación


class Proyecto(models.Model):
    """
    Modelo que representa un Proyecto.
    Un proyecto puede contener múltiples tareas y su estado se actualiza automáticamente según ellas.
    Ahora también tiene una lista de usuarios asignados.
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
    
    # Campo ManyToMany para asignar usuarios al proyecto
    usuarios = models.ManyToManyField(
        User,
        related_name='proyectos_usuario',
        blank=True,
        help_text="Usuarios asignados a este proyecto"
    )

    def __str__(self):
        return self.nombre

    def get_estado_display(self):
        return dict(Proyecto.ESTADOS).get(self.estado, "Desconocido")

    def actualizar_estado(self):
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
    Ahora también tiene un campo para asignarla a un usuario.
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

    # Campo para asignar la tarea a un usuario
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='tareas_usuario',
        help_text="Usuario responsable de esta tarea"
    )

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
        return dict(Tarea.ESTADOS_COMPLETADO).get(self.estado_completado, "Desconocido")